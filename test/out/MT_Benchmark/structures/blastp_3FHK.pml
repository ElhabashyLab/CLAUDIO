load blastp_3FHK.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_3FHK
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain D
show surface, chain D and blastp_3FHK
color 5, chain D
show cartoon, chain D
hide everything, show cartoon, chain E
show surface, chain E and blastp_3FHK
color 7, chain E
show cartoon, chain E
hide everything, show cartoon, chain F
show surface, chain F and blastp_3FHK
color 8, chain F
show cartoon, chain F
dist intra_3763_valid , resid 92 and blastp_3FHK and chain A and name cb, resid 113 and blastp_3FHK and chain A and name cb
dist intra_3763_6_valid , resid 92 and blastp_3FHK and chain D and name cb, resid 113 and blastp_3FHK and chain D and name cb
dist intra_3763_11_valid , resid 92 and blastp_3FHK and chain E and name cb, resid 113 and blastp_3FHK and chain E and name cb
dist intra_3763_16_valid , resid 92 and blastp_3FHK and chain F and name cb, resid 113 and blastp_3FHK and chain F and name cb
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
save blastp_3FHK.pse
png blastp_3FHK.png
