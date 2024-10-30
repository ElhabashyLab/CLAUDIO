import os
import socket
import time
import requests as r
import pandas as pd
import concurrent.futures

from claudio.utils.utils import verbose_print, round_self


def download_wrapper(filename: str, url: str, dataset: pd.DataFrame, pdb_id: str, chain: str, chain_b: str,pdb_file: str):
    """
    Downloads a pdb-file from a given url

    Parameters
    ----------
    filename : str,
    url : str,
    dataset : pd.DataFrame,
    pdb_id : str,
    chain : str,
    chain_b : str,
    pdb_file : str

    Returns 
    -------
    pdb_id : str,
    chain : str,
    chain_b : str,
    pdb_file : str,
    
    """
    if filename not in dataset["path"]:
        pdb_file = download_pdb_from_db(url, 0, 5)
        if pdb_file is None:
            return '-','-','-','-'
    return pdb_id, chain, chain_b, pdb_file

def download_pdbs(dataset:pd.DataFrame, search_tool: str, res_cutoff: float, output_directory: str, verbose_level: int):
    """
    Download pdb files either from RCSB or AlphaFold database (depending on earlier hhsearch or blastp search) into
    output directory

    Parameters
    ----------
    dataset : pd.DataFrame,
    search_tool : str,
    res_cutoff : float,
    output_directory : str,
    verbose_level : int,

    Returns
    -------
    dataset : pd.DataFrame
    """

    ind = 0
    
    # clear output directory of old pdb file results
    clear_output_dir(search_tool, output_directory)
    # Download pdb files for each datapoint
    def download_task(i,row, dataset):
        # Iterate over results
        for j, res in enumerate((row["all_results"] + ' ').split(' ')):

            pdb_id = res.split('_')[0]
            chain = '_'.join(res.split('|')[0].split('_')[1:]) if pdb_id else '-'
            chain_b = '_'.join(res.split('|')[1].split('_')[1:]) if pdb_id else '-'
            pdb_file = ''

            # If pdb entry found in RCSB, download from there
            if pdb_id:
                filename = f"{output_directory}{search_tool}_{pdb_id}.pdb"
                url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
            else:

                # if intra crosslink, download from AlphaFold
                if row.unip_id_a == row.unip_id_b:
                        
                        # Create custom alphafold pdb filename
                        pdb_id = f"af{row.unip_id_a}"
                        chain = 'A'
                        chain_b = 'A'
                        filename = f"{output_directory}{search_tool}_{pdb_id}.pdb"
                        url = f"https://alphafold.ebi.ac.uk/files/AF-{row.unip_id_a}-F1-model_v4.pdb"
                
                # no download possible
                else:
                    continue
            
            pdb_id, chain, chain_b, pdb_file = download_wrapper(filename, url, dataset, pdb_id, chain, chain_b,pdb_file)

            # Check whether method and resolution are accepted, return respective bool, method and resolution
            method_accepted, method, resolution = accept_resolution_method(pdb_file, pdb_id, res_cutoff)

            # Save method and resolution for best structure search result
            if j == 0:
                # Add method and resolution to dataset
                dataset.loc[i, ["best_res_pdb_method","best_res_pdb_resolution"]] = [method, resolution]

            # Stop Iteration of results if result gets accepted
            if method_accepted:
                not_nmr_alphafold = ("NMR" not in method) and ("ALPHAFOLD" not in method)
                no_nmr_found_yet = "NMR" not in dataset.loc[i, "pdb_method"]
                if not_nmr_alphafold or no_nmr_found_yet:
                    # Update pdb_id and chain in dataset, add filename to path and method,resolution to dataset
                    dataset.loc[i,["pdb_id","chain_a","chain_b","path","pdb_method","pdb_resolution"]] = [pdb_id,chain,chain_b,
                                                                                                        filename,method,resolution]

                    # Save pdb text to new pdb file with custom name
                    if (not os.path.exists(filename)) and (pdb_file is not None):
                        with open(filename, 'w') as f:
                            f.write(pdb_file)
                if "NMR" not in method:
                    break
        return dataset
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(download_task, i, row, dataset): (i,row) for i, row in dataset.iterrows()}

        for future in concurrent.futures.as_completed(futures):
            try:
                if future.result() is not None:
                    dataset = future.result()
                    ind += 1
                    verbose_print(f"\r\t[{round_self((ind * 100) / len(dataset.index), 2)}%]", 1, verbose_level, end='')
                    del futures[future]
            except Exception as e:
                print(e)

    verbose_print("", 1, verbose_level)

    return dataset


def clear_output_dir(search_tool: str, output_directory: str):
    """
    Clear output directory of pdb files starting with the specified search tool's name, to ensure that no old results
    or other files intervene in later parsing of the results

    Parameters
    ----------
    search_tool : str,
    output_directory : str

    Returns
    -------
        None
    """

    pdb_files = [x for x in os.listdir(output_directory) if x.endswith(".pdb") and x.startswith(search_tool)]
    for f in pdb_files:
        os.remove(f"{output_directory}{f}")


def download_pdb_from_db(url: str, i_try: int, max_try: int):
    """
    Attempt pdb download from online database, either as .pdb- or .cif-file. If this fails retry until max retry is reached
    
    Parameters
    ----------
    url : str,
    i_try : int,
    max_try : int

    Returns
    -------
    pdb_file : str | None 
    """
    
    try:
        if url.startswith("https://files.rcsb.org/"):
            # Attempt regular .pdb call from RCSB database
            pdb_file = ''.join(r.post(url).text)
            # If ordinary download call fails attempt .cif call (for mmCIF file)
            if pdb_file.startswith("<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\">"):
                cif_url = f"{'.'.join(url.split('.')[:-1])}.cif"
                pdb_file = ''.join(r.post(cif_url, timeout=1).text)
            return pdb_file
        else:
            # Attempt .pdb call from AlphaFold database
            pdb_file = r.get(url).text
            if "<Error><Code>NoSuchKey</Code><Message>The specified key does not exist.</Message></Error>" in pdb_file:
                return None
            else:
                return pdb_file
    # Retry on timeout if not reached max_try already, else return None
    except (r.exceptions.Timeout, TimeoutError):
        if i_try >= max_try:
            return None
        else:
            time.sleep(1)
            return download_pdb_from_db(url, i_try + 1, max_try)
    # Break execution if no connection to database possible
    except (ConnectionError, socket.gaierror, r.exceptions.ConnectionError) as e:
        if i_try == max_try:
            print(f"No connection to {'RCSB' if url.startswith('https://files.rcsb.org/') else 'AlphaFold'}"
                  f" API possible. Please try again later.")
            print(e)
        return download_pdb_from_db(url, i_try + 1, max_try)


def accept_resolution_method(pdb: str, pdb_id: str, res_cutoff: float):
    """
    decide whether a pdb should be accepted based on the used method and its resolution

    Parameters
    ----------
    pdb : str,
    pdb_id : str,
    res_cutoff : float

    Returns
    -------
    accept_resolution_method : bool,
    method : str,
    resolution : str | float
    """

    method, resolution = ('-' for _ in range(2))

    # If given pdb-file is empty return False
    if not pdb:
        return False, method, resolution
    # If pdb_id has length equal or higher than 5, it is an alphafold entry, return True
    elif len(pdb_id) >= 5:
        return True, "ALPHAFOLD", "ALPHAFOLD"
    # In other cases check whether experimental method for structure determination was diffraction or microscopy method,
    # and whether the resolution is below or equal to the threshhold, if so return True
    else:
        all_pdb_methods = ["X-RAY DIFFRACTION", "ELECTRON MICROSCOPY", "SOLUTION NMR", "ELECTRON CRYSTALLOGRAPHY",
                           "NEUTRON DIFFRACTION", "SOLID-STATE NMR", "SOLUTION SCATTERING", "FIBER DIFFRACTION",
                           "POWDER DIFFRACTION", "EPR", "THEORETICAL MODEL", "INFRARED SPECTROSCOPY"]
        accepted_pdb_methods = ["X-RAY DIFFRACTION", "ELECTRON MICROSCOPY", "ELECTRON CRYSTALLOGRAPHY",
                                "NEUTRON DIFFRACTION", "FIBER DIFFRACTION"]
        resolution_excepted_methods = ["SOLUTION NMR", "SOLID-STATE NMR"]
        accept_method = False
        accept_resolution = False

        for line in pdb.split('\n'):
            # If line startswith EXPDTA, it contains the information of the experimental method used for structure
            # determination
            if line.startswith("EXPDTA"):
                method = ' '.join([w for w in line.replace('  ', ' ').split() if w][1:])
                accept_method = method in accepted_pdb_methods
            # If line contains ANGSTROMS. and RESOLUTION. it contains the float value of the resolution, accept it if it
            # is below or equal to the threshhold
            elif ("ANGSTROMS." in line) and ("RESOLUTION." in line):
                resolution = float([w for w in line.replace('  ', ' ').split() if w][-2])
                accept_resolution = resolution <= res_cutoff
                break
            elif method in resolution_excepted_methods:
                accept_method = True
                accept_resolution = True
                resolution = 'NOT APPLICABLE'
                break

        return accept_method and accept_resolution, method, resolution
