load blastp_afO32106.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO32106
color 3, chain A
show cartoon, chain A
dist intra_1919_valid , resid 51 and blastp_afO32106 and chain A and name cb, resid 98 and blastp_afO32106 and chain A and name cb
dist intra_3036_out_range , resid 51 and blastp_afO32106 and chain A and name cb, resid 142 and blastp_afO32106 and chain A and name cb
dist intra_4577_unknown , resid 142 and blastp_afO32106 and chain A and name cb, resid 422 and blastp_afO32106 and chain A and name cb
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
save blastp_afO32106.pse
png blastp_afO32106.png
