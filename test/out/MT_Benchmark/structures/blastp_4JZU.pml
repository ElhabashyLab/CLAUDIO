load blastp_4JZU.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_4JZU
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_4JZU
color 5, chain B
show cartoon, chain B
dist intra_5171_valid , resid 109 and blastp_4JZU and chain A and name cb, resid 37 and blastp_4JZU and chain A and name cb
dist intra_5171_4_valid , resid 109 and blastp_4JZU and chain B and name cb, resid 37 and blastp_4JZU and chain B and name cb
dist inter_5171_2_valid , resid 109 and blastp_4JZU and chain A and name cb, resid 37 and blastp_4JZU and chain B and name cb
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
save blastp_4JZU.pse
png blastp_4JZU.png
