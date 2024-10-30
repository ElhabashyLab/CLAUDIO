load blastp_afO31605.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO31605
color 3, chain A
show cartoon, chain A
dist intra_804_valid , resid 111 and blastp_afO31605 and chain A and name cb, resid 115 and blastp_afO31605 and chain A and name cb
dist intra_1148_valid , resid 408 and blastp_afO31605 and chain A and name cb, resid 389 and blastp_afO31605 and chain A and name cb
dist intra_1329_valid , resid 132 and blastp_afO31605 and chain A and name cb, resid 111 and blastp_afO31605 and chain A and name cb
dist intra_1647_valid , resid 635 and blastp_afO31605 and chain A and name cb, resid 622 and blastp_afO31605 and chain A and name cb
dist intra_974_unknown , resid 67 and blastp_afO31605 and chain A and name cb, resid 382 and blastp_afO31605 and chain A and name cb
dist intra_3101_unknown , resid 67 and blastp_afO31605 and chain A and name cb, resid 422 and blastp_afO31605 and chain A and name cb
dist intra_4456_unknown , resid 67 and blastp_afO31605 and chain A and name cb, resid 381 and blastp_afO31605 and chain A and name cb
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
save blastp_afO31605.pse
png blastp_afO31605.png
