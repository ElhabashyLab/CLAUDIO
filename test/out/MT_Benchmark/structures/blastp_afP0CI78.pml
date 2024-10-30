load blastp_afP0CI78.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP0CI78
color 3, chain A
show cartoon, chain A
dist intra_45_valid , resid 5 and blastp_afP0CI78 and chain A and name cb, resid 19 and blastp_afP0CI78 and chain A and name cb
dist intra_530_valid , resid 5 and blastp_afP0CI78 and chain A and name cb, resid 96 and blastp_afP0CI78 and chain A and name cb
dist intra_562_valid , resid 42 and blastp_afP0CI78 and chain A and name cb, resid 15 and blastp_afP0CI78 and chain A and name cb
dist intra_1010_valid , resid 42 and blastp_afP0CI78 and chain A and name cb, resid 46 and blastp_afP0CI78 and chain A and name cb
dist intra_1174_valid , resid 84 and blastp_afP0CI78 and chain A and name cb, resid 96 and blastp_afP0CI78 and chain A and name cb
dist intra_1517_valid , resid 19 and blastp_afP0CI78 and chain A and name cb, resid 42 and blastp_afP0CI78 and chain A and name cb
dist intra_2303_valid , resid 96 and blastp_afP0CI78 and chain A and name cb, resid 74 and blastp_afP0CI78 and chain A and name cb
dist intra_2436_valid , resid 19 and blastp_afP0CI78 and chain A and name cb, resid 15 and blastp_afP0CI78 and chain A and name cb
dist intra_3702_valid , resid 19 and blastp_afP0CI78 and chain A and name cb, resid 8 and blastp_afP0CI78 and chain A and name cb
dist intra_3857_valid , resid 15 and blastp_afP0CI78 and chain A and name cb, resid 40 and blastp_afP0CI78 and chain A and name cb
dist intra_1122_unknown , resid 103 and blastp_afP0CI78 and chain A and name cb, resid 5 and blastp_afP0CI78 and chain A and name cb
dist intra_1275_unknown , resid 103 and blastp_afP0CI78 and chain A and name cb, resid 84 and blastp_afP0CI78 and chain A and name cb
dist intra_2392_unknown , resid 103 and blastp_afP0CI78 and chain A and name cb, resid 44 and blastp_afP0CI78 and chain A and name cb
dist intra_3267_unknown , resid 89 and blastp_afP0CI78 and chain A and name cb, resid 103 and blastp_afP0CI78 and chain A and name cb
dist intra_5106_unknown , resid 103 and blastp_afP0CI78 and chain A and name cb, resid 8 and blastp_afP0CI78 and chain A and name cb
dist intra_5293_unknown , resid 42 and blastp_afP0CI78 and chain A and name cb, resid 9 and blastp_afP0CI78 and chain A and name cb
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
save blastp_afP0CI78.pse
png blastp_afP0CI78.png
