load blastp_afO06478.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO06478
color 3, chain A
show cartoon, chain A
dist intra_2548_valid , resid 60 and blastp_afO06478 and chain A and name cb, resid 15 and blastp_afO06478 and chain A and name cb
dist intra_2911_valid , resid 59 and blastp_afO06478 and chain A and name cb, resid 15 and blastp_afO06478 and chain A and name cb
dist intra_4390_valid , resid 41 and blastp_afO06478 and chain A and name cb, resid 28 and blastp_afO06478 and chain A and name cb
dist intra_4606_valid , resid 452 and blastp_afO06478 and chain A and name cb, resid 126 and blastp_afO06478 and chain A and name cb
dist intra_2913_out_range , resid 59 and blastp_afO06478 and chain A and name cb, resid 426 and blastp_afO06478 and chain A and name cb
dist intra_3805_out_range , resid 426 and blastp_afO06478 and chain A and name cb, resid 58 and blastp_afO06478 and chain A and name cb
dist intra_1233_overlaps , resid 234 and blastp_afO06478 and chain A and name cb, resid 245 and blastp_afO06478 and chain A and name cb
dist intra_3568_same , resid 245 and blastp_afO06478 and chain A and name cb, resid 245 and blastp_afO06478 and chain A and name cb
dist intra_2040_unknown , resid 59 and blastp_afO06478 and chain A and name cb, resid 10 and blastp_afO06478 and chain A and name cb
dist intra_4471_unknown , resid 310 and blastp_afO06478 and chain A and name cb, resid 480 and blastp_afO06478 and chain A and name cb
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
save blastp_afO06478.pse
png blastp_afO06478.png
