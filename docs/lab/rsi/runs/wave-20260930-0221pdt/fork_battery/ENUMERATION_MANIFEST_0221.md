# ENUMERATION_MANIFEST_0221.md

Wave: wave-20260930-0221pdt. Run-start pin:
1f681e87b6a64fc65e4c01ead66b6db919c365b8 (tip at battery start;
mid-battery lane commits inert by pinned-commit discipline).
Origin tip at run start: bedf8b4aab0110e3c115fb1bca3903551a32577e
(unchanged; HEAD ref 27a4271f unchanged; read-only git ls-remote at
wave start).

Enumeration method: the 2321pdt 75-entry table carried forward
verbatim, with these changes: (a) new local archive
tnn-native-lab-wave-archive-20260929-2321pdt at
a4314633ac48591d3217d291c47b68f9e99ef77d (newly enumerated archive,
LIVE entry; created at 2321pdt end); (b) local-tnn-native-lab now
tested at the new run-start pin 1f681e87b (LIVE), and its prior-wave
pin fed72668 moves to the fixture set under the explicit renamed
entry local-20260929-2321pdt-tip (full date: the short name
local-2321pdt-tip was already taken by the 2026-09-28 2321pdt tip at
fab33cb4c); (c) the 2321pdt LIVE entry arch-wave-20260929-1721pdt at
7c11ac5af moves to the fixture set keeping its name. Total: 77 named
entries.

Live entries (2): arch-wave-20260929-2321pdt (a4314633, newly
enumerated archive), local-tnn-native-lab (1f681e87b, run-start tip).
Fixture entries (75): all other named entries, pinned to their
prior-tested SHAs; every one of the 75 carried fixture SHAs verified
to resolve in this repo before the run (git cat-file -t loop, 75/75
commit, zero misses). Duplicate SHA groups: {arch-wave-20260929-1721pdt,
local-1721pdt-tip} both at 7c11ac5af (carried); {arch-wave-20260927-0221pdt,
local-0221pdt-tip} per 1421pdt manifest (carried). Zero new remote refs
since 2321pdt (read-only git ls-remote at wave start:
origin/tnn-native-lab bedf8b4a, HEAD 27a4271f, fs-gr1, r2-7,
reorg/phase-0-1, wg-freeze, pull/1, pull/2, pull/3 heads all at their
2321pdt pins). Zero new local branches since 2321pdt except the new
2321pdt archive enumerated above; the experimental branches
(wave-20260927-0221pdt-exp1/exp2/sensory, wt-*, wave-debate-session-1-backup,
wt-forktest-debate-backup) resolve to the same SHAs as the existing
fixture entries, so they are covered by pinned-SHA extraction, not
re-enumerated.

Driver: batch_0221.sh (77 run() lines), derived from batch_2321.sh by
mechanical edit (wave name, scratch path ~/workspace/fb0930_0221pdt,
run-start pin, live/fixture rotation) plus the declared 2321pdt
carry-forward; body of the run lines byte-identical except the
rotation (verified by diff review: only the intended line changes;
the local-20260929-2321pdt-tip rename is declared above). run_one.sh
sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978,
byte-identical to the frozen instrument. Harness binary
~/workspace/fb1421/fork_battery sha256
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66,
re-verified byte-identical to the frozen instrument before the run
(re-verified, not rebuilt from source this wave). Scratch:
~/workspace/fb0930_0221pdt/E/ (77 entry dirs). Zero Python in battery
construction and execution; pure shell, git, sha256sum, pinned znc,
frozen pure-Zag harness.

No em-dashes in wave documentation.
