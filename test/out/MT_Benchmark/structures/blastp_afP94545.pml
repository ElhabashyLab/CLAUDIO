load blastp_afP94545.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP94545
color 3, chain A
show cartoon, chain A
dist intra_3013_valid , resid 15 and blastp_afP94545 and chain A and name cb, resid 35 and blastp_afP94545 and chain A and name cb
dist intra_4706_valid , resid 685 and blastp_afP94545 and chain A and name cb, resid 653 and blastp_afP94545 and chain A and name cb
dist intra_3719_unknown , resid 581 and blastp_afP94545 and chain A and name cb, resid 613 and blastp_afP94545 and chain A and name cb
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
save blastp_afP94545.pse
png blastp_afP94545.png
