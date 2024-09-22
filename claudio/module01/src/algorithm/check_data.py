import sys
from Bio.Align import PairwiseAligner
import pandas as pd

from claudio.utils.utils import verbose_print, round_self


def double_check_data(data: pd.DataFrame, filename: str, df_xl_res: pd.DataFrame, output_directory: str, verbose_level: int):
    """
    Check given datapoints and correct it, if possible/needed

    Parameters
    ----------
    data : pd.DataFrame,
    filename : str,
    df_xl_res : pd.DataFrame,
    output_directory : str,
    verbose_level : int

    Returns
    -------
    data : pd.DataFrame
    """

    log_text = ''
    ind = 0
    data_len = len(data.index)

    # Save known interactions (drop duplicates)
    known_inters = []

    # Save newly created datapoints (in order to ensure that they aren't duplicated multiple times)
    new_datapoints = []

    for i, row in data.iterrows():
        verbose_print(f"\r\t[{round_self(ind * 100 / data_len, 2)}%]", 1, verbose_level, end='')
        ind += 1

        # SUCCESS: Remove empty entry
        pos_information_missing = (sum([not pd.isna(row.pos_a), not pd.isna(row.res_pos_a)]) < 1) or \
                                  (sum([not pd.isna(row.pos_b), not pd.isna(row.res_pos_b)]) < 1)
        is_erroneous_data = (type(row["seq_a"]) != str) or (type(row["seq_b"]) != str) or \
                            (type(row["pep_a"]) != str) or (type(row["pep_b"]) != str) or pos_information_missing
        if is_erroneous_data:
            log_text += f"{i}: erroneous entry (missing " \
                        f"{'sequence or peptide info' if not pos_information_missing else 'position info'}" \
                        f"). will be dropped\n"
            data.drop(i, inplace=True)
            log_text += "\tREMOVE\n"
            continue

        # FAIL: Neither of the specified residues are in the peptide (wrong peptide, or faulty interaction found)
        if all(res not in row["pep_a"] for res in df_xl_res.res.tolist()):
            log_text += f"{i}_a: pep_a does not contain any of the specified residues!\n"
            log_text += "\tFAIL\n"
        if all(res not in row["pep_b"] for res in df_xl_res.res.tolist()):
            log_text += f"{i}_b: pep_b does not contain any of the specified residues!\n"
            log_text += "\tFAIL\n"

        # REPLACE: Replace methionineoxide with methionine in peptide
        if "Mo" in row["pep_a"]:
            row["pep_a"] = row["pep_a"].replace("Mo", "M")
            log_text += f"{i}_a: Found 'Mo' in pep_a.\n"
            log_text += "\tREPLACE: Mo -> M\n"
        if "Mo" in row["pep_b"]:
            row["pep_b"] = row["pep_b"].replace("Mo", "M")
            log_text += f"{i}_b: Found 'Mo' in pep_b.\n"
            log_text += "\tREPLACE: Mo -> M\n"

        # ISSUE: Check if peptide is in full sequence as is (possible insertions are not considered)
        if row["pep_a"] not in row["seq_a"]:
            log_text += f"{i}_a: pep_a is not completely in full seq_a\n"
            log_text += f"\tISSUE\n"
        if row["pep_b"] not in row["seq_b"]:
            log_text += f"{i}_b: pep_b is not completely in full seq_b\n"
            log_text += f"\tISSUE\n"

        # Recompute residue positions for site a and b
        row, log_text = check_pep_pos(i, row, 'a', df_xl_res, log_text, verbose_level)
        row, log_text = check_pep_pos(i, row, 'b', df_xl_res, log_text, verbose_level)
        # Update row
        data.loc[i, :] = row

        # ISSUE: Check if peptide occurs multiple times in full sequence as is (possible insertions are not considered)
        pep_found_multiple_times = False
        if row["seq_a"].count(row["pep_a"]) > 1:
            log_text += f"{i}_a: pep_a was found more than once in full seq_a\n"
            log_text += f"\tISSUE\n"
            pep_found_multiple_times = True
        if row["seq_b"].count(row["pep_b"]) > 1:
            log_text += f"{i}_b: pep_b was found more than once in full seq_b\n"
            log_text += f"\tISSUE\n"
            pep_found_multiple_times = True

        # If any peptide was found multiple times, create possible variations (add them later (*))
        if pep_found_multiple_times:
            datapoints, log_text = create_duplicates(row, df_xl_res, log_text)
            new_datapoints.append(datapoints)

        # If not in known interactions, save unip ids and positions in known interactions, else drop datapoint
        interaction_info = sorted([row["unip_id_a"], row["unip_id_b"], str(row["pos_a"]), str(row["pos_b"])])
        if interaction_info not in [x for _, x in known_inters]:
            known_inters.append((i, interaction_info))
        else:
            for known_i, known_inter in known_inters:
                if interaction_info == known_inter:
                    log_text += f"{i}: entry is a DUPLICATE (see entry {known_i}). will be removed\n"
                    data.drop(i, inplace=True)
                    log_text += "\tSUCCESS\n"
                    break

        verbose_print(f"\r\t[{round_self(ind * 100 / data_len, 2)}%]", 1, verbose_level, end='')
    verbose_print("", 1, verbose_level)

    # Add aforementioned possible variations to the end of the dataset (*)
    for dp in new_datapoints:
        data = pd.concat([data, dp]).drop_duplicates().reset_index(drop=True)

    log_text += f"\n======================================================================\nFinal result:\n" \
                f"\tFAILS: {log_text.count('FAIL')}\n" \
                f"\tREMOVES: {log_text.count('REMOVE')}\n" \
                f"\tSUCCESSES: {log_text.count('SUCCESS')}\n" \
                f"\tISSUES: {log_text.count('ISSUE')}\n" \
                f"\tDUPLICATES: {log_text.count('DUPLICATE')}\n" \
                f"\tCREATED: {log_text.count('CREATED')}"

    # Save logfile
    output_path = f"{output_directory}{filename}.log"
    with open(output_path, 'w') as log_f:
        log_f.write(log_text)

    return data


def check_pep_pos(i: int, row: pd.Series, site: str, df_xl_res: pd.DataFrame, log_text: str, verbose_level: int):
    """
    Check given positions and correct it, if possible/needed

    Parameters
    ----------
    i : int,
    row : pd.Series,
    site : str,
    df_xl_res : pd.DataFrame,
    log_text : str,
    verbose_level : int

    Returns
    -------
    row : pd.Series,
    log_text : str
    """

    seq = row[f"seq_{site}"]
    pep_pos = int(row[f"pos_{site}"])
    peptide = row[f"pep_{site}"]

    wrong_pos = False
    try:
        # Collect booleans whether aminoacid at given position is any of the residues with specified position
        fits_specification = []
        for _, dp in df_xl_res.iterrows():
            # residue may be found anywhere in the peptide
            if dp.pos == 0:
                fits_position = True
            # residue may be found at the start of the peptide
            elif dp.pos == 1:
                fits_position = dp.pos == pep_pos
            # residue may be found at the end of the peptide
            elif dp.pos == -1:
                fits_position = dp.pos == pep_pos + (len(peptide) - 1)
            else:
                print("Error! Unforeseen value for residue position specification (this should not be able to "
                      "happen here)!")
                sys.exit()
            fits_specification.append((seq[pep_pos - 1] == dp.res) and fits_position)
        # Check whether aminoacid at given position is any of the residues with specified position
        if not any(fits_specification):
            log_text += f"{i}_{site}: residue in peptide at pos_{site} is not any of the specified residues.\n"
            wrong_pos = True
    except IndexError:
        # Catch given position out of bounds exception
        log_text += f"{i}_{site}: given pos_{site} is out of bounds of sequence.\n"
        wrong_pos = True

    # Recompute position if acid at position is not of the specified ones, or if position out of bounds
    if wrong_pos:
        pos_replaced = False
        # Count peptide-as-is-occurences in full sequence
        pep_count_in_seq = seq.count(peptide)

        # Parse through possible residues
        for _, dp in df_xl_res.iterrows():
            # Peptide occurred exactly once in sequence (uniquely identified peptide)
            if pep_count_in_seq == 1:
                # If position has not been replaced yet
                if not pos_replaced:
                    log_text += f"\tfound pep_{site} exactly once in full sequence\n"
                    res_count = peptide.count(dp.res)
                    if res_count == 0:
                        log_text += f"\tno {dp.res} found in pep_{site}\n"
                    else:
                        # Check if residue at specified position is the searched one
                        if dp.pos != 0:
                            log_text += f"\tcheck {dp.res} at specified position (={dp.pos}) in seq\n"
                            log_text += f"\t\tVERIFY: new residue is '{dp.res}': " \
                                        f"{seq[0] == dp.res if dp.pos == 1 else seq[-1] == dp.res}\n"
                            if seq[0] == dp.res if dp.pos == 1 else seq[-1] == dp.res:
                                row[f"pos_{site}"] = dp.pos if dp.pos == 1 else pep_pos + (len(peptide) - 1)
                                log_text += f"\tREPLACE: pos_{site}: {pep_pos} -> " \
                                            f"{dp.pos if dp.pos == 1 else pep_pos + (len(peptide) - 1)}\n"
                                log_text += f"\tSUCCESS\n"
                                pos_replaced = True
                            else:
                                log_text += f"\tFAIL\n"
                        # Else, try to find searched residue
                        else:
                            # SUCCESS: Uniquely identified residue, replace given position with its (Verify,
                            # FAIL if wrong)
                            if res_count == 1:
                                log_text += f"\tfound {dp.res} exactly once in pep_{site}\n"
                                new_pos = seq.find(peptide) + peptide.find(dp.res) + 1
                                log_text += f"\t\tVERIFY: new residue is '{dp.res}': {seq[new_pos - 1] == dp.res}\n"
                                if seq[new_pos - 1] == dp.res:
                                    row[f"pos_{site}"] = new_pos
                                    log_text += f"\tREPLACE: pos_{site}: {pep_pos} -> {new_pos}\n"
                                    log_text += f"\tSUCCESS\n"
                                    pos_replaced = True
                                else:
                                    log_text += f"\tFAIL\n"

                            # More than one searched residue in peptide (impossible to identify correct one, if not
                            # specified by data)
                            else:
                                log_text += f"\tfound {dp.res} more than once in pep_{site}\n"
                                # SUCCESS: Try res_pos specification (only for data by Liu et al.), if so replace given
                                # position with it (Verify, FAIL if wrong)
                                try:
                                    res_pos = int(row[f"res_pos_{site}"])
                                    log_text += f"\tres_pos_{site} was given\n"
                                    new_pos = seq.find(peptide) + res_pos
                                    log_text += f"\t\tVERIFY: new residue is '{dp.res}': {seq[new_pos - 1] == dp.res}\n"
                                    if seq[new_pos - 1] == dp.res:
                                        row[f"pos_{site}"] = new_pos
                                        log_text += f"\tREPLACE: pos_{site}: {pep_pos} -> {new_pos}\n"
                                        log_text += f"\tSUCCESS\n"
                                        pos_replaced = True
                                    else:
                                        log_text += f"\tFAIL\n"
                                # FAIL: res_pos not given
                                except:
                                    log_text += f"\tres_pos_{site} was not given\n"
                                    log_text += "\tFAIL\n"

            # Align peptide to sequence, if peptide found more than once or not found
            else:
                # If position has not been replaced yet
                if not pos_replaced:
                    log_text += f"\tfound pep_{site} more than once or not even once in sequence\n"
                    try:
                        res_pos = int(row[f"res_pos_{site}"])
                        log_text += f"\tres_pos_{site} was given\n"
                        log_text += "\talign peptide to sequence\n"
                        new_pos = realign_pep_to_seq(seq, peptide, res_pos, verbose_level)
                        if new_pos is None:
                            log_text += f"\talignment attempt failed for residue '{dp.res}'\n"
                            log_text += "\tFAIL\n"
                        else:
                            log_text += f"\t\tVERIFY: new residue is '{dp.res}': {seq[new_pos - 1] == dp.res}\n"
                            if seq[new_pos - 1] == dp.res:
                                row[f"pos_{site}"] = new_pos
                                log_text += f"\tREPLACE: pos_{site}: {pep_pos} -> {new_pos}\n"
                                log_text += f"\tSUCCESS\n"
                                pos_replaced = True
                            else:
                                log_text += f"\tFAIL\n"
                    # FAIL: res_pos not given
                    except:
                        log_text += f"\tres_pos_{site} was not given\n"
                        log_text += "\tFAIL\n"

    return row, log_text


def realign_pep_to_seq(seq: str, peptide:str, res_pos: int, verbose_level:int):
    """
    Align peptide to sequence and based on res_pos in peptide compute res_pos in sequence, return None if this fails

    Parameters
    ----------
    seq : str,
    peptide : str,
    res_pos : int,
    verbose_level : int

    Returns
    -------
    new_res_pos : ( int | None )
    """

    # Set alignment parameters
    aligner = PairwiseAligner()
    aligner.mode = "local"
    aligner.open_gap_score = -4
    aligner.extend_gap_score = 0
    aligner.match_score = 1
    aligner.mismatch_score = 0
    # aligner.substitution_matrix = substitution_matrices.load("BLOSUM62")

    # Try aligning, if it fails return None
    try:
        alignment = aligner.align(seq, peptide)[0]
    except ValueError:
        return None
    verbose_print(f"\tAlignment:\n{alignment}", 3, verbose_level)
    aligned_seq = str(alignment).split('\n')[0]
    aligned_pep = str(alignment).split('\n')[2]

    # Find res_pos in aligned peptide
    aligned_pep_i = -1
    aligned_pep_pos = 0
    for i, c in enumerate(aligned_pep):
        aligned_pep_i = i
        if c not in [' ', '-']:
            aligned_pep_pos += 1
        if aligned_pep_pos == res_pos:
            break

    # Find res_pos in aligned sequence and compute according new_res_pos in unaligned sequence, return new_res_pos if
    # successful, else return None
    try:
        _ = aligned_seq[aligned_pep_i + 1]
        new_res_pos = len(aligned_seq[:aligned_pep_i + 1].replace(' ', '').replace('-', ''))
        if new_res_pos > 0:
            al_seq = str(alignment).split('\n')[1]
            verbose_print(f"\tAligned site (index: {aligned_pep_i}):\n"
                          f"\t\t{aligned_seq[aligned_pep_i]}\n"
                          f"\t\t{al_seq[aligned_pep_i]}\n"
                          f"\t\t{aligned_pep[aligned_pep_i]}", 2, verbose_level)
            return new_res_pos
        else:
            return None
    except IndexError:
        return None


def create_duplicates(row: pd.Series, df_xl_res: pd.DataFrame, log_text: str):
    """
    Check if peptides in datapoint occur multiple times in sequence, if so create dataset with possible permutations
    
    Parameters
    ----------
    row : pd.Series,
    df_xl_res : pd.DataFrame,
    log_text : str

    Returns
    -------
    new_datapoints : pd.DataFrame,
    log_text : str
    """

    new_datapoints = []

    shift_a, \
        shift_b = (-1 for _ in range(2))

    for _, dp in df_xl_res.iterrows():
        # set sequences
        seq_a = row.seq_a
        seq_b = row.seq_b

        # Only create new datapoints, if the current residue can be placed in multiple positions
        if dp.pos == 0:
            row.res_pos_a = str(row.res_pos_a)
            row.res_pos_b = str(row.res_pos_b)
            # Make sure that the crosslinked residue can be uniquely identified for pep_a
            if ((row.pep_a.count(dp.res) == 1) or row.res_pos_a.replace(' ', '')) and seq_a.count(row.pep_a) != 1:
                # Find all positions of pep_a
                pep_a_positions = [i for i in range(len(seq_a)) if seq_a[i:].startswith(row.pep_a)]
                # Compute shift for pos_a
                shift_a = row.pep_a.find(dp.res) if row.pep_a.count(dp.res) == 1 else int(row.res_pos_a) - 1
                # Add old pos_a if not already in position set
                old_pos_a = row.pos_a - shift_a - 1
                if old_pos_a not in pep_a_positions:
                    pep_a_positions.append(old_pos_a)
                pep_a_positions = sorted(pep_a_positions)

            # Make sure that the crosslinked residue can be uniquely identified for pep_b
            if ((row.pep_b.count(dp.res) == 1) or row.res_pos_b) and seq_b.count(row.pep_b) != 1:
                # Find all positions of pep_b
                pep_b_positions = [i for i in range(len(seq_b)) if seq_b[i:].startswith(row.pep_b)]
                # Compute shift for pos_b
                shift_b = row.pep_b.find(dp.res) if row.pep_b.count(dp.res) == 1 else int(row.res_pos_b) - 1
                # Add old pos_b if not already in position set
                old_pos_b = row.pos_b - shift_b - 1
                if old_pos_b not in pep_b_positions:
                    pep_b_positions.append(old_pos_b)
                pep_b_positions = sorted(pep_b_positions)

            # Iterate through all possible peptide position permutations
            ind = 1
            if shift_a != -1 and shift_b != -1:
                total_count = len(pep_a_positions) * len(pep_b_positions)
                for pos_a in pep_a_positions:
                    for pos_b in pep_b_positions:
                        # Create new datapoint and set up shifts
                        new_datapoint = row.copy()
                        new_pos_a = pos_a + shift_a + 1
                        new_pos_b = pos_b + shift_b + 1

                        # If the new datapoint is not equal to the existing one
                        if (not ((row.pos_a == new_pos_a) and (row.pos_b == new_pos_b))) or \
                                ((row.pep_a == row.pep_b) and (row.pos_b == new_pos_a) and (row.pos_a == new_pos_b)):
                            log_text += f"\tcreate new datapoint ({ind} of {total_count}):\n"
                            ind += 1

                            # Verify new_pos_a
                            log_text += f"\t\tpos_a: {row.pos_a} -> {new_pos_a}\n" \
                                        f"\t\tVERIFY: new residue is '{dp.res}': {seq_a[new_pos_a - 1] == dp.res}\n"
                            if seq_a[new_pos_a - 1] == dp.res:
                                log_text += f"\t\t\tCREATED\n"
                            else:
                                log_text += f"\t\t\tFAIL\n"
                            new_datapoint.pos_a = new_pos_a

                            # Verify new_pos_b
                            log_text += f"\t\tpos_b: {row.pos_b} -> {new_pos_b}\n" \
                                        f"\t\tVERIFY: new residue is '{dp.res}': {seq_b[new_pos_b - 1] == dp.res}\n"
                            if seq_b[new_pos_b - 1] == dp.res:
                                log_text += f"\t\t\tSUCCESS\n"
                            else:
                                log_text += f"\t\t\tFAIL\n"
                            new_datapoint.pos_b = new_pos_b

                            new_datapoints.append(new_datapoint)
                        else:
                            log_text += f"\tdatapoint already in dataset ({ind} of {total_count})\n"
                            ind += 1

            elif shift_a != -1:
                total_count = len(pep_a_positions)
                for pos_a in pep_a_positions:
                    # Create new datapoint and set up shifts
                    new_datapoint = row.copy()
                    new_pos_a = pos_a + shift_a + 1

                    # If the new datapoint is not equal to the existing one
                    if not (row.pos_a == new_pos_a):
                        log_text += f"\tcreate new datapoint ({ind} of {total_count}):\n"
                        ind += 1

                        # Verify new_pos_a
                        log_text += f"\t\tpos_a: {row.pos_a} -> {new_pos_a}\n" \
                                    f"\t\tVERIFY: new residue is '{dp.res}': {seq_a[new_pos_a - 1] == dp.res}\n"
                        if seq_a[new_pos_a - 1] == dp.res:
                            log_text += f"\t\t\tCREATED\n"
                        else:
                            log_text += f"\t\t\tFAIL\n"
                        new_datapoint.pos_a = new_pos_a

                        new_datapoints.append(new_datapoint)
                    else:
                        log_text += f"\tdatapoint already in dataset ({ind} of {total_count})\n"
                        ind += 1

            elif shift_b != -1:
                total_count = len(pep_b_positions)
                for pos_b in pep_b_positions:
                    # Create new datapoint and set up shifts
                    new_datapoint = row.copy()
                    new_pos_b = pos_b + shift_b + 1

                    # If the new datapoint is not equal to the existing one
                    if not (row.pos_b == new_pos_b):
                        log_text += f"\tcreate new datapoint ({ind} of {total_count}):\n"
                        ind += 1

                        # Verify new_pos_b
                        log_text += f"\t\tpos_b: {row.pos_b} -> {new_pos_b}\n" \
                                    f"\t\tVERIFY: new residue is '{dp.res}': {seq_b[new_pos_b - 1] == dp.res}\n"
                        if seq_b[new_pos_b - 1] == dp.res:
                            log_text += f"\t\t\tCREATED\n"
                        else:
                            log_text += f"\t\t\tFAIL\n"
                        new_datapoint.pos_b = new_pos_b

                        new_datapoints.append(new_datapoint)
                    else:
                        log_text += f"\tdatapoint already in dataset ({ind} of {total_count})\n"
                        ind += 1

            else:
                log_text += f"\tattempt to create new datapoints for peptide copies in full protein sequence failed\n" \
                            f"\tFAIL\n"

    return pd.concat(new_datapoints, axis=1).transpose(), log_text
