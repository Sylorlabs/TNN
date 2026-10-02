# ENUMERATION_MANIFEST_0821.md

Wave: wave-20260929-0821pdt. Run-start pin: d24eda8bdc34dee54aace6451b193754e96784ab.
Origin tip at run start: bedf8b4aab0110e3c115fb1bca3903551a32577e (unchanged; HEAD ref -> 27a4271f unchanged).
Enumeration method: the 0521pdt 65-entry table carried forward verbatim, with three changes: (a) new local archive
tnn-native-lab-wave-archive-20260929-0521pdt at 2e9326e6caf4a9462102e8dfc8058e7cec2404d6 (newly enumerated archive, LIVE entry);
(b) local-tnn-native-lab now tested at the new run-start tip d24eda8bdc34dee54aace6451b193754e96784ab (LIVE), and its prior-wave
pin d2fdf1225 (already tested LIVE at 0521pdt) moves to the fixture set under the explicit renamed entry local-0521pdt-tip;
(c) the 0521pdt LIVE entry arch-wave-20260929-0221pdt at d2fdf1225 moves to the fixture set keeping its name. Total: 67 named entries.
Live entries (2): arch-wave-20260929-0521pdt (2e9326e6), local-tnn-native-lab (d24eda8b).
Fixture entries (65): all other named entries, pinned to their prior-tested SHAs; the 63 carried fixture SHAs are
byte-identical to the 0521pdt table (verified by diff of the batch scripts, which shows only the intended live/fixture
rotation changes); duplicate SHA groups named in FORK_BATTERY_0821.md.
Zero new remote refs since 0521pdt (read-only git ls-remote at run start: origin/tnn-native-lab bedf8b4a, HEAD 27a4271f,
fs-gr1, r2-7, reorg/phase-0-1, wg-freeze, pull/1, pull/2, pull/3 heads all at their 0521pdt pins). Zero new local branches
since 0521pdt except the new 0521pdt archive; the 3 experimental branches (wave-20260927-0221pdt-exp1/exp2/sensory) resolve
to the same SHAs as the existing exp1/exp2/exp-sensory fixture entries (1010a63c, a2a36e65, c368b8e1), so they are covered
by pinned-SHA extraction, not re-enumerated.
Zero Python; pure shell, git, sha256sum, pinned znc, frozen pure-Zag harness.

Driver: batch_0821.sh (67 run() lines), derived from the frozen batch_0521.sh by mechanical sed (wave name, scratch
path, run-start pin) plus the declared live/fixture rotation; body of the run lines byte-identical except the rotation.
run_one.sh sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978, byte-identical to the frozen
instrument. Harness binary ~/workspace/fb1421/fork_battery sha256
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66, re-verified byte-identical to the frozen
instrument (re-verified, not rebuilt from source this wave). Negative-control fixtures neg1.zag, neg2.zag,
forkbat_hello.zag copied from fb0521pdt (SHAs recorded in FORK_BATTERY_0521.md).

Setup anomaly (caught by the pin check, no verdict affected): the first
background launch of this wave's runner pointed HARNESS at
~/workspace/fb1421/fork_battery/fork_battery (a path that does not exist;
the binary IS ~/workspace/fb1421/fork_battery). The runner's pin check
failed with exit 11 before any entry ran; the path was corrected and the
full battery re-run from scratch. No partial results were kept.

No em-dashes used in this document.
