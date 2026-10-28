"""calculates distances between interacting residues as part of Module02's
structural analysis submodule, utilizing topolink software to compute
topological and euclidean distances"""
import concurrent.futures
import os
import warnings
import numpy as np
import pandas as pd

from Bio.PDB import Polypeptide, PDBParser, FastMMCIFParser, Select, PDBIO

from claudio.utils.structure_io import read_structure_models
from claudio.utils.utils import verbose_print, round_self

warnings.filterwarnings("ignore")


def calculate_site_dists(data: pd.DataFrame, temp_dir: str,
                         df_xl_res: pd.DataFrame, plddt_cutoff: float,
                         topolink_bin: str | None, verbose_level: int):
    """
    calculate distances between interaction sites, and extend input dataset 
    by res_criteria, e.g. whether the found sites satisfy the criteria of 
    being the specified residue, the method used to find the sites in the 
    structure file, in case said method was alphafold the pLDDT, e.g. 
    confidence, value and finally the computed distances
    
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

    # Compute euclidean and topological distance of interacting residues with
    # topolink and add them all to the dataset
    data = compute_dists_with_topolink(data, temp_dir, df_xl_res,
                                       plddt_cutoff, topolink_bin,
                                       verbose_level)

    return data


def compute_dists_with_topolink(data: pd.DataFrame, temp_dir: str,
                                df_xl_res: pd.DataFrame, plddt_cutoff: float,
                                topolink_bin: str | None, verbose_level: int):
    """
    compute euclidean and topological distances between residues utilizing 
    topolink software, also saves logs of topolink computation into temporary 
    folder (careful: contents of this folder will be fully deleted each time 
    this script is executed)
    
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

    # create directory for topolink input files
    os.makedirs(f"{temp_dir}in/", exist_ok=True)
    # create directory for topolink structures
    os.makedirs(f"{temp_dir}struct/", exist_ok=True)

    # delete contents in temporary save
    files = [f"{temp_dir}{f}" for f in os.listdir(temp_dir)
             if f != '_.txt' and os.path.isfile(f"{temp_dir}{f}")]
    files.extend([f"{temp_dir}in/{f}" for f in os.listdir(f"{temp_dir}in/")
                  if os.path.isfile(f"{temp_dir}in/{f}")])
    files.extend([f"{temp_dir}struct/{f}"
                  for f in os.listdir(f"{temp_dir}struct/")
                  if os.path.isfile(f"{temp_dir}struct/{f}")])
    for f in files:
        os.remove(f)


    # Iterate over unique structures
    len_structures = len(data["path"].unique())
    def topo_task(structure):
        nonlocal ind
        # subselect only interactions belonging to structure
        subset = data[data["path"] == structure]

        # If empty structure marker found, skip this iteration
        if structure == '-':
            ind += 1
            return
        # If not empty structure marker found, save pdb id and isolate needed
        # chains from structure to reduce
        # computation
        pdb_id = os.path.basename(structure).split('_')[-1].split('.')[0]
        chain_ids = np.unique(subset[["chain_a", "chain_b"]].values)
        chain_map = build_topolink_chain_map(chain_ids)
        structure, residue_map = prepare_topolink_structure(
            structure, pdb_id, temp_dir, chain_ids,
        )
        # Check again if isolation of chains was successful,
        # if not skip iteration
        if structure == '-':
            ind += 1
            return

        # obs_inds stores (list of row indices, link strings, result_found).
        # obs_str is string of collected observed link strings for inputfile
        obs_inds = []
        obs_str = ''
        known_link_groups = {}
        subset = subset[subset["res_criteria_fulfilled"]
                        & subset["is_interfaced"]]
        for row in subset.itertuples():
            i = row.Index
            # Set boolean for whether pLDDT cutoff is unfulfilled if the used
            # method was alphafold
            plddt_unfulfilled = (row.method_a == "alphafold") and \
                                ((row.pLDDT_a != '-' and (float(row.pLDDT_a) < plddt_cutoff)) or \
                                 (row.pLDDT_b != '-' and (float(row.pLDDT_b) < plddt_cutoff)))
            # Don't compute dist for datapoints which do not fulfill
            # the residue, interface criteria, or pLDDT cutoff
            if not plddt_unfulfilled:
                try:
                    # observed LYS A 468 LYS A 457
                    # LINK: LYS A 457 CA LYS A 468 CA 11.814 12.568 YES 0.000 35.000 OK: FOUND 1 / 1 1 / 1 YY YY
                    topolink_pos_a = resolve_topolink_position(row, "a", residue_map)
                    topolink_pos_b = resolve_topolink_position(row, "b", residue_map)
                    if topolink_pos_a is None or topolink_pos_b is None:
                        continue

                    link_strs = [
                        ' '.join([
                            Polypeptide.one_to_three(row.seq_a[row.pos_a - 1]),
                            chain_map[row.chain_a], str(topolink_pos_a),
                        ]),
                        ' '.join([
                            Polypeptide.one_to_three(row.seq_b[row.pos_b - 1]),
                            chain_map[row.chain_b], str(topolink_pos_b),
                        ]),
                    ]
                    link_key = tuple(sorted(link_strs))
                    if link_key in known_link_groups:
                        known_link_groups[link_key].append(i)
                    else:
                        known_link_groups[link_key] = [i]
                        obs_str += f"  observed {' '.join(link_strs)}\n"
                        obs_inds.append(
                            (known_link_groups[link_key], link_strs, False)
                        )
                except:
                    continue

        if not obs_inds:
            ind += 1
            return

        # Creates inputfile for topolink,
        # utilizing templatefile: data/topolink_inputfile.inp
        topo_in = []
        project_path = '/'.join(os.path.abspath(__file__).replace('\\\\', '/').replace('\\', '/').split('/')[:-4])
        project_path = project_path + '/' if project_path else ""
        for line in [l for l in open(f"{project_path}data/topolink_inputfile.inp", 'r',
                                     encoding="utf-8").readlines()
                     if not l.startswith('#')]:
            if line.startswith("linkdir"):
                topo_in.append(f"linkdir {temp_dir}\n")
            elif line.startswith("structure"):
                topo_in.append(f"structure {structure}\n")
            elif line.startswith("  observed"):
                topo_in.append(obs_str)
            elif line.startswith("  linktype"):
                # "  linktype   MET     all      1       N           LYS     all     all       CB        35"
                for row_a in df_xl_res.itertuples():
                    i = row_a.Index
                    for row_b in df_xl_res.iloc[i:].itertuples():
                        type_str = ' '.join(["  linktype",
                                             Polypeptide.one_to_three(row_a.res),
                                             "all", "all", row_a.atom,
                                             Polypeptide.one_to_three(row_b.res),
                                             "all", "all", row_b.atom,
                                             "35"])
                        topo_in.append(type_str + '\n')
            else:
                topo_in.append(line)
        topo_in = ''.join(topo_in)
        # Write inputfile to temporary path
        # (will be overwritten during next iteration)
        topo_input_path = f"{temp_dir}in/topo_{pdb_id}_.tmp"
        with open(topo_input_path, 'w', encoding="utf-8") as f:
            f.write(topo_in)

        # Run topolink and pop terminal print to variable
        topolink_call = "topolink" if topolink_bin is None else f"{topolink_bin}topolink"
        res = os.popen(f"\"{topolink_call}\" \"{topo_input_path}\"").read()
        # Write both input and output to temporary file marked by pdb id,
        #  e.g. topo_1b0j.log, topo_afA2ASZ8.log, ...
        # in case the user wishes to review them later
        with open(f"{temp_dir}topo_{pdb_id}.log", 'w', encoding="utf-8") as f:
            f.write(f"IN:\n{topo_in}\n\n\nOUT:\n{res}")


        # zip topolink results with obs_inds
        # -> toplink_dists = [(index, eucl_dist, top_dist), ...]
        link_results = [' '.join(line.split())
                        for line in res.split('\n') if line.startswith("  LINK:")]
        for link_result in link_results:
            for i, obs_ind in enumerate(obs_inds):
                data_index, link_strs, _ = obs_ind
                # Check whether any possible first link string of observation
                # is in result, and check whether any possible second is in
                # result (after removing the first string)
                if any([(link_strs[0] + f" {atom_a}" in link_result) and
                        (link_strs[1] + f" {atom_b}" in link_result.replace(link_strs[0]
                                                                            + f" {atom_a}", ''))
                        for atom_a in df_xl_res.atom for atom_b in df_xl_res.atom]):
                    tplk_eucl = link_result.split(' ')[9]
                    tplk_topo = link_result.split(' ')[10]
                    # Check whether both distances computed by topolink did
                    # not pass the threshold, if so directly save them as
                    # floats to zipped distance collection and change
                    # according boolean in obs_inds to True (because it was
                    # found in the results of topolink)
                    if (not tplk_eucl.startswith('>')) and (not tplk_topo.startswith('>')):
                        toplink_dists.append((data_index, float(tplk_eucl), float(tplk_topo)))
                        obs_inds[i] = (data_index, link_strs, True)
                    # If euclidean distance by topolink surpasses threshold
                    # truncate greater-symbol, save both distances' float
                    # values to zipped distance collection and change
                    # according boolean in obs_inds to True (because it was
                    # found in the results of topolink)
                    elif tplk_eucl.startswith('>'):
                        toplink_dists.append((data_index,
                                              float(tplk_eucl.replace('>', '')),
                                              float(tplk_topo)))
                        obs_inds[i] = (data_index, link_strs, True)
                    # If topological distance by topolink surpasses threshold
                    # truncate greater-symbol, save both distances' float
                    # values to zipped distance collection and change according
                    # boolean in obs_inds to True (because it was found in the
                    # results of topolink)
                    elif tplk_topo.startswith('>'):
                        toplink_dists.append((data_index, float(tplk_eucl),
                                              float(tplk_topo.replace('>', ''))))
                        obs_inds[i] = (data_index, link_strs, True)
                    break
        # Iterate over observations again and check whether all were found
        # (e.g. check boolean in tuples), if not save Nans to zipped distance
        # collection
        for obs_ind in obs_inds:
            data_index, _, obs_res_found = obs_ind
            if not obs_res_found:
                toplink_dists.append((data_index, float('Nan'), float('Nan')))
        ind += 1
        progress = round_self((ind * 100) / len_structures, 2)
        verbose_print(f"TopoLink:[{progress}%]", 1, verbose_level, start='\r\t\t', end='')
        return

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(topo_task, structure):
                   structure for structure in sorted(data["path"].unique())}
        progress = round_self((ind * 100) / len_structures, 2)
        verbose_print(f"TopoLink:[{progress}%]", 1, verbose_level, start='\r\t\t', end='')

    for future in concurrent.futures.as_completed(futures):
        try:
            del futures[future]
        except Exception as e:
            print(e)

    verbose_print("", 1, verbose_level)

    # Initialize topolink columns for euclidean and topological distances
    data["eucl_dist_tplk"] = float("Nan")
    data["topo_dist_tplk"] = float("Nan")

    # For zipped distances in collection, replace them at specified index in
    # dataset
    for indices, eucl_dist, top_dist in toplink_dists:
        data.loc[indices, "eucl_dist_tplk"] = round_self(eucl_dist, 3)
        data.loc[indices, "topo_dist_tplk"] = round_self(top_dist, 3)

    # Fill topolink distances with zero, if positions equal
    data.loc[(data.pos_a == data.pos_b) & (data.unip_id_a == data.unip_id_b)
             & (data.chain_a == data.chain_b), "eucl_dist_tplk"] = 0.0
    data.loc[(data.pos_a == data.pos_b) & (data.unip_id_a == data.unip_id_b)
             & (data.chain_a == data.chain_b), "topo_dist_tplk"] = 0.0

    return data


def isolate_pdb_chain(path: str, pdb_id: str, temp_dir: str,
                      chain_ids: list[str]):
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
        structure = FastMMCIFParser().get_structure('', path).get_list()[0]

    class ChainSelect(Select):
        """
        overloads chain accept method
        """
        def accept_chain(self, chain):
            if chain.__repr__().split('=')[1][0] in chain_ids:
                return True
            return False

    # save new pdb to temporary pdb path
    new_path = f"{temp_dir}struct/{pdb_id}_tmp.pdb"
    io = PDBIO()
    io.set_structure(structure)
    io.save(new_path, ChainSelect())

    return new_path


def build_topolink_chain_map(chain_ids):
    """Assign distinct PDB chain IDs while preserving existing legal IDs."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    source_ids = sorted(set(chain_ids))
    if len(source_ids) > len(alphabet):
        raise ValueError(
            "TopoLink PDB export supports at most 62 selected chains"
        )

    chain_map = {
        chain_id: chain_id
        for chain_id in source_ids
        if len(chain_id) == 1 and chain_id in alphabet
    }
    available = iter(
        name for name in alphabet if name not in chain_map.values()
    )
    for chain_id in source_ids:
        if chain_id not in chain_map:
            chain_map[chain_id] = next(available)
    return chain_map


def prepare_topolink_structure(path, pdb_id, temp_dir, chain_ids):
    """Export a mapped copy and record original chain/residue identities."""
    model = read_structure_models(path)[0].copy()
    chain_map = build_topolink_chain_map(chain_ids)
    residue_map = {}
    mapping_rows = []
    source_path = os.path.abspath(path)

    # Detach all chains before renaming to avoid ID collisions.
    source_chains = list(model)
    for chain in source_chains:
        model.detach_child(chain.id)

    for chain in source_chains:
        source_chain = chain.id
        if source_chain not in chain_map:
            continue
        chain.id = chain_map[source_chain]

        residues = list(chain)
        for residue in residues:
            chain.detach_child(residue.id)

        for new_number, residue in enumerate(residues, start=1):
            hetflag, number, icode = residue.id
            residue_map[(source_chain, hetflag, number, icode)] = new_number
            mapping_rows.append(
                {
                    "source_path": source_path,
                    "source_chain": source_chain,
                    "source_hetflag": hetflag,
                    "source_resseq": number,
                    "source_icode": icode,
                    "topolink_chain": chain.id,
                    "topolink_resseq": new_number,
                }
            )
            residue.id = (hetflag, new_number, " ")
            chain.add(residue)
        model.add(chain)

    if not residue_map:
        return "-", {}

    new_path = f"{temp_dir}struct/{pdb_id}_tmp.pdb"
    writer = PDBIO()
    writer.set_structure(model)
    with open(new_path, "w", encoding="utf-8") as output:
        writer.save(output)
    pd.DataFrame(mapping_rows).to_csv(
        f"{temp_dir}struct/{pdb_id}_residue_map.csv", index=False
    )
    return new_path, residue_map


def resolve_topolink_position(row, site, residue_map):
    """Resolve an original residue to its unique exported number."""
    chain = getattr(row, f"chain_{site}")
    try:
        number = int(getattr(row, f"pdb_pos_{site}"))
    except (TypeError, ValueError, OverflowError):
        return None

    hetflag = getattr(row, f"pdb_hetflag_{site}", None)
    icode = getattr(row, f"pdb_icode_{site}", None)
    hetflag = None if pd.isna(hetflag) else (str(hetflag) or " ")
    icode = None if pd.isna(icode) else (str(icode) or " ")

    if hetflag is not None and icode is not None:
        return residue_map.get((chain, hetflag, number, icode))

    # Older input may lack identity fields; accept only a unique match.
    matches = []
    for source_id, exported_number in residue_map.items():
        source_chain, source_hetflag, source_number, source_icode = source_id
        if (
            source_chain == chain
            and source_number == number
            and (hetflag is None or source_hetflag == hetflag)
            and (icode is None or source_icode == icode)
        ):
            matches.append(exported_number)
    return matches[0] if len(matches) == 1 else None
