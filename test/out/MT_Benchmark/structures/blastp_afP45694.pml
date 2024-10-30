load blastp_afP45694.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP45694
color 3, chain A
show cartoon, chain A
dist intra_48_valid , resid 390 and blastp_afP45694 and chain A and name cb, resid 369 and blastp_afP45694 and chain A and name cb
dist intra_1381_valid , resid 7 and blastp_afP45694 and chain A and name cb, resid 268 and blastp_afP45694 and chain A and name cb
dist intra_1458_valid , resid 608 and blastp_afP45694 and chain A and name cb, resid 667 and blastp_afP45694 and chain A and name cb
dist intra_2776_valid , resid 370 and blastp_afP45694 and chain A and name cb, resid 339 and blastp_afP45694 and chain A and name cb
dist intra_4270_valid , resid 317 and blastp_afP45694 and chain A and name cb, resid 306 and blastp_afP45694 and chain A and name cb
dist intra_4898_valid , resid 238 and blastp_afP45694 and chain A and name cb, resid 203 and blastp_afP45694 and chain A and name cb
dist intra_5813_valid , resid 268 and blastp_afP45694 and chain A and name cb, resid 22 and blastp_afP45694 and chain A and name cb
dist intra_3734_same , resid 608 and blastp_afP45694 and chain A and name cb, resid 608 and blastp_afP45694 and chain A and name cb
dist intra_203_unknown , resid 358 and blastp_afP45694 and chain A and name cb, resid 390 and blastp_afP45694 and chain A and name cb
dist intra_2874_unknown , resid 594 and blastp_afP45694 and chain A and name cb, resid 667 and blastp_afP45694 and chain A and name cb
dist intra_2907_unknown , resid 594 and blastp_afP45694 and chain A and name cb, resid 608 and blastp_afP45694 and chain A and name cb
dist intra_3956_unknown , resid 7 and blastp_afP45694 and chain A and name cb, resid 1 and blastp_afP45694 and chain A and name cb
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
save blastp_afP45694.pse
png blastp_afP45694.png
