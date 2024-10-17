load blastp_2LXJ.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_2LXJ
color 3, chain A
show cartoon, chain A
dist intra_1197_valid , resid 65 and blastp_2LXJ and chain A and name cb, resid 39 and blastp_2LXJ and chain A and name cb
dist intra_1706_valid , resid 13 and blastp_2LXJ and chain A and name cb, resid 65 and blastp_2LXJ and chain A and name cb
dist intra_2982_valid , resid 65 and blastp_2LXJ and chain A and name cb, resid 1 and blastp_2LXJ and chain A and name cb
dist intra_3052_out_range , resid 13 and blastp_2LXJ and chain A and name cb, resid 1 and blastp_2LXJ and chain A and name cb
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
save blastp_2LXJ.pse
png blastp_2LXJ.png
