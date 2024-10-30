load blastp_afP18159.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP18159
color 3, chain A
show cartoon, chain A
dist intra_201_valid , resid 502 and blastp_afP18159 and chain A and name cb, resid 518 and blastp_afP18159 and chain A and name cb
dist intra_438_valid , resid 243 and blastp_afP18159 and chain A and name cb, resid 209 and blastp_afP18159 and chain A and name cb
dist intra_881_valid , resid 559 and blastp_afP18159 and chain A and name cb, resid 490 and blastp_afP18159 and chain A and name cb
dist intra_1977_valid , resid 559 and blastp_afP18159 and chain A and name cb, resid 487 and blastp_afP18159 and chain A and name cb
dist intra_4578_valid , resid 255 and blastp_afP18159 and chain A and name cb, resid 243 and blastp_afP18159 and chain A and name cb
dist intra_4661_valid , resid 84 and blastp_afP18159 and chain A and name cb, resid 197 and blastp_afP18159 and chain A and name cb
dist intra_708_unknown , resid 491 and blastp_afP18159 and chain A and name cb, resid 518 and blastp_afP18159 and chain A and name cb
dist intra_2454_unknown , resid 502 and blastp_afP18159 and chain A and name cb, resid 504 and blastp_afP18159 and chain A and name cb
dist intra_2985_unknown , resid 459 and blastp_afP18159 and chain A and name cb, resid 581 and blastp_afP18159 and chain A and name cb
dist intra_3575_unknown , resid 197 and blastp_afP18159 and chain A and name cb, resid 79 and blastp_afP18159 and chain A and name cb
dist intra_3970_unknown , resid 491 and blastp_afP18159 and chain A and name cb, resid 504 and blastp_afP18159 and chain A and name cb
dist intra_4150_unknown , resid 502 and blastp_afP18159 and chain A and name cb, resid 511 and blastp_afP18159 and chain A and name cb
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
save blastp_afP18159.pse
png blastp_afP18159.png
