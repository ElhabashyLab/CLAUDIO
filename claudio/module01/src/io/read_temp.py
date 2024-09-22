import pandas as pd


def read_temp_search_save(data: pd.DataFrame, tmp_filepath: str):
    """
    read temporary save file containing earlier uniprot search results, for quick reruns

    Parameters
    ----------
    data : pd.DataFrame,
    tmp_filepath : str

    Returns
    -------
    read_temp_search_save : pd.DataFrame
    """

    return pd.concat([data, pd.read_csv(tmp_filepath)], axis=1)
