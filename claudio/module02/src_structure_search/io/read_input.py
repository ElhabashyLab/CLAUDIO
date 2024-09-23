import pandas as pd


def read_in(input_filepath: str):
    """
    read inputfile (.sqcs file), and columns for results and for control

    Parameters
    ----------
    input_filepath : str

    Returns
    -------
    data : pd.DataFrame,
    filename : str
    """

    # Read input
    data = pd.read_csv(input_filepath, index_col=0)
    filename = input_filepath.split('/')[-1]

    # Add result and control columns
    data["all_results"] = ''
    data[["pdb_id", "path", "pdb_method", "pdb_resolution", "best_res_pdb_method", "best_res_pdb_resolution"]] = '-'
    data[["chain_a", "chain_b"]] = '-'

    return data, filename
