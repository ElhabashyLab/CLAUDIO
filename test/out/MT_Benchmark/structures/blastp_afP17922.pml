load blastp_afP17922.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP17922
color 3, chain A
show cartoon, chain A
dist intra_150_valid , resid 105 and blastp_afP17922 and chain A and name cb, resid 44 and blastp_afP17922 and chain A and name cb
dist intra_650_valid , resid 650 and blastp_afP17922 and chain A and name cb, resid 527 and blastp_afP17922 and chain A and name cb
dist intra_1558_valid , resid 650 and blastp_afP17922 and chain A and name cb, resid 536 and blastp_afP17922 and chain A and name cb
dist intra_1594_valid , resid 789 and blastp_afP17922 and chain A and name cb, resid 742 and blastp_afP17922 and chain A and name cb
dist intra_1760_valid , resid 371 and blastp_afP17922 and chain A and name cb, resid 357 and blastp_afP17922 and chain A and name cb
dist intra_2309_valid , resid 650 and blastp_afP17922 and chain A and name cb, resid 528 and blastp_afP17922 and chain A and name cb
dist intra_4003_valid , resid 371 and blastp_afP17922 and chain A and name cb, resid 1 and blastp_afP17922 and chain A and name cb
dist intra_5196_valid , resid 283 and blastp_afP17922 and chain A and name cb, resid 231 and blastp_afP17922 and chain A and name cb
dist intra_1524_unknown , resid 650 and blastp_afP17922 and chain A and name cb, resid 509 and blastp_afP17922 and chain A and name cb
dist intra_2545_unknown , resid 650 and blastp_afP17922 and chain A and name cb, resid 529 and blastp_afP17922 and chain A and name cb
dist intra_4086_unknown , resid 357 and blastp_afP17922 and chain A and name cb, resid 369 and blastp_afP17922 and chain A and name cb
dist intra_5582_unknown , resid 789 and blastp_afP17922 and chain A and name cb, resid 738 and blastp_afP17922 and chain A and name cb
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
save blastp_afP17922.pse
png blastp_afP17922.png
