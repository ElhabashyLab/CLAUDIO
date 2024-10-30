load blastp_afP50735.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP50735
color 3, chain A
show cartoon, chain A
dist intra_662_4_valid , resid 80 and blastp_afP50735 and chain A and name cb, resid 98 and blastp_afP50735 and chain A and name cb
dist intra_1390_valid , resid 416 and blastp_afP50735 and chain A and name cb, resid 189 and blastp_afP50735 and chain A and name cb
dist intra_2000_valid , resid 31 and blastp_afP50735 and chain A and name cb, resid 338 and blastp_afP50735 and chain A and name cb
dist intra_3168_valid , resid 416 and blastp_afP50735 and chain A and name cb, resid 80 and blastp_afP50735 and chain A and name cb
dist intra_3658_valid , resid 416 and blastp_afP50735 and chain A and name cb, resid 389 and blastp_afP50735 and chain A and name cb
dist intra_5838_valid , resid 416 and blastp_afP50735 and chain A and name cb, resid 92 and blastp_afP50735 and chain A and name cb
dist intra_4319_out_range , resid 52 and blastp_afP50735 and chain A and name cb, resid 416 and blastp_afP50735 and chain A and name cb
dist intra_528_unknown , resid 14 and blastp_afP50735 and chain A and name cb, resid 27 and blastp_afP50735 and chain A and name cb
dist intra_1529_unknown , resid 14 and blastp_afP50735 and chain A and name cb, resid 92 and blastp_afP50735 and chain A and name cb
dist intra_1921_unknown , resid 177 and blastp_afP50735 and chain A and name cb, resid 52 and blastp_afP50735 and chain A and name cb
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
save blastp_afP50735.pse
png blastp_afP50735.png
