load blastp_7O9F.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_7O9F
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_7O9F
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain C
show surface, chain C and blastp_7O9F
color 7, chain C
show cartoon, chain C
dist intra_571_valid , resid 67 and blastp_7O9F and chain A and name cb, resid 22 and blastp_7O9F and chain A and name cb
dist intra_571_5_valid , resid 67 and blastp_7O9F and chain B and name cb, resid 22 and blastp_7O9F and chain B and name cb
dist intra_571_9_valid , resid 67 and blastp_7O9F and chain C and name cb, resid 22 and blastp_7O9F and chain C and name cb
dist intra_2999_valid , resid 67 and blastp_7O9F and chain A and name cb, resid 20 and blastp_7O9F and chain A and name cb
dist intra_2999_5_valid , resid 67 and blastp_7O9F and chain B and name cb, resid 20 and blastp_7O9F and chain B and name cb
dist intra_2999_9_valid , resid 67 and blastp_7O9F and chain C and name cb, resid 20 and blastp_7O9F and chain C and name cb
dist intra_4207_valid , resid 66 and blastp_7O9F and chain A and name cb, resid 22 and blastp_7O9F and chain A and name cb
dist intra_4207_5_valid , resid 66 and blastp_7O9F and chain B and name cb, resid 22 and blastp_7O9F and chain B and name cb
dist intra_4207_9_valid , resid 66 and blastp_7O9F and chain C and name cb, resid 22 and blastp_7O9F and chain C and name cb
dist intra_4732_valid , resid 29 and blastp_7O9F and chain A and name cb, resid 50 and blastp_7O9F and chain A and name cb
dist intra_4732_5_valid , resid 29 and blastp_7O9F and chain B and name cb, resid 50 and blastp_7O9F and chain B and name cb
dist intra_4732_9_valid , resid 29 and blastp_7O9F and chain C and name cb, resid 50 and blastp_7O9F and chain C and name cb
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
save blastp_7O9F.pse
png blastp_7O9F.png
