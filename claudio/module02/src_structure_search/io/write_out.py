"""Writes csv file with results of structure search for Module02"""
import pandas as pd

def write_output(data: pd.DataFrame, filename: str, output_directory: str):
    """
    Overwrite dataset to input filepath as csv

    Parameters
    ----------
    data : pd.DataFrame,
    filename : str,
    output_directory : str

    Returns
    -------
    None
    """

    data.to_csv(f"{output_directory}{filename}_structdi.csv", index=True)
