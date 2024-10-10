load blastp_3HXP.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_3HXP
color 3, chain A
show cartoon, chain A
dist intra_1500_valid , resid 231 and blastp_3HXP and chain A and name cb, resid 226 and blastp_3HXP and chain A and name cb
dist intra_2580_valid , resid 46 and blastp_3HXP and chain A and name cb, resid 145 and blastp_3HXP and chain A and name cb
dist intra_3632_valid , resid 95 and blastp_3HXP and chain A and name cb, resid 164 and blastp_3HXP and chain A and name cb
dist intra_4091_valid , resid 175 and blastp_3HXP and chain A and name cb, resid 95 and blastp_3HXP and chain A and name cb
dist intra_5059_valid , resid 226 and blastp_3HXP and chain A and name cb, resid 229 and blastp_3HXP and chain A and name cb
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
save blastp_3HXP.pse
png blastp_3HXP.png
