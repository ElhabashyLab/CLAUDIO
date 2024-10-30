load blastp_afP08750.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP08750
color 3, chain A
show cartoon, chain A
dist intra_422_valid , resid 408 and blastp_afP08750 and chain A and name cb, resid 326 and blastp_afP08750 and chain A and name cb
dist intra_2208_valid , resid 381 and blastp_afP08750 and chain A and name cb, resid 361 and blastp_afP08750 and chain A and name cb
dist intra_2468_valid , resid 57 and blastp_afP08750 and chain A and name cb, resid 288 and blastp_afP08750 and chain A and name cb
dist intra_3140_valid , resid 153 and blastp_afP08750 and chain A and name cb, resid 85 and blastp_afP08750 and chain A and name cb
dist intra_3457_valid , resid 344 and blastp_afP08750 and chain A and name cb, resid 378 and blastp_afP08750 and chain A and name cb
dist intra_3597_valid , resid 323 and blastp_afP08750 and chain A and name cb, resid 356 and blastp_afP08750 and chain A and name cb
dist intra_3792_valid , resid 366 and blastp_afP08750 and chain A and name cb, resid 378 and blastp_afP08750 and chain A and name cb
dist intra_4907_valid , resid 250 and blastp_afP08750 and chain A and name cb, resid 300 and blastp_afP08750 and chain A and name cb
dist intra_5411_valid , resid 153 and blastp_afP08750 and chain A and name cb, resid 71 and blastp_afP08750 and chain A and name cb
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
save blastp_afP08750.pse
png blastp_afP08750.png
