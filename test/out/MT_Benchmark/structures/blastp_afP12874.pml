load blastp_afP12874.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP12874
color 3, chain A
show cartoon, chain A
dist intra_492_valid , resid 62 and blastp_afP12874 and chain A and name cb, resid 32 and blastp_afP12874 and chain A and name cb
dist intra_1383_valid , resid 62 and blastp_afP12874 and chain A and name cb, resid 8 and blastp_afP12874 and chain A and name cb
dist intra_1508_valid , resid 47 and blastp_afP12874 and chain A and name cb, resid 18 and blastp_afP12874 and chain A and name cb
dist intra_2044_valid , resid 18 and blastp_afP12874 and chain A and name cb, resid 56 and blastp_afP12874 and chain A and name cb
dist intra_4412_valid , resid 31 and blastp_afP12874 and chain A and name cb, resid 8 and blastp_afP12874 and chain A and name cb
dist intra_4635_valid , resid 45 and blastp_afP12874 and chain A and name cb, resid 18 and blastp_afP12874 and chain A and name cb
dist intra_5621_valid , resid 73 and blastp_afP12874 and chain A and name cb, resid 8 and blastp_afP12874 and chain A and name cb
dist intra_6109_unknown , resid 47 and blastp_afP12874 and chain A and name cb, resid 63 and blastp_afP12874 and chain A and name cb
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
save blastp_afP12874.pse
png blastp_afP12874.png
