load blastp_afP39121.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP39121
color 3, chain A
show cartoon, chain A
dist intra_178_valid , resid 213 and blastp_afP39121 and chain A and name cb, resid 23 and blastp_afP39121 and chain A and name cb
dist intra_212_valid , resid 78 and blastp_afP39121 and chain A and name cb, resid 119 and blastp_afP39121 and chain A and name cb
dist intra_338_valid , resid 13 and blastp_afP39121 and chain A and name cb, resid 23 and blastp_afP39121 and chain A and name cb
dist intra_1063_valid , resid 164 and blastp_afP39121 and chain A and name cb, resid 172 and blastp_afP39121 and chain A and name cb
dist intra_862_overlaps , resid 2 and blastp_afP39121 and chain A and name cb, resid 32 and blastp_afP39121 and chain A and name cb
dist intra_78_unknown , resid 189 and blastp_afP39121 and chain A and name cb, resid 2 and blastp_afP39121 and chain A and name cb
dist intra_96_unknown , resid 2 and blastp_afP39121 and chain A and name cb, resid 213 and blastp_afP39121 and chain A and name cb
dist intra_649_unknown , resid 119 and blastp_afP39121 and chain A and name cb, resid 74 and blastp_afP39121 and chain A and name cb
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
save blastp_afP39121.pse
png blastp_afP39121.png
