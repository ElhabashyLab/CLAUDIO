load blastp_afQ02114.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afQ02114
color 3, chain A
show cartoon, chain A
dist intra_1493_valid , resid 356 and blastp_afQ02114 and chain A and name cb, resid 482 and blastp_afQ02114 and chain A and name cb
dist intra_2382_valid , resid 92 and blastp_afQ02114 and chain A and name cb, resid 96 and blastp_afQ02114 and chain A and name cb
dist intra_3560_valid , resid 128 and blastp_afQ02114 and chain A and name cb, resid 144 and blastp_afQ02114 and chain A and name cb
dist intra_4130_valid , resid 144 and blastp_afQ02114 and chain A and name cb, resid 194 and blastp_afQ02114 and chain A and name cb
dist intra_5072_unknown , resid 95 and blastp_afQ02114 and chain A and name cb, resid 92 and blastp_afQ02114 and chain A and name cb
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
save blastp_afQ02114.pse
png blastp_afQ02114.png
