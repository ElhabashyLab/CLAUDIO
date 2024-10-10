load blastp_7SAE.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain R
show surface, chain R and blastp_7SAE
color 3, chain R
show cartoon, chain R
dist intra_1001_valid , resid 99 and blastp_7SAE and chain R and name cb, resid 61 and blastp_7SAE and chain R and name cb
dist intra_5807_valid , resid 94 and blastp_7SAE and chain R and name cb, resid 61 and blastp_7SAE and chain R and name cb
dist intra_2529_out_range , resid 94 and blastp_7SAE and chain R and name cb, resid 64 and blastp_7SAE and chain R and name cb
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
save blastp_7SAE.pse
png blastp_7SAE.png
