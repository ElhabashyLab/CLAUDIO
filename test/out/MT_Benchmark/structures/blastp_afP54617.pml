load blastp_afP54617.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP54617
color 3, chain A
show cartoon, chain A
dist intra_1867_valid , resid 154 and blastp_afP54617 and chain A and name cb, resid 147 and blastp_afP54617 and chain A and name cb
dist intra_2279_valid , resid 147 and blastp_afP54617 and chain A and name cb, resid 27 and blastp_afP54617 and chain A and name cb
dist intra_3773_valid , resid 154 and blastp_afP54617 and chain A and name cb, resid 142 and blastp_afP54617 and chain A and name cb
dist intra_658_unknown , resid 120 and blastp_afP54617 and chain A and name cb, resid 8 and blastp_afP54617 and chain A and name cb
dist intra_2814_unknown , resid 220 and blastp_afP54617 and chain A and name cb, resid 227 and blastp_afP54617 and chain A and name cb
dist intra_4648_unknown , resid 223 and blastp_afP54617 and chain A and name cb, resid 220 and blastp_afP54617 and chain A and name cb
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
save blastp_afP54617.pse
png blastp_afP54617.png
