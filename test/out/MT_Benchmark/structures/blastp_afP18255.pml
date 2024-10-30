load blastp_afP18255.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP18255
color 3, chain A
show cartoon, chain A
dist intra_867_valid , resid 36 and blastp_afP18255 and chain A and name cb, resid 227 and blastp_afP18255 and chain A and name cb
dist intra_991_valid , resid 194 and blastp_afP18255 and chain A and name cb, resid 35 and blastp_afP18255 and chain A and name cb
dist intra_1610_valid , resid 261 and blastp_afP18255 and chain A and name cb, resid 213 and blastp_afP18255 and chain A and name cb
dist intra_2787_valid , resid 19 and blastp_afP18255 and chain A and name cb, resid 6 and blastp_afP18255 and chain A and name cb
dist intra_3686_valid , resid 129 and blastp_afP18255 and chain A and name cb, resid 91 and blastp_afP18255 and chain A and name cb
dist intra_4294_valid , resid 91 and blastp_afP18255 and chain A and name cb, resid 87 and blastp_afP18255 and chain A and name cb
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
save blastp_afP18255.pse
png blastp_afP18255.png
