load blastp_afO31545.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO31545
color 3, chain A
show cartoon, chain A
dist intra_3196_valid , resid 463 and blastp_afO31545 and chain A and name cb, resid 435 and blastp_afO31545 and chain A and name cb
dist intra_3595_valid , resid 118 and blastp_afO31545 and chain A and name cb, resid 435 and blastp_afO31545 and chain A and name cb
dist intra_4349_valid , resid 410 and blastp_afO31545 and chain A and name cb, resid 383 and blastp_afO31545 and chain A and name cb
dist intra_6075_valid , resid 268 and blastp_afO31545 and chain A and name cb, resid 141 and blastp_afO31545 and chain A and name cb
dist intra_4377_unknown , resid 435 and blastp_afO31545 and chain A and name cb, resid 398 and blastp_afO31545 and chain A and name cb
dist intra_5016_unknown , resid 6 and blastp_afO31545 and chain A and name cb, resid 61 and blastp_afO31545 and chain A and name cb
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
save blastp_afO31545.pse
png blastp_afO31545.png
