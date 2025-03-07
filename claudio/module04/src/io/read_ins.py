import pandas as pd


def read_inputs(file1: str, file2: str):
    """
    read results of both reevaluations, return combined dataset
    
    Parameters
    ----------
    file1 : str,
    file2 : str

    Returns
    -------
    data : pd.DataFrame
    """

    data1 = pd.read_csv(file1, index_col=0, low_memory=False)
    data2 = pd.read_csv(file2, index_col=0)
    data = merge_datasets(data1, data2)
    data.loc[data.chain_a != data.chain_b, "homo_pep_overl"] = False

    return data


def merge_datasets(df1: pd.DataFrame, df2: pd.DataFrame):
    """
    merge ops analysis dataset into structural distance analysis dataset. 
    Furthermore, ensure that results of ops analysis are integrated for new
    datapoints of structural distance analysis

    Parameters
    ----------
    df1 : pd.DataFrame,
    df2 : pd.DataFrame

    Returns
    -------
    df1 : pd.DataFrame
    """

    for column in df2.columns:
        if column not in df1.columns:
            if type(df1.index[0]) == str:
                df1[column] = False
                for i in df1.index:
                    if '_' in str(i):
                        df1.loc[i, column] = df2.loc[int(str(i).split('_')[0]),
                                                     column]
                    else:
                        df1.loc[i, column] = df2.loc[int(i), column]
            else:
                df1[column] = df2[column].tolist()
    return df1
