load blastp_5OLN.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_5OLN
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_5OLN
color 5, chain B
show cartoon, chain B
dist intra_101_valid , resid 162 and blastp_5OLN and chain A and name cb, resid 187 and blastp_5OLN and chain A and name cb
dist intra_101_4_valid , resid 162 and blastp_5OLN and chain B and name cb, resid 187 and blastp_5OLN and chain B and name cb
dist intra_456_valid , resid 383 and blastp_5OLN and chain A and name cb, resid 422 and blastp_5OLN and chain A and name cb
dist intra_456_4_valid , resid 383 and blastp_5OLN and chain B and name cb, resid 422 and blastp_5OLN and chain B and name cb
dist intra_655_valid , resid 368 and blastp_5OLN and chain A and name cb, resid 162 and blastp_5OLN and chain A and name cb
dist intra_655_4_valid , resid 368 and blastp_5OLN and chain B and name cb, resid 162 and blastp_5OLN and chain B and name cb
dist intra_684_valid , resid 141 and blastp_5OLN and chain A and name cb, resid 314 and blastp_5OLN and chain A and name cb
dist intra_684_4_valid , resid 141 and blastp_5OLN and chain B and name cb, resid 314 and blastp_5OLN and chain B and name cb
dist intra_884_valid , resid 285 and blastp_5OLN and chain A and name cb, resid 147 and blastp_5OLN and chain A and name cb
dist intra_884_4_valid , resid 285 and blastp_5OLN and chain B and name cb, resid 147 and blastp_5OLN and chain B and name cb
dist intra_1628_valid , resid 295 and blastp_5OLN and chain A and name cb, resid 304 and blastp_5OLN and chain A and name cb
dist intra_1628_4_valid , resid 295 and blastp_5OLN and chain B and name cb, resid 304 and blastp_5OLN and chain B and name cb
dist intra_1689_valid , resid 285 and blastp_5OLN and chain A and name cb, resid 304 and blastp_5OLN and chain A and name cb
dist intra_1689_4_valid , resid 285 and blastp_5OLN and chain B and name cb, resid 304 and blastp_5OLN and chain B and name cb
dist intra_1865_valid , resid 422 and blastp_5OLN and chain A and name cb, resid 387 and blastp_5OLN and chain A and name cb
dist intra_1865_4_valid , resid 422 and blastp_5OLN and chain B and name cb, resid 387 and blastp_5OLN and chain B and name cb
dist intra_2805_valid , resid 209 and blastp_5OLN and chain A and name cb, resid 187 and blastp_5OLN and chain A and name cb
dist intra_2805_4_valid , resid 209 and blastp_5OLN and chain B and name cb, resid 187 and blastp_5OLN and chain B and name cb
dist intra_3049_valid , resid 368 and blastp_5OLN and chain A and name cb, resid 187 and blastp_5OLN and chain A and name cb
dist intra_3049_4_valid , resid 368 and blastp_5OLN and chain B and name cb, resid 187 and blastp_5OLN and chain B and name cb
dist intra_3156_valid , resid 162 and blastp_5OLN and chain A and name cb, resid 188 and blastp_5OLN and chain A and name cb
dist intra_3156_4_valid , resid 162 and blastp_5OLN and chain B and name cb, resid 188 and blastp_5OLN and chain B and name cb
dist intra_5266_valid , resid 285 and blastp_5OLN and chain A and name cb, resid 295 and blastp_5OLN and chain A and name cb
dist intra_5266_4_valid , resid 285 and blastp_5OLN and chain B and name cb, resid 295 and blastp_5OLN and chain B and name cb
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
save blastp_5OLN.pse
png blastp_5OLN.png
