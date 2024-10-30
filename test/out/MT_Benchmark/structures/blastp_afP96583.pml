load blastp_afP96583.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP96583
color 3, chain A
show cartoon, chain A
dist intra_390_valid , resid 504 and blastp_afP96583 and chain A and name cb, resid 575 and blastp_afP96583 and chain A and name cb
dist intra_1032_valid , resid 361 and blastp_afP96583 and chain A and name cb, resid 504 and blastp_afP96583 and chain A and name cb
dist intra_1522_valid , resid 534 and blastp_afP96583 and chain A and name cb, resid 545 and blastp_afP96583 and chain A and name cb
dist intra_1771_valid , resid 141 and blastp_afP96583 and chain A and name cb, resid 22 and blastp_afP96583 and chain A and name cb
dist intra_1785_valid , resid 386 and blastp_afP96583 and chain A and name cb, resid 383 and blastp_afP96583 and chain A and name cb
dist intra_1899_valid , resid 151 and blastp_afP96583 and chain A and name cb, resid 577 and blastp_afP96583 and chain A and name cb
dist intra_2353_valid , resid 474 and blastp_afP96583 and chain A and name cb, resid 500 and blastp_afP96583 and chain A and name cb
dist intra_2900_valid , resid 383 and blastp_afP96583 and chain A and name cb, resid 300 and blastp_afP96583 and chain A and name cb
dist intra_2997_valid , resid 89 and blastp_afP96583 and chain A and name cb, resid 120 and blastp_afP96583 and chain A and name cb
dist intra_3265_valid , resid 125 and blastp_afP96583 and chain A and name cb, resid 151 and blastp_afP96583 and chain A and name cb
dist intra_3657_valid , resid 74 and blastp_afP96583 and chain A and name cb, resid 120 and blastp_afP96583 and chain A and name cb
dist intra_3852_valid , resid 79 and blastp_afP96583 and chain A and name cb, resid 120 and blastp_afP96583 and chain A and name cb
dist intra_3005_unknown , resid 84 and blastp_afP96583 and chain A and name cb, resid 120 and blastp_afP96583 and chain A and name cb
dist intra_4442_unknown , resid 727 and blastp_afP96583 and chain A and name cb, resid 721 and blastp_afP96583 and chain A and name cb
dist intra_4668_unknown , resid 84 and blastp_afP96583 and chain A and name cb, resid 95 and blastp_afP96583 and chain A and name cb
dist intra_5795_unknown , resid 255 and blastp_afP96583 and chain A and name cb, resid 234 and blastp_afP96583 and chain A and name cb
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
save blastp_afP96583.pse
png blastp_afP96583.png
