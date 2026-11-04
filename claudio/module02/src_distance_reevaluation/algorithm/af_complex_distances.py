"""Calculate distances for strictly mapped endpoints in one AF complex."""

from math import isfinite
from pathlib import Path
from tempfile import mkdtemp
import subprocess

from Bio.PDB import MMCIFParser, PDBIO, Polypeptide

from claudio.utils.utils import round_self

import pandas as pd

from claudio.utils.utils import build_xl_dataset
from claudio.module02.src_distance_reevaluation.algorithm.af_complex_mapping import (
    prepare_complex_distance_input,
)
from claudio.module02.src_distance_reevaluation.algorithm.calc_site_distances import (
    parse_topolink_distance,
)


def calculate_complex_site_dists(
    data, temp_dir, xl_residues, plddt_cutoff, topolink_bin, verbose_level,
):
    cutoff = float(plddt_cutoff)
    if not isfinite(cutoff) or not 0 <= cutoff <= 100:
        raise ValueError("pLDDT cutoff must be between 0 and 100")

    rules = build_xl_dataset(xl_residues)
    result = prepare_complex_distance_input(data, rules)
    for prefix in ("eucl", "topo"):
        result[f"{prefix}_dist_tplk"] = float("nan")
        result[f"{prefix}_dist_lower_bound"] = float("nan")
        result[f"{prefix}_dist_raw"] = pd.Series(
            None, index=result.index, dtype="object",
        )
    result["distance_status"] = "not_evaluable"
    result["distance_reason"] = pd.Series(
        None, index=result.index, dtype="object"
    )

    eligible = []
    for position, (_, row) in enumerate(result.iterrows()):
        if not row["res_criteria_fulfilled"]:
            reason = (
                row["mapping_reason_a"]
                or row["mapping_reason_b"]
                or "unmapped_endpoint"
            )
        elif any(
            not isfinite(value)
            for site in ("a", "b")
            for value in row[f"mapping_coord_{site}"]
        ):
            reason = "invalid_coordinates"
        elif any(
            not isfinite(row[f"pLDDT_{site}"])
            or not 0 <= row[f"pLDDT_{site}"] <= 100
            for site in ("a", "b")
        ):
            reason = "invalid_plddt"
        elif any(row[f"pLDDT_{site}"] < cutoff for site in ("a", "b")):
            reason = "low_plddt"
        elif (
            row["chain_a"] == row["chain_b"]
            and row["mapped_residue_id_a"] == row["mapped_residue_id_b"]
            and row["mapping_atom_a"] == row["mapping_atom_b"]
        ):
            reason = "identical_atom_endpoints"
        else:
            eligible.append(position)
            continue
        result.iat[position, result.columns.get_loc("distance_reason")] = reason

    if not eligible:
        return result

    selected = result.iloc[eligible].copy().reset_index(drop=True)
    # Keep distant pairs within the selected complex so distance
    # violations are not removed by the legacy proximity prefilter.
    selected["is_interfaced"] = True
    computed = calculate_site_dists(
        selected, temp_dir, rules, cutoff, topolink_bin, verbose_level,
    )

    distance_columns = [
        f"{prefix}_dist{suffix}"
        for prefix in ("eucl", "topo")
        for suffix in ("_tplk", "_lower_bound", "_raw")
    ]
    for local_position, original_position in enumerate(eligible):
        computed_row = computed.loc[local_position]
        for column in distance_columns:
            result.iat[
                original_position, result.columns.get_loc(column)
            ] = computed_row.get(column, float("nan"))

        available = all(
            pd.notna(computed_row.get(column))
            and isfinite(computed_row[column])
            for column in ("eucl_dist_tplk", "topo_dist_tplk")
        )
        has_bound = any(
            pd.notna(computed_row.get(column))
            and isfinite(computed_row[column])
            for column in ("eucl_dist_lower_bound", "topo_dist_lower_bound")
        )
        if has_bound:
            status, reason = "lower_bound", "topolink_lower_bound"
        elif available:
            status, reason = "computed", None
        else:
            status, reason = "not_evaluable", "distance_unavailable"
        result.iat[
            original_position, result.columns.get_loc("distance_status")
        ] = status
        result.iat[
            original_position, result.columns.get_loc("distance_reason")
        ] = reason

    return result

def _export_complex(path, target, chain_ids):
    """Translate the selected AF chains and full residue IDs for PDB export."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    ids = sorted(set(chain_ids))
    if len(ids) > len(alphabet):
        raise ValueError("AF complex TopoLink export supports at most 62 chains")
    aliases = {name: name for name in ids if len(name) == 1 and name in alphabet}
    available = iter(name for name in alphabet if name not in aliases.values())
    for name in ids:
        if name not in aliases:
            aliases[name] = next(available)
    model = next(MMCIFParser(QUIET=True).get_structure("complex", path).get_models())
    chains = list(model)
    for chain in chains:
        model.detach_child(chain.id)
    residues = {}
    for chain in chains:
        original_chain = chain.id
        if original_chain not in aliases:
            continue
        chain.id = aliases[original_chain]
        children = list(chain)
        for residue in children:
            chain.detach_child(residue.id)
        for number, residue in enumerate(children, start=1):
            residues[(original_chain, residue.id)] = (chain.id, number, residue.resname)
            residue.id = (residue.id[0], number, " ")
            chain.add(residue)
        model.add(chain)
    writer = PDBIO()
    writer.set_structure(model)
    writer.save(str(target))
    return residues


def calculate_site_dists(data, temp_dir, rules, plddt_cutoff, topolink_bin, verbose_level):
    """Run TopoLink for AF candidates without changing the ordinary M2 engine."""
    result = data.copy()
    Path(temp_dir).mkdir(parents=True, exist_ok=True)
    template = (Path(__file__).resolve().parents[3] / "data" / "topolink_inputfile.inp").read_text()
    for source, group in result.groupby("path", sort=False):
        task = Path(mkdtemp(prefix="af_complex_", dir=temp_dir)).resolve()
        (task / "struct").mkdir()
        (task / "in").mkdir()
        residues = _export_complex(source, task / "struct" / "structure.pdb",
                                   list(group["chain_a"]) + list(group["chain_b"]))
        observations = {}
        for index, row in group.iterrows():
            endpoints = []
            for site in ("a", "b"):
                chain, number, name = residues[(row[f"chain_{site}"], row[f"mapped_residue_id_{site}"])]
                endpoints.append((name, chain, number, row[f"mapping_atom_{site}"]))
            key = tuple(sorted(endpoints))
            observations.setdefault(key, []).append(index)
        observed = []
        for first, second in observations:
            observed.append(f"  observed {first[0]} {first[1]} {first[2]} {second[0]} {second[1]} {second[2]}\n")
        types = []
        entries = list(rules.itertuples())
        for i, first in enumerate(entries):
            for second in entries[i:]:
                types.append(f"  linktype {Polypeptide.one_to_three(first.res)} all all {first.atom} "
                             f"{Polypeptide.one_to_three(second.res)} all all {second.atom} 35\n")
        lines = ["linkdir ./\n"]
        for line in template.splitlines(keepends=True):
            if line.startswith("structure "):
                lines.append("structure struct/structure.pdb\n")
            elif line.startswith("linkdir"):
                continue
            elif line.startswith("  observed"):
                lines.extend(observed)
            elif line.startswith("  linktype"):
                lines.extend(types)
            else:
                lines.append(line)
        text = "".join(lines)
        (task / "in" / "topolink.tmp").write_text(text, encoding="utf-8")
        call = "topolink" if topolink_bin is None else str((Path(topolink_bin) / "topolink").resolve())
        log = task / "topo_complex.log"
        try:
            execution = subprocess.run([call, "in/topolink.tmp"], cwd=str(task),
                                       capture_output=True, text=True, encoding="utf-8",
                                       errors="replace", check=False)
        except OSError as error:
            log.write_text(f"IN:\n{text}\nSTART ERROR:\n{error}\n", encoding="utf-8")
            raise RuntimeError(f"Could not start TopoLink; see {log}") from error
        log.write_text(f"SOURCE: {source}\nIN:\n{text}\nOUT:\n{execution.stdout}\n"
                       f"STDERR:\n{execution.stderr}\n", encoding="utf-8")
        if execution.returncode:
            raise RuntimeError(f"TopoLink failed with exit code {execution.returncode}; see {log}")
        for line in execution.stdout.splitlines():
            fields = line.split()
            if fields[:1] != ["LINK:"] or len(fields) < 11:
                continue
            try:
                first = (fields[1], fields[2], int(fields[3]), fields[4])
                second = (fields[5], fields[6], int(fields[7]), fields[8])
            except ValueError:
                continue
            indices = observations.get(tuple(sorted((first, second))), [])
            for prefix, token in (("eucl", fields[9]), ("topo", fields[10])):
                value, bound = parse_topolink_distance(token)
                for index in indices:
                    result.at[index, f"{prefix}_dist_tplk"] = round_self(value, 3)
                    result.at[index, f"{prefix}_dist_lower_bound"] = bound
                    result.at[index, f"{prefix}_dist_raw"] = token
    return result
