load blastp_afP08838.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP08838
color 3, chain A
show cartoon, chain A
dist intra_139_valid , resid 63 and blastp_afP08838 and chain A and name cb, resid 56 and blastp_afP08838 and chain A and name cb
dist intra_386_valid , resid 92 and blastp_afP08838 and chain A and name cb, resid 30 and blastp_afP08838 and chain A and name cb
dist intra_544_valid , resid 539 and blastp_afP08838 and chain A and name cb, resid 255 and blastp_afP08838 and chain A and name cb
dist intra_647_valid , resid 539 and blastp_afP08838 and chain A and name cb, resid 264 and blastp_afP08838 and chain A and name cb
dist intra_1024_valid , resid 250 and blastp_afP08838 and chain A and name cb, resid 177 and blastp_afP08838 and chain A and name cb
dist intra_3490_valid , resid 539 and blastp_afP08838 and chain A and name cb, resid 250 and blastp_afP08838 and chain A and name cb
dist intra_5555_valid , resid 30 and blastp_afP08838 and chain A and name cb, resid 90 and blastp_afP08838 and chain A and name cb
dist intra_5920_valid , resid 539 and blastp_afP08838 and chain A and name cb, resid 566 and blastp_afP08838 and chain A and name cb
dist intra_2635_unknown , resid 21 and blastp_afP08838 and chain A and name cb, resid 92 and blastp_afP08838 and chain A and name cb
dist intra_2898_unknown , resid 539 and blastp_afP08838 and chain A and name cb, resid 256 and blastp_afP08838 and chain A and name cb
dist intra_4886_unknown , resid 59 and blastp_afP08838 and chain A and name cb, resid 56 and blastp_afP08838 and chain A and name cb
dist intra_4925_unknown , resid 63 and blastp_afP08838 and chain A and name cb, resid 50 and blastp_afP08838 and chain A and name cb
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
save blastp_afP08838.pse
png blastp_afP08838.png
