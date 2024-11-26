load blastp_afP37465.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP37465
color 3, chain A
show cartoon, chain A
dist intra_190_valid , resid 659 and blastp_afP37465 and chain A and name cb, resid 598 and blastp_afP37465 and chain A and name cb
dist intra_320_valid , resid 186 and blastp_afP37465 and chain A and name cb, resid 201 and blastp_afP37465 and chain A and name cb
dist intra_613_valid , resid 316 and blastp_afP37465 and chain A and name cb, resid 308 and blastp_afP37465 and chain A and name cb
dist intra_1192_valid , resid 62 and blastp_afP37465 and chain A and name cb, resid 316 and blastp_afP37465 and chain A and name cb
dist intra_1289_valid , resid 210 and blastp_afP37465 and chain A and name cb, resid 186 and blastp_afP37465 and chain A and name cb
dist intra_1418_valid , resid 480 and blastp_afP37465 and chain A and name cb, resid 86 and blastp_afP37465 and chain A and name cb
dist intra_1914_valid , resid 380 and blastp_afP37465 and chain A and name cb, resid 515 and blastp_afP37465 and chain A and name cb
dist intra_2532_valid , resid 448 and blastp_afP37465 and chain A and name cb, resid 380 and blastp_afP37465 and chain A and name cb
dist intra_3477_valid , resid 316 and blastp_afP37465 and chain A and name cb, resid 274 and blastp_afP37465 and chain A and name cb
dist intra_1327_out_range , resid 618 and blastp_afP37465 and chain A and name cb, resid 582 and blastp_afP37465 and chain A and name cb
dist intra_1050_unknown , resid 582 and blastp_afP37465 and chain A and name cb, resid 619 and blastp_afP37465 and chain A and name cb
dist intra_1359_unknown , resid 316 and blastp_afP37465 and chain A and name cb, resid 298 and blastp_afP37465 and chain A and name cb
dist intra_3376_unknown , resid 659 and blastp_afP37465 and chain A and name cb, resid 590 and blastp_afP37465 and chain A and name cb
dist intra_5129_unknown , resid 533 and blastp_afP37465 and chain A and name cb, resid 298 and blastp_afP37465 and chain A and name cb
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
save blastp_afP37465.pse
png blastp_afP37465.png
