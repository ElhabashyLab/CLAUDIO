from io import StringIO
import requests as r
import time
import socket
import pandas as pd
import os
import concurrent.futures

from claudio.utils.utils import verbose_print, round_self


def structure_search(data: pd.DataFrame, search_tool: str, e_value: float, query_id: float, coverage: float, tmp_filepath: str, 
                     blast_bin: str | None, blast_db: str, hhsearch_bin: str | None, hhsearch_db: str, verbose_level: int):
    """
    Perform either hhsearch or blastp search for any unique uniprot entry in rcsb database and retrieve the best
    results, and save all entries for which no sufficient result was returned to retrieve these from alphafold
    database later

    Parameters
    ----------
    data : pd.DataFrame,
    search_tool : str,
    e_value : float,
    query_id : float,
    coverage : float,
    tmp_filepath : str,
    blast_bin : str | None,
    blast_db : str,
    hhsearch_bin : str | None,
    hhsearch_db : str,
    verbose_level : int

    Returns
    -------
    data : pd.DataFrame
    """
    #TODO contains legacy code for hhsearch

    not_found = []
    ind = 0

    # Save each already search uniprot entries' id and result for quick retrieval if reencountered (instead of repeating
    # the same search)
    already_searched = {}
    unique_prots = list(set(zip(data.unip_id_a, data.seq_a)) | set(zip(data.unip_id_b, data.seq_b)))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(perform_search, unip_id, seq, search_tool, e_value, query_id, coverage, tmp_filepath,
                                                   blast_bin, blast_db, hhsearch_bin, hhsearch_db): 
                                                   (unip_id,seq) for unip_id,seq in unique_prots}

        for future in concurrent.futures.as_completed(futures):
            try:
                if future.result() is not None:
                    best_results, pdb_id, chain, unip_id = future.result()
                    already_searched[unip_id] = (pdb_id, chain, ' '.join(best_results))
                    ind += 1
                    verbose_print(f"\r\t[{round_self((ind * 100) / len(unique_prots), 2)}%]", 1, verbose_level, end='')
                del futures[future]
            except Exception as e:
                print(e)

    # Write the results to the data frame
    verbose_print("", 1, verbose_level)            
    verbose_print(f"Write {search_tool} results", 2, verbose_level)
    ind = 0
    def write_res_task(i, row):
        if already_searched[row["unip_id_a"]][2] and already_searched[row["unip_id_b"]][2]:
            # Sort results into dataset
            _, _, best_results_a = already_searched[row["unip_id_a"]]
            _, _, best_results_b = already_searched[row["unip_id_b"]]

            # Join search results
            results_a = {result.split('_')[0]: '_'.join(result.split('_')[1:])
                         for result in best_results_a.split(' ')}
            results_b = {result.split('_')[0]: '_'.join(result.split('_')[1:])
                         for result in best_results_b.split(' ')}
            intersect_results = {key: (results_a[key], results_b[key])
                                 for key in [key for key in results_a.keys() if key in results_b.keys()]}

            # Add results to dataset
            if intersect_results:
                pdb_id = list(intersect_results.keys())[0]
                chain_a, chain_b = intersect_results[pdb_id]
                all_results = ' '.join([f"{key}_{value[0]}|_{value[1]}" for key, value in intersect_results.items()])
                new_cols = [pdb_id, chain_a, chain_b, all_results]
                data.loc[i,["pdb_id","chain_a","chain_b","all_results"]] = new_cols
        else:
            not_found.append(i)

        return

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(write_res_task, i, row): (i, row) for i, row in data.iterrows()}

        for future in concurrent.futures.as_completed(futures):
            try:
                ind += 1
                verbose_print(f"\r\t[{round_self((ind * 100) / len(data.index), 2)}%]", 1, verbose_level, end='')
                del futures[future]
            except Exception as e:
                print(e)
    verbose_print("", 1, verbose_level)

    # Save results to temporary save file
    data[["pdb_id", "chain_a", "chain_b", "all_results"]].to_csv(tmp_filepath, index=False)

    # Print ids of entries which were not found in rcsb database (will be retrieved from alphafold database instead)
    if not data[data.unip_id_a == data.unip_id_b].empty:
        not_found_proteins = pd.concat([data.loc[not_found].unip_id_a, data.loc[not_found].unip_id_b]).unique()
        verbose_print(f"\tProteins which yielded no results from RCSB database (will be retrieved from AlphaFold "
                      f"(n = {len(not_found_proteins)})): {not_found_proteins}", 2, verbose_level)

    return data


def perform_search(unip_id: str, sequence: str, search_tool: str, e_value: float, query_id: float, coverage: float, tmp_filepath: str, 
                   blast_bin: str | None, blast_db: str, hhsearch_bin: str | None, hhsearch_db: str):
    """
    Perform either hhsearch or blastp search for unique uniprot entry in rcsb database and return possible results

    Parameters
    ----------
    unip_id : str,
    sequence : str,
    search_tool : str,
    e_value : float,
    query_id : float,
    coverage : float,
    temp_path : str,
    blast_bin : str | None,
    blast_db : str,
    hhsearch_bin : str | None,
    hhsearch_db : str

    Returns
    -------
    best_result : list[str],
    pdb_id : str | None,
    chain : str | None,
    unip_id : str
    """

    # Save uniprot sequence in a temporary fasta file for search tool commandline call
    # (override before each new search)
    temp_path = '/'.join(tmp_filepath.split('/')[:-1]) + '/'
    with open(f"{temp_path}tmp{unip_id}.fasta", 'w') as tmp_file:
        tmp_file.write(f">{unip_id}\n{sequence}\n")
        tmp_file.close()
        search_results = []

        # Perform search with either hhsearch or blastp (Note: Watch environmental variables $BLASTDB,
        # $HHDB to be set according to instructions found in README.md)
        if search_tool == "blastp":
            blast_call = "blastp" if blast_bin is None else f"{blast_bin}blastp"
            command = f"\"{blast_call}\" -query \"{temp_path}tmp{unip_id}.fasta\" -db \"{blast_db}pdbaa\" " \
                      f"-evalue {e_value} -outfmt \"6 delim=, saccver pident qcovs evalue\""
            res = pd.read_csv(StringIO(os.popen(command).read()), sep=',', names=["pdb", "ident", "cov", "eval"],
                              dtype={"pdb": str, "ident": float, "cov": float, "eval": float})
            search_results = res[(res["ident"] >= query_id) & (res["cov"] >= coverage)]
            search_results = search_results.loc[:, "pdb"].tolist()

        elif search_tool == "hhsearch":
            hhsearch_call = "hhsearch" if hhsearch_bin is None else f"{hhsearch_bin}hhsearch"
            command = f"\"{hhsearch_call}\" -i \"{temp_path}tmp{unip_id}.fasta\" -d \"{hhsearch_db}pdb70\" -e {e_value} " \
                      f"-qid {query_id} -cov {coverage} -blasttab \"{temp_path}tmp{unip_id}.hhr\" -v 0 -cpu 20"
            os.system(command)
            search_results = [line.split('\t')[1]
                              for line in open(f"{temp_path}tmp{unip_id}.hhr", 'r').read().split('\n')
                              if line.split('\t')[0] == unip_id][:20]

        # Search identical Chain IDs for (inter) cross-links
        chains = [retrieve_identical_chain_ids(res.split('_')[0], res.split('_')[1], 5)
                  for res in search_results]
        search_results = [f"{res.split('_')[0]}_{'_'.join(chains[index])}"
                          if chains[index] is not None else res
                          for index, res in enumerate(search_results)]

        # If search successful, save result to respective container lists, and full result to
        # already_searched_res with specified chain
        if search_results and ('_' in search_results[0]):
            pdb_id = search_results[0].split('_')[0]
            chain = search_results[0].split('_')[1]
        # Elif no chain specified
        elif search_results:
            pdb_id = search_results[0][:4]
            chain = '-'
        # Else, search was unsuccessful
        else:
            pdb_id = None
            chain = None

    return search_results, pdb_id, chain, unip_id


def retrieve_identical_chain_ids(pdb_id: str, chain: str, max_try: int):
    """
    Access RCSB fastas to check for identical chain identifiers based on sequence

    Parameters
    ----------
    pdb_id : str,
    chain : str,
    max_try : int

    Returns
    -------
    new_chains : list[str] | None
    """

    num_connect_error = 0
    for _ in range(max_try):
        try:
            # on successful fasta download, attempt to find identical chain ids
            fasta_content = ''.join(r.get(f"https://www.rcsb.org/fasta/entry/{pdb_id}").text)
            chain_infos = [segment
                           for line in fasta_content.split('\n')
                           if line.startswith('>')
                           for segment in line.split('|')
                           if segment.startswith("Chain")]
            new_chains = [info.replace("Chains ", '').replace("Chain ", '')
                          for info in chain_infos]
            new_chains = [[sub_chain.split("[auth")[1].split(']')[0].replace(' ', '')
                           if "[auth" in sub_chain else sub_chain.replace(' ', '')
                           for sub_chain in new_chain.split(',')]
                          for new_chain in new_chains]
            new_chains = [chain_list for chain_list in new_chains if chain in chain_list][0]
            return new_chains
        # Retry on timeout after short sleep
        except (r.exceptions.Timeout, TimeoutError):
            time.sleep(1)
        # Retry if no connection to database possible
        except (ConnectionError, socket.gaierror, r.exceptions.ConnectionError) as e:
            num_connect_error += 1
            time.sleep(1)
        # If chain was not found immediately stop search
        except IndexError:
            break

    if num_connect_error > 0:
        print("No connection to RCSB API possible. Please try again later.")
    return None
