load blastp_2X7J.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_2X7J
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_2X7J
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain C
show surface, chain C and blastp_2X7J
color 7, chain C
show cartoon, chain C
hide everything, show cartoon, chain D
show surface, chain D and blastp_2X7J
color 8, chain D
show cartoon, chain D
dist intra_3723_valid , resid 283 and blastp_2X7J and chain A and name cb, resid 360 and blastp_2X7J and chain A and name cb
dist intra_3723_6_valid , resid 283 and blastp_2X7J and chain B and name cb, resid 360 and blastp_2X7J and chain B and name cb
dist intra_3723_11_valid , resid 283 and blastp_2X7J and chain C and name cb, resid 360 and blastp_2X7J and chain C and name cb
dist intra_3723_16_valid , resid 283 and blastp_2X7J and chain D and name cb, resid 360 and blastp_2X7J and chain D and name cb
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
save blastp_2X7J.pse
png blastp_2X7J.png