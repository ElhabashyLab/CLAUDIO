"""reads output of uniprot search"""
import pandas as pd


def read_unipsearch_out(input_filename: str):
    """
    read output of uniprot_search (intra XLs only)

    Parameters
    ----------
    input_filename : str

    Returns
    -------
    data : pd.DataFrame
    """

    data = pd.read_csv(input_filename, index_col=0)

    return data
