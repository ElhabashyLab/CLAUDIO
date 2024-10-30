load blastp_afP27876.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP27876
color 3, chain A
show cartoon, chain A
dist intra_200_valid , resid 215 and blastp_afP27876 and chain A and name cb, resid 176 and blastp_afP27876 and chain A and name cb
dist intra_261_valid , resid 148 and blastp_afP27876 and chain A and name cb, resid 192 and blastp_afP27876 and chain A and name cb
dist intra_287_valid , resid 215 and blastp_afP27876 and chain A and name cb, resid 149 and blastp_afP27876 and chain A and name cb
dist intra_328_valid , resid 3 and blastp_afP27876 and chain A and name cb, resid 205 and blastp_afP27876 and chain A and name cb
dist intra_1473_valid , resid 3 and blastp_afP27876 and chain A and name cb, resid 215 and blastp_afP27876 and chain A and name cb
dist intra_2125_valid , resid 111 and blastp_afP27876 and chain A and name cb, resid 118 and blastp_afP27876 and chain A and name cb
dist intra_3134_valid , resid 27 and blastp_afP27876 and chain A and name cb, resid 55 and blastp_afP27876 and chain A and name cb
dist intra_4823_valid , resid 192 and blastp_afP27876 and chain A and name cb, resid 181 and blastp_afP27876 and chain A and name cb
dist intra_3269_overlaps , resid 193 and blastp_afP27876 and chain A and name cb, resid 3 and blastp_afP27876 and chain A and name cb
dist intra_4136_overlaps , resid 35 and blastp_afP27876 and chain A and name cb, resid 3 and blastp_afP27876 and chain A and name cb
dist intra_104_unknown , resid 36 and blastp_afP27876 and chain A and name cb, resid 55 and blastp_afP27876 and chain A and name cb
dist intra_364_unknown , resid 28 and blastp_afP27876 and chain A and name cb, resid 55 and blastp_afP27876 and chain A and name cb
dist intra_656_unknown , resid 27 and blastp_afP27876 and chain A and name cb, resid 36 and blastp_afP27876 and chain A and name cb
dist intra_1551_unknown , resid 100 and blastp_afP27876 and chain A and name cb, resid 118 and blastp_afP27876 and chain A and name cb
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
save blastp_afP27876.pse
png blastp_afP27876.png
