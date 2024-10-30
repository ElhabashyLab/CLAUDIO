load blastp_afP09124.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP09124
color 3, chain A
show cartoon, chain A
dist intra_6_valid , resid 214 and blastp_afP09124 and chain A and name cb, resid 193 and blastp_afP09124 and chain A and name cb
dist intra_419_valid , resid 4 and blastp_afP09124 and chain A and name cb, resid 70 and blastp_afP09124 and chain A and name cb
dist intra_525_valid , resid 82 and blastp_afP09124 and chain A and name cb, resid 108 and blastp_afP09124 and chain A and name cb
dist intra_1739_valid , resid 332 and blastp_afP09124 and chain A and name cb, resid 270 and blastp_afP09124 and chain A and name cb
dist intra_3102_valid , resid 332 and blastp_afP09124 and chain A and name cb, resid 167 and blastp_afP09124 and chain A and name cb
dist intra_4489_valid , resid 115 and blastp_afP09124 and chain A and name cb, resid 4 and blastp_afP09124 and chain A and name cb
dist intra_3981_overlaps , resid 4 and blastp_afP09124 and chain A and name cb, resid 54 and blastp_afP09124 and chain A and name cb
dist intra_2299_unknown , resid 172 and blastp_afP09124 and chain A and name cb, resid 214 and blastp_afP09124 and chain A and name cb
dist intra_5692_unknown , resid 200 and blastp_afP09124 and chain A and name cb, resid 193 and blastp_afP09124 and chain A and name cb
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
save blastp_afP09124.pse
png blastp_afP09124.png
