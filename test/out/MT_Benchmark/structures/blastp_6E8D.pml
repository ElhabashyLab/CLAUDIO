load blastp_6E8D.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_6E8D
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_6E8D
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain C
show surface, chain C and blastp_6E8D
color 7, chain C
show cartoon, chain C
hide everything, show cartoon, chain D
show surface, chain D and blastp_6E8D
color 8, chain D
show cartoon, chain D
dist intra_1735_valid , resid 119 and blastp_6E8D and chain A and name cb, resid 51 and blastp_6E8D and chain A and name cb
dist intra_1735_6_valid , resid 119 and blastp_6E8D and chain B and name cb, resid 51 and blastp_6E8D and chain B and name cb
dist intra_1735_11_valid , resid 119 and blastp_6E8D and chain C and name cb, resid 51 and blastp_6E8D and chain C and name cb
dist intra_1735_16_valid , resid 119 and blastp_6E8D and chain D and name cb, resid 51 and blastp_6E8D and chain D and name cb
dist intra_3360_out_range , resid 301 and blastp_6E8D and chain A and name cb, resid 39 and blastp_6E8D and chain A and name cb
dist inter_1735_3_valid , resid 119 and blastp_6E8D and chain A and name cb, resid 51 and blastp_6E8D and chain C and name cb
dist inter_1735_8_valid , resid 119 and blastp_6E8D and chain B and name cb, resid 51 and blastp_6E8D and chain D and name cb
dist inter_1735_9_valid , resid 119 and blastp_6E8D and chain C and name cb, resid 51 and blastp_6E8D and chain A and name cb
dist inter_1735_14_valid , resid 119 and blastp_6E8D and chain D and name cb, resid 51 and blastp_6E8D and chain B and name cb
dist inter_3360_3_valid , resid 301 and blastp_6E8D and chain A and name cb, resid 39 and blastp_6E8D and chain C and name cb
dist inter_3360_8_valid , resid 301 and blastp_6E8D and chain B and name cb, resid 39 and blastp_6E8D and chain D and name cb
dist inter_3360_9_valid , resid 301 and blastp_6E8D and chain C and name cb, resid 39 and blastp_6E8D and chain A and name cb
dist inter_3360_10_valid , resid 301 and blastp_6E8D and chain C and name cb, resid 39 and blastp_6E8D and chain B and name cb
dist inter_3360_14_valid , resid 301 and blastp_6E8D and chain D and name cb, resid 39 and blastp_6E8D and chain B and name cb
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
save blastp_6E8D.pse
png blastp_6E8D.png
