"""Tests for reading metadata after an RCSB mmCIF fallback."""

import unittest
from unittest.mock import Mock, call, patch

from claudio.module02.src_structure_search.algorithm import pdb_download


class TestM2MMCIFMetadata(unittest.TestCase):
    def test_accepts_mmcif_metadata_after_pdb_download_fallback(self):
        cif_text = (
            "data_1ABC\n"
            "#\n"
            "_exptl.method 'X-RAY DIFFRACTION'\n"
            "_refine.ls_d_res_high 2.5\n"
            "#\n"
        )

        pdb_url = "https://files.rcsb.org/download/1ABC.pdb"
        cif_url = "https://files.rcsb.org/download/1ABC.cif"

        responses = [
            Mock(text="<!doctype html><html>Not found</html>"),
            Mock(text=cif_text),
        ]

        with patch.object(
            pdb_download.r, "get", side_effect=responses
        ) as mock_get:
            downloaded = pdb_download.download_pdb_from_db(
                pdb_url, 0, 5
            )

        self.assertEqual(
            mock_get.call_args_list,
            [
                call(pdb_url, timeout=60),
                call(cif_url, timeout=60),
            ],
        )
        self.assertEqual(downloaded, cif_text)

        result = pdb_download.accept_resolution_method_download(
            downloaded, "1ABC", 4.0
        )

        self.assertEqual(
            result,
            (True, "X-RAY DIFFRACTION", 2.5),
            "A qualifying mmCIF structure must not be rejected "
            "because its metadata uses a different format",
        )

    def test_applies_method_specific_resolution_and_inclusive_cutoff(self):
        for method, key, other_key in [
            ("X-RAY DIFFRACTION", "_refine.ls_d_res_high",
             "_em_3d_reconstruction.resolution"),
            ("ELECTRON MICROSCOPY", "_em_3d_reconstruction.resolution",
             "_refine.ls_d_res_high"),
        ]:
            for value, accepted in [(2.5, True), (4.0, True), (4.1, False)]:
                with self.subTest(method=method, resolution=value):
                    # The unrelated field must not override this method's value.
                    other_value = 9.0 if accepted else 1.0
                    text = (
                        "\n# Leading comment\ndata_1ABC\n"
                        f"_exptl.method '{method}'\n"
                        f"{key} {value}\n{other_key} {other_value}\n"
                    )
                    self.assertEqual(
                        pdb_download.accept_resolution_method_download(
                            text, "1ABC", 4.0
                        ),
                        (accepted, method, value),
                    )

    def test_rejects_missing_or_invalid_required_resolution(self):
        for method, key in [
            ("X-RAY DIFFRACTION", "_refine.ls_d_res_high"),
            ("ELECTRON MICROSCOPY", "_em_3d_reconstruction.resolution"),
        ]:
            for value in [None, "?", ".", "unknown", "0", "-1",
                          "nan", "inf", "-inf"]:
                with self.subTest(method=method, resolution=value):
                    text = f"data_1ABC\n_exptl.method '{method}'\n"
                    if value is not None:
                        text += f"{key} {value}\n"
                    self.assertEqual(
                        pdb_download.accept_resolution_method_download(
                            text, "1ABC", 4.0
                        ),
                        (False, method, "-"),
                    )

    def test_accepts_nmr_without_resolution(self):
        for method in ["SOLUTION NMR", "SOLID-STATE NMR"]:
            with self.subTest(method=method):
                text = f"data_1ABC\n_exptl.method '{method}'\n"
                self.assertEqual(
                    pdb_download.accept_resolution_method_download(
                        text, "1ABC", 4.0
                    ),
                    (True, method, "NOT APPLICABLE"),
                )

    def test_handles_missing_unsupported_and_multiple_methods(self):
        cases = [
            ("", (False, "-", "-")),
            ("_exptl.method 'SOLUTION SCATTERING'\n",
             (False, "SOLUTION SCATTERING", "-")),
            ("loop_\n_exptl.method\n'X-RAY DIFFRACTION'\n'SOLUTION NMR'\n#\n",
             (False, "X-RAY DIFFRACTION; SOLUTION NMR", "-")),
            ("loop_\n_exptl.method\n'X-RAY DIFFRACTION'\n'X-RAY DIFFRACTION'\n#\n",
             (True, "X-RAY DIFFRACTION", 2.5)),
        ]
        for methods, expected in cases:
            with self.subTest(methods=methods):
                text = "data_1ABC\n" + methods + "_refine.ls_d_res_high 2.5\n"
                self.assertEqual(
                    pdb_download.accept_resolution_method_download(
                        text, "1ABC", 4.0
                    ),
                    expected,
                )

    def test_requires_all_reported_resolutions_to_satisfy_cutoff(self):
        for method, key in [
            ("X-RAY DIFFRACTION", "_refine.ls_d_res_high"),
            ("ELECTRON MICROSCOPY", "_em_3d_reconstruction.resolution"),
        ]:
            for values, expected in [
                (["2.5", "4.0"], (True, method, 4.0)),
                (["2.5", "4.1"], (False, method, 4.1)),
                (["4.1", "2.5"], (False, method, 4.1)),
                (["2.5", "?"], (False, method, "-")),
            ]:
                with self.subTest(method=method, values=values):
                    text = (
                        f"data_1ABC\n_exptl.method '{method}'\n"
                        f"loop_\n{key}\n" + "\n".join(values) + "\n#\n"
                    )
                    self.assertEqual(
                        pdb_download.accept_resolution_method_download(
                            text, "1ABC", 4.0
                        ),
                        expected,
                    )

    def test_preserves_pdb_metadata_acceptance(self):
        for method in ["X-RAY DIFFRACTION", "ELECTRON MICROSCOPY"]:
            for value, accepted in [(2.5, True), (4.0, True), (4.1, False)]:
                with self.subTest(method=method, resolution=value):
                    text = (
                        f"HEADER    TEST STRUCTURE\nEXPDTA    {method}\n"
                        f"REMARK   2 RESOLUTION.    {value:.2f} ANGSTROMS.\n"
                        "END\n"
                    )
                    self.assertEqual(
                        pdb_download.accept_resolution_method_download(
                            text, "1ABC", 4.0
                        ),
                        (accepted, method, value),
                    )
        for method in ["SOLUTION NMR", "SOLID-STATE NMR"]:
            with self.subTest(method=method):
                text = f"HEADER    TEST STRUCTURE\nEXPDTA    {method}\nEND\n"
                self.assertEqual(
                    pdb_download.accept_resolution_method_download(
                        text, "1ABC", 4.0
                    ),
                    (True, method, "NOT APPLICABLE"),
                )


if __name__ == "__main__":
    unittest.main()
