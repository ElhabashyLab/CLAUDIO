load blastp_8H0S.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_8H0S
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain C
show surface, chain C and blastp_8H0S
color 5, chain C
show cartoon, chain C
hide everything, show cartoon, chain D
show surface, chain D and blastp_8H0S
color 7, chain D
show cartoon, chain D
hide everything, show cartoon, chain B
show surface, chain B and blastp_8H0S
color 8, chain B
show cartoon, chain B
dist intra_5893_valid , resid 189 and blastp_8H0S and chain A and name cb, resid 5 and blastp_8H0S and chain A and name cb
dist intra_5893_11_valid , resid 189 and blastp_8H0S and chain C and name cb, resid 5 and blastp_8H0S and chain C and name cb
dist inter_5893_4_valid , resid 189 and blastp_8H0S and chain A and name cb, resid 5 and blastp_8H0S and chain D and name cb
dist inter_5893_10_valid , resid 189 and blastp_8H0S and chain C and name cb, resid 5 and blastp_8H0S and chain B and name cb
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
save blastp_8H0S.pse
png blastp_8H0S.png
