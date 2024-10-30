load blastp_1TO0.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_1TO0
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_1TO0
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain C
show surface, chain C and blastp_1TO0
color 7, chain C
show cartoon, chain C
hide everything, show cartoon, chain D
show surface, chain D and blastp_1TO0
color 8, chain D
show cartoon, chain D
hide everything, show cartoon, chain E
show surface, chain E and blastp_1TO0
color 9, chain E
show cartoon, chain E
hide everything, show cartoon, chain F
show surface, chain F and blastp_1TO0
color 10, chain F
show cartoon, chain F
hide everything, show cartoon, chain G
show surface, chain G and blastp_1TO0
color 11, chain G
show cartoon, chain G
hide everything, show cartoon, chain H
show surface, chain H and blastp_1TO0
color 12, chain H
show cartoon, chain H
dist intra_3025_unknown , resid 1 and blastp_1TO0 and chain A and name cb, resid 66 and blastp_1TO0 and chain A and name cb
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
save blastp_1TO0.pse
png blastp_1TO0.png
