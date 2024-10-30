load blastp_afO32165.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO32165
color 3, chain A
show cartoon, chain A
dist intra_66_valid , resid 28 and blastp_afO32165 and chain A and name cb, resid 15 and blastp_afO32165 and chain A and name cb
dist intra_230_valid , resid 20 and blastp_afO32165 and chain A and name cb, resid 61 and blastp_afO32165 and chain A and name cb
dist intra_1249_valid , resid 45 and blastp_afO32165 and chain A and name cb, resid 50 and blastp_afO32165 and chain A and name cb
dist intra_2500_valid , resid 43 and blastp_afO32165 and chain A and name cb, resid 50 and blastp_afO32165 and chain A and name cb
dist intra_5011_valid , resid 323 and blastp_afO32165 and chain A and name cb, resid 358 and blastp_afO32165 and chain A and name cb
dist intra_5892_valid , resid 324 and blastp_afO32165 and chain A and name cb, resid 358 and blastp_afO32165 and chain A and name cb
dist intra_1376_unknown , resid 145 and blastp_afO32165 and chain A and name cb, resid 6 and blastp_afO32165 and chain A and name cb
dist intra_4157_unknown , resid 16 and blastp_afO32165 and chain A and name cb, resid 61 and blastp_afO32165 and chain A and name cb
dist intra_5355_unknown , resid 32 and blastp_afO32165 and chain A and name cb, resid 50 and blastp_afO32165 and chain A and name cb
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
save blastp_afO32165.pse
png blastp_afO32165.png
