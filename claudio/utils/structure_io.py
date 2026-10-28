"""Read PDB and mmCIF structure models."""

from Bio.PDB import MMCIFParser, PDBParser


def read_structure_models(path):
    path = str(path)

    if path.lower().endswith((".cif", ".mmcif")):
        models = MMCIFParser(QUIET=True).get_structure(
            "", path
        ).get_list()
    else:
        try:
            models = PDBParser(QUIET=True).get_structure(
                "", path
            ).get_list()
        except Exception:
            models = []

        if not models:
            models = MMCIFParser(QUIET=True).get_structure(
                "", path
            ).get_list()

    if not models:
        raise ValueError(f"No models found in structure file: {path}")

    return models
