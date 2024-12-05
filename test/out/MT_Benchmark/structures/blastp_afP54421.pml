load blastp_afP54421.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP54421
color 3, chain A
show cartoon, chain A
dist intra_1663_valid , resid 172 and blastp_afP54421 and chain A and name cb, resid 193 and blastp_afP54421 and chain A and name cb
dist intra_2325_valid , resid 154 and blastp_afP54421 and chain A and name cb, resid 165 and blastp_afP54421 and chain A and name cb
dist intra_3621_valid , resid 112 and blastp_afP54421 and chain A and name cb, resid 128 and blastp_afP54421 and chain A and name cb
dist intra_5579_valid , resid 165 and blastp_afP54421 and chain A and name cb, resid 201 and blastp_afP54421 and chain A and name cb
dist intra_6124_valid , resid 201 and blastp_afP54421 and chain A and name cb, resid 172 and blastp_afP54421 and chain A and name cb
dist intra_1582_unknown , resid 228 and blastp_afP54421 and chain A and name cb, resid 201 and blastp_afP54421 and chain A and name cb
dist intra_3007_unknown , resid 228 and blastp_afP54421 and chain A and name cb, resid 152 and blastp_afP54421 and chain A and name cb
dist intra_4693_unknown , resid 228 and blastp_afP54421 and chain A and name cb, resid 212 and blastp_afP54421 and chain A and name cb
dist intra_5261_unknown , resid 228 and blastp_afP54421 and chain A and name cb, resid 172 and blastp_afP54421 and chain A and name cb
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
save blastp_afP54421.pse
png blastp_afP54421.png
