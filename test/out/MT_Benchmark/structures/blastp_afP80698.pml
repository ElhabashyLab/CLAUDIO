load blastp_afP80698.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP80698
color 3, chain A
show cartoon, chain A
dist intra_245_valid , resid 33 and blastp_afP80698 and chain A and name cb, resid 37 and blastp_afP80698 and chain A and name cb
dist intra_322_valid , resid 245 and blastp_afP80698 and chain A and name cb, resid 143 and blastp_afP80698 and chain A and name cb
dist intra_480_valid , resid 368 and blastp_afP80698 and chain A and name cb, resid 117 and blastp_afP80698 and chain A and name cb
dist intra_1159_valid , resid 4 and blastp_afP80698 and chain A and name cb, resid 97 and blastp_afP80698 and chain A and name cb
dist intra_2938_valid , resid 385 and blastp_afP80698 and chain A and name cb, resid 415 and blastp_afP80698 and chain A and name cb
dist intra_3311_valid , resid 33 and blastp_afP80698 and chain A and name cb, resid 48 and blastp_afP80698 and chain A and name cb
dist intra_3662_valid , resid 117 and blastp_afP80698 and chain A and name cb, resid 7 and blastp_afP80698 and chain A and name cb
dist intra_3721_valid , resid 37 and blastp_afP80698 and chain A and name cb, resid 46 and blastp_afP80698 and chain A and name cb
dist intra_4162_valid , resid 37 and blastp_afP80698 and chain A and name cb, resid 48 and blastp_afP80698 and chain A and name cb
dist intra_4716_valid , resid 398 and blastp_afP80698 and chain A and name cb, resid 318 and blastp_afP80698 and chain A and name cb
dist intra_4759_valid , resid 318 and blastp_afP80698 and chain A and name cb, resid 346 and blastp_afP80698 and chain A and name cb
dist intra_5832_valid , resid 113 and blastp_afP80698 and chain A and name cb, resid 412 and blastp_afP80698 and chain A and name cb
dist intra_3912_overlaps , resid 79 and blastp_afP80698 and chain A and name cb, resid 4 and blastp_afP80698 and chain A and name cb
dist intra_4225_overlaps , resid 33 and blastp_afP80698 and chain A and name cb, resid 34 and blastp_afP80698 and chain A and name cb
dist intra_2194_unknown , resid 245 and blastp_afP80698 and chain A and name cb, resid 129 and blastp_afP80698 and chain A and name cb
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
save blastp_afP80698.pse
png blastp_afP80698.png
