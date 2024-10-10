load blastp_6KOB.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain B
show surface, chain B and blastp_6KOB
color 3, chain B
show cartoon, chain B
hide everything, show cartoon, chain F
show surface, chain F and blastp_6KOB
color 5, chain F
show cartoon, chain F
dist intra_1086_valid , resid 285 and blastp_6KOB and chain B and name cb, resid 227 and blastp_6KOB and chain B and name cb
dist intra_1086_4_valid , resid 285 and blastp_6KOB and chain F and name cb, resid 227 and blastp_6KOB and chain F and name cb
dist intra_6000_valid , resid 222 and blastp_6KOB and chain B and name cb, resid 227 and blastp_6KOB and chain B and name cb
dist intra_6000_4_valid , resid 222 and blastp_6KOB and chain F and name cb, resid 227 and blastp_6KOB and chain F and name cb
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
save blastp_6KOB.pse
png blastp_6KOB.png
