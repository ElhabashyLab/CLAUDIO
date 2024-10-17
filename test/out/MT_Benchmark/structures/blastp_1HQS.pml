load blastp_1HQS.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_1HQS
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_1HQS
color 5, chain B
show cartoon, chain B
dist intra_13_valid , resid 226 and blastp_1HQS and chain A and name cb, resid 178 and blastp_1HQS and chain A and name cb
dist intra_13_4_valid , resid 226 and blastp_1HQS and chain B and name cb, resid 178 and blastp_1HQS and chain B and name cb
dist intra_113_valid , resid 393 and blastp_1HQS and chain A and name cb, resid 133 and blastp_1HQS and chain A and name cb
dist intra_113_4_valid , resid 393 and blastp_1HQS and chain B and name cb, resid 133 and blastp_1HQS and chain B and name cb
dist intra_137_valid , resid 59 and blastp_1HQS and chain A and name cb, resid 70 and blastp_1HQS and chain A and name cb
dist intra_137_4_valid , resid 59 and blastp_1HQS and chain B and name cb, resid 70 and blastp_1HQS and chain B and name cb
dist intra_165_valid , resid 55 and blastp_1HQS and chain A and name cb, resid 70 and blastp_1HQS and chain A and name cb
dist intra_165_4_valid , resid 55 and blastp_1HQS and chain B and name cb, resid 70 and blastp_1HQS and chain B and name cb
dist intra_184_valid , resid 178 and blastp_1HQS and chain A and name cb, resid 225 and blastp_1HQS and chain A and name cb
dist intra_184_4_valid , resid 178 and blastp_1HQS and chain B and name cb, resid 225 and blastp_1HQS and chain B and name cb
dist intra_2627_valid , resid 214 and blastp_1HQS and chain A and name cb, resid 247 and blastp_1HQS and chain A and name cb
dist intra_2627_4_valid , resid 214 and blastp_1HQS and chain B and name cb, resid 247 and blastp_1HQS and chain B and name cb
dist intra_2634_valid , resid 48 and blastp_1HQS and chain A and name cb, resid 388 and blastp_1HQS and chain A and name cb
dist intra_2634_4_valid , resid 48 and blastp_1HQS and chain B and name cb, resid 388 and blastp_1HQS and chain B and name cb
dist intra_1531_out_range , resid 242 and blastp_1HQS and chain A and name cb, resid 158 and blastp_1HQS and chain A and name cb
dist intra_1312_overlaps , resid 6 and blastp_1HQS and chain A and name cb, resid 55 and blastp_1HQS and chain A and name cb
dist intra_1312_4_overlaps , resid 6 and blastp_1HQS and chain B and name cb, resid 55 and blastp_1HQS and chain B and name cb
dist intra_1065_same , resid 133 and blastp_1HQS and chain A and name cb, resid 133 and blastp_1HQS and chain A and name cb
dist inter_13_3_valid , resid 226 and blastp_1HQS and chain B and name cb, resid 178 and blastp_1HQS and chain A and name cb
dist inter_113_2_valid , resid 393 and blastp_1HQS and chain A and name cb, resid 133 and blastp_1HQS and chain B and name cb
dist inter_113_3_valid , resid 393 and blastp_1HQS and chain B and name cb, resid 133 and blastp_1HQS and chain A and name cb
dist inter_184_2_valid , resid 178 and blastp_1HQS and chain A and name cb, resid 225 and blastp_1HQS and chain B and name cb
dist inter_184_3_valid , resid 178 and blastp_1HQS and chain B and name cb, resid 225 and blastp_1HQS and chain A and name cb
dist inter_1065_2_valid , resid 133 and blastp_1HQS and chain A and name cb, resid 133 and blastp_1HQS and chain B and name cb
dist inter_1531_2_valid , resid 242 and blastp_1HQS and chain A and name cb, resid 158 and blastp_1HQS and chain B and name cb
dist inter_1531_3_valid , resid 242 and blastp_1HQS and chain B and name cb, resid 158 and blastp_1HQS and chain A and name cb
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
save blastp_1HQS.pse
png blastp_1HQS.png
