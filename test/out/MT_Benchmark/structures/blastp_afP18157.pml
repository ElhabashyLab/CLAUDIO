load blastp_afP18157.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP18157
color 3, chain A
show cartoon, chain A
dist intra_118_valid , resid 490 and blastp_afP18157 and chain A and name cb, resid 483 and blastp_afP18157 and chain A and name cb
dist intra_1488_valid , resid 217 and blastp_afP18157 and chain A and name cb, resid 176 and blastp_afP18157 and chain A and name cb
dist intra_1718_valid , resid 22 and blastp_afP18157 and chain A and name cb, resid 1 and blastp_afP18157 and chain A and name cb
dist intra_2266_valid , resid 141 and blastp_afP18157 and chain A and name cb, resid 117 and blastp_afP18157 and chain A and name cb
dist intra_2472_valid , resid 176 and blastp_afP18157 and chain A and name cb, resid 90 and blastp_afP18157 and chain A and name cb
dist intra_909_same , resid 490 and blastp_afP18157 and chain A and name cb, resid 490 and blastp_afP18157 and chain A and name cb
dist intra_1328_unknown , resid 211 and blastp_afP18157 and chain A and name cb, resid 176 and blastp_afP18157 and chain A and name cb
dist intra_2399_unknown , resid 211 and blastp_afP18157 and chain A and name cb, resid 172 and blastp_afP18157 and chain A and name cb
dist intra_3116_unknown , resid 490 and blastp_afP18157 and chain A and name cb, resid 478 and blastp_afP18157 and chain A and name cb
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
save blastp_afP18157.pse
png blastp_afP18157.png
