load blastp_afP96614.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP96614
color 3, chain A
show cartoon, chain A
dist intra_175_valid , resid 101 and blastp_afP96614 and chain A and name cb, resid 120 and blastp_afP96614 and chain A and name cb
dist intra_487_valid , resid 361 and blastp_afP96614 and chain A and name cb, resid 205 and blastp_afP96614 and chain A and name cb
dist intra_942_valid , resid 227 and blastp_afP96614 and chain A and name cb, resid 425 and blastp_afP96614 and chain A and name cb
dist intra_721_unknown , resid 361 and blastp_afP96614 and chain A and name cb, resid 197 and blastp_afP96614 and chain A and name cb
dist intra_1395_unknown , resid 443 and blastp_afP96614 and chain A and name cb, resid 279 and blastp_afP96614 and chain A and name cb
dist intra_4909_unknown , resid 205 and blastp_afP96614 and chain A and name cb, resid 355 and blastp_afP96614 and chain A and name cb
dist intra_5262_unknown , resid 476 and blastp_afP96614 and chain A and name cb, resid 443 and blastp_afP96614 and chain A and name cb
dist intra_5282_unknown , resid 476 and blastp_afP96614 and chain A and name cb, resid 279 and blastp_afP96614 and chain A and name cb
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
save blastp_afP96614.pse
png blastp_afP96614.png