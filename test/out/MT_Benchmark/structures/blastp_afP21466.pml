load blastp_afP21466.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP21466
color 3, chain A
show cartoon, chain A
dist intra_302_valid , resid 134 and blastp_afP21466 and chain A and name cb, resid 74 and blastp_afP21466 and chain A and name cb
dist intra_1396_valid , resid 77 and blastp_afP21466 and chain A and name cb, resid 134 and blastp_afP21466 and chain A and name cb
dist intra_1470_valid , resid 28 and blastp_afP21466 and chain A and name cb, resid 43 and blastp_afP21466 and chain A and name cb
dist intra_1787_valid , resid 28 and blastp_afP21466 and chain A and name cb, resid 10 and blastp_afP21466 and chain A and name cb
dist intra_2165_valid , resid 24 and blastp_afP21466 and chain A and name cb, resid 43 and blastp_afP21466 and chain A and name cb
dist intra_4490_valid , resid 10 and blastp_afP21466 and chain A and name cb, resid 43 and blastp_afP21466 and chain A and name cb
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
save blastp_afP21466.pse
png blastp_afP21466.png
