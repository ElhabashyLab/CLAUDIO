load blastp_afP38494.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP38494
color 3, chain A
show cartoon, chain A
dist intra_2438_valid , resid 271 and blastp_afP38494 and chain A and name cb, resid 326 and blastp_afP38494 and chain A and name cb
dist intra_159_unknown , resid 349 and blastp_afP38494 and chain A and name cb, resid 324 and blastp_afP38494 and chain A and name cb
dist intra_447_unknown , resid 144 and blastp_afP38494 and chain A and name cb, resid 110 and blastp_afP38494 and chain A and name cb
dist intra_682_unknown , resid 349 and blastp_afP38494 and chain A and name cb, resid 326 and blastp_afP38494 and chain A and name cb
dist intra_1926_unknown , resid 177 and blastp_afP38494 and chain A and name cb, resid 194 and blastp_afP38494 and chain A and name cb
dist intra_2050_unknown , resid 110 and blastp_afP38494 and chain A and name cb, resid 83 and blastp_afP38494 and chain A and name cb
dist intra_2457_unknown , resid 177 and blastp_afP38494 and chain A and name cb, resid 179 and blastp_afP38494 and chain A and name cb
dist intra_2567_unknown , resid 256 and blastp_afP38494 and chain A and name cb, resid 240 and blastp_afP38494 and chain A and name cb
dist intra_2628_unknown , resid 73 and blastp_afP38494 and chain A and name cb, resid 29 and blastp_afP38494 and chain A and name cb
dist intra_3072_unknown , resid 349 and blastp_afP38494 and chain A and name cb, resid 361 and blastp_afP38494 and chain A and name cb
dist intra_3900_unknown , resid 349 and blastp_afP38494 and chain A and name cb, resid 309 and blastp_afP38494 and chain A and name cb
dist intra_3954_unknown , resid 343 and blastp_afP38494 and chain A and name cb, resid 326 and blastp_afP38494 and chain A and name cb
dist intra_4180_unknown , resid 324 and blastp_afP38494 and chain A and name cb, resid 343 and blastp_afP38494 and chain A and name cb
dist intra_4387_unknown , resid 349 and blastp_afP38494 and chain A and name cb, resid 271 and blastp_afP38494 and chain A and name cb
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
save blastp_afP38494.pse
png blastp_afP38494.png
