load blastp_3OIC.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_3OIC
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain D
show surface, chain D and blastp_3OIC
color 5, chain D
show cartoon, chain D
dist intra_1052_4_valid , resid 18 and blastp_3OIC and chain D and name cb, resid 193 and blastp_3OIC and chain D and name cb
dist intra_2861_4_valid , resid 40 and blastp_3OIC and chain D and name cb, resid 193 and blastp_3OIC and chain D and name cb
dist intra_3794_valid , resid 40 and blastp_3OIC and chain A and name cb, resid 60 and blastp_3OIC and chain A and name cb
dist intra_3794_4_valid , resid 40 and blastp_3OIC and chain D and name cb, resid 60 and blastp_3OIC and chain D and name cb
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
save blastp_3OIC.pse
png blastp_3OIC.png
