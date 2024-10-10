load blastp_5XHU.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_5XHU
color 3, chain A
show cartoon, chain A
dist intra_308_valid , resid 53 and blastp_5XHU and chain A and name cb, resid 149 and blastp_5XHU and chain A and name cb
dist intra_1034_valid , resid 149 and blastp_5XHU and chain A and name cb, resid 41 and blastp_5XHU and chain A and name cb
dist intra_2012_valid , resid 41 and blastp_5XHU and chain A and name cb, resid 74 and blastp_5XHU and chain A and name cb
dist intra_2354_valid , resid 41 and blastp_5XHU and chain A and name cb, resid 67 and blastp_5XHU and chain A and name cb
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
save blastp_5XHU.pse
png blastp_5XHU.png
