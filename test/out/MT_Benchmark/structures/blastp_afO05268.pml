load blastp_afO05268.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO05268
color 3, chain A
show cartoon, chain A
dist intra_3131_valid , resid 317 and blastp_afO05268 and chain A and name cb, resid 332 and blastp_afO05268 and chain A and name cb
dist intra_5793_out_range , resid 125 and blastp_afO05268 and chain A and name cb, resid 332 and blastp_afO05268 and chain A and name cb
dist intra_71_unknown , resid 63 and blastp_afO05268 and chain A and name cb, resid 332 and blastp_afO05268 and chain A and name cb
dist intra_253_unknown , resid 320 and blastp_afO05268 and chain A and name cb, resid 63 and blastp_afO05268 and chain A and name cb
dist intra_5193_unknown , resid 63 and blastp_afO05268 and chain A and name cb, resid 75 and blastp_afO05268 and chain A and name cb
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
save blastp_afO05268.pse
png blastp_afO05268.png
