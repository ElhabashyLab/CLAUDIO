load blastp_3GFG.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_3GFG
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_3GFG
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain C
show surface, chain C and blastp_3GFG
color 7, chain C
show cartoon, chain C
hide everything, show cartoon, chain D
show surface, chain D and blastp_3GFG
color 8, chain D
show cartoon, chain D
hide everything, show cartoon, chain E
show surface, chain E and blastp_3GFG
color 9, chain E
show cartoon, chain E
hide everything, show cartoon, chain F
show surface, chain F and blastp_3GFG
color 10, chain F
show cartoon, chain F
hide everything, show cartoon, chain G
show surface, chain G and blastp_3GFG
color 11, chain G
show cartoon, chain G
hide everything, show cartoon, chain H
show surface, chain H and blastp_3GFG
color 12, chain H
show cartoon, chain H
hide everything, show cartoon, chain I
show surface, chain I and blastp_3GFG
color 14, chain I
show cartoon, chain I
hide everything, show cartoon, chain J
show surface, chain J and blastp_3GFG
color 15, chain J
show cartoon, chain J
hide everything, show cartoon, chain K
show surface, chain K and blastp_3GFG
color 16, chain K
show cartoon, chain K
hide everything, show cartoon, chain L
show surface, chain L and blastp_3GFG
color 17, chain L
show cartoon, chain L
dist intra_982_valid , resid 316 and blastp_3GFG and chain A and name cb, resid 143 and blastp_3GFG and chain A and name cb
dist intra_982_14_valid , resid 316 and blastp_3GFG and chain B and name cb, resid 143 and blastp_3GFG and chain B and name cb
dist intra_982_27_valid , resid 316 and blastp_3GFG and chain C and name cb, resid 143 and blastp_3GFG and chain C and name cb
dist intra_982_40_valid , resid 316 and blastp_3GFG and chain D and name cb, resid 143 and blastp_3GFG and chain D and name cb
dist intra_982_53_valid , resid 316 and blastp_3GFG and chain E and name cb, resid 143 and blastp_3GFG and chain E and name cb
dist intra_982_66_valid , resid 316 and blastp_3GFG and chain F and name cb, resid 143 and blastp_3GFG and chain F and name cb
dist intra_982_79_valid , resid 316 and blastp_3GFG and chain G and name cb, resid 143 and blastp_3GFG and chain G and name cb
dist intra_982_92_valid , resid 316 and blastp_3GFG and chain H and name cb, resid 143 and blastp_3GFG and chain H and name cb
dist intra_982_105_valid , resid 316 and blastp_3GFG and chain I and name cb, resid 143 and blastp_3GFG and chain I and name cb
dist intra_982_118_valid , resid 316 and blastp_3GFG and chain J and name cb, resid 143 and blastp_3GFG and chain J and name cb
dist intra_982_131_valid , resid 316 and blastp_3GFG and chain K and name cb, resid 143 and blastp_3GFG and chain K and name cb
dist intra_982_144_valid , resid 316 and blastp_3GFG and chain L and name cb, resid 143 and blastp_3GFG and chain L and name cb
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
save blastp_3GFG.pse
png blastp_3GFG.png
