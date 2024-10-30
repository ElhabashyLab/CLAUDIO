load blastp_afP45872.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP45872
color 3, chain A
show cartoon, chain A
dist intra_246_valid , resid 78 and blastp_afP45872 and chain A and name cb, resid 62 and blastp_afP45872 and chain A and name cb
dist intra_2439_valid , resid 293 and blastp_afP45872 and chain A and name cb, resid 279 and blastp_afP45872 and chain A and name cb
dist intra_3480_valid , resid 29 and blastp_afP45872 and chain A and name cb, resid 36 and blastp_afP45872 and chain A and name cb
dist intra_3932_valid , resid 279 and blastp_afP45872 and chain A and name cb, resid 29 and blastp_afP45872 and chain A and name cb
dist intra_3312_out_range , resid 293 and blastp_afP45872 and chain A and name cb, resid 29 and blastp_afP45872 and chain A and name cb
dist intra_5491_unknown , resid 144 and blastp_afP45872 and chain A and name cb, resid 244 and blastp_afP45872 and chain A and name cb
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
save blastp_afP45872.pse
png blastp_afP45872.png
