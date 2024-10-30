load blastp_afO31778.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO31778
color 3, chain A
show cartoon, chain A
dist intra_1434_valid , resid 290 and blastp_afO31778 and chain A and name cb, resid 316 and blastp_afO31778 and chain A and name cb
dist intra_1721_valid , resid 205 and blastp_afO31778 and chain A and name cb, resid 456 and blastp_afO31778 and chain A and name cb
dist intra_2091_valid , resid 483 and blastp_afO31778 and chain A and name cb, resid 258 and blastp_afO31778 and chain A and name cb
dist intra_642_unknown , resid 17 and blastp_afO31778 and chain A and name cb, resid 21 and blastp_afO31778 and chain A and name cb
dist intra_5797_unknown , resid 21 and blastp_afO31778 and chain A and name cb, resid 5 and blastp_afO31778 and chain A and name cb
dist intra_5924_unknown , resid 290 and blastp_afO31778 and chain A and name cb, resid 310 and blastp_afO31778 and chain A and name cb
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
save blastp_afO31778.pse
png blastp_afO31778.png
