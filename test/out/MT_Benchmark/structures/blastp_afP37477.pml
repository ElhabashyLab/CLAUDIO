load blastp_afP37477.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP37477
color 3, chain A
show cartoon, chain A
dist intra_667_valid , resid 135 and blastp_afP37477 and chain A and name cb, resid 123 and blastp_afP37477 and chain A and name cb
dist intra_2760_valid , resid 177 and blastp_afP37477 and chain A and name cb, resid 185 and blastp_afP37477 and chain A and name cb
dist intra_6058_valid , resid 135 and blastp_afP37477 and chain A and name cb, resid 55 and blastp_afP37477 and chain A and name cb
dist intra_3075_overlaps , resid 2 and blastp_afP37477 and chain A and name cb, resid 435 and blastp_afP37477 and chain A and name cb
dist intra_27_unknown , resid 157 and blastp_afP37477 and chain A and name cb, resid 2 and blastp_afP37477 and chain A and name cb
dist intra_134_unknown , resid 152 and blastp_afP37477 and chain A and name cb, resid 2 and blastp_afP37477 and chain A and name cb
dist intra_585_unknown , resid 2 and blastp_afP37477 and chain A and name cb, resid 440 and blastp_afP37477 and chain A and name cb
dist intra_1298_unknown , resid 2 and blastp_afP37477 and chain A and name cb, resid 98 and blastp_afP37477 and chain A and name cb
dist intra_2196_unknown , resid 152 and blastp_afP37477 and chain A and name cb, resid 177 and blastp_afP37477 and chain A and name cb
dist intra_5046_unknown , resid 398 and blastp_afP37477 and chain A and name cb, resid 2 and blastp_afP37477 and chain A and name cb
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
save blastp_afP37477.pse
png blastp_afP37477.png
