import pandas as pd

def write_output(data: pd.DataFrame, filename: str, output_directory: str):
    """
    write dataset to output file as csv
    
    Parameters
    ----------
    data : pd.DataFrame,
    filename : str,
    output_directory : str

    Returns
    -------
    None
    """

    out_filepath = f"{output_directory}{filename}_ops.csv"
    data.to_csv(out_filepath, index=True)
