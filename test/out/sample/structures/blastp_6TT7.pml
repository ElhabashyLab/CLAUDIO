load blastp_6TT7.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain I
show surface, chain I and blastp_6TT7
color 3, chain I
show cartoon, chain I
hide everything, show cartoon, chain B
show surface, chain B and blastp_6TT7
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain A
show surface, chain A and blastp_6TT7
color 6, chain A
show cartoon, chain A
hide everything, show cartoon, chain E
show surface, chain E and blastp_6TT7
color 7, chain E
show cartoon, chain E
hide everything, show cartoon, chain C
show surface, chain C and blastp_6TT7
color 8, chain C
show cartoon, chain C
dist intra_19_valid , resid 197 and blastp_6TT7 and chain A and name cb, resid 488 and blastp_6TT7 and chain A and name cb
dist inter_1_valid , resid 37 and blastp_6TT7 and chain I and name cb, resid 460 and blastp_6TT7 and chain A and name cb
dist inter_7_5_valid , resid 218 and blastp_6TT7 and chain B and name cb, resid 150 and blastp_6TT7 and chain E and name cb
dist inter_14_3_valid , resid 44 and blastp_6TT7 and chain I and name cb, resid 455 and blastp_6TT7 and chain C and name cb
show dashes
set dash_gap, 0.1
color blue, intra*_valid
color red, intra*_out_range
color red, intra*_overlaps
color red, intra*_same
color blue, inter*_valid
color red, inter*_out_range
color red, inter*_overlaps
color red, inter*_same
set dash_width, 9
center
save blastp_6TT7.pse
png blastp_6TT7.png
