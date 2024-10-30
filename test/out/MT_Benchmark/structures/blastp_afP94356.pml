load blastp_afP94356.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP94356
color 3, chain A
show cartoon, chain A
dist intra_156_valid , resid 53 and blastp_afP94356 and chain A and name cb, resid 97 and blastp_afP94356 and chain A and name cb
dist intra_321_valid , resid 98 and blastp_afP94356 and chain A and name cb, resid 56 and blastp_afP94356 and chain A and name cb
dist intra_382_valid , resid 56 and blastp_afP94356 and chain A and name cb, resid 97 and blastp_afP94356 and chain A and name cb
dist intra_1363_valid , resid 148 and blastp_afP94356 and chain A and name cb, resid 53 and blastp_afP94356 and chain A and name cb
dist intra_1642_valid , resid 153 and blastp_afP94356 and chain A and name cb, resid 138 and blastp_afP94356 and chain A and name cb
dist intra_1676_valid , resid 44 and blastp_afP94356 and chain A and name cb, resid 178 and blastp_afP94356 and chain A and name cb
dist intra_2269_valid , resid 148 and blastp_afP94356 and chain A and name cb, resid 63 and blastp_afP94356 and chain A and name cb
dist intra_2313_valid , resid 168 and blastp_afP94356 and chain A and name cb, resid 44 and blastp_afP94356 and chain A and name cb
dist intra_2724_valid , resid 44 and blastp_afP94356 and chain A and name cb, resid 170 and blastp_afP94356 and chain A and name cb
dist intra_3146_valid , resid 53 and blastp_afP94356 and chain A and name cb, resid 98 and blastp_afP94356 and chain A and name cb
dist intra_4516_valid , resid 168 and blastp_afP94356 and chain A and name cb, resid 178 and blastp_afP94356 and chain A and name cb
dist intra_5773_valid , resid 56 and blastp_afP94356 and chain A and name cb, resid 44 and blastp_afP94356 and chain A and name cb
dist intra_6037_valid , resid 133 and blastp_afP94356 and chain A and name cb, resid 63 and blastp_afP94356 and chain A and name cb
dist intra_229_out_range , resid 78 and blastp_afP94356 and chain A and name cb, resid 148 and blastp_afP94356 and chain A and name cb
dist intra_2004_out_range , resid 93 and blastp_afP94356 and chain A and name cb, resid 148 and blastp_afP94356 and chain A and name cb
dist intra_5634_out_range , resid 78 and blastp_afP94356 and chain A and name cb, resid 53 and blastp_afP94356 and chain A and name cb
dist intra_1009_unknown , resid 98 and blastp_afP94356 and chain A and name cb, resid 54 and blastp_afP94356 and chain A and name cb
dist intra_1119_unknown , resid 39 and blastp_afP94356 and chain A and name cb, resid 170 and blastp_afP94356 and chain A and name cb
dist intra_2784_unknown , resid 168 and blastp_afP94356 and chain A and name cb, resid 39 and blastp_afP94356 and chain A and name cb
dist intra_4355_unknown , resid 54 and blastp_afP94356 and chain A and name cb, resid 97 and blastp_afP94356 and chain A and name cb
dist intra_4366_unknown , resid 39 and blastp_afP94356 and chain A and name cb, resid 178 and blastp_afP94356 and chain A and name cb
dist intra_4487_unknown , resid 39 and blastp_afP94356 and chain A and name cb, resid 53 and blastp_afP94356 and chain A and name cb
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
save blastp_afP94356.pse
png blastp_afP94356.png
