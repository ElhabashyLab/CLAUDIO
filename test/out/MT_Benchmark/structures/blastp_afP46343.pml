load blastp_afP46343.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP46343
color 3, chain A
show cartoon, chain A
dist intra_418_valid , resid 150 and blastp_afP46343 and chain A and name cb, resid 128 and blastp_afP46343 and chain A and name cb
dist intra_2466_valid , resid 90 and blastp_afP46343 and chain A and name cb, resid 86 and blastp_afP46343 and chain A and name cb
dist intra_2883_valid , resid 276 and blastp_afP46343 and chain A and name cb, resid 260 and blastp_afP46343 and chain A and name cb
dist intra_2925_valid , resid 109 and blastp_afP46343 and chain A and name cb, resid 162 and blastp_afP46343 and chain A and name cb
dist intra_3440_valid , resid 276 and blastp_afP46343 and chain A and name cb, resid 317 and blastp_afP46343 and chain A and name cb
dist intra_6019_valid , resid 116 and blastp_afP46343 and chain A and name cb, resid 86 and blastp_afP46343 and chain A and name cb
dist intra_1495_overlaps , resid 276 and blastp_afP46343 and chain A and name cb, resid 273 and blastp_afP46343 and chain A and name cb
dist intra_2826_unknown , resid 150 and blastp_afP46343 and chain A and name cb, resid 122 and blastp_afP46343 and chain A and name cb
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
save blastp_afP46343.pse
png blastp_afP46343.png
