load blastp_afO06746.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO06746
color 3, chain A
show cartoon, chain A
dist intra_660_valid , resid 105 and blastp_afO06746 and chain A and name cb, resid 110 and blastp_afO06746 and chain A and name cb
dist intra_953_valid , resid 123 and blastp_afO06746 and chain A and name cb, resid 116 and blastp_afO06746 and chain A and name cb
dist intra_969_valid , resid 123 and blastp_afO06746 and chain A and name cb, resid 136 and blastp_afO06746 and chain A and name cb
dist intra_1344_valid , resid 84 and blastp_afO06746 and chain A and name cb, resid 63 and blastp_afO06746 and chain A and name cb
dist intra_1370_valid , resid 121 and blastp_afO06746 and chain A and name cb, resid 136 and blastp_afO06746 and chain A and name cb
dist intra_1572_valid , resid 123 and blastp_afO06746 and chain A and name cb, resid 110 and blastp_afO06746 and chain A and name cb
dist intra_1685_valid , resid 123 and blastp_afO06746 and chain A and name cb, resid 138 and blastp_afO06746 and chain A and name cb
dist intra_2631_valid , resid 98 and blastp_afO06746 and chain A and name cb, resid 84 and blastp_afO06746 and chain A and name cb
dist intra_2935_valid , resid 27 and blastp_afO06746 and chain A and name cb, resid 69 and blastp_afO06746 and chain A and name cb
dist intra_3600_valid , resid 27 and blastp_afO06746 and chain A and name cb, resid 36 and blastp_afO06746 and chain A and name cb
dist intra_4211_valid , resid 116 and blastp_afO06746 and chain A and name cb, resid 109 and blastp_afO06746 and chain A and name cb
dist intra_5477_valid , resid 105 and blastp_afO06746 and chain A and name cb, resid 123 and blastp_afO06746 and chain A and name cb
dist intra_5816_valid , resid 105 and blastp_afO06746 and chain A and name cb, resid 116 and blastp_afO06746 and chain A and name cb
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
save blastp_afO06746.pse
png blastp_afO06746.png
