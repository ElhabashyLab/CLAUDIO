load blastp_3PRH.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_3PRH
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_3PRH
color 5, chain B
show cartoon, chain B
dist intra_948_valid , resid 314 and blastp_3PRH and chain A and name cb, resid 318 and blastp_3PRH and chain A and name cb
dist intra_948_4_valid , resid 314 and blastp_3PRH and chain B and name cb, resid 318 and blastp_3PRH and chain B and name cb
dist intra_1373_valid , resid 217 and blastp_3PRH and chain A and name cb, resid 212 and blastp_3PRH and chain A and name cb
dist intra_1373_4_valid , resid 217 and blastp_3PRH and chain B and name cb, resid 212 and blastp_3PRH and chain B and name cb
dist intra_2157_valid , resid 270 and blastp_3PRH and chain A and name cb, resid 219 and blastp_3PRH and chain A and name cb
dist intra_2157_4_valid , resid 270 and blastp_3PRH and chain B and name cb, resid 219 and blastp_3PRH and chain B and name cb
dist intra_2636_valid , resid 219 and blastp_3PRH and chain A and name cb, resid 202 and blastp_3PRH and chain A and name cb
dist intra_2636_4_valid , resid 219 and blastp_3PRH and chain B and name cb, resid 202 and blastp_3PRH and chain B and name cb
dist intra_3335_valid , resid 219 and blastp_3PRH and chain A and name cb, resid 212 and blastp_3PRH and chain A and name cb
dist intra_3335_4_valid , resid 219 and blastp_3PRH and chain B and name cb, resid 212 and blastp_3PRH and chain B and name cb
dist intra_3909_valid , resid 179 and blastp_3PRH and chain A and name cb, resid 233 and blastp_3PRH and chain A and name cb
dist intra_4850_valid , resid 202 and blastp_3PRH and chain A and name cb, resid 217 and blastp_3PRH and chain A and name cb
dist intra_4850_4_valid , resid 202 and blastp_3PRH and chain B and name cb, resid 217 and blastp_3PRH and chain B and name cb
dist inter_948_2_valid , resid 314 and blastp_3PRH and chain A and name cb, resid 318 and blastp_3PRH and chain B and name cb
dist inter_948_3_valid , resid 314 and blastp_3PRH and chain B and name cb, resid 318 and blastp_3PRH and chain A and name cb
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
save blastp_3PRH.pse
png blastp_3PRH.png
