load blastp_afP94544.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP94544
color 3, chain A
show cartoon, chain A
dist intra_3397_valid , resid 148 and blastp_afP94544 and chain A and name cb, resid 92 and blastp_afP94544 and chain A and name cb
dist intra_3644_valid , resid 148 and blastp_afP94544 and chain A and name cb, resid 117 and blastp_afP94544 and chain A and name cb
dist intra_3974_valid , resid 217 and blastp_afP94544 and chain A and name cb, resid 92 and blastp_afP94544 and chain A and name cb
dist intra_4477_valid , resid 32 and blastp_afP94544 and chain A and name cb, resid 26 and blastp_afP94544 and chain A and name cb
dist intra_4579_valid , resid 103 and blastp_afP94544 and chain A and name cb, resid 99 and blastp_afP94544 and chain A and name cb
dist intra_6139_valid , resid 99 and blastp_afP94544 and chain A and name cb, resid 106 and blastp_afP94544 and chain A and name cb
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
save blastp_afP94544.pse
png blastp_afP94544.png
