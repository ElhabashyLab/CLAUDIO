load blastp_8CDU.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain C
show surface, chain C and blastp_8CDU
color 3, chain C
show cartoon, chain C
dist intra_2884_valid , resid 75 and blastp_8CDU and chain C and name cb, resid 159 and blastp_8CDU and chain C and name cb
dist intra_4318_valid , resid 158 and blastp_8CDU and chain C and name cb, resid 205 and blastp_8CDU and chain C and name cb
dist intra_6036_valid , resid 534 and blastp_8CDU and chain C and name cb, resid 482 and blastp_8CDU and chain C and name cb
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
save blastp_8CDU.pse
png blastp_8CDU.png
