"""Performs analysis of overlapping peptide sequences and interaction site adjacency"""
import pandas as pd
from claudio.utils.utils import round_self,verbose_print


def analyse_homo_signals(data: pd.DataFrame,verbose_level: int):
    """
    compute homology signals of interaction sites based on site adjacency 
    and peptide overlap
    
    Parameters
    ----------
    data : pd.DataFrame
    verbose_level: int

    Returns
    -------
    data : pd.DataFrame
    """
    peptide_copy_search = lambda x: search_for_peptide_copies(x, data)
    interaction_overlap = lambda x: compute_interaction_ovl(x, verbose_level)

    data["pep_copies_found"] = data.apply(peptide_copy_search, axis=1)
    data["homo_adjacency"] = data.apply(compute_interaction_adj, axis=1)
    data["homo_int_overl"] = data.apply(interaction_overlap, axis=1)
    data["homo_pep_overl"] = data.homo_int_overl > 0
    data = data.drop("pep_copies_found", axis=1)
    return data

def search_for_peptide_copies(data_row: pd.Series, data: pd.DataFrame):
    """
    search the dataset for in-sequence peptide copies. If so, return True 
    marking them to be excluded from the ops analysis
    
    Parameters
    ----------
    data_row : pd.Series
    data : pd.DataFrame

    Returns
    -------
        bool
    """
    is_protein_a = data_row.unip_id_a == data.unip_id_a
    is_protein_b = data_row.unip_id_b == data.unip_id_b
    same_proteins = is_protein_a & is_protein_b

    is_pep_a = data_row.pep_a == data.pep_a
    is_pep_b = data_row.pep_b == data.pep_b
    same_peptides = is_pep_a & is_pep_b

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
    compute interactions site adjacency, represented by value between 0 
    (residues far away on sequence) and 1 (residues are the same)
    
    Parameters
    ----------
    data_row : pd.Series

    Returns
    -------
    compute_interaction_dist: (float | int)
    """
    is_intra = data_row["unip_id_a"] == data_row["unip_id_b"]
    no_pep_copies = not data_row.pep_copies_found

    if is_intra and no_pep_copies:
        site_distance = abs(int(data_row["pos_a"]) - int(data_row["pos_b"]))
        adjacency = 1 - (site_distance / len(data_row["seq_a"]))
        return round_self(adjacency, 3)
    # If proteins of sites are not the same, no overlap can be computed
    return float("Nan")

def compute_interaction_ovl(data_row: pd.Series,verbose_level: int):
    """
    compute peptide overlap between/including interacting residues, 
    represented by value between 0 (no peptide overlap between/including
    interacting residues) and 1 (both interacting residues are in both 
    peptides)
    
    Parameters
    ----------
    data_row : pd.Series
    verbose_level: int

    Returns
    -------
    compute_interaction_overlap : (float | int)
    """
    is_intra = data_row["unip_id_a"] == data_row["unip_id_b"]
    no_pep_copies = not data_row.pep_copies_found

    if is_intra and no_pep_copies:
        if data_row["pos_a"] == data_row["pos_b"]:
            return 1.0
        site1, site2 = (('a', 'b')
                        if data_row["pos_a"] < data_row["pos_b"]
                        else ('b', 'a'))
        seq = data_row["seq_a"]
        pep_a, pep_b = (data_row[f"pep_{site1}"],
                        data_row[f"pep_{site2}"])
        pos_a, pos_b = (int(data_row[f"pos_{site1}"]) - 1,
                        int(data_row[f"pos_{site2}"]) - 1)

        # get indices of residues between/including interacting residues
        seq_a_inds = get_sequence_indices(seq, pep_a, verbose_level)
        seq_b_inds = get_sequence_indices(seq, pep_b, verbose_level)

        seq_a_inds = {ind for ind in seq_a_inds if ind >= pos_a}
        seq_b_inds = {ind for ind in seq_b_inds if ind <= pos_b}

        # compute intersect and union of index sets
        seq_intersect = seq_a_inds & seq_b_inds
        seq_union = seq_a_inds | seq_b_inds

        if not seq_intersect:
            return 0.0
        return round_self(len(seq_intersect) / len(seq_union), 3)
    # If proteins of sites are not the same, no overlap can be computed
    return float("Nan")

def get_sequence_indices(seq: str, peptide: str, verbose_level: int):
    """
    get the indices of a peptide in a sequence
    
    Parameters
    ----------
    seq : str
    peptide : str
    verbose_level: int

    Returns
    -------
    set of int
    """

    if seq.find(peptide) == -1:
        verbose_print(f"Peptide {peptide} not found in sequence {seq}", 1,
                      verbose_level,end='')
        return set()

    indices = set(range(seq.find(peptide),
                        seq.find(peptide) + len(peptide)))
    return indices
