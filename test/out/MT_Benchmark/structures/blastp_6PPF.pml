load blastp_6PPF.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain L
show surface, chain L and blastp_6PPF
color 3, chain L
show cartoon, chain L
hide everything, show cartoon, chain Q
show surface, chain Q and blastp_6PPF
color 5, chain Q
show cartoon, chain Q
dist intra_1675_valid , resid 72 and blastp_6PPF and chain L and name cb, resid 127 and blastp_6PPF and chain L and name cb
dist intra_4353_valid , resid 22 and blastp_6PPF and chain Q and name cb, resid 33 and blastp_6PPF and chain Q and name cb
dist intra_4881_valid , resid 29 and blastp_6PPF and chain L and name cb, resid 36 and blastp_6PPF and chain L and name cb
dist intra_1640_out_range , resid 127 and blastp_6PPF and chain L and name cb, resid 110 and blastp_6PPF and chain L and name cb
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
save blastp_6PPF.pse
png blastp_6PPF.png
