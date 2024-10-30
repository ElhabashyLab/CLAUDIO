load blastp_afO07021.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO07021
color 3, chain A
show cartoon, chain A
dist intra_1299_valid , resid 419 and blastp_afO07021 and chain A and name cb, resid 459 and blastp_afO07021 and chain A and name cb
dist intra_3042_valid , resid 406 and blastp_afO07021 and chain A and name cb, resid 459 and blastp_afO07021 and chain A and name cb
dist intra_3120_valid , resid 440 and blastp_afO07021 and chain A and name cb, resid 459 and blastp_afO07021 and chain A and name cb
dist intra_3259_valid , resid 393 and blastp_afO07021 and chain A and name cb, resid 385 and blastp_afO07021 and chain A and name cb
dist intra_4545_valid , resid 440 and blastp_afO07021 and chain A and name cb, resid 423 and blastp_afO07021 and chain A and name cb
dist intra_5032_valid , resid 437 and blastp_afO07021 and chain A and name cb, resid 459 and blastp_afO07021 and chain A and name cb
dist intra_5718_valid , resid 446 and blastp_afO07021 and chain A and name cb, resid 437 and blastp_afO07021 and chain A and name cb
dist intra_6041_out_range , resid 402 and blastp_afO07021 and chain A and name cb, resid 440 and blastp_afO07021 and chain A and name cb
dist intra_2586_unknown , resid 385 and blastp_afO07021 and chain A and name cb, resid 388 and blastp_afO07021 and chain A and name cb
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
save blastp_afO07021.pse
png blastp_afO07021.png
