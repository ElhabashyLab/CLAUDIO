load blastp_afO34526.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO34526
color 3, chain A
show cartoon, chain A
dist intra_412_valid , resid 728 and blastp_afO34526 and chain A and name cb, resid 608 and blastp_afO34526 and chain A and name cb
dist intra_742_valid , resid 754 and blastp_afO34526 and chain A and name cb, resid 779 and blastp_afO34526 and chain A and name cb
dist intra_1310_valid , resid 724 and blastp_afO34526 and chain A and name cb, resid 742 and blastp_afO34526 and chain A and name cb
dist intra_1455_valid , resid 766 and blastp_afO34526 and chain A and name cb, resid 779 and blastp_afO34526 and chain A and name cb
dist intra_2323_valid , resid 783 and blastp_afO34526 and chain A and name cb, resid 754 and blastp_afO34526 and chain A and name cb
dist intra_3366_valid , resid 728 and blastp_afO34526 and chain A and name cb, resid 717 and blastp_afO34526 and chain A and name cb
dist intra_861_overlaps , resid 754 and blastp_afO34526 and chain A and name cb, resid 766 and blastp_afO34526 and chain A and name cb
dist intra_1228_unknown , resid 718 and blastp_afO34526 and chain A and name cb, resid 742 and blastp_afO34526 and chain A and name cb
dist intra_4832_unknown , resid 650 and blastp_afO34526 and chain A and name cb, resid 527 and blastp_afO34526 and chain A and name cb
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
save blastp_afO34526.pse
png blastp_afO34526.png
