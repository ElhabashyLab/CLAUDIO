load blastp_afP54523.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP54523
color 3, chain A
show cartoon, chain A
dist intra_1447_valid , resid 285 and blastp_afP54523 and chain A and name cb, resid 279 and blastp_afP54523 and chain A and name cb
dist intra_5130_valid , resid 22 and blastp_afP54523 and chain A and name cb, resid 1 and blastp_afP54523 and chain A and name cb
dist intra_4755_out_range , resid 279 and blastp_afP54523 and chain A and name cb, resid 282 and blastp_afP54523 and chain A and name cb
dist intra_4064_overlaps , resid 217 and blastp_afP54523 and chain A and name cb, resid 210 and blastp_afP54523 and chain A and name cb
dist intra_1848_same , resid 210 and blastp_afP54523 and chain A and name cb, resid 210 and blastp_afP54523 and chain A and name cb
dist intra_1206_unknown , resid 348 and blastp_afP54523 and chain A and name cb, resid 310 and blastp_afP54523 and chain A and name cb
dist intra_5846_unknown , resid 310 and blastp_afP54523 and chain A and name cb, resid 336 and blastp_afP54523 and chain A and name cb
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
save blastp_afP54523.pse
png blastp_afP54523.png
