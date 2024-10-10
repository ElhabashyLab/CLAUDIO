load blastp_2VSQ.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_2VSQ
color 3, chain A
show cartoon, chain A
dist intra_1552_valid , resid 522 and blastp_2VSQ and chain A and name cb, resid 547 and blastp_2VSQ and chain A and name cb
dist intra_2607_valid , resid 6 and blastp_2VSQ and chain A and name cb, resid 74 and blastp_2VSQ and chain A and name cb
dist intra_2870_valid , resid 1015 and blastp_2VSQ and chain A and name cb, resid 1185 and blastp_2VSQ and chain A and name cb
dist intra_4329_valid , resid 6 and blastp_2VSQ and chain A and name cb, resid 76 and blastp_2VSQ and chain A and name cb
dist intra_4642_valid , resid 1015 and blastp_2VSQ and chain A and name cb, resid 76 and blastp_2VSQ and chain A and name cb
dist intra_5074_valid , resid 195 and blastp_2VSQ and chain A and name cb, resid 76 and blastp_2VSQ and chain A and name cb
dist intra_5592_valid , resid 192 and blastp_2VSQ and chain A and name cb, resid 181 and blastp_2VSQ and chain A and name cb
dist intra_1401_out_range , resid 923 and blastp_2VSQ and chain A and name cb, resid 547 and blastp_2VSQ and chain A and name cb
dist intra_2150_out_range , resid 956 and blastp_2VSQ and chain A and name cb, resid 988 and blastp_2VSQ and chain A and name cb
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
save blastp_2VSQ.pse
png blastp_2VSQ.png
