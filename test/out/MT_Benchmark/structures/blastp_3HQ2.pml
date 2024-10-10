load blastp_3HQ2.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_3HQ2
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_3HQ2
color 5, chain B
show cartoon, chain B
dist intra_1644_valid , resid 343 and blastp_3HQ2 and chain A and name cb, resid 194 and blastp_3HQ2 and chain A and name cb
dist intra_1644_4_valid , resid 343 and blastp_3HQ2 and chain B and name cb, resid 194 and blastp_3HQ2 and chain B and name cb
dist intra_2271_valid , resid 202 and blastp_3HQ2 and chain A and name cb, resid 254 and blastp_3HQ2 and chain A and name cb
dist intra_2271_4_valid , resid 202 and blastp_3HQ2 and chain B and name cb, resid 254 and blastp_3HQ2 and chain B and name cb
dist intra_3396_valid , resid 318 and blastp_3HQ2 and chain A and name cb, resid 202 and blastp_3HQ2 and chain A and name cb
dist intra_3396_4_valid , resid 318 and blastp_3HQ2 and chain B and name cb, resid 202 and blastp_3HQ2 and chain B and name cb
dist intra_3717_valid , resid 83 and blastp_3HQ2 and chain A and name cb, resid 469 and blastp_3HQ2 and chain A and name cb
dist intra_3717_4_valid , resid 83 and blastp_3HQ2 and chain B and name cb, resid 469 and blastp_3HQ2 and chain B and name cb
dist intra_4082_valid , resid 469 and blastp_3HQ2 and chain A and name cb, resid 89 and blastp_3HQ2 and chain A and name cb
dist intra_4082_4_valid , resid 469 and blastp_3HQ2 and chain B and name cb, resid 89 and blastp_3HQ2 and chain B and name cb
dist intra_5488_valid , resid 83 and blastp_3HQ2 and chain A and name cb, resid 468 and blastp_3HQ2 and chain A and name cb
dist intra_5488_4_valid , resid 83 and blastp_3HQ2 and chain B and name cb, resid 468 and blastp_3HQ2 and chain B and name cb
dist intra_6062_valid , resid 97 and blastp_3HQ2 and chain A and name cb, resid 89 and blastp_3HQ2 and chain A and name cb
dist intra_6062_4_valid , resid 97 and blastp_3HQ2 and chain B and name cb, resid 89 and blastp_3HQ2 and chain B and name cb
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
save blastp_3HQ2.pse
png blastp_3HQ2.png
