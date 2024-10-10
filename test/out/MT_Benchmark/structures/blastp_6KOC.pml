load blastp_6KOC.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_6KOC
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain E
show surface, chain E and blastp_6KOC
color 5, chain E
show cartoon, chain E
dist intra_5380_valid , resid 576 and blastp_6KOC and chain A and name cb, resid 556 and blastp_6KOC and chain A and name cb
dist intra_5380_4_valid , resid 576 and blastp_6KOC and chain E and name cb, resid 556 and blastp_6KOC and chain E and name cb
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
save blastp_6KOC.pse
png blastp_6KOC.png
