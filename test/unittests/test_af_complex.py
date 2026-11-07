import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
import gzip
from claudio.utils.af_complex import (
    read_complex_chains,
    fetch_complex_metadata,
    download_complex_cif,
)
from unittest.mock import Mock, patch

FIXTURE_DIR = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "af_complex"
)


class TestReadComplexChains(unittest.TestCase):

    def test_preserves_both_chains_and_their_protein_identities(self):
        structure_path = FIXTURE_DIR / "AF-0000000208747029.cif"

        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )

        chains = read_complex_chains(structure_path, records)

        self.assertEqual(len(chains), 2)

        by_id = {chain["chain_id"]: chain for chain in chains}
        self.assertEqual(set(by_id), {"A", "B"})

        self.assertEqual(by_id["A"]["protein_id"], "A0A0P0Y832")
        self.assertEqual(by_id["A"]["residue_count"], 346)

        self.assertEqual(by_id["B"]["protein_id"], "P0C2Z6")
        self.assertEqual(by_id["B"]["residue_count"], 507)

        for record in records:
            chain = by_id[record["chainId"]]
            self.assertEqual(chain["sequence"], record["sequence"])
    def test_rejects_sequence_mismatch(self):
        structure_path = FIXTURE_DIR / "AF-0000000208747029.cif"

        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )

        for record in records:
            if record["chainId"] == "A":
                record["sequence"] = "A" * len(record["sequence"])

        with self.assertRaises(ValueError):
            read_complex_chains(structure_path, records)
    def test_rejects_missing_chain_metadata(self):
        structure_path = FIXTURE_DIR / "AF-0000000208747029.cif"

        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )

        # Keep only chain A's metadata, leaving chain B without matching metadata.
        records = [
            record for record in records
            if record["chainId"] == "A"
        ]

        with self.assertRaisesRegex(ValueError, r"chain B"):
            read_complex_chains(structure_path, records)

class TestFetchComplexMetadata(unittest.TestCase):

    def test_fetches_metadata_for_both_chains(self):
        expected_records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )

        response = Mock()
        response.json.return_value = expected_records

        with patch(
            "claudio.utils.af_complex.requests.get",
            return_value=response,
        ) as mock_get:
            records = fetch_complex_metadata("AF-0000000208747029")

        mock_get.assert_called_once_with(
            "https://alphafold.ebi.ac.uk/api/prediction/AF-0000000208747029",
            timeout=30,
        )
        response.raise_for_status.assert_called_once_with()

        self.assertEqual(records, expected_records)
        self.assertEqual(
            {record["chainId"] for record in records},
            {"A", "B"},
        )

    def test_rejects_empty_metadata(self):
        response = Mock()
        response.json.return_value = []

        with patch(
            "claudio.utils.af_complex.requests.get",
            return_value=response,
        ):
            with self.assertRaisesRegex(ValueError, "No metadata"):
                fetch_complex_metadata("AF-0000000208747029")

    def test_rejects_non_complex_metadata(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        for record in records:
            record["isComplex"] = False

        response = Mock()
        response.json.return_value = records

        with patch(
            "claudio.utils.af_complex.requests.get",
            return_value=response,
        ):
            with self.assertRaisesRegex(ValueError, "not a complex"):
                fetch_complex_metadata("AF-0000000208747029")

class TestDownloadComplexCif(unittest.TestCase):
    def test_downloads_shared_structure_once(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        expected_content = (
            FIXTURE_DIR / "AF-0000000208747029.cif"
        ).read_bytes()

        response = Mock()
        response.content = expected_content

        with TemporaryDirectory() as output_dir:
            with patch(
                "claudio.utils.af_complex.requests.get",
                return_value=response,
            ) as mock_get:
                structure_path = download_complex_cif(
                    records, output_dir
                )

            mock_get.assert_called_once_with(
                records[0]["cifUrl"],
                timeout=30,
            )
            response.raise_for_status.assert_called_once_with()

            structure_path = Path(structure_path)
            self.assertEqual(structure_path.parent, Path(output_dir))
            self.assertEqual(structure_path.suffix, ".cif")
            self.assertEqual(
                structure_path.read_bytes(),
                expected_content,
            )
    def test_decompresses_gzip_content_before_saving(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        expected_content = (
            FIXTURE_DIR / "AF-0000000208747029.cif"
        ).read_bytes()

        response = Mock()
        response.content = gzip.compress(expected_content)

        with TemporaryDirectory() as output_dir:
            with patch(
                "claudio.utils.af_complex.requests.get",
                return_value=response,
            ):
                structure_path = download_complex_cif(
                    records, output_dir
                )

            self.assertEqual(
                Path(structure_path).read_bytes(),
                expected_content,
                "The saved mmCIF should contain decompressed content",
            )
    def test_rejects_inconsistent_cif_urls(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        records[1]["cifUrl"] = "https://example.org/different-model.cif"

        response = Mock()
        response.content = b"data_test\n"

        with TemporaryDirectory() as output_dir:
            with patch(
                "claudio.utils.af_complex.requests.get",
                return_value=response,
            ) as mock_get:
                with self.assertRaisesRegex(
                    ValueError, "Inconsistent CIF URLs"
                ):
                    download_complex_cif(records, output_dir)

                mock_get.assert_not_called()
    def test_rejects_inconsistent_model_identity(self):
        cases = [
            ("modelEntityId", "AF-different-model"),
            ("latestVersion", 999),
        ]

        for field, different_value in cases:
            with self.subTest(field=field):
                records = json.loads(
                    (FIXTURE_DIR / "metadata.json").read_text(
                        encoding="utf-8"
                    )
                )
                records[1][field] = different_value

                with TemporaryDirectory() as output_dir:
                    response = Mock()
                    response.content = b"data_test\n"

                    with patch(
                        "claudio.utils.af_complex.requests.get",
                        return_value=response,
                    ) as mock_get:
                        with self.assertRaisesRegex(
                            ValueError,
                            "Inconsistent model identity",
                        ):
                            download_complex_cif(records, output_dir)

                        mock_get.assert_not_called()
if __name__ == "__main__":
    unittest.main()
