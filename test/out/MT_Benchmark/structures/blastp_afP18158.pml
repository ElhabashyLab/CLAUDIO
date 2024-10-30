load blastp_afP18158.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP18158
color 3, chain A
show cartoon, chain A
dist intra_39_valid , resid 537 and blastp_afP18158 and chain A and name cb, resid 218 and blastp_afP18158 and chain A and name cb
dist intra_44_valid , resid 135 and blastp_afP18158 and chain A and name cb, resid 422 and blastp_afP18158 and chain A and name cb
dist intra_50_valid , resid 218 and blastp_afP18158 and chain A and name cb, resid 196 and blastp_afP18158 and chain A and name cb
dist intra_63_valid , resid 537 and blastp_afP18158 and chain A and name cb, resid 196 and blastp_afP18158 and chain A and name cb
dist intra_98_valid , resid 409 and blastp_afP18158 and chain A and name cb, resid 135 and blastp_afP18158 and chain A and name cb
dist intra_144_valid , resid 246 and blastp_afP18158 and chain A and name cb, resid 301 and blastp_afP18158 and chain A and name cb
dist intra_189_valid , resid 88 and blastp_afP18158 and chain A and name cb, resid 409 and blastp_afP18158 and chain A and name cb
dist intra_227_valid , resid 82 and blastp_afP18158 and chain A and name cb, resid 409 and blastp_afP18158 and chain A and name cb
dist intra_326_valid , resid 151 and blastp_afP18158 and chain A and name cb, resid 269 and blastp_afP18158 and chain A and name cb
dist intra_336_valid , resid 446 and blastp_afP18158 and chain A and name cb, resid 433 and blastp_afP18158 and chain A and name cb
dist intra_614_valid , resid 431 and blastp_afP18158 and chain A and name cb, resid 446 and blastp_afP18158 and chain A and name cb
dist intra_1012_valid , resid 242 and blastp_afP18158 and chain A and name cb, resid 196 and blastp_afP18158 and chain A and name cb
dist intra_2680_valid , resid 359 and blastp_afP18158 and chain A and name cb, resid 382 and blastp_afP18158 and chain A and name cb
dist intra_3667_valid , resid 88 and blastp_afP18158 and chain A and name cb, resid 382 and blastp_afP18158 and chain A and name cb
dist intra_4069_valid , resid 382 and blastp_afP18158 and chain A and name cb, resid 409 and blastp_afP18158 and chain A and name cb
dist intra_4807_valid , resid 46 and blastp_afP18158 and chain A and name cb, resid 401 and blastp_afP18158 and chain A and name cb
dist intra_5122_valid , resid 222 and blastp_afP18158 and chain A and name cb, resid 20 and blastp_afP18158 and chain A and name cb
dist intra_5141_valid , resid 146 and blastp_afP18158 and chain A and name cb, resid 161 and blastp_afP18158 and chain A and name cb
dist intra_5851_valid , resid 66 and blastp_afP18158 and chain A and name cb, resid 196 and blastp_afP18158 and chain A and name cb
dist intra_5633_overlaps , resid 183 and blastp_afP18158 and chain A and name cb, resid 1 and blastp_afP18158 and chain A and name cb
dist intra_292_unknown , resid 408 and blastp_afP18158 and chain A and name cb, resid 88 and blastp_afP18158 and chain A and name cb
dist intra_344_unknown , resid 537 and blastp_afP18158 and chain A and name cb, resid 187 and blastp_afP18158 and chain A and name cb
dist intra_503_unknown , resid 186 and blastp_afP18158 and chain A and name cb, resid 1 and blastp_afP18158 and chain A and name cb
dist intra_1131_unknown , resid 20 and blastp_afP18158 and chain A and name cb, resid 1 and blastp_afP18158 and chain A and name cb
dist intra_1387_unknown , resid 135 and blastp_afP18158 and chain A and name cb, resid 410 and blastp_afP18158 and chain A and name cb
dist intra_2163_unknown , resid 1 and blastp_afP18158 and chain A and name cb, resid 47 and blastp_afP18158 and chain A and name cb
dist intra_2681_unknown , resid 408 and blastp_afP18158 and chain A and name cb, resid 135 and blastp_afP18158 and chain A and name cb
dist intra_3225_unknown , resid 537 and blastp_afP18158 and chain A and name cb, resid 207 and blastp_afP18158 and chain A and name cb
dist intra_3292_unknown , resid 408 and blastp_afP18158 and chain A and name cb, resid 82 and blastp_afP18158 and chain A and name cb
dist intra_3845_unknown , resid 408 and blastp_afP18158 and chain A and name cb, resid 382 and blastp_afP18158 and chain A and name cb
dist intra_3960_unknown , resid 47 and blastp_afP18158 and chain A and name cb, resid 395 and blastp_afP18158 and chain A and name cb
dist intra_4017_unknown , resid 242 and blastp_afP18158 and chain A and name cb, resid 187 and blastp_afP18158 and chain A and name cb
dist intra_4202_unknown , resid 207 and blastp_afP18158 and chain A and name cb, resid 196 and blastp_afP18158 and chain A and name cb
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
save blastp_afP18158.pse
png blastp_afP18158.png
