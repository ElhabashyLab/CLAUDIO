load blastp_afO30509.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO30509
color 3, chain A
show cartoon, chain A
dist intra_486_valid , resid 223 and blastp_afO30509 and chain A and name cb, resid 254 and blastp_afO30509 and chain A and name cb
dist intra_1039_valid , resid 421 and blastp_afO30509 and chain A and name cb, resid 457 and blastp_afO30509 and chain A and name cb
dist intra_1132_valid , resid 385 and blastp_afO30509 and chain A and name cb, resid 454 and blastp_afO30509 and chain A and name cb
dist intra_1351_valid , resid 213 and blastp_afO30509 and chain A and name cb, resid 129 and blastp_afO30509 and chain A and name cb
dist intra_1392_valid , resid 408 and blastp_afO30509 and chain A and name cb, resid 457 and blastp_afO30509 and chain A and name cb
dist intra_1580_valid , resid 223 and blastp_afO30509 and chain A and name cb, resid 255 and blastp_afO30509 and chain A and name cb
dist intra_2171_valid , resid 408 and blastp_afO30509 and chain A and name cb, resid 397 and blastp_afO30509 and chain A and name cb
dist intra_2240_valid , resid 408 and blastp_afO30509 and chain A and name cb, resid 392 and blastp_afO30509 and chain A and name cb
dist intra_2322_valid , resid 385 and blastp_afO30509 and chain A and name cb, resid 392 and blastp_afO30509 and chain A and name cb
dist intra_2820_valid , resid 230 and blastp_afO30509 and chain A and name cb, resid 255 and blastp_afO30509 and chain A and name cb
dist intra_2838_valid , resid 129 and blastp_afO30509 and chain A and name cb, resid 262 and blastp_afO30509 and chain A and name cb
dist intra_3920_valid , resid 474 and blastp_afO30509 and chain A and name cb, resid 438 and blastp_afO30509 and chain A and name cb
dist intra_4184_valid , resid 379 and blastp_afO30509 and chain A and name cb, resid 457 and blastp_afO30509 and chain A and name cb
dist intra_4899_valid , resid 79 and blastp_afO30509 and chain A and name cb, resid 213 and blastp_afO30509 and chain A and name cb
dist intra_5301_valid , resid 385 and blastp_afO30509 and chain A and name cb, resid 457 and blastp_afO30509 and chain A and name cb
dist intra_849_unknown , resid 262 and blastp_afO30509 and chain A and name cb, resid 192 and blastp_afO30509 and chain A and name cb
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
save blastp_afO30509.pse
png blastp_afO30509.png
