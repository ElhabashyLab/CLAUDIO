load blastp_6M36.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain B
show surface, chain B and blastp_6M36
color 3, chain B
show cartoon, chain B
hide everything, show cartoon, chain D
show surface, chain D and blastp_6M36
color 5, chain D
show cartoon, chain D
hide everything, show cartoon, chain F
show surface, chain F and blastp_6M36
color 7, chain F
show cartoon, chain F
hide everything, show cartoon, chain H
show surface, chain H and blastp_6M36
color 8, chain H
show cartoon, chain H
hide everything, show cartoon, chain J
show surface, chain J and blastp_6M36
color 9, chain J
show cartoon, chain J
hide everything, show cartoon, chain L
show surface, chain L and blastp_6M36
color 10, chain L
show cartoon, chain L
hide everything, show cartoon, chain N
show surface, chain N and blastp_6M36
color 11, chain N
show cartoon, chain N
hide everything, show cartoon, chain P
show surface, chain P and blastp_6M36
color 12, chain P
show cartoon, chain P
dist intra_2197_unknown , resid 1 and blastp_6M36 and chain B and name cb, resid 33 and blastp_6M36 and chain B and name cb
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
save blastp_6M36.pse
png blastp_6M36.png
