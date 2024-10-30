load blastp_afO32162.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO32162
color 3, chain A
show cartoon, chain A
dist intra_5853_valid , resid 349 and blastp_afO32162 and chain A and name cb, resid 321 and blastp_afO32162 and chain A and name cb
dist intra_946_unknown , resid 18 and blastp_afO32162 and chain A and name cb, resid 4 and blastp_afO32162 and chain A and name cb
dist intra_970_unknown , resid 31 and blastp_afO32162 and chain A and name cb, resid 18 and blastp_afO32162 and chain A and name cb
dist intra_1694_unknown , resid 299 and blastp_afO32162 and chain A and name cb, resid 163 and blastp_afO32162 and chain A and name cb
dist intra_2063_unknown , resid 321 and blastp_afO32162 and chain A and name cb, resid 371 and blastp_afO32162 and chain A and name cb
dist intra_3997_unknown , resid 321 and blastp_afO32162 and chain A and name cb, resid 105 and blastp_afO32162 and chain A and name cb
dist intra_4271_unknown , resid 299 and blastp_afO32162 and chain A and name cb, resid 252 and blastp_afO32162 and chain A and name cb
dist intra_4520_unknown , resid 365 and blastp_afO32162 and chain A and name cb, resid 299 and blastp_afO32162 and chain A and name cb
dist intra_6064_unknown , resid 4 and blastp_afO32162 and chain A and name cb, resid 321 and blastp_afO32162 and chain A and name cb
dist intra_6146_unknown , resid 4 and blastp_afO32162 and chain A and name cb, resid 349 and blastp_afO32162 and chain A and name cb
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
save blastp_afO32162.pse
png blastp_afO32162.png
