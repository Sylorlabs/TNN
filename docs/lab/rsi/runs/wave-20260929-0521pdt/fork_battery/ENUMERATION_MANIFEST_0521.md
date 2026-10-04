# ENUMERATION_MANIFEST_0521.md

Wave: wave-20260929-0521pdt. Run-start pin: d2fdf1225ec973e1e07082af6b067fd1525cb643.
Origin tip at run start: bedf8b4aab0110e3c115fb1bca3903551a32577e (unchanged; HEAD ref -> 27a4271f unchanged).
Enumeration method: the 0221pdt 63-entry table carried forward verbatim, with three changes: (a) new local archive
tnn-native-lab-wave-archive-20260929-0221pdt at d2fdf1225 (newly enumerated archive, LIVE entry); (b) local-tnn-native-lab
now tested at the new run-start tip d2fdf1225 (LIVE), and its prior-wave pin a014dc1d9 (already tested LIVE at 0221pdt)
moves to the fixture set under the explicit renamed entry local-0221pdt-tip (this replaces the 0221pdt convention of
folding the prior live pin under an archive wave name, which was confusing; the rename is declared here); (c) the
0221pdt LIVE entry arch-wave-20260928-2321pdt at a014dc1d9 moves to the fixture set keeping its name. Total: 65 named entries.
Live entries (2): arch-wave-20260929-0221pdt (d2fdf1225), local-tnn-native-lab (d2fdf1225).
Fixture entries (63): all other named entries, pinned to their prior-tested SHAs; the 61 carried fixture SHAs are
byte-identical to the 0221pdt table (verified by diff of the batch scripts, which shows only the intended live/fixture
rotation changes); duplicate SHA groups named in FORK_BATTERY_0521.md.
Zero new remote refs since 0221pdt (read-only git ls-remote at run start: origin/tnn-native-lab bedf8b4a, HEAD 27a4271f,
fs-gr1, r2-7, reorg/phase-0-1, wg-freeze, pull/1, pull/2, pull/3 heads all at their 0221pdt pins; local rev-parse of
rh-main, rh-tnn-native-lab-live-tip, rh-pull-1-head, rh-pull-2-head, rh-pull-3-head, origin/tnn-native-lab all match
the fixture SHAs). Zero new local branches since 0221pdt except the new archive; the 3 new experimental branches
(wave-20260927-0221pdt-exp1/exp2/sensory) resolve to the same SHAs as the existing exp1/exp2/exp-sensory fixture entries
(1010a63c, a2a36e65, c368b8e1), so they are covered by pinned-SHA extraction, not re-enumerated.
Zero Python; pure shell, git, sha256sum, pinned znc, frozen pure-Zag harness.

Driver: batch_0521.sh (65 run() lines), derived from the frozen batch_0221.sh by mechanical sed (wave name, scratch
path, run-start pin) plus the declared live/fixture rotation; body of the run lines byte-identical except the rotation.
run_one.sh sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978, byte-identical to the frozen
instrument. Harness binary ~/workspace/fb1421/fork_battery sha256
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66, re-verified byte-identical to the frozen
instrument (re-verified, not rebuilt from source this wave). Negative-control fixtures neg1.zag, neg2.zag,
forkbat_hello.zag copied from fb0221pdt (SHAs recorded in FORK_BATTERY_0521.md).

No em-dashes used in this document.
