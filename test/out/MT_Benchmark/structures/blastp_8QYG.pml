load blastp_8QYG.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_8QYG
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_8QYG
color 5, chain B
show cartoon, chain B
dist intra_904_valid , resid 127 and blastp_8QYG and chain A and name cb, resid 94 and blastp_8QYG and chain A and name cb
dist intra_904_4_valid , resid 127 and blastp_8QYG and chain B and name cb, resid 94 and blastp_8QYG and chain B and name cb
dist inter_904_2_valid , resid 127 and blastp_8QYG and chain A and name cb, resid 94 and blastp_8QYG and chain B and name cb
dist inter_904_3_valid , resid 127 and blastp_8QYG and chain B and name cb, resid 94 and blastp_8QYG and chain A and name cb
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
save blastp_8QYG.pse
png blastp_8QYG.png