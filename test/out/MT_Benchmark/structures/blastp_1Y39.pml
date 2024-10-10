load blastp_1Y39.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_1Y39
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_1Y39
color 5, chain B
show cartoon, chain B
dist intra_192_valid , resid 16 and blastp_1Y39 and chain A and name cb, resid 47 and blastp_1Y39 and chain A and name cb
dist intra_192_4_valid , resid 216 and blastp_1Y39 and chain B and name cb, resid 247 and blastp_1Y39 and chain B and name cb
dist intra_819_valid , resid 6 and blastp_1Y39 and chain A and name cb, resid 47 and blastp_1Y39 and chain A and name cb
dist intra_819_4_valid , resid 206 and blastp_1Y39 and chain B and name cb, resid 247 and blastp_1Y39 and chain B and name cb
dist intra_1506_valid , resid 39 and blastp_1Y39 and chain A and name cb, resid 16 and blastp_1Y39 and chain A and name cb
dist intra_1506_4_valid , resid 239 and blastp_1Y39 and chain B and name cb, resid 216 and blastp_1Y39 and chain B and name cb
dist intra_2274_valid , resid 31 and blastp_1Y39 and chain A and name cb, resid 16 and blastp_1Y39 and chain A and name cb
dist intra_2274_4_valid , resid 231 and blastp_1Y39 and chain B and name cb, resid 216 and blastp_1Y39 and chain B and name cb
dist intra_2426_valid , resid 15 and blastp_1Y39 and chain A and name cb, resid 31 and blastp_1Y39 and chain A and name cb
dist intra_2426_4_valid , resid 215 and blastp_1Y39 and chain B and name cb, resid 231 and blastp_1Y39 and chain B and name cb
dist intra_2677_valid , resid 16 and blastp_1Y39 and chain A and name cb, resid 6 and blastp_1Y39 and chain A and name cb
dist intra_2677_4_valid , resid 216 and blastp_1Y39 and chain B and name cb, resid 206 and blastp_1Y39 and chain B and name cb
dist intra_5447_valid , resid 15 and blastp_1Y39 and chain A and name cb, resid 36 and blastp_1Y39 and chain A and name cb
dist intra_5447_4_valid , resid 215 and blastp_1Y39 and chain B and name cb, resid 236 and blastp_1Y39 and chain B and name cb
dist intra_5714_valid , resid 15 and blastp_1Y39 and chain A and name cb, resid 47 and blastp_1Y39 and chain A and name cb
dist intra_5714_4_valid , resid 215 and blastp_1Y39 and chain B and name cb, resid 247 and blastp_1Y39 and chain B and name cb
dist inter_1506_3_valid , resid 239 and blastp_1Y39 and chain B and name cb, resid 16 and blastp_1Y39 and chain A and name cb
dist inter_2274_3_valid , resid 231 and blastp_1Y39 and chain B and name cb, resid 16 and blastp_1Y39 and chain A and name cb
dist inter_2426_2_valid , resid 15 and blastp_1Y39 and chain A and name cb, resid 231 and blastp_1Y39 and chain B and name cb
dist inter_5714_2_valid , resid 15 and blastp_1Y39 and chain A and name cb, resid 247 and blastp_1Y39 and chain B and name cb
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
save blastp_1Y39.pse
png blastp_1Y39.png
