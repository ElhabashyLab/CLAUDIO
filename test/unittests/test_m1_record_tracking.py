"""Tests for tracing M1 records back to their input."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from claudio.module01.src.algorithm.check_data import double_check_data
from claudio.utils.utils import build_xl_dataset, clean_dataset
import pandas as pd

from claudio.module01.src.io.write_out import write_outputs
from claudio.module01.src.io.read_in import read_inputfile


class TestM1RecordTracking(unittest.TestCase):
    def test_assigns_distinct_source_ids_to_input_records(self):
        csv_text = (
            "peptide1,peptide2,position1,position2,"
            "k_pos1,k_pos2,entry1,entry2\n"
            "AK,KT,10,20,2,1,P00001,P00002\n"
            "AK,KT,10,20,2,1,P00001,P00002\n"
        )
        projections = {
            "peptide1": "pep_a",
            "peptide2": "pep_b",
            "position1": "pos_a",
            "position2": "pos_b",
            "k_pos1": "res_pos_a",
            "k_pos2": "res_pos_b",
            "entry1": "unip_id_a",
            "entry2": "unip_id_b",
        }

        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            input_path.write_text(csv_text, encoding="utf-8")
            data = read_inputfile(str(input_path), projections)

        self.assertIn("source_record_id", data.columns)
        self.assertEqual(
            data["source_record_id"].tolist(),
            ["record_000001", "record_000002"],
        )
    def test_preserves_positions_before_numeric_conversion(self):
        csv_text = (
            "peptide1,peptide2,position1,position2,"
            "k_pos1,k_pos2,entry1,entry2\n"
            "AK,KT,10.5,20,2,1,P00001,P00002\n"
        )
        projections = {
            "peptide1": "pep_a",
            "peptide2": "pep_b",
            "position1": "pos_a",
            "position2": "pos_b",
            "k_pos1": "res_pos_a",
            "k_pos2": "res_pos_b",
            "entry1": "unip_id_a",
            "entry2": "unip_id_b",
        }

        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            input_path.write_text(csv_text, encoding="utf-8")
            data = read_inputfile(str(input_path), projections)

        self.assertIn("original_pos_a", data.columns)
        self.assertIn("original_pos_b", data.columns)
        self.assertEqual(data.loc[0, "original_pos_a"], 10.5)
        self.assertEqual(data.loc[0, "original_pos_b"], 20)
    def test_rejects_existing_tracking_columns(self):
        projections = {
            "peptide1": "pep_a",
            "peptide2": "pep_b",
            "position1": "pos_a",
            "position2": "pos_b",
            "k_pos1": "res_pos_a",
            "k_pos2": "res_pos_b",
            "entry1": "unip_id_a",
            "entry2": "unip_id_b",
        }

        for column in (
            "source_record_id",
            "original_pos_a",
            "original_pos_b",
        ):
            with self.subTest(column=column):
                csv_text = (
                    "peptide1,peptide2,position1,position2,"
                    f"k_pos1,k_pos2,entry1,entry2,{column}\n"
                    "AK,KT,10,20,2,1,P00001,P00002,existing_value\n"
                )

                with TemporaryDirectory() as temp_dir:
                    input_path = Path(temp_dir) / "input.csv"
                    input_path.write_text(csv_text, encoding="utf-8")

                    with self.assertRaisesRegex(
                        ValueError, "Reserved tracking columns"
                    ):
                        read_inputfile(str(input_path), projections)
    def test_preserves_tracking_through_position_correction_and_cleanup(self):
        csv_text = (
            "peptide1,peptide2,position1,position2,"
            "k_pos1,k_pos2,entry1,entry2\n"
            "AKT,GKT,2,3,2,2,P00001,P00002\n"
        )
        projections = {
            "peptide1": "pep_a",
            "peptide2": "pep_b",
            "position1": "pos_a",
            "position2": "pos_b",
            "k_pos1": "res_pos_a",
            "k_pos2": "res_pos_b",
            "entry1": "unip_id_a",
            "entry2": "unip_id_b",
        }

        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            input_path.write_text(csv_text, encoding="utf-8")
            data = read_inputfile(str(input_path), projections)

            # Supply fixed sequences; this test does not query UniProt.
            data["seq_a"] = "MAAKT"
            data["seq_b"] = "MGKT"

            checked = double_check_data(
                data,
                "input",
                build_xl_dataset("K"),
                str(Path(temp_dir)) + "/",
                0,
            )
            cleaned = clean_dataset(checked)

        self.assertEqual(len(cleaned), 1)
        row = cleaned.iloc[0]

        self.assertEqual(row["pos_a"], 4)
        self.assertEqual(row["pos_b"], 3)
        self.assertEqual(row["original_pos_a"], 2)
        self.assertEqual(row["original_pos_b"], 3)
        self.assertEqual(row["source_record_id"], "record_000001")
    def test_preserves_tracking_when_expanding_candidate_positions(self):
        csv_text = (
            "peptide1,peptide2,position1,position2,"
            "k_pos1,k_pos2,entry1,entry2\n"
            "AKT,GKT,3,3,2,2,P00001,P00002\n"
        )
        projections = {
            "peptide1": "pep_a",
            "peptide2": "pep_b",
            "position1": "pos_a",
            "position2": "pos_b",
            "k_pos1": "res_pos_a",
            "k_pos2": "res_pos_b",
            "entry1": "unip_id_a",
            "entry2": "unip_id_b",
        }

        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            input_path.write_text(csv_text, encoding="utf-8")
            data = read_inputfile(str(input_path), projections)

            data["seq_a"] = "MAKTAKT"
            data["seq_b"] = "MGKT"

            checked = double_check_data(
                data,
                "input",
                build_xl_dataset("K"),
                str(Path(temp_dir)) + "/",
                0,
            )
            cleaned = clean_dataset(checked)

        self.assertEqual(len(cleaned), 2)
        self.assertEqual(set(cleaned["pos_a"]), {3, 6})
        self.assertEqual(set(cleaned["pos_b"]), {3})

        self.assertEqual(
            cleaned["source_record_id"].tolist(),
            ["record_000001", "record_000001"],
        )
        self.assertEqual(cleaned["original_pos_a"].tolist(), [3, 3])
        self.assertEqual(cleaned["original_pos_b"].tolist(), [3, 3])
    def test_preserves_tracking_in_written_sqcs(self):
        csv_text = (
            "peptide1,peptide2,position1,position2,"
            "k_pos1,k_pos2,entry1,entry2\n"
            "AKT,GKT,2,3,2,2,P00001,P00002\n"
        )
        projections = {
            "peptide1": "pep_a",
            "peptide2": "pep_b",
            "position1": "pos_a",
            "position2": "pos_b",
            "k_pos1": "res_pos_a",
            "k_pos2": "res_pos_b",
            "entry1": "unip_id_a",
            "entry2": "unip_id_b",
        }

        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            input_path.write_text(csv_text, encoding="utf-8")
            data = read_inputfile(str(input_path), projections)

            data["seq_a"] = "MAAKT"
            data["seq_b"] = "MGKT"
            output_dir = str(Path(temp_dir)) + "/"

            checked = double_check_data(
                data, "input", build_xl_dataset("K"), output_dir, 0
            )
            cleaned = clean_dataset(checked)

            # Protein-list generation is outside this test's scope.
            unique_proteins = pd.DataFrame({"protein_id": []})
            write_outputs(
                cleaned, unique_proteins, "input", output_dir, 0
            )

            saved = pd.read_csv(
                Path(temp_dir) / "input.sqcs",
                index_col=0,
            )

        self.assertEqual(len(saved), 1)
        row = saved.iloc[0]
        self.assertEqual(row["source_record_id"], "record_000001")
        self.assertEqual(row["original_pos_a"], 2)
        self.assertEqual(row["original_pos_b"], 3)
        self.assertEqual(row["pos_a"], 4)
        self.assertEqual(row["pos_b"], 3)
if __name__ == "__main__":
    unittest.main()
