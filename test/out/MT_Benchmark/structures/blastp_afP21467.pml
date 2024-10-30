load blastp_afP21467.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP21467
color 3, chain A
show cartoon, chain A
dist intra_10_valid , resid 97 and blastp_afP21467 and chain A and name cb, resid 126 and blastp_afP21467 and chain A and name cb
dist intra_475_valid , resid 62 and blastp_afP21467 and chain A and name cb, resid 69 and blastp_afP21467 and chain A and name cb
dist intra_541_valid , resid 52 and blastp_afP21467 and chain A and name cb, resid 62 and blastp_afP21467 and chain A and name cb
dist intra_693_valid , resid 148 and blastp_afP21467 and chain A and name cb, resid 155 and blastp_afP21467 and chain A and name cb
dist intra_1579_valid , resid 26 and blastp_afP21467 and chain A and name cb, resid 62 and blastp_afP21467 and chain A and name cb
dist intra_1807_valid , resid 52 and blastp_afP21467 and chain A and name cb, resid 26 and blastp_afP21467 and chain A and name cb
dist intra_2770_valid , resid 68 and blastp_afP21467 and chain A and name cb, resid 8 and blastp_afP21467 and chain A and name cb
dist intra_3280_valid , resid 97 and blastp_afP21467 and chain A and name cb, resid 159 and blastp_afP21467 and chain A and name cb
dist intra_1194_unknown , resid 155 and blastp_afP21467 and chain A and name cb, resid 139 and blastp_afP21467 and chain A and name cb
dist intra_1349_unknown , resid 26 and blastp_afP21467 and chain A and name cb, resid 43 and blastp_afP21467 and chain A and name cb
dist intra_1388_unknown , resid 43 and blastp_afP21467 and chain A and name cb, resid 62 and blastp_afP21467 and chain A and name cb
dist intra_3437_unknown , resid 148 and blastp_afP21467 and chain A and name cb, resid 150 and blastp_afP21467 and chain A and name cb
dist intra_3573_unknown , resid 97 and blastp_afP21467 and chain A and name cb, resid 113 and blastp_afP21467 and chain A and name cb
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
save blastp_afP21467.pse
png blastp_afP21467.png
