load blastp_afP36949.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP36949
color 3, chain A
show cartoon, chain A
dist intra_256_valid , resid 188 and blastp_afP36949 and chain A and name cb, resid 143 and blastp_afP36949 and chain A and name cb
dist intra_300_valid , resid 155 and blastp_afP36949 and chain A and name cb, resid 305 and blastp_afP36949 and chain A and name cb
dist intra_493_valid , resid 276 and blastp_afP36949 and chain A and name cb, resid 300 and blastp_afP36949 and chain A and name cb
dist intra_640_valid , resid 132 and blastp_afP36949 and chain A and name cb, resid 290 and blastp_afP36949 and chain A and name cb
dist intra_2247_valid , resid 305 and blastp_afP36949 and chain A and name cb, resid 259 and blastp_afP36949 and chain A and name cb
dist intra_2250_valid , resid 300 and blastp_afP36949 and chain A and name cb, resid 259 and blastp_afP36949 and chain A and name cb
dist intra_2897_valid , resid 132 and blastp_afP36949 and chain A and name cb, resid 293 and blastp_afP36949 and chain A and name cb
dist intra_5412_valid , resid 262 and blastp_afP36949 and chain A and name cb, resid 305 and blastp_afP36949 and chain A and name cb
dist intra_5730_unknown , resid 290 and blastp_afP36949 and chain A and name cb, resid 127 and blastp_afP36949 and chain A and name cb
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
save blastp_afP36949.pse
png blastp_afP36949.png
