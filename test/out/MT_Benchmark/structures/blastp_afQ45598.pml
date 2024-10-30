load blastp_afQ45598.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afQ45598
color 3, chain A
show cartoon, chain A
dist intra_2689_valid , resid 398 and blastp_afQ45598 and chain A and name cb, resid 405 and blastp_afQ45598 and chain A and name cb
dist intra_3246_valid , resid 254 and blastp_afQ45598 and chain A and name cb, resid 349 and blastp_afQ45598 and chain A and name cb
dist intra_4863_valid , resid 344 and blastp_afQ45598 and chain A and name cb, resid 337 and blastp_afQ45598 and chain A and name cb
dist intra_4940_valid , resid 398 and blastp_afQ45598 and chain A and name cb, resid 195 and blastp_afQ45598 and chain A and name cb
dist intra_3726_unknown , resid 254 and blastp_afQ45598 and chain A and name cb, resid 242 and blastp_afQ45598 and chain A and name cb
dist intra_4161_unknown , resid 254 and blastp_afQ45598 and chain A and name cb, resid 238 and blastp_afQ45598 and chain A and name cb
dist intra_5067_unknown , resid 464 and blastp_afQ45598 and chain A and name cb, resid 471 and blastp_afQ45598 and chain A and name cb
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
save blastp_afQ45598.pse
png blastp_afQ45598.png
