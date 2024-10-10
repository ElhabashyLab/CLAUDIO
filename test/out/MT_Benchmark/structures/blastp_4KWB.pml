load blastp_4KWB.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_4KWB
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain B
show surface, chain B and blastp_4KWB
color 5, chain B
show cartoon, chain B
hide everything, show cartoon, chain C
show surface, chain C and blastp_4KWB
color 7, chain C
show cartoon, chain C
hide everything, show cartoon, chain D
show surface, chain D and blastp_4KWB
color 8, chain D
show cartoon, chain D
hide everything, show cartoon, chain E
show surface, chain E and blastp_4KWB
color 9, chain E
show cartoon, chain E
hide everything, show cartoon, chain F
show surface, chain F and blastp_4KWB
color 10, chain F
show cartoon, chain F
hide everything, show cartoon, chain G
show surface, chain G and blastp_4KWB
color 11, chain G
show cartoon, chain G
hide everything, show cartoon, chain H
show surface, chain H and blastp_4KWB
color 12, chain H
show cartoon, chain H
dist intra_5438_valid , resid 91 and blastp_4KWB and chain A and name cb, resid 108 and blastp_4KWB and chain A and name cb
dist intra_5438_10_valid , resid 91 and blastp_4KWB and chain B and name cb, resid 108 and blastp_4KWB and chain B and name cb
dist intra_5438_19_valid , resid 91 and blastp_4KWB and chain C and name cb, resid 108 and blastp_4KWB and chain C and name cb
dist intra_5438_28_valid , resid 91 and blastp_4KWB and chain D and name cb, resid 108 and blastp_4KWB and chain D and name cb
dist intra_5438_37_valid , resid 91 and blastp_4KWB and chain E and name cb, resid 108 and blastp_4KWB and chain E and name cb
dist intra_5438_46_valid , resid 91 and blastp_4KWB and chain F and name cb, resid 108 and blastp_4KWB and chain F and name cb
dist intra_5438_55_valid , resid 91 and blastp_4KWB and chain G and name cb, resid 108 and blastp_4KWB and chain G and name cb
dist intra_5438_64_valid , resid 91 and blastp_4KWB and chain H and name cb, resid 108 and blastp_4KWB and chain H and name cb
dist inter_5438_8_valid , resid 91 and blastp_4KWB and chain A and name cb, resid 108 and blastp_4KWB and chain H and name cb
dist inter_5438_9_valid , resid 91 and blastp_4KWB and chain B and name cb, resid 108 and blastp_4KWB and chain A and name cb
dist inter_5438_18_valid , resid 91 and blastp_4KWB and chain C and name cb, resid 108 and blastp_4KWB and chain B and name cb
dist inter_5438_27_valid , resid 91 and blastp_4KWB and chain D and name cb, resid 108 and blastp_4KWB and chain C and name cb
dist inter_5438_36_valid , resid 91 and blastp_4KWB and chain E and name cb, resid 108 and blastp_4KWB and chain D and name cb
dist inter_5438_45_valid , resid 91 and blastp_4KWB and chain F and name cb, resid 108 and blastp_4KWB and chain E and name cb
dist inter_5438_54_valid , resid 91 and blastp_4KWB and chain G and name cb, resid 108 and blastp_4KWB and chain F and name cb
dist inter_5438_63_valid , resid 91 and blastp_4KWB and chain H and name cb, resid 108 and blastp_4KWB and chain G and name cb
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
save blastp_4KWB.pse
png blastp_4KWB.png
