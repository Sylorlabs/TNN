# B7 artifacts — fork H1: Witnessed Event Lattice

Human verdict: **PENDING-MICAH** (never silently passed).

Preregistered human bars (PREREG_H1.md §8 B7 / §9):
- native audio replay must pass a human double-blind field-recording equivalence test at 90% agreement;
- visual reconstruction/imagery judged realistic by >=80% of raters.

What each artifact shows: the event lattice H1 actually built from the fixture (witness spans = the exact input regions measured; sup/con = integer support/contradiction; disp = the memory contract's disposition). Audio excerpts are bit-exact slices of the fixture's own samples -- what H1 heard, nothing synthesized.

## colordisc / clean

p000.img truth=SAME H1=SAME conf=666 disp=INSTALL

note: clean primary fixture: correct judgment, contract INSTALLED (baseline behavior).

artifact: `colordisc_clean_overlay.png`

4 event records; witness rects = the exact spans H1 measured

## colordisc / trap

p007.img truth=DIFFERENT H1=SAME conf=117 disp=WITHHELD

note: contract WITHHELD a misleading input.

artifact: `colordisc_trap_overlay.png`

4 event records; witness rects = the exact spans H1 measured

## colorconst / clean

p000.img truth=SAME_SURFACE H1=SAME_SURFACE conf=607 disp=INSTALL

note: clean primary fixture: correct judgment, contract INSTALLED (baseline behavior).

artifact: `colorconst_clean_overlay.png`

3 event records; witness rects = the exact spans H1 measured

## colorconst / trap

p001.img truth=DIFFERENT H1=SAME_SURFACE conf=673 disp=INSTALL

note: contract INSTALLED on an adversarial input (shown honestly).

artifact: `colorconst_trap_overlay.png`

3 event records; witness rects = the exact spans H1 measured

## shapetrans / clean

p001.img truth=TRIANGLE H1=TRIANGLE conf=749 disp=INSTALL

note: clean primary fixture: correct judgment, contract INSTALLED (baseline behavior).

artifact: `shapetrans_clean_overlay.png`

5 event records; witness rects = the exact spans H1 measured

## shapetrans / trap

p001.img truth=TRIANGLE H1=TRIANGLE conf=119 disp=WITHHELD

note: contract WITHHELD a misleading input.

artifact: `shapetrans_trap_overlay.png`

5 event records; witness rects = the exact spans H1 measured

## pitchdisc / clean

p000.pcm truth=SAME H1=SAME conf=833 disp=INSTALL

note: clean primary fixture: correct judgment, contract INSTALLED (baseline behavior).

artifact: `pitchdisc_clean_ev0_ONSET_wit0.wav, pitchdisc_clean_ev1_SUSTAIN_wit0.wav, pitchdisc_clean_ev2_F0_SAME_wit0.wav, pitchdisc_clean_ev2_F0_SAME_wit1.wav`

bit-exact witness-span excerpts; waveform PNG shows shaded spans H1 measured

## pitchdisc / trap

p000.pcm truth=HIGHER H1=SAME conf=0 disp=WITHHELD

note: contract WITHHELD a misleading input.

artifact: `pitchdisc_trap_ev0_F0_SAME_wit0.wav`

bit-exact witness-span excerpts; waveform PNG shows shaded spans H1 measured

## timbredisc / clean

p000.pcm truth=PURE H1=PURE conf=707 disp=INSTALL

note: clean primary fixture: correct judgment, contract INSTALLED (baseline behavior).

artifact: `timbredisc_clean_ev0_TIMBRE_PURE_wit0.wav, timbredisc_clean_ev1_TIMBRE_PURE_wit0.wav, timbredisc_clean_ev2_TIMBRE_PURE_wit0.wav, timbredisc_clean_ev2_TIMBRE_PURE_wit1.wav`

bit-exact witness-span excerpts; waveform PNG shows shaded spans H1 measured

## timbredisc / trap

p000.pcm truth=RICH H1=DARK conf=737 disp=INSTALL

note: contract INSTALLED on an adversarial input (shown honestly).

artifact: `timbredisc_trap_ev0_TIMBRE_DARK_wit0.wav, timbredisc_trap_ev1_TIMBRE_DARK_wit0.wav, timbredisc_trap_ev2_TIMBRE_DARK_wit0.wav, timbredisc_trap_ev2_TIMBRE_DARK_wit1.wav`

bit-exact witness-span excerpts; waveform PNG shows shaded spans H1 measured

## motiondir / clean

p004.vid truth=E H1=E conf=833 disp=INSTALL

note: clean primary fixture: correct judgment, contract INSTALLED (baseline behavior).

artifact: `motiondir_clean_overlay.png`

middle frame; red arrow = DIR event; span events listed

## motiondir / trap

p000.vid truth=STILL H1=N conf=96 disp=WITHHELD

note: contract WITHHELD a misleading input.

artifact: `motiondir_trap_overlay.png`

middle frame; red arrow = DIR event; span events listed

