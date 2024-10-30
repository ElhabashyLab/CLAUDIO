load blastp_afP21472.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP21472
color 3, chain A
show cartoon, chain A
dist intra_18_valid , resid 33 and blastp_afP21472 and chain A and name cb, resid 26 and blastp_afP21472 and chain A and name cb
dist intra_392_valid , resid 33 and blastp_afP21472 and chain A and name cb, resid 20 and blastp_afP21472 and chain A and name cb
dist intra_1435_valid , resid 43 and blastp_afP21472 and chain A and name cb, resid 32 and blastp_afP21472 and chain A and name cb
dist intra_1677_valid , resid 56 and blastp_afP21472 and chain A and name cb, resid 43 and blastp_afP21472 and chain A and name cb
dist intra_2029_valid , resid 15 and blastp_afP21472 and chain A and name cb, resid 26 and blastp_afP21472 and chain A and name cb
dist intra_2827_valid , resid 20 and blastp_afP21472 and chain A and name cb, resid 32 and blastp_afP21472 and chain A and name cb
dist intra_3815_valid , resid 20 and blastp_afP21472 and chain A and name cb, resid 101 and blastp_afP21472 and chain A and name cb
dist intra_4123_valid , resid 33 and blastp_afP21472 and chain A and name cb, resid 15 and blastp_afP21472 and chain A and name cb
dist intra_4692_valid , resid 101 and blastp_afP21472 and chain A and name cb, resid 15 and blastp_afP21472 and chain A and name cb
dist intra_4767_valid , resid 101 and blastp_afP21472 and chain A and name cb, resid 43 and blastp_afP21472 and chain A and name cb
dist intra_5651_valid , resid 101 and blastp_afP21472 and chain A and name cb, resid 56 and blastp_afP21472 and chain A and name cb
dist intra_4436_out_range , resid 101 and blastp_afP21472 and chain A and name cb, resid 32 and blastp_afP21472 and chain A and name cb
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
save blastp_afP21472.pse
png blastp_afP21472.png
