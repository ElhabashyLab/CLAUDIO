load blastp_afP18579.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP18579
color 3, chain A
show cartoon, chain A
dist intra_715_valid , resid 114 and blastp_afP18579 and chain A and name cb, resid 198 and blastp_afP18579 and chain A and name cb
dist intra_1284_valid , resid 114 and blastp_afP18579 and chain A and name cb, resid 209 and blastp_afP18579 and chain A and name cb
dist intra_2184_valid , resid 209 and blastp_afP18579 and chain A and name cb, resid 213 and blastp_afP18579 and chain A and name cb
dist intra_2936_valid , resid 55 and blastp_afP18579 and chain A and name cb, resid 180 and blastp_afP18579 and chain A and name cb
dist intra_829_overlaps , resid 9 and blastp_afP18579 and chain A and name cb, resid 15 and blastp_afP18579 and chain A and name cb
dist intra_1690_overlaps , resid 9 and blastp_afP18579 and chain A and name cb, resid 12 and blastp_afP18579 and chain A and name cb
dist intra_5144_unknown , resid 213 and blastp_afP18579 and chain A and name cb, resid 199 and blastp_afP18579 and chain A and name cb
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
save blastp_afP18579.pse
png blastp_afP18579.png
