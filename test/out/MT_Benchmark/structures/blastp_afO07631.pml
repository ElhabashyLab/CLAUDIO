load blastp_afO07631.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO07631
color 3, chain A
show cartoon, chain A
dist intra_1775_valid , resid 596 and blastp_afO07631 and chain A and name cb, resid 541 and blastp_afO07631 and chain A and name cb
dist intra_1893_valid , resid 117 and blastp_afO07631 and chain A and name cb, resid 392 and blastp_afO07631 and chain A and name cb
dist intra_2573_valid , resid 543 and blastp_afO07631 and chain A and name cb, resid 560 and blastp_afO07631 and chain A and name cb
dist intra_3747_valid , resid 543 and blastp_afO07631 and chain A and name cb, resid 596 and blastp_afO07631 and chain A and name cb
dist intra_3774_valid , resid 543 and blastp_afO07631 and chain A and name cb, resid 497 and blastp_afO07631 and chain A and name cb
dist intra_4395_valid , resid 596 and blastp_afO07631 and chain A and name cb, resid 604 and blastp_afO07631 and chain A and name cb
dist intra_4882_valid , resid 596 and blastp_afO07631 and chain A and name cb, resid 606 and blastp_afO07631 and chain A and name cb
dist intra_5836_valid , resid 560 and blastp_afO07631 and chain A and name cb, resid 542 and blastp_afO07631 and chain A and name cb
dist intra_202_unknown , resid 543 and blastp_afO07631 and chain A and name cb, resid 553 and blastp_afO07631 and chain A and name cb
dist intra_434_unknown , resid 553 and blastp_afO07631 and chain A and name cb, resid 542 and blastp_afO07631 and chain A and name cb
dist intra_442_unknown , resid 61 and blastp_afO07631 and chain A and name cb, resid 263 and blastp_afO07631 and chain A and name cb
dist intra_938_unknown , resid 497 and blastp_afO07631 and chain A and name cb, resid 553 and blastp_afO07631 and chain A and name cb
dist intra_1013_unknown , resid 553 and blastp_afO07631 and chain A and name cb, resid 541 and blastp_afO07631 and chain A and name cb
dist intra_4102_unknown , resid 543 and blastp_afO07631 and chain A and name cb, resid 486 and blastp_afO07631 and chain A and name cb
dist intra_5740_unknown , resid 543 and blastp_afO07631 and chain A and name cb, resid 487 and blastp_afO07631 and chain A and name cb
show dashes
set dash_gap, 0.1
color 2, intra*_valid
color 2, intra*_out_range
color 2, intra*_overlaps
color 2, intra*_same
color black, intra*_unknown
color 13, inter*_valid
color 13, inter*_out_range
color 13, inter*_overlaps
color 13, inter*_same
color black, inter*_unknown
set dash_gap, 1, *_out_range
set dash_gap, 1, *_overlaps
set dash_gap, 1, *_same
hide dashes, *_unknown
set dash_width, 9
center
save blastp_afO07631.pse
png blastp_afO07631.png
