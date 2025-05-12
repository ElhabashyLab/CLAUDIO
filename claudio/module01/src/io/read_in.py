import sys
import pandas as pd


def read_inputfile(input_filepath: str, projections: dict):
    """
    read inputfile and use projections to map column names to unified naming

    Parameters
    ----------
    input_filepath : str,
    projections : dict

    Returns
    -------
    data : pd.DataFrame
    """

    data = pd.read_csv(input_filepath)
    try:
        data.rename(columns=projections, inplace=True)
    except Exception:
        print("Error! Given projection of column names failed! Check given comma-separated list!")
        sys.exit(1)

    return data
