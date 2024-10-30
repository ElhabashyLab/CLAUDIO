load blastp_afQ06752.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afQ06752
color 3, chain A
show cartoon, chain A
dist intra_1406_valid , resid 108 and blastp_afQ06752 and chain A and name cb, resid 95 and blastp_afQ06752 and chain A and name cb
dist intra_1503_valid , resid 188 and blastp_afQ06752 and chain A and name cb, resid 77 and blastp_afQ06752 and chain A and name cb
dist intra_1734_valid , resid 269 and blastp_afQ06752 and chain A and name cb, resid 77 and blastp_afQ06752 and chain A and name cb
dist intra_1788_valid , resid 320 and blastp_afQ06752 and chain A and name cb, resid 313 and blastp_afQ06752 and chain A and name cb
dist intra_3153_valid , resid 108 and blastp_afQ06752 and chain A and name cb, resid 426 and blastp_afQ06752 and chain A and name cb
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
save blastp_afQ06752.pse
png blastp_afQ06752.png
