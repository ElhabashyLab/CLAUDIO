load blastp_afP16263.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP16263
color 3, chain A
show cartoon, chain A
dist intra_114_valid , resid 153 and blastp_afP16263 and chain A and name cb, resid 135 and blastp_afP16263 and chain A and name cb
dist intra_1800_valid , resid 258 and blastp_afP16263 and chain A and name cb, resid 308 and blastp_afP16263 and chain A and name cb
dist intra_1976_valid , resid 191 and blastp_afP16263 and chain A and name cb, resid 201 and blastp_afP16263 and chain A and name cb
dist intra_4226_valid , resid 315 and blastp_afP16263 and chain A and name cb, resid 242 and blastp_afP16263 and chain A and name cb
dist intra_1023_unknown , resid 135 and blastp_afP16263 and chain A and name cb, resid 119 and blastp_afP16263 and chain A and name cb
dist intra_1165_unknown , resid 135 and blastp_afP16263 and chain A and name cb, resid 102 and blastp_afP16263 and chain A and name cb
dist intra_1172_unknown , resid 135 and blastp_afP16263 and chain A and name cb, resid 172 and blastp_afP16263 and chain A and name cb
dist intra_1996_unknown , resid 153 and blastp_afP16263 and chain A and name cb, resid 172 and blastp_afP16263 and chain A and name cb
dist intra_2604_unknown , resid 153 and blastp_afP16263 and chain A and name cb, resid 102 and blastp_afP16263 and chain A and name cb
dist intra_3389_unknown , resid 135 and blastp_afP16263 and chain A and name cb, resid 94 and blastp_afP16263 and chain A and name cb
dist intra_4227_unknown , resid 135 and blastp_afP16263 and chain A and name cb, resid 178 and blastp_afP16263 and chain A and name cb
dist intra_4283_unknown , resid 172 and blastp_afP16263 and chain A and name cb, resid 201 and blastp_afP16263 and chain A and name cb
dist intra_4677_unknown , resid 191 and blastp_afP16263 and chain A and name cb, resid 197 and blastp_afP16263 and chain A and name cb
dist intra_5242_unknown , resid 178 and blastp_afP16263 and chain A and name cb, resid 172 and blastp_afP16263 and chain A and name cb
dist intra_5431_unknown , resid 135 and blastp_afP16263 and chain A and name cb, resid 154 and blastp_afP16263 and chain A and name cb
dist intra_5648_unknown , resid 153 and blastp_afP16263 and chain A and name cb, resid 119 and blastp_afP16263 and chain A and name cb
dist intra_5870_unknown , resid 153 and blastp_afP16263 and chain A and name cb, resid 178 and blastp_afP16263 and chain A and name cb
dist intra_5939_unknown , resid 98 and blastp_afP16263 and chain A and name cb, resid 197 and blastp_afP16263 and chain A and name cb
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
save blastp_afP16263.pse
png blastp_afP16263.png
