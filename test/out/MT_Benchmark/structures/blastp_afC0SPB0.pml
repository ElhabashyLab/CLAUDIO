load blastp_afC0SPB0.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afC0SPB0
color 3, chain A
show cartoon, chain A
dist intra_1415_valid , resid 309 and blastp_afC0SPB0 and chain A and name cb, resid 277 and blastp_afC0SPB0 and chain A and name cb
dist intra_1729_valid , resid 65 and blastp_afC0SPB0 and chain A and name cb, resid 69 and blastp_afC0SPB0 and chain A and name cb
dist intra_2064_valid , resid 518 and blastp_afC0SPB0 and chain A and name cb, resid 104 and blastp_afC0SPB0 and chain A and name cb
dist intra_3284_valid , resid 505 and blastp_afC0SPB0 and chain A and name cb, resid 444 and blastp_afC0SPB0 and chain A and name cb
dist intra_5108_valid , resid 282 and blastp_afC0SPB0 and chain A and name cb, resid 309 and blastp_afC0SPB0 and chain A and name cb
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
save blastp_afC0SPB0.pse
png blastp_afC0SPB0.png
