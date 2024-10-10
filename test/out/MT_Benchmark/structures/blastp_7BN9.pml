load blastp_7BN9.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_7BN9
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_7BN9
color 5, chain B
show cartoon, chain B
dist intra_1056_valid , resid 227 and blastp_7BN9 and chain A and name cb, resid 211 and blastp_7BN9 and chain A and name cb
dist intra_1056_4_valid , resid 227 and blastp_7BN9 and chain B and name cb, resid 211 and blastp_7BN9 and chain B and name cb
dist intra_1062_valid , resid 227 and blastp_7BN9 and chain A and name cb, resid 260 and blastp_7BN9 and chain A and name cb
dist intra_1062_4_valid , resid 227 and blastp_7BN9 and chain B and name cb, resid 260 and blastp_7BN9 and chain B and name cb
dist intra_2444_valid , resid 323 and blastp_7BN9 and chain A and name cb, resid 77 and blastp_7BN9 and chain A and name cb
dist intra_3032_valid , resid 229 and blastp_7BN9 and chain A and name cb, resid 260 and blastp_7BN9 and chain A and name cb
dist intra_3032_4_valid , resid 229 and blastp_7BN9 and chain B and name cb, resid 260 and blastp_7BN9 and chain B and name cb
dist intra_3804_valid , resid 102 and blastp_7BN9 and chain A and name cb, resid 115 and blastp_7BN9 and chain A and name cb
dist intra_3811_valid , resid 323 and blastp_7BN9 and chain A and name cb, resid 279 and blastp_7BN9 and chain A and name cb
dist intra_3811_4_valid , resid 323 and blastp_7BN9 and chain B and name cb, resid 279 and blastp_7BN9 and chain B and name cb
dist intra_4241_valid , resid 61 and blastp_7BN9 and chain A and name cb, resid 68 and blastp_7BN9 and chain A and name cb
dist intra_4241_4_valid , resid 61 and blastp_7BN9 and chain B and name cb, resid 68 and blastp_7BN9 and chain B and name cb
dist intra_4335_valid , resid 80 and blastp_7BN9 and chain A and name cb, resid 111 and blastp_7BN9 and chain A and name cb
dist intra_4711_valid , resid 115 and blastp_7BN9 and chain A and name cb, resid 88 and blastp_7BN9 and chain A and name cb
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
save blastp_7BN9.pse
png blastp_7BN9.png
