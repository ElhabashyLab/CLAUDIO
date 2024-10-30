load blastp_afP21469.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP21469
color 3, chain A
show cartoon, chain A
dist intra_351_valid , resid 38 and blastp_afP21469 and chain A and name cb, resid 114 and blastp_afP21469 and chain A and name cb
dist intra_727_valid , resid 9 and blastp_afP21469 and chain A and name cb, resid 21 and blastp_afP21469 and chain A and name cb
dist intra_807_valid , resid 29 and blastp_afP21469 and chain A and name cb, resid 9 and blastp_afP21469 and chain A and name cb
dist intra_993_valid , resid 67 and blastp_afP21469 and chain A and name cb, resid 21 and blastp_afP21469 and chain A and name cb
dist intra_1740_valid , resid 136 and blastp_afP21469 and chain A and name cb, resid 143 and blastp_afP21469 and chain A and name cb
dist intra_1835_valid , resid 4 and blastp_afP21469 and chain A and name cb, resid 21 and blastp_afP21469 and chain A and name cb
dist intra_4231_valid , resid 136 and blastp_afP21469 and chain A and name cb, resid 76 and blastp_afP21469 and chain A and name cb
dist intra_5414_valid , resid 38 and blastp_afP21469 and chain A and name cb, resid 30 and blastp_afP21469 and chain A and name cb
dist intra_5420_valid , resid 137 and blastp_afP21469 and chain A and name cb, resid 76 and blastp_afP21469 and chain A and name cb
dist intra_5984_valid , resid 45 and blastp_afP21469 and chain A and name cb, resid 114 and blastp_afP21469 and chain A and name cb
dist intra_6065_valid , resid 4 and blastp_afP21469 and chain A and name cb, resid 29 and blastp_afP21469 and chain A and name cb
dist intra_2551_out_range , resid 38 and blastp_afP21469 and chain A and name cb, resid 35 and blastp_afP21469 and chain A and name cb
dist intra_2366_overlaps , resid 21 and blastp_afP21469 and chain A and name cb, resid 54 and blastp_afP21469 and chain A and name cb
dist intra_4276_unknown , resid 136 and blastp_afP21469 and chain A and name cb, resid 139 and blastp_afP21469 and chain A and name cb
dist intra_5416_unknown , resid 68 and blastp_afP21469 and chain A and name cb, resid 137 and blastp_afP21469 and chain A and name cb
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
save blastp_afP21469.pse
png blastp_afP21469.png
