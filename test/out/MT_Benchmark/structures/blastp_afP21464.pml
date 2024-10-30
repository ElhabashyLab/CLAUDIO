load blastp_afP21464.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP21464
color 3, chain A
show cartoon, chain A
dist intra_81_valid , resid 155 and blastp_afP21464 and chain A and name cb, resid 119 and blastp_afP21464 and chain A and name cb
dist intra_115_valid , resid 74 and blastp_afP21464 and chain A and name cb, resid 211 and blastp_afP21464 and chain A and name cb
dist intra_128_valid , resid 146 and blastp_afP21464 and chain A and name cb, resid 74 and blastp_afP21464 and chain A and name cb
dist intra_231_valid , resid 45 and blastp_afP21464 and chain A and name cb, resid 49 and blastp_afP21464 and chain A and name cb
dist intra_504_valid , resid 216 and blastp_afP21464 and chain A and name cb, resid 49 and blastp_afP21464 and chain A and name cb
dist intra_610_valid , resid 81 and blastp_afP21464 and chain A and name cb, resid 146 and blastp_afP21464 and chain A and name cb
dist intra_786_valid , resid 154 and blastp_afP21464 and chain A and name cb, resid 119 and blastp_afP21464 and chain A and name cb
dist intra_921_valid , resid 81 and blastp_afP21464 and chain A and name cb, resid 152 and blastp_afP21464 and chain A and name cb
dist intra_985_valid , resid 66 and blastp_afP21464 and chain A and name cb, resid 154 and blastp_afP21464 and chain A and name cb
dist intra_1021_valid , resid 155 and blastp_afP21464 and chain A and name cb, resid 109 and blastp_afP21464 and chain A and name cb
dist intra_1113_valid , resid 74 and blastp_afP21464 and chain A and name cb, resid 152 and blastp_afP21464 and chain A and name cb
dist intra_1220_valid , resid 66 and blastp_afP21464 and chain A and name cb, resid 155 and blastp_afP21464 and chain A and name cb
dist intra_1411_valid , resid 138 and blastp_afP21464 and chain A and name cb, resid 120 and blastp_afP21464 and chain A and name cb
dist intra_1660_valid , resid 109 and blastp_afP21464 and chain A and name cb, resid 154 and blastp_afP21464 and chain A and name cb
dist intra_2114_valid , resid 155 and blastp_afP21464 and chain A and name cb, resid 115 and blastp_afP21464 and chain A and name cb
dist intra_2135_valid , resid 81 and blastp_afP21464 and chain A and name cb, resid 211 and blastp_afP21464 and chain A and name cb
dist intra_2679_valid , resid 7 and blastp_afP21464 and chain A and name cb, resid 49 and blastp_afP21464 and chain A and name cb
dist intra_2844_valid , resid 138 and blastp_afP21464 and chain A and name cb, resid 131 and blastp_afP21464 and chain A and name cb
dist intra_3317_valid , resid 49 and blastp_afP21464 and chain A and name cb, resid 211 and blastp_afP21464 and chain A and name cb
dist intra_3919_valid , resid 73 and blastp_afP21464 and chain A and name cb, resid 81 and blastp_afP21464 and chain A and name cb
dist intra_4830_valid , resid 73 and blastp_afP21464 and chain A and name cb, resid 211 and blastp_afP21464 and chain A and name cb
dist intra_4845_valid , resid 74 and blastp_afP21464 and chain A and name cb, resid 66 and blastp_afP21464 and chain A and name cb
dist intra_4985_valid , resid 109 and blastp_afP21464 and chain A and name cb, resid 115 and blastp_afP21464 and chain A and name cb
dist intra_5929_valid , resid 152 and blastp_afP21464 and chain A and name cb, resid 115 and blastp_afP21464 and chain A and name cb
dist intra_546_unknown , resid 49 and blastp_afP21464 and chain A and name cb, resid 36 and blastp_afP21464 and chain A and name cb
dist intra_1141_unknown , resid 155 and blastp_afP21464 and chain A and name cb, resid 116 and blastp_afP21464 and chain A and name cb
dist intra_1307_unknown , resid 75 and blastp_afP21464 and chain A and name cb, resid 152 and blastp_afP21464 and chain A and name cb
dist intra_1541_unknown , resid 155 and blastp_afP21464 and chain A and name cb, resid 59 and blastp_afP21464 and chain A and name cb
dist intra_1840_unknown , resid 74 and blastp_afP21464 and chain A and name cb, resid 144 and blastp_afP21464 and chain A and name cb
dist intra_1960_unknown , resid 146 and blastp_afP21464 and chain A and name cb, resid 75 and blastp_afP21464 and chain A and name cb
dist intra_2589_unknown , resid 75 and blastp_afP21464 and chain A and name cb, resid 211 and blastp_afP21464 and chain A and name cb
dist intra_3746_unknown , resid 133 and blastp_afP21464 and chain A and name cb, resid 120 and blastp_afP21464 and chain A and name cb
dist intra_3785_unknown , resid 144 and blastp_afP21464 and chain A and name cb, resid 75 and blastp_afP21464 and chain A and name cb
dist intra_4426_unknown , resid 131 and blastp_afP21464 and chain A and name cb, resid 133 and blastp_afP21464 and chain A and name cb
dist intra_5419_unknown , resid 81 and blastp_afP21464 and chain A and name cb, resid 144 and blastp_afP21464 and chain A and name cb
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
save blastp_afP21464.pse
png blastp_afP21464.png
