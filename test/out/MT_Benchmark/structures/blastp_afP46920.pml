load blastp_afP46920.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP46920
color 3, chain A
show cartoon, chain A
dist intra_1276_valid , resid 331 and blastp_afP46920 and chain A and name cb, resid 305 and blastp_afP46920 and chain A and name cb
dist intra_2186_valid , resid 286 and blastp_afP46920 and chain A and name cb, resid 305 and blastp_afP46920 and chain A and name cb
dist intra_3083_valid , resid 304 and blastp_afP46920 and chain A and name cb, resid 331 and blastp_afP46920 and chain A and name cb
dist intra_5712_valid , resid 286 and blastp_afP46920 and chain A and name cb, resid 331 and blastp_afP46920 and chain A and name cb
dist intra_142_out_range , resid 286 and blastp_afP46920 and chain A and name cb, resid 206 and blastp_afP46920 and chain A and name cb
dist intra_1527_unknown , resid 278 and blastp_afP46920 and chain A and name cb, resid 206 and blastp_afP46920 and chain A and name cb
dist intra_1585_unknown , resid 286 and blastp_afP46920 and chain A and name cb, resid 278 and blastp_afP46920 and chain A and name cb
dist intra_2990_unknown , resid 2 and blastp_afP46920 and chain A and name cb, resid 295 and blastp_afP46920 and chain A and name cb
dist intra_4631_unknown , resid 2 and blastp_afP46920 and chain A and name cb, resid 286 and blastp_afP46920 and chain A and name cb
dist intra_5640_unknown , resid 2 and blastp_afP46920 and chain A and name cb, resid 14 and blastp_afP46920 and chain A and name cb
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
save blastp_afP46920.pse
png blastp_afP46920.png
