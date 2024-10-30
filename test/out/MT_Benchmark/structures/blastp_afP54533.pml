load blastp_afP54533.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP54533
color 3, chain A
show cartoon, chain A
dist intra_452_valid , resid 103 and blastp_afP54533 and chain A and name cb, resid 106 and blastp_afP54533 and chain A and name cb
dist intra_2630_valid , resid 386 and blastp_afP54533 and chain A and name cb, resid 226 and blastp_afP54533 and chain A and name cb
dist intra_3787_valid , resid 37 and blastp_afP54533 and chain A and name cb, resid 103 and blastp_afP54533 and chain A and name cb
dist intra_6002_unknown , resid 35 and blastp_afP54533 and chain A and name cb, resid 38 and blastp_afP54533 and chain A and name cb
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
save blastp_afP54533.pse
png blastp_afP54533.png
