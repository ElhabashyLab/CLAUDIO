"""Tests for assigning protein endpoints to AF complex chains."""

import json
import unittest
from pathlib import Path
import pandas as pd
from claudio.utils.af_complex import read_complex_chains
from claudio.module02.src_structure_search.algorithm.af_complex_search import (
    match_complex_chains, assign_complex_chain_pairs, retrieve_af_complex,
)
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch
from click.testing import CliRunner
from claudio.module02.src_structure_search.main import main as structure_search_main
FIXTURE_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "af_complex"


class TestMatchComplexChains(unittest.TestCase):
    def test_matches_both_proteins_to_their_chains(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        chains = read_complex_chains(
            FIXTURE_DIR / "AF-0000000208747029.cif",
            records,
        )
        by_id = {chain["chain_id"]: chain for chain in chains}

        pairs = match_complex_chains(
            chains=chains,
            protein_a="A0A0P0Y832",
            sequence_a=by_id["A"]["sequence"],
            protein_b="P0C2Z6",
            sequence_b=by_id["B"]["sequence"],
        )

        self.assertEqual(pairs, [("A", "B")])
    def test_reverses_chain_assignment_when_endpoints_are_reversed(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        chains = read_complex_chains(
            FIXTURE_DIR / "AF-0000000208747029.cif",
            records,
        )
        by_id = {chain["chain_id"]: chain for chain in chains}

        pairs = match_complex_chains(
            chains=chains,
            protein_a="P0C2Z6",
            sequence_a=by_id["B"]["sequence"],
            protein_b="A0A0P0Y832",
            sequence_b=by_id["A"]["sequence"],
        )

        self.assertEqual(pairs, [("B", "A")])
    def test_rejects_sequence_mismatch_at_either_endpoint(self):
        chains = [
            {
                "chain_id": "A",
                "protein_id": "TEST_P1",
                "sequence": "MAAKT",
            },
            {
                "chain_id": "B",
                "protein_id": "TEST_P2",
                "sequence": "MGKT",
            },
        ]

        for site in ("a", "b"):
            with self.subTest(site=site):
                sequence_a = "MAAKT"
                sequence_b = "MGKT"

                if site == "a":
                    sequence_a = "MAAKV"
                else:
                    sequence_b = "MGKV"

                pairs = match_complex_chains(
                    chains=chains,
                    protein_a="TEST_P1",
                    sequence_a=sequence_a,
                    protein_b="TEST_P2",
                    sequence_b=sequence_b,
                )

                self.assertEqual(pairs, [])
    def test_preserves_all_matching_chain_pairs(self):
        chains = [
            {
                "chain_id": "A",
                "protein_id": "TEST_P1",
                "sequence": "MAAKT",
            },
            {
                "chain_id": "C",
                "protein_id": "TEST_P1",
                "sequence": "MAAKT",
            },
            {
                "chain_id": "B",
                "protein_id": "TEST_P2",
                "sequence": "MGKT",
            },
            {
                "chain_id": "D",
                "protein_id": "TEST_P2",
                "sequence": "MGKT",
            },
        ]

        pairs = match_complex_chains(
            chains=chains,
            protein_a="TEST_P1",
            sequence_a="MAAKT",
            protein_b="TEST_P2",
            sequence_b="MGKT",
        )

        self.assertEqual(len(pairs), 4)
        self.assertEqual(
            set(pairs),
            {("A", "B"), ("A", "D"), ("C", "B"), ("C", "D")},
        )
    def test_preserves_same_chain_and_cross_chain_homomer_options(self):
        chains = [
            {
                "chain_id": "A",
                "protein_id": "TEST_P1",
                "sequence": "MAAKT",
            },
            {
                "chain_id": "B",
                "protein_id": "TEST_P1",
                "sequence": "MAAKT",
            },
        ]

        pairs = match_complex_chains(
            chains=chains,
            protein_a="TEST_P1",
            sequence_a="MAAKT",
            protein_b="TEST_P1",
            sequence_b="MAAKT",
        )

        self.assertEqual(len(pairs), 4)
        self.assertEqual(
            set(pairs),
            {("A", "A"), ("A", "B"), ("B", "A"), ("B", "B")},
        )
    def test_assigns_chains_to_record_and_preserves_provenance(self):
        chains = [
            {
                "chain_id": "A",
                "protein_id": "TEST_P1",
                "sequence": "MAAKT",
            },
            {
                "chain_id": "B",
                "protein_id": "TEST_P2",
                "sequence": "MGKT",
            },
        ]
        data = pd.DataFrame([{
            "unip_id_a": "TEST_P1",
            "unip_id_b": "TEST_P2",
            "seq_a": "MAAKT",
            "seq_b": "MGKT",
            "pos_a": 4,
            "pos_b": 3,
            "original_pos_a": 2,
            "original_pos_b": 3,
            "position_status_a": "corrected",
            "position_status_b": "valid",
            "source_record_id": "record_000001",
        }])
        original = data.copy(deep=True)

        result = assign_complex_chain_pairs(data, chains)

        self.assertEqual(len(result), 1)
        self.assertIn("chain_a", result.columns)
        self.assertIn("chain_b", result.columns)

        row = result.iloc[0]
        self.assertEqual((row["chain_a"], row["chain_b"]), ("A", "B"))

        for column in original.columns:
            self.assertEqual(row[column], original.iloc[0][column])

        pd.testing.assert_frame_equal(data, original)
    def test_expands_record_into_all_chain_pairs(self):
        chains = [
            {
                "chain_id": "A",
                "protein_id": "TEST_P1",
                "sequence": "MAAKT",
            },
            {
                "chain_id": "C",
                "protein_id": "TEST_P1",
                "sequence": "MAAKT",
            },
            {
                "chain_id": "B",
                "protein_id": "TEST_P2",
                "sequence": "MGKT",
            },
        ]
        data = pd.DataFrame([{
            "unip_id_a": "TEST_P1",
            "unip_id_b": "TEST_P2",
            "seq_a": "MAAKT",
            "seq_b": "MGKT",
            "pos_a": 4,
            "pos_b": 3,
            "original_pos_a": 2,
            "original_pos_b": 3,
            "position_status_a": "corrected",
            "position_status_b": "valid",
            "source_record_id": "record_000001",
        }])

        result = assign_complex_chain_pairs(data, chains)

        self.assertEqual(len(result), 2)
        self.assertEqual(
            set(zip(result["chain_a"], result["chain_b"])),
            {("A", "B"), ("C", "B")},
        )
        self.assertTrue(result["af_match_status"].eq("matched").all())

        for column in data.columns:
            self.assertTrue(
                result[column].eq(data.iloc[0][column]).all(),
                f"Original field changed during expansion: {column}",
            )

        self.assertTrue(result.index.is_unique)
    def test_preserves_unmatched_records_and_clears_old_chain_assignments(self):
        chains = [
            {
                "chain_id": "A",
                "protein_id": "TEST_P1",
                "sequence": "MAAKT",
            },
            {
                "chain_id": "B",
                "protein_id": "TEST_P2",
                "sequence": "MGKT",
            },
        ]

        for failure in ("protein_id", "sequence"):
            with self.subTest(failure=failure):
                record = {
                    "unip_id_a": "TEST_P1",
                    "unip_id_b": "TEST_P2",
                    "seq_a": "MAAKT",
                    "seq_b": "MGKT",
                    "source_record_id": "record_000001",
                    "chain_a": "OLD_A",
                    "chain_b": "OLD_B",
                }
                if failure == "protein_id":
                    record["unip_id_b"] = "MISSING_PROTEIN"
                else:
                    record["seq_b"] = "MGKV"

                original = pd.DataFrame([record])
                result = assign_complex_chain_pairs(original, chains)

                self.assertEqual(len(result), 1)
                row = result.iloc[0]
                self.assertEqual(
                    row["af_match_status"], "no_matching_chain_pair"
                )
                self.assertEqual(
                    (row["chain_a"], row["chain_b"]), ("-", "-")
                )

                for column in original.columns:
                    if column not in ("chain_a", "chain_b"):
                        self.assertEqual(row[column], record[column])

                self.assertEqual(original.iloc[0]["chain_a"], "OLD_A")
                self.assertEqual(original.iloc[0]["chain_b"], "OLD_B")
    def test_retrieves_complex_and_assigns_record_chains(self):
        model_id = "AF-0000000208747029"
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        metadata_by_chain = {
            record["chainId"]: record for record in records
        }
        cif_content = (
            FIXTURE_DIR / f"{model_id}.cif"
        ).read_bytes()

        data = pd.DataFrame([{
            "unip_id_a": "A0A0P0Y832",
            "unip_id_b": "P0C2Z6",
            "seq_a": metadata_by_chain["A"]["sequence"],
            "seq_b": metadata_by_chain["B"]["sequence"],
            "source_record_id": "record_000001",
        }])

        metadata_response = Mock()
        metadata_response.json.return_value = records
        structure_response = Mock()
        structure_response.content = cif_content

        with TemporaryDirectory() as output_dir:
            with patch(
                "claudio.utils.af_complex.requests.get",
                side_effect=[metadata_response, structure_response],
            ):
                result = retrieve_af_complex(
                    data, model_id, output_dir
                )

            self.assertEqual(len(result), 1)
            self.assertIn("path", result.columns)

            row = result.iloc[0]
            self.assertEqual(
                (row["chain_a"], row["chain_b"]), ("A", "B")
            )
            self.assertEqual(row["af_model_id"], model_id)
            self.assertEqual(row["af_model_version"], 1)
            self.assertEqual(row["af_match_status"], "matched")
            self.assertEqual(
                row["source_record_id"], "record_000001"
            )

            structure_path = Path(row["path"])
            self.assertEqual(structure_path.parent, Path(output_dir))
            self.assertEqual(
                structure_path.read_bytes(), cif_content
            )
            self.assertIn("af_metadata_path", result.columns)
            metadata_path = Path(row["af_metadata_path"])

            self.assertEqual(metadata_path.parent, Path(output_dir))
            self.assertTrue(metadata_path.is_file())
            self.assertEqual(
                json.loads(metadata_path.read_text(encoding="utf-8")),
                records,
            )
    def test_rejects_unexpected_model_before_downloading_structure(self):
        model_id = "AF-0000000208747029"
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        for record in records:
            record["modelEntityId"] = "AF-unexpected-model"

        metadata_response = Mock()
        metadata_response.json.return_value = records

        structure_response = Mock()
        structure_response.content = (
            FIXTURE_DIR / f"{model_id}.cif"
        ).read_bytes()

        data = pd.DataFrame([{
            "unip_id_a": "A0A0P0Y832",
            "unip_id_b": "P0C2Z6",
            "seq_a": next(
                record["sequence"] for record in records
                if record["chainId"] == "A"
            ),
            "seq_b": next(
                record["sequence"] for record in records
                if record["chainId"] == "B"
            ),
            "source_record_id": "record_000001",
        }])

        with TemporaryDirectory() as output_dir:
            with patch(
                "claudio.utils.af_complex.requests.get",
                side_effect=[metadata_response, structure_response],
            ) as mock_get:
                with self.assertRaisesRegex(
                    ValueError, "Unexpected model identity"
                ):
                    retrieve_af_complex(data, model_id, output_dir)

                self.assertEqual(mock_get.call_count, 1)
                self.assertEqual(list(Path(output_dir).iterdir()), [])
    def test_retrieval_preserves_unmatched_records_without_structure_path(self):
        model_id = "AF-0000000208747029"
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        by_chain = {
            record["chainId"]: record for record in records
        }

        matched_record = {
            "unip_id_a": "A0A0P0Y832",
            "unip_id_b": "P0C2Z6",
            "seq_a": by_chain["A"]["sequence"],
            "seq_b": by_chain["B"]["sequence"],
            "source_record_id": "record_000001",
            "path": "old_structure.pdb",
        }
        unmatched_record = matched_record.copy()
        unmatched_record["unip_id_b"] = "MISSING_PROTEIN"
        unmatched_record["source_record_id"] = "record_000002"

        metadata_response = Mock()
        metadata_response.json.return_value = records
        structure_response = Mock()
        structure_response.content = (
            FIXTURE_DIR / f"{model_id}.cif"
        ).read_bytes()

        with TemporaryDirectory() as output_dir:
            with patch(
                "claudio.utils.af_complex.requests.get",
                side_effect=[metadata_response, structure_response],
            ):
                result = retrieve_af_complex(
                    pd.DataFrame([matched_record, unmatched_record]),
                    model_id,
                    output_dir,
                )

            self.assertEqual(len(result), 2)
            by_source = result.set_index("source_record_id")
            matched = by_source.loc["record_000001"]
            unmatched = by_source.loc["record_000002"]

            self.assertEqual(matched["af_match_status"], "matched")
            self.assertTrue(Path(matched["path"]).is_file())

            self.assertEqual(
                unmatched["af_match_status"], "no_matching_chain_pair"
            )
            self.assertEqual(unmatched["path"], "-")
            self.assertEqual(
                (unmatched["chain_a"], unmatched["chain_b"]),
                ("-", "-"),
            )

            # Metadata identifies the model that was attempted.
            self.assertEqual(unmatched["af_model_id"], model_id)
            self.assertTrue(
                Path(unmatched["af_metadata_path"]).is_file()
            )
    def test_cli_retrieves_specified_complex_without_blast_database(self):
        model_id = "AF-0000000208747029"
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        by_chain = {
            record["chainId"]: record for record in records
        }
        data = pd.DataFrame([{
            "unip_id_a": "A0A0P0Y832",
            "unip_id_b": "P0C2Z6",
            "seq_a": by_chain["A"]["sequence"],
            "seq_b": by_chain["B"]["sequence"],
            "source_record_id": "record_000001",
        }])

        metadata_response = Mock()
        metadata_response.json.return_value = records
        structure_response = Mock()
        structure_response.content = (
            FIXTURE_DIR / f"{model_id}.cif"
        ).read_bytes()

        with TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            input_path = folder / "input.sqcs"
            output_dir = folder / "output"
            data.to_csv(input_path)

            with patch(
                "claudio.utils.af_complex.requests.get",
                side_effect=[metadata_response, structure_response],
            ):
                execution = CliRunner().invoke(
                    structure_search_main,
                    [
                        "-i", str(input_path),
                        "-o", str(output_dir),
                        "--af-complex-model", model_id,
                        "-bldb", str(folder / "missing_blast_database") + "/",
                        "-v", "0",
                    ],
                )

            self.assertEqual(
                execution.exit_code,
                0,
                f"{execution.output}\n{execution.exception!r}",
            )

            output_path = output_dir / "input.sqcs_structdi.csv"
            self.assertTrue(output_path.is_file())
            result = pd.read_csv(output_path, index_col=0)

            self.assertEqual(len(result), 1)
            row = result.iloc[0]
            self.assertEqual(row["af_model_id"], model_id)
            self.assertEqual(row["af_match_status"], "matched")
            self.assertEqual(
                (row["chain_a"], row["chain_b"]), ("A", "B")
            )
            self.assertEqual(
                row["source_record_id"], "record_000001"
            )
            self.assertTrue(Path(row["path"]).is_file())
            self.assertTrue(Path(row["af_metadata_path"]).is_file())

    def test_preserves_input_indices_without_chain_expansion(self):
        chains = [
            {
                "chain_id": "A",
                "protein_id": "TEST_P1",
                "sequence": "MAAKT",
            },
            {
                "chain_id": "B",
                "protein_id": "TEST_P2",
                "sequence": "MGKT",
            },
        ]
        data = pd.DataFrame(
            [
                {
                    "unip_id_a": "TEST_P1",
                    "unip_id_b": "TEST_P2",
                    "seq_a": "MAAKT",
                    "seq_b": "MGKT",
                    "source_record_id": source_id,
                }
                for source_id in ("record_000008", "record_000013")
            ],
            index=[7, 12],
        )

        result = assign_complex_chain_pairs(data, chains)

        self.assertEqual(result.index.tolist(), [7, 12])
        self.assertEqual(
            result["source_record_id"].tolist(),
            ["record_000008", "record_000013"],
        )
        self.assertEqual(
            list(zip(result["chain_a"], result["chain_b"])),
            [("A", "B"), ("A", "B")],
        )
    def test_cli_without_model_keeps_legacy_search_route(self):
        data = pd.DataFrame([{
            "unip_id_a": "TEST_P1",
            "unip_id_b": "TEST_P2",
            "seq_a": "MAAKT",
            "seq_b": "MGKT",
            "source_record_id": "record_000001",
        }], index=[7])

        def search_result(data, *args):
            return data.assign(
                pdb_id="1ABC",
                chain_a="A",
                chain_b="B",
                all_results="1ABC_A|_B",
            )

        def download_result(data, *args):
            return data.assign(
                path="legacy_structure.pdb",
                pdb_method="X-RAY DIFFRACTION",
                pdb_resolution=2.0,
            )

        with TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            input_path = folder / "legacy.sqcs"
            output_dir = folder / "output"
            database_dir = folder / "database"
            database_dir.mkdir()

            # Only satisfies the entry-point file-existence check.
            # The external search itself is simulated below.
            (database_dir / "pdbaa.phr").touch()
            data.to_csv(input_path)

            with patch(
                "claudio.module02.src_structure_search.main.structure_search",
                side_effect=search_result,
            ) as search_mock, patch(
                "claudio.module02.src_structure_search.main.download_pdbs",
                side_effect=download_result,
            ) as download_mock, patch(
                "claudio.module02.src_structure_search.main.retrieve_af_complex",
            ) as af_mock:
                execution = CliRunner().invoke(
                    structure_search_main,
                    [
                        "-i", str(input_path),
                        "-o", str(output_dir),
                        "-bldb", str(database_dir) + "/",
                        "-v", "0",
                    ],
                )

            self.assertEqual(
                execution.exit_code,
                0,
                f"{execution.output}\n{execution.exception!r}",
            )
            search_mock.assert_called_once()
            download_mock.assert_called_once()
            af_mock.assert_not_called()

            result = pd.read_csv(
                output_dir / "legacy.sqcs_structdi.csv",
                index_col=0,
            )
            self.assertEqual(result.index.tolist(), [7])
            self.assertEqual(result.iloc[0]["pdb_id"], "1ABC")
            self.assertEqual(
                result.iloc[0]["source_record_id"],
                "record_000001",
            )
if __name__ == "__main__":
    unittest.main()
