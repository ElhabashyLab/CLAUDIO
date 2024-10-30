load blastp_afP39596.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP39596
color 3, chain A
show cartoon, chain A
dist intra_531_valid , resid 253 and blastp_afP39596 and chain A and name cb, resid 224 and blastp_afP39596 and chain A and name cb
dist intra_1106_valid , resid 190 and blastp_afP39596 and chain A and name cb, resid 183 and blastp_afP39596 and chain A and name cb
dist intra_1967_valid , resid 190 and blastp_afP39596 and chain A and name cb, resid 347 and blastp_afP39596 and chain A and name cb
dist intra_3583_valid , resid 358 and blastp_afP39596 and chain A and name cb, resid 185 and blastp_afP39596 and chain A and name cb
dist intra_4973_unknown , resid 142 and blastp_afP39596 and chain A and name cb, resid 137 and blastp_afP39596 and chain A and name cb
dist intra_5653_unknown , resid 142 and blastp_afP39596 and chain A and name cb, resid 36 and blastp_afP39596 and chain A and name cb
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
save blastp_afP39596.pse
png blastp_afP39596.png
