"""Write preprocessing reports and the SQCS input for later modules."""
import pandas as pd
from claudio.utils.utils import verbose_print


def write_outputs(data: pd.DataFrame, unique_proteins_list: pd.DataFrame,
                  filename: str, output_directory: str, verbose_level: int):
    """Write the protein list, record tracking report, and downstream SQCS file.

    Source IDs and original positions remain in the preprocessing report.
    Only validated endpoints enter SQCS, retaining their report row indices.
    Rejected records and position statuses remain in the preprocessing report.

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
    status_columns = ["position_status_a", "position_status_b"]
    included = pd.Series(True, index=data.index, dtype=bool)
    report = data.reindex(columns=report_columns).copy()
    if any(column in data.columns for column in status_columns):
        statuses = data.reindex(columns=status_columns)
        accepted = statuses.isin(["valid", "corrected"])
        included = accepted.all(axis=1)
        report[status_columns] = statuses
        report["included_in_sqcs"] = included
        report["exclusion_reason"] = [
            "; ".join(
                f"{column}={'missing' if pd.isna(value) else value}"
                for column, value in zip(status_columns, values)
                if pd.isna(value) or value not in ("valid", "corrected")
            )
            for values in statuses.itertuples(index=False, name=None)
        ]
    tracking_columns += status_columns + ["included_in_sqcs", "exclusion_reason"]
    verbose_print("\tWrite preprocessing record tracking report", 0, verbose_level)
    output_path = f"{output_directory}{filename}_record_tracking.csv"
    report.to_csv(output_path, index=True)

    verbose_print("\tWrite SQCS-file (a CSV-file) for further steps in CLAUDIO",
                  0, verbose_level)
    output_path = f"{output_directory}{filename}.sqcs"
    data.loc[included].drop(columns=tracking_columns, errors="ignore").to_csv(
        output_path, index=True,
    )
