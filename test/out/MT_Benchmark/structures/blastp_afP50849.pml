load blastp_afP50849.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP50849
color 3, chain A
show cartoon, chain A
dist intra_157_valid , resid 682 and blastp_afP50849 and chain A and name cb, resid 575 and blastp_afP50849 and chain A and name cb
dist intra_681_valid , resid 274 and blastp_afP50849 and chain A and name cb, resid 263 and blastp_afP50849 and chain A and name cb
dist intra_729_valid , resid 575 and blastp_afP50849 and chain A and name cb, resid 629 and blastp_afP50849 and chain A and name cb
dist intra_799_valid , resid 682 and blastp_afP50849 and chain A and name cb, resid 662 and blastp_afP50849 and chain A and name cb
dist intra_868_valid , resid 274 and blastp_afP50849 and chain A and name cb, resid 303 and blastp_afP50849 and chain A and name cb
dist intra_913_valid , resid 274 and blastp_afP50849 and chain A and name cb, resid 295 and blastp_afP50849 and chain A and name cb
dist intra_932_valid , resid 72 and blastp_afP50849 and chain A and name cb, resid 87 and blastp_afP50849 and chain A and name cb
dist intra_943_valid , resid 295 and blastp_afP50849 and chain A and name cb, resid 49 and blastp_afP50849 and chain A and name cb
dist intra_1224_valid , resid 247 and blastp_afP50849 and chain A and name cb, resid 300 and blastp_afP50849 and chain A and name cb
dist intra_1609_valid , resid 682 and blastp_afP50849 and chain A and name cb, resid 629 and blastp_afP50849 and chain A and name cb
dist intra_1890_valid , resid 676 and blastp_afP50849 and chain A and name cb, resid 700 and blastp_afP50849 and chain A and name cb
dist intra_2704_valid , resid 579 and blastp_afP50849 and chain A and name cb, resid 682 and blastp_afP50849 and chain A and name cb
dist intra_2762_valid , resid 303 and blastp_afP50849 and chain A and name cb, resid 292 and blastp_afP50849 and chain A and name cb
dist intra_2923_valid , resid 303 and blastp_afP50849 and chain A and name cb, resid 295 and blastp_afP50849 and chain A and name cb
dist intra_3222_valid , resid 691 and blastp_afP50849 and chain A and name cb, resid 676 and blastp_afP50849 and chain A and name cb
dist intra_3390_valid , resid 52 and blastp_afP50849 and chain A and name cb, resid 292 and blastp_afP50849 and chain A and name cb
dist intra_3421_valid , resid 611 and blastp_afP50849 and chain A and name cb, resid 629 and blastp_afP50849 and chain A and name cb
dist intra_3634_valid , resid 511 and blastp_afP50849 and chain A and name cb, resid 303 and blastp_afP50849 and chain A and name cb
dist intra_3665_valid , resid 292 and blastp_afP50849 and chain A and name cb, resid 234 and blastp_afP50849 and chain A and name cb
dist intra_3724_valid , resid 280 and blastp_afP50849 and chain A and name cb, resid 245 and blastp_afP50849 and chain A and name cb
dist intra_4439_valid , resid 303 and blastp_afP50849 and chain A and name cb, resid 263 and blastp_afP50849 and chain A and name cb
dist intra_4722_valid , resid 611 and blastp_afP50849 and chain A and name cb, resid 608 and blastp_afP50849 and chain A and name cb
dist intra_5070_valid , resid 676 and blastp_afP50849 and chain A and name cb, resid 698 and blastp_afP50849 and chain A and name cb
dist intra_460_out_range , resid 575 and blastp_afP50849 and chain A and name cb, resid 420 and blastp_afP50849 and chain A and name cb
dist intra_2733_out_range , resid 263 and blastp_afP50849 and chain A and name cb, resid 49 and blastp_afP50849 and chain A and name cb
dist intra_1925_overlaps , resid 575 and blastp_afP50849 and chain A and name cb, resid 565 and blastp_afP50849 and chain A and name cb
dist intra_2649_overlaps , resid 79 and blastp_afP50849 and chain A and name cb, resid 72 and blastp_afP50849 and chain A and name cb
dist intra_334_unknown , resid 263 and blastp_afP50849 and chain A and name cb, resid 26 and blastp_afP50849 and chain A and name cb
dist intra_1593_unknown , resid 677 and blastp_afP50849 and chain A and name cb, resid 575 and blastp_afP50849 and chain A and name cb
dist intra_2142_unknown , resid 49 and blastp_afP50849 and chain A and name cb, resid 293 and blastp_afP50849 and chain A and name cb
dist intra_2286_unknown , resid 274 and blastp_afP50849 and chain A and name cb, resid 293 and blastp_afP50849 and chain A and name cb
dist intra_3331_unknown , resid 303 and blastp_afP50849 and chain A and name cb, resid 267 and blastp_afP50849 and chain A and name cb
dist intra_3372_unknown , resid 247 and blastp_afP50849 and chain A and name cb, resid 296 and blastp_afP50849 and chain A and name cb
dist intra_3911_unknown , resid 677 and blastp_afP50849 and chain A and name cb, resid 682 and blastp_afP50849 and chain A and name cb
dist intra_4014_unknown , resid 293 and blastp_afP50849 and chain A and name cb, resid 267 and blastp_afP50849 and chain A and name cb
dist intra_4771_unknown , resid 293 and blastp_afP50849 and chain A and name cb, resid 52 and blastp_afP50849 and chain A and name cb
dist intra_5977_unknown , resid 296 and blastp_afP50849 and chain A and name cb, resid 292 and blastp_afP50849 and chain A and name cb
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
save blastp_afP50849.pse
png blastp_afP50849.png
