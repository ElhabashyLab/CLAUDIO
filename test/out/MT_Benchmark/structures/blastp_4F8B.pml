load blastp_4F8B.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_4F8B
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_4F8B
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain C
show surface, chain C and blastp_4F8B
color 7, chain C
show cartoon, chain C
hide everything, show cartoon, chain D
show surface, chain D and blastp_4F8B
color 8, chain D
show cartoon, chain D
hide everything, show cartoon, chain E
show surface, chain E and blastp_4F8B
color 9, chain E
show cartoon, chain E
dist intra_4783_overlaps , resid 145 and blastp_4F8B and chain A and name cb, resid 142 and blastp_4F8B and chain A and name cb
dist inter_4783_2_valid , resid 145 and blastp_4F8B and chain A and name cb, resid 142 and blastp_4F8B and chain B and name cb
dist inter_4783_3_valid , resid 145 and blastp_4F8B and chain A and name cb, resid 142 and blastp_4F8B and chain C and name cb
dist inter_4783_4_valid , resid 145 and blastp_4F8B and chain A and name cb, resid 142 and blastp_4F8B and chain D and name cb
dist inter_4783_5_valid , resid 145 and blastp_4F8B and chain A and name cb, resid 142 and blastp_4F8B and chain E and name cb
dist inter_4783_6_valid , resid 145 and blastp_4F8B and chain B and name cb, resid 142 and blastp_4F8B and chain A and name cb
dist inter_4783_8_valid , resid 145 and blastp_4F8B and chain B and name cb, resid 142 and blastp_4F8B and chain C and name cb
dist inter_4783_9_valid , resid 145 and blastp_4F8B and chain B and name cb, resid 142 and blastp_4F8B and chain D and name cb
dist inter_4783_10_valid , resid 145 and blastp_4F8B and chain B and name cb, resid 142 and blastp_4F8B and chain E and name cb
dist inter_4783_11_valid , resid 145 and blastp_4F8B and chain C and name cb, resid 142 and blastp_4F8B and chain A and name cb
dist inter_4783_12_valid , resid 145 and blastp_4F8B and chain C and name cb, resid 142 and blastp_4F8B and chain B and name cb
dist inter_4783_14_valid , resid 145 and blastp_4F8B and chain C and name cb, resid 142 and blastp_4F8B and chain D and name cb
dist inter_4783_15_valid , resid 145 and blastp_4F8B and chain C and name cb, resid 142 and blastp_4F8B and chain E and name cb
dist inter_4783_16_valid , resid 145 and blastp_4F8B and chain D and name cb, resid 142 and blastp_4F8B and chain A and name cb
dist inter_4783_17_valid , resid 145 and blastp_4F8B and chain D and name cb, resid 142 and blastp_4F8B and chain B and name cb
dist inter_4783_18_valid , resid 145 and blastp_4F8B and chain D and name cb, resid 142 and blastp_4F8B and chain C and name cb
dist inter_4783_20_valid , resid 145 and blastp_4F8B and chain D and name cb, resid 142 and blastp_4F8B and chain E and name cb
dist inter_4783_21_valid , resid 145 and blastp_4F8B and chain E and name cb, resid 142 and blastp_4F8B and chain A and name cb
dist inter_4783_22_valid , resid 145 and blastp_4F8B and chain E and name cb, resid 142 and blastp_4F8B and chain B and name cb
dist inter_4783_23_valid , resid 145 and blastp_4F8B and chain E and name cb, resid 142 and blastp_4F8B and chain C and name cb
dist inter_4783_24_valid , resid 145 and blastp_4F8B and chain E and name cb, resid 142 and blastp_4F8B and chain D and name cb
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
save blastp_4F8B.pse
png blastp_4F8B.png
