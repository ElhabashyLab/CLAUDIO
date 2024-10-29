load blastp_5LOJ.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_5LOJ
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_5LOJ
color 5, chain B
show cartoon, chain B
dist intra_645_valid , resid 47 and blastp_5LOJ and chain A and name cb, resid 25 and blastp_5LOJ and chain A and name cb
dist intra_645_4_valid , resid 47 and blastp_5LOJ and chain B and name cb, resid 25 and blastp_5LOJ and chain B and name cb
dist intra_1319_valid , resid 47 and blastp_5LOJ and chain A and name cb, resid 158 and blastp_5LOJ and chain A and name cb
dist intra_1319_4_valid , resid 47 and blastp_5LOJ and chain B and name cb, resid 158 and blastp_5LOJ and chain B and name cb
dist intra_1668_valid , resid 158 and blastp_5LOJ and chain A and name cb, resid 248 and blastp_5LOJ and chain A and name cb
dist intra_1668_4_valid , resid 158 and blastp_5LOJ and chain B and name cb, resid 248 and blastp_5LOJ and chain B and name cb
dist intra_1763_valid , resid 47 and blastp_5LOJ and chain A and name cb, resid 248 and blastp_5LOJ and chain A and name cb
dist intra_1763_4_valid , resid 47 and blastp_5LOJ and chain B and name cb, resid 248 and blastp_5LOJ and chain B and name cb
dist inter_1319_3_valid , resid 47 and blastp_5LOJ and chain B and name cb, resid 158 and blastp_5LOJ and chain A and name cb
dist inter_1668_2_valid , resid 158 and blastp_5LOJ and chain A and name cb, resid 248 and blastp_5LOJ and chain B and name cb
dist inter_1668_3_valid , resid 158 and blastp_5LOJ and chain B and name cb, resid 248 and blastp_5LOJ and chain A and name cb
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
save blastp_5LOJ.pse
png blastp_5LOJ.png
