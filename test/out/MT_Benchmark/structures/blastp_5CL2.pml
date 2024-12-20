load blastp_5CL2.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_5CL2
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_5CL2
color 5, chain B
show cartoon, chain B
dist intra_64_unknown , resid 70 and blastp_5CL2 and chain A and name cb, resid 63 and blastp_5CL2 and chain A and name cb
dist intra_355_unknown , resid 6 and blastp_5CL2 and chain A and name cb, resid 70 and blastp_5CL2 and chain A and name cb
dist intra_1099_unknown , resid 6 and blastp_5CL2 and chain A and name cb, resid 43 and blastp_5CL2 and chain A and name cb
dist intra_1144_unknown , resid 17 and blastp_5CL2 and chain A and name cb, resid 43 and blastp_5CL2 and chain A and name cb
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
save blastp_5CL2.pse
png blastp_5CL2.png
