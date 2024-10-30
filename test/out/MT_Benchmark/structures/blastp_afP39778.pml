load blastp_afP39778.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP39778
color 3, chain A
show cartoon, chain A
dist intra_4100_valid , resid 246 and blastp_afP39778 and chain A and name cb, resid 122 and blastp_afP39778 and chain A and name cb
dist intra_4552_valid , resid 74 and blastp_afP39778 and chain A and name cb, resid 47 and blastp_afP39778 and chain A and name cb
dist intra_824_out_range , resid 74 and blastp_afP39778 and chain A and name cb, resid 45 and blastp_afP39778 and chain A and name cb
dist intra_4383_out_range , resid 246 and blastp_afP39778 and chain A and name cb, resid 47 and blastp_afP39778 and chain A and name cb
dist intra_1918_unknown , resid 1 and blastp_afP39778 and chain A and name cb, resid 45 and blastp_afP39778 and chain A and name cb
dist intra_3833_unknown , resid 246 and blastp_afP39778 and chain A and name cb, resid 1 and blastp_afP39778 and chain A and name cb
dist intra_4423_unknown , resid 177 and blastp_afP39778 and chain A and name cb, resid 141 and blastp_afP39778 and chain A and name cb
dist intra_5366_unknown , resid 141 and blastp_afP39778 and chain A and name cb, resid 143 and blastp_afP39778 and chain A and name cb
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
save blastp_afP39778.pse
png blastp_afP39778.png
