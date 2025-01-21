load blastp_7ABR.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_7ABR
color 3, chain A
show cartoon, chain A
hide everything, show cartoon, chain D
show surface, chain D and blastp_7ABR
color 5, chain D
show cartoon, chain D
hide everything, show cartoon, chain E
show surface, chain E and blastp_7ABR
color 7, chain E
show cartoon, chain E
hide everything, show cartoon, chain B
show surface, chain B and blastp_7ABR
color 8, chain B
show cartoon, chain B
hide everything, show cartoon, chain C
show surface, chain C and blastp_7ABR
color 9, chain C
show cartoon, chain C
hide everything, show cartoon, chain F
show surface, chain F and blastp_7ABR
color 10, chain F
show cartoon, chain F
dist intra_570_22_valid , resid 609 and blastp_7ABR and chain D and name cb, resid 605 and blastp_7ABR and chain D and name cb
dist intra_570_29_valid , resid 609 and blastp_7ABR and chain E and name cb, resid 605 and blastp_7ABR and chain E and name cb
dist intra_2899_22_valid , resid 522 and blastp_7ABR and chain D and name cb, resid 683 and blastp_7ABR and chain D and name cb
dist intra_2899_29_valid , resid 522 and blastp_7ABR and chain E and name cb, resid 683 and blastp_7ABR and chain E and name cb
dist intra_4352_22_valid , resid 685 and blastp_7ABR and chain D and name cb, resid 522 and blastp_7ABR and chain D and name cb
dist intra_4352_29_valid , resid 685 and blastp_7ABR and chain E and name cb, resid 522 and blastp_7ABR and chain E and name cb
dist intra_4560_out_range , resid 401 and blastp_7ABR and chain A and name cb, resid 187 and blastp_7ABR and chain A and name cb
dist intra_4723_overlaps , resid 322 and blastp_7ABR and chain A and name cb, resid 326 and blastp_7ABR and chain A and name cb
dist intra_2089_unknown , resid 717 and blastp_7ABR and chain A and name cb, resid 326 and blastp_7ABR and chain A and name cb
dist inter_570_23_valid , resid 609 and blastp_7ABR and chain D and name cb, resid 605 and blastp_7ABR and chain E and name cb
dist inter_714_9_valid , resid 376 and blastp_7ABR and chain B and name cb, resid 551 and blastp_7ABR and chain C and name cb
dist inter_714_16_valid , resid 376 and blastp_7ABR and chain C and name cb, resid 498 and blastp_7ABR and chain D and name cb
dist inter_2081_23_valid , resid 522 and blastp_7ABR and chain D and name cb, resid 771 and blastp_7ABR and chain E and name cb
dist inter_2089_19_valid , resid 643 and blastp_7ABR and chain D and name cb, resid 326 and blastp_7ABR and chain A and name cb
dist inter_2089_20_valid , resid 643 and blastp_7ABR and chain D and name cb, resid 326 and blastp_7ABR and chain B and name cb
dist inter_2089_21_valid , resid 643 and blastp_7ABR and chain D and name cb, resid 326 and blastp_7ABR and chain C and name cb
dist inter_2089_26_valid , resid 643 and blastp_7ABR and chain E and name cb, resid 326 and blastp_7ABR and chain B and name cb
dist inter_2089_27_valid , resid 643 and blastp_7ABR and chain E and name cb, resid 326 and blastp_7ABR and chain C and name cb
dist inter_2089_30_valid , resid 643 and blastp_7ABR and chain E and name cb, resid 326 and blastp_7ABR and chain F and name cb
dist inter_3479_4_valid , resid 322 and blastp_7ABR and chain A and name cb, resid 580 and blastp_7ABR and chain D and name cb
dist inter_3479_5_valid , resid 322 and blastp_7ABR and chain A and name cb, resid 580 and blastp_7ABR and chain E and name cb
dist inter_3479_10_valid , resid 322 and blastp_7ABR and chain B and name cb, resid 580 and blastp_7ABR and chain D and name cb
dist inter_3479_11_valid , resid 322 and blastp_7ABR and chain B and name cb, resid 580 and blastp_7ABR and chain E and name cb
dist inter_3479_17_valid , resid 322 and blastp_7ABR and chain C and name cb, resid 580 and blastp_7ABR and chain E and name cb
dist inter_3479_35_valid , resid 322 and blastp_7ABR and chain F and name cb, resid 580 and blastp_7ABR and chain E and name cb
dist inter_4560_6_valid , resid 401 and blastp_7ABR and chain A and name cb, resid 187 and blastp_7ABR and chain F and name cb
dist inter_4560_7_valid , resid 401 and blastp_7ABR and chain B and name cb, resid 187 and blastp_7ABR and chain A and name cb
dist inter_4560_14_valid , resid 401 and blastp_7ABR and chain C and name cb, resid 187 and blastp_7ABR and chain B and name cb
dist inter_4723_2_valid , resid 322 and blastp_7ABR and chain A and name cb, resid 326 and blastp_7ABR and chain B and name cb
dist inter_4723_3_valid , resid 322 and blastp_7ABR and chain A and name cb, resid 326 and blastp_7ABR and chain C and name cb
dist inter_4723_6_valid , resid 322 and blastp_7ABR and chain A and name cb, resid 326 and blastp_7ABR and chain F and name cb
dist inter_4723_7_valid , resid 322 and blastp_7ABR and chain B and name cb, resid 326 and blastp_7ABR and chain A and name cb
dist inter_4723_9_valid , resid 322 and blastp_7ABR and chain B and name cb, resid 326 and blastp_7ABR and chain C and name cb
dist inter_4723_12_valid , resid 322 and blastp_7ABR and chain B and name cb, resid 326 and blastp_7ABR and chain F and name cb
dist inter_4723_13_valid , resid 322 and blastp_7ABR and chain C and name cb, resid 326 and blastp_7ABR and chain A and name cb
dist inter_4723_14_valid , resid 322 and blastp_7ABR and chain C and name cb, resid 326 and blastp_7ABR and chain B and name cb
dist inter_4723_31_valid , resid 322 and blastp_7ABR and chain F and name cb, resid 326 and blastp_7ABR and chain A and name cb
dist inter_4723_32_valid , resid 322 and blastp_7ABR and chain F and name cb, resid 326 and blastp_7ABR and chain B and name cb
dist inter_4723_33_valid , resid 322 and blastp_7ABR and chain F and name cb, resid 326 and blastp_7ABR and chain C and name cb
dist inter_5357_23_valid , resid 685 and blastp_7ABR and chain D and name cb, resid 771 and blastp_7ABR and chain E and name cb
dist inter_5571_23_valid , resid 694 and blastp_7ABR and chain D and name cb, resid 771 and blastp_7ABR and chain E and name cb
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
save blastp_7ABR.pse
png blastp_7ABR.png
