load blastp_3F7J.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_3F7J
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_3F7J
color 5, chain B
show cartoon, chain B
dist intra_2032_valid , resid 42 and blastp_3F7J and chain A and name cb, resid 6 and blastp_3F7J and chain A and name cb
dist intra_2032_4_valid , resid 42 and blastp_3F7J and chain B and name cb, resid 6 and blastp_3F7J and chain B and name cb
dist intra_3064_valid , resid 128 and blastp_3F7J and chain A and name cb, resid 134 and blastp_3F7J and chain A and name cb
dist intra_3064_4_valid , resid 128 and blastp_3F7J and chain B and name cb, resid 134 and blastp_3F7J and chain B and name cb
dist intra_4084_valid , resid 26 and blastp_3F7J and chain A and name cb, resid 232 and blastp_3F7J and chain A and name cb
dist intra_4084_4_valid , resid 26 and blastp_3F7J and chain B and name cb, resid 232 and blastp_3F7J and chain B and name cb
dist inter_4084_2_valid , resid 26 and blastp_3F7J and chain A and name cb, resid 232 and blastp_3F7J and chain B and name cb
dist inter_4084_3_valid , resid 26 and blastp_3F7J and chain B and name cb, resid 232 and blastp_3F7J and chain A and name cb
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
save blastp_3F7J.pse
png blastp_3F7J.png
