load blastp_afO34348.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO34348
color 3, chain A
show cartoon, chain A
dist intra_1108_valid , resid 181 and blastp_afO34348 and chain A and name cb, resid 188 and blastp_afO34348 and chain A and name cb
dist intra_1332_valid , resid 59 and blastp_afO34348 and chain A and name cb, resid 169 and blastp_afO34348 and chain A and name cb
dist intra_1802_valid , resid 181 and blastp_afO34348 and chain A and name cb, resid 174 and blastp_afO34348 and chain A and name cb
dist intra_4866_valid , resid 274 and blastp_afO34348 and chain A and name cb, resid 280 and blastp_afO34348 and chain A and name cb
dist intra_5107_valid , resid 139 and blastp_afO34348 and chain A and name cb, resid 135 and blastp_afO34348 and chain A and name cb
dist intra_5522_valid , resid 51 and blastp_afO34348 and chain A and name cb, resid 165 and blastp_afO34348 and chain A and name cb
dist intra_2113_unknown , resid 51 and blastp_afO34348 and chain A and name cb, resid 40 and blastp_afO34348 and chain A and name cb
dist intra_5031_unknown , resid 177 and blastp_afO34348 and chain A and name cb, resid 188 and blastp_afO34348 and chain A and name cb
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
save blastp_afO34348.pse
png blastp_afO34348.png
