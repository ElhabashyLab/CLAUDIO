import os
import pandas as pd


def write_outputs(data: pd.DataFrame, filename: str, compute_scoring: bool,
                  output_directory: str):
    """
    write outputs

    Parameters
    ----------
    data : pd.DataFrame, 
    filename : str,
    compute_scoring : bool,
    output_directory: str

    Returns
    -------
    None

    """

    # save list of already written results by uniprot ids
    already_written = []

    # create subdirectories, if not already in output directory
    output_homo_dir = f"{output_directory}homomers"
    output_hetero_dir = f"{output_directory}heteromers"
    if (data.XL_type == "intra").any() and not os.path.exists(output_homo_dir):
        os.mkdir(output_homo_dir)
    if (data.XL_type == "inter").any() and not os.path.exists(output_hetero_dir):
        os.mkdir(output_hetero_dir)

    for row in data.itertuples():
        unip_id = f"{row.unip_id_a}_{row.unip_id_b}" if row.unip_id_a != row.unip_id_b else row.unip_id_a

        # only write new result files if results for uniprot entry were
        # not written yet
        if (unip_id not in already_written) and (row.XL_type == "inter"):
            is_intra = row.unip_id_a == row.unip_id_b

            output_subdirectory = f"{output_homo_dir}/{unip_id}" if is_intra else f"{output_hetero_dir}/{unip_id}"
            if not os.path.exists(output_subdirectory):
                os.mkdir(output_subdirectory)

            # If intra crosslink, write fasta with subsequent
            # number of sequences
            if is_intra:
                # if valid oligo-states were found, create fasta with
                # respective number of sequence copies (ex.: 3mer -> 3 seqs)
                if row.swiss_model_homology:
                    for oligo_state in row.swiss_model_homology.split('_'):
                        num_mer = int(oligo_state.replace("homo", '').replace("mer", ''))
                        with open(f"{output_subdirectory}/{unip_id}_{oligo_state}.fasta", 'w', encoding="utf-8") as f:
                            content = f">{unip_id}\n{row.seq_a}\n"
                            for _ in range(num_mer):
                                f.write(content)
                # else assume unknown homomer, with two sequences for now,
                # but leave oligo-state field in filename empty
                # (user may decide here)
                else:
                    with open(f"{output_subdirectory}/{unip_id}_new_homomer.fasta", 'w', encoding="utf-8") as f:
                        content = f">{unip_id}\n{row.seq_a}\n"
                        f.write(content + content)
            # Else write multi fasta with involved sequences for
            # heteromer complex
            else:
                # If heteromeric state given by SWISS-MODEL write
                # title plainly, else write identifier for new heteromer
                multifasta_filename = f"{unip_id}_heteromer.fasta" \
                    if "hetero" in row.swiss_model_homology else f"{unip_id}_new_heteromer.fasta"
                with open(f"{output_subdirectory}/{multifasta_filename}", 'w', encoding="utf-8") as f:
                    content = f">{row.unip_id_a}\n{row.seq_a}\n\n>{row.unip_id_b}\n{row.seq_b}"
                    f.write(content)

            # write all interactions for current uniprot id into a csv
            if row.unip_id_a == row.unip_id_b:
                unip_arg = (data.unip_id_a == unip_id) & (data.unip_id_b == unip_id)
            else:
                unip_arg = ((data.unip_id_a == unip_id.split('_')[0]) & (data.unip_id_b == unip_id.split('_')[1])) | \
                            ((data.unip_id_a == unip_id.split('_')[1]) & (data.unip_id_b == unip_id.split('_')[0]))

            data[unip_arg][['pdb_id', 'chain_a', 'chain_b', 'pdb_pos_a',
                            'pdb_pos_b', 'pos_a', 'pos_b', 
                            'swiss_model_homology', 'XL_type']]\
                .to_csv(f"{output_subdirectory}/{unip_id}_{row.swiss_model_homology}.csv", index=False)

            # add uniprot id to list of already finished results
            if is_intra:
                already_written.append(unip_id)
            else:
                already_written.append(unip_id)
                already_written.append(f"{unip_id.split('_')[1]}_{unip_id.split('_')[0]}")

    # write full output dataset containing all given and computed information
    # select columns
    all_cols = ["unip_id_a", "unip_id_b", "pos_a", "pos_b", "pep_a", "pep_b",
                "res_pos_a", "res_pos_b", "seq_a", "seq_b", "path", "pdb_id", 
                "pdb_method", "pdb_resolution", "chain_a", "chain_b", 
                "pdb_pos_a", "pdb_pos_b", "pLDDT_a", "pLDDT_b", 
                "is_interfaced", "topo_dist", "eucl_dist", "homo_adjacency", 
                "homo_int_overl", "homo_pep_overl", "evidence", "XL_type", 
                "XL_confirmed", "swiss_model_homology"]
    out_columns = ["unip_id_a", "unip_id_b", "pos_a", "pos_b", "pep_a",
                   "pep_b", "res_pos_a", "res_pos_b", "pdb_id", "pdb_method",
                   "pdb_resolution", "chain_a", "chain_b", "pdb_pos_a", 
                   "pdb_pos_b", "pLDDT_a", "pLDDT_b", "topo_dist", "eucl_dist",
                   "homo_pep_overl", "evidence", "XL_type", "XL_confirmed",
                   "swiss_model_homology"]
    if compute_scoring:
        out_columns.insert(20, "homo_adjacency")
        out_columns.insert(21, "homo_int_overl")

    # also, select columns which were in the input but were unused by this tool
    out_columns.extend([col for col in data.columns if col not in all_cols])

    data[out_columns].to_csv(f"{output_directory}{filename}_final.csv")

    # try:
    #     write_small_test_sets(data)
    # except Exception:
    #     pass


def write_small_test_sets(data: pd.DataFrame):
    """
    write small sample datasets, one containing 10 and one with 100 samples of 
    xls mapped onto alphafold structures

    Parameters
    ----------
    data : pd.DataFrame,

    Returns
    -------
        None
    """

    test_data = data[(data.pdb_id.astype(str).str.len() > 4) &
                     (~data.index.astype(str).str.contains('_'))][
        ["unip_id_a", "unip_id_b", "pos_a", "pos_b", "pep_a", "pep_b",
         "res_pos_a", "res_pos_b"]
    ]
    test_data["Organism"] = ""
    test_data.rename(columns={"unip_id_a": "entry1",
                              "unip_id_b": "entry2",
                              "pos_a": "position1",
                              "pos_b": "position2",
                              "pep_a": "peptide1",
                              "pep_b": "peptide2",
                              "res_pos_a": "k_pos1",
                              "res_pos_b": "k_pos2"}, inplace=True)
    pdb_mchains_found = {str(i): not data[data.index.astype(str).str.startswith(i) &
                                          data.index.astype(str).str.contains('_')].empty
                         for i in data.index if '_' not in str(i)}
    test_data = test_data.loc[(not pdb_mchains_found[str(i)]
                               for i in test_data.index)]
    if len(test_data.index) >= 10:
        print("Wrote xl dataset with 10 samples.")
        test_data.sample(10).to_csv("../test/sample_data_10.csv",
                                    index=False)

        if len(test_data.index) >= 100:
            print("Wrote xl dataset with 100 samples.")
            test_data.sample(100).to_csv("../test/sample_data_100.csv",
                                         index=False)

    if len(test_data.index) < 10:
        print(f"Not enough datapoints to create sample dataset (found only {len(test_data.index)}).")
        raise RuntimeError(f"Not enough datapoints to create sample dataset (found only {len(test_data.index)}).")
