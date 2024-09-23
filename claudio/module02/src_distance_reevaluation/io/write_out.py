import pandas as pd

def write_output(data: pd.DataFrame, filepath: str):
    """
    write dataset to output file as csv

    Parameters
    ----------
    data : pd.DataFrame,
    filepath : str

    Returns
        None
    """

    data.to_csv(filepath, index=True)
