load blastp_3BHP.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_3BHP
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_3BHP
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain C
show surface, chain C and blastp_3BHP
color 7, chain C
show cartoon, chain C
dist intra_4512_valid , resid 32 and blastp_3BHP and chain A and name cb, resid 39 and blastp_3BHP and chain A and name cb
dist intra_4512_5_valid , resid 32 and blastp_3BHP and chain B and name cb, resid 39 and blastp_3BHP and chain B and name cb
dist intra_4512_9_valid , resid 32 and blastp_3BHP and chain C and name cb, resid 39 and blastp_3BHP and chain C and name cb
dist intra_4529_valid , resid 39 and blastp_3BHP and chain A and name cb, resid 46 and blastp_3BHP and chain A and name cb
dist intra_4529_5_valid , resid 39 and blastp_3BHP and chain B and name cb, resid 46 and blastp_3BHP and chain B and name cb
dist intra_4529_9_valid , resid 39 and blastp_3BHP and chain C and name cb, resid 46 and blastp_3BHP and chain C and name cb
dist inter_4512_2_valid , resid 32 and blastp_3BHP and chain A and name cb, resid 39 and blastp_3BHP and chain B and name cb
dist inter_4512_3_valid , resid 32 and blastp_3BHP and chain A and name cb, resid 39 and blastp_3BHP and chain C and name cb
dist inter_4512_4_valid , resid 32 and blastp_3BHP and chain B and name cb, resid 39 and blastp_3BHP and chain A and name cb
dist inter_4512_6_valid , resid 32 and blastp_3BHP and chain B and name cb, resid 39 and blastp_3BHP and chain C and name cb
dist inter_4512_7_valid , resid 32 and blastp_3BHP and chain C and name cb, resid 39 and blastp_3BHP and chain A and name cb
dist inter_4512_8_valid , resid 32 and blastp_3BHP and chain C and name cb, resid 39 and blastp_3BHP and chain B and name cb
dist inter_4529_2_valid , resid 39 and blastp_3BHP and chain A and name cb, resid 46 and blastp_3BHP and chain B and name cb
dist inter_4529_3_valid , resid 39 and blastp_3BHP and chain A and name cb, resid 46 and blastp_3BHP and chain C and name cb
dist inter_4529_4_valid , resid 39 and blastp_3BHP and chain B and name cb, resid 46 and blastp_3BHP and chain A and name cb
dist inter_4529_6_valid , resid 39 and blastp_3BHP and chain B and name cb, resid 46 and blastp_3BHP and chain C and name cb
dist inter_4529_7_valid , resid 39 and blastp_3BHP and chain C and name cb, resid 46 and blastp_3BHP and chain A and name cb
dist inter_4529_8_valid , resid 39 and blastp_3BHP and chain C and name cb, resid 46 and blastp_3BHP and chain B and name cb
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
save blastp_3BHP.pse
png blastp_3BHP.png
