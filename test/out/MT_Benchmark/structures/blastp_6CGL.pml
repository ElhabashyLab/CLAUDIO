load blastp_6CGL.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_6CGL
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_6CGL
color 5, chain B
show cartoon, chain B
dist intra_1234_valid , resid 209 and blastp_6CGL and chain A and name cb, resid 228 and blastp_6CGL and chain A and name cb
dist intra_1234_4_valid , resid 209 and blastp_6CGL and chain B and name cb, resid 228 and blastp_6CGL and chain B and name cb
dist intra_1246_4_valid , resid 276 and blastp_6CGL and chain B and name cb, resid 221 and blastp_6CGL and chain B and name cb
dist intra_1626_valid , resid 228 and blastp_6CGL and chain A and name cb, resid 276 and blastp_6CGL and chain A and name cb
dist intra_1626_4_valid , resid 228 and blastp_6CGL and chain B and name cb, resid 276 and blastp_6CGL and chain B and name cb
dist intra_2395_valid , resid 336 and blastp_6CGL and chain A and name cb, resid 296 and blastp_6CGL and chain A and name cb
dist intra_2395_4_valid , resid 336 and blastp_6CGL and chain B and name cb, resid 296 and blastp_6CGL and chain B and name cb
dist intra_4135_valid , resid 209 and blastp_6CGL and chain A and name cb, resid 214 and blastp_6CGL and chain A and name cb
dist intra_4135_4_valid , resid 209 and blastp_6CGL and chain B and name cb, resid 221 and blastp_6CGL and chain B and name cb
dist intra_5682_valid , resid 276 and blastp_6CGL and chain A and name cb, resid 265 and blastp_6CGL and chain A and name cb
dist intra_5682_4_valid , resid 276 and blastp_6CGL and chain B and name cb, resid 265 and blastp_6CGL and chain B and name cb
dist intra_1246_out_range , resid 276 and blastp_6CGL and chain A and name cb, resid 214 and blastp_6CGL and chain A and name cb
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
save blastp_6CGL.pse
png blastp_6CGL.png
