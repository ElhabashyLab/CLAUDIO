load blastp_1DKR.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_1DKR
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_1DKR
color 5, chain B
show cartoon, chain B
dist intra_784_4_valid , resid 22 and blastp_1DKR and chain B and name cb, resid 7 and blastp_1DKR and chain B and name cb
dist intra_1456_valid , resid 290 and blastp_1DKR and chain A and name cb, resid 270 and blastp_1DKR and chain A and name cb
dist intra_1456_4_valid , resid 290 and blastp_1DKR and chain B and name cb, resid 270 and blastp_1DKR and chain B and name cb
dist intra_1862_valid , resid 279 and blastp_1DKR and chain A and name cb, resid 22 and blastp_1DKR and chain A and name cb
dist intra_1862_4_valid , resid 279 and blastp_1DKR and chain B and name cb, resid 22 and blastp_1DKR and chain B and name cb
dist intra_3370_4_valid , resid 7 and blastp_1DKR and chain B and name cb, resid 88 and blastp_1DKR and chain B and name cb
dist intra_471_4_overlaps , resid 34 and blastp_1DKR and chain B and name cb, resid 7 and blastp_1DKR and chain B and name cb
dist intra_3497_overlaps , resid 197 and blastp_1DKR and chain A and name cb, resid 189 and blastp_1DKR and chain A and name cb
dist inter_3497_2_valid , resid 197 and blastp_1DKR and chain A and name cb, resid 189 and blastp_1DKR and chain B and name cb
dist inter_3497_3_valid , resid 197 and blastp_1DKR and chain B and name cb, resid 189 and blastp_1DKR and chain A and name cb
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
save blastp_1DKR.pse
png blastp_1DKR.png
