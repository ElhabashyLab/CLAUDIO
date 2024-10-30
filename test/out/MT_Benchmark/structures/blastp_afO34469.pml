load blastp_afO34469.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO34469
color 3, chain A
show cartoon, chain A
dist intra_1907_valid , resid 488 and blastp_afO34469 and chain A and name cb, resid 445 and blastp_afO34469 and chain A and name cb
dist intra_2409_valid , resid 114 and blastp_afO34469 and chain A and name cb, resid 140 and blastp_afO34469 and chain A and name cb
dist intra_2720_valid , resid 497 and blastp_afO34469 and chain A and name cb, resid 466 and blastp_afO34469 and chain A and name cb
dist intra_5209_valid , resid 83 and blastp_afO34469 and chain A and name cb, resid 97 and blastp_afO34469 and chain A and name cb
dist intra_2877_unknown , resid 493 and blastp_afO34469 and chain A and name cb, resid 583 and blastp_afO34469 and chain A and name cb
dist intra_5726_unknown , resid 466 and blastp_afO34469 and chain A and name cb, resid 583 and blastp_afO34469 and chain A and name cb
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
save blastp_afO34469.pse
png blastp_afO34469.png
