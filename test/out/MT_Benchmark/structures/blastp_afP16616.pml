load blastp_afP16616.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP16616
color 3, chain A
show cartoon, chain A
dist intra_1422_valid , resid 287 and blastp_afP16616 and chain A and name cb, resid 299 and blastp_afP16616 and chain A and name cb
dist intra_1460_valid , resid 20 and blastp_afP16616 and chain A and name cb, resid 27 and blastp_afP16616 and chain A and name cb
dist intra_2766_valid , resid 43 and blastp_afP16616 and chain A and name cb, resid 63 and blastp_afP16616 and chain A and name cb
dist intra_1560_unknown , resid 54 and blastp_afP16616 and chain A and name cb, resid 43 and blastp_afP16616 and chain A and name cb
dist intra_2258_unknown , resid 314 and blastp_afP16616 and chain A and name cb, resid 54 and blastp_afP16616 and chain A and name cb
dist intra_5666_unknown , resid 54 and blastp_afP16616 and chain A and name cb, resid 39 and blastp_afP16616 and chain A and name cb
dist intra_5791_unknown , resid 299 and blastp_afP16616 and chain A and name cb, resid 275 and blastp_afP16616 and chain A and name cb
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
save blastp_afP16616.pse
png blastp_afP16616.png
