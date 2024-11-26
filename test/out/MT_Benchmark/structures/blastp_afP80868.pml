load blastp_afP80868.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP80868
color 3, chain A
show cartoon, chain A
dist intra_22_valid , resid 469 and blastp_afP80868 and chain A and name cb, resid 421 and blastp_afP80868 and chain A and name cb
dist intra_214_valid , resid 490 and blastp_afP80868 and chain A and name cb, resid 564 and blastp_afP80868 and chain A and name cb
dist intra_289_valid , resid 594 and blastp_afP80868 and chain A and name cb, resid 490 and blastp_afP80868 and chain A and name cb
dist intra_464_valid , resid 422 and blastp_afP80868 and chain A and name cb, resid 469 and blastp_afP80868 and chain A and name cb
dist intra_591_valid , resid 589 and blastp_afP80868 and chain A and name cb, resid 687 and blastp_afP80868 and chain A and name cb
dist intra_2871_valid , resid 323 and blastp_afP80868 and chain A and name cb, resid 421 and blastp_afP80868 and chain A and name cb
dist intra_4219_valid , resid 679 and blastp_afP80868 and chain A and name cb, resid 688 and blastp_afP80868 and chain A and name cb
dist intra_3078_out_range , resid 341 and blastp_afP80868 and chain A and name cb, resid 494 and blastp_afP80868 and chain A and name cb
dist intra_3622_out_range , resid 341 and blastp_afP80868 and chain A and name cb, resid 421 and blastp_afP80868 and chain A and name cb
dist intra_1030_unknown , resid 428 and blastp_afP80868 and chain A and name cb, resid 315 and blastp_afP80868 and chain A and name cb
dist intra_1211_unknown , resid 422 and blastp_afP80868 and chain A and name cb, resid 315 and blastp_afP80868 and chain A and name cb
dist intra_2663_unknown , resid 428 and blastp_afP80868 and chain A and name cb, resid 301 and blastp_afP80868 and chain A and name cb
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
save blastp_afP80868.pse
png blastp_afP80868.png
