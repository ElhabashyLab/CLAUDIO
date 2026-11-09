"""Retrieve and inspect existing AlphaFold protein-complex models."""

from Bio.PDB import MMCIFParser
from Bio.SeqUtils import seq1
import requests
from pathlib import Path
import gzip
class ComplexMetadataMismatchError(ValueError):
    """Structure chains do not match their AFDB metadata."""
def read_complex_chains(structure_path, records):
    """Read protein chains and associate them with AFDB metadata."""
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure("af_complex", str(structure_path))
    model = next(structure.get_models())

    metadata_by_chain = {
        record["chainId"]: record
        for record in records
    }

    chains = []

    for chain in model:
        residues = [
            residue for residue in chain
            if residue.id[0] == " "
        ]

        sequence = "".join(
            seq1(residue.resname)
            for residue in residues
        )

        if chain.id not in metadata_by_chain:
            raise ComplexMetadataMismatchError(
                f"Missing metadata for chain {chain.id}"
            )

        metadata = metadata_by_chain[chain.id]
        if sequence != metadata["sequence"]:
            raise ComplexMetadataMismatchError(
                f"Sequence mismatch for chain {chain.id}: "
                "structure sequence differs from AFDB metadata"
            )

        chains.append({
            "chain_id": chain.id,
            "protein_id": metadata["uniprotAccession"],
            "residue_count": len(residues),
            "sequence": sequence,
        })

    return chains

def fetch_complex_metadata(model_id):
    """Retrieve AFDB metadata for an existing protein-complex model."""
    url = f"https://alphafold.ebi.ac.uk/api/prediction/{model_id}"

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    records = response.json()
    if records == []:
        raise ValueError(f"No metadata found for model {model_id}")

    for record in records:
        if record.get("isComplex") is not True:
            raise ValueError(f"Model {model_id} is not a complex")

    return records
def download_complex_cif(records, output_dir):
    """Download a complex mmCIF file and return its local path."""
    cif_urls = {record["cifUrl"] for record in records}
    if len(cif_urls) != 1:
        raise ValueError("Inconsistent CIF URLs in complex metadata")

    model_identities = {
        (record["modelEntityId"], record["latestVersion"])
        for record in records
    }
    if len(model_identities) != 1:
        raise ValueError("Inconsistent model identity in complex metadata")
    record = records[0]
    url = record["cifUrl"]

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = (
        f"{record['modelEntityId']}"
        f"-model_v{record['latestVersion']}.cif"
    )
    structure_path = output_dir / filename
    content = response.content
    if content.startswith(b"\x1f\x8b"):
        content = gzip.decompress(content)

    structure_path.write_bytes(content)

    return structure_path

def fetch_complex_candidates(uniprot_id):
    """Return AFDB complex candidates containing a UniProt accession."""
    url = f"https://alphafold.ebi.ac.uk/api/complex/{uniprot_id}"
    response = requests.get(url, timeout=30)

    if response.status_code == 404:
        return []

    response.raise_for_status()
    return response.json()

def restore_preprocessing_tracking(data, sqcs_path):
    """Recover AF mapping provenance from the matching M1 report, not M3 input."""
    import pandas as pd

    source = Path(sqcs_path)
    report_path = source.with_name(source.stem + "_record_tracking.csv")
    if not report_path.is_file():
        return data.copy()
    report = pd.read_csv(report_path, index_col=0)
    if not report.index.is_unique or not data.index.is_unique:
        raise ValueError("Preprocessing report and input indices must be unique")
    if not data.index.isin(report.index).all():
        raise ValueError("Input rows are missing from the preprocessing report")
    report = report.loc[data.index]
    for column in ("unip_id_a", "unip_id_b", "pos_a", "pos_b"):
        if column not in report or column not in data:
            raise ValueError(f"Preprocessing report identity is missing: {column}")
        equal = data[column].eq(report[column]).fillna(False)
        equal |= data[column].isna() & report[column].isna()
        if not equal.all():
            raise ValueError(f"Input does not match preprocessing report: {column}")
    if "included_in_sqcs" not in report or not report["included_in_sqcs"].eq(True).all():
        raise ValueError("Input contains a row excluded by the preprocessing report")
    result = data.copy()
    columns = ["source_record_id", "candidate_id", "original_pos_a", "original_pos_b",
               "position_status_a", "position_status_b"]
    for column in columns:
        if column not in report:
            continue
        if column in result:
            equal = result[column].eq(report[column]).fillna(False)
            equal |= result[column].isna() & report[column].isna()
            if not equal.all():
                raise ValueError(f"Input contradicts preprocessing report: {column}")
        result[column] = report[column]
    return result
