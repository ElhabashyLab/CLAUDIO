load blastp_afP54547.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP54547
color 3, chain A
show cartoon, chain A
dist intra_800_valid , resid 163 and blastp_afP54547 and chain A and name cb, resid 132 and blastp_afP54547 and chain A and name cb
dist intra_1421_valid , resid 24 and blastp_afP54547 and chain A and name cb, resid 183 and blastp_afP54547 and chain A and name cb
dist intra_3849_valid , resid 24 and blastp_afP54547 and chain A and name cb, resid 149 and blastp_afP54547 and chain A and name cb
dist intra_6015_valid , resid 149 and blastp_afP54547 and chain A and name cb, resid 230 and blastp_afP54547 and chain A and name cb
dist intra_5029_out_range , resid 392 and blastp_afP54547 and chain A and name cb, resid 183 and blastp_afP54547 and chain A and name cb
dist intra_153_unknown , resid 392 and blastp_afP54547 and chain A and name cb, resid 1 and blastp_afP54547 and chain A and name cb
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
save blastp_afP54547.pse
png blastp_afP54547.png
