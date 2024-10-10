load blastp_5VH6.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_5VH6
color 3, chain A
show cartoon, chain A
dist intra_425_valid , resid 263 and blastp_5VH6 and chain A and name cb, resid 136 and blastp_5VH6 and chain A and name cb
dist intra_1722_valid , resid 263 and blastp_5VH6 and chain A and name cb, resid 137 and blastp_5VH6 and chain A and name cb
dist intra_1798_valid , resid 9 and blastp_5VH6 and chain A and name cb, resid 73 and blastp_5VH6 and chain A and name cb
dist intra_2037_valid , resid 139 and blastp_5VH6 and chain A and name cb, resid 263 and blastp_5VH6 and chain A and name cb
dist intra_3903_valid , resid 136 and blastp_5VH6 and chain A and name cb, resid 23 and blastp_5VH6 and chain A and name cb
dist intra_4530_valid , resid 263 and blastp_5VH6 and chain A and name cb, resid 23 and blastp_5VH6 and chain A and name cb
dist intra_213_out_range , resid 139 and blastp_5VH6 and chain A and name cb, resid 246 and blastp_5VH6 and chain A and name cb
dist intra_2413_out_range , resid 136 and blastp_5VH6 and chain A and name cb, resid 246 and blastp_5VH6 and chain A and name cb
dist intra_4259_out_range , resid 341 and blastp_5VH6 and chain A and name cb, resid 314 and blastp_5VH6 and chain A and name cb
dist intra_3765_unknown , resid 197 and blastp_5VH6 and chain A and name cb, resid 341 and blastp_5VH6 and chain A and name cb
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
save blastp_5VH6.pse
png blastp_5VH6.png
