load blastp_afP54418.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP54418
color 3, chain A
show cartoon, chain A
dist intra_955_valid , resid 59 and blastp_afP54418 and chain A and name cb, resid 375 and blastp_afP54418 and chain A and name cb
dist intra_3620_valid , resid 375 and blastp_afP54418 and chain A and name cb, resid 512 and blastp_afP54418 and chain A and name cb
dist intra_4556_valid , resid 59 and blastp_afP54418 and chain A and name cb, resid 166 and blastp_afP54418 and chain A and name cb
dist intra_275_unknown , resid 274 and blastp_afP54418 and chain A and name cb, resid 440 and blastp_afP54418 and chain A and name cb
dist intra_1286_unknown , resid 59 and blastp_afP54418 and chain A and name cb, resid 362 and blastp_afP54418 and chain A and name cb
dist intra_2495_unknown , resid 274 and blastp_afP54418 and chain A and name cb, resid 439 and blastp_afP54418 and chain A and name cb
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
save blastp_afP54418.pse
png blastp_afP54418.png
