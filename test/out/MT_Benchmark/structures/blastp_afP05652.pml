load blastp_afP05652.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP05652
color 3, chain A
show cartoon, chain A
dist intra_1102_valid , resid 459 and blastp_afP05652 and chain A and name cb, resid 464 and blastp_afP05652 and chain A and name cb
dist intra_1874_valid , resid 410 and blastp_afP05652 and chain A and name cb, resid 437 and blastp_afP05652 and chain A and name cb
dist intra_5234_valid , resid 464 and blastp_afP05652 and chain A and name cb, resid 453 and blastp_afP05652 and chain A and name cb
dist intra_522_unknown , resid 634 and blastp_afP05652 and chain A and name cb, resid 553 and blastp_afP05652 and chain A and name cb
dist intra_1105_unknown , resid 399 and blastp_afP05652 and chain A and name cb, resid 490 and blastp_afP05652 and chain A and name cb
dist intra_5056_unknown , resid 464 and blastp_afP05652 and chain A and name cb, resid 454 and blastp_afP05652 and chain A and name cb
dist intra_5780_unknown , resid 399 and blastp_afP05652 and chain A and name cb, resid 411 and blastp_afP05652 and chain A and name cb
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
save blastp_afP05652.pse
png blastp_afP05652.png
