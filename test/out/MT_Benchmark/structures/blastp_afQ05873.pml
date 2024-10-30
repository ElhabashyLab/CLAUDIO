load blastp_afQ05873.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afQ05873
color 3, chain A
show cartoon, chain A
dist intra_305_valid , resid 848 and blastp_afQ05873 and chain A and name cb, resid 839 and blastp_afQ05873 and chain A and name cb
dist intra_518_valid , resid 157 and blastp_afQ05873 and chain A and name cb, resid 165 and blastp_afQ05873 and chain A and name cb
dist intra_609_valid , resid 96 and blastp_afQ05873 and chain A and name cb, resid 528 and blastp_afQ05873 and chain A and name cb
dist intra_1649_valid , resid 115 and blastp_afQ05873 and chain A and name cb, resid 106 and blastp_afQ05873 and chain A and name cb
dist intra_2431_valid , resid 831 and blastp_afQ05873 and chain A and name cb, resid 824 and blastp_afQ05873 and chain A and name cb
dist intra_3800_valid , resid 828 and blastp_afQ05873 and chain A and name cb, resid 867 and blastp_afQ05873 and chain A and name cb
dist intra_5715_valid , resid 839 and blastp_afQ05873 and chain A and name cb, resid 831 and blastp_afQ05873 and chain A and name cb
dist intra_1072_unknown , resid 19 and blastp_afQ05873 and chain A and name cb, resid 1 and blastp_afQ05873 and chain A and name cb
dist intra_1923_unknown , resid 1 and blastp_afQ05873 and chain A and name cb, resid 542 and blastp_afQ05873 and chain A and name cb
dist intra_4004_unknown , resid 27 and blastp_afQ05873 and chain A and name cb, resid 1 and blastp_afQ05873 and chain A and name cb
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
save blastp_afQ05873.pse
png blastp_afQ05873.png
