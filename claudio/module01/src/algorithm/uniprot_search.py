import concurrent.futures
import socket
import sys
import pandas as pd
import requests as r

from claudio.utils.utils import verbose_print, round_self


def do_uniprot_search(data: pd.DataFrame, tmp_filepath: str,
                      verbose_level: int):
    """
    Retrieve full uniprot sequences and IDs if not given
    
    Parameters
    ----------
    data : pd.DataFrame,
    tmp_filepath : str,
    verbose_level : int

    Returns
    -------
    data : pd.DataFrame
    """

    unip_ids_a = data["unip_id_a"].unique().tolist()
    unip_ids_b = data["unip_id_b"].unique().tolist()
    unip_ids = list(set(unip_ids_a + unip_ids_b))
    already_searched = query_uniprot(unip_ids, verbose_level)
    # retrieve sequences from uniprot entries
    data["seq_a"] = search_uniprot(data, verbose_level, already_searched,
                                   site='a')
    data["seq_b"] = search_uniprot(data, verbose_level, already_searched,
                                   site='b')

    # save results in temporary save file (can be used on rerun, instead of
    # searching results again)
    data[["seq_a", "seq_b"]].to_csv(tmp_filepath, index=False)

    return data


def search_uniprot(data: pd.DataFrame, verbose_level: int, already_searched,
                   site='a'):
    """
    search uniprot database for sequences

    Parameters
    ----------
    data : pd.DataFrame,
    verbose_level : int,
    already_searched : dict[str,list[str]],
    site : str

    Returns
    -------
    seq : list[str],
    already_searched : dict[str,list[str]]
    """
    #TODO why is site defaulted?

    seqs = [[]for _ in range(len(data.index))]

    # Sort uniprot search result sequences to datapoints
    ind = 0
    def retrieve_seqs_task(i,row):
        unip_id = row[f"unip_id_{site}"]
        # If search failed, or no uniprot id was given, return nan
        if pd.isna(unip_id) or already_searched[unip_id] is None or not already_searched[unip_id]:
            return i, float('nan')
        # Else, parse through all possible sequences discovered
        else:
            result = already_searched[unip_id]
            fitting_seq_found = False
            seq = ''
            if len(result) > 1:
                # Check for each sequence whether both peptides were
                # discovered in the sequences
                for seq in result:
                    peptide_arg = (row["pep_a"] in seq) and (row["pep_b"] in seq) \
                        if row["unip_id_a"] == row["unip_id_b"] else (row[f"pep_{site}"] in seq)
                    # If a fitting sequences, containing both peptides was
                    # found set argument to True
                    if peptide_arg:
                        fitting_seq_found = True
                        break
            # If argument is not True, return the first discovered sequence
            if not fitting_seq_found:
                seq = result[0]
            # Add final sequence to list
            return i, seq

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(retrieve_seqs_task, i, row):
                   (i,row) for i, row in data.iterrows()}

        for future in concurrent.futures.as_completed(futures):
            try:
                i, seq = future.result()
                seqs[i] = seq
                ind += 1
                progress = round_self(ind * 100 / len(data.index), 2)
                verbose_print(f"\r\tSite_{site}:[{progress}%]", 1,
                              verbose_level, end='')
                del futures[future]
            except Exception as e:
                print(e)
    verbose_print("", 1, verbose_level)

    return seqs


def query_uniprot(unip_ids: list, verbose_level: int):
    """
    Query the uniprot database for sequences

    Parameters
    ----------

    unip_ids : list[str],
    already_searched : dict[str,list[str]],
    verbose_level : int

    Returns
    -------
    already_searched : dict[str,list[str]]
    """

    already_searched = {}

    # retrieve uniprot sequences for all uniquely discovered uniprot ids
    def query_task(unip_id):
        # if search for unip id has not been performed yet, do so, and add it
        # to already_searched dictionary
        if unip_id not in already_searched or already_searched[unip_id] is None:
            url = f"https://rest.uniprot.org/uniprotkb/search?format=fasta&query={unip_id}"
            try:
                url_return_text = r.get(url,timeout=60).text
                return_failed = "Error encountered when streaming data. Please try again later." in url_return_text
                # if successful continue
                if not return_failed:
                    result = [''.join(x.split('\n')[1:])
                              for x in url_return_text.split('>') if x]
                    # remove empty strings, should not occur if uniprot
                    # fasta-files are properly formatted, added due to a '>'
                    # which was included in the header of the fasta file
                    result = [part.strip() for part in result if part.strip()]
                    already_searched[unip_id] = result
                # else print error message and raise ValueError
                else:
                    verbose_print(f"\tWarning! UniProt API call failed for UniProt_ID={unip_id}.\n\tReturned message: "
                                  f"{url_return_text}", 2, verbose_level)
                    already_searched[unip_id] = None
            except (r.exceptions.Timeout, ConnectionError, socket.gaierror,
                    r.exceptions.ConnectionError) as e:
                print("No connection to UniProt API possible. Please try again later.")
                print(e)
                sys.exit(1)
            except ValueError:
                print("Error! Encountered at least one faulty return from the UniProt database.")
                sys.exit(1)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(query_task, id): id for id in unip_ids}

        for future in concurrent.futures.as_completed(futures):
            try:
                if future.result() is not None:
                    _ = future.result()
                del futures[future]
            except Exception as e:
                print(e)

    return already_searched
