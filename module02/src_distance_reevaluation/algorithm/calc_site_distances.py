import pandas as pd
from Bio.PDB import Polypeptide, PDBParser, MMCIFParser, Select, PDBIO
import numpy as np
import warnings
import os

warnings.filterwarnings("ignore")


def calculate_site_dists(data, plddt_cutoff, intra_only, topolink_bin):
    # calculate distances between interaction sites, and extend input dataset by res_criteria, e.g. whether the found
    # sites satisfy the criteria of being the specified residue, the method used to find the sites in the structure
    # file, in case said method was alphafold the pLDDT, e.g. confidence, value and finally the computed distances
    #
    # input data: pd.DataFrame, plddt_cutoff: float, intra_only: bool, topolink_bin: str/None
    # return data: pd.DataFrame

    # Self-compute euclidean distances in structures
    self_eucl_dists = []
    for i, row in data.iterrows():
        # If both pdb positions were found, compute euclidean distance and add it to distances, else add Nan
        if (not pd.isna(row["pdb_pos_a"])) and (not pd.isna(row["pdb_pos_b"])):
            # Set boolean for whether pLDDT cutoff is unfulfilled if the used method was alphafold
            plddt_unfulfilled = (row["method_a"] == "alphafold") and \
                                ((float(row["pLDDT_a"]) < plddt_cutoff) or (float(row["pLDDT_b"]) < plddt_cutoff))
            # If no structure file given for interaction or residue criteria fulfilled or pLDDT unfulfilled,
            # add Nan to distances
            if row["path"] == '-' or not row["res_criteria_fulfilled"] or plddt_unfulfilled:
                self_eucl_dists.append(float("Nan"))
            # Else load structure (either with normal PDBParser or MMCIFParser)
            else:
                try:
                    chains = PDBParser().get_structure('', row["path"]).get_list()[0].get_list()
                except:
                    chains = MMCIFParser().get_structure('', row["path"]).get_list()[0].get_list()
                # If used method is alphafold, the required chain is always A (e.g. the first in the structure)
                if row["method_a"] == "alphafold":
                    chain_a = chains[0]
                    chain_b = chains[0]
                    chain_a_found = True
                    chain_b_found = True
                # Else search for matching chain by chain_id
                else:
                    chain_a_found = False
                    chain_b_found = False
                    for c in chains:
                        if c.__repr__().split('=')[1][0] == row["chain" if intra_only else "chain_a"]:
                            chain_a = c
                            chain_a_found = True
                            if intra_only:
                                chain_b = c
                                chain_b_found = True
                                break
                            elif chain_b_found:
                                break
                        if not intra_only and c.__repr__().split('=')[1][0] == row["chain_b"]:
                            chain_b = c
                            chain_b_found = True
                            if chain_a_found:
                                break

                # If chains were not successfully found add Nan to distances
                if not (chain_a_found and chain_b_found):
                    self_eucl_dists.append(float("Nan"))
                # Else try accessing coordinates to compute euclidean distance
                else:
                    res_a = chain_a.__getitem__(int(row["pdb_pos_a"]))
                    res_b = chain_b.__getitem__(int(row["pdb_pos_b"]))
                    try:
                        eucl_dist = np.sqrt(np.sum((res_a["CB"].get_coord() - res_b["CB"].get_coord()) ** 2))
                        self_eucl_dists.append(eucl_dist)
                    except:
                        self_eucl_dists.append(float("Nan"))
        else:
            self_eucl_dists.append(float("Nan"))

    # Add self-computed euclidean distances to dataset
    data["eucl_dist"] = [round_self(dist, 3) for dist in self_eucl_dists]
    # Compute euclidean and topological distance of interacting residues with topolink and add them all to the dataset
    data = compute_dists_with_topolink(data, plddt_cutoff, intra_only, topolink_bin)

    return data


def compute_dists_with_topolink(data, plddt_cutoff, intra_only, topolink_bin):
    # compute euclidean and topological distances between residues utilizing topolink software, also saves logs of
    # topolink computation into temporary folder "data/temp/dist_reeval" (careful: contents of this folder will be fully
    # deleted each time this script is executed
    #
    # input data: pd.DataFrame, plddt_cutoff: float, intra_only: bool, topolink_bin: str/None
    # return data: pd.DataFrame

    toplink_dists = []
    ind = 0

    # delete contents in temporary save
    project_path = '/'.join(os.path.abspath(__file__).split('/')[:-4])
    project_path = project_path + '/' if project_path else ""
    files = [f"{project_path}data/temp/dist_reeval/{f}" for f in os.listdir(f"{project_path}/data/temp/dist_reeval/")]
    for f in files:
        os.remove(f)

    # Iterate over unique structures
    for structure in sorted(data["path"].unique()):
        print(f"\r\t[{round((ind * 100) / len(data['path'].unique()), 2)}%]", end='')

        # subselect only interactions belonging to structure
        subset = data[data["path"] == structure]

        # If empty structure marker found, skip this iteration
        if structure == '-':
            ind += 1
            continue
        # If not empty structure marker found, save pdb id and isolate needed chains from structure to reduce
        # computation
        else:
            pdb_id = structure.split('_')[-1].split('.')[0]
            structure = isolate_pdb_chain(
                structure, subset["chain"].unique() if intra_only else np.unique(subset[["chain_a", "chain_b"]].values))
            # Check again if isolation of chains was successful, if not skip iteration
            if structure == '-':
                ind += 1
                continue

        # obs_inds is container to save tuples: (index of observation in dataset, string of observed link, boolean
        # whether link was found in topolink results (initialized as False))
        # obs_str is string of collected observed link strings for inputfile
        obs_inds = []
        obs_str = ''
        known_link_strs = []
        for i, row in subset.iterrows():
            # Set boolean for whether pLDDT cutoff is unfulfilled if the used method was alphafold
            plddt_unfulfilled = (row["method_a"] == "alphafold") and \
                                ((float(row["pLDDT_a"]) < plddt_cutoff) or (float(row["pLDDT_b"]) < plddt_cutoff))
            # Don't compute dist for datapoints which do not fulfill the residue criteria, or pLDDT cutoff
            if row["res_criteria_fulfilled"] and not plddt_unfulfilled:
                try:
                    # observed LYS A 468 LYS A 457
                    # LINK: LYS A 457 CA LYS A 468 CA 11.814 12.568 YES 0.000 35.000 OK: FOUND 1 / 1 1 / 1 YY YY
                    link_strs = [
                        ' '.join([Polypeptide.one_to_three(row['seq' if intra_only else 'seq_a'][row['pos_a'] - 1]),
                                  row['chain' if intra_only else 'chain_a'], str(int(row['pdb_pos_a']))]),
                        ' '.join([Polypeptide.one_to_three(row['seq' if intra_only else 'seq_b'][row['pos_b'] - 1]),
                                  row['chain' if intra_only else 'chain_b'], str(int(row['pdb_pos_b']))])]
                    if link_strs not in known_link_strs:
                        obs_str += f"  observed {' '.join(link_strs)}\n"
                        obs_inds.append((i, link_strs, False))
                        known_link_strs.append(link_strs)
                        known_link_strs.append([link_strs[3], link_strs[4], link_strs[5],
                                                link_strs[0], link_strs[1], link_strs[2]])
                except:
                    continue

        # Creates inputfile for topolink, utilizing templatefile: data/in/topolink_inputfile.inp
        topo_in = []
        project_path = '/'.join(os.path.abspath(__file__).split('/')[:-4])
        project_path = project_path + '/' if project_path else ""
        for line in open(f"{project_path}data/in/topolink_inputfile.inp", 'r').readlines():
            if line.startswith("linkdir"):
                topo_in.append(f"linkdir {project_path}data/temp/dist_reeval")
            elif line.startswith("structure"):
                topo_in.append(f"structure {structure}")
            elif line.startswith("  observed"):
                topo_in.append(obs_str)
            else:
                topo_in.append(line)
        topo_in = ''.join(topo_in)
        # Write inputfile to temporary path (will be overwritten during next iteration)
        with open(f"{project_path}data/temp/dist_reeval/topo.tmp", 'w') as f:
            f.write(topo_in)

        # Run topolink and pop terminal print to variable
        topolink_call = "topolink" if topolink_bin is None else f"{topolink_bin}topolink"
        res = os.popen(f"{topolink_call} {project_path}data/temp/dist_reeval/topo.tmp").read()
        # Write both input and output to temporary file marked by pdb id, e.g. topo_1b0j.log, topo_afA2ASZ8.log, ...
        # in case the user wishes to review them later
        with open(f"{project_path}data/temp/dist_reeval/topo_{pdb_id}.log", 'w') as f:
            f.write(f"IN:\n{topo_in}\n\n\nOUT:\n{res}")

        # zip topolink results with obs_inds
        # -> toplink_dists = [(index, eucl_dist, top_dist), ...]
        link_results = [' '.join(line.split()) for line in res.split('\n') if line.startswith("  LINK:")]
        for link_result in link_results:
            for i, obs_ind in enumerate(obs_inds):
                data_index, link_strs, _ = obs_ind
                # Check whether first link string of observation is in result, and check whether second is in result
                # (after removing the first string)
                if (link_strs[0] + " CB" in link_result) and \
                        (link_strs[1] + " CB" in link_result.replace(link_strs[0] + " CB", '')):
                    tplk_eucl = link_result.split(' ')[9]
                    tplk_topo = link_result.split(' ')[10]
                    # Check whether both distances computed by topolink did not pass the threshold,
                    # if so directly save them as floats to zipped distance collection
                    # and change according boolean in obs_inds to True (because it was found in the results of topolink)
                    if (not tplk_eucl.startswith('>')) and (not tplk_topo.startswith('>')):
                        toplink_dists.append((data_index, float(tplk_eucl), float(tplk_topo)))
                        obs_inds[i] = (data_index, link_strs, True)
                    # If euclidean distance by topolink surpasses threshold truncate greater-symbol,
                    # save both distances' float values to zipped distance collection
                    # and change according boolean in obs_inds to True (because it was found in the results of topolink)
                    elif tplk_eucl.startswith('>'):
                        toplink_dists.append((data_index, float(tplk_eucl.replace('>', '')), float(tplk_topo)))
                        obs_inds[i] = (data_index, link_strs, True)
                    # If topological distance by topolink surpasses threshold truncate greater-symbol,
                    # save both distances' float values to zipped distance collection
                    # and change according boolean in obs_inds to True (because it was found in the results of topolink)
                    elif tplk_topo.startswith('>'):
                        toplink_dists.append((data_index, float(tplk_eucl), float(tplk_topo.replace('>', ''))))
                        obs_inds[i] = (data_index, link_strs, True)
                    break
        # Iterate over observations again and check whether all were found (e.g. check boolean in tuples), if not save
        # Nans to zipped distance collection
        for obs_ind in obs_inds:
            data_index, _, obs_res_found = obs_ind
            if not obs_res_found:
                toplink_dists.append((data_index, float('Nan'), float('Nan')))

        ind += 1
        print(f"\r\t[{round((ind * 100) / len(data['path'].unique()), 2)}%]", end='')
    print()

    # Initialize topolink columns for euclidean and topological distances
    data["eucl_dist_tplk"] = float("Nan")
    data["topo_dist_tplk"] = float("Nan")

    # For zipped distances in collection, replace them at specified index in dataset
    for dist in toplink_dists:
        index, eucl_dist, top_dist = dist
        data.loc[index, "eucl_dist_tplk"] = round_self(eucl_dist, 3)
        data.loc[index, "topo_dist_tplk"] = round_self(top_dist, 3)

    # Fill topolink distances with zero, if self-computed distance is zero
    data["eucl_dist_tplk"] = data.apply(lambda x: 0.0 if x.eucl_dist == 0 else x.eucl_dist_tplk, axis=1)
    data["topo_dist_tplk"] = data.apply(lambda x: 0.0 if x.eucl_dist == 0 else x.topo_dist_tplk, axis=1)

    return data


def isolate_pdb_chain(path, chain_ids):
    # isolate chain with interaction and write only this chain to pdb
    #
    # input path: str, chain_ids: list(str)
    # return new_path: str

    # Parse pdb structure
    try:
        structure = PDBParser().get_structure('', path)
    except:
        structure = MMCIFParser().get_structure('', path)

    # overload chain accept method
    class ChainSelect(Select):
        def accept_chain(self, chain):
            if chain.__repr__().split('=')[1][0] in chain_ids:
                return True
            else:
                return False

    # save new pdb to temporary pdb path
    project_path = '/'.join(os.path.abspath(__file__).split('/')[:-4])
    project_path = project_path + '/' if project_path else ""
    new_path = f"{project_path}data/temp/dist_reeval/tmp.pdb"
    io = PDBIO()
    io.set_structure(structure)
    io.save(new_path, ChainSelect())

    return new_path


def round_self(value, decimals):
    # simple decimal rounding function (python by itself has a tendency to round fragmented with the buit-in function)
    #
    # input value: float, decimals: int
    # return rounded_value: float/int

    # If decimal less than 1, the resulting value will be an integer
    if pd.isna(value):
        return float("Nan")
    if decimals < 1:
        rounded_value = int(int((value * (10 ** decimals)) + .5) / (10 ** decimals))
        return rounded_value
    # Else, the resulting value will be a float
    else:
        rounded_value = int((value * (10 ** decimals)) + .5) / (10 ** decimals)
        return rounded_value
