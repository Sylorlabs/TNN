# ENUMERATION_MANIFEST (fork-battery run, 2026-09-30, wave-20260930-2321pdt)

Total: 87 named entries (1 LIVE, 86 fixture).

Run-start pin: 23c2c0206b0e08997c7695b5813be5d8aa293da0 (local
tnn-native-lab tip at enumeration time; pinned-commit discipline: every
extraction is by pinned SHA, never by live ref, so mid-battery lane
commits are inert).

Enumeration method: the 0821pdt wave's 84-entry table carried forward
verbatim, with these changes:
(a) local-tnn-native-lab now tested at the new run-start pin
23c2c0206b0e08997c7695b5813be5d8aa293da0 (LIVE); its prior-wave pin
fdadcbe3c7b49887e795462a11664122349591c1 moves to the fixture set
under the new entry local-20260930-2321pdt-tip.
(b) Two new archive branches since the 0821pdt wave, added as fixtures:
arch-wave-20260930-0821pdt at bb9b56a34d2063d41118db1b2aa4a0366790f15d
(the 0821pdt wave's own archive, committed mid-wave after enumeration)
and arch-wave-20260930-1121pdt at caf07be920075ccc9027aea075f4ee566a2420a3.
(c) All 45 other live branch tips resolve to pins already in the
carried-forward table (checked by exact SHA match against the 0821pdt
driver SHA set; 68 unique SHAs). No live branch tip moved since the
0821pdt wave except the three accounted for in (a) and (b). The two
mid-wave commits on tnn-native-lab since the 0821pdt run-start pin
(97b28e6a6 CORE-FREEZE-RUN-COMPLETE and ce1a7c5f8 CORE-FREEZE-TNN2
prereg) are ancestors of the new run-start pin and are covered by the
LIVE extraction at the tip pin, not separately enumerated.

Remote: read-only git ls-remote this run shows zero new refs
(origin/tnn-native-lab bedf8b4aa unchanged; HEAD/main 27a4271f; fs-gr1,
r2-7, reorg/phase-0-1, wg-freeze, pull/1, pull/2, pull/3 heads all at
their prior pins). Stale refs/remotes/rh-* carried as fixtures.

ARCHIVE-BRANCH IMMUTABILITY CHECK (automated in the enumeration step):
every tnn-native-lab-wave-archive-* branch tip was checked against the
set of SHAs pinned in the 0821pdt wave's driver table. Result: all 43
existing archive branches resolve to pins in the table or are the two
new entries added in (b); ZERO movement of existing pins. The four
previously documented driver entries with no live branch
(arch-wave-20260929-1721pdt-tip2, arch-20260924-0821pdt,
arch-wave-20260927-0821pdt, arch-wave-20260929-1721pdt old pin) remain
unchanged in status. The standing rule holds: archive branches are
immutable; re-create, never move.

rh-pull-1-head (5802fec8) and rh-pull-2-head (4b76bb59) are non-TNN trees
with the pinned toolchain path absent (expected UNTESTABLE).

Driver: batch_2321pdt.sh (87 run() lines), derived from batch_0821pdt.sh
by mechanical edit (wave name, scratch path ~/workspace/fb0930_2321pdt,
run-start pin, live/fixture rotation) plus the four declared
additions/rotations; the 84 carried run lines byte-identical except the
LIVE pin rotation. run_one.sh sha256
4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978,
byte-identical to the frozen instrument.
Harness: REBUILT this run from committed source
docs/lab/rsi/runs/wave-20260927-2321pdt/forks/fork_battery.zag (sha256
f38d9154eecb2a6e7a1682c1f6850da80aba7fbe6d73e5e6f4b31aac3f719738)
with the pinned znc (498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef);
rebuilt binary sha256
a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66,
BYTE-IDENTICAL to the frozen instrument ~/workspace/fb1421/fork_battery.
Scratch: ~/workspace/fb0930_2321pdt/E/ (87 entry dirs). Zero Python in
battery construction and execution; pure shell, git, sha256sum, pinned
znc, pure-Zag harness.

CONSISTENCY GATE (pre-run gate): consistency_gate.sh --pre-run asserts
(A1) driver run() count equals the manifest's declared total and (A2)
every run() SHA resolves, BEFORE the battery executes. The full gate
(A1-A4) still blocks the results commit. Pre-run gate result: recorded
in the results file.

No em-dashes in this documentation.
