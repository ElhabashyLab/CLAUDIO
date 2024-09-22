import socket
import sys
import pandas as pd
import requests as r

from claudio.utils.utils import verbose_print, round_self


def do_uniprot_search(data: pd.DataFrame, tmp_filepath: str, verbose_level: int):
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

    # retrieve sequences from uniprot entries
    data["seq_a"], search_result_dict = search_uniprot(data, verbose_level, site='a')
    data["seq_b"], _ = search_uniprot(data, verbose_level, already_searched=search_result_dict, site='b')

    # save results in temporary save file (can be used on rerun, instead of searching results again)
    data[["seq_a", "seq_b"]].to_csv(tmp_filepath, index=False)

    return data


def search_uniprot(data: pd.DataFrame, verbose_level: int, already_searched={}, site='a'):
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
    #TODO why is already_searched and site defaulted?

    seqs = []

    # create list of unique uniprot ids
    unip_ids = data[f"unip_id_{site}"].unique().tolist()

    # retrieve uniprot sequences for all uniquely discovered uniprot ids
    for id in unip_ids:
        # if search for unip id has not been performed yet, do so, and add it to already_searched dictionary
        if id not in already_searched.keys() or already_searched[id] is None:
            url = f"https://rest.uniprot.org/uniprotkb/search?format=fasta&query={id}"
            try:
                url_return_text = r.get(url).text
                return_failed = "Error encountered when streaming data. Please try again later." in url_return_text
                # if successful continue
                if not return_failed:
                    result = [''.join(x.split('\n')[1:]) for x in url_return_text.split('>') if x]
                    already_searched[id] = result
                # else print error message and raise ValueError
                else:
                    verbose_print(f"\tWarning! UniProt API call failed for UniProt_ID={id}.\n\tReturned message: "
                                  f"{url_return_text}", 2, verbose_level)
                    already_searched[id] = None
            except (r.exceptions.Timeout, ConnectionError, socket.gaierror, r.exceptions.ConnectionError) as e:
                print("No connection to UniProt API possible. Please try again later.")
                print(e)
                sys.exit()
            except ValueError:
                print("Error! Encountered at least one faulty return from the UniProt database.")
                sys.exit()

    # Sort uniprot search result sequences to datapoints
    ind = 0
    for _, row in data.iterrows():
        id = row[f"unip_id_{site}"]
        ind += 1
        verbose_print(f"\r\tSite_{site}:[{round_self(ind * 100 / len(data.index), 2)}%]", 1, verbose_level, end='')
        # If search failed, or no uniprot id was given, return nan
        if pd.isna(id) or already_searched[id] is None or not already_searched[id]:
            seqs.append(float('nan'))
        # Else, parse through all possible sequences discovered
        else:
            result = already_searched[id]
            fitting_seq_found = False
            seq = ''
            if len(result) > 1:
                # Check for each sequence whether both peptides were discovered in the sequences
                for seq in result:
                    peptide_arg = (row["pep_a"] in seq) and (row["pep_b"] in seq) \
                        if row["unip_id_a"] == row["unip_id_b"] else (row[f"pep_{site}"] in seq)
                    # If a fitting sequences, containing both peptides was found set argument to True
                    if peptide_arg:
                        fitting_seq_found = True
                        break
            # If argument is not True, return the first discovered sequence
            if not fitting_seq_found:
                seq = result[0]
            # Add final sequence to list
            seqs.append(seq)
    verbose_print("", 1, verbose_level)

    return seqs, already_searched
