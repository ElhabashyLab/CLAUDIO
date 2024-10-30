load blastp_afP21881.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP21881
color 3, chain A
show cartoon, chain A
dist intra_920_valid , resid 21 and blastp_afP21881 and chain A and name cb, resid 7 and blastp_afP21881 and chain A and name cb
dist intra_963_valid , resid 7 and blastp_afP21881 and chain A and name cb, resid 14 and blastp_afP21881 and chain A and name cb
dist intra_1515_valid , resid 283 and blastp_afP21881 and chain A and name cb, resid 325 and blastp_afP21881 and chain A and name cb
dist intra_1901_valid , resid 283 and blastp_afP21881 and chain A and name cb, resid 287 and blastp_afP21881 and chain A and name cb
dist intra_2731_valid , resid 21 and blastp_afP21881 and chain A and name cb, resid 13 and blastp_afP21881 and chain A and name cb
dist intra_2858_valid , resid 340 and blastp_afP21881 and chain A and name cb, resid 325 and blastp_afP21881 and chain A and name cb
dist intra_3330_valid , resid 287 and blastp_afP21881 and chain A and name cb, resid 325 and blastp_afP21881 and chain A and name cb
dist intra_3946_valid , resid 13 and blastp_afP21881 and chain A and name cb, resid 215 and blastp_afP21881 and chain A and name cb
dist intra_4980_valid , resid 334 and blastp_afP21881 and chain A and name cb, resid 325 and blastp_afP21881 and chain A and name cb
dist intra_5176_valid , resid 7 and blastp_afP21881 and chain A and name cb, resid 20 and blastp_afP21881 and chain A and name cb
dist intra_6054_valid , resid 283 and blastp_afP21881 and chain A and name cb, resid 215 and blastp_afP21881 and chain A and name cb
dist intra_6055_valid , resid 13 and blastp_afP21881 and chain A and name cb, resid 20 and blastp_afP21881 and chain A and name cb
dist intra_310_overlaps , resid 21 and blastp_afP21881 and chain A and name cb, resid 14 and blastp_afP21881 and chain A and name cb
dist intra_3895_overlaps , resid 334 and blastp_afP21881 and chain A and name cb, resid 333 and blastp_afP21881 and chain A and name cb
dist intra_4160_overlaps , resid 7 and blastp_afP21881 and chain A and name cb, resid 15 and blastp_afP21881 and chain A and name cb
dist intra_5026_overlaps , resid 340 and blastp_afP21881 and chain A and name cb, resid 334 and blastp_afP21881 and chain A and name cb
dist intra_1048_same , resid 334 and blastp_afP21881 and chain A and name cb, resid 334 and blastp_afP21881 and chain A and name cb
dist intra_1598_same , resid 21 and blastp_afP21881 and chain A and name cb, resid 21 and blastp_afP21881 and chain A and name cb
dist intra_2375_unknown , resid 287 and blastp_afP21881 and chain A and name cb, resid 271 and blastp_afP21881 and chain A and name cb
dist intra_3581_unknown , resid 13 and blastp_afP21881 and chain A and name cb, resid 15 and blastp_afP21881 and chain A and name cb
dist intra_3910_unknown , resid 309 and blastp_afP21881 and chain A and name cb, resid 4 and blastp_afP21881 and chain A and name cb
dist intra_3939_unknown , resid 7 and blastp_afP21881 and chain A and name cb, resid 4 and blastp_afP21881 and chain A and name cb
dist intra_4624_unknown , resid 4 and blastp_afP21881 and chain A and name cb, resid 14 and blastp_afP21881 and chain A and name cb
dist intra_4710_unknown , resid 4 and blastp_afP21881 and chain A and name cb, resid 325 and blastp_afP21881 and chain A and name cb
dist intra_5721_unknown , resid 215 and blastp_afP21881 and chain A and name cb, resid 271 and blastp_afP21881 and chain A and name cb
dist intra_5998_unknown , resid 325 and blastp_afP21881 and chain A and name cb, resid 271 and blastp_afP21881 and chain A and name cb
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
save blastp_afP21881.pse
png blastp_afP21881.png
