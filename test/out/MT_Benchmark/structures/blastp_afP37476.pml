load blastp_afP37476.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP37476
color 3, chain A
show cartoon, chain A
dist intra_2011_valid , resid 562 and blastp_afP37476 and chain A and name cb, resid 569 and blastp_afP37476 and chain A and name cb
dist intra_3199_valid , resid 341 and blastp_afP37476 and chain A and name cb, resid 161 and blastp_afP37476 and chain A and name cb
dist intra_3252_valid , resid 341 and blastp_afP37476 and chain A and name cb, resid 356 and blastp_afP37476 and chain A and name cb
dist intra_3668_valid , resid 578 and blastp_afP37476 and chain A and name cb, resid 598 and blastp_afP37476 and chain A and name cb
dist intra_3886_valid , resid 48 and blastp_afP37476 and chain A and name cb, resid 95 and blastp_afP37476 and chain A and name cb
dist intra_4047_valid , resid 48 and blastp_afP37476 and chain A and name cb, resid 68 and blastp_afP37476 and chain A and name cb
dist intra_4805_same , resid 84 and blastp_afP37476 and chain A and name cb, resid 84 and blastp_afP37476 and chain A and name cb
dist intra_1708_unknown , resid 627 and blastp_afP37476 and chain A and name cb, resid 632 and blastp_afP37476 and chain A and name cb
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
save blastp_afP37476.pse
png blastp_afP37476.png
