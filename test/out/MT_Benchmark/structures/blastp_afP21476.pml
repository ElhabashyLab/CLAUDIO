load blastp_afP21476.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP21476
color 3, chain A
show cartoon, chain A
dist intra_148_valid , resid 56 and blastp_afP21476 and chain A and name cb, resid 32 and blastp_afP21476 and chain A and name cb
dist intra_226_valid , resid 18 and blastp_afP21476 and chain A and name cb, resid 27 and blastp_afP21476 and chain A and name cb
dist intra_255_valid , resid 7 and blastp_afP21476 and chain A and name cb, resid 27 and blastp_afP21476 and chain A and name cb
dist intra_1112_valid , resid 28 and blastp_afP21476 and chain A and name cb, resid 56 and blastp_afP21476 and chain A and name cb
dist intra_1243_valid , resid 56 and blastp_afP21476 and chain A and name cb, resid 81 and blastp_afP21476 and chain A and name cb
dist intra_1283_valid , resid 18 and blastp_afP21476 and chain A and name cb, resid 32 and blastp_afP21476 and chain A and name cb
dist intra_3143_valid , resid 7 and blastp_afP21476 and chain A and name cb, resid 70 and blastp_afP21476 and chain A and name cb
dist intra_3502_valid , resid 28 and blastp_afP21476 and chain A and name cb, resid 18 and blastp_afP21476 and chain A and name cb
dist intra_3592_valid , resid 7 and blastp_afP21476 and chain A and name cb, resid 32 and blastp_afP21476 and chain A and name cb
dist intra_2834_out_range , resid 28 and blastp_afP21476 and chain A and name cb, resid 7 and blastp_afP21476 and chain A and name cb
dist intra_3764_overlaps , resid 7 and blastp_afP21476 and chain A and name cb, resid 22 and blastp_afP21476 and chain A and name cb
dist intra_2072_unknown , resid 18 and blastp_afP21476 and chain A and name cb, resid 22 and blastp_afP21476 and chain A and name cb
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
save blastp_afP21476.pse
png blastp_afP21476.png
