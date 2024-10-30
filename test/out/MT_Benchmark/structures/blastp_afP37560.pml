load blastp_afP37560.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP37560
color 3, chain A
show cartoon, chain A
dist intra_4186_valid , resid 8 and blastp_afP37560 and chain A and name cb, resid 59 and blastp_afP37560 and chain A and name cb
dist intra_5777_valid , resid 103 and blastp_afP37560 and chain A and name cb, resid 97 and blastp_afP37560 and chain A and name cb
dist intra_5882_out_range , resid 97 and blastp_afP37560 and chain A and name cb, resid 8 and blastp_afP37560 and chain A and name cb
dist intra_1375_unknown , resid 103 and blastp_afP37560 and chain A and name cb, resid 91 and blastp_afP37560 and chain A and name cb
dist intra_2152_unknown , resid 91 and blastp_afP37560 and chain A and name cb, resid 59 and blastp_afP37560 and chain A and name cb
dist intra_2201_unknown , resid 100 and blastp_afP37560 and chain A and name cb, resid 91 and blastp_afP37560 and chain A and name cb
dist intra_3728_unknown , resid 98 and blastp_afP37560 and chain A and name cb, resid 91 and blastp_afP37560 and chain A and name cb
dist intra_5469_unknown , resid 103 and blastp_afP37560 and chain A and name cb, resid 59 and blastp_afP37560 and chain A and name cb
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
save blastp_afP37560.pse
png blastp_afP37560.png
