load blastp_afP13243.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP13243
color 3, chain A
show cartoon, chain A
dist intra_56_valid , resid 220 and blastp_afP13243 and chain A and name cb, resid 14 and blastp_afP13243 and chain A and name cb
dist intra_65_valid , resid 221 and blastp_afP13243 and chain A and name cb, resid 200 and blastp_afP13243 and chain A and name cb
dist intra_521_valid , resid 193 and blastp_afP13243 and chain A and name cb, resid 221 and blastp_afP13243 and chain A and name cb
dist intra_738_valid , resid 14 and blastp_afP13243 and chain A and name cb, resid 200 and blastp_afP13243 and chain A and name cb
dist intra_1167_valid , resid 251 and blastp_afP13243 and chain A and name cb, resid 259 and blastp_afP13243 and chain A and name cb
dist intra_1752_valid , resid 242 and blastp_afP13243 and chain A and name cb, resid 251 and blastp_afP13243 and chain A and name cb
dist intra_4806_valid , resid 242 and blastp_afP13243 and chain A and name cb, resid 259 and blastp_afP13243 and chain A and name cb
dist intra_4814_valid , resid 14 and blastp_afP13243 and chain A and name cb, resid 221 and blastp_afP13243 and chain A and name cb
dist intra_5243_valid , resid 242 and blastp_afP13243 and chain A and name cb, resid 275 and blastp_afP13243 and chain A and name cb
dist intra_5_unknown , resid 168 and blastp_afP13243 and chain A and name cb, resid 242 and blastp_afP13243 and chain A and name cb
dist intra_155_unknown , resid 168 and blastp_afP13243 and chain A and name cb, resid 230 and blastp_afP13243 and chain A and name cb
dist intra_249_unknown , resid 221 and blastp_afP13243 and chain A and name cb, resid 168 and blastp_afP13243 and chain A and name cb
dist intra_365_unknown , resid 168 and blastp_afP13243 and chain A and name cb, resid 251 and blastp_afP13243 and chain A and name cb
dist intra_469_unknown , resid 194 and blastp_afP13243 and chain A and name cb, resid 221 and blastp_afP13243 and chain A and name cb
dist intra_1402_unknown , resid 246 and blastp_afP13243 and chain A and name cb, resid 259 and blastp_afP13243 and chain A and name cb
dist intra_2347_unknown , resid 168 and blastp_afP13243 and chain A and name cb, resid 259 and blastp_afP13243 and chain A and name cb
dist intra_4571_unknown , resid 168 and blastp_afP13243 and chain A and name cb, resid 246 and blastp_afP13243 and chain A and name cb
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
save blastp_afP13243.pse
png blastp_afP13243.png
