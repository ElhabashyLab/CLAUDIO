load blastp_afP80240.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP80240
color 3, chain A
show cartoon, chain A
dist intra_112_valid , resid 76 and blastp_afP80240 and chain A and name cb, resid 129 and blastp_afP80240 and chain A and name cb
dist intra_558_valid , resid 76 and blastp_afP80240 and chain A and name cb, resid 5 and blastp_afP80240 and chain A and name cb
dist intra_815_valid , resid 55 and blastp_afP80240 and chain A and name cb, resid 37 and blastp_afP80240 and chain A and name cb
dist intra_957_valid , resid 135 and blastp_afP80240 and chain A and name cb, resid 76 and blastp_afP80240 and chain A and name cb
dist intra_1485_valid , resid 5 and blastp_afP80240 and chain A and name cb, resid 129 and blastp_afP80240 and chain A and name cb
dist intra_2953_valid , resid 76 and blastp_afP80240 and chain A and name cb, resid 155 and blastp_afP80240 and chain A and name cb
dist intra_4400_valid , resid 14 and blastp_afP80240 and chain A and name cb, resid 76 and blastp_afP80240 and chain A and name cb
dist intra_5408_valid , resid 30 and blastp_afP80240 and chain A and name cb, resid 37 and blastp_afP80240 and chain A and name cb
dist intra_1567_unknown , resid 15 and blastp_afP80240 and chain A and name cb, resid 129 and blastp_afP80240 and chain A and name cb
dist intra_2822_unknown , resid 15 and blastp_afP80240 and chain A and name cb, resid 135 and blastp_afP80240 and chain A and name cb
dist intra_4011_unknown , resid 30 and blastp_afP80240 and chain A and name cb, resid 15 and blastp_afP80240 and chain A and name cb
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
save blastp_afP80240.pse
png blastp_afP80240.png
