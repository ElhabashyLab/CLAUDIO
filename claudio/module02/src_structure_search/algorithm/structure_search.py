from io import StringIO
import requests as r
import time
import socket
import pandas as pd
import os
import platform


from utils.utils import verbose_print, round_self


def structure_search(data, search_tool, e_value, query_id, coverage, tmp_filepath, blast_bin, blast_db, hhsearch_bin,
                     hhsearch_db, verbose_level):
    # Perform either hhsearch or blastp search for any unique uniprot entry in rcsb database and retrieve the best
    # results, and save all entries for which no sufficient result was returned to retrieve these from alphafold
    # database later
    #
    # input data: pd.DataFrame, search_tool: str, e_value: float, query_id: float, coverage: float, tmp_filepath: str,
    # blast_bin: str/None, blast_db: str, hhsearch_bin: str/None, hhsearch_db: str, verbose_level: int
    # return dataset: pd.DataFrame

    # Container lists for search results
    not_found = []
    ind = 0

    # Save each already search uniprot entries' id and result for quick retrieval if reencountered (instead of repeating
    # the same search)
    already_searched = {}

    for i, row in data.iterrows():
        # If encountered a new uniprot entry at site_a, do search and save results
        if row["unip_id_a"] not in already_searched.keys():
            best_results, pdb_id, chain = perform_search(row, 'a', search_tool, e_value, query_id, coverage,
                                                         tmp_filepath, blast_bin, blast_db, hhsearch_bin, hhsearch_db)
            already_searched[row["unip_id_a"]] = (pdb_id, chain, ' '.join(best_results))
        # If encountered a new uniprot entry at site_b, do search and save results
        if row["unip_id_b"] not in already_searched.keys():
            best_results, pdb_id, chain = perform_search(row, 'b', search_tool, e_value, query_id, coverage,
                                                         tmp_filepath, blast_bin, blast_db, hhsearch_bin, hhsearch_db)
            already_searched[row["unip_id_b"]] = (pdb_id, chain, ' '.join(best_results))

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
                data.loc[i, "pdb_id"] = pdb_id
                data.loc[i, "chain_a"] = chain_a
                data.loc[i, "chain_b"] = chain_b
                data.loc[i, "all_results"] = ' '.join([f"{key}_{value[0]}|_{value[1]}"
                                                       for key, value in intersect_results.items()])
        else:
            not_found.append(i)
        ind += 1
        verbose_print(f"\r\t[{round_self(ind * 100 / len(data.index), 2)}%]", 1, verbose_level, end='')
    verbose_print("", 1, verbose_level)

    # Save results to temporary save file
    data[["pdb_id", "chain_a", "chain_b", "all_results"]].to_csv(tmp_filepath, index=False)

    # Print ids of entries which were not found in rcsb database (will be retrieved from alphafold database instead)
    if not data[data.unip_id_a == data.unip_id_b].empty:
        not_found_proteins = pd.concat([data.loc[not_found].unip_id_a, data.loc[not_found].unip_id_b]).unique()
        verbose_print(f"\tProteins which yielded no results from RCSB database (will be retrieved from AlphaFold "
                      f"(n = {len(not_found_proteins)})): {not_found_proteins}", 2, verbose_level)

    return data


def perform_search(data, site, search_tool, e_value, query_id, coverage, tmp_filepath, blast_bin, blast_db,
                   hhsearch_bin, hhsearch_db):
    # Perform either hhsearch or blastp search for unique uniprot entry in rcsb database and return possible results
    #
    # input data: pd.Series, site: str, search_tool: str, e_value: float, query_id: float,
    # coverage: float, temp_path: str, blast_bin: str/None, blast_db: str, hhsearch_bin: str/None, hhsearch_db: str
    # return best_result: list(str), pdb_id: str/None, chain: str/None

    # Save uniprot sequence in a temporary fasta file for search tool commandline call
    # (override before each new search)
    temp_path = '/'.join(tmp_filepath.split('/')[:-1]) + '/'
    with open(f"{temp_path}tmp{data.name}.fasta", 'w') as tmp_file:
        tmp_file.write(f">{data[f'unip_id_{site}']}\n{data[f'seq_{site}']}\n")
        tmp_file.close()
        search_results = []

        # Perform search with either hhsearch or blastp (Note: Watch environmental variables $BLASTDB,
        # $HHDB to be set according to instructions found in README.md)
        if search_tool == "blastp":
            blast_call = "blastp" if blast_bin is None else f"{blast_bin}blastp"
            blast_call = f"& \"{blast_call}\"" if platform.system() == "Windows" else blast_call.replace(' ', '\\ ')
            command = f"{blast_call} -query \"{temp_path}tmp{data.name}.fasta\" -db \"{blast_db}pdbaa\" " \
                      f"-evalue {e_value} -outfmt \"6 delim=, saccver pident qcovs evalue\""
            res = pd.read_csv(StringIO(os.popen(command).read()), sep=',', names=["pdb", "ident", "cov", "eval"],
                              dtype={"pdb": str, "ident": float, "cov": float, "eval": float})
            search_results = res[(res["ident"] >= query_id) & (res["cov"] >= coverage)]
            search_results = search_results.loc[:, "pdb"].tolist()

        elif search_tool == "hhsearch":
            hhsearch_call = "hhsearch" if hhsearch_bin is None else f"{hhsearch_bin}hhsearch"
            hhsearch_call = f"& \"{hhsearch_call}\"" if platform.system() == "Windows" else hhsearch_call.replace(' ', '\\ ')
            command = f"{hhsearch_call} -i \"{temp_path}tmp{data.name}.fasta\" -d \"{hhsearch_db}pdb70\" -e {e_value} " \
                      f"-qid {query_id} -cov {coverage} -blasttab \"{temp_path}tmp{data.name}.hhr\" -v 0 -cpu 20"
            os.system(command)
            search_results = [line.split('\t')[1]
                              for line in open(f"{temp_path}tmp{data.name}.hhr", 'r').read().split('\n')
                              if line.split('\t')[0] == data[f'unip_id_{site}']][:20]

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

    return search_results, pdb_id, chain


def retrieve_identical_chain_ids(pdb_id, chain, max_try):
    # Access RCSB fastas to check for identical chain identifiers based on sequence
    #
    # input pdb_id: str, chain: str, max_try: int
    # return new_chains: list(str)/None

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
