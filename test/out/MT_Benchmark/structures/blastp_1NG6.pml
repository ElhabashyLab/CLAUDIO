load blastp_1NG6.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_1NG6
color 3, chain A
show cartoon, chain A
dist intra_284_valid , resid 116 and blastp_1NG6 and chain A and name cb, resid 141 and blastp_1NG6 and chain A and name cb
dist intra_417_valid , resid 30 and blastp_1NG6 and chain A and name cb, resid 12 and blastp_1NG6 and chain A and name cb
dist intra_986_valid , resid 133 and blastp_1NG6 and chain A and name cb, resid 62 and blastp_1NG6 and chain A and name cb
dist intra_1110_valid , resid 79 and blastp_1NG6 and chain A and name cb, resid 20 and blastp_1NG6 and chain A and name cb
dist intra_2477_valid , resid 141 and blastp_1NG6 and chain A and name cb, resid 62 and blastp_1NG6 and chain A and name cb
dist intra_1320_overlaps , resid 28 and blastp_1NG6 and chain A and name cb, resid 12 and blastp_1NG6 and chain A and name cb
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
save blastp_1NG6.pse
png blastp_1NG6.png
