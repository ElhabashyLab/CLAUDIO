load blastp_7OJ2.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_7OJ2
color 3, chain A
show cartoon, chain A
dist intra_41_unknown , resid 399 and blastp_7OJ2 and chain A and name cb, resid 74 and blastp_7OJ2 and chain A and name cb
dist intra_106_unknown , resid 117 and blastp_7OJ2 and chain A and name cb, resid 87 and blastp_7OJ2 and chain A and name cb
dist intra_1959_unknown , resid 399 and blastp_7OJ2 and chain A and name cb, resid 87 and blastp_7OJ2 and chain A and name cb
dist intra_2469_unknown , resid 412 and blastp_7OJ2 and chain A and name cb, resid 74 and blastp_7OJ2 and chain A and name cb
dist intra_3174_unknown , resid 411 and blastp_7OJ2 and chain A and name cb, resid 74 and blastp_7OJ2 and chain A and name cb
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
save blastp_7OJ2.pse
png blastp_7OJ2.png
