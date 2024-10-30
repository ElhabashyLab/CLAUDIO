load blastp_afP40778.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP40778
color 3, chain A
show cartoon, chain A
dist intra_91_valid , resid 100 and blastp_afP40778 and chain A and name cb, resid 10 and blastp_afP40778 and chain A and name cb
dist intra_724_valid , resid 302 and blastp_afP40778 and chain A and name cb, resid 45 and blastp_afP40778 and chain A and name cb
dist intra_2819_valid , resid 296 and blastp_afP40778 and chain A and name cb, resid 302 and blastp_afP40778 and chain A and name cb
dist intra_3627_valid , resid 296 and blastp_afP40778 and chain A and name cb, resid 45 and blastp_afP40778 and chain A and name cb
dist intra_5226_valid , resid 10 and blastp_afP40778 and chain A and name cb, resid 59 and blastp_afP40778 and chain A and name cb
dist intra_2937_unknown , resid 100 and blastp_afP40778 and chain A and name cb, resid 1 and blastp_afP40778 and chain A and name cb
dist intra_5994_unknown , resid 296 and blastp_afP40778 and chain A and name cb, resid 329 and blastp_afP40778 and chain A and name cb
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
save blastp_afP40778.pse
png blastp_afP40778.png
