# L3B v2 robustness: result

Target: L3B constructor v2 (7a1d3265d, L3B-V2-PASS). Adversary findings
addressed: ambiguous dispatch by silent first-match, and archive
exhaustion panic (5be03c94f, run 2 BOUNDED).

Prereg PREREG_L3B_V2_ROBUST.md frozen alone at 92c73aeca, strictly
before this implementation. Pure Zag + POSIX shell. Contaminated paper
untouched.

## Verdict: L3B-V2-ROBUST-PASS

Harness run_robust.sh exits 0. All 17 mechanism bars plus all 7 audit
bars pass, 3/3 byte-identical, exit code 0 on all runs.

## Mechanism

Two bounded changes to the frozen-menu constructor; the 205-program
grammar and the base interpreter are sha256-identical to v2.

1. Ambiguity representation. try_dispatch now collects ALL archived
   versions matching a probe instead of returning the first match. On
   2 or more matches it writes an explicit ambiguity record to learner
   state (probe n in am_n, match count in am_c, matching serials in
   am_ser, chosen serial in am_w) and resolves by the generic policy
   most-recently-constructed (max serial). A TRACE-AMBIGUOUS line is
   emitted; silent first-match is never used. The single-match path is
   byte-for-byte the v2 behavior.

2. Archive-exhaustion discipline. do_fire refuses a 9th-version
   archive write with an explicit learner-observable TRACE-ARCHIVE-FULL
   signal, an event counter (cnt cell 11), and a persistent status
   latch (g cell 5). No panic, no eviction, no silent corruption.

## Evidence

- A2 reproduction: TABLE n=205, hidden 3/3, quadfound=1, interp e=25
  (RB-F1a..d PASS).
- B2 reproduction: creates=2, dispatches=2, archive keys
  V,(A,V,V) and V,(A,V,C4), hidden=3 switch=2 final=1, recallok=2/2
  (RB-F2a..d PASS).
- AMB (adversary Family C probes): creates=3; reactivation
  from=3 to=2 on=21; then `TRACE-AMBIGUOUS on=6 matches=2 chosen=3
  policy=most-recent` followed by dispatch from=2 to=3 on=6. The old
  wrong first-match pick (to=1 on=6) no longer occurs; the ambiguity
  record reads on=6 matches=2 chosen=3. Probes at n=7,8,9 are direct
  hits, no 4th version (RB-AMB1..5 PASS).
- ARCH (adversary Families D then E, one lifetime): creates=8;
  revisit `TRACE-DISPATCH from=8 to=1 on=21`, revisit tally=2;
  the 9th-version attempt emits `TRACE-ARCHIVE-FULL inst=5 ep=3`,
  creates stays 8, archfull events=1, latch=1, exit code 0
  (RB-ARCH1/2/3a/3b PASS).

## Kill bars

- K1 PASS: prereg 92c73aeca strictly precedes this implementation
  (merge-base verified).
- K2 PASS: the ambiguous probe emits an explicit ambiguity record and
  resolves by policy (chosen=3, not first-match), 3/3; the 9th version
  is refused without panic, 3/3, exit 0.
- K3 PASS: grammar region sha256 727a0c2a identical to v2;
  interpreter region sha256 aee8090b identical to v2; zero new
  semantic cases, modes, bridges, or handlers (harness audits);
  pure Zag; shell-only dash check passes on all lane files.

## ONE-SYSTEM RULE accounting

- Cognition source lines added: ~+110 (ambiguity two-pass, record,
  archive guard, state; plus the rb_step harness wrapper).
- New hardcoded semantic cases: 0.
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 0.
- Learner-state structures created: am_ser(8), am_n(1), am_c(1),
  am_w(1); cnt cells 10 (ambiguity events), 11 (archive-full events);
  g cell 5 (archive-full latch).
- Capability-source delta: small and bounded; no grammar change.

## Ceiling and next step

Bounded L2, unchanged from v2. The menu is still finite (205 programs);
menu-exhaustion behavior is unchanged. These fixes make the frozen-menu
mechanism robust but do not constitute incremental construction. The
incremental-construction redesign remains a separate research program
per the standing lane ruling.
