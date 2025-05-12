import os
import concurrent.futures
import socket
import time
import pandas as pd
from Bio.PDB import Polypeptide, PDBParser, FastMMCIFParser
from Bio.Align import PairwiseAligner
import requests as r
import numpy as np

from claudio.utils.utils import verbose_print, round_self

_MAX_INTERFACE_DISTANCE = 50
# cache for parsed pdb-structures to prevent multiple parsing of the same file
pdb_cache = {}


def search_site_pos_in_pdb(data: pd.DataFrame, df_xl_res: pd.DataFrame,
                           verbose_level: int):
    """
    search for site positions in pdb, extend input dataset by res_criteria, 
    e.g. whether the found sites satisfy the criteria of being the specified 
    residue, the method used to find the sites in the structure file, in case 
    said method was alphafold the pLDDT, e.g. confidence, value, and download 
    new alphafold pdb into directory, if needed

    Parameters
    ----------
    data : pd.DataFrame,
    df_xl_res : pd.DataFrame,
    verbose_level : int

    Returns 
    -------
    data : pd.DataFrame
    """

    # Read shift file given by EMBL-EBI database
    # (see: https://www.ebi.ac.uk/pdbe/docs/sifts/quick.html) for rcsb files
    # to uniprot entries
    project_path = '/'.join(os.path.abspath(__file__).replace('\\\\', '/').replace('\\', '/').split('/')[:-4])
    project_path = project_path + '/' if project_path else ""
    pdb_uni_map = pd.read_csv(f"{project_path}data/pdb_chain_uniprot.csv",
                              header=1)
    pdb_uni_map["PDB"] = [x.upper() for x in pdb_uni_map["PDB"]]

    # Define data container lists
    ind = 0

    # Save numbers for performance/success statistics
    errors = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    successes, true_res_crits = ([0,0], [0,0])

    # Initialize columns for results
    data["pdb_pos_a"] = None
    data["pdb_pos_b"] = None
    data["res_criteria_fulfilled"] = False
    data["res_crit_a"] = False
    data["res_crit_b"] = False
    data["method_a"] = ""
    data["method_b"] = ""
    data["pLDDT_a"] = "-"
    data["pLDDT_b"] = "-"
    data["is_interfaced"] = False

    # vectorized computation of xl_type
    data["xl_type"] = np.where(data["unip_id_a"] == data["unip_id_b"],
                               "intra", "inter")
    xl_res_list = df_xl_res.res.tolist()

    global pdb_cache
    pdb_cache = {}
    populate_pdb_cache(data, verbose_level)

    # Iterate over given dataset
    def search_site_task(i, row):

        # If saved path is not '-' perform site distance calculation,
        # else append values to list containers indicating a fail here
        both_pdbs_found = row["path"] != '-'
        if both_pdbs_found:
            # Search site_a in structure file
            pdb_pos_a, res_criteria_a, method_a, i_error_a, pLDDT_a, new_path, atom_coord_a = \
                compute_site_pos(i, row, 'a', row["xl_type"], pdb_uni_map, "", xl_res_list, verbose_level)
            # If method used for site_a is alphafold, set method
            # for set_b to alphafold as well
            method_b = "" if method_a != "alphafold" else "alphafold"

            # Search site_b in structure file
            pdb_pos_b, res_criteria_b, method_b, i_error_b, pLDDT_b, new_path, atom_coord_b = \
                compute_site_pos(i, row, 'b', row["xl_type"], pdb_uni_map,
                                 method_b, xl_res_list, verbose_level)

            # If method for site_b was alphafold, but not for site_a,
            # search site_a again with alphafold method specified this time
            if method_b == "alphafold" and method_a != "alphafold":
                pdb_pos_a, res_criteria_a, method_a, i_error_a, pLDDT_a, new_path, atom_coord_a = \
                    compute_site_pos(i, row, 'a', row["xl_type"], pdb_uni_map, "alphafold", xl_res_list,
                                     verbose_level)

            # Replace path if alphafold file was downloaded instead
            if new_path and row["xl_type"] == "intra":
                new_res = [new_path,'A','A',
                           new_path.split('_')[-1].split('.')[0],"ALPHAFOLD",
                           "ALPHAFOLD"]
                data.loc[i,["path","chain_a","chain_b","pdb_id","pdb_method","pdb_resolution"]] = new_res

            # Append results to data container lists
            res_cols = ["pdb_pos_a","pdb_pos_b","method_a","method_b",
                        "pLDDT_a","pLDDT_b","res_crit_a","res_crit_b",
                        "res_criteria_fulfilled"]
            data.loc[i,res_cols] = [pdb_pos_a,pdb_pos_b,method_a,method_b,
                                    pLDDT_a,pLDDT_b,res_criteria_a,
                                    res_criteria_b,(res_criteria_a
                                                    and res_criteria_b)]

            if atom_coord_a is not None and atom_coord_b is not None:
                interface_distance = np.sqrt(np.sum((atom_coord_a
                                                     - atom_coord_b) ** 2))
                data.loc[i,"is_interfaced"] = (interface_distance
                                               <= _MAX_INTERFACE_DISTANCE)

            # Increase counters for performance/success statistics
            true_res_crits[0] += 1 if res_criteria_a else 0
            true_res_crits[1] += 1 if res_criteria_b else 0
            if i_error_a >= 0:
                errors[0][i_error_a] += 1
            else:
                successes[0] += 1
            if i_error_b >= 0:
                errors[1][i_error_b] += 1
            else:
                successes[1] += 1

        return data

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(search_site_task, i, row):
                   (i, row) for i, row in data.iterrows()}

        for future in concurrent.futures.as_completed(futures):
            try:
                if future.result() is not None:
                    data = future.result()
                    ind += 1
                    progress = round_self((ind * 100) / len(data.index), 2)
                    verbose_print(f"\r\tSearch site pos:[{progress}%]", 1, verbose_level,
                                  end='')
                del futures[future]
            except Exception as e:
                print(e)

    verbose_print("", 1, verbose_level)

    # Print site specific error and success statistics
    verbose_print(f"\tErrors & Successes:"
                  f"\n\t\ta:"
                  f"\n\t\t\tIndexError with unip_pos: {errors[0][0]}"
                  f"\n\t\t\tNo model in pdb, or other error with command: \"chains = models[0].get_list()\": "
                  f"{errors[0][1]}"
                  f"\n\t\t\tChain ID was not found in pdb file: {errors[0][2]}"
                  f"\n\t\t\tEntry not found in pdb_chain_uniprot.csv: {errors[0][3]}"
                  f"\n\t\t\tResidue not found by id, and following alphafold replacement download attempt failed: "
                  f"{errors[0][4]}"
                  f"\n\t\t\tGot non-aminoacid at residue position: {errors[0][5]}"
                  f"\n\t\t\tNo C-beta found: {errors[0][6]}\n"
                  f"\n\t\t\tSuccessfully computed pdb positions: {successes[0]}"
                  f"\n\t\t\t\tNumber of fulfilled residue criteria: {true_res_crits[0]}"
                  f"\n\t\tb:"
                  f"\n\t\t\tIndexError with unip_pos: {errors[1][0]}"
                  f"\n\t\t\tNo model in pdb, or other error with command: \"chains = models[0].get_list()\": "
                  f"{errors[1][1]}"
                  f"\n\t\t\tChain ID was not found in pdb file: {errors[1][2]}"
                  f"\n\t\t\tEntry not found in pdb_chain_uniprot.csv: {errors[1][3]}"
                  f"\n\t\t\tResidue not found by id, and following alphafold replacement download attempt failed: "
                  f"{errors[1][4]}"
                  f"\n\t\t\tGot non-aminoacid at residue position: {errors[1][5]}"
                  f"\n\t\t\tNo C-beta found: {errors[1][6]}\n"
                  f"\n\t\t\tSuccessfully computed pdb positions: {successes[1]}"
                  f"\n\t\t\t\tNumber of fulfilled residue criteria: {true_res_crits[1]}"
                  f"\n\t\tTotal number of entries not found in databases: "
                  f"{len(data[data.path == '-'])}", 2, verbose_level)

    return data


def compute_site_pos(i: int, data: pd.Series, site_id: int, xl_type: str,
                     pdb_uni_map: pd.DataFrame, method: str, xl_res_list: list,
                     verbose_level: int):
    """
    Search site in structure file and return threedimensional position

    Parameters 
    ----------
    i : int,
    data : pd.Series,
    site_id : int,
    xl_type : str,
    pdb_uni_map : pd.DataFrame,
    method : str,
    xl_res_list : list,
    verbose_level : int

    Returns
    -------
    pdb_pos : int,
    res_criteria : bool,
    method : str,
    i_error : int,
    pLDDT: float,
    new_path_a : str,
    atom_coord : [float, float, float] | None
    """

    # Extract pdb_id, chain_id and unip_id from data
    pdb_id = data["pdb_id"]
    chain_id = data[f"chain_{site_id}"]
    unip_id = data[f"unip_id_{site_id}"]
    unip_seq = data[f"seq_{site_id}"]
    new_path = ''

    # Test whether specified position is accessible in uniprot sequence,
    # if not return fail with i_error = 0
    try:
        verbose_print(f"\n\tunip_pos:{data[f'pos_{site_id}']}, Acid at pos: {unip_seq[data[f'pos_{site_id}'] - 1]} ,"
                      f" fulfills residue criteria: {unip_seq[data[f'pos_{site_id}'] - 1] in xl_res_list}",
                      4, verbose_level)
    except IndexError:
        verbose_print(f"\n\tIndexError with unip_pos: {data[f'pos_{site_id}']} (entry: {i}, unip_id: {unip_id})", 4,
                      verbose_level)
        return None, False, method, 0, '-', '', None

    # Check whether structure file was already parsed, if not parse it and
    # save it in cache
    models = pdb_cache.get(data["path"])

    # Try accessing list of chains, if exception is thrown, e.g. structure
    # file is empty, return fail with i_error = 1
    try:
        chains = models[0].get_list()
    except:
        verbose_print(f"\tWarning! No model in pdb: \"chains = models[0].get_list()\".\n\t\t\t(entry: {i}, pdb: "
                      f"{pdb_id}:{chain_id})", 2, verbose_level)
        return None, False, method, 1, '-', '', None

    # If chain_id was unspecified by structure search tool,
    # e.g. chain_id == '-', use first(/only) chain in structure
    # file, else search for chain with matching id
    if chain_id == '-':
        chain = chains[0]
    else:
        chain_found = False
        for c in chains:
            if c.__repr__().split('=')[1][0] == chain_id:
                chain = c
                chain_found = True
                break
        # If specified chain id was not found, return fail with i_error = 2
        if not chain_found:
            verbose_print(f"\tWarning! Chain ID was not found in pdb file ({pdb_id}:{chain_id}).", 2, verbose_level)
            return None, False, method, 2, '-', '', None

    # If pdb is from rcsb database (indicated by len(id) <= 4), try computing
    # uniprot to pdb index shift via EMBL-EBI shift file
    # (pdb_chain_uniprot.csv)
    if len(pdb_id) <= 4:
        if method != "alphafold":
            pdb_uni_map_entry = pdb_uni_map[(pdb_uni_map["PDB"] == pdb_id) & (pdb_uni_map["CHAIN"] == chain_id) &
                                            (pdb_uni_map["SP_PRIMARY"] == unip_id)]
            shift = compute_pdb_uniprot_shift(pdb_uni_map_entry) if not pdb_uni_map_entry.empty else None
        else:
            shift = None

        # If shift computation failed, attempt realigning pdb sequence to
        # uniprot sequence; If alphafold is specified as method already
        # completely replace current structure model with new downloaded
        # alphafold structure
        if shift is None or method == "alphafold":
            method = "realigning" if method != "alphafold" else "alphafold"
            pdb_seq = ''
            for res in chain.get_list():
                try:
                    pdb_seq += Polypeptide.three_to_one(res.get_resname())
                except:
                    continue
            if method == "realigning":
                # Attempt realigning if method not alphafold
                residue_pos = realign_unip_pos_in_pdb_seq(pdb_seq, unip_seq,
                                                          data[f"pos_{site_id}"],
                                                          verbose_level)
            else:
                residue_pos = None

            # If method alphafold or realignment attempt failed, replace with
            # rcsb structure alphafold structure and continue with
            # method = "alphafold"
            if (residue_pos is None or method == "alphafold") and xl_type == "intra":
                verbose_print(f"\tSelf computed res pos ({unip_id}, {data[f'pos_{site_id}']}): {residue_pos}\n"
                              f"\tThis position is not in range of the pdb_seq!", 4, verbose_level)
                verbose_print("\tAttempt replacement alphafold download.", 2, verbose_level)
                chain, new_path = replacement_alphafold_download(unip_id, data["path"])

                if chain is None:
                    # If alphafold replacement of structure failed,
                    # return fail with i_error = 4
                    verbose_print(f"\tReplacement alphafold download attempt returned an error ({unip_id} probably not "
                                  f"found in database).\n\t\t\t(entry: {i}, unip: {unip_id}, pdb: {pdb_id}:{chain_id})",
                                  2, verbose_level)
                    return None, False, method, 4, '-', '', None
                # Else replacement was successful
                method = "alphafold"
                residue_pos = data[f"pos_{site_id}"]
                try:
                    verbose_print(f"\tReplacement attempt successful (new residue: "
                                  f"{Polypeptide.three_to_one(chain.__getitem__(residue_pos).get_resname())}).", 2,
                                  verbose_level)
                except:
                    pass
            # Elif residue position was not found and inter crosslink, as no
            # replacement is possible means this position cannot be retrieved
            elif residue_pos is None and xl_type == "inter":
                return None, False, method, 4, '-', '', None
            # Else print computed position by realigning and continue with
            # method = "realigning"
            else:
                verbose_print(f"\tSelf computed res pos ({unip_id}, {data[f'pos_{site_id}']}): {residue_pos}, "
                              f"fulfills residue criteria: {pdb_seq[residue_pos - 1] in xl_res_list}:"
                              f"{pdb_seq[residue_pos - 1]}", 4, verbose_level)
        # Else print position given by shift file and continue with
        # method = "pdb_chain_uniprot"
        else:
            method = "pdb_chain_uniprot"
            residue_pos = data[f"pos_{site_id}"] + shift
            verbose_print(f"\tComputed res pos with pdb_chain_uniprot.csv ({unip_id}, {data[f'pos_{site_id}']}): "
                          f"{residue_pos}", 4, verbose_level)
    # Else specified structure file is already an alphafold entry,
    # thus continue with method = "alphafold"
    else:
        method = "alphafold"
        residue_pos = data[f"pos_{site_id}"]
        verbose_print(f"\tRes pos in alphafold entry ({unip_id}, {data[f'pos_{site_id}']}): {residue_pos}", 4,
                      verbose_level)

    # If method either pdb_chain_uniprot or alphafold, directly retrieve
    # residue by index, else gather pdb sequence and manually retrieve the
    # i-th residue
    try:
        if method in ["alphafold", "pdb_chain_uniprot"]:
            res = chain.__getitem__(residue_pos)

        else:
            res = None
            chain_index = 0
            for residue in chain.get_list():
                try:
                    Polypeptide.three_to_one(residue.get_resname())
                    chain_index += 1
                    if chain_index == residue_pos:
                        res = residue
                        break
                except:
                    continue
    # If exception is thrown, attempt replacing structure with fresh alphafold
    # download; if this fails as well, return fail with i_error = 4
    except:
        verbose_print(f"\tWarning! Residue not found by id (maybe out of bounds).\n\t\t\t"
                      f"(entry: {i}, pdb: {pdb_id}:{chain_id})", 2, verbose_level)
        resseq_ids = [int(res.__repr__().split('=')[2].split(' ')[0]) for res in chain.get_list()]
        verbose_print(f"\t\t\tsearched pos: {residue_pos}, actual interval: ({min(resseq_ids)}, {max(resseq_ids)})", 4,
                      verbose_level)

        if xl_type == "intra":
            verbose_print("\tAttempt replacement alphafold download.", 2,
                          verbose_level)
            chain, new_path = replacement_alphafold_download(unip_id,
                                                             data["path"])
            # If alphafold replacement of structure failed, return fail with
            # i_error = 4
            if chain is None:
                verbose_print(f"\tReplacement alphafold download attempt returned an error ({unip_id} probably not "
                              f"found in database).\n\t\t\t(entry: {i}, unip: {unip_id}, pdb: {pdb_id}:{chain_id})", 2,
                              verbose_level)
                return None, False, method, 4, '-', '', None
            # Else replacement was successful
            res = chain.__getitem__(residue_pos)
            try:
                verbose_print(f"\tReplacement attempt successful (new residue: "
                              f"{Polypeptide.three_to_one(res.get_resname())}).", 2, verbose_level)
            except:
                pass
        else:
            # Cannot find residue at position and no alphafold replacement
            # possible with inter crosslink
            verbose_print(f"\tWarning! Cannot find residue at position and no alphafold replacement possible for inter "
                          f"crosslink (pos={residue_pos}).\n\t\t\t(entry: {i}, pdb: {pdb_id}:{chain_id})", 2,
                          verbose_level)
            return None, False, method, 4, '-', '', None
    # Check whether residue criteria is fulfilled, if not attempt final
    # alphafold replacement; Check whether a valid CB is accessible for
    # specified residue, else return fail with i_error = 6
    try:
        # Check whether specified residue has valid name, else return fail
        # with i_error = 5
        try:
            resname = Polypeptide.three_to_one(res.get_resname())
        except:
            verbose_print(f"\tWarning! Got non-aminoacid at residue position ({res.get_resname()}).\n\t\t\t"
                          f"(entry: {i}, pdb: {pdb_id}:{chain_id})", 2, verbose_level)
            return None, False, method, 5, '-', '', None
        res_criteria = (resname in xl_res_list) and (resname == unip_seq[data[f'pos_{site_id}'] - 1])
        verbose_print(f"\tFinal residue is '{resname}' (thus res_criteria_{site_id}: {res_criteria})", 4, verbose_level)
        # If residue criteria fulfilled return result
        if res_criteria:
            try:
                _ = res["CB"]
                return int(res.get_id()[1]), res_criteria, method, -1,\
                    res["CB"].get_bfactor() if method == "alphafold" else '-', new_path, res["CB"].get_coord()
            except:
                pass
        # Else attempt final alphafold replacement, if this fails return fail
        # with i_error = 4
        if xl_type == "intra":
            verbose_print("\tAttempt replacement alphafold download.", 2,
                          verbose_level)
            chain, new_path = replacement_alphafold_download(unip_id,
                                                             data["path"])
            if chain is None:
                verbose_print(f"\tReplacement alphafold download attempt returned an error ({unip_id} probably not "
                              f"found in database).\n\t\t\t(entry: {i}, unip: {unip_id}, pdb: {pdb_id}:{chain_id})", 2,
                              verbose_level)
                return None, False, method, 4, '-', '', None
            # Check whether specified residue by alphafold has valid name,
            # else return fail with i_error = 5
            try:
                method = "alphafold"
                residue_pos = data[f"pos_{site_id}"]
                res = chain.__getitem__(residue_pos)
                verbose_print(f"\tReplacement attempt successful (new residue: "
                              f"{Polypeptide.three_to_one(res.get_resname())}).",
                              2, verbose_level)
                resname = Polypeptide.three_to_one(res.get_resname())
                res_criteria = resname in xl_res_list
                verbose_print(f"\tFinal residue is '{resname}' (thus res_criteria_{site_id}: {res_criteria})", 4,
                              verbose_level)
                return (int(res.get_id()[1]), res_criteria, method, -1,
                        res["CB"].get_bfactor(), new_path,
                        res["CB"].get_coord())
            except:
                verbose_print(f"\tWarning! Got non-aminoacid at residue position ({res.get_resname()}).\n\t\t\t"
                              f"(entry: {i}, pdb: {pdb_id}:{chain_id})", 2, verbose_level)
                return None, False, method, 5, '-', '', None
        else:
            # Wrong residue and no alphafold replacement possible
            # with inter crosslink
            verbose_print(f"\tWarning! Wrong residue at position and no alphafold replacement possible for inter "
                          f"crosslink ({res.get_resname()}).\n\t\t\t(entry: {i}, pdb: {pdb_id}:{chain_id})", 2,
                          verbose_level)
            return None, False, method, 4, '-', '', None
    except:
        verbose_print(f"\tWarning! No C-beta found ({res.get_resname()}).\n\t\t\t"
                      f"(entry: {i}, pdb: {pdb_id}:{chain_id})", 2, verbose_level)
        return None, False, method, 6, '-', '', None

def compute_pdb_uniprot_shift(pdb_uni_map_entry: pd.DataFrame):
    """
    Compute shift by a finding entry with closely related indeces (neighbours)
    for pdb and uniprot, search through entries recursively until either 
    satisfying result found, or dataset empty (in the latter case return None)
    
    Parameters
    ----------
    pdb_uni_map_entry : pd.DataFrame

    Returns
    -------
    shift : int | None
    """

    sp_beg = int(pdb_uni_map_entry["SP_BEG"].iloc[0])
    sp_end = int(pdb_uni_map_entry["SP_END"].iloc[0])
    pdb_beg = pdb_uni_map_entry["PDB_BEG"].iloc[0]
    pdb_end = pdb_uni_map_entry["PDB_END"].iloc[0]
    # Set acceptable neighbour ranges
    neighbours_beg = (sp_beg-1, sp_beg+2)
    neighbours_end = (sp_end-1, sp_end+2)

    # If pdb start is not None and in range, return shift
    if pdb_beg != "None" and \
            int(pdb_beg) in range(neighbours_beg[0], neighbours_beg[1]):
        return int(pdb_beg) - sp_beg
    # Elif pdb end is not None and in range, return shift
    elif pdb_end != "None" and \
            int(pdb_end) in range(neighbours_end[0], neighbours_end[1]):
        return int(pdb_end) - sp_end
    # Else if dataset not empty, recursively call function again with dataset
    # except first entry, else return None
    else:
        if not pdb_uni_map_entry[1:].empty:
            return compute_pdb_uniprot_shift(pdb_uni_map_entry[1:])
        return None

def realign_unip_pos_in_pdb_seq(pdb_seq: str, unip_seq: str, unip_pos: int,
                                verbose_level: int):
    """
    Realign pdb sequence to uniprot sequence, and compute position of residue 
    in pdb sequence which is specified by unip_pos in uniprot sequence, if 
    this fails return None
    
    Parameters
    ----------
    pdb_seq : str,
    unip_seq : str,
    unip_pos : int,
    verbose_level : int

    Returns
    -------
    pdb_pos : int | None
    """

    # Set alignment parameters
    aligner = PairwiseAligner()
    aligner.mode = "local"
    aligner.gap_score = -5
    aligner.match_score = 1
    aligner.mismatch_score = 0
    # aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")

    # Try aligning, if it fails return None
    try:
        alignment = aligner.align(pdb_seq, unip_seq)[0]
    except ValueError:
        return None
    verbose_print(f"\t\tAlignment:\n{alignment}", 3, verbose_level)
    aligned_pdb_seq = str(alignment).split('\n',maxsplit=1)[0]
    aligned_unip_seq = str(alignment).split('\n')[2]

    # Find unip_pos in aligned uniprot sequence
    aligned_unip_i = -1
    aligned_unip_pos = 0
    for i, c in enumerate(aligned_unip_seq):
        aligned_unip_i = i
        if c not in [' ', '-']:
            aligned_unip_pos += 1
        if aligned_unip_pos == unip_pos:
            break

    # Find unip_pos in aligned pdb sequence and compute according pdb_pos in
    # unaligned pdb sequence, return pdb_pos if successful, else return None
    try:
        _ = aligned_pdb_seq[aligned_unip_i + 1]
        pdb_pos = len(aligned_pdb_seq[:aligned_unip_i + 1].replace(' ', '').replace('-', ''))
        if pdb_pos > 0:
            al_seq = str(alignment).split('\n')[1]
            verbose_print(f"\t\tAligned site (index: {aligned_unip_i}):\n"
                          f"\t\t\t{aligned_pdb_seq[aligned_unip_i]}\n"
                          f"\t\t\t{al_seq[aligned_unip_i]}\n"
                          f"\t\t\t{aligned_unip_seq[aligned_unip_i]}", 3, 
                          verbose_level)
            return pdb_pos
        return None
    except IndexError:
        return None


def replacement_alphafold_download(unip_id: str, path: str, i_try: int = 0):
    """
    Attempt to download a replacement alphafold structure model (also return 
    path to new pdb), return None if attempt fails
    
    Parameters
    ----------
    unip_id : str,
    path : str

    Returns
    -------
    chain : Bio.PDB.Chain | None
    new_path : str |  ''
    """
    max_try = 5
    # ex.: data/out/structure_search/blastp_6G2J.pdb
    new_path = f"{'_'.join(path.split('_')[:-1])}_af{unip_id}.pdb"

    if not os.path.exists(new_path):
        url = f"https://alphafold.ebi.ac.uk/files/AF-{unip_id}-F1-model_v4.pdb"
        with open(new_path, 'w', encoding="utf-8") as f:
            try:
                f.write(r.get(url,timeout=60).text)
            except r.exceptions.Timeout:
                if i_try >= max_try:
                    return None, ''

                time.sleep(1)
                return replacement_alphafold_download(unip_id, path,
                                                        i_try + 1)

            except (ConnectionError, socket.gaierror,
                    r.exceptions.ConnectionError) as e:
                if i_try == max_try:
                    print("No connection to AlphaFold API possible. Please try again later.")
                    print(e)
                return replacement_alphafold_download(unip_id, path,
                                                      i_try + 1)
    try:
        models = pdb_cache.get(new_path,None)
        if models is None:
            models = PDBParser().get_structure('', new_path).get_list()
            pdb_cache[new_path] = models

        return models[0].get_list()[0], new_path
    except:
        return None, ''


def populate_pdb_cache(data: pd.DataFrame, verbose_level: int):
    """
    Populate pdb_cache with parsed pdb structures to prevent multiple parsing
    of the same file

    Parameters
    ----------
    data : pd.DataFrame,
    verbose_level : int

    Returns
    -------
    None
    """

    ind = 0
    def parse_task(path):
        global pdb_cache
        # Parse structure file with normal PDBParser, if exception thrown use
        # FastMMCIFParser
        if path != '-':
            try:
                models = PDBParser().get_structure('', path).get_list()
            except:
                models = FastMMCIFParser().get_structure('', path).get_list()

            pdb_cache[path] = models

    with concurrent.futures.ThreadPoolExecutor() as executor:
        len_paths = len(data["path"].unique().tolist())
        futures = {executor.submit(parse_task, path):
                   path for path in data["path"].unique().tolist()}

    for future in concurrent.futures.as_completed(futures):
        try:
            ind += 1
            progress = round_self((ind * 100) / len_paths, 2)
            verbose_print(f"\r\tParsing {len_paths} structure files: [{progress}%]",
                          1, verbose_level, end='')
            del futures[future]
        except Exception as e:
            print(e)
    verbose_print("", 1, verbose_level)
