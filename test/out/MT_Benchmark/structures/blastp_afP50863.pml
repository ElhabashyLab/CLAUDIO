load blastp_afP50863.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP50863
color 3, chain A
show cartoon, chain A
dist intra_377_valid , resid 292 and blastp_afP50863 and chain A and name cb, resid 282 and blastp_afP50863 and chain A and name cb
dist intra_4446_valid , resid 313 and blastp_afP50863 and chain A and name cb, resid 292 and blastp_afP50863 and chain A and name cb
dist intra_5594_valid , resid 88 and blastp_afP50863 and chain A and name cb, resid 30 and blastp_afP50863 and chain A and name cb
dist intra_6010_valid , resid 342 and blastp_afP50863 and chain A and name cb, resid 347 and blastp_afP50863 and chain A and name cb
dist intra_347_out_range , resid 292 and blastp_afP50863 and chain A and name cb, resid 319 and blastp_afP50863 and chain A and name cb
dist intra_1296_unknown , resid 97 and blastp_afP50863 and chain A and name cb, resid 88 and blastp_afP50863 and chain A and name cb
dist intra_1350_unknown , resid 292 and blastp_afP50863 and chain A and name cb, resid 314 and blastp_afP50863 and chain A and name cb
dist intra_1496_unknown , resid 96 and blastp_afP50863 and chain A and name cb, resid 88 and blastp_afP50863 and chain A and name cb
dist intra_2277_unknown , resid 264 and blastp_afP50863 and chain A and name cb, resid 292 and blastp_afP50863 and chain A and name cb
dist intra_2723_unknown , resid 96 and blastp_afP50863 and chain A and name cb, resid 49 and blastp_afP50863 and chain A and name cb
dist intra_3705_unknown , resid 91 and blastp_afP50863 and chain A and name cb, resid 88 and blastp_afP50863 and chain A and name cb
dist intra_4568_unknown , resid 78 and blastp_afP50863 and chain A and name cb, resid 96 and blastp_afP50863 and chain A and name cb
dist intra_5662_unknown , resid 287 and blastp_afP50863 and chain A and name cb, resid 282 and blastp_afP50863 and chain A and name cb
dist intra_5848_unknown , resid 78 and blastp_afP50863 and chain A and name cb, resid 30 and blastp_afP50863 and chain A and name cb
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
save blastp_afP50863.pse
png blastp_afP50863.png
