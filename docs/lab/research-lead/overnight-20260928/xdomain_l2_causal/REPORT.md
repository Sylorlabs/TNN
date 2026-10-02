# REPORT: XDOMAIN-L2-IFACE (cross-domain L2 interface adaptation)

Worker: XDomain L2 Interface-Adaptation Worker. Branch: tnn-native-lab.
Local only, never pushed. Frozen PREREG.md committed as 5a849a249 before
any implementation; one transparent pre-implementation amendment
(PREREG_AMENDMENT1.md: D_COUNT teaching values corrected 2,3 -> 1,1).

## Verdict

**XDOMAIN-L2-IFACE-PASS.** Kill bars K1-K10 all pass. No bar was weakened;
no prereg violation occurred.

## What was demonstrated

X = learned causal path model (NODE -> PATH, walks r=91, returns the full
cause-to-effect node sequence). Y = learned intervention selector
(NODE -> NUM, expects a single intervention target node, r=92 lookup).
The H1-style contract-checked composer detects X.out (PATH=3) != Y.in
(NODE=1), refuses the pair, and emits MISMATCH. Triggered only by that
detection, the adapt bracket searches the learner's own inventory for a
PATH -> NODE projection, tries candidates in node-id order, and selects
by the learner-owned intervenability rule: the projected value must be
one the downstream consumer Y successfully executes on
(exec_map(Y, proj) != -1), grounded in learner state (no relation named
in the rule), with the full pipeline verified against the target by real
execution. FIRST (projects the start node 11, Y fails) is rejected; LAST
(projects the effect node 13, Y yields 101) is accepted. The composite
Z = X;LAST;Y is promoted with LINK14 provenance to all three segments,
a type-16 adapted-via edge Z -> LAST, and type-15 co-use edges X -> LAST
and LAST -> Y written on episode success. The same adapter (id 2) is
reused on a second query with a different path length (4 vs 3) via the
generalized composite, with zero re-adaptation.

## Per-bar results

- K1 (A1 treat): PASS. Checks c1(adapter=2)=1 c2(link14)=1
  c3(t16+t15)=1 c4(counts)=1 c5(mismatch recorded)=1. Trace:
  `MISMATCH a=0 out=3 b=5 in=1`, then
  `ADAPT-TRY c=1 proj=11 yexec=-1 plen=3 REJECT`, then
  `ADAPT-TRY c=2 proj=13 yexec=101 plen=3 ADAPT-OK`,
  `Z-ADAPT z=8 a=0 c=2 b=5`.
- K2 (A2 reuse): PASS. Query 1 solves via ADAPT-OK; query 2
  (21 -> 102, path length 4) solves via `Z-SINGLE m=8` (the adapted
  composite generalizes); solving composite segment id == 2 (same
  adapter); adapt_ok count stays 1; nmaps stays 9; edge counts unchanged
  (type14=3, type15=2, type16=1). No one-off hack: the adapter works for
  a different path length with no new adaptation.
- K3 (A3/A4/A5 ablations): PASS. All Z-FAIL. A5 is the decisive one: X
  and Y intact, LAST killed -> Z-FAIL; trace shows ADAPT-TRY rejections
  for c=1 (proj 11, yexec -1) and c=3 (proj 12, yexec -1) plus
  target-check rejections; zero promotions. The adapter did the work.
- K4 (A6 no-adapt control): PASS. Z-FAIL; MISMATCH traced; zero ADAPT-
  trace lines (grep count 0); zero type-15/16 edges. Exact composition
  (singles, contract-checked pairs, H2 value-passing) provably cannot
  solve the mismatch task. The noadapt build differs by exactly one line
  (diff shows only `fn adapt_on()i32 { return 1; }` -> `return 0;`).
- K5 (A7 fresh): PASS. Z-FAIL, no teaching, nothing to adapt.
- K6 (A8 impossible): PASS. Z-FAIL on chain 31->32->33 with no
  intervention facts; every projection rejected (yexec -1); zero
  promotions; zero type-14/15/16 edges. Clean reject, no hallucinated
  interface.
- K7 (determinism): PASS. 3/3 byte-identical runs for both binaries.
  sha256 adapt build:
  6f3a005647c332eea97d2f53f9d3ee606225d95f30b75897dd70821546bad2ee
  sha256 noadapt build:
  8fa17a38abecabcaf46bb38c9f980f2cd1c48cae744c89bc9e78ddb26e404d3f
- K8 (no dashes): PASS. check_no_dash.sh clean on all deliverables
  (NAMECHECK.md, PREREG.md, PREREG_AMENDMENT1.md, both .zag files, both
  run logs).
- K9 (0-new-machinery): PASS. edge_add calls use only types 14, 15, 16
  (verified by grep). Zero new MAP types, opcodes, modes, bridges,
  handlers, semantic cases. PATH is a generic value kind in the kind
  probe (handle-range test); all eight MAP signatures learned from
  probe_kind observations with zero per-MAP literals.
- K10 (white-box traceability): PASS. The run log names every projection
  tried (c=1 FIRST, c=2 LAST, c=3 D_PROJ), its projected node, the
  consumer-exec result (yexec), the path length, and the accept/reject
  reason, so the selection of LAST is attributable to learner state.

## Adapter synthesis trace (A1, verbatim)

MISMATCH a=0 out=3 b=5 in=1
ADAPT-TRY c=1 proj=11 yexec=-1 plen=3 REJECT
ADAPT-TRY c=2 proj=13 yexec=101 plen=3 ADAPT-OK
Z-ADAPT z=8 a=0 c=2 b=5

Reading: the composer refuses X->Y on the PATH vs NODE contract
mismatch; the bracket tries the in-inventory PATH->NODE projections in
node-id order; FIRST projects node 11, on which Y fails (yexec -1), so
it is rejected by the intervenability rule; LAST projects node 13, on
which Y executes to 101, matching the target, so it is accepted and the
adapted composite is promoted. No researcher choice is involved at any
step: candidates, order, and selection criterion are all learner-state
driven.

## Ablation numbers

| Arm | Setup | Result |
| A1 | treat | ADAPT-OK, z=8, adapter=2 |
| A2 | treat + 2nd query (plen 4) | both solve, adapter reused, adapt_ok=1 |
| A3 | X killed | Z-FAIL |
| A4 | Y killed | Z-FAIL |
| A5 | adapter (LAST) killed, X+Y intact | Z-FAIL, 0 promotions |
| A6 | noadapt build | Z-FAIL, 0 ADAPT- lines |
| A7 | fresh | Z-FAIL |
| A8 | no intervention facts | Z-FAIL, 0 edges |

## Cognition lines added

ia_core.zag: 612 total lines, 575 non-comment lines. This is the entire
new learner cognition for the experiment: kind probe, path records,
nine behaviors, teaching, contract-checked solver, adapt bracket,
promotion with provenance, and the eight-arm battery. ia_full_noadapt.zag
is the one-line control variant. No shared files were modified.

## Toolchain

Safebin active (36 tools, python3/python absent, rc=1 on both); pinned
znc_linux_x86_64_abed8aa1; pure Zag throughout. Compiler-defect
workarounds honored: u8-backed cells with g32/s32; single-buffer
e1str/e1i64 output with one raw syscall (binaries exit rc=0 asserting
full write); no cast-slice `.len` reliance; if-nesting <= 3 via hoisted
flags; no `!(.. && ..)` in while conditions (grep verified empty);
capacity far under limits (fixed tables: 48 facts, 12 MAPs, 24 path
records, 64 edges).

## Commits

- 5a849a249 frozen prereg (PREREG.md + PREREG_AMENDMENT1.md +
  NAMECHECK.md Step 0 guard, committed alone before implementation).
- (implementation + REPORT commit hash to be recorded at commit time).

## Notes for the ledger

Interface adaptation (the last undemonstrated L2 operation alongside
substitute/iterative-extend in flight) is now demonstrated
cross-domain: mismatch detection via learned typed contracts, learner-
triggered adapter selection from own inventory by a learner-owned
intervenability rule, execution verification, provenance with reused
edge types, reuse on a different path length, and full ablation
causality (X, Y, and the adapter each necessary; exact reuse
insufficient).
