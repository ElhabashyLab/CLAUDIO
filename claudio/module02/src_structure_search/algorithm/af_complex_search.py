import pandas as pd
from claudio.utils.af_complex import (
    fetch_complex_metadata,
    download_complex_cif,
    read_complex_chains,
    fetch_complex_candidates,
)
import json
from pathlib import Path
"""Match XL-MS protein endpoints to existing AF complex chains."""


def match_complex_chains(
    chains, protein_a, sequence_a, protein_b, sequence_b,
):
    """Return chain pairs matching both protein identities and sequences."""
    chains_a = [
        chain["chain_id"]
        for chain in chains
        if chain["protein_id"] == protein_a
        and chain["sequence"] == sequence_a
    ]
    chains_b = [
        chain["chain_id"]
        for chain in chains
        if chain["protein_id"] == protein_b
        and chain["sequence"] == sequence_b
    ]

    return [
        (chain_a, chain_b)
        for chain_a in chains_a
        for chain_b in chains_b
    ]
def assign_complex_chain_pairs(data, chains):
    """Assign matching complex chain pairs to input records."""
    assigned_rows = []
    reserved_indices = {str(index) for index in data.index}

    for input_index, row in data.iterrows():
        pairs = match_complex_chains(
            chains=chains,
            protein_a=row["unip_id_a"],
            sequence_a=row["seq_a"],
            protein_b=row["unip_id_b"],
            sequence_b=row["seq_b"],
        )

        if not pairs:
            assigned = row.copy()
            assigned["chain_a"] = "-"
            assigned["chain_b"] = "-"
            assigned["af_match_status"] = "no_matching_chain_pair"
            assigned_rows.append(assigned)
            continue

        for candidate_number, (chain_a, chain_b) in enumerate(pairs):
            assigned = row.copy()

            if candidate_number > 0:
                suffix = candidate_number
                candidate_index = f"{input_index}_{suffix}"

                while candidate_index in reserved_indices:
                    suffix += 1
                    candidate_index = f"{input_index}_{suffix}"

                reserved_indices.add(candidate_index)
                assigned = assigned.rename(candidate_index)
            assigned["chain_a"] = chain_a
            assigned["chain_b"] = chain_b
            assigned["af_match_status"] = "matched"
            assigned_rows.append(assigned)

    if not assigned_rows:
        result = data.copy()
        result["chain_a"] = pd.Series(index=result.index, dtype="object")
        result["chain_b"] = pd.Series(index=result.index, dtype="object")
        result["af_match_status"] = pd.Series(
            index=result.index, dtype="object"
        )
        return result

    return pd.DataFrame(assigned_rows)
def retrieve_af_complex(data, model_id, output_dir):
    """Retrieve a specified AF complex and assign its chains to records."""
    records = fetch_complex_metadata(model_id)

    returned_model_ids = {
        record.get("modelEntityId") for record in records
    }
    if returned_model_ids != {model_id}:
        raise ValueError(
            f"Unexpected model identity: requested {model_id}, "
            f"received {returned_model_ids}"
        )

    structure_path = download_complex_cif(records, output_dir)
    chains = read_complex_chains(structure_path, records)
    metadata_path = Path(output_dir) / (
        f"{records[0]['modelEntityId']}"
        f"-metadata_v{records[0]['latestVersion']}.json"
    )
    metadata_path.write_text(
        json.dumps(records, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    result = assign_complex_chain_pairs(data, chains)

    result["af_model_id"] = records[0]["modelEntityId"]
    result["af_model_version"] = records[0]["latestVersion"]
    result["af_metadata_path"] = str(metadata_path)
    result["path"] = "-"
    matched = result["af_match_status"].eq("matched")
    result.loc[matched, "path"] = str(structure_path)

    return result


def filter_complex_candidates(candidates, protein_a, protein_b):
    """Keep complex candidates containing both input proteins."""
    matching = []

    for candidate in candidates:
        if candidate.get("isComplex") is not True:
            continue

        proteins = candidate.get("uniprotAccession", [])

        if protein_a in proteins and protein_b in proteins:
            matching.append(candidate)

    return matching


def discover_complex_candidates(protein_a, protein_b):
    """Discover existing AFDB complexes containing both input proteins."""
    candidates = fetch_complex_candidates(protein_a)

    return filter_complex_candidates(
        candidates,
        protein_a=protein_a,
        protein_b=protein_b,
    )


def retrieve_discovered_complexes(data, output_dir):
    """Discover and retrieve complex models for input protein pairs."""
    pair_positions = {}

    # Group row positions by protein pair.
    # A-B and B-A share the same discovery query.
    for position, (protein_a, protein_b) in enumerate(
        zip(data["unip_id_a"], data["unip_id_b"])
    ):
        pair = tuple(sorted((protein_a, protein_b)))
        pair_positions.setdefault(pair, []).append(position)

    model_positions = {}
    unmatched_positions = []

    # Discover models and collect their associated input rows.
    for pair, positions in pair_positions.items():
        candidates = discover_complex_candidates(*pair)

        if len(candidates) == 0:
            unmatched_positions.extend(positions)
            continue

        for candidate in candidates:
            model_id = candidate["modelEntityId"]
            model_positions.setdefault(model_id, set()).update(positions)

    retrieved = []

    # Retrieve each model once, using only its associated records.
    for model_id, positions in model_positions.items():
        subset = data.iloc[sorted(positions)].copy()
        result = retrieve_af_complex(subset, model_id, output_dir)
        retrieved.append(result)

    # Preserve records for which discovery found no candidate.
    if unmatched_positions:
        unmatched = data.iloc[sorted(unmatched_positions)].copy()

        unmatched["af_match_status"] = "no_candidate_model"
        unmatched["chain_a"] = "-"
        unmatched["chain_b"] = "-"
        unmatched["path"] = "-"
        unmatched["af_model_id"] = pd.NA
        unmatched["af_model_version"] = pd.NA
        unmatched["af_metadata_path"] = pd.NA

        retrieved.append(unmatched)

    if not retrieved:
        return data.copy()

    if len(retrieved) == 1:
        return retrieved[0]

    combined = pd.concat(retrieved)

    # Keep candidate indices unique across models.
    reserved_indices = {str(index) for index in combined.index}
    used_indices = set()
    unique_indices = []

    for index in combined.index:
        new_index = index

        if str(index) in used_indices:
            suffix = 1
            new_index = f"{index}_{suffix}"

            while (
                str(new_index) in reserved_indices
                or str(new_index) in used_indices
            ):
                suffix += 1
                new_index = f"{index}_{suffix}"

        used_indices.add(str(new_index))
        unique_indices.append(new_index)

    combined.index = pd.Index(
        unique_indices,
        name=combined.index.name,
    )

    return combined