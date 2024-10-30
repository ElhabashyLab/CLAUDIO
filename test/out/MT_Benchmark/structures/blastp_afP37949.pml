load blastp_afP37949.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP37949
color 3, chain A
show cartoon, chain A
dist intra_2402_valid , resid 527 and blastp_afP37949 and chain A and name cb, resid 554 and blastp_afP37949 and chain A and name cb
dist intra_3004_valid , resid 232 and blastp_afP37949 and chain A and name cb, resid 273 and blastp_afP37949 and chain A and name cb
dist intra_3559_valid , resid 546 and blastp_afP37949 and chain A and name cb, resid 520 and blastp_afP37949 and chain A and name cb
dist intra_5081_valid , resid 520 and blastp_afP37949 and chain A and name cb, resid 527 and blastp_afP37949 and chain A and name cb
dist intra_6104_valid , resid 37 and blastp_afP37949 and chain A and name cb, resid 76 and blastp_afP37949 and chain A and name cb
dist intra_5965_unknown , resid 525 and blastp_afP37949 and chain A and name cb, resid 610 and blastp_afP37949 and chain A and name cb
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
save blastp_afP37949.pse
png blastp_afP37949.png
