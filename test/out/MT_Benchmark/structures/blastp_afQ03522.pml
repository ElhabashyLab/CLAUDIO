load blastp_afQ03522.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afQ03522
color 3, chain A
show cartoon, chain A
dist intra_439_valid , resid 348 and blastp_afQ03522 and chain A and name cb, resid 326 and blastp_afQ03522 and chain A and name cb
dist intra_551_valid , resid 206 and blastp_afQ03522 and chain A and name cb, resid 210 and blastp_afQ03522 and chain A and name cb
dist intra_770_valid , resid 304 and blastp_afQ03522 and chain A and name cb, resid 136 and blastp_afQ03522 and chain A and name cb
dist intra_4209_valid , resid 367 and blastp_afQ03522 and chain A and name cb, resid 388 and blastp_afQ03522 and chain A and name cb
dist intra_5269_valid , resid 304 and blastp_afQ03522 and chain A and name cb, resid 134 and blastp_afQ03522 and chain A and name cb
dist intra_2460_same , resid 206 and blastp_afQ03522 and chain A and name cb, resid 206 and blastp_afQ03522 and chain A and name cb
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
save blastp_afQ03522.pse
png blastp_afQ03522.png
