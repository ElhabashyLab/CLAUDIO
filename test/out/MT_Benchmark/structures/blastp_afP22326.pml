load blastp_afP22326.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP22326
color 3, chain A
show cartoon, chain A
dist intra_97_valid , resid 83 and blastp_afP22326 and chain A and name cb, resid 235 and blastp_afP22326 and chain A and name cb
dist intra_138_valid , resid 245 and blastp_afP22326 and chain A and name cb, resid 338 and blastp_afP22326 and chain A and name cb
dist intra_600_valid , resid 227 and blastp_afP22326 and chain A and name cb, resid 83 and blastp_afP22326 and chain A and name cb
dist intra_1466_valid , resid 209 and blastp_afP22326 and chain A and name cb, resid 25 and blastp_afP22326 and chain A and name cb
dist intra_2141_valid , resid 209 and blastp_afP22326 and chain A and name cb, resid 83 and blastp_afP22326 and chain A and name cb
dist intra_2355_valid , resid 227 and blastp_afP22326 and chain A and name cb, resid 235 and blastp_afP22326 and chain A and name cb
dist intra_2587_valid , resid 232 and blastp_afP22326 and chain A and name cb, resid 83 and blastp_afP22326 and chain A and name cb
dist intra_2694_valid , resid 338 and blastp_afP22326 and chain A and name cb, resid 422 and blastp_afP22326 and chain A and name cb
dist intra_4364_valid , resid 209 and blastp_afP22326 and chain A and name cb, resid 142 and blastp_afP22326 and chain A and name cb
dist intra_4851_valid , resid 209 and blastp_afP22326 and chain A and name cb, resid 152 and blastp_afP22326 and chain A and name cb
dist intra_2800_overlaps , resid 2 and blastp_afP22326 and chain A and name cb, resid 26 and blastp_afP22326 and chain A and name cb
dist intra_2453_unknown , resid 2 and blastp_afP22326 and chain A and name cb, resid 31 and blastp_afP22326 and chain A and name cb
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
save blastp_afP22326.pse
png blastp_afP22326.png
