load blastp_afP21880.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP21880
color 3, chain A
show cartoon, chain A
dist intra_51_valid , resid 173 and blastp_afP21880 and chain A and name cb, resid 92 and blastp_afP21880 and chain A and name cb
dist intra_129_valid , resid 34 and blastp_afP21880 and chain A and name cb, resid 111 and blastp_afP21880 and chain A and name cb
dist intra_270_valid , resid 34 and blastp_afP21880 and chain A and name cb, resid 108 and blastp_afP21880 and chain A and name cb
dist intra_703_valid , resid 116 and blastp_afP21880 and chain A and name cb, resid 108 and blastp_afP21880 and chain A and name cb
dist intra_1597_valid , resid 230 and blastp_afP21880 and chain A and name cb, resid 69 and blastp_afP21880 and chain A and name cb
dist intra_2538_valid , resid 173 and blastp_afP21880 and chain A and name cb, resid 98 and blastp_afP21880 and chain A and name cb
dist intra_4183_valid , resid 34 and blastp_afP21880 and chain A and name cb, resid 141 and blastp_afP21880 and chain A and name cb
dist intra_538_out_range , resid 98 and blastp_afP21880 and chain A and name cb, resid 158 and blastp_afP21880 and chain A and name cb
dist intra_699_out_range , resid 108 and blastp_afP21880 and chain A and name cb, resid 158 and blastp_afP21880 and chain A and name cb
dist intra_1183_out_range , resid 111 and blastp_afP21880 and chain A and name cb, resid 158 and blastp_afP21880 and chain A and name cb
dist intra_2348_out_range , resid 298 and blastp_afP21880 and chain A and name cb, resid 108 and blastp_afP21880 and chain A and name cb
dist intra_1292_overlaps , resid 108 and blastp_afP21880 and chain A and name cb, resid 98 and blastp_afP21880 and chain A and name cb
dist intra_4843_overlaps , resid 111 and blastp_afP21880 and chain A and name cb, resid 108 and blastp_afP21880 and chain A and name cb
dist intra_95_unknown , resid 34 and blastp_afP21880 and chain A and name cb, resid 2 and blastp_afP21880 and chain A and name cb
dist intra_197_unknown , resid 92 and blastp_afP21880 and chain A and name cb, resid 41 and blastp_afP21880 and chain A and name cb
dist intra_225_unknown , resid 173 and blastp_afP21880 and chain A and name cb, resid 88 and blastp_afP21880 and chain A and name cb
dist intra_696_unknown , resid 108 and blastp_afP21880 and chain A and name cb, resid 2 and blastp_afP21880 and chain A and name cb
dist intra_2690_unknown , resid 111 and blastp_afP21880 and chain A and name cb, resid 2 and blastp_afP21880 and chain A and name cb
dist intra_3782_unknown , resid 108 and blastp_afP21880 and chain A and name cb, resid 41 and blastp_afP21880 and chain A and name cb
dist intra_3862_unknown , resid 34 and blastp_afP21880 and chain A and name cb, resid 129 and blastp_afP21880 and chain A and name cb
dist intra_4362_unknown , resid 111 and blastp_afP21880 and chain A and name cb, resid 41 and blastp_afP21880 and chain A and name cb
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
save blastp_afP21880.pse
png blastp_afP21880.png
