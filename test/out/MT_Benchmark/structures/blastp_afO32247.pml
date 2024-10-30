load blastp_afO32247.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO32247
color 3, chain A
show cartoon, chain A
dist intra_330_valid , resid 539 and blastp_afO32247 and chain A and name cb, resid 576 and blastp_afO32247 and chain A and name cb
dist intra_619_valid , resid 227 and blastp_afO32247 and chain A and name cb, resid 196 and blastp_afO32247 and chain A and name cb
dist intra_723_valid , resid 188 and blastp_afO32247 and chain A and name cb, resid 196 and blastp_afO32247 and chain A and name cb
dist intra_3165_valid , resid 378 and blastp_afO32247 and chain A and name cb, resid 421 and blastp_afO32247 and chain A and name cb
dist intra_4581_valid , resid 227 and blastp_afO32247 and chain A and name cb, resid 188 and blastp_afO32247 and chain A and name cb
dist intra_4601_valid , resid 119 and blastp_afO32247 and chain A and name cb, resid 188 and blastp_afO32247 and chain A and name cb
dist intra_5453_valid , resid 227 and blastp_afO32247 and chain A and name cb, resid 216 and blastp_afO32247 and chain A and name cb
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
save blastp_afO32247.pse
png blastp_afO32247.png
