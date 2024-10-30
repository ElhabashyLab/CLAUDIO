load blastp_afP22250.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP22250
color 3, chain A
show cartoon, chain A
dist intra_550_valid , resid 163 and blastp_afP22250 and chain A and name cb, resid 102 and blastp_afP22250 and chain A and name cb
dist intra_1000_valid , resid 134 and blastp_afP22250 and chain A and name cb, resid 145 and blastp_afP22250 and chain A and name cb
dist intra_1241_valid , resid 443 and blastp_afP22250 and chain A and name cb, resid 434 and blastp_afP22250 and chain A and name cb
dist intra_1801_valid , resid 446 and blastp_afP22250 and chain A and name cb, resid 443 and blastp_afP22250 and chain A and name cb
dist intra_3316_valid , resid 438 and blastp_afP22250 and chain A and name cb, resid 430 and blastp_afP22250 and chain A and name cb
dist intra_3572_valid , resid 152 and blastp_afP22250 and chain A and name cb, resid 48 and blastp_afP22250 and chain A and name cb
dist intra_3170_unknown , resid 48 and blastp_afP22250 and chain A and name cb, resid 255 and blastp_afP22250 and chain A and name cb
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
save blastp_afP22250.pse
png blastp_afP22250.png
