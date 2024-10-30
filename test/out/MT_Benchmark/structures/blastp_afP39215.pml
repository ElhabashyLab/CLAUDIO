load blastp_afP39215.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP39215
color 3, chain A
show cartoon, chain A
dist intra_3090_valid , resid 96 and blastp_afP39215 and chain A and name cb, resid 128 and blastp_afP39215 and chain A and name cb
dist intra_4443_valid , resid 126 and blastp_afP39215 and chain A and name cb, resid 96 and blastp_afP39215 and chain A and name cb
dist intra_4445_valid , resid 224 and blastp_afP39215 and chain A and name cb, resid 211 and blastp_afP39215 and chain A and name cb
dist intra_4757_valid , resid 126 and blastp_afP39215 and chain A and name cb, resid 89 and blastp_afP39215 and chain A and name cb
dist intra_4792_unknown , resid 220 and blastp_afP39215 and chain A and name cb, resid 189 and blastp_afP39215 and chain A and name cb
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
save blastp_afP39215.pse
png blastp_afP39215.png
