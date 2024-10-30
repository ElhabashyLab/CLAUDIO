load blastp_afO32023.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO32023
color 3, chain A
show cartoon, chain A
dist intra_2536_valid , resid 138 and blastp_afO32023 and chain A and name cb, resid 91 and blastp_afO32023 and chain A and name cb
dist intra_2662_valid , resid 72 and blastp_afO32023 and chain A and name cb, resid 65 and blastp_afO32023 and chain A and name cb
dist intra_2180_overlaps , resid 72 and blastp_afO32023 and chain A and name cb, resid 70 and blastp_afO32023 and chain A and name cb
dist intra_3068_unknown , resid 83 and blastp_afO32023 and chain A and name cb, resid 138 and blastp_afO32023 and chain A and name cb
dist intra_4900_unknown , resid 83 and blastp_afO32023 and chain A and name cb, resid 70 and blastp_afO32023 and chain A and name cb
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
save blastp_afO32023.pse
png blastp_afO32023.png
