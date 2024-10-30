load blastp_afP80886.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP80886
color 3, chain A
show cartoon, chain A
dist intra_193_valid , resid 61 and blastp_afP80886 and chain A and name cb, resid 79 and blastp_afP80886 and chain A and name cb
dist intra_324_valid , resid 14 and blastp_afP80886 and chain A and name cb, resid 186 and blastp_afP80886 and chain A and name cb
dist intra_973_valid , resid 179 and blastp_afP80886 and chain A and name cb, resid 227 and blastp_afP80886 and chain A and name cb
dist intra_1236_valid , resid 358 and blastp_afP80886 and chain A and name cb, resid 380 and blastp_afP80886 and chain A and name cb
dist intra_1638_valid , resid 70 and blastp_afP80886 and chain A and name cb, resid 36 and blastp_afP80886 and chain A and name cb
dist intra_1902_valid , resid 227 and blastp_afP80886 and chain A and name cb, resid 14 and blastp_afP80886 and chain A and name cb
dist intra_1929_valid , resid 56 and blastp_afP80886 and chain A and name cb, resid 94 and blastp_afP80886 and chain A and name cb
dist intra_2019_valid , resid 56 and blastp_afP80886 and chain A and name cb, resid 64 and blastp_afP80886 and chain A and name cb
dist intra_3114_valid , resid 106 and blastp_afP80886 and chain A and name cb, resid 143 and blastp_afP80886 and chain A and name cb
dist intra_3318_valid , resid 56 and blastp_afP80886 and chain A and name cb, resid 79 and blastp_afP80886 and chain A and name cb
dist intra_542_unknown , resid 61 and blastp_afP80886 and chain A and name cb, resid 71 and blastp_afP80886 and chain A and name cb
dist intra_2578_unknown , resid 226 and blastp_afP80886 and chain A and name cb, resid 14 and blastp_afP80886 and chain A and name cb
dist intra_2801_unknown , resid 226 and blastp_afP80886 and chain A and name cb, resid 179 and blastp_afP80886 and chain A and name cb
dist intra_3704_unknown , resid 177 and blastp_afP80886 and chain A and name cb, resid 226 and blastp_afP80886 and chain A and name cb
dist intra_4054_unknown , resid 358 and blastp_afP80886 and chain A and name cb, resid 360 and blastp_afP80886 and chain A and name cb
dist intra_4121_unknown , resid 96 and blastp_afP80886 and chain A and name cb, resid 171 and blastp_afP80886 and chain A and name cb
dist intra_4174_unknown , resid 177 and blastp_afP80886 and chain A and name cb, resid 227 and blastp_afP80886 and chain A and name cb
dist intra_4603_unknown , resid 171 and blastp_afP80886 and chain A and name cb, resid 95 and blastp_afP80886 and chain A and name cb
dist intra_4820_unknown , resid 176 and blastp_afP80886 and chain A and name cb, resid 95 and blastp_afP80886 and chain A and name cb
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
save blastp_afP80886.pse
png blastp_afP80886.png
