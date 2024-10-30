load blastp_afP42305.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP42305
color 3, chain A
show cartoon, chain A
dist intra_4698_valid , resid 107 and blastp_afP42305 and chain A and name cb, resid 250 and blastp_afP42305 and chain A and name cb
dist intra_4942_valid , resid 460 and blastp_afP42305 and chain A and name cb, resid 476 and blastp_afP42305 and chain A and name cb
dist intra_5010_valid , resid 476 and blastp_afP42305 and chain A and name cb, resid 401 and blastp_afP42305 and chain A and name cb
dist intra_5259_valid , resid 377 and blastp_afP42305 and chain A and name cb, resid 337 and blastp_afP42305 and chain A and name cb
dist intra_5741_valid , resid 377 and blastp_afP42305 and chain A and name cb, resid 232 and blastp_afP42305 and chain A and name cb
dist intra_4379_unknown , resid 113 and blastp_afP42305 and chain A and name cb, resid 137 and blastp_afP42305 and chain A and name cb
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
save blastp_afP42305.pse
png blastp_afP42305.png
