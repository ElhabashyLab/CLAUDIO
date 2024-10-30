load blastp_afP29727.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP29727
color 3, chain A
show cartoon, chain A
dist intra_121_valid , resid 258 and blastp_afP29727 and chain A and name cb, resid 493 and blastp_afP29727 and chain A and name cb
dist intra_2678_valid , resid 369 and blastp_afP29727 and chain A and name cb, resid 505 and blastp_afP29727 and chain A and name cb
dist intra_4020_valid , resid 300 and blastp_afP29727 and chain A and name cb, resid 288 and blastp_afP29727 and chain A and name cb
dist intra_4407_valid , resid 290 and blastp_afP29727 and chain A and name cb, resid 282 and blastp_afP29727 and chain A and name cb
dist intra_5235_valid , resid 258 and blastp_afP29727 and chain A and name cb, resid 282 and blastp_afP29727 and chain A and name cb
dist intra_4699_unknown , resid 345 and blastp_afP29727 and chain A and name cb, resid 505 and blastp_afP29727 and chain A and name cb
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
save blastp_afP29727.pse
png blastp_afP29727.png
