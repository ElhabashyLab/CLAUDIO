import os
import sys

import pandas as pd


def verbose_print(print_string, threshold, verbose_level, end='\n'):
    # print given string, if verbose_level is higher than threshold
    #
    # input print_string: str, threshold: int, verbose_level: int, end: str
    # no return

    if verbose_level > threshold:
        print(print_string, end=end)


def clean_input_paths(path_strs):
    # get absolute paths and apply windowsos path translation, if not NoneType (else return None) and if it does not
    # contain an environmental variable (else return it as is)
    #
    # input path_strs: iterable(str)
    # return abs_paths: list(str)

    abs_paths = []
    for path_str in path_strs:
        if path_str in [None, "None"]:
            abs_paths.append(None)
        elif '$' in path_str:
            abs_paths.append(path_str)
        else:
            abs_paths.append(os.path.abspath(path_str.replace("\\\\", '/').replace('\\', '/')))

    return abs_paths


def create_out_path(output_directory, input_filepath):
    # create output directory, if not already existing
    #
    # input output_directory: str, input_filepath: str
    # return output_directory: str

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


def evaluate_boolean_input(input_str):
    # evaluate boolean value of input string
    #
    # input input_str: str
    # return boolean

    if str(input_str).lower() in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif str(input_str).lower() in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"Error! Could not change type of input to boolean (given:{input_str}).")


def build_xl_dataset(xl_residues):
    # build residue dataset from comma-separated xl_residues input string, specifying residue, atom type, and position
    #
    # input xl_residues: str
    # return df_xl_res: pd.DataFrame

    res_list, pos_list, atom_list = ([] for _ in range(3))

    for s in xl_residues.replace(';', ',').split(','):
        if ':' in s:
            if s.count(':') != 2:
                print(f"Error! Found ':' in one xl_res input, but less or more than two-times. If you wish "
                      f"to specify either the position or the atom type make sure you always add two ':' "
                      f"in the input (specific: {s}, full: {xl_residues}).")
                return None
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
            print(f"Error! Found {atom} as atom type, which is not allowed. Please only use either backbone atoms or CB"
                  f" (either \"N\", \"CA\", \"C\", \"O\", or \"CB\")")
            return None

    return df_xl_res


def round_self(value, decimals):
    # simple decimal rounding function (python by itself has a tendency to round fragmented with the built-in function)
    #
    # input value: float, decimals: int
    # return rounded_value: float/int

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


def clean_dataset(data, method=""):
    # Cleaning of structure data dataset for outputs
    #
    # input data: pd.DataFrame
    # return data: pd.DataFrame

    if not method:
        # Drop datapoints with ident index, if data values are all identical
        if "pdb_id" in data.columns:
            drop_indeces,\
                already_checked = ([] for _ in range(2))
            for i, row in data.iterrows():
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
                         "res_criteria_fulfilled", "res_crit_a", "res_crit_b", "method_a", "method_b", "is_interfaced"]:
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
            for i, row in data.iterrows():
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
            data["sort_index_i"] = [int(i.split('_')[0]) for i in data.index]
            data["sort_index_j"] = [int(i.split('_')[1]) if '_' in i else 1 for i in data.index]
            data = data.sort_values(["sort_index_i", "sort_index_j"]).drop("sort_index_i", axis=1).drop("sort_index_j", axis=1)
    elif method == "minimize":
        # intra_to_inter_i = {"dist": 0, "ops": 0, "both": 0, "same": 0}
        # special_ops = []

        drop_indeces = []
        for ind in [i for i in data.index if '_' not in str(i)]:
            is_intra = data.loc[ind].XL_type == "intra"
            data_ind_snippet = data.loc[[i for i in data.index if str(i).split('_')[0] == str(ind)]]
            if len(data_ind_snippet.index) > 1:
                inter_snip = data_ind_snippet[data_ind_snippet.XL_type == "inter"]
                intra_snip = data_ind_snippet[data_ind_snippet.XL_type == "intra"]
                drop_indeces.extend([i for i in inter_snip.index if is_intra or (i != inter_snip.topo_dist.idxmin())])
                drop_indeces.extend([i for i in intra_snip.index if (not is_intra) or (i != intra_snip.topo_dist.idxmin())])

            if all((i in drop_indeces for i in data_ind_snippet.index)):
                drop_indeces.remove(data_ind_snippet.index[0])

        #     kept_i = [i for i in data_ind_snippet.index if i not in drop_indeces]
        #     to_be_disposed = data_ind_snippet.iloc[0]
        #     to_be_kept = data_ind_snippet.loc[kept_i[0]]
        #     if (to_be_kept.evidence or
        #         ((to_be_kept.unip_id_a == to_be_kept.unip_id_b) and
        #          (to_be_kept.XL_type == "inter"))) and \
        #             (not to_be_kept.evidence):
        #         if ("overlap" in to_be_disposed.evidence) and ("distance" in to_be_disposed.evidence):
        #             intra_to_inter_i["both"] += 1
        #             special_ops.append((to_be_disposed.name, to_be_disposed.pdb_id))
        #         elif "same" in to_be_disposed.evidence:
        #             intra_to_inter_i["same"] += 1
        #         elif "overlap" in to_be_disposed.evidence:
        #             intra_to_inter_i["ops"] += 1
        #         elif "distance" in to_be_disposed.evidence:
        #             intra_to_inter_i["dist"] += 1
        #
        # print(intra_to_inter_i)
        # print(special_ops)
        data = data.drop(index=drop_indeces)

    return data
