# ENUMERATION_MANIFEST_1121.md

Wave: wave-20260929-1121pdt. Run-start pin: 5f86e6cb2eaedb115235e4af52684a44b7c6eb36
(verified: git rev-parse HEAD at task start returned exactly this SHA; HEAD did not move).
Origin tip at run start: bedf8b4aab0110e3c115fb1bca3903551a32577e (unchanged; HEAD ref -> 27a4271f unchanged).

Enumeration method: the 0821pdt 67-entry table carried forward verbatim, with three changes: (a) new local archive
tnn-native-lab-wave-archive-20260929-0821pdt at 5f86e6cb2eaedb115235e4af52684a44b7c6eb36 (newly enumerated archive, LIVE entry;
note the archive branch resolves to the run-start tip, since the 0821pdt archive was created at the wave-end judge commit);
(b) local-tnn-native-lab now tested at the new run-start tip 5f86e6cb2eaedb115235e4af52684a44b7c6eb36 (LIVE), and its prior-wave
pin d24eda8b (already tested LIVE at 0821pdt) moves to the fixture set under the explicit renamed entry local-0821pdt-tip;
(c) the 0821pdt LIVE entry arch-wave-20260929-0521pdt at 2e9326e6 moves to the fixture set keeping its name. Total: 69 named entries.
Live entries (2): arch-wave-20260929-0821pdt (5f86e6cb2, newly enumerated archive),
local-tnn-native-lab (5f86e6cb2, run-start tip). Both LIVE entries extract the same commit.
Fixture entries (67): all other named entries, pinned to their prior-tested SHAs; every one of the 67 carried fixture SHAs
verified to resolve in this repo before the run (git cat-file -t loop, zero misses). Duplicate SHA groups named in
FORK_BATTERY_1121.md.
Zero new remote refs since 0821pdt (read-only git ls-remote at run start: origin/tnn-native-lab bedf8b4a, HEAD 27a4271f,
fs-gr1, r2-7, reorg/phase-0-1, wg-freeze, pull/1, pull/2, pull/3 heads all at their 0821pdt pins). Zero new local branches
since 0821pdt except the new 0821pdt archive; the 3 experimental branches (wave-20260927-0221pdt-exp1/exp2/sensory) resolve
to the same SHAs as the existing exp1/exp2/exp-sensory fixture entries (1010a63c, a2a36e65, c368b8e1), so they are covered
by pinned-SHA extraction, not re-enumerated.
Zero Python; pure shell, git, sha256sum, pinned znc, frozen pure-Zag harness.

Driver: batch_1121.sh (69 run() lines), derived from batch_0821.sh by mechanical edit (wave name, scratch
path ~/workspace/fb1121pdt, run-start pin) plus the declared live/fixture rotation; body of the run lines byte-identical
except the rotation. Confirmed by diff: the only changes are the header lines, the scratch path, the pin, and the top
live/fixture block.
run_one.sh sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978, byte-identical to the frozen
instrument. Harness binary ~/workspace/fb1421/fork_battery sha256
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66, re-verified byte-identical to the frozen
instrument (re-verified, not rebuilt from source this wave). Negative-control fixtures neg1.zag, neg2.zag,
forkbat_hello.zag copied from fb0821pdt (SHAs: b55b57a1b25d17f0165c0d20796d6058dec4050c34a35ed9700e698f5aa6eb2a,
79d8449b2de1b4af943901aac223b728aad17af2df34f11933fe3ace153567c2,
a24fe17df8fb164b64897142cc357f70910bb8442cd6bbc633b8cbff49d14d82).

Setup anomaly (caught by the driver launch, no verdict affected): the copied batch_1121.sh lacked the executable
bit (cp preserved 644), so the first background launch failed with "./batch_1121.sh: Permission denied" (driver exit
126) before any entry ran. The bit was set with chmod +x and the full battery re-run from scratch. No partial
results were kept (the only E-dir content at that point was a pre-launch smoke test dir, removed before re-run).

No em-dashes used in this document.
