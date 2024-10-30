load blastp_afP39814.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP39814
color 3, chain A
show cartoon, chain A
dist intra_1398_valid , resid 560 and blastp_afP39814 and chain A and name cb, resid 556 and blastp_afP39814 and chain A and name cb
dist intra_2539_valid , resid 15 and blastp_afP39814 and chain A and name cb, resid 28 and blastp_afP39814 and chain A and name cb
dist intra_2853_valid , resid 160 and blastp_afP39814 and chain A and name cb, resid 156 and blastp_afP39814 and chain A and name cb
dist intra_3178_valid , resid 355 and blastp_afP39814 and chain A and name cb, resid 372 and blastp_afP39814 and chain A and name cb
dist intra_4954_valid , resid 422 and blastp_afP39814 and chain A and name cb, resid 467 and blastp_afP39814 and chain A and name cb
dist intra_5901_valid , resid 68 and blastp_afP39814 and chain A and name cb, resid 60 and blastp_afP39814 and chain A and name cb
dist intra_3677_unknown , resid 336 and blastp_afP39814 and chain A and name cb, resid 330 and blastp_afP39814 and chain A and name cb
dist intra_3823_unknown , resid 408 and blastp_afP39814 and chain A and name cb, resid 429 and blastp_afP39814 and chain A and name cb
dist intra_5342_unknown , resid 330 and blastp_afP39814 and chain A and name cb, resid 247 and blastp_afP39814 and chain A and name cb
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
save blastp_afP39814.pse
png blastp_afP39814.png
