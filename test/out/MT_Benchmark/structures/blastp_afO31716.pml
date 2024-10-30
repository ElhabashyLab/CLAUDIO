load blastp_afO31716.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO31716
color 3, chain A
show cartoon, chain A
dist intra_325_valid , resid 517 and blastp_afO31716 and chain A and name cb, resid 533 and blastp_afO31716 and chain A and name cb
dist intra_394_valid , resid 90 and blastp_afO31716 and chain A and name cb, resid 70 and blastp_afO31716 and chain A and name cb
dist intra_918_valid , resid 445 and blastp_afO31716 and chain A and name cb, resid 45 and blastp_afO31716 and chain A and name cb
dist intra_2475_valid , resid 257 and blastp_afO31716 and chain A and name cb, resid 291 and blastp_afO31716 and chain A and name cb
dist intra_3137_valid , resid 298 and blastp_afO31716 and chain A and name cb, resid 15 and blastp_afO31716 and chain A and name cb
dist intra_220_unknown , resid 84 and blastp_afO31716 and chain A and name cb, resid 70 and blastp_afO31716 and chain A and name cb
dist intra_2584_unknown , resid 291 and blastp_afO31716 and chain A and name cb, resid 278 and blastp_afO31716 and chain A and name cb
dist intra_4281_unknown , resid 258 and blastp_afO31716 and chain A and name cb, resid 256 and blastp_afO31716 and chain A and name cb
dist intra_4586_unknown , resid 291 and blastp_afO31716 and chain A and name cb, resid 280 and blastp_afO31716 and chain A and name cb
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
save blastp_afO31716.pse
png blastp_afO31716.png
