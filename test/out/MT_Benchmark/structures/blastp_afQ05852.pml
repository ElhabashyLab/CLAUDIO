load blastp_afQ05852.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afQ05852
color 3, chain A
show cartoon, chain A
dist intra_1242_valid , resid 89 and blastp_afQ05852 and chain A and name cb, resid 92 and blastp_afQ05852 and chain A and name cb
dist intra_812_out_range , resid 83 and blastp_afQ05852 and chain A and name cb, resid 191 and blastp_afQ05852 and chain A and name cb
dist intra_2249_same , resid 186 and blastp_afQ05852 and chain A and name cb, resid 186 and blastp_afQ05852 and chain A and name cb
dist intra_1751_unknown , resid 187 and blastp_afQ05852 and chain A and name cb, resid 83 and blastp_afQ05852 and chain A and name cb
dist intra_3496_unknown , resid 83 and blastp_afQ05852 and chain A and name cb, resid 194 and blastp_afQ05852 and chain A and name cb
dist intra_4110_unknown , resid 191 and blastp_afQ05852 and chain A and name cb, resid 81 and blastp_afQ05852 and chain A and name cb
dist intra_5863_unknown , resid 81 and blastp_afQ05852 and chain A and name cb, resid 194 and blastp_afQ05852 and chain A and name cb
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
save blastp_afQ05852.pse
png blastp_afQ05852.png
