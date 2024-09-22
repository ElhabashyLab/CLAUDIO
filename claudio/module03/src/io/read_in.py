import pandas as pd


def read_in(input_filepath : str):
    """ read outfile from uniprot search and isolate intra interactions only
    
    Parameters
    ----------
    input_filepath : str
    
    Returns
    -------
    data : pd.DataFrame
    """
    return pd.read_csv(input_filepath, index_col=0)
