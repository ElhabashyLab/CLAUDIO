load blastp_afO31501.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afO31501
color 3, chain A
show cartoon, chain A
dist intra_1104_valid , resid 799 and blastp_afO31501 and chain A and name cb, resid 193 and blastp_afO31501 and chain A and name cb
dist intra_2327_valid , resid 815 and blastp_afO31501 and chain A and name cb, resid 744 and blastp_afO31501 and chain A and name cb
dist intra_2775_valid , resid 297 and blastp_afO31501 and chain A and name cb, resid 240 and blastp_afO31501 and chain A and name cb
dist intra_3522_valid , resid 809 and blastp_afO31501 and chain A and name cb, resid 793 and blastp_afO31501 and chain A and name cb
dist intra_5617_valid , resid 793 and blastp_afO31501 and chain A and name cb, resid 799 and blastp_afO31501 and chain A and name cb
dist intra_5825_valid , resid 605 and blastp_afO31501 and chain A and name cb, resid 123 and blastp_afO31501 and chain A and name cb
dist intra_5833_valid , resid 799 and blastp_afO31501 and chain A and name cb, resid 191 and blastp_afO31501 and chain A and name cb
dist intra_5381_out_range , resid 772 and blastp_afO31501 and chain A and name cb, resid 817 and blastp_afO31501 and chain A and name cb
dist intra_4538_unknown , resid 301 and blastp_afO31501 and chain A and name cb, resid 605 and blastp_afO31501 and chain A and name cb
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
save blastp_afO31501.pse
png blastp_afO31501.png
