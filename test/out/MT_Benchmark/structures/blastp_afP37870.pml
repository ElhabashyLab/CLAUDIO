load blastp_afP37870.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP37870
color 3, chain A
show cartoon, chain A
dist intra_1288_valid , resid 1067 and blastp_afP37870 and chain A and name cb, resid 849 and blastp_afP37870 and chain A and name cb
dist intra_168_unknown , resid 709 and blastp_afP37870 and chain A and name cb, resid 669 and blastp_afP37870 and chain A and name cb
dist intra_817_unknown , resid 868 and blastp_afP37870 and chain A and name cb, resid 849 and blastp_afP37870 and chain A and name cb
dist intra_933_unknown , resid 709 and blastp_afP37870 and chain A and name cb, resid 685 and blastp_afP37870 and chain A and name cb
dist intra_1445_unknown , resid 1067 and blastp_afP37870 and chain A and name cb, resid 1040 and blastp_afP37870 and chain A and name cb
dist intra_2491_unknown , resid 868 and blastp_afP37870 and chain A and name cb, resid 803 and blastp_afP37870 and chain A and name cb
dist intra_4045_unknown , resid 849 and blastp_afP37870 and chain A and name cb, resid 1192 and blastp_afP37870 and chain A and name cb
dist intra_4834_unknown , resid 919 and blastp_afP37870 and chain A and name cb, resid 1047 and blastp_afP37870 and chain A and name cb
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
save blastp_afP37870.pse
png blastp_afP37870.png
