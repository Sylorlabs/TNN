# Coordinator rulings on H5R prereg Q1-Q5 (wave-20261001-2021pdt)

Date: 2026-10-02. These rulings are part of the frozen prereg; implementation
is authorized only after this file and PREREG_H5R.md are committed alone.

Q1: CONFIRM Option A. Delete the shadow-fact teaching (promote_graph line
551); the MAP node itself becomes the retrieval structure via the activate
extension. Option A is one-system-rule aligned (one structure, one read
path; the duplicated representation is removed, not patched). Option B
(provenance-linked shadow fact) is NOT authorized; a builder wanting Option
B needs a fresh prereg because KB-W0 distinguishes the options.

Q2: CONFIRM the working-file base. Byte-copy of the H5 lane's committed
docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/tnn3_h5.zag. Coordinator
records its SHA-256 at freeze; it must match the file that built the
verified tnn3_h5.bin (SHA-256
344ac89fb338ddbf46bea6be4c526d99410ea643278ab91fb06d76b7e33c4eb7).

Q3: CONFIRM the dropped fact-key KB-B2/KB-B3 bars. The red team proved the
unmodified TNN-2 baseline passes them, so they are non-discriminating and
cannot evidence the H5R substrate change. They are replaced by the MAP-key
KB-B2R (16/16) and KB-B3R (4/4) bars, which pin the exact (s_m,r_m)
convention from section 2.

Q4: CONFIRM. Adversary lane: TNN3H5R-ADV (a new independent agent, no
shared working state with the builder). Sealed directory:
docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5R/sealed/ (created by the
adversary; the builder has no read path). At least two worlds are designed
post-freeze with no implementation knowledge, per section 6.2.

Q5: CONFIRM the 36-snapshot white-box protocol (snapshot before every
MAP-key probe: 12 probes x 3 snapshots) and the frozen world-design
constraint of no OBSERVE on any MAP key in any world (section 6.8, section
4.6). Both are necessary for KB-W0.

Implementation is AUTHORIZED after this commit. The builder must satisfy
KB-S1 (both hunks in the committed diff) before the sealed run proceeds.
