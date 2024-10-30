load blastp_afP68575.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP68575
color 3, chain A
show cartoon, chain A
dist intra_809_valid , resid 80 and blastp_afP68575 and chain A and name cb, resid 73 and blastp_afP68575 and chain A and name cb
dist intra_1521_valid , resid 91 and blastp_afP68575 and chain A and name cb, resid 80 and blastp_afP68575 and chain A and name cb
dist intra_2397_valid , resid 91 and blastp_afP68575 and chain A and name cb, resid 73 and blastp_afP68575 and chain A and name cb
dist intra_1784_unknown , resid 78 and blastp_afP68575 and chain A and name cb, resid 73 and blastp_afP68575 and chain A and name cb
dist intra_2378_unknown , resid 66 and blastp_afP68575 and chain A and name cb, resid 78 and blastp_afP68575 and chain A and name cb
dist intra_5947_unknown , resid 66 and blastp_afP68575 and chain A and name cb, resid 91 and blastp_afP68575 and chain A and name cb
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
save blastp_afP68575.pse
png blastp_afP68575.png
