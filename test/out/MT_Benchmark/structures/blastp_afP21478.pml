load blastp_afP21478.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP21478
color 3, chain A
show cartoon, chain A
dist intra_2855_valid , resid 8 and blastp_afP21478 and chain A and name cb, resid 3 and blastp_afP21478 and chain A and name cb
dist intra_2894_valid , resid 8 and blastp_afP21478 and chain A and name cb, resid 25 and blastp_afP21478 and chain A and name cb
dist intra_3986_valid , resid 44 and blastp_afP21478 and chain A and name cb, resid 25 and blastp_afP21478 and chain A and name cb
dist intra_4006_valid , resid 40 and blastp_afP21478 and chain A and name cb, resid 25 and blastp_afP21478 and chain A and name cb
dist intra_4670_valid , resid 25 and blastp_afP21478 and chain A and name cb, resid 3 and blastp_afP21478 and chain A and name cb
dist intra_6001_valid , resid 40 and blastp_afP21478 and chain A and name cb, resid 48 and blastp_afP21478 and chain A and name cb
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
save blastp_afP21478.pse
png blastp_afP21478.png
