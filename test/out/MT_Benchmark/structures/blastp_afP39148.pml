load blastp_afP39148.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP39148
color 3, chain A
show cartoon, chain A
dist intra_36_valid , resid 349 and blastp_afP39148 and chain A and name cb, resid 325 and blastp_afP39148 and chain A and name cb
dist intra_103_valid , resid 411 and blastp_afP39148 and chain A and name cb, resid 1 and blastp_afP39148 and chain A and name cb
dist intra_185_valid , resid 58 and blastp_afP39148 and chain A and name cb, resid 245 and blastp_afP39148 and chain A and name cb
dist intra_279_valid , resid 248 and blastp_afP39148 and chain A and name cb, resid 244 and blastp_afP39148 and chain A and name cb
dist intra_319_valid , resid 411 and blastp_afP39148 and chain A and name cb, resid 16 and blastp_afP39148 and chain A and name cb
dist intra_523_valid , resid 248 and blastp_afP39148 and chain A and name cb, resid 58 and blastp_afP39148 and chain A and name cb
dist intra_539_out_range , resid 340 and blastp_afP39148 and chain A and name cb, resid 58 and blastp_afP39148 and chain A and name cb
dist intra_569_out_range , resid 349 and blastp_afP39148 and chain A and name cb, resid 245 and blastp_afP39148 and chain A and name cb
dist intra_1118_out_range , resid 349 and blastp_afP39148 and chain A and name cb, resid 58 and blastp_afP39148 and chain A and name cb
dist intra_147_unknown , resid 341 and blastp_afP39148 and chain A and name cb, resid 325 and blastp_afP39148 and chain A and name cb
dist intra_388_unknown , resid 325 and blastp_afP39148 and chain A and name cb, resid 58 and blastp_afP39148 and chain A and name cb
dist intra_1688_unknown , resid 325 and blastp_afP39148 and chain A and name cb, resid 51 and blastp_afP39148 and chain A and name cb
dist intra_2316_unknown , resid 340 and blastp_afP39148 and chain A and name cb, resid 51 and blastp_afP39148 and chain A and name cb
dist intra_2502_unknown , resid 349 and blastp_afP39148 and chain A and name cb, resid 51 and blastp_afP39148 and chain A and name cb
dist intra_2647_unknown , resid 248 and blastp_afP39148 and chain A and name cb, resid 51 and blastp_afP39148 and chain A and name cb
dist intra_2905_unknown , resid 341 and blastp_afP39148 and chain A and name cb, resid 58 and blastp_afP39148 and chain A and name cb
dist intra_2957_unknown , resid 245 and blastp_afP39148 and chain A and name cb, resid 51 and blastp_afP39148 and chain A and name cb
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
save blastp_afP39148.pse
png blastp_afP39148.png
