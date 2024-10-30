load blastp_afP24281.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP24281
color 3, chain A
show cartoon, chain A
dist intra_1883_valid , resid 85 and blastp_afP24281 and chain A and name cb, resid 32 and blastp_afP24281 and chain A and name cb
dist intra_2480_valid , resid 20 and blastp_afP24281 and chain A and name cb, resid 12 and blastp_afP24281 and chain A and name cb
dist intra_2664_valid , resid 20 and blastp_afP24281 and chain A and name cb, resid 13 and blastp_afP24281 and chain A and name cb
dist intra_4167_valid , resid 85 and blastp_afP24281 and chain A and name cb, resid 20 and blastp_afP24281 and chain A and name cb
dist intra_4216_valid , resid 18 and blastp_afP24281 and chain A and name cb, resid 12 and blastp_afP24281 and chain A and name cb
dist intra_5285_valid , resid 17 and blastp_afP24281 and chain A and name cb, resid 10 and blastp_afP24281 and chain A and name cb
dist intra_5913_valid , resid 17 and blastp_afP24281 and chain A and name cb, resid 24 and blastp_afP24281 and chain A and name cb
dist intra_5410_unknown , resid 10 and blastp_afP24281 and chain A and name cb, resid 14 and blastp_afP24281 and chain A and name cb
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
save blastp_afP24281.pse
png blastp_afP24281.png
