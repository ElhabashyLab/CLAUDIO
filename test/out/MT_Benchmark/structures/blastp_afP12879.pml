load blastp_afP12879.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP12879
color 3, chain A
show cartoon, chain A
dist intra_1058_valid , resid 65 and blastp_afP12879 and chain A and name cb, resid 41 and blastp_afP12879 and chain A and name cb
dist intra_2806_valid , resid 78 and blastp_afP12879 and chain A and name cb, resid 82 and blastp_afP12879 and chain A and name cb
dist intra_4789_valid , resid 56 and blastp_afP12879 and chain A and name cb, resid 31 and blastp_afP12879 and chain A and name cb
dist intra_1426_unknown , resid 35 and blastp_afP12879 and chain A and name cb, resid 65 and blastp_afP12879 and chain A and name cb
dist intra_2659_unknown , resid 1 and blastp_afP12879 and chain A and name cb, resid 56 and blastp_afP12879 and chain A and name cb
dist intra_4106_unknown , resid 1 and blastp_afP12879 and chain A and name cb, resid 82 and blastp_afP12879 and chain A and name cb
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
save blastp_afP12879.pse
png blastp_afP12879.png
