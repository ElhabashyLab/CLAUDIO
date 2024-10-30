load blastp_afP26899.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP26899
color 3, chain A
show cartoon, chain A
dist intra_174_valid , resid 125 and blastp_afP26899 and chain A and name cb, resid 12 and blastp_afP26899 and chain A and name cb
dist intra_746_valid , resid 399 and blastp_afP26899 and chain A and name cb, resid 407 and blastp_afP26899 and chain A and name cb
dist intra_1358_valid , resid 399 and blastp_afP26899 and chain A and name cb, resid 401 and blastp_afP26899 and chain A and name cb
dist intra_1571_valid , resid 402 and blastp_afP26899 and chain A and name cb, resid 399 and blastp_afP26899 and chain A and name cb
dist intra_2411_valid , resid 67 and blastp_afP26899 and chain A and name cb, resid 247 and blastp_afP26899 and chain A and name cb
dist intra_4311_valid , resid 219 and blastp_afP26899 and chain A and name cb, resid 165 and blastp_afP26899 and chain A and name cb
dist intra_384_unknown , resid 165 and blastp_afP26899 and chain A and name cb, resid 385 and blastp_afP26899 and chain A and name cb
dist intra_1267_unknown , resid 403 and blastp_afP26899 and chain A and name cb, resid 399 and blastp_afP26899 and chain A and name cb
dist intra_1323_unknown , resid 125 and blastp_afP26899 and chain A and name cb, resid 1 and blastp_afP26899 and chain A and name cb
dist intra_1728_unknown , resid 1 and blastp_afP26899 and chain A and name cb, resid 12 and blastp_afP26899 and chain A and name cb
dist intra_1873_unknown , resid 163 and blastp_afP26899 and chain A and name cb, resid 219 and blastp_afP26899 and chain A and name cb
dist intra_3958_unknown , resid 118 and blastp_afP26899 and chain A and name cb, resid 12 and blastp_afP26899 and chain A and name cb
dist intra_4380_unknown , resid 67 and blastp_afP26899 and chain A and name cb, resid 223 and blastp_afP26899 and chain A and name cb
dist intra_4524_unknown , resid 10 and blastp_afP26899 and chain A and name cb, resid 125 and blastp_afP26899 and chain A and name cb
dist intra_5117_unknown , resid 163 and blastp_afP26899 and chain A and name cb, resid 385 and blastp_afP26899 and chain A and name cb
dist intra_5429_unknown , resid 125 and blastp_afP26899 and chain A and name cb, resid 7 and blastp_afP26899 and chain A and name cb
dist intra_5458_unknown , resid 1 and blastp_afP26899 and chain A and name cb, resid 126 and blastp_afP26899 and chain A and name cb
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
save blastp_afP26899.pse
png blastp_afP26899.png
