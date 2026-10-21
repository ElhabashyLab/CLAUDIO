"""Tests for plotting M3 data without evaluated results."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from claudio.module03.src.algorithm.create_histograms import (
    create_homo_signal_histograms,
)


class TestM3MissingResultsPlotting(unittest.TestCase):
    def test_skips_plots_when_all_results_are_missing(self):
        data = pd.DataFrame({
            "unip_id_a": ["TEST_PROTEIN"],
            "unip_id_b": ["TEST_PROTEIN"],
            "homo_adjacency": [float("nan")],
            "homo_int_overl": [float("nan")],
            "homo_pep_overl": pd.Series([pd.NA], dtype="boolean"),
        })

        try:
            with TemporaryDirectory() as output_dir:
                create_homo_signal_histograms(
                    data, "all_missing", output_dir + "/"
                )
                self.assertEqual(
                    list(Path(output_dir).glob("*.png")),
                    [],
                    "No evaluated results means no result plots",
                )
        finally:
            plt.close("all")
    def test_pie_counts_only_evaluated_results(self):
        from matplotlib.patches import Wedge

        data = pd.DataFrame({
            "unip_id_a": ["TEST_PROTEIN"] * 3,
            "unip_id_b": ["TEST_PROTEIN"] * 3,
            "homo_adjacency": [0.8, 0.5, float("nan")],
            "homo_int_overl": [1.0, 0.0, float("nan")],
            "homo_pep_overl": pd.Series(
                [True, False, pd.NA], dtype="boolean"
            ),
        })

        plt.close("all")
        try:
            with TemporaryDirectory() as output_dir:
                create_homo_signal_histograms(
                    data, "mixed", output_dir + "/"
                )

                self.assertTrue(
                    (Path(output_dir) / "mixed_pep_ovl_pie.png").is_file()
                )

                pie_axes = [
                    axis
                    for number in plt.get_fignums()
                    for axis in plt.figure(number).axes
                    if axis.get_title()
                    == "Proportion of Xlinks with OPSs in intra-links"
                ]
                self.assertEqual(len(pie_axes), 1)

                wedges = [
                    patch for patch in pie_axes[0].patches
                    if isinstance(patch, Wedge)
                ]
                self.assertEqual(len(wedges), 2)
                for wedge in wedges:
                    self.assertAlmostEqual(
                        wedge.theta2 - wedge.theta1,
                        180.0,
                        places=4,
                    )

                labels = [
                    text.get_text() for text in pie_axes[0].texts
                ]
                self.assertEqual(labels.count("50.0%\n(n=1)"), 2)
        finally:
            plt.close("all")

if __name__ == "__main__":
    unittest.main()
