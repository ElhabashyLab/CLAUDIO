"""writes outputs for Module02's distance evaluation as intermediate results
for further processing in CLAUDIO"""
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
