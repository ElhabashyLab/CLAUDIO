load blastp_afP37437.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP37437
color 3, chain A
show cartoon, chain A
dist intra_494_valid , resid 132 and blastp_afP37437 and chain A and name cb, resid 114 and blastp_afP37437 and chain A and name cb
dist intra_659_valid , resid 114 and blastp_afP37437 and chain A and name cb, resid 56 and blastp_afP37437 and chain A and name cb
dist intra_806_valid , resid 10 and blastp_afP37437 and chain A and name cb, resid 14 and blastp_afP37437 and chain A and name cb
dist intra_1208_valid , resid 109 and blastp_afP37437 and chain A and name cb, resid 96 and blastp_afP37437 and chain A and name cb
dist intra_1520_valid , resid 114 and blastp_afP37437 and chain A and name cb, resid 109 and blastp_afP37437 and chain A and name cb
dist intra_1595_valid , resid 1 and blastp_afP37437 and chain A and name cb, resid 19 and blastp_afP37437 and chain A and name cb
dist intra_2278_valid , resid 51 and blastp_afP37437 and chain A and name cb, resid 1 and blastp_afP37437 and chain A and name cb
dist intra_3176_valid , resid 132 and blastp_afP37437 and chain A and name cb, resid 10 and blastp_afP37437 and chain A and name cb
dist intra_3239_valid , resid 15 and blastp_afP37437 and chain A and name cb, resid 1 and blastp_afP37437 and chain A and name cb
dist intra_3870_valid , resid 114 and blastp_afP37437 and chain A and name cb, resid 10 and blastp_afP37437 and chain A and name cb
dist intra_4632_valid , resid 33 and blastp_afP37437 and chain A and name cb, resid 1 and blastp_afP37437 and chain A and name cb
dist intra_5008_valid , resid 146 and blastp_afP37437 and chain A and name cb, resid 104 and blastp_afP37437 and chain A and name cb
dist intra_3989_out_range , resid 114 and blastp_afP37437 and chain A and name cb, resid 1 and blastp_afP37437 and chain A and name cb
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
save blastp_afP37437.pse
png blastp_afP37437.png
