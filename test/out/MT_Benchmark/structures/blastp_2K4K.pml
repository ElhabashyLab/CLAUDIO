load blastp_2K4K.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_2K4K
color 3, chain A
show cartoon, chain A
dist intra_741_valid , resid 85 and blastp_2K4K and chain A and name cb, resid 92 and blastp_2K4K and chain A and name cb
dist intra_876_valid , resid 85 and blastp_2K4K and chain A and name cb, resid 61 and blastp_2K4K and chain A and name cb
dist intra_2211_valid , resid 86 and blastp_2K4K and chain A and name cb, resid 92 and blastp_2K4K and chain A and name cb
dist intra_4040_valid , resid 92 and blastp_2K4K and chain A and name cb, resid 4 and blastp_2K4K and chain A and name cb
dist intra_4705_valid , resid 85 and blastp_2K4K and chain A and name cb, resid 89 and blastp_2K4K and chain A and name cb
dist intra_5554_valid , resid 69 and blastp_2K4K and chain A and name cb, resid 4 and blastp_2K4K and chain A and name cb
dist intra_5645_valid , resid 85 and blastp_2K4K and chain A and name cb, resid 71 and blastp_2K4K and chain A and name cb
dist intra_2481_out_range , resid 114 and blastp_2K4K and chain A and name cb, resid 92 and blastp_2K4K and chain A and name cb
dist intra_3598_out_range , resid 125 and blastp_2K4K and chain A and name cb, resid 85 and blastp_2K4K and chain A and name cb
dist intra_4770_out_range , resid 85 and blastp_2K4K and chain A and name cb, resid 114 and blastp_2K4K and chain A and name cb
dist intra_6134_out_range , resid 85 and blastp_2K4K and chain A and name cb, resid 112 and blastp_2K4K and chain A and name cb
dist intra_6143_out_range , resid 69 and blastp_2K4K and chain A and name cb, resid 92 and blastp_2K4K and chain A and name cb
dist intra_4195_unknown , resid 114 and blastp_2K4K and chain A and name cb, resid 71 and blastp_2K4K and chain A and name cb
dist intra_5393_unknown , resid 125 and blastp_2K4K and chain A and name cb, resid 71 and blastp_2K4K and chain A and name cb
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
save blastp_2K4K.pse
png blastp_2K4K.png
