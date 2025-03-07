import pandas as pd


def create_ident_chain_copies(data: pd.DataFrame):
    """
    Create and append datapoints for identical chains in structures

    Parameters
    ----------
    data : pd.DataFrame

    Returns
    -------
    data : pd.DataFrame
    """

    new_data_infos, new_datapoints = ([] for _ in range(2))
    num_before = len(data.index)
    print(f"Creating datapoints for multiple chain options: {num_before}",
          end='')

    # Annotate identical chains, and replace multi-chain notation into single
    data = data.apply(lambda x: annotate_multi_chain_dps(x, new_data_infos), 
                      axis=1)

    # Create datapoints off of annotated multi-chains
    for new_data_info in new_data_infos:
        already_found_opts = []
        dp, chain_a_opts, chain_b_opts = new_data_info
        count = 1
        dp_name = dp.name
        for i, chain_a in enumerate(chain_a_opts.split('_')):
            if chain_a != '-':
                dp.chain_a = chain_a
            for j, chain_b in enumerate(chain_b_opts.split('_')):
                if chain_b != '-':
                    dp.chain_b = chain_b
                dp = dp.rename(f"{dp_name}_{count}")
                if (i, j) != (0, 0):
                    if (dp.unip_id_a == dp.unip_id_b) and (dp.pos_a == dp.pos_b):
                        already_annotated = (dp.chain_b, dp.chain_a) in already_found_opts
                        if not already_annotated:
                            new_datapoints.append(dp.copy())
                            already_found_opts.append((dp.chain_a, dp.chain_b))
                    else:
                        new_datapoints.append(dp.copy())
                count += 1

    if new_datapoints:
        # Add new datapoints to dataset
        new_datapoints = pd.concat(new_datapoints, axis=1).transpose()
        data = pd.concat([data, new_datapoints])
        print(f" -> {len(data.index)} datapoints (number of new datapoints: {len(data.index) - num_before})")

    return data


def annotate_multi_chain_dps(data_row: pd.Series, 
                             new_data_infos: list[tuple[pd.Series,str,str]]):
    """
    Annotate options if multiple chains were found, if so furthermore replace 
    this with the first option

    Parameters
    ----------
    data_row : pd.Series,
    new_data_infos : list[tuple[pd.Series,str,str]]

    Returns
    -------
    data : pd.DataFrame
    """

    chain_a_opts_found = '_' in data_row.chain_a
    chain_b_opts_found = '_' in data_row.chain_b
    if (chain_a_opts_found or chain_b_opts_found) and (len(data_row.pdb_id) == 4):
        new_data_infos.append((data_row.copy(), data_row.chain_a, data_row.chain_b))

        data_row.chain_a = data_row.chain_a.split('_')[0]
        data_row.chain_b = data_row.chain_b.split('_')[0]
    return data_row
