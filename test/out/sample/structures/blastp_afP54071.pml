load blastp_afP54071.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP54071
color 3, chain A
show cartoon, chain A
dist intra_104_valid , resid 451 and blastp_afP54071 and chain A and name cb, resid 400 and blastp_afP54071 and chain A and name cb
show dashes
set dash_gap, 0.1
color blue, intra*_valid
color red, intra*_out_range
color red, intra*_overlaps
color red, intra*_same
color blue, inter*_valid
color red, inter*_out_range
color red, inter*_overlaps
color red, inter*_same
set dash_width, 9
center
save blastp_afP54071.pse
png blastp_afP54071.png