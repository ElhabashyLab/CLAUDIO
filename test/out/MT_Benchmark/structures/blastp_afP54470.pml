load blastp_afP54470.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP54470
color 3, chain A
show cartoon, chain A
dist intra_2139_valid , resid 266 and blastp_afP54470 and chain A and name cb, resid 122 and blastp_afP54470 and chain A and name cb
dist intra_2490_valid , resid 123 and blastp_afP54470 and chain A and name cb, resid 167 and blastp_afP54470 and chain A and name cb
dist intra_2963_valid , resid 167 and blastp_afP54470 and chain A and name cb, resid 266 and blastp_afP54470 and chain A and name cb
dist intra_5865_valid , resid 193 and blastp_afP54470 and chain A and name cb, resid 266 and blastp_afP54470 and chain A and name cb
dist intra_5543_same , resid 203 and blastp_afP54470 and chain A and name cb, resid 203 and blastp_afP54470 and chain A and name cb
dist intra_2497_unknown , resid 266 and blastp_afP54470 and chain A and name cb, resid 115 and blastp_afP54470 and chain A and name cb
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
save blastp_afP54470.pse
png blastp_afP54470.png
