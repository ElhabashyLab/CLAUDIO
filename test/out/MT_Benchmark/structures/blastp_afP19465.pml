load blastp_afP19465.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP19465
color 3, chain A
show cartoon, chain A
dist intra_237_valid , resid 38 and blastp_afP19465 and chain A and name cb, resid 6 and blastp_afP19465 and chain A and name cb
dist intra_2276_valid , resid 34 and blastp_afP19465 and chain A and name cb, resid 6 and blastp_afP19465 and chain A and name cb
dist intra_2571_valid , resid 34 and blastp_afP19465 and chain A and name cb, resid 38 and blastp_afP19465 and chain A and name cb
dist intra_4149_valid , resid 38 and blastp_afP19465 and chain A and name cb, resid 105 and blastp_afP19465 and chain A and name cb
dist intra_1563_overlaps , resid 15 and blastp_afP19465 and chain A and name cb, resid 6 and blastp_afP19465 and chain A and name cb
dist intra_4915_unknown , resid 15 and blastp_afP19465 and chain A and name cb, resid 105 and blastp_afP19465 and chain A and name cb
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
save blastp_afP19465.pse
png blastp_afP19465.png
