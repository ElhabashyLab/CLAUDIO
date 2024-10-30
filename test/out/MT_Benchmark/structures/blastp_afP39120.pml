load blastp_afP39120.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP39120
color 3, chain A
show cartoon, chain A
dist intra_295_valid , resid 68 and blastp_afP39120 and chain A and name cb, resid 126 and blastp_afP39120 and chain A and name cb
dist intra_413_valid , resid 261 and blastp_afP39120 and chain A and name cb, resid 301 and blastp_afP39120 and chain A and name cb
dist intra_624_valid , resid 301 and blastp_afP39120 and chain A and name cb, resid 251 and blastp_afP39120 and chain A and name cb
dist intra_1075_valid , resid 249 and blastp_afP39120 and chain A and name cb, resid 301 and blastp_afP39120 and chain A and name cb
dist intra_2512_valid , resid 57 and blastp_afP39120 and chain A and name cb, resid 68 and blastp_afP39120 and chain A and name cb
dist intra_5233_valid , resid 63 and blastp_afP39120 and chain A and name cb, resid 56 and blastp_afP39120 and chain A and name cb
dist intra_1462_unknown , resid 301 and blastp_afP39120 and chain A and name cb, resid 250 and blastp_afP39120 and chain A and name cb
dist intra_1478_unknown , resid 64 and blastp_afP39120 and chain A and name cb, resid 126 and blastp_afP39120 and chain A and name cb
dist intra_1774_unknown , resid 293 and blastp_afP39120 and chain A and name cb, resid 251 and blastp_afP39120 and chain A and name cb
dist intra_2854_unknown , resid 249 and blastp_afP39120 and chain A and name cb, resid 293 and blastp_afP39120 and chain A and name cb
dist intra_4178_unknown , resid 56 and blastp_afP39120 and chain A and name cb, resid 64 and blastp_afP39120 and chain A and name cb
dist intra_5445_unknown , resid 293 and blastp_afP39120 and chain A and name cb, resid 250 and blastp_afP39120 and chain A and name cb
dist intra_5868_unknown , resid 261 and blastp_afP39120 and chain A and name cb, resid 293 and blastp_afP39120 and chain A and name cb
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
save blastp_afP39120.pse
png blastp_afP39120.png
