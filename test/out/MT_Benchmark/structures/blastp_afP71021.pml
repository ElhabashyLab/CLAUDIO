load blastp_afP71021.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP71021
color 3, chain A
show cartoon, chain A
dist intra_265_valid , resid 113 and blastp_afP71021 and chain A and name cb, resid 110 and blastp_afP71021 and chain A and name cb
dist intra_1038_valid , resid 11 and blastp_afP71021 and chain A and name cb, resid 34 and blastp_afP71021 and chain A and name cb
dist intra_1184_valid , resid 42 and blastp_afP71021 and chain A and name cb, resid 34 and blastp_afP71021 and chain A and name cb
dist intra_2328_valid , resid 122 and blastp_afP71021 and chain A and name cb, resid 110 and blastp_afP71021 and chain A and name cb
dist intra_2410_valid , resid 90 and blastp_afP71021 and chain A and name cb, resid 98 and blastp_afP71021 and chain A and name cb
dist intra_4070_valid , resid 126 and blastp_afP71021 and chain A and name cb, resid 110 and blastp_afP71021 and chain A and name cb
dist intra_5635_valid , resid 122 and blastp_afP71021 and chain A and name cb, resid 126 and blastp_afP71021 and chain A and name cb
dist intra_2655_overlaps , resid 43 and blastp_afP71021 and chain A and name cb, resid 42 and blastp_afP71021 and chain A and name cb
dist intra_3188_overlaps , resid 122 and blastp_afP71021 and chain A and name cb, resid 113 and blastp_afP71021 and chain A and name cb
dist intra_5725_same , resid 122 and blastp_afP71021 and chain A and name cb, resid 122 and blastp_afP71021 and chain A and name cb
dist intra_3500_unknown , resid 90 and blastp_afP71021 and chain A and name cb, resid 95 and blastp_afP71021 and chain A and name cb
dist intra_3961_unknown , resid 114 and blastp_afP71021 and chain A and name cb, resid 110 and blastp_afP71021 and chain A and name cb
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
save blastp_afP71021.pse
png blastp_afP71021.png
