"""reads input file and maps the column names to a unified naming scheme
 for module01"""
import sys
import pandas as pd
import numpy as np

from claudio.utils.utils import is_floatable_str


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

    for col, val in {"unip_id_a": 'str',
                     "unip_id_b": 'str',
                     "pos_a": 'int64',
                     "pos_b": 'int64',
                     "pep_a": 'str',
                     "pep_b": 'str',
                     "res_pos_a": 'float64',
                     "res_pos_b": 'float64'}.items():
        try:
            data[col] = data[col].apply(lambda x: str(x).replace(' ', '')).dropna()
            if val == 'int64':
                data[col] = data[col].apply(
                    lambda x: int(float(x)) if (not np.isnan(float(x))) and is_floatable_str(x) else -1
                )
            elif val == 'float64':
                data[col] = data[col].apply(lambda x: float(x) if is_floatable_str(x) else np.nan)
            else:
                data[col] = data[col].astype(val)
        except Exception as e:
            print(f"Error! Failed to set dtype in column={col} (initial column={[k for k, v in projections.items() if v == col]}) -> {repr(e)}")
            sys.exit(1)

    return data
