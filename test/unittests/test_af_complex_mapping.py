"""Tests for mapping protein positions into AF complex structures."""

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from Bio.PDB import MMCIFParser, MMCIFIO
from claudio.module02.src_distance_reevaluation.algorithm.af_complex_mapping import (
    map_complex_residue,
)


FIXTURE_DIR = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "af_complex"
)


class TestAFComplexMapping(unittest.TestCase):
    def test_maps_chain_a_lysine_to_its_cb_atom(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        metadata = next(
            record for record in records
            if record["chainId"] == "A"
        )

        result = map_complex_residue(
            structure_path=FIXTURE_DIR / "AF-0000000208747029.cif",
            records=records,
            protein_id="A0A0P0Y832",
            protein_sequence=metadata["sequence"],
            chain_id="A",
            protein_position=67,
            atom_name="CB",
            position_status="valid",
        )

        self.assertEqual(result["mapping_status"], "mapped")
        self.assertEqual(result["protein_id"], "A0A0P0Y832")
        self.assertEqual(result["protein_position"], 67)
        self.assertEqual(result["chain_id"], "A")
        self.assertEqual(result["residue_id"], (" ", 67, " "))
        self.assertEqual(result["residue_name"], "LYS")
        self.assertEqual(result["atom_name"], "CB")

        expected_coordinates = (20.938, 33.286, 12.461)
        self.assertEqual(len(result["coord"]), 3)
        for actual, expected in zip(
            result["coord"], expected_coordinates
        ):
            self.assertAlmostEqual(actual, expected, places=3)
    def test_preserves_structure_numbering_and_insertion_code(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        metadata = next(
            record for record in records
            if record["chainId"] == "A"
        )

        structure = MMCIFParser(QUIET=True).get_structure(
            "renumbered",
            str(FIXTURE_DIR / "AF-0000000208747029.cif"),
        )
        model = next(structure.get_models())
        chain = model["A"]
        residues = list(chain)

        # Detach first to avoid collisions with existing residue IDs.
        for residue in residues:
            chain.detach_child(residue.id)

        for residue in residues:
            hetero_flag, number, insertion_code = residue.id
            residue.id = (
                hetero_flag,
                number + 100,
                "A" if number == 67 else insertion_code,
            )
            chain.add(residue)

        with TemporaryDirectory() as directory:
            structure_path = Path(directory) / "renumbered.cif"
            writer = MMCIFIO()
            writer.set_structure(structure)
            writer.save(str(structure_path))

            result = map_complex_residue(
                structure_path=structure_path,
                records=records,
                protein_id="A0A0P0Y832",
                protein_sequence=metadata["sequence"],
                chain_id="A",
                protein_position=67,
                atom_name="CB",
                position_status="valid",
            )

        self.assertEqual(result["mapping_status"], "mapped")
        self.assertEqual(result["protein_position"], 67)
        self.assertEqual(result["chain_id"], "A")
        self.assertEqual(result["residue_id"], (" ", 167, "A"))
        self.assertEqual(result["residue_name"], "LYS")
    def test_does_not_map_unresolved_positions(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        metadata = next(
            record for record in records
            if record["chainId"] == "A"
        )

        for status in ("ambiguous", "invalid"):
            with self.subTest(position_status=status):
                result = map_complex_residue(
                    structure_path=(
                        FIXTURE_DIR / "AF-0000000208747029.cif"
                    ),
                    records=records,
                    protein_id="A0A0P0Y832",
                    protein_sequence=metadata["sequence"],
                    chain_id="A",
                    protein_position=67,
                    atom_name="CB",
                    position_status=status,
                )

                self.assertEqual(
                    result["mapping_status"], "not_evaluable"
                )
                self.assertEqual(
                    result["mapping_reason"], "unresolved_position"
                )
                self.assertIsNone(result["residue_id"])
                self.assertIsNone(result["coord"])
    def test_reports_out_of_range_positions_without_crashing(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        metadata = next(
            record for record in records
            if record["chainId"] == "A"
        )

        # Chain A has 346 residues; positions are one-based.
        for position in (0, -1, 347):
            with self.subTest(protein_position=position):
                result = map_complex_residue(
                    structure_path=(
                        FIXTURE_DIR / "AF-0000000208747029.cif"
                    ),
                    records=records,
                    protein_id="A0A0P0Y832",
                    protein_sequence=metadata["sequence"],
                    chain_id="A",
                    protein_position=position,
                    atom_name="CB",
                    position_status="valid",
                )

                self.assertEqual(
                    result["mapping_status"], "not_evaluable"
                )
                self.assertEqual(
                    result["mapping_reason"], "position_out_of_range"
                )
                self.assertEqual(
                    result["protein_position"], position
                )
                self.assertIsNone(result["residue_id"])
                self.assertIsNone(result["coord"])
    def test_reports_chain_assignment_failures(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        metadata = next(
            record for record in records
            if record["chainId"] == "A"
        )

        arguments = {
            "structure_path": (
                FIXTURE_DIR / "AF-0000000208747029.cif"
            ),
            "records": records,
            "protein_id": "A0A0P0Y832",
            "protein_sequence": metadata["sequence"],
            "chain_id": "A",
            "protein_position": 67,
            "atom_name": "CB",
            "position_status": "valid",
        }

        cases = (
            (
                {"chain_id": "Z"},
                "chain_not_found",
            ),
            (
                {"protein_id": "P0C2Z6"},
                "protein_identity_mismatch",
            ),
            (
                {"protein_sequence": metadata["sequence"][:-1]},
                "sequence_mismatch",
            ),
        )

        for changes, expected_reason in cases:
            with self.subTest(reason=expected_reason):
                parameters = {**arguments, **changes}
                result = map_complex_residue(**parameters)

                self.assertEqual(
                    result["mapping_status"], "not_evaluable"
                )
                self.assertEqual(
                    result["mapping_reason"], expected_reason
                )
                self.assertIsNone(result["residue_id"])
                self.assertIsNone(result["coord"])
    def test_reports_missing_atom_and_preserves_residue_identity(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        metadata = next(
            record for record in records
            if record["chainId"] == "A"
        )

        structure = MMCIFParser(QUIET=True).get_structure(
            "missing_atom",
            str(FIXTURE_DIR / "AF-0000000208747029.cif"),
        )
        model = next(structure.get_models())

        # Remove CB only; other atoms, including CA, remain.
        residue = model["A"][67]
        residue.detach_child("CB")

        with TemporaryDirectory() as directory:
            structure_path = Path(directory) / "missing_cb.cif"
            writer = MMCIFIO()
            writer.set_structure(structure)
            writer.save(str(structure_path))

            result = map_complex_residue(
                structure_path=structure_path,
                records=records,
                protein_id="A0A0P0Y832",
                protein_sequence=metadata["sequence"],
                chain_id="A",
                protein_position=67,
                atom_name="CB",
                position_status="valid",
            )

        self.assertEqual(result["mapping_status"], "not_evaluable")
        self.assertEqual(result["mapping_reason"], "missing_atom")
        self.assertEqual(result["residue_id"], (" ", 67, " "))
        self.assertEqual(result["residue_name"], "LYS")
        self.assertEqual(result["atom_name"], "CB")
        self.assertIsNone(result["coord"])
    def test_validates_numeric_position_values(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        metadata = next(
            record for record in records
            if record["chainId"] == "A"
        )

        cases = (
            (67.0, "mapped", None),
            (67.5, "not_evaluable", "invalid_protein_position"),
            (float("nan"), "not_evaluable", "invalid_protein_position"),
            (float("inf"), "not_evaluable", "invalid_protein_position"),
            (None, "not_evaluable", "invalid_protein_position"),
            (True, "not_evaluable", "invalid_protein_position"),
        )

        for position, expected_status, expected_reason in cases:
            with self.subTest(protein_position=position):
                result = map_complex_residue(
                    structure_path=(
                        FIXTURE_DIR / "AF-0000000208747029.cif"
                    ),
                    records=records,
                    protein_id="A0A0P0Y832",
                    protein_sequence=metadata["sequence"],
                    chain_id="A",
                    protein_position=position,
                    atom_name="CB",
                    position_status="valid",
                )

                self.assertEqual(
                    result["mapping_status"], expected_status
                )
                self.assertEqual(
                    result["mapping_reason"], expected_reason
                )

                if expected_status == "mapped":
                    self.assertIsInstance(
                        result["protein_position"], int
                    )
                    self.assertEqual(result["protein_position"], 67)
                    self.assertEqual(
                        result["residue_id"], (" ", 67, " ")
                    )
                else:
                    self.assertIsNone(result["residue_id"])
                    self.assertIsNone(result["coord"])
    def test_reports_incomplete_structure_without_shifting_positions(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        metadata = next(
            record for record in records
            if record["chainId"] == "A"
        )

        structure = MMCIFParser(QUIET=True).get_structure(
            "incomplete",
            str(FIXTURE_DIR / "AF-0000000208747029.cif"),
        )
        model = next(structure.get_models())

        # Remove the residue immediately before target position 67.
        model["A"].detach_child((" ", 66, " "))

        with TemporaryDirectory() as directory:
            structure_path = Path(directory) / "incomplete.cif"
            writer = MMCIFIO()
            writer.set_structure(structure)
            writer.save(str(structure_path))

            result = map_complex_residue(
                structure_path=structure_path,
                records=records,
                protein_id="A0A0P0Y832",
                protein_sequence=metadata["sequence"],
                chain_id="A",
                protein_position=67,
                atom_name="CB",
                position_status="valid",
            )

        self.assertEqual(result["mapping_status"], "not_evaluable")
        self.assertEqual(
            result["mapping_reason"], "structure_metadata_mismatch"
        )
        self.assertIsNone(result["residue_id"])
        self.assertIsNone(result["coord"])
if __name__ == "__main__":
    unittest.main()
