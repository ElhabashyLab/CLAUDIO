load blastp_4B2O.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_4B2O
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_4B2O
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain C
show surface, chain C and blastp_4B2O
color 7, chain C
show cartoon, chain C
hide everything, show cartoon, chain D
show surface, chain D and blastp_4B2O
color 8, chain D
show cartoon, chain D
dist intra_924_valid , resid 50 and blastp_4B2O and chain A and name cb, resid 19 and blastp_4B2O and chain A and name cb
dist intra_924_6_valid , resid 50 and blastp_4B2O and chain B and name cb, resid 19 and blastp_4B2O and chain B and name cb
dist intra_924_11_valid , resid 50 and blastp_4B2O and chain C and name cb, resid 19 and blastp_4B2O and chain C and name cb
dist intra_924_16_valid , resid 50 and blastp_4B2O and chain D and name cb, resid 19 and blastp_4B2O and chain D and name cb
dist intra_2105_valid , resid 108 and blastp_4B2O and chain A and name cb, resid 246 and blastp_4B2O and chain A and name cb
dist intra_2105_6_valid , resid 108 and blastp_4B2O and chain B and name cb, resid 246 and blastp_4B2O and chain B and name cb
dist intra_2105_11_valid , resid 108 and blastp_4B2O and chain C and name cb, resid 246 and blastp_4B2O and chain C and name cb
dist intra_2105_16_valid , resid 108 and blastp_4B2O and chain D and name cb, resid 246 and blastp_4B2O and chain D and name cb
dist intra_4205_valid , resid 73 and blastp_4B2O and chain A and name cb, resid 215 and blastp_4B2O and chain A and name cb
dist intra_4205_6_valid , resid 73 and blastp_4B2O and chain B and name cb, resid 215 and blastp_4B2O and chain B and name cb
dist intra_4205_11_valid , resid 73 and blastp_4B2O and chain C and name cb, resid 215 and blastp_4B2O and chain C and name cb
dist intra_4205_16_valid , resid 73 and blastp_4B2O and chain D and name cb, resid 215 and blastp_4B2O and chain D and name cb
dist intra_5418_valid , resid 215 and blastp_4B2O and chain A and name cb, resid 218 and blastp_4B2O and chain A and name cb
dist intra_5418_6_valid , resid 215 and blastp_4B2O and chain B and name cb, resid 218 and blastp_4B2O and chain B and name cb
dist intra_5418_11_valid , resid 215 and blastp_4B2O and chain C and name cb, resid 218 and blastp_4B2O and chain C and name cb
dist intra_5418_16_valid , resid 215 and blastp_4B2O and chain D and name cb, resid 218 and blastp_4B2O and chain D and name cb
dist inter_4205_3_valid , resid 73 and blastp_4B2O and chain A and name cb, resid 215 and blastp_4B2O and chain C and name cb
dist inter_4205_8_valid , resid 73 and blastp_4B2O and chain B and name cb, resid 215 and blastp_4B2O and chain D and name cb
dist inter_4205_9_valid , resid 73 and blastp_4B2O and chain C and name cb, resid 215 and blastp_4B2O and chain A and name cb
dist inter_4205_14_valid , resid 73 and blastp_4B2O and chain D and name cb, resid 215 and blastp_4B2O and chain B and name cb
dist inter_5418_4_valid , resid 215 and blastp_4B2O and chain A and name cb, resid 218 and blastp_4B2O and chain D and name cb
dist inter_5418_7_valid , resid 215 and blastp_4B2O and chain B and name cb, resid 218 and blastp_4B2O and chain C and name cb
dist inter_5418_10_valid , resid 215 and blastp_4B2O and chain C and name cb, resid 218 and blastp_4B2O and chain B and name cb
dist inter_5418_13_valid , resid 215 and blastp_4B2O and chain D and name cb, resid 218 and blastp_4B2O and chain A and name cb
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
save blastp_4B2O.pse
png blastp_4B2O.png
