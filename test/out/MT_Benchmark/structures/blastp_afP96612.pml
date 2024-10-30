load blastp_afP96612.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP96612
color 3, chain A
show cartoon, chain A
dist intra_2118_out_range , resid 351 and blastp_afP96612 and chain A and name cb, resid 151 and blastp_afP96612 and chain A and name cb
dist intra_2332_out_range , resid 351 and blastp_afP96612 and chain A and name cb, resid 38 and blastp_afP96612 and chain A and name cb
dist intra_2919_out_range , resid 151 and blastp_afP96612 and chain A and name cb, resid 347 and blastp_afP96612 and chain A and name cb
dist intra_4300_out_range , resid 347 and blastp_afP96612 and chain A and name cb, resid 197 and blastp_afP96612 and chain A and name cb
dist intra_4473_out_range , resid 152 and blastp_afP96612 and chain A and name cb, resid 281 and blastp_afP96612 and chain A and name cb
dist intra_4628_out_range , resid 38 and blastp_afP96612 and chain A and name cb, resid 347 and blastp_afP96612 and chain A and name cb
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
save blastp_afP96612.pse
png blastp_afP96612.png
