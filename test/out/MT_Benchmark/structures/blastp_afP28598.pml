load blastp_afP28598.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP28598
color 3, chain A
show cartoon, chain A
dist intra_84_valid , resid 369 and blastp_afP28598 and chain A and name cb, resid 362 and blastp_afP28598 and chain A and name cb
dist intra_332_valid , resid 42 and blastp_afP28598 and chain A and name cb, resid 388 and blastp_afP28598 and chain A and name cb
dist intra_402_valid , resid 41 and blastp_afP28598 and chain A and name cb, resid 388 and blastp_afP28598 and chain A and name cb
dist intra_568_valid , resid 325 and blastp_afP28598 and chain A and name cb, resid 275 and blastp_afP28598 and chain A and name cb
dist intra_1143_valid , resid 131 and blastp_afP28598 and chain A and name cb, resid 495 and blastp_afP28598 and chain A and name cb
dist intra_1425_valid , resid 208 and blastp_afP28598 and chain A and name cb, resid 320 and blastp_afP28598 and chain A and name cb
dist intra_1618_valid , resid 179 and blastp_afP28598 and chain A and name cb, resid 320 and blastp_afP28598 and chain A and name cb
dist intra_1910_valid , resid 33 and blastp_afP28598 and chain A and name cb, resid 41 and blastp_afP28598 and chain A and name cb
dist intra_2132_valid , resid 325 and blastp_afP28598 and chain A and name cb, resid 495 and blastp_afP28598 and chain A and name cb
dist intra_2206_valid , resid 33 and blastp_afP28598 and chain A and name cb, resid 104 and blastp_afP28598 and chain A and name cb
dist intra_2643_valid , resid 388 and blastp_afP28598 and chain A and name cb, resid 57 and blastp_afP28598 and chain A and name cb
dist intra_3125_valid , resid 325 and blastp_afP28598 and chain A and name cb, resid 362 and blastp_afP28598 and chain A and name cb
dist intra_621_out_range , resid 117 and blastp_afP28598 and chain A and name cb, resid 33 and blastp_afP28598 and chain A and name cb
dist intra_1519_out_range , resid 388 and blastp_afP28598 and chain A and name cb, resid 275 and blastp_afP28598 and chain A and name cb
dist intra_5906_out_range , resid 33 and blastp_afP28598 and chain A and name cb, resid 42 and blastp_afP28598 and chain A and name cb
dist intra_1015_unknown , resid 369 and blastp_afP28598 and chain A and name cb, resid 349 and blastp_afP28598 and chain A and name cb
dist intra_1175_unknown , resid 36 and blastp_afP28598 and chain A and name cb, resid 388 and blastp_afP28598 and chain A and name cb
dist intra_1360_unknown , resid 379 and blastp_afP28598 and chain A and name cb, resid 41 and blastp_afP28598 and chain A and name cb
dist intra_2501_unknown , resid 42 and blastp_afP28598 and chain A and name cb, resid 379 and blastp_afP28598 and chain A and name cb
dist intra_3790_unknown , resid 36 and blastp_afP28598 and chain A and name cb, resid 379 and blastp_afP28598 and chain A and name cb
dist intra_3797_unknown , resid 379 and blastp_afP28598 and chain A and name cb, resid 275 and blastp_afP28598 and chain A and name cb
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
save blastp_afP28598.pse
png blastp_afP28598.png
