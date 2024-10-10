load blastp_7OJR.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_7OJR
color 3, chain A
show cartoon, chain A
dist intra_670_valid , resid 425 and blastp_7OJR and chain A and name cb, resid 368 and blastp_7OJR and chain A and name cb
dist intra_877_valid , resid 3 and blastp_7OJR and chain A and name cb, resid 25 and blastp_7OJR and chain A and name cb
dist intra_1386_valid , resid 296 and blastp_7OJR and chain A and name cb, resid 425 and blastp_7OJR and chain A and name cb
dist intra_1876_valid , resid 158 and blastp_7OJR and chain A and name cb, resid 38 and blastp_7OJR and chain A and name cb
dist intra_1881_valid , resid 270 and blastp_7OJR and chain A and name cb, resid 300 and blastp_7OJR and chain A and name cb
dist intra_2988_valid , resid 425 and blastp_7OJR and chain A and name cb, resid 292 and blastp_7OJR and chain A and name cb
dist intra_3975_valid , resid 425 and blastp_7OJR and chain A and name cb, resid 366 and blastp_7OJR and chain A and name cb
dist intra_4573_valid , resid 296 and blastp_7OJR and chain A and name cb, resid 357 and blastp_7OJR and chain A and name cb
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
save blastp_7OJR.pse
png blastp_7OJR.png
