load blastp_afP37571.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP37571
color 3, chain A
show cartoon, chain A
dist intra_454_valid , resid 438 and blastp_afP37571 and chain A and name cb, resid 419 and blastp_afP37571 and chain A and name cb
dist intra_570_3_valid , resid 609 and blastp_afP37571 and chain A and name cb, resid 605 and blastp_afP37571 and chain A and name cb
dist intra_714_valid , resid 376 and blastp_afP37571 and chain A and name cb, resid 498 and blastp_afP37571 and chain A and name cb
dist intra_1367_8_valid , resid 59 and blastp_afP37571 and chain A and name cb, resid 133 and blastp_afP37571 and chain A and name cb
dist intra_1819_valid , resid 457 and blastp_afP37571 and chain A and name cb, resid 414 and blastp_afP37571 and chain A and name cb
dist intra_2089_12_valid , resid 643 and blastp_afP37571 and chain A and name cb, resid 326 and blastp_afP37571 and chain A and name cb
dist intra_2899_valid , resid 522 and blastp_afP37571 and chain A and name cb, resid 683 and blastp_afP37571 and chain A and name cb
dist intra_3197_2_valid , resid 12 and blastp_afP37571 and chain A and name cb, resid 461 and blastp_afP37571 and chain A and name cb
dist intra_3479_valid , resid 322 and blastp_afP37571 and chain A and name cb, resid 580 and blastp_afP37571 and chain A and name cb
dist intra_3757_10_valid , resid 457 and blastp_afP37571 and chain A and name cb, resid 461 and blastp_afP37571 and chain A and name cb
dist intra_4076_valid , resid 12 and blastp_afP37571 and chain A and name cb, resid 457 and blastp_afP37571 and chain A and name cb
dist intra_4352_valid , resid 685 and blastp_afP37571 and chain A and name cb, resid 522 and blastp_afP37571 and chain A and name cb
dist intra_1465_out_range , resid 133 and blastp_afP37571 and chain A and name cb, resid 175 and blastp_afP37571 and chain A and name cb
dist intra_2081_out_range , resid 522 and blastp_afP37571 and chain A and name cb, resid 771 and blastp_afP37571 and chain A and name cb
dist intra_5571_out_range , resid 694 and blastp_afP37571 and chain A and name cb, resid 771 and blastp_afP37571 and chain A and name cb
dist intra_1130_unknown , resid 669 and blastp_afP37571 and chain A and name cb, resid 666 and blastp_afP37571 and chain A and name cb
dist intra_1498_unknown , resid 609 and blastp_afP37571 and chain A and name cb, resid 586 and blastp_afP37571 and chain A and name cb
dist intra_3532_unknown , resid 808 and blastp_afP37571 and chain A and name cb, resid 788 and blastp_afP37571 and chain A and name cb
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
save blastp_afP37571.pse
png blastp_afP37571.png
