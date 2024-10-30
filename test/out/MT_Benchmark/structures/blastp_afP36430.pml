load blastp_afP36430.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP36430
color 3, chain A
show cartoon, chain A
dist intra_472_valid , resid 790 and blastp_afP36430 and chain A and name cb, resid 766 and blastp_afP36430 and chain A and name cb
dist intra_671_valid , resid 757 and blastp_afP36430 and chain A and name cb, resid 778 and blastp_afP36430 and chain A and name cb
dist intra_1953_valid , resid 757 and blastp_afP36430 and chain A and name cb, resid 797 and blastp_afP36430 and chain A and name cb
dist intra_1839_unknown , resid 298 and blastp_afP36430 and chain A and name cb, resid 288 and blastp_afP36430 and chain A and name cb
dist intra_3593_unknown , resid 757 and blastp_afP36430 and chain A and name cb, resid 767 and blastp_afP36430 and chain A and name cb
dist intra_4358_unknown , resid 581 and blastp_afP36430 and chain A and name cb, resid 563 and blastp_afP36430 and chain A and name cb
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
save blastp_afP36430.pse
png blastp_afP36430.png
