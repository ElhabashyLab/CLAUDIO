load blastp_afP55872.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP55872
color 3, chain A
show cartoon, chain A
dist intra_1107_valid , resid 87 and blastp_afP55872 and chain A and name cb, resid 103 and blastp_afP55872 and chain A and name cb
dist intra_1361_valid , resid 109 and blastp_afP55872 and chain A and name cb, resid 87 and blastp_afP55872 and chain A and name cb
dist intra_4206_valid , resid 131 and blastp_afP55872 and chain A and name cb, resid 154 and blastp_afP55872 and chain A and name cb
dist intra_4871_valid , resid 118 and blastp_afP55872 and chain A and name cb, resid 82 and blastp_afP55872 and chain A and name cb
dist intra_5180_valid , resid 154 and blastp_afP55872 and chain A and name cb, resid 82 and blastp_afP55872 and chain A and name cb
dist intra_5365_valid , resid 154 and blastp_afP55872 and chain A and name cb, resid 118 and blastp_afP55872 and chain A and name cb
dist intra_785_unknown , resid 141 and blastp_afP55872 and chain A and name cb, resid 131 and blastp_afP55872 and chain A and name cb
dist intra_3931_unknown , resid 65 and blastp_afP55872 and chain A and name cb, resid 131 and blastp_afP55872 and chain A and name cb
dist intra_4263_unknown , resid 87 and blastp_afP55872 and chain A and name cb, resid 91 and blastp_afP55872 and chain A and name cb
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
save blastp_afP55872.pse
png blastp_afP55872.png
