"""Write preprocessing reports and the SQCS input for later modules."""
import pandas as pd
from claudio.utils.utils import verbose_print


def write_outputs(data: pd.DataFrame, unique_proteins_list: pd.DataFrame,
                  filename: str, output_directory: str, verbose_level: int):
    """Write the protein list, record tracking report, and downstream SQCS file.

    Source IDs and original positions remain in the preprocessing report.
    The SQCS file uses the same row indices without these tracking columns.

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
    verbose_print("\tWrite list of unique proteins", 0, verbose_level)
    output_path = f"{output_directory}{filename}_unique_proteins.csv"
    unique_proteins_list.to_csv(output_path, index=True)

    tracking_columns = [
        "source_record_id", "original_pos_a", "original_pos_b",
    ]
    report_columns = [
        "source_record_id", "unip_id_a", "unip_id_b",
        "original_pos_a", "original_pos_b", "pos_a", "pos_b",
    ]
    verbose_print("\tWrite preprocessing record tracking report", 0, verbose_level)
    output_path = f"{output_directory}{filename}_record_tracking.csv"
    data.reindex(columns=report_columns).to_csv(output_path, index=True)

    verbose_print("\tWrite SQCS-file (a CSV-file) for further steps in CLAUDIO",
                  0, verbose_level)
    output_path = f"{output_directory}{filename}.sqcs"
    data.drop(columns=tracking_columns, errors="ignore").to_csv(
        output_path, index=True,
    )
