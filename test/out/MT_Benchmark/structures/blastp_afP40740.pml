load blastp_afP40740.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP40740
color 3, chain A
show cartoon, chain A
dist intra_130_valid , resid 157 and blastp_afP40740 and chain A and name cb, resid 217 and blastp_afP40740 and chain A and name cb
dist intra_3616_valid , resid 331 and blastp_afP40740 and chain A and name cb, resid 256 and blastp_afP40740 and chain A and name cb
dist intra_3907_valid , resid 6 and blastp_afP40740 and chain A and name cb, resid 347 and blastp_afP40740 and chain A and name cb
dist intra_4782_valid , resid 157 and blastp_afP40740 and chain A and name cb, resid 147 and blastp_afP40740 and chain A and name cb
dist intra_4902_out_range , resid 6 and blastp_afP40740 and chain A and name cb, resid 274 and blastp_afP40740 and chain A and name cb
dist intra_1202_unknown , resid 228 and blastp_afP40740 and chain A and name cb, resid 336 and blastp_afP40740 and chain A and name cb
dist intra_1300_unknown , resid 198 and blastp_afP40740 and chain A and name cb, resid 157 and blastp_afP40740 and chain A and name cb
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
save blastp_afP40740.pse
png blastp_afP40740.png
