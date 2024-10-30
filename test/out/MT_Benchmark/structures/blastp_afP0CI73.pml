load blastp_afP0CI73.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP0CI73
color 3, chain A
show cartoon, chain A
dist intra_59_valid , resid 338 and blastp_afP0CI73 and chain A and name cb, resid 366 and blastp_afP0CI73 and chain A and name cb
dist intra_563_valid , resid 23 and blastp_afP0CI73 and chain A and name cb, resid 254 and blastp_afP0CI73 and chain A and name cb
dist intra_675_valid , resid 265 and blastp_afP0CI73 and chain A and name cb, resid 254 and blastp_afP0CI73 and chain A and name cb
dist intra_927_valid , resid 23 and blastp_afP0CI73 and chain A and name cb, resid 265 and blastp_afP0CI73 and chain A and name cb
dist intra_2790_valid , resid 265 and blastp_afP0CI73 and chain A and name cb, resid 19 and blastp_afP0CI73 and chain A and name cb
dist intra_3030_valid , resid 23 and blastp_afP0CI73 and chain A and name cb, resid 245 and blastp_afP0CI73 and chain A and name cb
dist intra_2321_out_range , resid 530 and blastp_afP0CI73 and chain A and name cb, resid 595 and blastp_afP0CI73 and chain A and name cb
dist intra_2930_unknown , resid 530 and blastp_afP0CI73 and chain A and name cb, resid 109 and blastp_afP0CI73 and chain A and name cb
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
save blastp_afP0CI73.pse
png blastp_afP0CI73.png
