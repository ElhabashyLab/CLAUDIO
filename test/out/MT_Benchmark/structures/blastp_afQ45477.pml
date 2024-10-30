load blastp_afQ45477.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afQ45477
color 3, chain A
show cartoon, chain A
dist intra_342_valid , resid 107 and blastp_afQ45477 and chain A and name cb, resid 401 and blastp_afQ45477 and chain A and name cb
dist intra_1020_valid , resid 831 and blastp_afQ45477 and chain A and name cb, resid 896 and blastp_afQ45477 and chain A and name cb
dist intra_1230_valid , resid 107 and blastp_afQ45477 and chain A and name cb, resid 597 and blastp_afQ45477 and chain A and name cb
dist intra_2781_valid , resid 123 and blastp_afQ45477 and chain A and name cb, resid 157 and blastp_afQ45477 and chain A and name cb
dist intra_3365_valid , resid 597 and blastp_afQ45477 and chain A and name cb, resid 610 and blastp_afQ45477 and chain A and name cb
dist intra_3650_valid , resid 400 and blastp_afQ45477 and chain A and name cb, resid 597 and blastp_afQ45477 and chain A and name cb
dist intra_3660_valid , resid 430 and blastp_afQ45477 and chain A and name cb, resid 579 and blastp_afQ45477 and chain A and name cb
dist intra_3977_valid , resid 824 and blastp_afQ45477 and chain A and name cb, resid 882 and blastp_afQ45477 and chain A and name cb
dist intra_4301_valid , resid 114 and blastp_afQ45477 and chain A and name cb, resid 401 and blastp_afQ45477 and chain A and name cb
dist intra_4703_valid , resid 219 and blastp_afQ45477 and chain A and name cb, resid 290 and blastp_afQ45477 and chain A and name cb
dist intra_5160_valid , resid 141 and blastp_afQ45477 and chain A and name cb, resid 29 and blastp_afQ45477 and chain A and name cb
dist intra_5264_valid , resid 29 and blastp_afQ45477 and chain A and name cb, resid 610 and blastp_afQ45477 and chain A and name cb
dist intra_2771_unknown , resid 82 and blastp_afQ45477 and chain A and name cb, resid 401 and blastp_afQ45477 and chain A and name cb
dist intra_4672_unknown , resid 82 and blastp_afQ45477 and chain A and name cb, resid 400 and blastp_afQ45477 and chain A and name cb
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
save blastp_afQ45477.pse
png blastp_afQ45477.png
