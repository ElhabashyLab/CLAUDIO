import pandas as pd
from Bio.PDB import Polypeptide, PDBParser, MMCIFParser
from Bio.Align import PairwiseAligner
import requests as r
import os
import sys


def search_site_pos_in_pdb(data, df_xl_res):
    # search for site positions in pdb, extend input dataset by res_criteria, e.g. whether the found
    # sites satisfy the criteria of being the specified residue, the method used to find the sites in the structure
    # file, in case said method was alphafold the pLDDT, e.g. confidence, value, and download new alphafold pdb into
    # directory, if needed
    #
    # input data: pd.DataFrame, df_xl_res: pd.DataFrame
    # return data: pd.DataFrame

    # Read shift file given by EMBL-EBI database (see: https://www.ebi.ac.uk/pdbe/docs/sifts/quick.html) for rcsb files
    # to uniprot entries
    project_path = '/'.join(os.path.abspath(__file__).split('/')[:-4])
    project_path = project_path + '/' if project_path else ""
    pdb_uni_map = pd.read_csv(f"{project_path}data/in/pdb_chain_uniprot.csv", header=1)
    pdb_uni_map["PDB"] = [x.upper() for x in pdb_uni_map["PDB"]]

    # Define data container lists
    ind = 0
    pdb_pos_as,\
        pdb_pos_bs,\
        res_criteria = ([] for _ in range(3))
    res_crit_site_specific, \
        methods, \
        pLDDTs = ([[], []] for _ in range(3))

    # Save numbers for performance/success statistics
    errors = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    successes, \
        true_res_crits = ([0, 0] for _ in range(2))

    # Iterate over given dataset
    for i, row in data.iterrows():
        print(f"\r\t[{round((ind * 100) / len(data.index), 2)}%]", end='')
        # If saved path is not '-' perform site distance calculation, else append values to list containers indicating
        # a fail here
        both_pdbs_found = row["path"] != '-'
        if not both_pdbs_found:
            pdb_pos_as.append(None)
            pdb_pos_bs.append(None)
            res_criteria.append(False)
            res_crit_site_specific[0].append(False)
            res_crit_site_specific[1].append(False)
            methods[0].append('')
            methods[1].append('')
            pLDDTs[0].append('-')
            pLDDTs[1].append('-')
        else:
            # Search site_a in structure file
            pdb_pos_a, res_criteria_a, method_a, i_error_a, pLDDT_a, new_path = \
                compute_site_pos(i, row, 'a', pdb_uni_map, "", df_xl_res)
            # If method used for site_a is alphafold, set method for set_b to alphafold as well
            method_b = "" if method_a != "alphafold" else "alphafold"

            # Search site_b in structure file
            pdb_pos_b, res_criteria_b, method_b, i_error_b, pLDDT_b, new_path = \
                compute_site_pos(i, row, 'b', pdb_uni_map, method_b, df_xl_res)

            # If method for site_b was alphafold, but not for site_a, search site_a again with alphafold method
            # specified this time
            if method_b == "alphafold" and method_a != "alphafold":
                pdb_pos_a, res_criteria_a, method_a, i_error_a, pLDDT_a, new_path = \
                    compute_site_pos(i, row, 'a', pdb_uni_map, "alphafold", df_xl_res)

            # Replace path if alphafold file was downloaded instead
            if new_path:
                data.loc[i, "path"] = new_path
                data.loc[i, "chain"] = 'A'
                data.loc[i, "pdb_id"] = new_path.split('_')[-2]
                data.loc[i, "pdb_method"] = "ALPHAFOLD"
                data.loc[i, "pdb_resolution"] = "ALPHAFOLD"

            # Append results to data container lists
            pdb_pos_as.append(pdb_pos_a)
            pdb_pos_bs.append(pdb_pos_b)
            methods[0].append(method_a)
            methods[1].append(method_b)
            pLDDTs[0].append(pLDDT_a)
            pLDDTs[1].append(pLDDT_b)
            res_crit_site_specific[0].append(res_criteria_a)
            res_crit_site_specific[1].append(res_criteria_b)
            res_criteria.append(res_criteria_a and res_criteria_b)

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

        ind += 1
        print(f"\r\t[{round((ind * 100) / len(data.index), 2)}%]", end='')
    print()

    # Print site specific error and success statistics
    print(f"\tErrors & Successes:"
          f"\n\t\ta:"
          f"\n\t\t\tIndexError with unip_pos: {errors[0][0]}"
          f"\n\t\t\tNo model in pdb, or other error with command: \"chains = models[0].get_list()\": {errors[0][1]}"
          f"\n\t\t\tChain ID was not found in pdb file: {errors[0][2]}"
          f"\n\t\t\tEntry not found in pdb_chain_uniprot.csv: {errors[0][3]}"
          f"\n\t\t\tResidue not found by id, and following alphafold replacement download attempt failed: {errors[0][4]}"
          f"\n\t\t\tGot non-aminoacid at residue position: {errors[0][5]}"
          f"\n\t\t\tNo C-beta found: {errors[0][6]}\n"
          f"\n\t\t\tSuccessfully computed pdb positions: {successes[0]}"
          f"\n\t\t\t\tNumber of fulfilled residue criteria: {true_res_crits[0]}"
          f"\n\t\tb:"
          f"\n\t\t\tIndexError with unip_pos: {errors[1][0]}"
          f"\n\t\t\tNo model in pdb, or other error with command: \"chains = models[0].get_list()\": {errors[1][1]}"
          f"\n\t\t\tChain ID was not found in pdb file: {errors[1][2]}"
          f"\n\t\t\tEntry not found in pdb_chain_uniprot.csv: {errors[1][3]}"
          f"\n\t\t\tResidue not found by id, and following alphafold replacement download attempt failed: {errors[1][4]}"
          f"\n\t\t\tGot non-aminoacid at residue position: {errors[1][5]}"
          f"\n\t\t\tNo C-beta found: {errors[1][6]}\n"
          f"\n\t\t\tSuccessfully computed pdb positions: {successes[1]}"
          f"\n\t\t\t\tNumber of fulfilled residue criteria: {true_res_crits[1]}"
          f"\n\t\tTotal number of entries not found in databases: "
          f"{len(data[data.path == '-'])}")

    # Append data container lists to dataset
    data["pdb_pos_a"] = pdb_pos_as
    data["pdb_pos_b"] = pdb_pos_bs
    data["res_criteria_fulfilled"] = res_criteria
    data["res_crit_a"] = res_crit_site_specific[0]
    data["res_crit_b"] = res_crit_site_specific[1]
    data["method_a"] = methods[0]
    data["method_b"] = methods[1]
    data["pLDDT_a"] = pLDDTs[0]
    data["pLDDT_b"] = pLDDTs[1]

    return data


def compute_site_pos(i, data, site_id, pdb_uni_map, method, df_xl_res):
    # Search site in structure file and return threedimensional position
    #
    # input i: int, data: pd.Series, site_id: int, pdb_uni_map: pd.DataFrame, method: str, df_xl_res: pd.DataFrame
    # return pdb_pos: int, res_criteria: bool, method: str, i_error: int, pLDDT: float, new_path_a: str

    # Extract pdb_id, chain_id and unip_id from data
    pdb_id = data["pdb_id"]
    chain_id = data["chain"]
    unip_id = data[f"unip_id_{site_id}"]
    new_path = ''
    # Test whether specified position is accessible in uniprot sequence, if not return fail with i_error = 0
    try:
        print(f"\n\tunip_pos:{data[f'pos_{site_id}']}, Acid at pos: {data[f'seq_{site_id}'][data[f'pos_{site_id}'] - 1]}"
              f", fulfills residue criteria: {data[f'seq_{site_id}'][data[f'pos_{site_id}'] - 1] in df_xl_res.res.tolist()}")
    except IndexError:
        print(f"\n\tIndexError with unip_pos: {data[f'pos_{site_id}']} (entry: {i}, unip_id: {unip_id})")
        return None, False, method, 0, '-', ''

    # Parse structure file with normal PDBParser, if exception thrown use MMCIFParser
    try:
        models = PDBParser().get_structure('', data["path"]).get_list()
    except:
        models = MMCIFParser().get_structure('', data["path"]).get_list()

    # Try accessing list of chains, if exception is thrown, e.g. structure file is empty, return fail with i_error = 1
    try:
        chains = models[0].get_list()
    except:
        print(f"\tWarning! No model in pdb: \"chains = models[0].get_list()\".\n\t\t\t(entry: {i}, pdb: "
              f"{pdb_id}:{chain_id})")
        return None, False, method, 1, '-', ''

    # If chain_id was unspecified by structure search tool, e.g. chain_id == '-', use first(/only) chain in structure
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
            print(f"\tWarning! Chain ID was not found in pdb file ({pdb_id}:{chain_id}).")
            return None, False, method, 2, '-', ''

    # If pdb is from rcsb database (indicated by len(id) <= 4), try computing uniprot to pdb index shift via EMBL-EBI
    # shift file (pdb_chain_uniprot.csv)
    if len(pdb_id) <= 4:
        if method != "alphafold":
            pdb_uni_map_entry = pdb_uni_map[(pdb_uni_map["PDB"] == pdb_id) & (pdb_uni_map["CHAIN"] == chain_id) &
                                            (pdb_uni_map["SP_PRIMARY"] == unip_id)]
            shift = compute_pdb_uniprot_shift(pdb_uni_map_entry) if not pdb_uni_map_entry.empty else None
        else:
            shift = None

        # If shift computation failed, attempt realigning pdb sequence to uniprot sequence; If alphafold is specified as
        # method already completly replace current structure model with new downloaded alphafold structure
        if shift is None or method == "alphafold":
            # Attempt realigning if method not alphafold
            pdb_seq = ''
            for res in chain.get_list():
                try:
                    pdb_seq += Polypeptide.three_to_one(res.get_resname())
                except:
                    continue
            unip_seq = data[f"seq_{site_id}"]
            method = "realigning" if method != "alphafold" else "alphafold"
            if method == "realigning":
                residue_pos = realign_unip_pos_in_pdb_seq(pdb_seq, unip_seq, data[f"pos_{site_id}"])
            else:
                residue_pos = None

            # If method alphafold or realingment attempt failed, replace with rcsb structure alphafold structure
            # and continue with method = "alphafold"
            if residue_pos is None or method == "alphafold":
                print(f"\tSelf computed res pos ({unip_id}, {data[f'pos_{site_id}']}): {residue_pos}\n"
                      f"\tThis position is not in range of the pdb_seq!")
                print("\tAttempt replacement alphafold download.")
                chain, new_path = replacement_alphafold_download(unip_id, data["path"])

                if chain is None:
                    # If alphafold replacement of structure failed, return fail with i_error = 4
                    print(f"\tReplacement alphafold download attempt returned an error ({unip_id} probably not found in"
                          f" database).\n\t\t\t(entry: {i}, unip: {unip_id}, pdb: {pdb_id}:{chain_id})")
                    return None, False, method, 4, '-', ''
                else:
                    method = "alphafold"
                    residue_pos = data[f"pos_{site_id}"]
                    try:
                        print(f"\tReplacement attempt successful (new residue: "
                              f"{Polypeptide.three_to_one(chain.__getitem__(residue_pos).get_resname())}).")
                    except:
                        pass
            # Else print computed position by realigning and continue with method = "realigning"
            else:
                print(f"\tSelf computed res pos ({unip_id}, {data[f'pos_{site_id}']}): {residue_pos}, "
                      f"fulfills residue criteria: {pdb_seq[residue_pos - 1] in df_xl_res.res.tolist()}:{pdb_seq[residue_pos - 1]}")
        # Else print position given by shift file and continue with method = "pdb_chain_uniprot"
        else:
            method = "pdb_chain_uniprot"
            residue_pos = data[f"pos_{site_id}"] + shift
            print(f"\tComputed res pos with pdb_chain_uniprot.csv ({unip_id}, {data[f'pos_{site_id}']}): {residue_pos}")
    # Else specified structure file is already an alphafold entry, thus continue with method = "alphafold"
    else:
        method = "alphafold"
        residue_pos = data[f"pos_{site_id}"]
        print(f"\tRes pos in alphafold entry ({unip_id}, {data[f'pos_{site_id}']}): {residue_pos}")

    # If method either pdb_chain_uniprot or alphafold, directly retrieve residue by index, else gather pdb sequence
    # and manually retrieve the i-th residue
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
    # If exception is thrown, attempt replacing structure with fresh alphafold download; if this fails as well, return
    # fail with i_error = 4
    except:
        print(f"\tWarning! Residue not found by id (maybe out of bounds).\n\t\t\t"
              f"(entry: {i}, pdb: {pdb_id}:{chain_id})")
        resseq_ids = [int(res.__repr__().split('=')[2].split(' ')[0]) for res in chain.get_list()]
        print(f"\t\t\tsearched pos: {residue_pos}, actual interval: ({min(resseq_ids)}, {max(resseq_ids)})")

        print("\tAttempt replacement alphafold download.")
        chain, new_path = replacement_alphafold_download(unip_id, data["path"])
        if chain is None:
            print(f"\tReplacement alphafold download attempt returned an error ({unip_id} probably not found in "
                  f"database).\n\t\t\t(entry: {i}, unip: {unip_id}, pdb: {pdb_id}:{chain_id})")
            return None, False, method, 4, '-', ''
        else:
            res = chain.__getitem__(residue_pos)
            try:
                print(f"\tReplacement attempt successful (new residue: {Polypeptide.three_to_one(res.get_resname())}).")
            except:
                pass
    # Check whether residue criteria is fulfilled, if not attempt final alphafold replacement; Check whether a valid CB is
    # accessible for specified residue, else return fail with i_error = 6
    try:
        # Check whether specified residue has valid name, else return fail with i_error = 5
        try:
            resname = Polypeptide.three_to_one(res.get_resname())
        except:
            print(f"\tWarning! Got non-aminoacid at residue position ({res.get_resname()}).\n\t\t\t"
                  f"(entry: {i}, pdb: {pdb_id}:{chain_id})")
            return None, False, method, 5, '-', ''
        res_criteria = (resname in df_xl_res.res.tolist()) and \
                       (resname == data[f'seq_{site_id}'][data[f'pos_{site_id}'] - 1])
        print(f"\tFinal residue is '{resname}' (thus res_criteria_{site_id}: {res_criteria})")
        # If residue criteria fulfilled return result
        if res_criteria:
            try:
                _ = res["CB"]
                return int(res.get_id()[1]), res_criteria, method, -1,\
                       res["CB"].get_bfactor() if method == "alphafold" else '-', new_path
            except:
                pass
        # Else attempt final alphafold replacement, if this fails return fail with i_error = 4
        print("\tAttempt replacement alphafold download.")
        chain, new_path = replacement_alphafold_download(unip_id, data["path"])
        if chain is None:
            print(f"\tReplacement alphafold download attempt returned an error ({unip_id} probably not found in "
                  f"database).\n\t\t\t(entry: {i}, unip: {unip_id}, pdb: {pdb_id}:{chain_id})")
            return None, False, method, 4, '-', ''
        else:
            # Check whether specified residue by alphafold has valid name, else return fail with i_error = 5
            try:
                method = "alphafold"
                residue_pos = data[f"pos_{site_id}"]
                res = chain.__getitem__(residue_pos)
                print(f"\tReplacement attempt successful "
                      f"(new residue: {Polypeptide.three_to_one(res.get_resname())}).")
                resname = Polypeptide.three_to_one(res.get_resname())
                res_criteria = resname in df_xl_res.res.tolist()
                print(f"\tFinal residue is '{resname}' (thus res_criteria_{site_id}: {res_criteria})")
                return int(res.get_id()[1]), res_criteria, method, -1, res["CB"].get_bfactor(), new_path
            except:
                print(f"\tWarning! Got non-aminoacid at residue position ({res.get_resname()}).\n\t\t\t"
                      f"(entry: {i}, pdb: {pdb_id}:{chain_id})")
                return None, False, method, 5, '-', ''
    except:
        print(f"\tWarning! No C-beta found ({res.get_resname()}).\n\t\t\t"
              f"(entry: {i}, pdb: {pdb_id}:{chain_id})")
        return None, False, method, 6, '-', ''


def compute_pdb_uniprot_shift(pdb_uni_map_entry):
    # Compute shift by a finding entry with closely related indeces (neighbours) for pdb and uniprot, search through
    # entries recursively until either satisfying result found, or dataset empty (in the latter case return None)
    #
    # input pdb_uni_map_entry: pd.DataFrame
    # return shift: int

    # Set acceptable neighbour ranges
    neighbours_beg = (int(pdb_uni_map_entry["SP_BEG"].iloc[0])-1, int(pdb_uni_map_entry["SP_BEG"].iloc[0])+2)
    neighbours_end = (int(pdb_uni_map_entry["SP_END"].iloc[0])-1, int(pdb_uni_map_entry["SP_END"].iloc[0])+2)

    # If pdb start is not None and in range, return shift
    if pdb_uni_map_entry["PDB_BEG"].iloc[0] != "None" and \
            int(pdb_uni_map_entry["PDB_BEG"].iloc[0]) in range(neighbours_beg[0], neighbours_beg[1]):
        return int(pdb_uni_map_entry["PDB_BEG"].iloc[0]) - int(pdb_uni_map_entry["SP_BEG"].iloc[0])
    # Elif pdb end is not None and in range, return shift
    elif pdb_uni_map_entry["PDB_END"].iloc[0] != "None" and \
            int(pdb_uni_map_entry["PDB_END"].iloc[0]) in range(neighbours_end[0], neighbours_end[1]):
        return int(pdb_uni_map_entry["PDB_END"].iloc[0]) - int(pdb_uni_map_entry["SP_END"].iloc[0])
    # Else if dataset not empty, recursively call function again with dataset except first entry, else return None
    else:
        if not pdb_uni_map_entry[1:].empty:
            return compute_pdb_uniprot_shift(pdb_uni_map_entry[1:])
        else:
            return None


def realign_unip_pos_in_pdb_seq(pdb_seq, unip_seq, unip_pos):
    # Realign pdb sequence to uniprot sequence, and compute position of residue in pdb sequence which is specified by
    # unip_pos in uniprot sequence, if this fails return None
    #
    # input pdb_seq: str, unip_seq: str, unip_pos: int
    # return pdb_pos: int

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
    print(f"\t\tAlignment:\n{alignment}")
    aligned_pdb_seq = str(alignment).split('\n')[0]
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

    # Find unip_pos in aligned pdb sequence and compute according pdb_pos in unaligned pdb sequence, return pdb_pos if
    # successful, else return None
    try:
        _ = aligned_pdb_seq[aligned_unip_i + 1]
        pdb_pos = len(aligned_pdb_seq[:aligned_unip_i + 1].replace(' ', '').replace('-', ''))
        if pdb_pos > 0:
            al_seq = str(alignment).split('\n')[1]
            print(f"\t\tAligned site (index: {aligned_unip_i}):\n"
                  f"\t\t\t{aligned_pdb_seq[aligned_unip_i]}\n"
                  f"\t\t\t{al_seq[aligned_unip_i]}\n"
                  f"\t\t\t{aligned_unip_seq[aligned_unip_i]}")
            return pdb_pos
        else:
            return None
    except IndexError:
        return None


def replacement_alphafold_download(unip_id, path):
    # Attempt to download a replacement alphafold structure model (also return path to new pdb),
    # return None if attempt fails
    #
    # input unip_id: str, path: str
    # return chain: Bio.PDB.Chain, new_path: str

    #ex.: data/out/structure_search/blastp_6G2J.pdb
    new_path = f"{'_'.join(path.split('_')[:-2])}_af{unip_id}.pdb"
    if not os.path.exists(new_path):
        URL = f"https://alphafold.ebi.ac.uk/files/AF-{unip_id}-F1-model_v1.pdb"
        with open(new_path, 'w') as f:
            try:
                f.write(r.get(URL).text)
            except ConnectionError as e:
                print("No connection to AlphaFold API possible. Please try again later.")
                print(e)
                sys.exit()
    try:
        return PDBParser().get_structure('', new_path).get_list()[0].get_list()[0], new_path
    except:
        return None, ''
