load blastp_afP08821.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP08821
color 3, chain A
show cartoon, chain A
dist intra_67_valid , resid 37 and blastp_afP08821 and chain A and name cb, resid 75 and blastp_afP08821 and chain A and name cb
dist intra_595_valid , resid 80 and blastp_afP08821 and chain A and name cb, resid 41 and blastp_afP08821 and chain A and name cb
dist intra_851_valid , resid 86 and blastp_afP08821 and chain A and name cb, resid 80 and blastp_afP08821 and chain A and name cb
dist intra_1476_valid , resid 92 and blastp_afP08821 and chain A and name cb, resid 83 and blastp_afP08821 and chain A and name cb
dist intra_4274_valid , resid 41 and blastp_afP08821 and chain A and name cb, resid 75 and blastp_afP08821 and chain A and name cb
dist intra_564_out_range , resid 92 and blastp_afP08821 and chain A and name cb, resid 75 and blastp_afP08821 and chain A and name cb
dist intra_762_out_range , resid 92 and blastp_afP08821 and chain A and name cb, resid 37 and blastp_afP08821 and chain A and name cb
dist intra_1026_out_range , resid 83 and blastp_afP08821 and chain A and name cb, resid 37 and blastp_afP08821 and chain A and name cb
dist intra_3472_out_range , resid 92 and blastp_afP08821 and chain A and name cb, resid 59 and blastp_afP08821 and chain A and name cb
dist intra_4204_unknown , resid 38 and blastp_afP08821 and chain A and name cb, resid 75 and blastp_afP08821 and chain A and name cb
dist intra_6117_unknown , resid 92 and blastp_afP08821 and chain A and name cb, resid 62 and blastp_afP08821 and chain A and name cb
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
save blastp_afP08821.pse
png blastp_afP08821.png
