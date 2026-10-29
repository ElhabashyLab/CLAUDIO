"""Reads temporary save file containing hhsearch or blastp search results."""
import pandas as pd


def read_temp_file(data: pd.DataFrame, tmp_filepath: str):
    """Restore search results only when cached input identities match."""
    tmp_data = pd.read_csv(tmp_filepath)
    result_columns = ["pdb_id", "all_results", "chain_a", "chain_b"]
    identity_columns = ["unip_id_a", "unip_id_b", "seq_a", "seq_b"]

    required_columns = set(result_columns + identity_columns)
    if not required_columns.issubset(tmp_data.columns):
        raise ValueError(
            "Search cache lacks required identity or result columns; "
            "rerun structure search"
        )

    if len(tmp_data) != len(data):
        raise ValueError(
            "Search cache row count does not match input data; "
            "rerun structure search"
        )

    cached_identity = tmp_data[identity_columns].reset_index(drop=True)
    input_identity = (
        data[identity_columns].astype(str).reset_index(drop=True)
    )
    if not cached_identity.equals(input_identity):
        raise ValueError(
            "Search cache input identity or row order does not match; "
            "rerun structure search"
        )

    data[result_columns] = tmp_data[result_columns].to_numpy()
    return data.fillna('')
