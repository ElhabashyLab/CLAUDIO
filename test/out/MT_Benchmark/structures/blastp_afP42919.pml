load blastp_afP42919.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP42919
color 3, chain A
show cartoon, chain A
dist intra_485_valid , resid 48 and blastp_afP42919 and chain A and name cb, resid 39 and blastp_afP42919 and chain A and name cb
dist intra_1085_valid , resid 147 and blastp_afP42919 and chain A and name cb, resid 170 and blastp_afP42919 and chain A and name cb
dist intra_2351_valid , resid 214 and blastp_afP42919 and chain A and name cb, resid 207 and blastp_afP42919 and chain A and name cb
dist intra_3612_valid , resid 48 and blastp_afP42919 and chain A and name cb, resid 207 and blastp_afP42919 and chain A and name cb
dist intra_3692_valid , resid 39 and blastp_afP42919 and chain A and name cb, resid 207 and blastp_afP42919 and chain A and name cb
dist intra_4822_valid , resid 170 and blastp_afP42919 and chain A and name cb, resid 268 and blastp_afP42919 and chain A and name cb
dist intra_6034_valid , resid 48 and blastp_afP42919 and chain A and name cb, resid 214 and blastp_afP42919 and chain A and name cb
dist intra_1828_out_range , resid 101 and blastp_afP42919 and chain A and name cb, resid 207 and blastp_afP42919 and chain A and name cb
dist intra_3293_out_range , resid 48 and blastp_afP42919 and chain A and name cb, resid 101 and blastp_afP42919 and chain A and name cb
dist intra_4549_unknown , resid 147 and blastp_afP42919 and chain A and name cb, resid 168 and blastp_afP42919 and chain A and name cb
dist intra_5225_unknown , resid 126 and blastp_afP42919 and chain A and name cb, resid 170 and blastp_afP42919 and chain A and name cb
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
save blastp_afP42919.pse
png blastp_afP42919.png
