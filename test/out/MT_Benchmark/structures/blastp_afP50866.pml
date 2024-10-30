load blastp_afP50866.pdb
hide all
bg_color white
set transparency, 0.8
zoom center, 50;
hide everything, show cartoon, chain A
show surface, chain A and blastp_afP50866
color 3, chain A
show cartoon, chain A
dist intra_337_valid , resid 322 and blastp_afP50866 and chain A and name cb, resid 329 and blastp_afP50866 and chain A and name cb
dist intra_788_valid , resid 283 and blastp_afP50866 and chain A and name cb, resid 83 and blastp_afP50866 and chain A and name cb
dist intra_5352_overlaps , resid 262 and blastp_afP50866 and chain A and name cb, resid 271 and blastp_afP50866 and chain A and name cb
dist intra_131_unknown , resid 283 and blastp_afP50866 and chain A and name cb, resid 262 and blastp_afP50866 and chain A and name cb
dist intra_263_unknown , resid 283 and blastp_afP50866 and chain A and name cb, resid 271 and blastp_afP50866 and chain A and name cb
dist intra_1066_unknown , resid 101 and blastp_afP50866 and chain A and name cb, resid 94 and blastp_afP50866 and chain A and name cb
dist intra_1237_unknown , resid 262 and blastp_afP50866 and chain A and name cb, resid 277 and blastp_afP50866 and chain A and name cb
dist intra_1494_unknown , resid 101 and blastp_afP50866 and chain A and name cb, resid 175 and blastp_afP50866 and chain A and name cb
dist intra_1557_unknown , resid 277 and blastp_afP50866 and chain A and name cb, resid 417 and blastp_afP50866 and chain A and name cb
dist intra_1962_unknown , resid 310 and blastp_afP50866 and chain A and name cb, resid 277 and blastp_afP50866 and chain A and name cb
dist intra_2042_unknown , resid 324 and blastp_afP50866 and chain A and name cb, resid 101 and blastp_afP50866 and chain A and name cb
dist intra_2218_unknown , resid 311 and blastp_afP50866 and chain A and name cb, resid 329 and blastp_afP50866 and chain A and name cb
dist intra_2693_unknown , resid 262 and blastp_afP50866 and chain A and name cb, resid 189 and blastp_afP50866 and chain A and name cb
dist intra_2695_unknown , resid 262 and blastp_afP50866 and chain A and name cb, resid 278 and blastp_afP50866 and chain A and name cb
dist intra_5792_unknown , resid 271 and blastp_afP50866 and chain A and name cb, resid 278 and blastp_afP50866 and chain A and name cb
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
save blastp_afP50866.pse
png blastp_afP50866.png
