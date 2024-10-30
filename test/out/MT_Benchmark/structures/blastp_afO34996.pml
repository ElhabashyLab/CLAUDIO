load blastp_afO34996.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO34996
color 3, chain A
show cartoon, chain A
dist intra_854_valid , resid 168 and blastp_afO34996 and chain A and name cb, resid 208 and blastp_afO34996 and chain A and name cb
dist intra_2735_valid , resid 208 and blastp_afO34996 and chain A and name cb, resid 201 and blastp_afO34996 and chain A and name cb
dist intra_3388_valid , resid 205 and blastp_afO34996 and chain A and name cb, resid 231 and blastp_afO34996 and chain A and name cb
dist intra_3718_valid , resid 552 and blastp_afO34996 and chain A and name cb, resid 555 and blastp_afO34996 and chain A and name cb
dist intra_5178_valid , resid 76 and blastp_afO34996 and chain A and name cb, resid 47 and blastp_afO34996 and chain A and name cb
dist intra_6131_valid , resid 552 and blastp_afO34996 and chain A and name cb, resid 536 and blastp_afO34996 and chain A and name cb
dist intra_2530_unknown , resid 154 and blastp_afO34996 and chain A and name cb, resid 170 and blastp_afO34996 and chain A and name cb
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
save blastp_afO34996.pse
png blastp_afO34996.png
