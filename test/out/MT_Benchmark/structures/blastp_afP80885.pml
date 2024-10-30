load blastp_afP80885.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP80885
color 3, chain A
show cartoon, chain A
dist intra_345_valid , resid 156 and blastp_afP80885 and chain A and name cb, resid 153 and blastp_afP80885 and chain A and name cb
dist intra_1306_valid , resid 68 and blastp_afP80885 and chain A and name cb, resid 156 and blastp_afP80885 and chain A and name cb
dist intra_2546_valid , resid 498 and blastp_afP80885 and chain A and name cb, resid 513 and blastp_afP80885 and chain A and name cb
dist intra_4007_valid , resid 478 and blastp_afP80885 and chain A and name cb, resid 485 and blastp_afP80885 and chain A and name cb
dist intra_222_out_range , resid 485 and blastp_afP80885 and chain A and name cb, resid 266 and blastp_afP80885 and chain A and name cb
dist intra_4028_overlaps , resid 347 and blastp_afP80885 and chain A and name cb, resid 342 and blastp_afP80885 and chain A and name cb
dist intra_755_unknown , resid 156 and blastp_afP80885 and chain A and name cb, resid 146 and blastp_afP80885 and chain A and name cb
dist intra_827_unknown , resid 267 and blastp_afP80885 and chain A and name cb, resid 485 and blastp_afP80885 and chain A and name cb
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
save blastp_afP80885.pse
png blastp_afP80885.png
