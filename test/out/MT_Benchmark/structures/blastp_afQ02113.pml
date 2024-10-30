load blastp_afQ02113.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afQ02113
color 3, chain A
show cartoon, chain A
dist intra_1414_valid , resid 131 and blastp_afQ02113 and chain A and name cb, resid 83 and blastp_afQ02113 and chain A and name cb
dist intra_1482_valid , resid 655 and blastp_afQ02113 and chain A and name cb, resid 666 and blastp_afQ02113 and chain A and name cb
dist intra_1748_valid , resid 108 and blastp_afQ02113 and chain A and name cb, resid 161 and blastp_afQ02113 and chain A and name cb
dist intra_2748_valid , resid 53 and blastp_afQ02113 and chain A and name cb, resid 378 and blastp_afQ02113 and chain A and name cb
dist intra_3369_valid , resid 296 and blastp_afQ02113 and chain A and name cb, resid 83 and blastp_afQ02113 and chain A and name cb
dist intra_4715_valid , resid 246 and blastp_afQ02113 and chain A and name cb, resid 217 and blastp_afQ02113 and chain A and name cb
dist intra_4604_out_range , resid 108 and blastp_afQ02113 and chain A and name cb, resid 153 and blastp_afQ02113 and chain A and name cb
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
save blastp_afQ02113.pse
png blastp_afQ02113.png
