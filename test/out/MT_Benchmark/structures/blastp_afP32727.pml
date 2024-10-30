load blastp_afP32727.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP32727
color 3, chain A
show cartoon, chain A
dist intra_116_valid , resid 14 and blastp_afP32727 and chain A and name cb, resid 111 and blastp_afP32727 and chain A and name cb
dist intra_209_valid , resid 148 and blastp_afP32727 and chain A and name cb, resid 190 and blastp_afP32727 and chain A and name cb
dist intra_297_valid , resid 205 and blastp_afP32727 and chain A and name cb, resid 329 and blastp_afP32727 and chain A and name cb
dist intra_833_valid , resid 184 and blastp_afP32727 and chain A and name cb, resid 148 and blastp_afP32727 and chain A and name cb
dist intra_1393_valid , resid 190 and blastp_afP32727 and chain A and name cb, resid 111 and blastp_afP32727 and chain A and name cb
dist intra_1576_valid , resid 16 and blastp_afP32727 and chain A and name cb, resid 111 and blastp_afP32727 and chain A and name cb
dist intra_1693_valid , resid 187 and blastp_afP32727 and chain A and name cb, resid 111 and blastp_afP32727 and chain A and name cb
dist intra_3297_valid , resid 205 and blastp_afP32727 and chain A and name cb, resid 223 and blastp_afP32727 and chain A and name cb
dist intra_4728_valid , resid 173 and blastp_afP32727 and chain A and name cb, resid 266 and blastp_afP32727 and chain A and name cb
dist intra_5279_valid , resid 184 and blastp_afP32727 and chain A and name cb, resid 190 and blastp_afP32727 and chain A and name cb
dist intra_2015_out_range , resid 179 and blastp_afP32727 and chain A and name cb, resid 111 and blastp_afP32727 and chain A and name cb
dist intra_2645_out_range , resid 205 and blastp_afP32727 and chain A and name cb, resid 111 and blastp_afP32727 and chain A and name cb
dist intra_1817_unknown , resid 1 and blastp_afP32727 and chain A and name cb, resid 111 and blastp_afP32727 and chain A and name cb
dist intra_4724_unknown , resid 185 and blastp_afP32727 and chain A and name cb, resid 111 and blastp_afP32727 and chain A and name cb
dist intra_5115_unknown , resid 157 and blastp_afP32727 and chain A and name cb, resid 266 and blastp_afP32727 and chain A and name cb
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
save blastp_afP32727.pse
png blastp_afP32727.png
