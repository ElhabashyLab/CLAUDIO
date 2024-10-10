load blastp_3GFV.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_3GFV
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_3GFV
color 5, chain B
show cartoon, chain B
dist intra_3055_valid , resid 20 and blastp_3GFV and chain A and name cb, resid 141 and blastp_3GFV and chain A and name cb
dist intra_3055_4_valid , resid 20 and blastp_3GFV and chain B and name cb, resid 141 and blastp_3GFV and chain B and name cb
dist intra_3322_valid , resid 190 and blastp_3GFV and chain A and name cb, resid 210 and blastp_3GFV and chain A and name cb
dist intra_3322_4_valid , resid 190 and blastp_3GFV and chain B and name cb, resid 210 and blastp_3GFV and chain B and name cb
dist intra_4765_valid , resid 190 and blastp_3GFV and chain A and name cb, resid 127 and blastp_3GFV and chain A and name cb
dist intra_4765_4_valid , resid 190 and blastp_3GFV and chain B and name cb, resid 127 and blastp_3GFV and chain B and name cb
dist intra_5873_valid , resid 141 and blastp_3GFV and chain A and name cb, resid 150 and blastp_3GFV and chain A and name cb
dist intra_5873_4_valid , resid 141 and blastp_3GFV and chain B and name cb, resid 150 and blastp_3GFV and chain B and name cb
dist intra_6114_valid , resid 29 and blastp_3GFV and chain A and name cb, resid 20 and blastp_3GFV and chain A and name cb
dist intra_6114_4_valid , resid 29 and blastp_3GFV and chain B and name cb, resid 20 and blastp_3GFV and chain B and name cb
dist inter_3322_2_valid , resid 190 and blastp_3GFV and chain A and name cb, resid 210 and blastp_3GFV and chain B and name cb
dist inter_3322_3_valid , resid 190 and blastp_3GFV and chain B and name cb, resid 210 and blastp_3GFV and chain A and name cb
dist inter_6114_2_valid , resid 29 and blastp_3GFV and chain A and name cb, resid 20 and blastp_3GFV and chain B and name cb
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
save blastp_3GFV.pse
png blastp_3GFV.png
