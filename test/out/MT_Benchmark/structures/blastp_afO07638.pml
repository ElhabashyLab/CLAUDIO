load blastp_afO07638.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO07638
color 3, chain A
show cartoon, chain A
dist intra_2710_valid , resid 26 and blastp_afO07638 and chain A and name cb, resid 18 and blastp_afO07638 and chain A and name cb
dist intra_2625_overlaps , resid 1 and blastp_afO07638 and chain A and name cb, resid 11 and blastp_afO07638 and chain A and name cb
dist intra_2429_unknown , resid 1 and blastp_afO07638 and chain A and name cb, resid 23 and blastp_afO07638 and chain A and name cb
dist intra_2812_unknown , resid 1 and blastp_afO07638 and chain A and name cb, resid 12 and blastp_afO07638 and chain A and name cb
dist intra_3399_unknown , resid 18 and blastp_afO07638 and chain A and name cb, resid 1 and blastp_afO07638 and chain A and name cb
dist intra_3492_unknown , resid 1 and blastp_afO07638 and chain A and name cb, resid 70 and blastp_afO07638 and chain A and name cb
dist intra_5902_unknown , resid 26 and blastp_afO07638 and chain A and name cb, resid 1 and blastp_afO07638 and chain A and name cb
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
save blastp_afO07638.pse
png blastp_afO07638.png
