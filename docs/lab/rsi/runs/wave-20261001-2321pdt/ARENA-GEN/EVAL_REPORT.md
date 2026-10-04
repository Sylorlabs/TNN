# EVALUATION REPORT: ARENA-GEN multi-bare-prompt generality test (wave-20261001-2321pdt)

Prereg: PREREG_MULTIBARE.md, frozen in commit ef30ef8d1 before
any battery generation, build, or run. All kill bars and the
decision rule are from that frozen prereg; none moved.

Verdict: NARROW (per the frozen decision rule; see section 6).

## 1. Mechanism under test

DEFRECALL as committed in ARENA5 implementation commit
2320c3454 (defrecall_contestant.zag, 1312 lines), extracted
via git show, never from working files. Built with the pinned
znc (src/tools/toolchain/znc_linux_x86_64_abed8aa1).

Source sha256 (extracted):
fcadb78994f772da69f95917b5a6b88a1d386a994d5faf761eccd032d46c68d9

Built binary sha256:
3d629deda888c18d19ff95ce9819829f2c268cf8e459330b7c573c3892cd57d7

This is byte-identical to ARENA5's sealed defrecall binary
(SEALED_EVAL.md), confirming the source is the committed
implementation.

v6 baseline built from the committed v6 source
(docs/lab/rsi/runs/wave-20261001-1721pdt/ARENA/refreeze/devint1_contestant_v6.zag
in commit 947675258). Binary sha256:
5d2be6acf4d98ef2118e2e1f2e52d87d38a9f848cb83e04d8b252199ce966f15,
byte-identical to ARENA5's v6 binary.

Arena scorer rebuilt from the committed frozen source; binary
sha256 3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076,
matches the refreeze record.

## 2. Multi-bare-prompt battery (frozen spec, hashed before runs)

File: battery/multibare_turns.jsonl
sha256: 022c7a756d5c206e98993429e0c9fdb9995fbe7064cf7eaf6afe57d68fad0f60

18 turns: 1 brief, 9 expo f events (entities Alpha, Beta,
Gamma, Delta, Epsilon, Zeta, Eta, Theta, Iota; fresh names,
never in any battery), 7 test turns, 1 done.

Test items and frozen expected behaviors:
- item 0, q="listnames" (bare): enumerate 9 names; set F1 >= 0.900
- item 1, q="recall" (bare, novel): enumerate 9 names; set F1 >= 0.900
- item 2, q="who" (bare, novel): enumerate 9 names; set F1 >= 0.900
- item 3, q="whattime" (bare, novel): exactly "UNKNOWN"
- item 4, q="invent" (bare, novel): exactly "UNKNOWN"
- item 5, q="invent|notation" (parameterized): exactly "UNKNOWN"
- item 6, q="foo|bar" (parameterized, novel): exactly "UNKNOWN"

## 3. Multi-bare-prompt results (3 runs, fresh state each)

All three runs completed 18 turns. Stripped reply streams
(ms, rss_kb excluded) are byte-identical across runs:
sha256 a493bd8aa3377c6068a6bdf2955952750ffb4b56a876d27af70d27a96400de28
(all three). Trace files byte-identical:
sha256 53ebe312ff4f15e6dae451898279dc770a83ede92ddb355ed0b2208f9c0d7bc3
(all three). AG-4 PASS.

Per-item replies (identical all three runs):

| item | q | reply | expected | score |
|------|---|-------|----------|-------|
| 0 | listnames (bare) | Alpha,Beta,Gamma,Delta,Epsilon,Zeta,Eta,Theta,Iota | enumerate | 1.000 PASS |
| 1 | recall (bare) | Alpha,Beta,Gamma,Delta,Epsilon,Zeta,Eta,Theta,Iota | enumerate | 1.000 PASS |
| 2 | who (bare) | Alpha,Beta,Gamma,Delta,Epsilon,Zeta,Eta,Theta,Iota | enumerate | 1.000 PASS |
| 3 | whattime (bare) | Alpha,Beta,Gamma,Delta,Epsilon,Zeta,Eta,Theta,Iota | UNKNOWN | 0.000 FAIL |
| 4 | invent (bare) | Alpha,Beta,Gamma,Delta,Epsilon,Zeta,Eta,Theta,Iota | UNKNOWN | 0.000 FAIL |
| 5 | invent\|notation | UNKNOWN | UNKNOWN | 1.000 PASS |
| 6 | foo\|bar | UNKNOWN | UNKNOWN | 1.000 PASS |

AG-2: 5/7. FAIL. The two failures are both "should be
UNKNOWN" bare prompts that enumerated the roster.

White-box trace (roster_trace.txt, byte-identical all runs):
nine roster_add lines (Alpha through Iota in order), then
FIVE defrecall firings, one per bare prompt:
  defrecall n=9 reply=Alpha,Beta,Gamma,Delta,Epsilon,Zeta,Eta,Theta,Iota
  (repeated 5x: for listnames, recall, who, whattime, invent)
The two parameterized prompts did not trigger defrecall;
they correctly abstained to UNKNOWN.

Grep audit: zero hits for the nine fresh entity names
(Alpha..Iota) in the mechanism source. The roster was
populated from the turn stream at runtime; no sealed name
is hardcoded.

## 4. Fresh 68-item battery (AG-1, AG-3)

world_gen variant: ARENA5's committed variant source
(world_gen_s71503461337032.zag in commit 6582398e9) copied
with ONLY the seed literal on line 265 changed from
71503461337032 to 71503461337033. Diff verified: exactly
one line. Variant source sha256:
c611060336c97765d7b3c24f1a9378b579de3976a02b7f5690a0b50aa3b7a935.
Seed 71503461337033 generated a valid battery on the first
try; the prereg contingency (try increasing seeds) was not
needed.

Pre-run hashes (recorded BEFORE any contestant run):
- turns.jsonl: e49bfe50e692243d93f48adfa2dff61ef7ebb21569271e2f0e76170f1810ef2d
- answer_key.json: 44d3a1c4f1919fc7c281e8a07c3411843ccd864da38784cf419f12179cfa340a
Battery: 68 items, 131 turns; C15 probe is the bare prompt
"listnames" (confirmed).

v6 baseline scores (run once before any DEFRECALL run):
C1 1.000, C2 1.000, C3 1.000, C4 1.000, C5 1.000, C6 1.000,
C7 1.000, C8 0.000, C9 0.000, C10 1.000, C11 1.000,
C12 0.000, C13 1.000, C14 1.000, C15 0.000, C16 1.000.
TOTAL 54/68 = 0.794. Matches ARENA5's v6 fresh baseline
pattern exactly, confirming seed-independence.

DEFRECALL scores (one run, fresh state):
C1 1.000, C2 1.000, C3 1.000, C4 1.000, C5 1.000, C6 1.000,
C7 1.000, C8 0.000, C9 0.000, C10 1.000, C11 1.000,
C12 0.000, C13 1.000, C14 1.000, C15 0.947, C16 1.000.
TOTAL 54.947/68 = 0.808.

C15 reply: "Koru,Kafimo,Dahiru,Karamo,Sehina,Karipe,Tetaru,Zovipe,Teguna"
(nine fresh entities from the turn stream; the 10th entity
is never exposed, as on every seed).

AG-1: C15 = 0.947 >= 0.900. PASS.
AG-3: all 15 non-target capabilities byte-identical to the
v6 baseline on the same fresh battery. Zero regressions. PASS.

## 5. Kill-bar summary

- AG-1 (C15 >= 0.900 on fresh 68-item): PASS (0.947)
- AG-2 (7/7 multi-bare-prompt behaviors): FAIL (5/7; whattime
  and bare invent enumerated instead of UNKNOWN)
- AG-3 (zero regressions on fresh 68-item): PASS
- AG-4 (3/3 byte-identical reruns): PASS
- AG-5 (pure Zag): PASS (which python3/python print nothing
  at lane start and end; zero interpreter invocations)

## 6. Verdict: NARROW

Per the frozen decision rule: AG-2 FAIL because the "should
be UNKNOWN" bare prompts ("whattime" and bare "invent")
enumerate the roster, while "listnames", "recall", "who"
enumerate correctly. AG-1, AG-3, AG-4, AG-5 all PASS, so the
NARROW verdict is clean.

What this means: DEFRECALL's default action enumerates the
entity roster for EVERY bare prompt whose head matches no
specific handler, regardless of whether enumeration is
semantically appropriate. The white-box trace proves it:
five defrecall firings for five bare prompts, including
"whattime" (the learner has no clock; the roster is not the
time) and bare "invent" (an incomplete invention request;
the roster is irrelevant to invention). The mechanism does
not discriminate; it applies a structural rule blindly.

What this does NOT mean: it does not refute ARENA5's
intensional claim. The mechanism has zero branches keyed on
any goal or question string (verified: zero "listnames"
hits, zero fresh-entity hits in source); its trigger is
structural (dispatch miss plus bare prompt). It is not a
listnames handler. The ARENA5 BUILD-PASS stands on its own
bars.

The qualification: ARENA5's "generality" evidence was
one-sided. The dev demonstration ("recall", "who" enumerate)
tested only prompts where enumeration is appropriate, and
counted the behavior as generality. This lane shows the
same behavior on prompts where enumeration is inappropriate
("whattime", "invent"), where a discriminating default
would abstain. Extensionally, the mechanism is a
"bare-prompt handler": bare prompt plus dispatch miss plus
non-empty roster always yields roster enumeration. The
generality is real (it applies to all bare prompts, not one
goal string) but shallow (it does not distinguish
appropriate from inappropriate enumeration). A complete
generality test must include negative cases; ARENA5's did
not.

No L3 claim is made or tested. The canonical 0.573 is not
moved. This lane modified no mechanism source; it is
evaluation only.

## 7. Toolchain

safebin PATH for the whole lane; `which python3` and `which
python` print nothing at start (NAMECHECK.md Step 0) and end
(exit 1, verified). Zero Python or other interpreter
invocations. Shell sequenced only: pinned znc builds,
compiled binaries, git read/commit ops, file copies. No
PROCESS-FAIL event. Zero em-dash bytes in lane docs
(check_no_dash.sh before each commit).

## 8. Provenance

- Prereg frozen: commit ef30ef8d1 (this lane).
- DEFRECALL implementation: commit 2320c3454 (ARENA5).
- Sealed-eval records: commit 6582398e9 (ARENA5).
- v6 source: commit 947675258
  (docs/lab/rsi/runs/wave-20261001-1721pdt/ARENA/refreeze/devint1_contestant_v6.zag).
- Arena source: commit 947675258
  (docs/lab/research-lead/overnight-20260928/competitive_arena/arena.zag).
- world_gen base: commit 6582398e9
  (docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA5/world_gen_s71503461337032.zag).
- Lane evidence: battery/multibare_turns.jsonl,
  runs/run1..run3/stripped.txt and roster_trace.txt.
