load blastp_6SDK.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_6SDK
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_6SDK
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain C
show surface, chain C and blastp_6SDK
color 7, chain C
show cartoon, chain C
hide everything, show cartoon, chain D
show surface, chain D and blastp_6SDK
color 8, chain D
show cartoon, chain D
dist intra_233_valid , resid 85 and blastp_6SDK and chain A and name cb, resid 40 and blastp_6SDK and chain A and name cb
dist intra_233_6_valid , resid 85 and blastp_6SDK and chain B and name cb, resid 40 and blastp_6SDK and chain B and name cb
dist intra_233_11_valid , resid 85 and blastp_6SDK and chain C and name cb, resid 40 and blastp_6SDK and chain C and name cb
dist intra_233_16_valid , resid 85 and blastp_6SDK and chain D and name cb, resid 40 and blastp_6SDK and chain D and name cb
dist intra_3183_valid , resid 186 and blastp_6SDK and chain A and name cb, resid 190 and blastp_6SDK and chain A and name cb
dist intra_3183_6_valid , resid 186 and blastp_6SDK and chain B and name cb, resid 190 and blastp_6SDK and chain B and name cb
dist intra_3183_11_valid , resid 186 and blastp_6SDK and chain C and name cb, resid 190 and blastp_6SDK and chain C and name cb
dist intra_3183_16_valid , resid 186 and blastp_6SDK and chain D and name cb, resid 190 and blastp_6SDK and chain D and name cb
dist intra_4691_unknown , resid 225 and blastp_6SDK and chain A and name cb, resid 190 and blastp_6SDK and chain A and name cb
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
save blastp_6SDK.pse
png blastp_6SDK.png
