load blastp_afP54542.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP54542
color 3, chain A
show cartoon, chain A
dist intra_370_valid , resid 22 and blastp_afP54542 and chain A and name cb, resid 180 and blastp_afP54542 and chain A and name cb
dist intra_1186_valid , resid 262 and blastp_afP54542 and chain A and name cb, resid 212 and blastp_afP54542 and chain A and name cb
dist intra_4464_valid , resid 256 and blastp_afP54542 and chain A and name cb, resid 212 and blastp_afP54542 and chain A and name cb
dist intra_1479_out_range , resid 180 and blastp_afP54542 and chain A and name cb, resid 198 and blastp_afP54542 and chain A and name cb
dist intra_1037_overlaps , resid 212 and blastp_afP54542 and chain A and name cb, resid 208 and blastp_afP54542 and chain A and name cb
dist intra_1124_unknown , resid 198 and blastp_afP54542 and chain A and name cb, resid 349 and blastp_afP54542 and chain A and name cb
dist intra_1831_unknown , resid 188 and blastp_afP54542 and chain A and name cb, resid 349 and blastp_afP54542 and chain A and name cb
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
save blastp_afP54542.pse
png blastp_afP54542.png
