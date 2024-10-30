load blastp_afP28599.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP28599
color 3, chain A
show cartoon, chain A
dist intra_465_valid , resid 38 and blastp_afP28599 and chain A and name cb, resid 59 and blastp_afP28599 and chain A and name cb
dist intra_2280_valid , resid 59 and blastp_afP28599 and chain A and name cb, resid 1 and blastp_afP28599 and chain A and name cb
dist intra_5043_valid , resid 38 and blastp_afP28599 and chain A and name cb, resid 1 and blastp_afP28599 and chain A and name cb
dist intra_5195_overlaps , resid 54 and blastp_afP28599 and chain A and name cb, resid 1 and blastp_afP28599 and chain A and name cb
dist intra_282_same , resid 31 and blastp_afP28599 and chain A and name cb, resid 31 and blastp_afP28599 and chain A and name cb
dist intra_127_unknown , resid 68 and blastp_afP28599 and chain A and name cb, resid 31 and blastp_afP28599 and chain A and name cb
dist intra_421_unknown , resid 75 and blastp_afP28599 and chain A and name cb, resid 31 and blastp_afP28599 and chain A and name cb
dist intra_1747_unknown , resid 33 and blastp_afP28599 and chain A and name cb, resid 68 and blastp_afP28599 and chain A and name cb
dist intra_1947_unknown , resid 38 and blastp_afP28599 and chain A and name cb, resid 19 and blastp_afP28599 and chain A and name cb
dist intra_2265_unknown , resid 31 and blastp_afP28599 and chain A and name cb, resid 33 and blastp_afP28599 and chain A and name cb
dist intra_4964_unknown , resid 75 and blastp_afP28599 and chain A and name cb, resid 33 and blastp_afP28599 and chain A and name cb
dist intra_6142_unknown , resid 38 and blastp_afP28599 and chain A and name cb, resid 9 and blastp_afP28599 and chain A and name cb
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
save blastp_afP28599.pse
png blastp_afP28599.png
