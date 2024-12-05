load blastp_afO31662.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO31662
color 3, chain A
show cartoon, chain A
dist intra_1988_overlaps , resid 2 and blastp_afO31662 and chain A and name cb, resid 183 and blastp_afO31662 and chain A and name cb
dist intra_2345_overlaps , resid 2 and blastp_afO31662 and chain A and name cb, resid 182 and blastp_afO31662 and chain A and name cb
dist intra_612_unknown , resid 2 and blastp_afO31662 and chain A and name cb, resid 181 and blastp_afO31662 and chain A and name cb
dist intra_5268_unknown , resid 2 and blastp_afO31662 and chain A and name cb, resid 14 and blastp_afO31662 and chain A and name cb
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
save blastp_afO31662.pse
png blastp_afO31662.png
