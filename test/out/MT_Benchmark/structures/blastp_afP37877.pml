load blastp_afP37877.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP37877
color 3, chain A
show cartoon, chain A
dist intra_16_valid , resid 3 and blastp_afP37877 and chain A and name cb, resid 78 and blastp_afP37877 and chain A and name cb
dist intra_516_valid , resid 198 and blastp_afP37877 and chain A and name cb, resid 183 and blastp_afP37877 and chain A and name cb
dist intra_1304_out_range , resid 198 and blastp_afP37877 and chain A and name cb, resid 290 and blastp_afP37877 and chain A and name cb
dist intra_2119_overlaps , resid 3 and blastp_afP37877 and chain A and name cb, resid 71 and blastp_afP37877 and chain A and name cb
dist intra_3352_overlaps , resid 2 and blastp_afP37877 and chain A and name cb, resid 71 and blastp_afP37877 and chain A and name cb
dist intra_1279_unknown , resid 2 and blastp_afP37877 and chain A and name cb, resid 78 and blastp_afP37877 and chain A and name cb
dist intra_3378_unknown , resid 198 and blastp_afP37877 and chain A and name cb, resid 202 and blastp_afP37877 and chain A and name cb
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
save blastp_afP37877.pse
png blastp_afP37877.png
