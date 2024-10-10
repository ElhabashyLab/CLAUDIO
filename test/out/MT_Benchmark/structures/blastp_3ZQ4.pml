load blastp_3ZQ4.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_3ZQ4
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain C
show surface, chain C and blastp_3ZQ4
color 5, chain C
show cartoon, chain C
hide everything, show cartoon, chain D
show surface, chain D and blastp_3ZQ4
color 7, chain D
show cartoon, chain D
hide everything, show cartoon, chain E
show surface, chain E and blastp_3ZQ4
color 8, chain E
show cartoon, chain E
dist intra_1111_valid , resid 129 and blastp_3ZQ4 and chain A and name cb, resid 153 and blastp_3ZQ4 and chain A and name cb
dist intra_1111_6_valid , resid 129 and blastp_3ZQ4 and chain C and name cb, resid 153 and blastp_3ZQ4 and chain C and name cb
dist intra_1111_11_valid , resid 129 and blastp_3ZQ4 and chain D and name cb, resid 153 and blastp_3ZQ4 and chain D and name cb
dist intra_1111_16_valid , resid 129 and blastp_3ZQ4 and chain E and name cb, resid 153 and blastp_3ZQ4 and chain E and name cb
dist intra_2726_valid , resid 251 and blastp_3ZQ4 and chain A and name cb, resid 292 and blastp_3ZQ4 and chain A and name cb
dist intra_2726_6_valid , resid 251 and blastp_3ZQ4 and chain C and name cb, resid 292 and blastp_3ZQ4 and chain C and name cb
dist intra_2726_11_valid , resid 251 and blastp_3ZQ4 and chain D and name cb, resid 292 and blastp_3ZQ4 and chain D and name cb
dist intra_2726_16_valid , resid 251 and blastp_3ZQ4 and chain E and name cb, resid 292 and blastp_3ZQ4 and chain E and name cb
dist intra_3525_valid , resid 129 and blastp_3ZQ4 and chain A and name cb, resid 132 and blastp_3ZQ4 and chain A and name cb
dist intra_3525_6_valid , resid 129 and blastp_3ZQ4 and chain C and name cb, resid 132 and blastp_3ZQ4 and chain C and name cb
dist intra_3525_11_valid , resid 129 and blastp_3ZQ4 and chain D and name cb, resid 132 and blastp_3ZQ4 and chain D and name cb
dist intra_3525_16_valid , resid 129 and blastp_3ZQ4 and chain E and name cb, resid 132 and blastp_3ZQ4 and chain E and name cb
dist inter_2726_3_valid , resid 251 and blastp_3ZQ4 and chain A and name cb, resid 292 and blastp_3ZQ4 and chain D and name cb
dist inter_2726_8_valid , resid 251 and blastp_3ZQ4 and chain C and name cb, resid 292 and blastp_3ZQ4 and chain E and name cb
dist inter_2726_9_valid , resid 251 and blastp_3ZQ4 and chain D and name cb, resid 292 and blastp_3ZQ4 and chain A and name cb
dist inter_2726_14_valid , resid 251 and blastp_3ZQ4 and chain E and name cb, resid 292 and blastp_3ZQ4 and chain C and name cb
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
save blastp_3ZQ4.pse
png blastp_3ZQ4.png
