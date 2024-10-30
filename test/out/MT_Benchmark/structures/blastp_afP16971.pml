load blastp_afP16971.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP16971
color 3, chain A
show cartoon, chain A
dist intra_2102_valid , resid 248 and blastp_afP16971 and chain A and name cb, resid 214 and blastp_afP16971 and chain A and name cb
dist intra_2373_valid , resid 182 and blastp_afP16971 and chain A and name cb, resid 21 and blastp_afP16971 and chain A and name cb
dist intra_2471_valid , resid 26 and blastp_afP16971 and chain A and name cb, resid 248 and blastp_afP16971 and chain A and name cb
dist intra_3254_valid , resid 182 and blastp_afP16971 and chain A and name cb, resid 248 and blastp_afP16971 and chain A and name cb
dist intra_4279_valid , resid 182 and blastp_afP16971 and chain A and name cb, resid 13 and blastp_afP16971 and chain A and name cb
dist intra_6008_valid , resid 182 and blastp_afP16971 and chain A and name cb, resid 17 and blastp_afP16971 and chain A and name cb
dist intra_2623_same , resid 196 and blastp_afP16971 and chain A and name cb, resid 196 and blastp_afP16971 and chain A and name cb
dist intra_950_unknown , resid 182 and blastp_afP16971 and chain A and name cb, resid 30 and blastp_afP16971 and chain A and name cb
dist intra_1564_unknown , resid 30 and blastp_afP16971 and chain A and name cb, resid 248 and blastp_afP16971 and chain A and name cb
dist intra_5003_unknown , resid 17 and blastp_afP16971 and chain A and name cb, resid 30 and blastp_afP16971 and chain A and name cb
dist intra_5514_unknown , resid 27 and blastp_afP16971 and chain A and name cb, resid 182 and blastp_afP16971 and chain A and name cb
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
save blastp_afP16971.pse
png blastp_afP16971.png
