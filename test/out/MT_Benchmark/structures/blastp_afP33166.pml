load blastp_afP33166.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP33166
color 3, chain A
show cartoon, chain A
dist intra_1_valid , resid 239 and blastp_afP33166 and chain A and name cb, resid 297 and blastp_afP33166 and chain A and name cb
dist intra_20_valid , resid 297 and blastp_afP33166 and chain A and name cb, resid 255 and blastp_afP33166 and chain A and name cb
dist intra_269_valid , resid 297 and blastp_afP33166 and chain A and name cb, resid 266 and blastp_afP33166 and chain A and name cb
dist intra_937_valid , resid 266 and blastp_afP33166 and chain A and name cb, resid 42 and blastp_afP33166 and chain A and name cb
dist intra_1207_valid , resid 210 and blastp_afP33166 and chain A and name cb, resid 297 and blastp_afP33166 and chain A and name cb
dist intra_1341_valid , resid 10 and blastp_afP33166 and chain A and name cb, resid 266 and blastp_afP33166 and chain A and name cb
dist intra_2160_valid , resid 38 and blastp_afP33166 and chain A and name cb, resid 266 and blastp_afP33166 and chain A and name cb
dist intra_2817_valid , resid 38 and blastp_afP33166 and chain A and name cb, resid 42 and blastp_afP33166 and chain A and name cb
dist intra_4147_valid , resid 239 and blastp_afP33166 and chain A and name cb, resid 5 and blastp_afP33166 and chain A and name cb
dist intra_5842_valid , resid 5 and blastp_afP33166 and chain A and name cb, resid 38 and blastp_afP33166 and chain A and name cb
dist intra_2094_out_range , resid 266 and blastp_afP33166 and chain A and name cb, resid 255 and blastp_afP33166 and chain A and name cb
dist intra_4741_out_range , resid 297 and blastp_afP33166 and chain A and name cb, resid 316 and blastp_afP33166 and chain A and name cb
dist intra_2098_same , resid 266 and blastp_afP33166 and chain A and name cb, resid 266 and blastp_afP33166 and chain A and name cb
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
save blastp_afP33166.pse
png blastp_afP33166.png
