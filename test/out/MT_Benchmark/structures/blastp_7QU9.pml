load blastp_7QU9.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_7QU9
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_7QU9
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain C
show surface, chain C and blastp_7QU9
color 7, chain C
show cartoon, chain C
dist intra_2415_valid , resid 55 and blastp_7QU9 and chain A and name cb, resid 64 and blastp_7QU9 and chain A and name cb
dist intra_2415_5_valid , resid 55 and blastp_7QU9 and chain B and name cb, resid 64 and blastp_7QU9 and chain B and name cb
dist intra_2415_9_valid , resid 55 and blastp_7QU9 and chain C and name cb, resid 64 and blastp_7QU9 and chain C and name cb
dist intra_4023_valid , resid 55 and blastp_7QU9 and chain A and name cb, resid 30 and blastp_7QU9 and chain A and name cb
dist intra_4023_5_valid , resid 55 and blastp_7QU9 and chain B and name cb, resid 30 and blastp_7QU9 and chain B and name cb
dist intra_4023_9_valid , resid 55 and blastp_7QU9 and chain C and name cb, resid 30 and blastp_7QU9 and chain C and name cb
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
save blastp_7QU9.pse
png blastp_7QU9.png
