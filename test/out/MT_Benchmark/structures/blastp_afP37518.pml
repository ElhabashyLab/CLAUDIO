load blastp_afP37518.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP37518
color 3, chain A
show cartoon, chain A
dist intra_540_valid , resid 303 and blastp_afP37518 and chain A and name cb, resid 350 and blastp_afP37518 and chain A and name cb
dist intra_1083_valid , resid 303 and blastp_afP37518 and chain A and name cb, resid 189 and blastp_afP37518 and chain A and name cb
dist intra_1205_valid , resid 167 and blastp_afP37518 and chain A and name cb, resid 176 and blastp_afP37518 and chain A and name cb
dist intra_1338_valid , resid 15 and blastp_afP37518 and chain A and name cb, resid 192 and blastp_afP37518 and chain A and name cb
dist intra_1477_valid , resid 189 and blastp_afP37518 and chain A and name cb, resid 299 and blastp_afP37518 and chain A and name cb
dist intra_5288_valid , resid 189 and blastp_afP37518 and chain A and name cb, resid 302 and blastp_afP37518 and chain A and name cb
dist intra_3608_unknown , resid 89 and blastp_afP37518 and chain A and name cb, resid 78 and blastp_afP37518 and chain A and name cb
dist intra_5325_unknown , resid 303 and blastp_afP37518 and chain A and name cb, resid 180 and blastp_afP37518 and chain A and name cb
dist intra_5489_unknown , resid 180 and blastp_afP37518 and chain A and name cb, resid 299 and blastp_afP37518 and chain A and name cb
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
save blastp_afP37518.pse
png blastp_afP37518.png
