load blastp_afP37871.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP37871
color 3, chain A
show cartoon, chain A
dist intra_356_unknown , resid 377 and blastp_afP37871 and chain A and name cb, resid 393 and blastp_afP37871 and chain A and name cb
dist intra_691_unknown , resid 888 and blastp_afP37871 and chain A and name cb, resid 1179 and blastp_afP37871 and chain A and name cb
dist intra_802_unknown , resid 373 and blastp_afP37871 and chain A and name cb, resid 406 and blastp_afP37871 and chain A and name cb
dist intra_2225_unknown , resid 148 and blastp_afP37871 and chain A and name cb, resid 161 and blastp_afP37871 and chain A and name cb
dist intra_3061_unknown , resid 1011 and blastp_afP37871 and chain A and name cb, resid 1037 and blastp_afP37871 and chain A and name cb
dist intra_3190_unknown , resid 30 and blastp_afP37871 and chain A and name cb, resid 38 and blastp_afP37871 and chain A and name cb
dist intra_4245_unknown , resid 373 and blastp_afP37871 and chain A and name cb, resid 393 and blastp_afP37871 and chain A and name cb
dist intra_4253_unknown , resid 888 and blastp_afP37871 and chain A and name cb, resid 1170 and blastp_afP37871 and chain A and name cb
dist intra_4708_unknown , resid 616 and blastp_afP37871 and chain A and name cb, resid 565 and blastp_afP37871 and chain A and name cb
dist intra_5088_unknown , resid 1170 and blastp_afP37871 and chain A and name cb, resid 1182 and blastp_afP37871 and chain A and name cb
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
save blastp_afP37871.pse
png blastp_afP37871.png
