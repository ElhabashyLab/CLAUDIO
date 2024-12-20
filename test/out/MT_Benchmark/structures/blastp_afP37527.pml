load blastp_afP37527.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP37527
color 3, chain A
show cartoon, chain A
dist intra_1514_valid , resid 276 and blastp_afP37527 and chain A and name cb, resid 246 and blastp_afP37527 and chain A and name cb
dist intra_3869_overlaps , resid 2 and blastp_afP37527 and chain A and name cb, resid 250 and blastp_afP37527 and chain A and name cb
dist intra_1596_unknown , resid 149 and blastp_afP37527 and chain A and name cb, resid 174 and blastp_afP37527 and chain A and name cb
dist intra_1906_unknown , resid 2 and blastp_afP37527 and chain A and name cb, resid 262 and blastp_afP37527 and chain A and name cb
dist intra_2329_unknown , resid 148 and blastp_afP37527 and chain A and name cb, resid 187 and blastp_afP37527 and chain A and name cb
dist intra_3129_unknown , resid 2 and blastp_afP37527 and chain A and name cb, resid 18 and blastp_afP37527 and chain A and name cb
dist intra_4188_unknown , resid 2 and blastp_afP37527 and chain A and name cb, resid 246 and blastp_afP37527 and chain A and name cb
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
save blastp_afP37527.pse
png blastp_afP37527.png
