load blastp_afP80861.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP80861
color 3, chain A
show cartoon, chain A
dist intra_0_valid , resid 37 and blastp_afP80861 and chain A and name cb, resid 134 and blastp_afP80861 and chain A and name cb
dist intra_383_valid , resid 220 and blastp_afP80861 and chain A and name cb, resid 351 and blastp_afP80861 and chain A and name cb
dist intra_473_valid , resid 220 and blastp_afP80861 and chain A and name cb, resid 189 and blastp_afP80861 and chain A and name cb
dist intra_1536_valid , resid 220 and blastp_afP80861 and chain A and name cb, resid 183 and blastp_afP80861 and chain A and name cb
dist intra_3610_valid , resid 71 and blastp_afP80861 and chain A and name cb, resid 66 and blastp_afP80861 and chain A and name cb
dist intra_1287_out_range , resid 338 and blastp_afP80861 and chain A and name cb, resid 220 and blastp_afP80861 and chain A and name cb
dist intra_1297_out_range , resid 338 and blastp_afP80861 and chain A and name cb, resid 183 and blastp_afP80861 and chain A and name cb
dist intra_2026_out_range , resid 338 and blastp_afP80861 and chain A and name cb, resid 351 and blastp_afP80861 and chain A and name cb
dist intra_2813_unknown , resid 338 and blastp_afP80861 and chain A and name cb, resid 189 and blastp_afP80861 and chain A and name cb
dist intra_2943_unknown , resid 351 and blastp_afP80861 and chain A and name cb, resid 214 and blastp_afP80861 and chain A and name cb
dist intra_3893_unknown , resid 220 and blastp_afP80861 and chain A and name cb, resid 333 and blastp_afP80861 and chain A and name cb
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
save blastp_afP80861.pse
png blastp_afP80861.png
