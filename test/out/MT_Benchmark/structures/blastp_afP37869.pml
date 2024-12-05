load blastp_afP37869.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP37869
color 3, chain A
show cartoon, chain A
dist intra_725_unknown , resid 229 and blastp_afP37869 and chain A and name cb, resid 430 and blastp_afP37869 and chain A and name cb
dist intra_736_unknown , resid 308 and blastp_afP37869 and chain A and name cb, resid 324 and blastp_afP37869 and chain A and name cb
dist intra_1961_unknown , resid 409 and blastp_afP37869 and chain A and name cb, resid 323 and blastp_afP37869 and chain A and name cb
dist intra_2216_unknown , resid 409 and blastp_afP37869 and chain A and name cb, resid 308 and blastp_afP37869 and chain A and name cb
dist intra_2752_unknown , resid 409 and blastp_afP37869 and chain A and name cb, resid 238 and blastp_afP37869 and chain A and name cb
dist intra_3611_unknown , resid 409 and blastp_afP37869 and chain A and name cb, resid 329 and blastp_afP37869 and chain A and name cb
dist intra_4351_unknown , resid 323 and blastp_afP37869 and chain A and name cb, resid 281 and blastp_afP37869 and chain A and name cb
dist intra_4776_unknown , resid 322 and blastp_afP37869 and chain A and name cb, resid 324 and blastp_afP37869 and chain A and name cb
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
save blastp_afP37869.pse
png blastp_afP37869.png
