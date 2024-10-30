load blastp_afP54475.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP54475
color 3, chain A
show cartoon, chain A
dist intra_705_valid , resid 32 and blastp_afP54475 and chain A and name cb, resid 206 and blastp_afP54475 and chain A and name cb
dist intra_751_valid , resid 65 and blastp_afP54475 and chain A and name cb, resid 40 and blastp_afP54475 and chain A and name cb
dist intra_2881_valid , resid 32 and blastp_afP54475 and chain A and name cb, resid 5 and blastp_afP54475 and chain A and name cb
dist intra_3539_valid , resid 40 and blastp_afP54475 and chain A and name cb, resid 206 and blastp_afP54475 and chain A and name cb
dist intra_5335_valid , resid 200 and blastp_afP54475 and chain A and name cb, resid 40 and blastp_afP54475 and chain A and name cb
dist intra_2290_out_range , resid 200 and blastp_afP54475 and chain A and name cb, resid 32 and blastp_afP54475 and chain A and name cb
dist intra_502_unknown , resid 213 and blastp_afP54475 and chain A and name cb, resid 32 and blastp_afP54475 and chain A and name cb
dist intra_813_unknown , resid 195 and blastp_afP54475 and chain A and name cb, resid 213 and blastp_afP54475 and chain A and name cb
dist intra_1547_unknown , resid 201 and blastp_afP54475 and chain A and name cb, resid 40 and blastp_afP54475 and chain A and name cb
dist intra_2566_unknown , resid 32 and blastp_afP54475 and chain A and name cb, resid 207 and blastp_afP54475 and chain A and name cb
dist intra_4083_unknown , resid 405 and blastp_afP54475 and chain A and name cb, resid 391 and blastp_afP54475 and chain A and name cb
dist intra_4595_unknown , resid 201 and blastp_afP54475 and chain A and name cb, resid 32 and blastp_afP54475 and chain A and name cb
dist intra_4680_unknown , resid 116 and blastp_afP54475 and chain A and name cb, resid 123 and blastp_afP54475 and chain A and name cb
dist intra_4966_unknown , resid 123 and blastp_afP54475 and chain A and name cb, resid 106 and blastp_afP54475 and chain A and name cb
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
save blastp_afP54475.pse
png blastp_afP54475.png
