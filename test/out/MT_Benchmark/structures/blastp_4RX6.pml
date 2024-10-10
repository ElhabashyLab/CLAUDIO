load blastp_4RX6.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_4RX6
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_4RX6
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain D
show surface, chain D and blastp_4RX6
color 7, chain D
show cartoon, chain D
dist intra_3209_valid , resid 91 and blastp_4RX6 and chain A and name cb, resid 87 and blastp_4RX6 and chain A and name cb
dist intra_3209_5_valid , resid 91 and blastp_4RX6 and chain B and name cb, resid 87 and blastp_4RX6 and chain B and name cb
dist intra_3209_9_valid , resid 91 and blastp_4RX6 and chain D and name cb, resid 87 and blastp_4RX6 and chain D and name cb
dist intra_5505_out_range , resid 59 and blastp_4RX6 and chain A and name cb, resid 24 and blastp_4RX6 and chain A and name cb
dist inter_5505_3_valid , resid 59 and blastp_4RX6 and chain A and name cb, resid 24 and blastp_4RX6 and chain D and name cb
dist inter_5505_4_valid , resid 59 and blastp_4RX6 and chain B and name cb, resid 24 and blastp_4RX6 and chain A and name cb
dist inter_5505_8_valid , resid 59 and blastp_4RX6 and chain D and name cb, resid 24 and blastp_4RX6 and chain B and name cb
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
save blastp_4RX6.pse
png blastp_4RX6.png
