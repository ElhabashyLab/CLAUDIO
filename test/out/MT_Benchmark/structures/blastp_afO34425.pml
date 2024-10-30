load blastp_afO34425.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO34425
color 3, chain A
show cartoon, chain A
dist intra_55_valid , resid 193 and blastp_afO34425 and chain A and name cb, resid 105 and blastp_afO34425 and chain A and name cb
dist intra_666_valid , resid 335 and blastp_afO34425 and chain A and name cb, resid 115 and blastp_afO34425 and chain A and name cb
dist intra_1321_valid , resid 71 and blastp_afO34425 and chain A and name cb, resid 4 and blastp_afO34425 and chain A and name cb
dist intra_2014_valid , resid 105 and blastp_afO34425 and chain A and name cb, resid 81 and blastp_afO34425 and chain A and name cb
dist intra_2164_valid , resid 124 and blastp_afO34425 and chain A and name cb, resid 193 and blastp_afO34425 and chain A and name cb
dist intra_2947_valid , resid 103 and blastp_afO34425 and chain A and name cb, resid 193 and blastp_afO34425 and chain A and name cb
dist intra_4080_valid , resid 335 and blastp_afO34425 and chain A and name cb, resid 116 and blastp_afO34425 and chain A and name cb
dist intra_4328_valid , resid 116 and blastp_afO34425 and chain A and name cb, resid 105 and blastp_afO34425 and chain A and name cb
dist intra_2298_out_range , resid 116 and blastp_afO34425 and chain A and name cb, resid 193 and blastp_afO34425 and chain A and name cb
dist intra_93_unknown , resid 193 and blastp_afO34425 and chain A and name cb, resid 104 and blastp_afO34425 and chain A and name cb
dist intra_575_unknown , resid 193 and blastp_afO34425 and chain A and name cb, resid 200 and blastp_afO34425 and chain A and name cb
dist intra_5999_unknown , resid 335 and blastp_afO34425 and chain A and name cb, resid 106 and blastp_afO34425 and chain A and name cb
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
save blastp_afO34425.pse
png blastp_afO34425.png
