load blastp_afO05519.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO05519
color 3, chain A
show cartoon, chain A
dist intra_1335_valid , resid 257 and blastp_afO05519 and chain A and name cb, resid 264 and blastp_afO05519 and chain A and name cb
dist intra_3778_valid , resid 239 and blastp_afO05519 and chain A and name cb, resid 23 and blastp_afO05519 and chain A and name cb
dist intra_5958_valid , resid 264 and blastp_afO05519 and chain A and name cb, resid 287 and blastp_afO05519 and chain A and name cb
dist intra_6106_valid , resid 84 and blastp_afO05519 and chain A and name cb, resid 99 and blastp_afO05519 and chain A and name cb
dist intra_5923_unknown , resid 264 and blastp_afO05519 and chain A and name cb, resid 252 and blastp_afO05519 and chain A and name cb
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
save blastp_afO05519.pse
png blastp_afO05519.png
