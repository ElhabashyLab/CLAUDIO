import pandas as pd


def read_in(input_filepath):
    # read outfile from uniprot search and isolate intra interactions only
    #
    # input input_filepath: str
    # return data: pd.DataFrame

    data = pd.read_csv(input_filepath, index_col=0)

    return data[data["XL_type"] == "intra"]
