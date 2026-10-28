"""Checks data for duplicates, missing information, and corrects it if possible."""
import sys
from Bio.Align import PairwiseAligner
import pandas as pd

from claudio.utils.utils import verbose_print, round_self


def double_check_data(data: pd.DataFrame, filename: str,
                      df_xl_res: pd.DataFrame, output_directory: str,
                      verbose_level: int):
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
    known_inters = set()

    # Save newly created datapoints (in order to ensure that they
    # aren't duplicated multiple times)
    new_datapoints = []

    # Add columns to df for peptide repeats
    data["pep_a_repeated"] = False
    data["pep_b_repeated"] = False
    data["pep_a_repeat_count"] = 0
    data["pep_b_repeat_count"] = 0

    for i, row in data.iterrows():
        verbose_print(f"[{round_self(ind * 100 / data_len, 2)}%]", 1,
                      verbose_level, start='\r\t\t', end='')
        ind += 1

        # SUCCESS: Remove empty entry
        pos_info_missing = (sum([not pd.isna(row.pos_a), not pd.isna(row.res_pos_a)]) < 1) or \
                                  (sum([not pd.isna(row.pos_b), not pd.isna(row.res_pos_b)]) < 1)
        is_erroneous_data = ((not isinstance(row["unip_id_a"], str))
                             or (not isinstance(row["unip_id_b"], str))
                             or (row["unip_id_a"] == 'nan')
                             or (row["unip_id_b"] == 'nan')
                             or (not isinstance(row["seq_a"], str))
                             or (not isinstance(row["seq_b"], str))
                             or (row["seq_a"] == 'nan')
                             or (row["seq_b"] == 'nan')
                             or (not isinstance(row["pep_a"], str))
                             or (not isinstance(row["pep_b"], str))
                             or (row["pep_a"] == 'nan')
                             or (row["pep_b"] == 'nan')
                             or pos_info_missing)
        if is_erroneous_data:
            log_text += f"{i}: erroneous entry (missing " \
                        f"{'position info' if pos_info_missing else 'sequence or peptide info'}" \
                        f"). will be dropped\n"
            data.drop(i, inplace=True)
            log_text += "\tREMOVE\n"
            continue

        # FAIL: Neither of the specified residues are in the peptide
        # (wrong peptide, or faulty interaction found)
        if all(res not in row["pep_a"] for res in df_xl_res.res.tolist()):
            log_text += f"{i}_a: pep_a does not contain any of the specified residues!\n"
            log_text += "\tFAIL\n"
        if all(res not in row["pep_b"] for res in df_xl_res.res.tolist()):
            log_text += f"{i}_b: pep_b does not contain any of the specified residues!\n"
            log_text += "\tFAIL\n"

        # REPLACE: Replace methionineoxide with methionine in peptide
        if any([m in row["pep_a"] for m in ['Mox', 'Mo']]):
            row["pep_a"] = row["pep_a"].replace("Mox", "M").replace("Mo", "M")
            log_text += f"{i}_a: Found 'Mo(x)' in pep_a.\n"
            log_text += "\tREPLACE: Mo(x) -> M\n"
        if any([m in row["pep_b"] for m in ['Mox', 'Mo']]):
            row["pep_b"] = row["pep_b"].replace("Mox", "M").replace("Mo", "M")
            log_text += f"{i}_b: Found 'Mo(x)' in pep_b.\n"
            log_text += "\tREPLACE: Mo(x) -> M\n"

        # ISSUE: Check if peptide is in full sequence as is
        # (possible insertions are not considered)
        if row["pep_a"] not in row["seq_a"]:
            log_text += f"{i}_a: pep_a is not completely in full seq_a\n"
            log_text += "\tISSUE\n"
        if row["pep_b"] not in row["seq_b"]:
            log_text += f"{i}_b: pep_b is not completely in full seq_b\n"
            log_text += "\tISSUE\n"

        # Recompute both endpoints; a failed record must not stop the batch.
        for site in ("a", "b"):
            row, log_text = check_pep_pos(
                i, row, site, df_xl_res, log_text, verbose_level,
            )
            if row is None:
                log_text += (
                    f"{i}_{site}: position recovery failed; entry will be dropped.\n"
                    "\tREMOVE\n"
                )
                data.drop(i, inplace=True)
                break
        if row is None:
            continue

        # ISSUE: Check if peptide occurs multiple times in full sequence
        # as is (possible insertions are not considered)
        pep_found_multiple_times = False
        pep_a_repeat_count = row["seq_a"].count(row["pep_a"])
        pep_b_repeat_count = row["seq_b"].count(row["pep_b"])
        if pep_a_repeat_count > 1:
            row["pep_a_repeated"] = True
            row["pep_a_repeat_count"] = pep_a_repeat_count
            log_text += f"{i}_a: pep_a was found more than once in full seq_a\n"
            log_text += "\tISSUE\n"
            pep_found_multiple_times = True
        if pep_b_repeat_count > 1:
            row["pep_b_repeated"] = True
            row["pep_b_repeat_count"] = pep_b_repeat_count
            log_text += f"{i}_b: pep_b was found more than once in full seq_b\n"
            log_text += "\tISSUE\n"
            pep_found_multiple_times = True

        # Update row
        data.loc[i, :] = row

        # If any peptide was found multiple times, create possible variations
        # (add them later (*))
        if pep_found_multiple_times:
            datapoints, log_text = create_duplicates(row, df_xl_res, log_text)
            new_datapoints.append(datapoints)

        # If not in known interactions, save unip ids and positions in known
        # interactions, else drop datapoint
        interaction_info = tuple(sorted([row["unip_id_a"], row["unip_id_b"],
                                         str(row["pos_a"]), str(row["pos_b"])]))
        if interaction_info not in [x for _, x in known_inters]:
            known_inters.add((i, interaction_info))
        else:
            for known_i, known_inter in known_inters:
                if interaction_info == known_inter:
                    log_text += f"{i}: entry is a DUPLICATE (see entry {known_i}). will be removed\n"
                    data.drop(i, inplace=True)
                    log_text += "\tSUCCESS\n"
                    break

        verbose_print(f"[{round_self(ind * 100 / data_len, 2)}%]", 1,
                      verbose_level, start='\r\t\t', end='')
    verbose_print("", 1, verbose_level)

    # Add aforementioned possible variations to the end of the dataset (*)
    if new_datapoints:
        data = pd.concat([data] + new_datapoints).drop_duplicates().reset_index(drop=True)

    log_text += f"\n======================================================================\nFinal result:\n" \
                f"\tFAILS: {log_text.count('FAIL')}\n" \
                f"\tREMOVES: {log_text.count('REMOVE')}\n" \
                f"\tSUCCESSES: {log_text.count('SUCCESS')}\n" \
                f"\tISSUES: {log_text.count('ISSUE')}\n" \
                f"\tDUPLICATES: {log_text.count('DUPLICATE')}\n" \
                f"\tCREATED: {log_text.count('CREATED')}"

    # Save logfile
    output_path = f"{output_directory}{filename}_preprocessing.log"
    with open(output_path, 'w', encoding="utf-8") as log_f:
        log_f.write(log_text)

    return data


def check_pep_pos(i: int, row: pd.Series, site: str, df_xl_res: pd.DataFrame,
                  log_text: str, verbose_level: int):
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
    row : pd.Series | None,
        Corrected row, or None when no reliable position can be recovered.
    log_text : str
    """

    seq = row[f"seq_{site}"]
    pep_pos = row[f"pos_{site}"]
    peptide = row[f"pep_{site}"]

    wrong_pos = False
    try:
        # Collect booleans whether aminoacid at given position is any of the
        # residues with specified position
        fits_specification = []
        for dp in df_xl_res.itertuples():
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
                print("Error! Unforeseen value for residue position specification "
                      "(this should not be able to happen here)!")
                sys.exit(1)
            fits_specification.append((seq[pep_pos - 1] == dp.res) and fits_position)
        # Check whether aminoacid at given position is any of the residues
        # with specified position
        if not any(fits_specification):
            log_text += f"{i}_{site}: residue in peptide at pos_{site} is not any of the specified residues.\n"
            wrong_pos = True
    except IndexError:
        # Catch given position out of bounds exception
        log_text += f"{i}_{site}: given pos_{site} is out of bounds of sequence.\n"
        wrong_pos = True
    # Check whether the protein position agrees with the peptide position.
    res_pos = row.get(f"res_pos_{site}", float("nan"))
    peptide_position = None
    if pd.notna(res_pos):
        try:
            value = float(res_pos)
        except (TypeError, ValueError, OverflowError):
            value = float("nan")

        if (
            isinstance(res_pos, bool) or not value.is_integer()
            or not 1 <= value <= len(peptide)
        ):
            log_text += (
                f"{i}_{site}: Invalid peptide position {res_pos}; "
                "attempting recovery.\n"
            )
            return _recover_peptide_position(
                i, row, site, df_xl_res, log_text, verbose_level,
            )
        else:
            peptide_position = int(value)
            peptide_residue = peptide[peptide_position - 1]
            if peptide_residue not in set(df_xl_res["res"]):
                log_text += (
                    f"{i}_{site}: peptide position does not satisfy "
                    f"cross-link residue rules ({peptide_residue}); "
                    "attempting recovery.\n"
                )
                return _recover_peptide_position(
                    i, row, site, df_xl_res, log_text, verbose_level,
                )

            peptide_start = pep_pos - peptide_position
            peptide_matches = (
                peptide_start >= 0
                and seq[peptide_start:peptide_start + len(peptide)] == peptide
            )
            if not peptide_matches:
                log_text += (
                    f"{i}_{site}: protein position does not match "
                    "the supplied peptide and peptide position.\n"
                )
                wrong_pos = True
    elif peptide:
        peptide_starts = [
            start for start in range(len(seq) - len(peptide) + 1)
            if seq.startswith(peptide, start)
        ]
        if len(peptide_starts) == 1:
            peptide_start = peptide_starts[0]
            if not peptide_start <= pep_pos - 1 < peptide_start + len(peptide):
                log_text += (
                    f"{i}_{site}: protein position is outside "
                    "the uniquely matched peptide.\n"
                )
                wrong_pos = True

    if wrong_pos:
        return _recover_peptide_position(
            i, row, site, df_xl_res, log_text, verbose_level,
            peptide_position=peptide_position,
        )
    return row, log_text


def _recover_peptide_position(i, row, site, df_xl_res, log_text,
                             verbose_level, peptide_position=None):
    """Recover a protein position from exact matches or sequence alignment.

    Parameters
    ----------
    i : int,
    row : pd.Series,
    site : str,
    df_xl_res : pd.DataFrame,
    log_text : str,
    verbose_level : int,
    peptide_position : int | None
        Restrict recovery to this peptide position when it is trustworthy.

    Returns
    -------
    row : pd.Series | None,
        Corrected row, or None if recovery fails or remains ambiguous.
    log_text : str
    """
    seq = row[f"seq_{site}"]
    peptide = row[f"pep_{site}"]
    if not seq or not peptide:
        log_text += f"{i}_{site}: empty sequence or peptide; recovery failed.\n\tFAIL\n"
        return None, log_text
    offsets = (
        [peptide_position - 1] if peptide_position is not None
        else range(len(peptide))
    )

    def allowed(position, offset):
        return any(
            seq[position - 1] == peptide[offset] == rule.res
            and (
                rule.pos == 0
                or (rule.pos == 1 and position == 1)
                or (rule.pos == -1 and position == len(seq))
            )
            for rule in df_xl_res.itertuples()
        )

    candidates = set()
    starts = [
        start for start in range(len(seq) - len(peptide) + 1)
        if peptide and seq.startswith(peptide, start)
    ]
    for start in starts:
        for offset in offsets:
            position = start + offset + 1
            if allowed(position, offset):
                candidates.add((position, offset + 1))

    if not starts and peptide:
        log_text += f"{i}_{site}: attempt sequence alignment for peptide recovery.\n"
        aligner = PairwiseAligner()
        aligner.mode = "local"
        aligner.open_gap_score = -4
        aligner.extend_gap_score = 0
        aligner.match_score = 1
        aligner.mismatch_score = 0
        alignments = aligner.align(seq, peptide)
        for number, alignment in enumerate(alignments):
            if number >= 1000:
                log_text += (
                    f"{i}_{site}: AMBIGUOUS: too many optimal alignments "
                    "to establish a reliable position.\n\tFAIL\n"
                )
                return None, log_text
            target, query = alignment.aligned
            if (
                len(query) == 0 or query[0][0] != 0
                or query[-1][1] != len(peptide)
            ):
                continue
            verbose_print(f"\tAlignment:\n{alignment}", 3, verbose_level)
            for offset in offsets:
                for target_block, query_block in zip(target, query):
                    if query_block[0] <= offset < query_block[1]:
                        position = int(target_block[0] + offset - query_block[0] + 1)
                        if allowed(position, offset):
                            candidates.add((position, offset + 1))
                        break

    supported = {
        candidate for candidate in candidates
        if candidate[0] == row[f"pos_{site}"]
    }
    if len(supported) == 1:
        position, offset = supported.pop()
    elif len(candidates) == 1:
        position, offset = candidates.pop()
    elif candidates:
        log_text += (
            f"{i}_{site}: AMBIGUOUS: possible protein/peptide positions "
            f"{sorted(candidates)}; no unique correction.\n\tFAIL\n"
        )
        return None, log_text
    else:
        log_text += f"{i}_{site}: no reliable cross-link position found.\n\tFAIL\n"
        return None, log_text

    corrected = row.copy()
    corrected[f"pos_{site}"] = position
    corrected[f"res_pos_{site}"] = offset
    log_text += (
        f"{i}_{site}: REPLACE: pos_{site}: {row[f'pos_{site}']} -> {position}; "
        f"res_pos_{site}: {row.get(f'res_pos_{site}')} -> {offset}\n"
        "\tSUCCESS\n"
    )
    return corrected, log_text


def realign_pep_to_seq(seq: str, peptide:str, res_pos: int,
                       verbose_level:int):
    """
    Align peptide to sequence and based on res_pos in peptide compute res_pos
    in sequence, return None if this fails

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
    aligned_seq = str(alignment).split('\n',maxsplit=1)[0]
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

    # Find res_pos in aligned sequence and compute according new_res_pos in
    # unaligned sequence, return new_res_pos if successful, else return None
    try:
        _ = aligned_seq[aligned_pep_i + 1]
        new_res_pos = len(aligned_seq[:aligned_pep_i + 1].replace(' ', '').replace('-', ''))
        if new_res_pos > 0:
            al_seq = str(alignment).split('\n')[1]
            verbose_print(f"\tAligned site (index: {aligned_pep_i}):\n"
                          f"\t\t{aligned_seq[aligned_pep_i]}\n"
                          f"\t\t{al_seq[aligned_pep_i]}\n"
                          f"\t\t{aligned_pep[aligned_pep_i]}", 2, 
                          verbose_level)
            return new_res_pos
        return None
    except IndexError:
        return None


def create_duplicates(row: pd.Series, df_xl_res: pd.DataFrame, log_text: str):
    """
    Check if peptides in datapoint occur multiple times in sequence, 
    if so create dataset with possible permutations
    
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

    for dp in df_xl_res.itertuples():
        # set sequences
        seq_a = row.seq_a
        seq_b = row.seq_b

        # Only create new datapoints, if the current residue can be placed in
        # multiple positions
        if dp.pos == 0:
            # Make sure that the crosslinked residue can be uniquely
            # identified for pep_a
            a_is_unique = ((row.pep_a.count(dp.res) == 1) or not pd.isna(row.res_pos_a)) and (seq_a.count(row.pep_a) != 1)
            if a_is_unique:
                # Find all positions of pep_a
                pep_a_positions = [i for i in range(len(seq_a)) if seq_a[i:].startswith(row.pep_a)]
                # Compute shift for pos_a
                shift_a = row.pep_a.find(dp.res) if row.pep_a.count(dp.res) == 1 else int(row.res_pos_a) - 1
                # Add old pos_a if not already in position set
                old_pos_a = row.pos_a - shift_a - 1
                if old_pos_a not in pep_a_positions:
                    pep_a_positions.append(old_pos_a)
                pep_a_positions = sorted(pep_a_positions)

            # Make sure that the crosslinked residue can be uniquely
            # identified for pep_b
            b_is_unique = ((row.pep_b.count(dp.res) == 1) or not pd.isna(row.res_pos_b)) and (seq_b.count(row.pep_b) != 1)
            if b_is_unique:
                # Find all positions of pep_b
                pep_b_positions = [i for i in range(len(seq_b)) if seq_b[i:].startswith(row.pep_b)]
                # Compute shift for pos_b
                shift_b = row.pep_b.find(dp.res) if row.pep_b.count(dp.res) == 1 else int(row.res_pos_b) - 1
                # Add old pos_b if not already in position set
                old_pos_b = int(row.res_pos_b) - shift_b - 1
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
                                log_text += "\t\t\tCREATED\n"
                            else:
                                log_text += "\t\t\tFAIL\n"
                            new_datapoint.pos_a = new_pos_a

                            # Verify new_pos_b
                            log_text += f"\t\tpos_b: {row.pos_b} -> {new_pos_b}\n" \
                                        f"\t\tVERIFY: new residue is '{dp.res}': {seq_b[new_pos_b - 1] == dp.res}\n"
                            if seq_b[new_pos_b - 1] == dp.res:
                                log_text += "\t\t\tSUCCESS\n"
                            else:
                                log_text += "\t\t\tFAIL\n"
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
                    if row.pos_a != new_pos_a:
                        log_text += f"\tcreate new datapoint ({ind} of {total_count}):\n"
                        ind += 1

                        # Verify new_pos_a
                        log_text += f"\t\tpos_a: {row.pos_a} -> {new_pos_a}\n" \
                                    f"\t\tVERIFY: new residue is '{dp.res}': {seq_a[new_pos_a - 1] == dp.res}\n"
                        if seq_a[new_pos_a - 1] == dp.res:
                            log_text += "\t\t\tCREATED\n"
                        else:
                            log_text += "\t\t\tFAIL\n"
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
                    if row.pos_b != new_pos_b:
                        log_text += f"\tcreate new datapoint ({ind} of {total_count}):\n"
                        ind += 1

                        # Verify new_pos_b
                        log_text += f"\t\tpos_b: {row.pos_b} -> {new_pos_b}\n" \
                                    f"\t\tVERIFY: new residue is '{dp.res}': {seq_b[new_pos_b - 1] == dp.res}\n"
                        if seq_b[new_pos_b - 1] == dp.res:
                            log_text += "\t\t\tCREATED\n"
                        else:
                            log_text += "\t\t\tFAIL\n"
                        new_datapoint.pos_b = new_pos_b

                        new_datapoints.append(new_datapoint)
                    else:
                        log_text += f"\tdatapoint already in dataset ({ind} of {total_count})\n"
                        ind += 1

            else:
                log_text += "\tattempt to create new datapoints for peptide copies in full protein sequence failed\n" \
                            "\tFAIL\n"

    return pd.concat(new_datapoints, axis=1).transpose(), log_text
