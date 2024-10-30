load blastp_afO34962.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO34962
color 3, chain A
show cartoon, chain A
dist intra_778_valid , resid 201 and blastp_afO34962 and chain A and name cb, resid 237 and blastp_afO34962 and chain A and name cb
dist intra_1878_valid , resid 12 and blastp_afO34962 and chain A and name cb, resid 17 and blastp_afO34962 and chain A and name cb
dist intra_2129_out_range , resid 30 and blastp_afO34962 and chain A and name cb, resid 12 and blastp_afO34962 and chain A and name cb
dist intra_5518_out_range , resid 404 and blastp_afO34962 and chain A and name cb, resid 12 and blastp_afO34962 and chain A and name cb
dist intra_5997_out_range , resid 401 and blastp_afO34962 and chain A and name cb, resid 12 and blastp_afO34962 and chain A and name cb
dist intra_4297_unknown , resid 237 and blastp_afO34962 and chain A and name cb, resid 187 and blastp_afO34962 and chain A and name cb
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
save blastp_afO34962.pse
png blastp_afO34962.png
