load blastp_afP23129.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP23129
color 3, chain A
show cartoon, chain A
dist intra_34_valid , resid 842 and blastp_afP23129 and chain A and name cb, resid 929 and blastp_afP23129 and chain A and name cb
dist intra_54_valid , resid 165 and blastp_afP23129 and chain A and name cb, resid 411 and blastp_afP23129 and chain A and name cb
dist intra_857_valid , resid 173 and blastp_afP23129 and chain A and name cb, resid 134 and blastp_afP23129 and chain A and name cb
dist intra_1795_valid , resid 182 and blastp_afP23129 and chain A and name cb, resid 134 and blastp_afP23129 and chain A and name cb
dist intra_4502_valid , resid 447 and blastp_afP23129 and chain A and name cb, resid 173 and blastp_afP23129 and chain A and name cb
dist intra_5831_valid , resid 516 and blastp_afP23129 and chain A and name cb, resid 524 and blastp_afP23129 and chain A and name cb
dist intra_3918_overlaps , resid 62 and blastp_afP23129 and chain A and name cb, resid 56 and blastp_afP23129 and chain A and name cb
dist intra_206_unknown , resid 104 and blastp_afP23129 and chain A and name cb, resid 411 and blastp_afP23129 and chain A and name cb
dist intra_511_unknown , resid 213 and blastp_afP23129 and chain A and name cb, resid 929 and blastp_afP23129 and chain A and name cb
dist intra_1805_unknown , resid 528 and blastp_afP23129 and chain A and name cb, resid 930 and blastp_afP23129 and chain A and name cb
dist intra_2179_unknown , resid 447 and blastp_afP23129 and chain A and name cb, resid 311 and blastp_afP23129 and chain A and name cb
dist intra_2561_unknown , resid 842 and blastp_afP23129 and chain A and name cb, resid 918 and blastp_afP23129 and chain A and name cb
dist intra_2712_unknown , resid 100 and blastp_afP23129 and chain A and name cb, resid 411 and blastp_afP23129 and chain A and name cb
dist intra_3486_unknown , resid 447 and blastp_afP23129 and chain A and name cb, resid 304 and blastp_afP23129 and chain A and name cb
dist intra_4218_unknown , resid 1 and blastp_afP23129 and chain A and name cb, resid 134 and blastp_afP23129 and chain A and name cb
dist intra_4306_unknown , resid 74 and blastp_afP23129 and chain A and name cb, resid 62 and blastp_afP23129 and chain A and name cb
dist intra_4312_unknown , resid 153 and blastp_afP23129 and chain A and name cb, resid 411 and blastp_afP23129 and chain A and name cb
dist intra_4347_unknown , resid 151 and blastp_afP23129 and chain A and name cb, resid 104 and blastp_afP23129 and chain A and name cb
dist intra_4572_unknown , resid 213 and blastp_afP23129 and chain A and name cb, resid 577 and blastp_afP23129 and chain A and name cb
dist intra_4725_unknown , resid 213 and blastp_afP23129 and chain A and name cb, resid 918 and blastp_afP23129 and chain A and name cb
dist intra_4766_unknown , resid 62 and blastp_afP23129 and chain A and name cb, resid 121 and blastp_afP23129 and chain A and name cb
dist intra_6060_unknown , resid 213 and blastp_afP23129 and chain A and name cb, resid 561 and blastp_afP23129 and chain A and name cb
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
save blastp_afP23129.pse
png blastp_afP23129.png
