load blastp_afP37474.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP37474
color 3, chain A
show cartoon, chain A
dist intra_1584_valid , resid 260 and blastp_afP37474 and chain A and name cb, resid 252 and blastp_afP37474 and chain A and name cb
dist intra_4565_valid , resid 579 and blastp_afP37474 and chain A and name cb, resid 564 and blastp_afP37474 and chain A and name cb
dist intra_853_unknown , resid 259 and blastp_afP37474 and chain A and name cb, resid 252 and blastp_afP37474 and chain A and name cb
dist intra_2981_unknown , resid 1099 and blastp_afP37474 and chain A and name cb, resid 1148 and blastp_afP37474 and chain A and name cb
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
save blastp_afP37474.pse
png blastp_afP37474.png
