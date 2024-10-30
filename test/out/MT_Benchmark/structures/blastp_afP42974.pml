load blastp_afP42974.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP42974
color 3, chain A
show cartoon, chain A
dist intra_917_valid , resid 402 and blastp_afP42974 and chain A and name cb, resid 390 and blastp_afP42974 and chain A and name cb
dist intra_1204_valid , resid 35 and blastp_afP42974 and chain A and name cb, resid 55 and blastp_afP42974 and chain A and name cb
dist intra_3687_valid , resid 330 and blastp_afP42974 and chain A and name cb, resid 264 and blastp_afP42974 and chain A and name cb
dist intra_4210_valid , resid 330 and blastp_afP42974 and chain A and name cb, resid 106 and blastp_afP42974 and chain A and name cb
dist intra_3995_out_range , resid 330 and blastp_afP42974 and chain A and name cb, resid 112 and blastp_afP42974 and chain A and name cb
dist intra_1978_unknown , resid 384 and blastp_afP42974 and chain A and name cb, resid 402 and blastp_afP42974 and chain A and name cb
dist intra_6009_unknown , resid 112 and blastp_afP42974 and chain A and name cb, resid 390 and blastp_afP42974 and chain A and name cb
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
save blastp_afP42974.pse
png blastp_afP42974.png
