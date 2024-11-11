import os
import numpy as np
import warnings
import pandas as pd
import concurrent.futures

from Bio.PDB import Polypeptide, PDBParser, MMCIFParser, Select, PDBIO

from claudio.utils.utils import verbose_print, round_self

warnings.filterwarnings("ignore")


def calculate_site_dists(data: pd.DataFrame, temp_dir: str, df_xl_res: pd.DataFrame, plddt_cutoff: float, topolink_bin: str | None,
                          verbose_level: int):
    """
    calculate distances between interaction sites, and extend input dataset by res_criteria, e.g. whether the found
    sites satisfy the criteria of being the specified residue, the method used to find the sites in the structure
    file, in case said method was alphafold the pLDDT, e.g. confidence, value and finally the computed distances
    
    Parameters
    ----------
    data : pd.DataFrame,
    temp_dir : str,
    df_xl_res : pd.DataFrame,
    plddt_cutoff : float,
    topolink_bin : str | None,
    verbose_level : int

    Returns
    -------
    data : pd.DataFrame
    """

    # Compute euclidean and topological distance of interacting residues with topolink and add them all to the dataset
    data = compute_dists_with_topolink(data, temp_dir, df_xl_res, plddt_cutoff, topolink_bin, verbose_level)

    return data


def compute_dists_with_topolink(data: pd.DataFrame, temp_dir: str, df_xl_res: pd.DataFrame, plddt_cutoff: float, topolink_bin: str | None,
                                 verbose_level: int):
    """
    compute euclidean and topological distances between residues utilizing topolink software, also saves logs of
    topolink computation into temporary folder (careful: contents of this folder will be fully deleted each time this
    script is executed)
    
    Parameters
    ----------
    data : pd.DataFrame,
    temp_dir : str,
    df_xl_res : pd.DataFrame,
    plddt_cutoff : float,
    topolink_bin : str | None,
    verbose_level : int

    Returns 
    -------
    data : pd.DataFrame
    """

    toplink_dists = []
    ind = 0
    structures = {}
    
    # create directory for topolink input files
    os.makedirs(f"{temp_dir}in/", exist_ok=True)
    # create directory for topolink structures
    os.makedirs(f"{temp_dir}struct/", exist_ok=True)

    # delete contents in temporary save
    files = [f"{temp_dir}{f}" for f in os.listdir(temp_dir)
             if f != '_.txt' and os.path.isfile(f"{temp_dir}{f}")]
    files.extend([f"{temp_dir}in/{f}" for f in os.listdir(f"{temp_dir}in/") if os.path.isfile(f"{temp_dir}in/{f}")])
    files.extend([f"{temp_dir}struct/{f}" for f in os.listdir(f"{temp_dir}struct/") if os.path.isfile(f"{temp_dir}struct/{f}")])
    for f in files:
        os.remove(f)


    # Iterate over unique structures
    len_structures = len(data["path"].unique())
    for structure in sorted(data["path"].unique()):
        verbose_print(f"\r\tWrite inputs for Topolink:[{round_self((ind * 100) / len_structures, 2)}%]", 1, verbose_level,end='')

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
            structure = isolate_pdb_chain(structure, pdb_id, temp_dir, np.unique(subset[["chain_a", "chain_b"]].values))
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
        subset = subset[subset["res_criteria_fulfilled"] & subset["is_interfaced"]]
        for i, row in subset.iterrows():
            # Set boolean for whether pLDDT cutoff is unfulfilled if the used method was alphafold
            plddt_unfulfilled = (row["method_a"] == "alphafold") and \
                                ((row["pLDDT_a"] != '-' and (float(row["pLDDT_a"]) < plddt_cutoff)) or \
                                 (row["pLDDT_b"] != '-' and (float(row["pLDDT_b"]) < plddt_cutoff)))
            # Don't compute dist for datapoints which do not fulfill the residue, interface criteria, or pLDDT cutoff
            if not plddt_unfulfilled:
                try:
                    # observed LYS A 468 LYS A 457
                    # LINK: LYS A 457 CA LYS A 468 CA 11.814 12.568 YES 0.000 35.000 OK: FOUND 1 / 1 1 / 1 YY YY
                    link_strs = [
                        ' '.join([Polypeptide.one_to_three(row['seq_a'][row['pos_a'] - 1]), row['chain_a'],
                                  str(int(row['pdb_pos_a']))]),
                        ' '.join([Polypeptide.one_to_three(row['seq_b'][row['pos_b'] - 1]), row['chain_b'],
                                  str(int(row['pdb_pos_b']))])]
                    if link_strs not in known_link_strs:
                        obs_str += f"  observed {' '.join(link_strs)}\n"
                        obs_inds.append((i, link_strs, False))
                        known_link_strs.append(link_strs)
                        known_link_strs.append([link_strs[1], link_strs[0]])
                except:
                    continue

        # Creates inputfile for topolink, utilizing templatefile: data/topolink_inputfile.inp
        topo_in = []
        project_path = '/'.join(os.path.abspath(__file__).replace('\\\\', '/').replace('\\', '/').split('/')[:-4])
        project_path = project_path + '/' if project_path else ""
        for line in [l for l in open(f"{project_path}data/topolink_inputfile.inp", 'r').readlines()
                     if not l.startswith('#')]:
            if line.startswith("linkdir"):
                topo_in.append(f"linkdir {temp_dir}\n")
            elif line.startswith("structure"):
                topo_in.append(f"structure {structure}\n")
            elif line.startswith("  observed"):
                topo_in.append(obs_str)
            elif line.startswith("  linktype"):
                # "  linktype   MET     all      1       N           LYS     all     all       CB        35"
                for i, row_a in df_xl_res.iterrows():
                    for _, row_b in df_xl_res.iloc[i:].iterrows():
                        type_str = ' '.join(["  linktype",
                                             Polypeptide.one_to_three(row_a.res), "all", "all", row_a.atom,
                                             Polypeptide.one_to_three(row_b.res), "all", "all", row_b.atom,
                                             "35"])
                        topo_in.append(type_str + '\n')
            else:
                topo_in.append(line)
        topo_in = ''.join(topo_in)
        # Write inputfile to temporary path (will be overwritten during next iteration)
        with open(f"{temp_dir}in/topo_{pdb_id}_.tmp", 'w') as f:
            f.write(topo_in)
        structures[pdb_id] = [obs_inds,topo_in]

        ind += 1
        verbose_print(f"\r\tWrite inputs for Topolink:[{round_self((ind * 100) / len_structures, 2)}%]", 1, verbose_level,end='')

    verbose_print("", 1, verbose_level)
    in_files = [os.path.join(f"{temp_dir}in/", f) for f in os.listdir(f"{temp_dir}in/") if os.path.isfile(os.path.join(f"{temp_dir}in/", f))]
    ind = 0

    def topo_task(input):
        pdb_id = input.split('_')[-2]
        topo_in = structures[pdb_id][1]
        # Run topolink and pop terminal print to variable
        topolink_call = "topolink" if topolink_bin is None else f"{topolink_bin}topolink"
        res = os.popen(f"\"{topolink_call}\" \"{input}\"").read()
        # Write both input and output to temporary file marked by pdb id, e.g. topo_1b0j.log, topo_afA2ASZ8.log, ...
        # in case the user wishes to review them later
        with open(f"{temp_dir}topo_{pdb_id}.log", 'w') as f:
            f.write(f"IN:\n{topo_in}\n\n\nOUT:\n{res}")
        structures[pdb_id] = structures[pdb_id] + [res]
        return None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(topo_task, input): input for input in in_files}
        verbose_print(f"\r\tTopoLink:[{round_self((ind * 100) / len(in_files), 2)}%]", 1, verbose_level,end='')

    for future in concurrent.futures.as_completed(futures):
        try:
            ind += 1
            verbose_print(f"\r\tTopoLink:[{round_self((ind * 100) / len(in_files), 2)}%]", 1, verbose_level,end='')
            del futures[future]
        except Exception as e:
            print(e)

    for container in structures.values():
        obs_inds = container[0]
        res = container[2]
        # zip topolink results with obs_inds
        # -> toplink_dists = [(index, eucl_dist, top_dist), ...]
        link_results = [' '.join(line.split()) for line in res.split('\n') if line.startswith("  LINK:")]
        for link_result in link_results:
            for i, obs_ind in enumerate(obs_inds):
                data_index, link_strs, _ = obs_ind
                # Check whether any possible first link string of observation is in result, and check whether any
                # possible second is in result (after removing the first string)
                if any([(link_strs[0] + f" {atom_a}" in link_result) and
                        (link_strs[1] + f" {atom_b}" in link_result.replace(link_strs[0] + f" {atom_a}", ''))
                        for atom_a in df_xl_res.atom for atom_b in df_xl_res.atom]):
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

    verbose_print("", 1, verbose_level)

    # Initialize topolink columns for euclidean and topological distances
    data["eucl_dist_tplk"] = float("Nan")
    data["topo_dist_tplk"] = float("Nan")

    # For zipped distances in collection, replace them at specified index in dataset
    for dist in toplink_dists:
        index, eucl_dist, top_dist = dist
        data.loc[index, "eucl_dist_tplk"] = round_self(eucl_dist, 3)
        data.loc[index, "topo_dist_tplk"] = round_self(top_dist, 3)

    # Fill topolink distances with zero, if positions equal
    data["eucl_dist_tplk"] = data.apply(lambda x: 0.0 if (x.pos_a == x.pos_b) &
                                                         (x.unip_id_a == x.unip_id_b) &
                                                         (x.chain_a == x.chain_b) else x.eucl_dist_tplk, axis=1)
    data["topo_dist_tplk"] = data.apply(lambda x: 0.0 if (x.pos_a == x.pos_b) &
                                                         (x.unip_id_a == x.unip_id_b) &
                                                         (x.chain_a == x.chain_b) else x.topo_dist_tplk, axis=1)

    return data


def isolate_pdb_chain(path: str, pdb_id: str, temp_dir: str, chain_ids: list[str]):
    """
    isolate chains with cross-links and write only those chains to pdb

    Parameters
    ----------
    path : str,
    pdb_id : str,
    temp_dir : str,
    chain_ids : list[str]

    Returns
    -------
    new_path : str
    """

    try:
        structure = PDBParser().get_structure('', path).get_list()[0]
    except:
        structure = MMCIFParser().get_structure('', path).get_list()[0]

    # overload chain accept method
    class ChainSelect(Select):
        def accept_chain(self, chain):
            if chain.__repr__().split('=')[1][0] in chain_ids:
                return True
            else:
                return False

    # save new pdb to temporary pdb path
    new_path = f"{temp_dir}struct/{pdb_id}_tmp.pdb"
    io = PDBIO()
    io.set_structure(structure)
    io.save(new_path, ChainSelect())

    return new_path
