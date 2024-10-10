load blastp_1COZ.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_1COZ
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_1COZ
color 5, chain B
show cartoon, chain B
dist intra_673_valid , resid 47 and blastp_1COZ and chain A and name cb, resid 123 and blastp_1COZ and chain A and name cb
dist intra_673_4_valid , resid 547 and blastp_1COZ and chain B and name cb, resid 623 and blastp_1COZ and chain B and name cb
dist intra_2572_valid , resid 72 and blastp_1COZ and chain A and name cb, resid 121 and blastp_1COZ and chain A and name cb
dist intra_2572_4_valid , resid 572 and blastp_1COZ and chain B and name cb, resid 621 and blastp_1COZ and chain B and name cb
dist intra_3737_valid , resid 47 and blastp_1COZ and chain A and name cb, resid 121 and blastp_1COZ and chain A and name cb
dist intra_3737_4_valid , resid 547 and blastp_1COZ and chain B and name cb, resid 621 and blastp_1COZ and chain B and name cb
dist inter_673_2_valid , resid 47 and blastp_1COZ and chain A and name cb, resid 623 and blastp_1COZ and chain B and name cb
dist inter_673_3_valid , resid 547 and blastp_1COZ and chain B and name cb, resid 123 and blastp_1COZ and chain A and name cb
dist inter_2572_2_valid , resid 72 and blastp_1COZ and chain A and name cb, resid 621 and blastp_1COZ and chain B and name cb
dist inter_2572_3_valid , resid 572 and blastp_1COZ and chain B and name cb, resid 121 and blastp_1COZ and chain A and name cb
dist inter_3737_2_valid , resid 47 and blastp_1COZ and chain A and name cb, resid 621 and blastp_1COZ and chain B and name cb
dist inter_3737_3_valid , resid 547 and blastp_1COZ and chain B and name cb, resid 121 and blastp_1COZ and chain A and name cb
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
save blastp_1COZ.pse
png blastp_1COZ.png
