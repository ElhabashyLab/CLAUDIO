import os
import pandas as pd


def verbose_print(print_string: str, threshold: int, verbose_level: int, end='\n'):
    """
    print given string, if verbose_level is higher than threshold

    Parameters
    ----------
    print_string : str,
    threshold : int,
    verbose_level : int,
    end : str

    Returns
    -------
        None
    """

    if verbose_level > threshold:
        print(print_string.replace('\x00', ''), end=end)


def clean_input_paths(path_strs):
    """
    get absolute paths and apply windowsos path translation, if not NoneType (else return None) and if it does not
    contain an environmental variable (else return it as is)

    Parameters
    ----------
    path_strs : iterable[str]

    Returns
    -------
    out_paths : list[str]
    """
    #TODO check input type

    out_paths = [os.path.abspath(os.path.expandvars(path_str)).replace("\\\\", '/').replace('\\', '/')
                 if path_str not in [None, "None"] else None
                 for path_str in path_strs]

    return [op if (op is None) or op.endswith('/') or os.path.isfile(op) else op + '/' for op in out_paths]


def create_out_path(output_directory: str, input_filepath: str):
    """
    create output directory, if not already existing

    Parameters
    ----------
    output_directory : str,
    input_filepath : str

    Returns
    -------
    output_directory : str
    """

    output_directory = output_directory if output_directory else '/'.join(input_filepath.split('/')[:-1])
    output_directory = output_directory.replace('\\', '/')
    output_directory += '' if output_directory.endswith('/') else '/'
    output_directory_splits = output_directory.split('/')
    sub_paths = ['/'.join(output_directory_splits[:i + 1]) for i in range(len(output_directory_splits))]
    sub_paths = [e for e in sub_paths if e]
    for sub_path in sub_paths:
        if not os.path.exists(sub_path):
            os.mkdir(sub_path)
    return output_directory


def evaluate_boolean_input(input_str: str):
    """
    evaluate boolean value of input string

    Parameters
    ----------
    input_str : str

    Returns
    -------
        bool

    Raises
    ------
        ValueError
    """

    if str(input_str).lower() in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif str(input_str).lower() in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"Error! Could not change type of input to boolean (given:{input_str}).")


def build_xl_dataset(xl_residues: str):
    """
    build residue dataset from comma-separated xl_residues input string, specifying residue, atom type, and position

    Parameters
    ----------
    xl_residues : str
    
    Returns
    -------
    df_xl_res : pd.DataFrame
    """

    res_list, pos_list, atom_list = ([] for _ in range(3))

    for s in xl_residues.replace(';', ',').split(','):
        if ':' in s:
            if s.count(':') != 2:
                raise Exception(f"Error! Found ':' in one xl_res input, but less or more than two-times. If you wish "
                                f"to specify either the position or the atom type make sure you always add two ':' "
                                f"in the input (specific: {s}, full: {xl_residues}).")
            res_list.append(s.split(':')[0])
            atom_list.append(s.split(':')[1] if s.split(':')[1] else "CB")
            pos_list.append(int(s.split(':')[2]) if s.split(':')[2] else 0)
        else:
            res_list.append(s)
            atom_list.append("CB")
            pos_list.append(0)
    df_xl_res = pd.DataFrame()
    df_xl_res["res"] = res_list
    df_xl_res["atom"] = atom_list
    df_xl_res["pos"] = pos_list

    for atom in df_xl_res.atom:
        if atom not in ["N", "CA", "C", "O", "CB"]:
            raise Exception(f"Error! Found {atom} as atom type, which is not allowed. Please only use either backbone "
                            f"atoms or CB (either \"N\", \"CA\", \"C\", \"O\", or \"CB\")")

    return df_xl_res


def round_self(value: float, decimals: int):
    """
    simple decimal rounding function (python by itself has a tendency to round fragmented with the built-in function)

    Parameters 
    ----------
    value : float,
    decimals : int

    Returns
    -------
    rounded_value : float | int
    """

    # If decimal less than 1, the resulting value will be an integer
    if pd.isna(value):
        return float("Nan")
    if decimals < 1:
        rounded_value = int(f"{int((value * (10 ** decimals)) + .5) / (10 ** decimals):.{decimals}f}")
        return rounded_value
    # Else, the resulting value will be a float
    else:
        rounded_value = float(f"{int((value * (10 ** decimals)) + .5) / (10 ** decimals):.{decimals}f}")
        return rounded_value


def clean_dataset(data: pd.DataFrame, method=""):
    """
    Cleaning of structure data dataset for outputs

    Parameters
    ----------
    data : pd.DataFrame

    Returns 
    -------
    data : pd.DataFrame
    """

    if not method:
        # Drop datapoints with ident index, if data values are all identical
        if "pdb_id" in data.columns:
            drop_indeces,\
                already_checked = ([] for _ in range(2))
            for row in data.itertuples():
                i = row.Index
                if ('_' in str(i)) and (i not in already_checked):
                    drop_criteria = (data.pos_a == row.pos_a) & (data.pos_b == row.pos_b) & \
                                    (data.pep_a == row.pep_a) & (data.pep_b == row.pep_b) & \
                                    ((data.res_pos_a == row.res_pos_a) | (pd.isna(data.res_pos_a) & pd.isna(row.res_pos_a))) & \
                                    ((data.res_pos_b == row.res_pos_b) | (pd.isna(data.res_pos_b) & pd.isna(row.res_pos_b)))
                    if all([rename_col in data.columns for rename_col in ["chain_a", "chain_b", "pdb_id"]]):
                        drop_criteria = drop_criteria & (data.chain_a == row.chain_a) & (data.chain_b == row.chain_b) & \
                                        (data.pdb_id == row.pdb_id)
                    if all([rename_col in data.columns for rename_col in ["evidence"]]):
                        drop_criteria = drop_criteria & (data.evidence == row.evidence)

                    if len(data[drop_criteria].index) > 1:
                        drop_indeces.extend(list(data[drop_criteria].index)[1:])
                    already_checked.extend(list(data[drop_criteria].index))
            data = data.drop(index=drop_indeces)

        # Drop specified data columns
        for drop_col in ["all_results", "best_res_pdb_method", "best_res_pdb_resolution",
                         "res_criteria_fulfilled", "res_crit_a", "res_crit_b", "method_a", "method_b", "is_interfaced","xl_type"]:
            if drop_col in data.columns:
                data = data.drop(drop_col, axis=1)

        # Rename certain result columns
        if all([rename_col in data.columns for rename_col in ["eucl_dist_tplk", "topo_dist_tplk"]]):
            data = data.rename(columns={"eucl_dist_tplk": "eucl_dist", "topo_dist_tplk": "topo_dist"})

        # Ascertain data types
        data = data.astype({"pos_a": int, "pos_b": int, "pep_a": str, "pep_b": str, "res_pos_a": int, "res_pos_b": int},
                           errors="ignore")
        if "unip_id" in data.columns:
            data = data.astype({"unip_id": str, "seq": str}, errors="ignore")
        else:
            data = data.astype({"unip_id_a": str, "unip_id_b": str, "seq_a": str, "seq_b": str}, errors="ignore")
        if "pdb_id" in data.columns:
            data = data.astype({"pdb_id": str, "pdb_method": str, "pdb_resolution": str,
                                "pdb_pos_a": int, "pdb_pos_b": int, "pLDDT_a": float, "pLDDT_b": float,
                                "topo_dist": float}, errors="ignore")
            if "unip_id" in data.columns:
                data.astype({"chain": str}, errors="ignore")
            else:
                data.astype({"chain_a": str, "chain_b": str}, errors="ignore")
        if "homo_pep_overl" in data.columns:
            data = data.astype({"homo_adjacency": float, "homo_int_overl": float, "homo_pep_overl": bool}, errors="ignore")
        if "evidence" in data.columns:
            data = data.astype({"evidence": str, "XL_type": str, "swiss_model_homology": str}, errors="ignore")

        # Reduce multichain examples to fitting ones (if present)
        if "evidence" in data.columns:
            drop_indeces,\
                already_checked = ([] for _ in range(2))
            for row in data.itertuples():
                i = row.Index
                if ('_' in str(i)) and (i not in already_checked):
                    multi_chain_criteria = (data.unip_id_a == row.unip_id_a) & \
                                           (data.unip_id_b == row.unip_id_b) & \
                                           ((data.pos_a == row.pos_a) | (pd.isna(data.pos_a) & pd.isna(row.pos_a))) & \
                                           ((data.pos_b == row.pos_b) | (pd.isna(data.pos_b) & pd.isna(row.pos_b))) & \
                                           (data.pep_a == row.pep_a) & \
                                           (data.pep_b == row.pep_b)
                    multi_chain_set = data[multi_chain_criteria]
                    if not multi_chain_set[multi_chain_set.XL_confirmed].empty:
                        drop_indeces.extend(list(multi_chain_set[~multi_chain_set.XL_confirmed].index))
                        if not multi_chain_set[multi_chain_set.XL_confirmed & (multi_chain_set.evidence == '')].empty:
                            drop_indeces.extend(list(multi_chain_set[multi_chain_set.evidence != ''].index))
                    already_checked.extend(list(multi_chain_set.index))
            data = data.drop(index=[drop_index for drop_index in drop_indeces if '_' in drop_index])

        # Sort rows
        if any([type(i) == str for i in data.index]):
            data["sort_index_i"] = [int(i.split('_')[0]) if type(i) == str else i for i in data.index]
            data["sort_index_j"] = [int(i.split('_')[1]) if type(i) == str and '_' in i else 1 for i in data.index]
            data = data.sort_values(["sort_index_i", "sort_index_j"]).drop("sort_index_i", axis=1).drop("sort_index_j", axis=1)

    return data

def minimize_dataset(data: pd.DataFrame):
    """
    Cleaning of structure data dataset for outputs

    Parameters
    ----------
    data : pd.DataFrame

    Returns 
    -------
    data : pd.DataFrame
    """

    drop_indeces = []
    for ind in [i for i in data.index if '_' not in str(i)]:
        is_intra = data.loc[ind].XL_type == "intra"
        data_ind_snippet = data.loc[[i for i in data.index if str(i).split('_')[0] == str(ind)]]
        if len(data_ind_snippet.index) > 1:
            inter_snip = data_ind_snippet[data_ind_snippet.XL_type == "inter"]
            intra_snip = data_ind_snippet[data_ind_snippet.XL_type == "intra"]
            no_evidence_found = inter_snip.evidence == ''
            dist_calc = ~pd.isna(inter_snip.topo_dist)
            if not inter_snip[no_evidence_found & dist_calc].empty:
                drop_indeces.extend([i for i in inter_snip.index if is_intra or
                                        (i != inter_snip[no_evidence_found & dist_calc].topo_dist.idxmin())])
            elif not inter_snip[dist_calc].empty:
                drop_indeces.extend([i for i in inter_snip.index if is_intra or
                                        (i != inter_snip[dist_calc].topo_dist.idxmin())])
            elif not inter_snip[no_evidence_found].empty:
                drop_indeces.extend([i for i in inter_snip.index if is_intra or
                                        (i != inter_snip[no_evidence_found].topo_dist.idxmin())])
            else:
                drop_indeces.extend([i for i in inter_snip.index
                                        if is_intra or (i != inter_snip.topo_dist.idxmin())])

            drop_indeces.extend([i for i in intra_snip.index
                                    if (not is_intra) or (i != intra_snip.topo_dist.idxmin())])

        if all((i in drop_indeces for i in data_ind_snippet.index)):
            drop_indeces.remove(data_ind_snippet.index[0])

    data = data.drop(index=drop_indeces)

    for row in data.itertuples():
        copies_found = (row.seq_a.count(row.pep_a) > 1) or (row.seq_b.count(row.pep_b) > 1)
        if copies_found:
            i = row.Index
            for next_row in data.itertuples():
                next_i = next_row.Index
                if type(next_i) == str and int(next_i.split('_')[0]) > int(i.split('_')[0]):
                    same_proteins = (row.unip_id_a == next_row.unip_id_a) and (row.unip_id_b == next_row.unip_id_b)
                    same_peptides = (row.pep_a == next_row.pep_a) and (row.pep_b == next_row.pep_b)
                    if same_proteins and same_peptides:
                        data = data.drop(index=next_i)

    return data
