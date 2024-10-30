load blastp_afP38493.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP38493
color 3, chain A
show cartoon, chain A
dist intra_358_valid , resid 4 and blastp_afP38493 and chain A and name cb, resid 122 and blastp_afP38493 and chain A and name cb
dist intra_1245_valid , resid 4 and blastp_afP38493 and chain A and name cb, resid 74 and blastp_afP38493 and chain A and name cb
dist intra_1400_valid , resid 104 and blastp_afP38493 and chain A and name cb, resid 182 and blastp_afP38493 and chain A and name cb
dist intra_1568_valid , resid 22 and blastp_afP38493 and chain A and name cb, resid 163 and blastp_afP38493 and chain A and name cb
dist intra_1781_valid , resid 27 and blastp_afP38493 and chain A and name cb, resid 74 and blastp_afP38493 and chain A and name cb
dist intra_3012_valid , resid 164 and blastp_afP38493 and chain A and name cb, resid 22 and blastp_afP38493 and chain A and name cb
dist intra_4016_valid , resid 64 and blastp_afP38493 and chain A and name cb, resid 114 and blastp_afP38493 and chain A and name cb
dist intra_3468_unknown , resid 158 and blastp_afP38493 and chain A and name cb, resid 22 and blastp_afP38493 and chain A and name cb
dist intra_3879_unknown , resid 27 and blastp_afP38493 and chain A and name cb, resid 65 and blastp_afP38493 and chain A and name cb
dist intra_5950_unknown , resid 64 and blastp_afP38493 and chain A and name cb, resid 107 and blastp_afP38493 and chain A and name cb
dist intra_5968_unknown , resid 182 and blastp_afP38493 and chain A and name cb, resid 92 and blastp_afP38493 and chain A and name cb
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
save blastp_afP38493.pse
png blastp_afP38493.png
