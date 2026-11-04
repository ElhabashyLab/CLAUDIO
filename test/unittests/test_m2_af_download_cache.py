"""Do not let failed AlphaFold downloads poison the cache."""
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np
from Bio.PDB import PDBIO
from Bio.PDB.Atom import Atom
from Bio.PDB.Chain import Chain
from Bio.PDB.Model import Model
from Bio.PDB.Residue import Residue

from claudio.module02.src_distance_reevaluation.algorithm import search_pdb_pos


class TestM2AFDownloadCache(unittest.TestCase):

    def test_timeout_does_not_poison_a_later_download(self):
        model = Model(0)
        chain = Chain("A")
        residue = Residue((" ", 1, " "), "LYS", " ")
        residue.add(
            Atom(
                "CB", np.array([5.0, 0.0, 0.0]), 95.0, 1.0,
                " ", " CB ", 1, element="C",
            )
        )
        chain.add(residue)
        model.add(chain)
        stream = io.StringIO()
        writer = PDBIO()
        writer.set_structure(model)
        writer.save(stream)
        pdb_text = stream.getvalue()

        with tempfile.TemporaryDirectory() as folder:
            source = str(Path(folder) / "blastp_1ABC.pdb")
            cache = Path(folder) / "blastp_afP12345.pdb"
            with patch.object(
                search_pdb_pos, "pdb_cache", {}
            ), patch.object(search_pdb_pos.time, "sleep"):
                with patch.object(
                    search_pdb_pos.r, "get",
                    side_effect=search_pdb_pos.r.exceptions.Timeout("timeout"),
                ):
                    failed_chain, failed_path = (
                        search_pdb_pos.replacement_alphafold_download(
                            "P12345", source, 0
                        )
                    )

                self.assertIsNone(failed_chain)
                self.assertEqual(failed_path, "")
                self.assertFalse(
                    cache.exists(),
                    "A failed download must not leave a final cache file",
                )

                response = Mock(
                    status_code=200, text=pdb_text,
                    content=pdb_text.encode("utf-8"),
                )
                with patch.object(
                    search_pdb_pos.r, "get", return_value=response
                ):
                    downloaded_chain, downloaded_path = (
                        search_pdb_pos.replacement_alphafold_download(
                            "P12345", source, 0
                        )
                    )

                self.assertIsNotNone(downloaded_chain)
                self.assertEqual(downloaded_path, str(cache))
                self.assertGreater(cache.stat().st_size, 0)
                np.testing.assert_allclose(
                    downloaded_chain[1]["CB"].coord, [5.0, 0.0, 0.0]
                )

    def test_replaces_an_existing_invalid_cache(self):
        model = Model(0)
        chain = Chain("A")
        residue = Residue((" ", 1, " "), "LYS", " ")
        residue.add(
            Atom(
                "CB", np.array([5.0, 0.0, 0.0]), 95.0, 1.0,
                " ", " CB ", 1, element="C",
            )
        )
        chain.add(residue)
        model.add(chain)
        stream = io.StringIO()
        writer = PDBIO()
        writer.set_structure(model)
        writer.save(stream)
        pdb_text = stream.getvalue()

        for old_content in ("", "not a PDB structure\n"):
            for stale_memory in (False, True):
                with self.subTest(
                    old_content=old_content, stale_memory=stale_memory
                ), tempfile.TemporaryDirectory() as folder:
                    source = str(Path(folder) / "blastp_1ABC.pdb")
                    cache = Path(folder) / "blastp_afP12345.pdb"
                    cache.write_text(old_content, encoding="utf-8")
                    memory = {str(cache): []} if stale_memory else {}
                    response = Mock(
                        status_code=200, text=pdb_text,
                        content=pdb_text.encode("utf-8"),
                    )

                    with patch.object(
                        search_pdb_pos, "pdb_cache", memory
                    ), patch.object(
                        search_pdb_pos.r, "get", return_value=response
                    ):
                        actual_chain, actual_path = (
                            search_pdb_pos.replacement_alphafold_download(
                                "P12345", source, 0
                            )
                        )

                    self.assertIsNotNone(
                        actual_chain,
                        "An invalid cache must allow a fresh download",
                    )
                    self.assertEqual(actual_path, str(cache))
                    self.assertEqual(
                        cache.read_text(encoding="utf-8"), pdb_text
                    )
                    np.testing.assert_allclose(
                        actual_chain[1]["CB"].coord, [5.0, 0.0, 0.0]
                    )

    def test_invalid_download_leaves_no_cache_or_temporary_file(self):
        for content in ("", "not a PDB structure\n"):
            with self.subTest(content=content):
                with tempfile.TemporaryDirectory() as folder:
                    root = Path(folder)
                    source = str(root / "blastp_1ABC.pdb")
                    cache = root / "blastp_afP12345.pdb"
                    memory = {}
                    response = Mock(
                        status_code=200, text=content,
                        content=content.encode("utf-8"),
                    )
                    with patch.object(
                        search_pdb_pos, "pdb_cache", memory
                    ), patch.object(
                        search_pdb_pos.r, "get", return_value=response
                    ):
                        actual_chain, actual_path = (
                            search_pdb_pos.replacement_alphafold_download(
                                "P12345", source, 0
                            )
                        )

                    self.assertIsNone(actual_chain)
                    self.assertEqual(actual_path, "")
                    self.assertFalse(cache.exists())
                    self.assertNotIn(str(cache), memory)
                    self.assertEqual(
                        list(root.iterdir()), [],
                        "Invalid downloads must not leave temporary files",
                    )

if __name__ == "__main__":
    unittest.main()
