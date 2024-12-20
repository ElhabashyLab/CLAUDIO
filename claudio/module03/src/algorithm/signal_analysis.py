from claudio.utils.utils import round_self
import pandas as pd


def analyse_homo_signals(data: pd.DataFrame):
    """
    compute homology signals of interaction sites based on site adjacency and peptide overlap
    
    Parameters
    ----------
    data : pd.DataFrame

    Returns
    -------
    data : pd.DataFrame
    """

    data["pep_copies_found"] = data.apply(lambda x: search_for_peptide_copies(x, data), axis=1)
    data["homo_adjacency"] = data.apply(lambda x: compute_interaction_adj(x), axis=1)
    data["homo_int_overl"] = data.apply(lambda x: compute_interaction_overlap(x), axis=1)
    data["homo_pep_overl"] = data.homo_int_overl > 0
    data = data.drop("pep_copies_found", axis=1)
    return data


def search_for_peptide_copies(data_row: pd.Series, data: pd.DataFrame):
    """
    search the dataset for in-sequence peptide copies. If so, return True marking them to be excluded from
    the ops analysis
    
    Parameters
    ----------
    data_row : pd.Series
    data : pd.DataFrame

    Returns
    -------
        bool
    """

    same_proteins = (data_row.unip_id_a == data.unip_id_a) & (data_row.unip_id_b == data.unip_id_b)
    same_peptides = (data_row.pep_a == data.pep_a) & (data_row.pep_b == data.pep_b)
    filtered_data = data[same_proteins & same_peptides]

    for _, row in filtered_data.iterrows():
        if data_row.name != row.name:
            a_copy_found = data_row.seq_a.count(data_row.pep_a) > 1
            b_copy_found = data_row.seq_b.count(data_row.pep_b) > 1
            if a_copy_found or b_copy_found:
                return True
    return False


def compute_interaction_adj(data_row: pd.Series):
    """
    compute interactions site adjacency, represented by value between 0 (residues far away on sequence) and 1
    (residues are the same)
    
    Parameters
    ----------
    data_row : pd.Series

    Returns
    -------
    compute_interaction_dist: (float | int)
    """

    if (data_row["unip_id_a"] == data_row["unip_id_b"]) and (not data_row.pep_copies_found):
        adjacency = 1 - (abs(int(data_row["pos_a"]) - int(data_row["pos_b"])) /
                         len(data_row["seq_a"]))
        return round_self(adjacency, 3)
    # If proteins of sites are not the same, no overlap can be computed
    else:
        return float("Nan")


def compute_interaction_overlap(data_row: pd.Series):
    """
    compute peptide overlap between/including interacting residues, represented by value between 0
    (no peptide overlap between/including interacting residues) and 1 (both interacting residues are in both peptides)
    
    Parameters
    ----------
    data_row : pd.Series

    Returns
    -------
    compute_interaction_overlap : (float | int)
    """

    if (data_row["unip_id_a"] == data_row["unip_id_b"]) and (not data_row.pep_copies_found):
        if data_row["pos_a"] == data_row["pos_b"]:
            return 1.0
        else:
            site1, site2 = ('a', 'b') if data_row["pos_a"] < data_row["pos_b"] else ('b', 'a')
            seq, pep_a, pep_b, pos_a, pos_b = (data_row["seq_a"], data_row[f"pep_{site1}"],
                                               data_row[f"pep_{site2}"], int(data_row[f"pos_{site1}"]) - 1,
                                               int(data_row[f"pos_{site2}"]) - 1)

            # save indices of residues in peptides between/including interacting residues
            seq_a_inds = set(range(seq.find(pep_a), seq.find(pep_a) + len(pep_a)))
            seq_b_inds = set(range(seq.find(pep_b), seq.find(pep_b) + len(pep_b)))

            # filter indices based on positions
            seq_a_inds = {ind for ind in seq_a_inds if ind >= pos_a}
            seq_b_inds = {ind for ind in seq_b_inds if ind <= pos_b}

            # compute intersect and union of index sets
            seq_intersect = seq_a_inds & seq_b_inds
            seq_union = seq_a_inds | seq_b_inds

            if not seq_intersect:
                return 0.0
            else:
                return round_self(len(seq_intersect) / len(seq_union), 3)
    # If proteins of sites are not the same, no overlap can be computed
    else:
        return float("Nan")
