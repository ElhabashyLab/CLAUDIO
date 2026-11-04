"""Reads temporary save file containing hhsearch or blastp search results."""
import pandas as pd


def read_temp_file(data: pd.DataFrame, tmp_filepath: str):
    """
    read temporary save file containing earlier hhsearch or blastp 
    search results and concatenate them to the dataset, for quick reruns

    Parameters
    ----------
    data : pd.DataFrame,
    tmp_filepath : str

    Returns
    -------
    read_temp_file : pd.DataFrame
    """

    tmp_data = pd.read_csv(tmp_filepath)

    data["pdb_id"] = tmp_data["pdb_id"]
    data["all_results"] = tmp_data["all_results"]
    data["chain_a"] = tmp_data["chain_a"]
    data["chain_b"] = tmp_data["chain_b"]

    return data.fillna('')
