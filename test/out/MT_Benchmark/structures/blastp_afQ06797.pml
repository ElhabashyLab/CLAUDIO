load blastp_afQ06797.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afQ06797
color 3, chain A
show cartoon, chain A
dist intra_122_valid , resid 141 and blastp_afQ06797 and chain A and name cb, resid 167 and blastp_afQ06797 and chain A and name cb
dist intra_132_valid , resid 54 and blastp_afQ06797 and chain A and name cb, resid 205 and blastp_afQ06797 and chain A and name cb
dist intra_208_valid , resid 54 and blastp_afQ06797 and chain A and name cb, resid 167 and blastp_afQ06797 and chain A and name cb
dist intra_281_valid , resid 134 and blastp_afQ06797 and chain A and name cb, resid 167 and blastp_afQ06797 and chain A and name cb
dist intra_765_valid , resid 32 and blastp_afQ06797 and chain A and name cb, resid 19 and blastp_afQ06797 and chain A and name cb
dist intra_896_valid , resid 151 and blastp_afQ06797 and chain A and name cb, resid 160 and blastp_afQ06797 and chain A and name cb
dist intra_1055_valid , resid 32 and blastp_afQ06797 and chain A and name cb, resid 13 and blastp_afQ06797 and chain A and name cb
dist intra_1145_valid , resid 54 and blastp_afQ06797 and chain A and name cb, resid 210 and blastp_afQ06797 and chain A and name cb
dist intra_1599_valid , resid 71 and blastp_afQ06797 and chain A and name cb, resid 184 and blastp_afQ06797 and chain A and name cb
dist intra_2275_valid , resid 32 and blastp_afQ06797 and chain A and name cb, resid 7 and blastp_afQ06797 and chain A and name cb
dist intra_2363_valid , resid 160 and blastp_afQ06797 and chain A and name cb, resid 141 and blastp_afQ06797 and chain A and name cb
dist intra_2570_valid , resid 54 and blastp_afQ06797 and chain A and name cb, resid 141 and blastp_afQ06797 and chain A and name cb
dist intra_2652_valid , resid 200 and blastp_afQ06797 and chain A and name cb, resid 141 and blastp_afQ06797 and chain A and name cb
dist intra_3217_valid , resid 160 and blastp_afQ06797 and chain A and name cb, resid 71 and blastp_afQ06797 and chain A and name cb
dist intra_3302_valid , resid 160 and blastp_afQ06797 and chain A and name cb, resid 198 and blastp_afQ06797 and chain A and name cb
dist intra_3538_valid , resid 71 and blastp_afQ06797 and chain A and name cb, resid 134 and blastp_afQ06797 and chain A and name cb
dist intra_3950_valid , resid 141 and blastp_afQ06797 and chain A and name cb, resid 80 and blastp_afQ06797 and chain A and name cb
dist intra_5198_valid , resid 141 and blastp_afQ06797 and chain A and name cb, resid 177 and blastp_afQ06797 and chain A and name cb
dist intra_5584_valid , resid 85 and blastp_afQ06797 and chain A and name cb, resid 80 and blastp_afQ06797 and chain A and name cb
dist intra_5864_valid , resid 205 and blastp_afQ06797 and chain A and name cb, resid 141 and blastp_afQ06797 and chain A and name cb
dist intra_6130_valid , resid 205 and blastp_afQ06797 and chain A and name cb, resid 167 and blastp_afQ06797 and chain A and name cb
dist intra_3679_out_range , resid 80 and blastp_afQ06797 and chain A and name cb, resid 167 and blastp_afQ06797 and chain A and name cb
dist intra_1170_unknown , resid 205 and blastp_afQ06797 and chain A and name cb, resid 232 and blastp_afQ06797 and chain A and name cb
dist intra_1412_unknown , resid 198 and blastp_afQ06797 and chain A and name cb, resid 232 and blastp_afQ06797 and chain A and name cb
dist intra_2346_unknown , resid 200 and blastp_afQ06797 and chain A and name cb, resid 232 and blastp_afQ06797 and chain A and name cb
dist intra_3073_unknown , resid 32 and blastp_afQ06797 and chain A and name cb, resid 8 and blastp_afQ06797 and chain A and name cb
dist intra_3340_unknown , resid 142 and blastp_afQ06797 and chain A and name cb, resid 160 and blastp_afQ06797 and chain A and name cb
dist intra_3963_unknown , resid 160 and blastp_afQ06797 and chain A and name cb, resid 185 and blastp_afQ06797 and chain A and name cb
dist intra_4191_unknown , resid 54 and blastp_afQ06797 and chain A and name cb, resid 199 and blastp_afQ06797 and chain A and name cb
dist intra_5051_unknown , resid 232 and blastp_afQ06797 and chain A and name cb, resid 185 and blastp_afQ06797 and chain A and name cb
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
save blastp_afQ06797.pse
png blastp_afQ06797.png
