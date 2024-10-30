load blastp_afP35136.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP35136
color 3, chain A
show cartoon, chain A
dist intra_264_valid , resid 365 and blastp_afP35136 and chain A and name cb, resid 390 and blastp_afP35136 and chain A and name cb
dist intra_489_valid , resid 316 and blastp_afP35136 and chain A and name cb, resid 323 and blastp_afP35136 and chain A and name cb
dist intra_1316_valid , resid 51 and blastp_afP35136 and chain A and name cb, resid 207 and blastp_afP35136 and chain A and name cb
dist intra_2255_valid , resid 373 and blastp_afP35136 and chain A and name cb, resid 64 and blastp_afP35136 and chain A and name cb
dist intra_2554_out_range , resid 178 and blastp_afP35136 and chain A and name cb, resid 390 and blastp_afP35136 and chain A and name cb
dist intra_722_unknown , resid 508 and blastp_afP35136 and chain A and name cb, resid 217 and blastp_afP35136 and chain A and name cb
dist intra_3213_unknown , resid 178 and blastp_afP35136 and chain A and name cb, resid 376 and blastp_afP35136 and chain A and name cb
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
save blastp_afP35136.pse
png blastp_afP35136.png
