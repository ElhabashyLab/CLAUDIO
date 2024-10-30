load blastp_afP36947.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP36947
color 3, chain A
show cartoon, chain A
dist intra_242_valid , resid 413 and blastp_afP36947 and chain A and name cb, resid 313 and blastp_afP36947 and chain A and name cb
dist intra_514_valid , resid 383 and blastp_afP36947 and chain A and name cb, resid 378 and blastp_afP36947 and chain A and name cb
dist intra_1553_valid , resid 413 and blastp_afP36947 and chain A and name cb, resid 326 and blastp_afP36947 and chain A and name cb
dist intra_1590_valid , resid 406 and blastp_afP36947 and chain A and name cb, resid 318 and blastp_afP36947 and chain A and name cb
dist intra_2507_valid , resid 406 and blastp_afP36947 and chain A and name cb, resid 313 and blastp_afP36947 and chain A and name cb
dist intra_2582_valid , resid 406 and blastp_afP36947 and chain A and name cb, resid 336 and blastp_afP36947 and chain A and name cb
dist intra_2890_valid , resid 318 and blastp_afP36947 and chain A and name cb, resid 326 and blastp_afP36947 and chain A and name cb
dist intra_3462_valid , resid 233 and blastp_afP36947 and chain A and name cb, resid 383 and blastp_afP36947 and chain A and name cb
dist intra_4339_valid , resid 367 and blastp_afP36947 and chain A and name cb, resid 378 and blastp_afP36947 and chain A and name cb
dist intra_4479_valid , resid 367 and blastp_afP36947 and chain A and name cb, resid 413 and blastp_afP36947 and chain A and name cb
dist intra_4905_valid , resid 314 and blastp_afP36947 and chain A and name cb, resid 259 and blastp_afP36947 and chain A and name cb
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
save blastp_afP36947.pse
png blastp_afP36947.png
