import requests as r
import pandas as pd
import time
import os
import gzip
import shutil
import numpy as np
import concurrent.futures
from Bio import PDB
from claudio.utils.utils import verbose_print, round_self
import warnings

warnings.filterwarnings("ignore", category=PDB.StructureBuilder.PDBConstructionWarning)

def query_pdb_after_date(date_str: str):
    """
    Query the PDB database for all IDs of files which were modified or created after a certain date.

    Parameters
    ----------
    date_str : str
        The date in the format 'YYYY-MM-DD'.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the PDB IDs and their corresponding dates.
    """
    url = "https://search.rcsb.org/rcsbsearch/v2/query"
    query = {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "entity_poly.rcsb_entity_polymer_type",
                        "operator": "exact_match",
                        "value": "Protein"
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                    "attribute": "exptl.method",
                    "operator": "in",
                    "value": [
                        "X-RAY DIFFRACTION",
                        "ELECTRON MICROSCOPY",
                        "ELECTRON CRYSTALLOGRAPHY",
                        "NEUTRON DIFFRACTION",
                        "FIBER DIFFRACTION",
                        "SOLUTION NMR",
                        "SOLID-STATE NMR"
                    ]
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_accession_info.revision_date",
                        "operator": "greater_or_equal",
                        "value": date_str
                    }
                }
            ]
        },
        "request_options": {
            "return_all_hits": True
        },
        "return_type": "entry"
    }

    try:
        response = r.post(url, json=query)
        response.raise_for_status()
    except Exception as e:
        print(e)
        return pd.DataFrame(columns=['pdb_id', 'modification_date'])

    if response.status_code == 204:
        verbose_print("No new PDB files found.", 1, 2)
        return pd.DataFrame(columns=['pdb_id', 'modification_date'])
    else:
        data = response.json()
        pdb_ids = [entry['identifier'] for entry in data['result_set']]
        print(len(pdb_ids))
        df = pd.DataFrame({'pdb_id': pdb_ids, 'modification_date': time.strftime("%Y-%m-%d")})
        return df

def download_pdbs(data, output_dir):
    """
    Download the PDB files for a given list of PDB IDs.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the PDB IDs and their corresponding dates.

    Returns
    -------
    data : pd.DataFrame
        DataFrame containing the PDB IDs and their corresponding dates, methods and resolutions.
    None
    """
    accepted_pdb_methods = ["X-RAY DIFFRACTION", "ELECTRON MICROSCOPY", "ELECTRON CRYSTALLOGRAPHY",
                            "NEUTRON DIFFRACTION", "FIBER DIFFRACTION"]
    resolution_excepted_methods = ["SOLUTION NMR", "SOLID-STATE NMR"]
    def download_pdb_task(pdb_id):
        # Attempt regular .pdb call from RCSB database
        pdb_file = ''
        url = f'https://files.rcsb.org/download/{pdb_id}.pdb'
        pdb_file = ''.join(r.post(url).text)
        filename = f'{output_dir}{pdb_id}.pdb'

        # If ordinary download call fails attempt .cif call (for mmCIF file)
        if pdb_file.startswith("<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 2.0//EN\">"):
            print("is cif",pdb_id)
            cif_url = f"{'.'.join(url.split('.')[:-1])}.cif"
            pdb_file = ''.join(r.post(cif_url, timeout=1).text)
            filename = f'{output_dir}{pdb_id}.cif'

            accept_method = False         
            lines = pdb_file.split('\n')
            for line in lines:
                # If line startswith _exptl.method, it contains the information of the experimental method used for structure
                # determination
                if line.startswith("_exptl.method "):
                    method = ''.join([w for w in line.split(sep="\'") if w][1])
                    accept_method = method in accepted_pdb_methods
                    data.loc[data['pdb_id'] == pdb_id, 'method'] = method
                    if method in resolution_excepted_methods:
                        resolution = np.NaN
                        data.loc[data['pdb_id'] == pdb_id, 'resolution'] = resolution
                    break
                # If line contains _em_3d_reconstruction.resolution or _refine.ls_d_res_high, depending on the used method,
                # it contains the float value of the resolution, accept it if it
                # is below or equal to the threshhold
            if method == "ELECTRON MICROSCOPY":
                for line in pdb_file.split('\n'):
                    if line.startswith("_em_3d_reconstruction.resolution ") and accept_method:
                        resolution = float([w for w in line.replace('  ', ' ').split() if w][1])
                        data.loc[data['pdb_id'] == pdb_id, 'resolution'] = resolution
                        break
            else: 
                if method in accepted_pdb_methods:
                    for line in pdb_file.split('\n'):
                        if line.startswith("_refine.ls_d_res_high") and accept_method:
                            resolution = float([w for w in line.replace('  ', ' ').split() if w][1])
                            data.loc[data['pdb_id'] == pdb_id, 'resolution'] = resolution
                            break
        else:
            lines = pdb_file.split('\n')
            for line in lines:
                if line.startswith("EXPDTA"):
                    method = ' '.join([w for w in line.replace('  ', ' ').split() if w][1:])
                    data.loc[data['pdb_id'] == pdb_id, 'method'] = method
                elif ("ANGSTROMS." in line) and ("RESOLUTION." in line):
                    resolution = float([w for w in line.replace('  ', ' ').split() if w][-2])
                    data.loc[data['pdb_id'] == pdb_id, 'resolution'] = resolution
                    break
            if method in resolution_excepted_methods:
                resolution = np.NaN
                data.loc[data['pdb_id'] == pdb_id, 'resolution'] = resolution
            
        
        with gzip.open(f'{filename}.gz', 'wt') as f:
            f.write(pdb_file)
    
    if data.empty:
        return
    else:
        verbose_print(f"Download progress:", 1, 2)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(download_pdb_task, pdb_id): pdb_id for pdb_id in data['pdb_id']}
            ind = 0
            for future in concurrent.futures.as_completed(futures):
                try:
                    ind += 1
                    verbose_print(f"\r\t[{round_self((ind * 100) / len(data.index), 2)}%]", 1, 2, end='')
                    del futures[future]
                except Exception as e:
                    print(e)
        verbose_print("", 1, 2)
    return data


def update_pdb_database():
    """
    Update the PDB database with the latest PDB files.

    Returns
    -------
    None
    """
    
    # read the existing PDB IDs to check when the last update was made
    if os.path.exists('./claudio/data/pdb/pdb_ids.csv'):
        df = pd.read_csv('./claudio/data/pdb/pdb_ids.csv')
        # find the oldest update-date in the database
        oldest_date = pd.to_datetime(df["modification_date"]).min()
        date_str = oldest_date.strftime('%Y-%m-%d')
    else:
        df = pd.DataFrame(columns=['pdb_id', 'modification_date', 'method', 'resolution'])
        date_str = '2000-01-01'
    # query the PDB database for all files which were updated after the oldest update-date
    # and download them

    new_pdbs = query_pdb_after_date(date_str)
    if new_pdbs.empty:
        return
    else:
        new_pdbs = download_pdbs(new_pdbs,'./claudio/data/pdb/')

        # update the PDB IDs file
        df["modification_date"] = pd.to_datetime(df["modification_date"])
        new_pdbs["modification_date"] = pd.to_datetime(new_pdbs["modification_date"])
        df = pd.concat([df,new_pdbs])
        df = df.sort_values("modification_date").drop_duplicates(subset="pdb_id", keep="last")
        # df = populate_pdb_info(df, new_pdbs['pdb_id'].tolist(), './claudio/data/pdb/')
            
        df["modification_date"] = time.strftime("%Y-%m-%d")
        df.to_csv('./claudio/data/pdb/pdb_ids.csv', index=False)

# update_pdb_database()
