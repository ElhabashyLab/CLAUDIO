load blastp_afO34443.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO34443
color 3, chain A
show cartoon, chain A
dist intra_453_valid , resid 89 and blastp_afO34443 and chain A and name cb, resid 105 and blastp_afO34443 and chain A and name cb
dist intra_3866_valid , resid 15 and blastp_afO34443 and chain A and name cb, resid 82 and blastp_afO34443 and chain A and name cb
dist intra_4284_valid , resid 169 and blastp_afO34443 and chain A and name cb, resid 1 and blastp_afO34443 and chain A and name cb
dist intra_2618_out_range , resid 29 and blastp_afO34443 and chain A and name cb, resid 109 and blastp_afO34443 and chain A and name cb
dist intra_3671_unknown , resid 15 and blastp_afO34443 and chain A and name cb, resid 98 and blastp_afO34443 and chain A and name cb
dist intra_4934_unknown , resid 98 and blastp_afO34443 and chain A and name cb, resid 82 and blastp_afO34443 and chain A and name cb
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
save blastp_afO34443.pse
png blastp_afO34443.png
