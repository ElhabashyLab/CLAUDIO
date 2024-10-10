load blastp_8ARE.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_8ARE
color 3, chain A
show cartoon, chain A
dist intra_692_valid , resid 350 and blastp_8ARE and chain A and name cb, resid 364 and blastp_8ARE and chain A and name cb
dist intra_852_valid , resid 290 and blastp_8ARE and chain A and name cb, resid 372 and blastp_8ARE and chain A and name cb
dist intra_3341_valid , resid 370 and blastp_8ARE and chain A and name cb, resid 290 and blastp_8ARE and chain A and name cb
dist intra_3864_valid , resid 267 and blastp_8ARE and chain A and name cb, resid 337 and blastp_8ARE and chain A and name cb
dist intra_1356_out_range , resid 242 and blastp_8ARE and chain A and name cb, resid 337 and blastp_8ARE and chain A and name cb
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
save blastp_8ARE.pse
png blastp_8ARE.png
