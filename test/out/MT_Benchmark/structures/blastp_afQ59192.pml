load blastp_afQ59192.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afQ59192
color 3, chain A
show cartoon, chain A
dist intra_1064_valid , resid 342 and blastp_afQ59192 and chain A and name cb, resid 287 and blastp_afQ59192 and chain A and name cb
dist intra_2189_valid , resid 277 and blastp_afQ59192 and chain A and name cb, resid 603 and blastp_afQ59192 and chain A and name cb
dist intra_3923_valid , resid 566 and blastp_afQ59192 and chain A and name cb, resid 543 and blastp_afQ59192 and chain A and name cb
dist intra_4890_valid , resid 380 and blastp_afQ59192 and chain A and name cb, resid 305 and blastp_afQ59192 and chain A and name cb
dist intra_4906_valid , resid 438 and blastp_afQ59192 and chain A and name cb, resid 411 and blastp_afQ59192 and chain A and name cb
dist intra_5175_valid , resid 376 and blastp_afQ59192 and chain A and name cb, resid 380 and blastp_afQ59192 and chain A and name cb
dist intra_5585_valid , resid 277 and blastp_afQ59192 and chain A and name cb, resid 342 and blastp_afQ59192 and chain A and name cb
dist intra_6138_valid , resid 460 and blastp_afQ59192 and chain A and name cb, resid 621 and blastp_afQ59192 and chain A and name cb
dist intra_3526_out_range , resid 380 and blastp_afQ59192 and chain A and name cb, resid 422 and blastp_afQ59192 and chain A and name cb
dist intra_4609_unknown , resid 340 and blastp_afQ59192 and chain A and name cb, resid 105 and blastp_afQ59192 and chain A and name cb
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
save blastp_afQ59192.pse
png blastp_afQ59192.png
