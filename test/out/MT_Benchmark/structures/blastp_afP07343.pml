load blastp_afP07343.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP07343
color 3, chain A
show cartoon, chain A
dist intra_306_valid , resid 14 and blastp_afP07343 and chain A and name cb, resid 29 and blastp_afP07343 and chain A and name cb
dist intra_690_valid , resid 459 and blastp_afP07343 and chain A and name cb, resid 174 and blastp_afP07343 and chain A and name cb
dist intra_1182_valid , resid 38 and blastp_afP07343 and chain A and name cb, resid 19 and blastp_afP07343 and chain A and name cb
dist intra_1251_valid , resid 19 and blastp_afP07343 and chain A and name cb, resid 29 and blastp_afP07343 and chain A and name cb
dist intra_1698_valid , resid 29 and blastp_afP07343 and chain A and name cb, resid 38 and blastp_afP07343 and chain A and name cb
dist intra_2293_valid , resid 250 and blastp_afP07343 and chain A and name cb, resid 59 and blastp_afP07343 and chain A and name cb
dist intra_2978_valid , resid 38 and blastp_afP07343 and chain A and name cb, resid 45 and blastp_afP07343 and chain A and name cb
dist intra_5023_valid , resid 14 and blastp_afP07343 and chain A and name cb, resid 33 and blastp_afP07343 and chain A and name cb
dist intra_5757_valid , resid 428 and blastp_afP07343 and chain A and name cb, resid 421 and blastp_afP07343 and chain A and name cb
dist intra_3195_same , resid 38 and blastp_afP07343 and chain A and name cb, resid 38 and blastp_afP07343 and chain A and name cb
dist intra_628_unknown , resid 5 and blastp_afP07343 and chain A and name cb, resid 29 and blastp_afP07343 and chain A and name cb
dist intra_1095_unknown , resid 45 and blastp_afP07343 and chain A and name cb, resid 69 and blastp_afP07343 and chain A and name cb
dist intra_3141_unknown , resid 428 and blastp_afP07343 and chain A and name cb, resid 394 and blastp_afP07343 and chain A and name cb
dist intra_3744_unknown , resid 8 and blastp_afP07343 and chain A and name cb, resid 29 and blastp_afP07343 and chain A and name cb
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
save blastp_afP07343.pse
png blastp_afP07343.png
