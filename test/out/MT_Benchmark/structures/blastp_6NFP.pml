load blastp_6NFP.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_6NFP
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain D
show surface, chain D and blastp_6NFP
color 5, chain D
show cartoon, chain D
dist intra_381_valid , resid 56 and blastp_6NFP and chain A and name cb, resid 79 and blastp_6NFP and chain A and name cb
dist intra_6022_valid , resid 56 and blastp_6NFP and chain A and name cb, resid 75 and blastp_6NFP and chain A and name cb
dist inter_381_4_valid , resid 56 and blastp_6NFP and chain A and name cb, resid 79 and blastp_6NFP and chain D and name cb
dist inter_6022_4_valid , resid 56 and blastp_6NFP and chain A and name cb, resid 75 and blastp_6NFP and chain D and name cb
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
save blastp_6NFP.pse
png blastp_6NFP.png
