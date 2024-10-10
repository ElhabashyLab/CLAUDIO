load blastp_1PYF.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_1PYF
color 3, chain A
show cartoon, chain A
dist intra_513_valid , resid 105 and blastp_1PYF and chain A and name cb, resid 89 and blastp_1PYF and chain A and name cb
dist intra_1239_valid , resid 247 and blastp_1PYF and chain A and name cb, resid 307 and blastp_1PYF and chain A and name cb
dist intra_5177_valid , resid 239 and blastp_1PYF and chain A and name cb, resid 247 and blastp_1PYF and chain A and name cb
dist intra_5213_valid , resid 112 and blastp_1PYF and chain A and name cb, resid 89 and blastp_1PYF and chain A and name cb
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
save blastp_1PYF.pse
png blastp_1PYF.png
