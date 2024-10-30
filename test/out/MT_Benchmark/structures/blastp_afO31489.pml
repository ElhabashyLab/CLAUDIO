load blastp_afO31489.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO31489
color 3, chain A
show cartoon, chain A
dist intra_587_valid , resid 366 and blastp_afO31489 and chain A and name cb, resid 359 and blastp_afO31489 and chain A and name cb
dist intra_1265_valid , resid 120 and blastp_afO31489 and chain A and name cb, resid 83 and blastp_afO31489 and chain A and name cb
dist intra_1343_valid , resid 633 and blastp_afO31489 and chain A and name cb, resid 321 and blastp_afO31489 and chain A and name cb
dist intra_1374_valid , resid 577 and blastp_afO31489 and chain A and name cb, resid 630 and blastp_afO31489 and chain A and name cb
dist intra_2973_valid , resid 198 and blastp_afO31489 and chain A and name cb, resid 239 and blastp_afO31489 and chain A and name cb
dist intra_3119_valid , resid 115 and blastp_afO31489 and chain A and name cb, resid 278 and blastp_afO31489 and chain A and name cb
dist intra_3520_valid , resid 630 and blastp_afO31489 and chain A and name cb, resid 591 and blastp_afO31489 and chain A and name cb
dist intra_4173_valid , resid 593 and blastp_afO31489 and chain A and name cb, resid 577 and blastp_afO31489 and chain A and name cb
dist intra_4182_valid , resid 630 and blastp_afO31489 and chain A and name cb, resid 311 and blastp_afO31489 and chain A and name cb
dist intra_5189_valid , resid 630 and blastp_afO31489 and chain A and name cb, resid 321 and blastp_afO31489 and chain A and name cb
dist intra_3979_unknown , resid 1 and blastp_afO31489 and chain A and name cb, resid 89 and blastp_afO31489 and chain A and name cb
dist intra_5483_unknown , resid 77 and blastp_afO31489 and chain A and name cb, resid 120 and blastp_afO31489 and chain A and name cb
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
save blastp_afO31489.pse
png blastp_afO31489.png
