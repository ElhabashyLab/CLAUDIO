load blastp_afP80859.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP80859
color 3, chain A
show cartoon, chain A
dist intra_1042_valid , resid 38 and blastp_afP80859 and chain A and name cb, resid 75 and blastp_afP80859 and chain A and name cb
dist intra_1268_valid , resid 106 and blastp_afP80859 and chain A and name cb, resid 264 and blastp_afP80859 and chain A and name cb
dist intra_2173_valid , resid 260 and blastp_afP80859 and chain A and name cb, resid 75 and blastp_afP80859 and chain A and name cb
dist intra_3082_valid , resid 106 and blastp_afP80859 and chain A and name cb, resid 113 and blastp_afP80859 and chain A and name cb
dist intra_1846_unknown , resid 469 and blastp_afP80859 and chain A and name cb, resid 241 and blastp_afP80859 and chain A and name cb
dist intra_2406_unknown , resid 136 and blastp_afP80859 and chain A and name cb, resid 469 and blastp_afP80859 and chain A and name cb
dist intra_2478_unknown , resid 241 and blastp_afP80859 and chain A and name cb, resid 460 and blastp_afP80859 and chain A and name cb
dist intra_3991_unknown , resid 70 and blastp_afP80859 and chain A and name cb, resid 260 and blastp_afP80859 and chain A and name cb
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
save blastp_afP80859.pse
png blastp_afP80859.png
