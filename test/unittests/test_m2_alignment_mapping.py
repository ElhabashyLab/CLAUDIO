"""Map UniProt sequence positions through alignments without crossing gaps."""
import unittest

from claudio.module02.src_distance_reevaluation.algorithm.search_pdb_pos import (
    realign_unip_pos_in_pdb_seq,
)


class TestM2AlignmentMapping(unittest.TestCase):
    pdb_seq = "ACDEFGHILMRNPQSTVWYACDEFGHILM"
    unip_seq = "ACDEFGHILMKRNPQSTVWYACDEFGHILM"

    def test_does_not_map_a_residue_missing_from_structure(self):
        position = realign_unip_pos_in_pdb_seq(
            self.pdb_seq, self.unip_seq, 11, 0
        )
        self.assertIsNone(
            position,
            "A gap must not map to the preceding structure residue",
        )

    def test_maps_the_last_residue_of_identical_sequences(self):
        position = realign_unip_pos_in_pdb_seq("AKK", "AKK", 3, 0)
        self.assertEqual(position, 3, "The last aligned residue is valid")

    def test_preserves_mapping_on_both_sides_of_a_gap(self):
        for unip_pos, expected in ((10, 10), (12, 11)):
            with self.subTest(unip_pos=unip_pos):
                position = realign_unip_pos_in_pdb_seq(
                    self.pdb_seq, self.unip_seq, unip_pos, 0
                )
                self.assertEqual(position, expected)


if __name__ == "__main__":
    unittest.main()
