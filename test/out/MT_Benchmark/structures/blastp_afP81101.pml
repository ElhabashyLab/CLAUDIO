load blastp_afP81101.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP81101
color 3, chain A
show cartoon, chain A
dist intra_409_valid , resid 170 and blastp_afP81101 and chain A and name cb, resid 10 and blastp_afP81101 and chain A and name cb
dist intra_507_valid , resid 144 and blastp_afP81101 and chain A and name cb, resid 140 and blastp_afP81101 and chain A and name cb
dist intra_975_valid , resid 125 and blastp_afP81101 and chain A and name cb, resid 176 and blastp_afP81101 and chain A and name cb
dist intra_1160_valid , resid 162 and blastp_afP81101 and chain A and name cb, resid 10 and blastp_afP81101 and chain A and name cb
dist intra_1417_valid , resid 15 and blastp_afP81101 and chain A and name cb, resid 10 and blastp_afP81101 and chain A and name cb
dist intra_2122_valid , resid 162 and blastp_afP81101 and chain A and name cb, resid 3 and blastp_afP81101 and chain A and name cb
dist intra_2585_valid , resid 115 and blastp_afP81101 and chain A and name cb, resid 119 and blastp_afP81101 and chain A and name cb
dist intra_2917_valid , resid 176 and blastp_afP81101 and chain A and name cb, resid 119 and blastp_afP81101 and chain A and name cb
dist intra_3051_valid , resid 176 and blastp_afP81101 and chain A and name cb, resid 180 and blastp_afP81101 and chain A and name cb
dist intra_3074_valid , resid 15 and blastp_afP81101 and chain A and name cb, resid 39 and blastp_afP81101 and chain A and name cb
dist intra_4199_valid , resid 15 and blastp_afP81101 and chain A and name cb, resid 3 and blastp_afP81101 and chain A and name cb
dist intra_879_overlaps , resid 163 and blastp_afP81101 and chain A and name cb, resid 10 and blastp_afP81101 and chain A and name cb
dist intra_4359_overlaps , resid 13 and blastp_afP81101 and chain A and name cb, resid 3 and blastp_afP81101 and chain A and name cb
dist intra_6155_overlaps , resid 4 and blastp_afP81101 and chain A and name cb, resid 163 and blastp_afP81101 and chain A and name cb
dist intra_1581_unknown , resid 142 and blastp_afP81101 and chain A and name cb, resid 140 and blastp_afP81101 and chain A and name cb
dist intra_2535_unknown , resid 162 and blastp_afP81101 and chain A and name cb, resid 2 and blastp_afP81101 and chain A and name cb
dist intra_3275_unknown , resid 4 and blastp_afP81101 and chain A and name cb, resid 170 and blastp_afP81101 and chain A and name cb
dist intra_4585_unknown , resid 119 and blastp_afP81101 and chain A and name cb, resid 112 and blastp_afP81101 and chain A and name cb
dist intra_6066_unknown , resid 176 and blastp_afP81101 and chain A and name cb, resid 120 and blastp_afP81101 and chain A and name cb
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
save blastp_afP81101.pse
png blastp_afP81101.png
