import pandas as pd
from claudio.utils.utils import verbose_print


def write_outputs(data: pd.DataFrame, unique_proteins_list: pd.DataFrame,
                  filename: str, output_directory: str, verbose_level: int):
    """
    write outputs to files: One csv-file for the users information on unique 
    proteins and one csv-file marked with the extension .sqcs, signaling 
    CLAUDIO that this dataset is processed for its uses

    Parameters
    ----------
    data : pd.DataFrame,
    unique_proteins_list : pd.DataFrame,
    filename : str,
    output_directory : str,
    verbose_level : int

    Returns 
    -------
        None
    """

    # write list of unique proteins
    verbose_print("\tWrite list of unique proteins", 0, verbose_level)
    output_path = f"{output_directory}{filename}_unique_proteins.csv"
    unique_proteins_list.to_csv(output_path, index=True)

    verbose_print("\tWrite SQCS-file (a CSV-file) for further steps in CLAUDIO",
                  0, verbose_level)
    output_path = f"{output_directory}{filename}.sqcs"
    data.to_csv(output_path, index=True)
