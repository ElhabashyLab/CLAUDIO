load blastp_afO07608.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO07608
color 3, chain A
show cartoon, chain A
dist intra_644_valid , resid 101 and blastp_afO07608 and chain A and name cb, resid 1 and blastp_afO07608 and chain A and name cb
dist intra_2253_valid , resid 141 and blastp_afO07608 and chain A and name cb, resid 46 and blastp_afO07608 and chain A and name cb
dist intra_873_unknown , resid 131 and blastp_afO07608 and chain A and name cb, resid 173 and blastp_afO07608 and chain A and name cb
dist intra_1248_unknown , resid 248 and blastp_afO07608 and chain A and name cb, resid 144 and blastp_afO07608 and chain A and name cb
dist intra_4153_unknown , resid 131 and blastp_afO07608 and chain A and name cb, resid 167 and blastp_afO07608 and chain A and name cb
dist intra_4453_unknown , resid 131 and blastp_afO07608 and chain A and name cb, resid 169 and blastp_afO07608 and chain A and name cb
dist intra_5444_unknown , resid 176 and blastp_afO07608 and chain A and name cb, resid 169 and blastp_afO07608 and chain A and name cb
dist intra_5550_unknown , resid 255 and blastp_afO07608 and chain A and name cb, resid 169 and blastp_afO07608 and chain A and name cb
dist intra_5860_unknown , resid 131 and blastp_afO07608 and chain A and name cb, resid 176 and blastp_afO07608 and chain A and name cb
dist intra_5889_unknown , resid 144 and blastp_afO07608 and chain A and name cb, resid 176 and blastp_afO07608 and chain A and name cb
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
save blastp_afO07608.pse
png blastp_afO07608.png
