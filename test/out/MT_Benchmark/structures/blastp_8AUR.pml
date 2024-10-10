load blastp_8AUR.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_8AUR
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_8AUR
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain C
show surface, chain C and blastp_8AUR
color 7, chain C
show cartoon, chain C
dist intra_700_valid , resid 176 and blastp_8AUR and chain A and name cb, resid 160 and blastp_8AUR and chain A and name cb
dist intra_700_5_valid , resid 176 and blastp_8AUR and chain B and name cb, resid 160 and blastp_8AUR and chain B and name cb
dist intra_700_9_valid , resid 176 and blastp_8AUR and chain C and name cb, resid 160 and blastp_8AUR and chain C and name cb
dist intra_1379_valid , resid 136 and blastp_8AUR and chain A and name cb, resid 152 and blastp_8AUR and chain A and name cb
dist intra_1379_5_valid , resid 136 and blastp_8AUR and chain B and name cb, resid 152 and blastp_8AUR and chain B and name cb
dist intra_1379_9_valid , resid 136 and blastp_8AUR and chain C and name cb, resid 152 and blastp_8AUR and chain C and name cb
dist intra_1405_valid , resid 176 and blastp_8AUR and chain A and name cb, resid 126 and blastp_8AUR and chain A and name cb
dist intra_1405_5_valid , resid 176 and blastp_8AUR and chain B and name cb, resid 126 and blastp_8AUR and chain B and name cb
dist intra_1405_9_valid , resid 176 and blastp_8AUR and chain C and name cb, resid 126 and blastp_8AUR and chain C and name cb
dist intra_1419_valid , resid 176 and blastp_8AUR and chain A and name cb, resid 155 and blastp_8AUR and chain A and name cb
dist intra_1419_5_valid , resid 176 and blastp_8AUR and chain B and name cb, resid 155 and blastp_8AUR and chain B and name cb
dist intra_1419_9_valid , resid 176 and blastp_8AUR and chain C and name cb, resid 155 and blastp_8AUR and chain C and name cb
dist intra_1665_valid , resid 240 and blastp_8AUR and chain A and name cb, resid 250 and blastp_8AUR and chain A and name cb
dist intra_1665_5_valid , resid 240 and blastp_8AUR and chain B and name cb, resid 250 and blastp_8AUR and chain B and name cb
dist intra_1665_9_valid , resid 240 and blastp_8AUR and chain C and name cb, resid 250 and blastp_8AUR and chain C and name cb
dist intra_1842_valid , resid 260 and blastp_8AUR and chain A and name cb, resid 176 and blastp_8AUR and chain A and name cb
dist intra_1842_5_valid , resid 260 and blastp_8AUR and chain B and name cb, resid 176 and blastp_8AUR and chain B and name cb
dist intra_1842_9_valid , resid 260 and blastp_8AUR and chain C and name cb, resid 176 and blastp_8AUR and chain C and name cb
dist intra_1998_valid , resid 260 and blastp_8AUR and chain A and name cb, resid 160 and blastp_8AUR and chain A and name cb
dist intra_1998_5_valid , resid 260 and blastp_8AUR and chain B and name cb, resid 160 and blastp_8AUR and chain B and name cb
dist intra_1998_9_valid , resid 260 and blastp_8AUR and chain C and name cb, resid 160 and blastp_8AUR and chain C and name cb
dist intra_2145_valid , resid 201 and blastp_8AUR and chain A and name cb, resid 152 and blastp_8AUR and chain A and name cb
dist intra_2145_5_valid , resid 201 and blastp_8AUR and chain B and name cb, resid 152 and blastp_8AUR and chain B and name cb
dist intra_2145_9_valid , resid 201 and blastp_8AUR and chain C and name cb, resid 152 and blastp_8AUR and chain C and name cb
dist intra_2789_valid , resid 65 and blastp_8AUR and chain A and name cb, resid 126 and blastp_8AUR and chain A and name cb
dist intra_2789_5_valid , resid 65 and blastp_8AUR and chain B and name cb, resid 126 and blastp_8AUR and chain B and name cb
dist intra_2789_9_valid , resid 65 and blastp_8AUR and chain C and name cb, resid 126 and blastp_8AUR and chain C and name cb
dist intra_3304_valid , resid 155 and blastp_8AUR and chain A and name cb, resid 152 and blastp_8AUR and chain A and name cb
dist intra_3304_5_valid , resid 155 and blastp_8AUR and chain B and name cb, resid 152 and blastp_8AUR and chain B and name cb
dist intra_3304_9_valid , resid 155 and blastp_8AUR and chain C and name cb, resid 152 and blastp_8AUR and chain C and name cb
dist intra_4816_valid , resid 160 and blastp_8AUR and chain A and name cb, resid 126 and blastp_8AUR and chain A and name cb
dist intra_4816_5_valid , resid 160 and blastp_8AUR and chain B and name cb, resid 126 and blastp_8AUR and chain B and name cb
dist intra_4816_9_valid , resid 160 and blastp_8AUR and chain C and name cb, resid 126 and blastp_8AUR and chain C and name cb
dist intra_5205_valid , resid 216 and blastp_8AUR and chain A and name cb, resid 136 and blastp_8AUR and chain A and name cb
dist intra_5205_5_valid , resid 216 and blastp_8AUR and chain B and name cb, resid 136 and blastp_8AUR and chain B and name cb
dist intra_5205_9_valid , resid 216 and blastp_8AUR and chain C and name cb, resid 136 and blastp_8AUR and chain C and name cb
dist intra_26_out_range , resid 209 and blastp_8AUR and chain A and name cb, resid 144 and blastp_8AUR and chain A and name cb
dist inter_26_3_valid , resid 209 and blastp_8AUR and chain A and name cb, resid 144 and blastp_8AUR and chain C and name cb
dist inter_26_4_valid , resid 209 and blastp_8AUR and chain B and name cb, resid 144 and blastp_8AUR and chain A and name cb
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
save blastp_8AUR.pse
png blastp_8AUR.png
