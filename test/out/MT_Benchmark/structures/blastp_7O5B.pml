load blastp_7O5B.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain g
show surface, chain g and blastp_7O5B
color 3, chain g
show cartoon, chain g
hide everything, show cartoon, chain a
show surface, chain a and blastp_7O5B
color 5, chain a
show cartoon, chain a
dist intra_571_valid , resid 65 and blastp_7O5B and chain g and name cb, resid 20 and blastp_7O5B and chain g and name cb
dist intra_641_valid , resid 203 and blastp_7O5B and chain a and name cb, resid 81 and blastp_7O5B and chain a and name cb
dist intra_1076_valid , resid 63 and blastp_7O5B and chain a and name cb, resid 71 and blastp_7O5B and chain a and name cb
dist intra_1273_valid , resid 59 and blastp_7O5B and chain a and name cb, resid 77 and blastp_7O5B and chain a and name cb
dist intra_1543_valid , resid 71 and blastp_7O5B and chain a and name cb, resid 38 and blastp_7O5B and chain a and name cb
dist intra_1604_valid , resid 197 and blastp_7O5B and chain a and name cb, resid 59 and blastp_7O5B and chain a and name cb
dist intra_2178_valid , resid 59 and blastp_7O5B and chain a and name cb, resid 71 and blastp_7O5B and chain a and name cb
dist intra_2999_valid , resid 65 and blastp_7O5B and chain g and name cb, resid 18 and blastp_7O5B and chain g and name cb
dist intra_3701_valid , resid 197 and blastp_7O5B and chain a and name cb, resid 71 and blastp_7O5B and chain a and name cb
dist intra_3745_valid , resid 66 and blastp_7O5B and chain a and name cb, resid 77 and blastp_7O5B and chain a and name cb
dist intra_4207_valid , resid 64 and blastp_7O5B and chain g and name cb, resid 20 and blastp_7O5B and chain g and name cb
dist intra_4522_valid , resid 63 and blastp_7O5B and chain a and name cb, resid 56 and blastp_7O5B and chain a and name cb
dist intra_4732_valid , resid 27 and blastp_7O5B and chain g and name cb, resid 48 and blastp_7O5B and chain g and name cb
dist intra_4988_valid , resid 158 and blastp_7O5B and chain a and name cb, resid 124 and blastp_7O5B and chain a and name cb
dist intra_5085_valid , resid 197 and blastp_7O5B and chain a and name cb, resid 117 and blastp_7O5B and chain a and name cb
dist intra_5399_valid , resid 197 and blastp_7O5B and chain a and name cb, resid 63 and blastp_7O5B and chain a and name cb
dist intra_5620_valid , resid 117 and blastp_7O5B and chain a and name cb, resid 196 and blastp_7O5B and chain a and name cb
dist intra_5937_valid , resid 77 and blastp_7O5B and chain a and name cb, resid 81 and blastp_7O5B and chain a and name cb
dist intra_4240_out_range , resid 77 and blastp_7O5B and chain a and name cb, resid 158 and blastp_7O5B and chain a and name cb
dist intra_5312_out_range , resid 81 and blastp_7O5B and chain a and name cb, resid 158 and blastp_7O5B and chain a and name cb
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
save blastp_7O5B.pse
png blastp_7O5B.png
