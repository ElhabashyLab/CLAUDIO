load blastp_afP25812.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP25812
color 3, chain A
show cartoon, chain A
dist intra_1210_valid , resid 553 and blastp_afP25812 and chain A and name cb, resid 514 and blastp_afP25812 and chain A and name cb
dist intra_1512_valid , resid 568 and blastp_afP25812 and chain A and name cb, resid 625 and blastp_afP25812 and chain A and name cb
dist intra_3694_valid , resid 199 and blastp_afP25812 and chain A and name cb, resid 270 and blastp_afP25812 and chain A and name cb
dist intra_4282_valid , resid 563 and blastp_afP25812 and chain A and name cb, resid 560 and blastp_afP25812 and chain A and name cb
dist intra_4618_valid , resid 290 and blastp_afP25812 and chain A and name cb, resid 89 and blastp_afP25812 and chain A and name cb
dist intra_4950_valid , resid 625 and blastp_afP25812 and chain A and name cb, resid 579 and blastp_afP25812 and chain A and name cb
dist intra_4720_unknown , resid 290 and blastp_afP25812 and chain A and name cb, resid 276 and blastp_afP25812 and chain A and name cb
dist intra_5007_unknown , resid 262 and blastp_afP25812 and chain A and name cb, resid 199 and blastp_afP25812 and chain A and name cb
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
save blastp_afP25812.pse
png blastp_afP25812.png
