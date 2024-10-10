load blastp_3OQM.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_3OQM
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain C
show surface, chain C and blastp_3OQM
color 5, chain C
show cartoon, chain C
dist intra_1487_valid , resid 31 and blastp_3OQM and chain A and name cb, resid 36 and blastp_3OQM and chain A and name cb
dist intra_1487_4_valid , resid 31 and blastp_3OQM and chain C and name cb, resid 36 and blastp_3OQM and chain C and name cb
dist intra_2873_valid , resid 31 and blastp_3OQM and chain A and name cb, resid 37 and blastp_3OQM and chain A and name cb
dist intra_2873_4_valid , resid 31 and blastp_3OQM and chain C and name cb, resid 37 and blastp_3OQM and chain C and name cb
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
save blastp_3OQM.pse
png blastp_3OQM.png
