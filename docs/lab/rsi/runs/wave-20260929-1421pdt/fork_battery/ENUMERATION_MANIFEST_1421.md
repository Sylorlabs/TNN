# ENUMERATION_MANIFEST_1421.md

Wave: wave-20260929-1421pdt. Run-start pin: d18f7f68d3792c58346861b89eab374c2e728ef0
(verified: git rev-parse HEAD at task start returned exactly this SHA; HEAD has
since moved only by this wave's own prereg-freeze commit 55fece368, which is
inert for the battery under pinned-commit discipline).
Origin tip at run start: bedf8b4aab0110e3c115fb1bca3903551a32577e (unchanged; HEAD ref -> 27a4271f unchanged; read-only git ls-remote at wave start).

Enumeration method: the 1121pdt 69-entry table carried forward verbatim, with
four changes: (a) new local archive tnn-native-lab-wave-archive-20260929-1121pdt
at d18f7f68d (newly enumerated archive, LIVE entry; created this wave to pin
the 1121pdt partial-evidence tip, which had no archive pointer because that
wave died INCOMPLETE); (b) local-tnn-native-lab now tested at the new
run-start tip d18f7f68d (LIVE), and its prior-wave pin 5f86e6cb2 (already
tested LIVE at 1121pdt) moves to the fixture set under the explicit renamed
entry local-1121pdt-tip; (c) the 1121pdt LIVE entry arch-wave-20260929-0821pdt
at 5f86e6cb2 moves to the fixture set keeping its name; (d) the 0821pdt LIVE
entries arch-wave-20260929-0521pdt (2e9326e6) and local-0821pdt-tip (d24eda8b)
are carried as fixtures with names kept. Total: 71 named entries.
Live entries (2): arch-wave-20260929-1121pdt (d18f7f68d, newly enumerated
archive), local-tnn-native-lab (d18f7f68d, run-start tip). Both LIVE entries
extract the same commit.
Fixture entries (69): all other named entries, pinned to their prior-tested
SHAs; every one of the 69 carried fixture SHAs verified to resolve in this
repo before the run (git cat-file -t loop, zero misses). Duplicate SHA groups
named in FORK_BATTERY_1421.md.
Zero new remote refs since 1121pdt (read-only git ls-remote at wave start:
origin/tnn-native-lab bedf8b4a, HEAD 27a4271f, fs-gr1, r2-7, reorg/phase-0-1,
wg-freeze, pull/1, pull/2, pull/3 heads all at their 1121pdt pins). Zero new
local branches since 1121pdt except the new 1121pdt archive created above; the
3 experimental branches (wave-20260927-0221pdt-exp1/exp2/sensory) resolve to
the same SHAs as the existing exp1/exp2/exp-sensory fixture entries
(1010a63c, a2a36e65, c368b8e1), so they are covered by pinned-SHA extraction,
not re-enumerated.
Zero Python; pure shell, git, sha256sum, pinned znc, frozen pure-Zag harness.

Driver: batch_1421.sh (71 run() lines), derived from batch_0821.sh by
mechanical edit (wave name, scratch path ~/workspace/fb1421pdt, run-start
pin, live/fixture rotation) plus the declared 1121pdt carry-forward; body
of the run lines byte-identical except the rotation. run_one.sh sha256
4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978,
byte-identical to the frozen instrument. Harness binary
~/workspace/fb1421/fork_battery re-verified byte-identical to the frozen
instrument before the run (sha256 checked, recorded in FORK_BATTERY_1421.md).
