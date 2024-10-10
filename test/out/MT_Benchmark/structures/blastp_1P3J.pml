load blastp_1P3J.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_1P3J
color 3, chain A
show cartoon, chain A
dist intra_141_valid , resid 170 and blastp_1P3J and chain A and name cb, resid 177 and blastp_1P3J and chain A and name cb
dist intra_154_valid , resid 74 and blastp_1P3J and chain A and name cb, resid 40 and blastp_1P3J and chain A and name cb
dist intra_1109_valid , resid 170 and blastp_1P3J and chain A and name cb, resid 176 and blastp_1P3J and chain A and name cb
dist intra_2511_valid , resid 74 and blastp_1P3J and chain A and name cb, resid 69 and blastp_1P3J and chain A and name cb
dist intra_2747_valid , resid 55 and blastp_1P3J and chain A and name cb, resid 177 and blastp_1P3J and chain A and name cb
dist intra_3516_valid , resid 74 and blastp_1P3J and chain A and name cb, resid 39 and blastp_1P3J and chain A and name cb
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
save blastp_1P3J.pse
png blastp_1P3J.png
