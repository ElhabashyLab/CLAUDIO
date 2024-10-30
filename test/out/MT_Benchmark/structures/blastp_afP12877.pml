load blastp_afP12877.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP12877
color 3, chain A
show cartoon, chain A
dist intra_354_valid , resid 179 and blastp_afP12877 and chain A and name cb, resid 19 and blastp_afP12877 and chain A and name cb
dist intra_3373_valid , resid 120 and blastp_afP12877 and chain A and name cb, resid 179 and blastp_afP12877 and chain A and name cb
dist intra_3552_valid , resid 133 and blastp_afP12877 and chain A and name cb, resid 120 and blastp_afP12877 and chain A and name cb
dist intra_2176_overlaps , resid 168 and blastp_afP12877 and chain A and name cb, resid 11 and blastp_afP12877 and chain A and name cb
dist intra_272_unknown , resid 19 and blastp_afP12877 and chain A and name cb, resid 168 and blastp_afP12877 and chain A and name cb
dist intra_2674_unknown , resid 33 and blastp_afP12877 and chain A and name cb, resid 81 and blastp_afP12877 and chain A and name cb
dist intra_3661_unknown , resid 120 and blastp_afP12877 and chain A and name cb, resid 168 and blastp_afP12877 and chain A and name cb
dist intra_6084_unknown , resid 70 and blastp_afP12877 and chain A and name cb, resid 88 and blastp_afP12877 and chain A and name cb
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
save blastp_afP12877.pse
png blastp_afP12877.png
