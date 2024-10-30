load blastp_afP17889.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP17889
color 3, chain A
show cartoon, chain A
dist intra_2553_valid , resid 636 and blastp_afP17889 and chain A and name cb, resid 677 and blastp_afP17889 and chain A and name cb
dist intra_3451_valid , resid 695 and blastp_afP17889 and chain A and name cb, resid 636 and blastp_afP17889 and chain A and name cb
dist intra_5390_valid , resid 488 and blastp_afP17889 and chain A and name cb, resid 394 and blastp_afP17889 and chain A and name cb
dist intra_4000_unknown , resid 695 and blastp_afP17889 and chain A and name cb, resid 510 and blastp_afP17889 and chain A and name cb
dist intra_4018_unknown , resid 69 and blastp_afP17889 and chain A and name cb, resid 61 and blastp_afP17889 and chain A and name cb
dist intra_4036_unknown , resid 510 and blastp_afP17889 and chain A and name cb, resid 545 and blastp_afP17889 and chain A and name cb
dist intra_4269_unknown , resid 510 and blastp_afP17889 and chain A and name cb, resid 539 and blastp_afP17889 and chain A and name cb
dist intra_6101_unknown , resid 70 and blastp_afP17889 and chain A and name cb, resid 67 and blastp_afP17889 and chain A and name cb
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
save blastp_afP17889.pse
png blastp_afP17889.png
