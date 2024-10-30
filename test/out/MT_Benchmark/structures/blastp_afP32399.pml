load blastp_afP32399.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP32399
color 3, chain A
show cartoon, chain A
dist intra_793_valid , resid 212 and blastp_afP32399 and chain A and name cb, resid 205 and blastp_afP32399 and chain A and name cb
dist intra_928_valid , resid 432 and blastp_afP32399 and chain A and name cb, resid 298 and blastp_afP32399 and chain A and name cb
dist intra_1045_valid , resid 460 and blastp_afP32399 and chain A and name cb, resid 270 and blastp_afP32399 and chain A and name cb
dist intra_1137_valid , resid 256 and blastp_afP32399 and chain A and name cb, resid 460 and blastp_afP32399 and chain A and name cb
dist intra_1257_valid , resid 256 and blastp_afP32399 and chain A and name cb, resid 467 and blastp_afP32399 and chain A and name cb
dist intra_1469_valid , resid 189 and blastp_afP32399 and chain A and name cb, resid 205 and blastp_afP32399 and chain A and name cb
dist intra_1952_valid , resid 188 and blastp_afP32399 and chain A and name cb, resid 195 and blastp_afP32399 and chain A and name cb
dist intra_2046_valid , resid 210 and blastp_afP32399 and chain A and name cb, resid 205 and blastp_afP32399 and chain A and name cb
dist intra_3053_valid , resid 481 and blastp_afP32399 and chain A and name cb, resid 245 and blastp_afP32399 and chain A and name cb
dist intra_3094_valid , resid 210 and blastp_afP32399 and chain A and name cb, resid 516 and blastp_afP32399 and chain A and name cb
dist intra_3948_valid , resid 432 and blastp_afP32399 and chain A and name cb, resid 283 and blastp_afP32399 and chain A and name cb
dist intra_4467_valid , resid 508 and blastp_afP32399 and chain A and name cb, resid 210 and blastp_afP32399 and chain A and name cb
dist intra_5778_valid , resid 212 and blastp_afP32399 and chain A and name cb, resid 508 and blastp_afP32399 and chain A and name cb
dist intra_5830_valid , resid 189 and blastp_afP32399 and chain A and name cb, resid 541 and blastp_afP32399 and chain A and name cb
dist intra_5835_valid , resid 270 and blastp_afP32399 and chain A and name cb, resid 453 and blastp_afP32399 and chain A and name cb
dist intra_362_out_range , resid 178 and blastp_afP32399 and chain A and name cb, resid 205 and blastp_afP32399 and chain A and name cb
dist intra_371_out_range , resid 123 and blastp_afP32399 and chain A and name cb, resid 189 and blastp_afP32399 and chain A and name cb
dist intra_940_out_range , resid 123 and blastp_afP32399 and chain A and name cb, resid 188 and blastp_afP32399 and chain A and name cb
dist intra_5957_out_range , resid 123 and blastp_afP32399 and chain A and name cb, resid 530 and blastp_afP32399 and chain A and name cb
dist intra_1077_unknown , resid 256 and blastp_afP32399 and chain A and name cb, resid 454 and blastp_afP32399 and chain A and name cb
dist intra_1851_unknown , resid 298 and blastp_afP32399 and chain A and name cb, resid 425 and blastp_afP32399 and chain A and name cb
dist intra_2134_unknown , resid 311 and blastp_afP32399 and chain A and name cb, resid 424 and blastp_afP32399 and chain A and name cb
dist intra_2685_unknown , resid 123 and blastp_afP32399 and chain A and name cb, resid 508 and blastp_afP32399 and chain A and name cb
dist intra_3730_unknown , resid 212 and blastp_afP32399 and chain A and name cb, resid 199 and blastp_afP32399 and chain A and name cb
dist intra_3984_unknown , resid 541 and blastp_afP32399 and chain A and name cb, resid 509 and blastp_afP32399 and chain A and name cb
dist intra_4185_unknown , resid 350 and blastp_afP32399 and chain A and name cb, resid 357 and blastp_afP32399 and chain A and name cb
dist intra_4433_unknown , resid 502 and blastp_afP32399 and chain A and name cb, resid 154 and blastp_afP32399 and chain A and name cb
dist intra_4768_unknown , resid 123 and blastp_afP32399 and chain A and name cb, resid 210 and blastp_afP32399 and chain A and name cb
dist intra_5560_unknown , resid 508 and blastp_afP32399 and chain A and name cb, resid 159 and blastp_afP32399 and chain A and name cb
dist intra_5565_unknown , resid 340 and blastp_afP32399 and chain A and name cb, resid 336 and blastp_afP32399 and chain A and name cb
dist intra_5820_unknown , resid 212 and blastp_afP32399 and chain A and name cb, resid 159 and blastp_afP32399 and chain A and name cb
dist intra_5976_unknown , resid 212 and blastp_afP32399 and chain A and name cb, resid 154 and blastp_afP32399 and chain A and name cb
dist intra_5982_unknown , resid 516 and blastp_afP32399 and chain A and name cb, resid 154 and blastp_afP32399 and chain A and name cb
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
save blastp_afP32399.pse
png blastp_afP32399.png
