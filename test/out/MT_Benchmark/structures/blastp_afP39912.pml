load blastp_afP39912.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP39912
color 3, chain A
show cartoon, chain A
dist intra_626_valid , resid 32 and blastp_afP39912 and chain A and name cb, resid 100 and blastp_afP39912 and chain A and name cb
dist intra_834_valid , resid 92 and blastp_afP39912 and chain A and name cb, resid 38 and blastp_afP39912 and chain A and name cb
dist intra_987_valid , resid 100 and blastp_afP39912 and chain A and name cb, resid 92 and blastp_afP39912 and chain A and name cb
dist intra_996_valid , resid 225 and blastp_afP39912 and chain A and name cb, resid 113 and blastp_afP39912 and chain A and name cb
dist intra_1126_valid , resid 32 and blastp_afP39912 and chain A and name cb, resid 38 and blastp_afP39912 and chain A and name cb
dist intra_1863_valid , resid 351 and blastp_afP39912 and chain A and name cb, resid 143 and blastp_afP39912 and chain A and name cb
dist intra_4580_valid , resid 143 and blastp_afP39912 and chain A and name cb, resid 355 and blastp_afP39912 and chain A and name cb
dist intra_5397_overlaps , resid 2 and blastp_afP39912 and chain A and name cb, resid 36 and blastp_afP39912 and chain A and name cb
dist intra_1416_unknown , resid 38 and blastp_afP39912 and chain A and name cb, resid 2 and blastp_afP39912 and chain A and name cb
dist intra_3861_unknown , resid 2 and blastp_afP39912 and chain A and name cb, resid 12 and blastp_afP39912 and chain A and name cb
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
save blastp_afP39912.pse
png blastp_afP39912.png
