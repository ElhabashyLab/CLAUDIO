load blastp_6GOW.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain D
show surface, chain D and blastp_6GOW
color 3, chain D
show cartoon, chain D
dist intra_2498_valid , resid 136 and blastp_6GOW and chain D and name cb, resid 153 and blastp_6GOW and chain D and name cb
dist intra_223_out_range , resid 219 and blastp_6GOW and chain D and name cb, resid 136 and blastp_6GOW and chain D and name cb
dist intra_2205_out_range , resid 136 and blastp_6GOW and chain D and name cb, resid 51 and blastp_6GOW and chain D and name cb
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
save blastp_6GOW.pse
png blastp_6GOW.png
