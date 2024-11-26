load blastp_afP21879.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP21879
color 3, chain A
show cartoon, chain A
dist intra_1812_valid , resid 399 and blastp_afP21879 and chain A and name cb, resid 117 and blastp_afP21879 and chain A and name cb
dist intra_2992_valid , resid 133 and blastp_afP21879 and chain A and name cb, resid 159 and blastp_afP21879 and chain A and name cb
dist intra_4831_valid , resid 399 and blastp_afP21879 and chain A and name cb, resid 115 and blastp_afP21879 and chain A and name cb
dist intra_535_unknown , resid 66 and blastp_afP21879 and chain A and name cb, resid 399 and blastp_afP21879 and chain A and name cb
dist intra_1190_unknown , resid 411 and blastp_afP21879 and chain A and name cb, resid 66 and blastp_afP21879 and chain A and name cb
dist intra_1437_unknown , resid 22 and blastp_afP21879 and chain A and name cb, resid 441 and blastp_afP21879 and chain A and name cb
dist intra_3613_unknown , resid 412 and blastp_afP21879 and chain A and name cb, resid 66 and blastp_afP21879 and chain A and name cb
dist intra_4118_unknown , resid 480 and blastp_afP21879 and chain A and name cb, resid 1 and blastp_afP21879 and chain A and name cb
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
save blastp_afP21879.pse
png blastp_afP21879.png
