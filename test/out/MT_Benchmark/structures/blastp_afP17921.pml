load blastp_afP17921.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP17921
color 3, chain A
show cartoon, chain A
dist intra_905_valid , resid 56 and blastp_afP17921 and chain A and name cb, resid 6 and blastp_afP17921 and chain A and name cb
dist intra_1587_valid , resid 321 and blastp_afP17921 and chain A and name cb, resid 236 and blastp_afP17921 and chain A and name cb
dist intra_3841_valid , resid 321 and blastp_afP17921 and chain A and name cb, resid 237 and blastp_afP17921 and chain A and name cb
dist intra_4484_valid , resid 48 and blastp_afP17921 and chain A and name cb, resid 1 and blastp_afP17921 and chain A and name cb
dist intra_1155_unknown , resid 236 and blastp_afP17921 and chain A and name cb, resid 317 and blastp_afP17921 and chain A and name cb
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
save blastp_afP17921.pse
png blastp_afP17921.png
