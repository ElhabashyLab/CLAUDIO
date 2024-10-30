load blastp_afP09339.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP09339
color 3, chain A
show cartoon, chain A
dist intra_60_valid , resid 41 and blastp_afP09339 and chain A and name cb, resid 75 and blastp_afP09339 and chain A and name cb
dist intra_117_valid , resid 67 and blastp_afP09339 and chain A and name cb, resid 82 and blastp_afP09339 and chain A and name cb
dist intra_317_valid , resid 32 and blastp_afP09339 and chain A and name cb, resid 17 and blastp_afP09339 and chain A and name cb
dist intra_379_valid , resid 66 and blastp_afP09339 and chain A and name cb, resid 82 and blastp_afP09339 and chain A and name cb
dist intra_664_valid , resid 32 and blastp_afP09339 and chain A and name cb, resid 44 and blastp_afP09339 and chain A and name cb
dist intra_1408_valid , resid 634 and blastp_afP09339 and chain A and name cb, resid 171 and blastp_afP09339 and chain A and name cb
dist intra_1613_valid , resid 277 and blastp_afP09339 and chain A and name cb, resid 285 and blastp_afP09339 and chain A and name cb
dist intra_1666_valid , resid 701 and blastp_afP09339 and chain A and name cb, resid 712 and blastp_afP09339 and chain A and name cb
dist intra_2661_valid , resid 707 and blastp_afP09339 and chain A and name cb, resid 772 and blastp_afP09339 and chain A and name cb
dist intra_4501_valid , resid 475 and blastp_afP09339 and chain A and name cb, resid 592 and blastp_afP09339 and chain A and name cb
dist intra_5030_valid , resid 777 and blastp_afP09339 and chain A and name cb, resid 676 and blastp_afP09339 and chain A and name cb
dist intra_5694_out_range , resid 683 and blastp_afP09339 and chain A and name cb, resid 712 and blastp_afP09339 and chain A and name cb
dist intra_2230_overlaps , resid 10 and blastp_afP09339 and chain A and name cb, resid 59 and blastp_afP09339 and chain A and name cb
dist intra_2380_overlaps , resid 6 and blastp_afP09339 and chain A and name cb, resid 59 and blastp_afP09339 and chain A and name cb
dist intra_2458_overlaps , resid 6 and blastp_afP09339 and chain A and name cb, resid 113 and blastp_afP09339 and chain A and name cb
dist intra_40_unknown , resid 67 and blastp_afP09339 and chain A and name cb, resid 10 and blastp_afP09339 and chain A and name cb
dist intra_124_unknown , resid 67 and blastp_afP09339 and chain A and name cb, resid 6 and blastp_afP09339 and chain A and name cb
dist intra_459_unknown , resid 59 and blastp_afP09339 and chain A and name cb, resid 82 and blastp_afP09339 and chain A and name cb
dist intra_848_unknown , resid 10 and blastp_afP09339 and chain A and name cb, resid 66 and blastp_afP09339 and chain A and name cb
dist intra_1364_unknown , resid 6 and blastp_afP09339 and chain A and name cb, resid 66 and blastp_afP09339 and chain A and name cb
dist intra_1877_unknown , resid 6 and blastp_afP09339 and chain A and name cb, resid 123 and blastp_afP09339 and chain A and name cb
dist intra_1949_unknown , resid 33 and blastp_afP09339 and chain A and name cb, resid 75 and blastp_afP09339 and chain A and name cb
dist intra_2721_unknown , resid 285 and blastp_afP09339 and chain A and name cb, resid 265 and blastp_afP09339 and chain A and name cb
dist intra_2949_unknown , resid 10 and blastp_afP09339 and chain A and name cb, resid 6 and blastp_afP09339 and chain A and name cb
dist intra_3059_unknown , resid 59 and blastp_afP09339 and chain A and name cb, resid 76 and blastp_afP09339 and chain A and name cb
dist intra_3483_unknown , resid 6 and blastp_afP09339 and chain A and name cb, resid 82 and blastp_afP09339 and chain A and name cb
dist intra_3549_unknown , resid 285 and blastp_afP09339 and chain A and name cb, resid 261 and blastp_afP09339 and chain A and name cb
dist intra_4131_unknown , resid 10 and blastp_afP09339 and chain A and name cb, resid 17 and blastp_afP09339 and chain A and name cb
dist intra_4597_unknown , resid 66 and blastp_afP09339 and chain A and name cb, resid 76 and blastp_afP09339 and chain A and name cb
dist intra_4622_unknown , resid 41 and blastp_afP09339 and chain A and name cb, resid 68 and blastp_afP09339 and chain A and name cb
dist intra_4945_unknown , resid 17 and blastp_afP09339 and chain A and name cb, resid 6 and blastp_afP09339 and chain A and name cb
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
save blastp_afP09339.pse
png blastp_afP09339.png
