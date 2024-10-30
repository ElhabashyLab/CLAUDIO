load blastp_afP54169.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP54169
color 3, chain A
show cartoon, chain A
dist intra_398_valid , resid 248 and blastp_afP54169 and chain A and name cb, resid 278 and blastp_afP54169 and chain A and name cb
dist intra_1629_valid , resid 32 and blastp_afP54169 and chain A and name cb, resid 53 and blastp_afP54169 and chain A and name cb
dist intra_2376_valid , resid 248 and blastp_afP54169 and chain A and name cb, resid 221 and blastp_afP54169 and chain A and name cb
dist intra_5899_valid , resid 248 and blastp_afP54169 and chain A and name cb, resid 222 and blastp_afP54169 and chain A and name cb
dist intra_1101_unknown , resid 156 and blastp_afP54169 and chain A and name cb, resid 196 and blastp_afP54169 and chain A and name cb
dist intra_1149_unknown , resid 248 and blastp_afP54169 and chain A and name cb, resid 274 and blastp_afP54169 and chain A and name cb
dist intra_4735_unknown , resid 200 and blastp_afP54169 and chain A and name cb, resid 73 and blastp_afP54169 and chain A and name cb
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
save blastp_afP54169.pse
png blastp_afP54169.png
