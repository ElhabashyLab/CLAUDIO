load blastp_7AQC.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain R
show surface, chain R and blastp_7AQC
color 3, chain R
show cartoon, chain R
hide everything, show cartoon, chain Y
show surface, chain Y and blastp_7AQC
color 5, chain Y
show cartoon, chain Y
dist intra_219_valid , resid 26 and blastp_7AQC and chain R and name cb, resid 47 and blastp_7AQC and chain R and name cb
dist intra_2619_valid , resid 20 and blastp_7AQC and chain Y and name cb, resid 36 and blastp_7AQC and chain Y and name cb
dist intra_3167_valid , resid 83 and blastp_7AQC and chain Y and name cb, resid 54 and blastp_7AQC and chain Y and name cb
dist intra_6118_valid , resid 521 and blastp_7AQC and chain R and name cb, resid 288 and blastp_7AQC and chain R and name cb
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
save blastp_7AQC.pse
png blastp_7AQC.png
