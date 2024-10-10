load blastp_4UG3.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_4UG3
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_4UG3
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain C
show surface, chain C and blastp_4UG3
color 7, chain C
show cartoon, chain C
hide everything, show cartoon, chain D
show surface, chain D and blastp_4UG3
color 8, chain D
show cartoon, chain D
dist intra_5591_valid , resid 32 and blastp_4UG3 and chain A and name cb, resid 16 and blastp_4UG3 and chain A and name cb
dist intra_5591_6_valid , resid 32 and blastp_4UG3 and chain B and name cb, resid 16 and blastp_4UG3 and chain B and name cb
dist intra_5591_11_valid , resid 32 and blastp_4UG3 and chain C and name cb, resid 16 and blastp_4UG3 and chain C and name cb
dist intra_5591_16_valid , resid 32 and blastp_4UG3 and chain D and name cb, resid 16 and blastp_4UG3 and chain D and name cb
dist intra_5849_valid , resid 7 and blastp_4UG3 and chain A and name cb, resid 16 and blastp_4UG3 and chain A and name cb
dist intra_5849_6_valid , resid 7 and blastp_4UG3 and chain B and name cb, resid 16 and blastp_4UG3 and chain B and name cb
dist intra_5849_11_valid , resid 7 and blastp_4UG3 and chain C and name cb, resid 16 and blastp_4UG3 and chain C and name cb
dist intra_5849_16_valid , resid 7 and blastp_4UG3 and chain D and name cb, resid 16 and blastp_4UG3 and chain D and name cb
dist inter_5591_2_valid , resid 32 and blastp_4UG3 and chain A and name cb, resid 16 and blastp_4UG3 and chain B and name cb
dist inter_5591_3_valid , resid 32 and blastp_4UG3 and chain A and name cb, resid 16 and blastp_4UG3 and chain C and name cb
dist inter_5591_4_valid , resid 32 and blastp_4UG3 and chain A and name cb, resid 16 and blastp_4UG3 and chain D and name cb
dist inter_5591_5_valid , resid 32 and blastp_4UG3 and chain B and name cb, resid 16 and blastp_4UG3 and chain A and name cb
dist inter_5591_12_valid , resid 32 and blastp_4UG3 and chain C and name cb, resid 16 and blastp_4UG3 and chain D and name cb
dist inter_5591_15_valid , resid 32 and blastp_4UG3 and chain D and name cb, resid 16 and blastp_4UG3 and chain C and name cb
dist inter_5849_2_valid , resid 7 and blastp_4UG3 and chain A and name cb, resid 16 and blastp_4UG3 and chain B and name cb
dist inter_5849_5_valid , resid 7 and blastp_4UG3 and chain B and name cb, resid 16 and blastp_4UG3 and chain A and name cb
dist inter_5849_8_valid , resid 7 and blastp_4UG3 and chain B and name cb, resid 16 and blastp_4UG3 and chain D and name cb
dist inter_5849_12_valid , resid 7 and blastp_4UG3 and chain C and name cb, resid 16 and blastp_4UG3 and chain D and name cb
dist inter_5849_13_valid , resid 7 and blastp_4UG3 and chain D and name cb, resid 16 and blastp_4UG3 and chain A and name cb
dist inter_5849_14_valid , resid 7 and blastp_4UG3 and chain D and name cb, resid 16 and blastp_4UG3 and chain B and name cb
dist inter_5849_15_valid , resid 7 and blastp_4UG3 and chain D and name cb, resid 16 and blastp_4UG3 and chain C and name cb
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
save blastp_4UG3.pse
png blastp_4UG3.png
