load blastp_4GOT.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_4GOT
color 3, chain A
show cartoon, chain A
dist intra_400_valid , resid 169 and blastp_4GOT and chain A and name cb, resid 182 and blastp_4GOT and chain A and name cb
dist intra_1554_valid , resid 264 and blastp_4GOT and chain A and name cb, resid 39 and blastp_4GOT and chain A and name cb
dist intra_2051_valid , resid 39 and blastp_4GOT and chain A and name cb, resid 63 and blastp_4GOT and chain A and name cb
dist intra_2292_valid , resid 56 and blastp_4GOT and chain A and name cb, resid 246 and blastp_4GOT and chain A and name cb
dist intra_3392_valid , resid 256 and blastp_4GOT and chain A and name cb, resid 225 and blastp_4GOT and chain A and name cb
dist intra_6056_valid , resid 190 and blastp_4GOT and chain A and name cb, resid 39 and blastp_4GOT and chain A and name cb
dist intra_4079_out_range , resid 237 and blastp_4GOT and chain A and name cb, resid 102 and blastp_4GOT and chain A and name cb
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
save blastp_4GOT.pse
png blastp_4GOT.png
