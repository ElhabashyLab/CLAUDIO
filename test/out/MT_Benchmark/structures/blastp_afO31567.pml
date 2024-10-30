load blastp_afO31567.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO31567
color 3, chain A
show cartoon, chain A
dist intra_158_valid , resid 163 and blastp_afO31567 and chain A and name cb, resid 55 and blastp_afO31567 and chain A and name cb
dist intra_1221_valid , resid 323 and blastp_afO31567 and chain A and name cb, resid 191 and blastp_afO31567 and chain A and name cb
dist intra_3054_valid , resid 323 and blastp_afO31567 and chain A and name cb, resid 184 and blastp_afO31567 and chain A and name cb
dist intra_3459_valid , resid 176 and blastp_afO31567 and chain A and name cb, resid 184 and blastp_afO31567 and chain A and name cb
dist intra_4341_valid , resid 267 and blastp_afO31567 and chain A and name cb, resid 83 and blastp_afO31567 and chain A and name cb
dist intra_4743_valid , resid 41 and blastp_afO31567 and chain A and name cb, resid 124 and blastp_afO31567 and chain A and name cb
dist intra_1214_unknown , resid 163 and blastp_afO31567 and chain A and name cb, resid 42 and blastp_afO31567 and chain A and name cb
dist intra_1648_unknown , resid 325 and blastp_afO31567 and chain A and name cb, resid 191 and blastp_afO31567 and chain A and name cb
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
save blastp_afO31567.pse
png blastp_afO31567.png
