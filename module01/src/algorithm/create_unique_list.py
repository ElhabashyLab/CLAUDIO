import sys

import pandas as pd
import requests as r
from io import StringIO
import os


def create_list_of_unique_proteins(data, search_tool, blast_bin, blast_db, hhsearch_bin, hhsearch_db, hhsearch_out):
    # create pandas dataframe of unique proteins depending on uniprot ids, and in the same way create list of unique
    # protein interaction pairs
    #
    # input data: pd.DataFrame, search_tool: str, blast_bin: str/None, blast_db: str, hhsearch_bin: str/None,
    # hhsearch_db: str, hhsearch_out:str
    # return unique_pair_list: pd.DataFrame, unique_proteins_list: pd.DataFrame

    # Create data container lists
    unique_proteins, \
        unique_pairs, \
        unique_protein_indeces, \
        unique_pair_indeces, \
        unique_protein_counts, \
        unique_pair_counts, \
        unique_sequences = ([] for _ in range(7))

    for i, row in data.iterrows():
        pair = (row["unip_id_a"], row["unip_id_b"])
        seqs = (row["seq_a"], row["seq_b"])

        # Check if first protein of pair is a new protein, if so add them to list of unique proteins, add their index
        # to list of unique protein indeces and set the respective count to 1, else just increase the counter by one
        is_known_protein = pair[0] in unique_proteins
        if not is_known_protein:
            unique_proteins.append(pair[0])
            unique_protein_indeces.append(i)
            unique_protein_counts.append(1)
            unique_sequences.append(seqs[0])
        else:
            unique_protein_counts[unique_proteins.index(pair[0])] += 1

        # Check if second protein of pair is a new protein, if so add them to list of unique proteins, add their index
        # to list of unique protein indeces and set the respective count to 1, else just increase the counter by one
        is_known_protein = pair[1] in unique_proteins
        if not is_known_protein:
            unique_proteins.append(pair[1])
            unique_protein_indeces.append(i)
            unique_protein_counts.append(1)
            unique_sequences.append(seqs[1])
        elif pair[0] != pair[1]:
            unique_protein_counts[unique_proteins.index(pair[1])] += 1

        # Check if protein pair is a new pair (also check reverse tuple), if so add it to list of unique pairs, add
        # its index to list of unique pair indeces and set the respective count to 1,
        # else just increase the counter by one
        is_known_pair = (pair in unique_pairs) or (reversed(pair) in unique_pairs)
        if not is_known_pair:
            unique_pairs.append(pair)
            unique_pair_indeces.append(i)
            unique_pair_counts.append(1)
        else:
            try:
                unique_pair_counts[unique_pairs.index(pair)] += 1
            except KeyError:
                unique_pair_counts[unique_pairs.index(reversed(pair))] += 1

    # Apply uniprot search for information on unique proteins
    infos = search_uniprot_metadata(unique_proteins)
    # Apply blastp or hhsearch search for pdb entries on unique proteins by their sequences
    pdbs = search_pdb_entries(unique_proteins, unique_sequences, search_tool, blast_bin, blast_db, hhsearch_bin,
                              hhsearch_db, hhsearch_out)
    # Retrieve pair (sequences and) pdb entries for unique pair list
    _, pair_pdbs = get_pair_seqs_pdbs(unique_sequences, pdbs, unique_proteins, unique_pairs)

    # Collect information of unique proteins for final unique protein list dataset
    unique_proteins_list = pd.DataFrame()
    unique_proteins_list["index"] = unique_protein_indeces
    for i, head in enumerate(infos[0][0].split('\t')):
        unique_proteins_list[head] = [info[1].split('\t')[i].replace('\"', '') for info in infos]
    unique_proteins_list["pdb"] = pdbs
    # unique_proteins_list["ostat"] = get_oligo_states(unique_proteins)
    unique_proteins_list["count"] = unique_protein_counts

    # Collect information of unique protein pairs for final unique protein pair list dataset
    unique_pair_list = pd.DataFrame()
    unique_pair_list["index"] = unique_pair_indeces
    unique_pair_list["protein1"] = [x for x, _ in unique_pairs]
    unique_pair_list["protein2"] = [x for _, x in unique_pairs]
    unique_pair_list["pdb1"] = [x for x, _ in pair_pdbs]
    unique_pair_list["pdb2"] = [x for _, x in pair_pdbs]
    unique_pair_list["count"] = unique_pair_counts

    return unique_pair_list, unique_proteins_list


def search_uniprot_metadata(unique_proteins):
    # retrieve full sequences and info from uniprot database by given entries
    #
    # input unique_proteins: list(str)
    # return infos: list(list(str))

    # Create data container lists
    infos = []

    ind = 1
    # Iterate over proteins (proteins = uniprot ids)
    for protein in unique_proteins:
        print(f"\r\t[{round(ind * 100 / len(unique_proteins), 2)}%]", end='')
        ind += 1

        # Retrieve uniprot information on protein
        urllib = f"https://rest.uniprot.org/uniprotkb/search?query={protein}&format=tsv"
        try:
            info = r.get(urllib).text.split('\n')
        except ConnectionError as e:
            print("No connection to UniProt API possible. Please try again later.")
            print(e)
            sys.exit()

        # Add information and sequence to container lists
        infos.append(info)
    print()

    return infos


def search_pdb_entries(proteins, sequences, search_tool, blast_bin, blast_db, hhsearch_bin, hhsearch_db,
                       hhsearch_out):
    # use either hhsearch or blastp as search tool on protein sequence in order to retrieve matching pdb id, if no
    # result was found add an alphafold entry id instead (id: af<uniprot_id>_A)
    #
    # input proteins: list(str), sequences: list(str), search_tool: str, blast_bin: str/None, blast_db: str,
    # hhsearch_bin: str/None, hhsearch_db: str, hhsearch_out: str
    # return pdbs: list(str)

    # Create data container list
    pdbs = []

    ind = 1
    # Iterate over proteins (proteins = uniprot ids)
    for i, protein in enumerate(proteins):
        print(f"\r\t[{round(ind * 100 / len(proteins), 2)}%]", end='')
        ind += 1

        # Create temporary fasta file at data/temp/unique_protein_list for commandline application in search tools
        project_path = '/'.join(os.path.abspath(__file__).split('/')[:-4])
        temp_path = f"{project_path}/data/temp/unique_protein_list/"
        with open(f"{temp_path}tmp.fasta", 'w') as tmp_file:
            tmp_file.write(f">Name\n{sequences[i]}\n")

        # Initialize result as False
        res = False

        # Depending on given string either perform blastp or hhsearch
        if search_tool == "blastp":
            blast_call = "blastp" if blast_bin is None else f"{blast_bin}blastp"
            cmd = f"{blast_call} -query {temp_path}tmp.fasta -db {blast_db}pdbaa -evalue 1e-5 -max_target_seqs 20 " \
                  f"-outfmt \"6 delim=, saccver pident qcovs evalue\""
            res = pd.read_csv(StringIO(os.popen(cmd).read()),
                              sep=',',
                              names=["pdb", "ident", "cov", "eval"],
                              dtype={"pdb": str, "ident": float, "cov": float, "eval": float})
            # Isolate search result to entries with identity of at least 90% and coverage of at least 50%
            res = res[(res["ident"] >= 90) & (res["cov"] >= 50)]
            # If no result remains reset result to False, else take first fitting entry from pdb column
            if res.empty:
                res = False
            else:
                res = res.iloc[0, :]["pdb"]
        elif search_tool == "hsearch":
            hhearch_call = "hhsearch" if hhsearch_bin is None else f"{hhsearch_bin}hhsearch"
            cmd = f"{hhearch_call} -i {temp_path}tmp.fasta -d {hhsearch_db}pdb70 -e 1e-5 -qid 90 -cov 50 -blasttab " \
                  f"{hhsearch_out} -v 0 -cpu 20"
            os.system(cmd)
            # Open hhsearch output (Note: hhsearch outs cannot be retrieved from the commandline, as it is the case with
            # blastp)
            res = open(f"{temp_path}tmp.hhr", 'r').read().split('\n')[9][4:10]
        # If result is not False, append it to container list, else append alphafold entry id instead
        if res:
            pdbs.append(res)
        else:
            pdbs.append(f"af{protein}_A")
    print()

    return pdbs


def get_pair_seqs_pdbs(sequences, pdbs, unique_proteins, unique_pairs):
    # match sequences and pdb ids of proteins from unique protein list to protein pairs in unique pair list
    #
    # input sequences: list(str), pdbs: list(str), unique_proteins: list(str), unique_pairs: list((str, str))
    # return pair_sequences: list((str, str)), pair_pdbs: list((str, str))

    # Create data container lists
    pair_sequences, \
        pair_pdbs = ([] for _ in range(2))

    # Iterate over protein pairs
    for pair in unique_pairs:
        # Intialize targets
        seq1, \
            seq2, \
            pdb1, \
            pdb2 = ('' for _ in range(4))

        # Iterate over sequences and pdb ids, if respective unique protein matches to either pair protein, save their
        # sequence in pdb id
        for i in range(len(unique_proteins)):
            if pair[0] == unique_proteins[i]:
                seq1 = sequences[i]
                pdb1 = pdbs[i]
            if pair[1] == unique_proteins[i]:
                seq2 = sequences[i]
                pdb2 = pdbs[i]
            # If both sequences were found, e.g. the pair was fully discovered, append them to container lists, and
            # skip to next iteration
            if seq1 and seq2:
                pair_sequences.append((seq1, seq2))
                pair_pdbs.append((pdb1, pdb2))
                break

    return pair_sequences, pair_pdbs
