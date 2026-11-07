"""Route AF complex mappings to distance calculation without losing records."""

import subprocess
import json
from tempfile import TemporaryDirectory
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
from Bio.PDB import PDBParser

from claudio.module02.src_distance_reevaluation.algorithm.af_complex_distances import (
    calculate_complex_site_dists,
)


FIXTURE_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "af_complex"


class TestAFComplexDistances(unittest.TestCase):
    def setUp(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        chains = {record["chainId"]: record for record in records}
        self.row = {
            "source_record_id": "record_000001",
            "candidate_id": "candidate_000001",
            "experiment": "condition_A",
            "af_match_status": "matched",
            "af_model_id": "AF-0000000208747029",
            "af_model_version": 1,
            "af_metadata_path": str(FIXTURE_DIR / "metadata.json"),
            "path": str(FIXTURE_DIR / "AF-0000000208747029.cif"),
            "unip_id_a": chains["A"]["uniprotAccession"],
            "unip_id_b": chains["B"]["uniprotAccession"],
            "seq_a": chains["A"]["sequence"],
            "seq_b": chains["B"]["sequence"],
            "chain_a": "A", "chain_b": "B",
            "original_pos_a": 67, "original_pos_b": 11,
            "pos_a": 67, "pos_b": 11,
            "position_status_a": "valid", "position_status_b": "valid",
        }

    def test_computes_mapped_pair_and_preserves_unresolved_records(self):
        unresolved = {
            **self.row,
            "source_record_id": "record_000002",
            "position_status_a": "ambiguous",
        }
        missing = {
            **self.row,
            "source_record_id": "record_000003",
            "af_match_status": "no_candidate_model",
            "path": "-", "af_metadata_path": "-",
            "chain_a": "-", "chain_b": "-",
        }
        data = pd.DataFrame(
            [self.row, unresolved, missing],
            index=pd.Index([7, "7_1", 12], name="candidate_index"),
        )
        original = data.copy(deep=True)
        expected = float(np.linalg.norm(
            np.array((20.938, 33.286, 12.461))
            - np.array((-41.383, 25.017, 10.236))
        ))

        def fake_distances(selected, *args):
            self.assertEqual(selected["source_record_id"].tolist(), ["record_000001"])
            self.assertEqual(selected.iloc[0]["pdb_pos_a"], 67)
            self.assertEqual(selected.iloc[0]["pdb_pos_b"], 11)
            result = selected.copy()
            result["eucl_dist_tplk"] = round(expected, 3)
            result["topo_dist_tplk"] = round(expected + 1.0, 3)
            return result

        with patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "af_complex_distances.calculate_site_dists",
            side_effect=fake_distances,
        ) as calculate, patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "search_pdb_pos.replacement_alphafold_download"
        ) as replace:
            result = calculate_complex_site_dists(
                data, "unused/", "K", 0.0, None, 0
            )

        pd.testing.assert_frame_equal(data, original)
        pd.testing.assert_frame_equal(result[original.columns], original)
        pd.testing.assert_index_equal(result.index, original.index)
        calculate.assert_called_once()
        replace.assert_not_called()
        self.assertEqual(result.iloc[0]["distance_status"], "computed")
        self.assertAlmostEqual(result.iloc[0]["eucl_dist_tplk"], expected, places=3)
        for position, reason in ((1, "unresolved_position"), (2, "no_candidate_model")):
            row = result.iloc[position]
            self.assertEqual(row["distance_status"], "not_evaluable")
            self.assertEqual(row["distance_reason"], reason)
            self.assertTrue(pd.isna(row["eucl_dist_tplk"]))
            self.assertTrue(pd.isna(row["topo_dist_tplk"]))

    def test_unresolved_same_site_does_not_receive_zero_distance(self):
        row = dict(self.row)
        for field in ("unip_id", "seq", "chain", "pos", "original_pos"):
            row[f"{field}_b"] = row[f"{field}_a"]
        row["position_status_a"] = "ambiguous"
        data = pd.DataFrame([row])
        with patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "af_complex_distances.calculate_site_dists"
        ) as calculate:
            result = calculate_complex_site_dists(
                data, "unused/", "K", 0.0, None, 0
            )
        calculate.assert_not_called()
        self.assertEqual(result.iloc[0]["distance_status"], "not_evaluable")
        self.assertTrue(pd.isna(result.iloc[0]["eucl_dist_tplk"]))
        self.assertTrue(pd.isna(result.iloc[0]["topo_dist_tplk"]))


    def test_low_plddt_keeps_mapping_but_skips_distance_calculation(self):
        data = pd.DataFrame([self.row])
        with patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "af_complex_distances.calculate_site_dists"
        ) as calculate:
            result = calculate_complex_site_dists(
                data, "unused/", "K", 70.0, None, 0
            )
        calculate.assert_not_called()
        row = result.iloc[0]
        self.assertEqual(row["mapping_status_a"], "mapped")
        self.assertEqual(row["mapping_status_b"], "mapped")
        self.assertAlmostEqual(row["pLDDT_b"], 56.86, places=2)
        self.assertEqual(row["distance_reason"], "low_plddt")
        self.assertTrue(pd.isna(row["eucl_dist_tplk"]))
        self.assertTrue(pd.isna(row["topo_dist_tplk"]))

    def test_missing_engine_results_replace_stale_distances(self):
        data = pd.DataFrame([{
            **self.row,
            "eucl_dist_tplk": 10.0, "topo_dist_tplk": 12.0,
            "distance_status": "computed", "distance_reason": "old result",
        }])

        def no_result(selected, *args):
            result = selected.copy()
            result["eucl_dist_tplk"] = float("nan")
            result["topo_dist_tplk"] = float("nan")
            return result

        with patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "af_complex_distances.calculate_site_dists",
            side_effect=no_result,
        ):
            result = calculate_complex_site_dists(
                data, "unused/", "K", 0.0, None, 0
            )
        row = result.iloc[0]
        self.assertEqual(row["distance_status"], "not_evaluable")
        self.assertEqual(row["distance_reason"], "distance_unavailable")
        self.assertTrue(pd.isna(row["eucl_dist_tplk"]))
        self.assertTrue(pd.isna(row["topo_dist_tplk"]))

    def test_lower_bounds_have_their_own_status_and_keep_raw_tokens(self):
        unresolved = {
            **self.row, "source_record_id": "record_000002",
            "position_status_a": "ambiguous",
        }
        data = pd.DataFrame([self.row, unresolved], index=[7, 12])

        def bounded(selected, *args):
            result = selected.copy()
            result["eucl_dist_tplk"] = 62.907
            result["topo_dist_tplk"] = float("nan")
            result["eucl_dist_lower_bound"] = float("nan")
            result["topo_dist_lower_bound"] = 75.957
            result["eucl_dist_raw"] = "62.907"
            result["topo_dist_raw"] = ">75.957"
            return result

        with patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "af_complex_distances.calculate_site_dists", side_effect=bounded,
        ):
            result = calculate_complex_site_dists(
                data, "unused/", "K", 0.0, None, 0,
            )
        row = result.loc[7]
        self.assertEqual(row["distance_status"], "lower_bound")
        self.assertEqual(row["distance_reason"], "topolink_lower_bound")
        self.assertEqual(row["topo_dist_lower_bound"], 75.957)
        self.assertEqual(row["topo_dist_raw"], ">75.957")
        self.assertTrue(pd.isna(row["topo_dist_tplk"]))
        self.assertEqual(result.loc[12, "distance_reason"], "unresolved_position")
        self.assertTrue(pd.isna(result.loc[12, "topo_dist_lower_bound"]))
        self.assertTrue(pd.isna(result.loc[12, "topo_dist_raw"]))

    def test_unresolved_records_do_not_keep_stale_bound_fields(self):
        data = pd.DataFrame([{
            **self.row, "position_status_a": "ambiguous",
            "topo_dist_lower_bound": 100.0, "topo_dist_raw": ">100",
        }])
        with patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "af_complex_distances.calculate_site_dists",
        ) as calculate:
            result = calculate_complex_site_dists(
                data, "unused/", "K", 0.0, None, 0,
            )
        calculate.assert_not_called()
        self.assertEqual(result.iloc[0]["distance_status"], "not_evaluable")
        self.assertTrue(pd.isna(result.iloc[0]["topo_dist_lower_bound"]))
        self.assertTrue(pd.isna(result.iloc[0]["topo_dist_raw"]))

    def test_rejects_invalid_cutoff_before_reading_structure(self):
        with patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "af_complex_distances.prepare_complex_distance_input"
        ) as prepare:
            for cutoff in (-1, 101, float("nan"), float("inf")):
                with self.subTest(cutoff=cutoff):
                    with self.assertRaisesRegex(ValueError, "pLDDT cutoff"):
                        calculate_complex_site_dists(
                            pd.DataFrame([self.row]), "unused/", "K",
                            cutoff, None, 0,
                        )
            prepare.assert_not_called()

    def test_empty_input_does_not_call_distance_engine(self):
        data = pd.DataFrame([self.row]).iloc[:0]
        with patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "af_complex_distances.calculate_site_dists"
        ) as calculate:
            result = calculate_complex_site_dists(
                data, "unused/", "K", 0.0, None, 0
            )
        calculate.assert_not_called()
        pd.testing.assert_frame_equal(result[data.columns], data)
        self.assertTrue(result.empty)
        for column in ("distance_status", "distance_reason",
                       "eucl_dist_tplk", "topo_dist_tplk"):
            self.assertIn(column, result.columns)

    def test_export_and_backfill_use_the_same_model_for_reversed_records(self):
        reverse = dict(self.row)
        reverse["source_record_id"] = "record_000002"
        for field in ("unip_id", "seq", "chain", "pos", "original_pos"):
            reverse[f"{field}_a"] = self.row[f"{field}_b"]
            reverse[f"{field}_b"] = self.row[f"{field}_a"]
        data = pd.DataFrame(
            [self.row, reverse],
            index=pd.Index([7, "7_1"], name="candidate_index"),
        )
        original = data.copy(deep=True)
        expected = float(np.linalg.norm(
            np.array((20.938, 33.286, 12.461))
            - np.array((-41.383, 25.017, 10.236))
        ))

        def run_topolink(command, **kwargs):
            input_path = Path(kwargs["cwd"]) / command[-1]
            lines = input_path.read_text().splitlines()
            structure_path = next(
                line.split(maxsplit=1)[1]
                for line in lines if line.startswith("structure ")
            )
            model = next(PDBParser(QUIET=True).get_structure(
                "export", (Path(kwargs["cwd"]) / structure_path)
            ).get_models())
            observed = [
                line.split() for line in lines
                if line.strip().startswith("observed ")
            ]
            self.assertEqual(len(observed), 1)
            link = observed[0]
            atom_a = model[link[2]][int(link[3])]["CB"]
            atom_b = model[link[5]][int(link[6])]["CB"]
            distance = float(np.linalg.norm(
                atom_a.get_coord() - atom_b.get_coord()
            ))
            self.assertGreater(distance, 50.0)
            self.assertAlmostEqual(distance, expected, places=3)
            return subprocess.CompletedProcess(
                command, 0,
                stdout=(
                    f"  LINK: {' '.join(link[1:4])} CB "
                    f"{' '.join(link[4:7])} CB "
                    f"{distance:.3f} {distance + 1.0:.3f} "
                    "YES 0.000 100.000 OK: FOUND\n"
                ),
                stderr="",
            )

        with TemporaryDirectory() as folder:
            with patch(
                "claudio.module02.src_distance_reevaluation.algorithm."
                "af_complex_distances.subprocess.run",
                side_effect=run_topolink,
            ) as topolink:
                result = calculate_complex_site_dists(
                    data, folder + "/", "K", 0.0, None, 0
                )
            topolink.assert_called_once()
            logs = list(Path(folder).glob("*/topo_complex.log"))
            self.assertEqual(len(logs), 1)
            self.assertIn(self.row["path"], logs[0].read_text())
            self.assertEqual(
                len(list(Path(folder).glob("*/struct/structure.pdb"))), 1
            )

        pd.testing.assert_frame_equal(data, original)
        pd.testing.assert_frame_equal(result[data.columns], data)
        self.assertEqual(result["distance_status"].tolist(), ["computed"] * 2)
        np.testing.assert_allclose(
            result["eucl_dist_tplk"], round(expected, 3), atol=0.001
        )
        np.testing.assert_allclose(
            result["topo_dist_tplk"], round(expected + 1.0, 3), atol=0.001
        )

if __name__ == "__main__":
    unittest.main()
