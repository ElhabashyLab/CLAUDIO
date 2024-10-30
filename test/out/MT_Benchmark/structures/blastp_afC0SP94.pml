load blastp_afC0SP94.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afC0SP94
color 3, chain A
show cartoon, chain A
dist intra_646_valid , resid 169 and blastp_afC0SP94 and chain A and name cb, resid 90 and blastp_afC0SP94 and chain A and name cb
dist intra_1355_valid , resid 280 and blastp_afC0SP94 and chain A and name cb, resid 270 and blastp_afC0SP94 and chain A and name cb
dist intra_1542_valid , resid 42 and blastp_afC0SP94 and chain A and name cb, resid 131 and blastp_afC0SP94 and chain A and name cb
dist intra_4334_valid , resid 162 and blastp_afC0SP94 and chain A and name cb, resid 50 and blastp_afC0SP94 and chain A and name cb
dist intra_6071_valid , resid 80 and blastp_afC0SP94 and chain A and name cb, resid 261 and blastp_afC0SP94 and chain A and name cb
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
save blastp_afC0SP94.pse
png blastp_afC0SP94.png
