load blastp_afP51834.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP51834
color 3, chain A
show cartoon, chain A
dist intra_3084_valid , resid 268 and blastp_afP51834 and chain A and name cb, resid 898 and blastp_afP51834 and chain A and name cb
dist intra_4887_valid , resid 713 and blastp_afP51834 and chain A and name cb, resid 465 and blastp_afP51834 and chain A and name cb
dist intra_6115_valid , resid 247 and blastp_afP51834 and chain A and name cb, resid 930 and blastp_afP51834 and chain A and name cb
dist intra_3242_unknown , resid 668 and blastp_afP51834 and chain A and name cb, resid 666 and blastp_afP51834 and chain A and name cb
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
save blastp_afP51834.pse
png blastp_afP51834.png
