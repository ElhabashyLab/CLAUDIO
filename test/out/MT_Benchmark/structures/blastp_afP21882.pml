load blastp_afP21882.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP21882
color 3, chain A
show cartoon, chain A
dist intra_543_valid , resid 175 and blastp_afP21882 and chain A and name cb, resid 219 and blastp_afP21882 and chain A and name cb
dist intra_2117_valid , resid 313 and blastp_afP21882 and chain A and name cb, resid 226 and blastp_afP21882 and chain A and name cb
dist intra_2227_valid , resid 313 and blastp_afP21882 and chain A and name cb, resid 175 and blastp_afP21882 and chain A and name cb
dist intra_2408_valid , resid 313 and blastp_afP21882 and chain A and name cb, resid 321 and blastp_afP21882 and chain A and name cb
dist intra_3602_unknown , resid 219 and blastp_afP21882 and chain A and name cb, resid 164 and blastp_afP21882 and chain A and name cb
dist intra_5303_unknown , resid 292 and blastp_afP21882 and chain A and name cb, resid 321 and blastp_afP21882 and chain A and name cb
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
save blastp_afP21882.pse
png blastp_afP21882.png
