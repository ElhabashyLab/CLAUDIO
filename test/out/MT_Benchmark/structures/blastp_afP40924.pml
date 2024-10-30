load blastp_afP40924.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP40924
color 3, chain A
show cartoon, chain A
dist intra_4_valid , resid 125 and blastp_afP40924 and chain A and name cb, resid 64 and blastp_afP40924 and chain A and name cb
dist intra_21_valid , resid 242 and blastp_afP40924 and chain A and name cb, resid 197 and blastp_afP40924 and chain A and name cb
dist intra_77_valid , resid 86 and blastp_afP40924 and chain A and name cb, resid 45 and blastp_afP40924 and chain A and name cb
dist intra_262_valid , resid 7 and blastp_afP40924 and chain A and name cb, resid 45 and blastp_afP40924 and chain A and name cb
dist intra_327_valid , resid 173 and blastp_afP40924 and chain A and name cb, resid 7 and blastp_afP40924 and chain A and name cb
dist intra_470_valid , resid 107 and blastp_afP40924 and chain A and name cb, resid 89 and blastp_afP40924 and chain A and name cb
dist intra_517_valid , resid 342 and blastp_afP40924 and chain A and name cb, resid 308 and blastp_afP40924 and chain A and name cb
dist intra_1378_valid , resid 27 and blastp_afP40924 and chain A and name cb, resid 359 and blastp_afP40924 and chain A and name cb
dist intra_1545_valid , resid 394 and blastp_afP40924 and chain A and name cb, resid 180 and blastp_afP40924 and chain A and name cb
dist intra_1548_valid , resid 4 and blastp_afP40924 and chain A and name cb, resid 45 and blastp_afP40924 and chain A and name cb
dist intra_1641_valid , resid 86 and blastp_afP40924 and chain A and name cb, resid 107 and blastp_afP40924 and chain A and name cb
dist intra_1746_valid , resid 64 and blastp_afP40924 and chain A and name cb, resid 197 and blastp_afP40924 and chain A and name cb
dist intra_2052_valid , resid 106 and blastp_afP40924 and chain A and name cb, resid 89 and blastp_afP40924 and chain A and name cb
dist intra_2054_valid , resid 7 and blastp_afP40924 and chain A and name cb, resid 394 and blastp_afP40924 and chain A and name cb
dist intra_2177_valid , resid 132 and blastp_afP40924 and chain A and name cb, resid 90 and blastp_afP40924 and chain A and name cb
dist intra_3133_valid , resid 12 and blastp_afP40924 and chain A and name cb, resid 107 and blastp_afP40924 and chain A and name cb
dist intra_4296_valid , resid 26 and blastp_afP40924 and chain A and name cb, resid 359 and blastp_afP40924 and chain A and name cb
dist intra_5823_valid , resid 86 and blastp_afP40924 and chain A and name cb, resid 106 and blastp_afP40924 and chain A and name cb
dist intra_6129_valid , resid 197 and blastp_afP40924 and chain A and name cb, resid 201 and blastp_afP40924 and chain A and name cb
dist intra_1176_overlaps , resid 152 and blastp_afP40924 and chain A and name cb, resid 7 and blastp_afP40924 and chain A and name cb
dist intra_789_unknown , resid 45 and blastp_afP40924 and chain A and name cb, resid 80 and blastp_afP40924 and chain A and name cb
dist intra_916_unknown , resid 236 and blastp_afP40924 and chain A and name cb, resid 197 and blastp_afP40924 and chain A and name cb
dist intra_1453_unknown , resid 119 and blastp_afP40924 and chain A and name cb, resid 64 and blastp_afP40924 and chain A and name cb
dist intra_3273_unknown , resid 27 and blastp_afP40924 and chain A and name cb, resid 343 and blastp_afP40924 and chain A and name cb
dist intra_4615_unknown , resid 342 and blastp_afP40924 and chain A and name cb, resid 299 and blastp_afP40924 and chain A and name cb
dist intra_5204_unknown , resid 333 and blastp_afP40924 and chain A and name cb, resid 308 and blastp_afP40924 and chain A and name cb
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
save blastp_afP40924.pse
png blastp_afP40924.png
