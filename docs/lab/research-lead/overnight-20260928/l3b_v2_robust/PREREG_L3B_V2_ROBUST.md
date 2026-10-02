# PREREG: L3B v2 robustness (ambiguity representation + archive-exhaustion discipline)

Frozen before any implementation. Pure Zag + POSIX shell only. No Python at
any stage. Contaminated paper untouched.

## Step 0: name check

The standing rules at the top of the repo-root LOOP_STATE.md are: (1) PURE
ZAG ONLY, no Python anywhere in loop work, including glue, analysis,
verifiers, and harnesses; (2) fork testing, every local and remote
branch/fork enumerated and tested with the frozen battery every wave;
(3) the pure-Zag red line scope ruling, fixture provisioning counts as
loop work and is Zag-only; (4) shell-only byte checks via
worker_snippets/check_no_dash.sh, never python3. Rule (1) governs this
task directly: I write the mechanism, the run harness, and all audits in
pure Zag and POSIX shell, and I use the shell-only dash snippet for byte
checks. Rules (2) and (3) are honored by creating no forks and no
fixtures; rule (4) is honored per rule (1). I proceed only after this
paragraph is committed.

## Problem

L3B-V2-PASS (7a1d3265d) survived its independent adversary
(L3B-V2-ADV-BOUNDED, 5be03c94f), which documented two load-bearing
limitations of the frozen-menu constructor:

1. Ambiguous dispatch: when two archived versions explain a probe, the
   mechanism silently commits to the lowest-index match (first-match),
   with no ambiguity representation in learner state.
2. Archive exhaustion: the 9th distinct version against 8-entry archive
   arrays panics the znc runtime (slice index out of bounds, exit 1, 3/3
   identical). No guard, eviction policy, or error path exists.

The standing lane ruling forbids grammar expansion (no 500 or 5000 entry
menu) and assigns incremental construction to a separate research
program. This task is bounded engineering robustness on the frozen menu.

## Design (frozen)

### Ambiguity representation

When a single-failure dispatch probe matches two or more archived
versions (excluding the active one), the mechanism must:

- write an explicit ambiguity record into learner state: the probe n,
  the match count, the list of matching version serials, the chosen
  serial, and the policy name;
- resolve by a stated GENERIC policy, never silent first-match.

Policy: most-recently-constructed (max serial). Justification: recency
is a domain-independent rule; the newest version reflects the most
recent unexplained-failure evidence. It is not a per-case rule, and it
makes no reference to families A2/B2/C/D/E.

Trace on the ambiguity path:
`TRACE-AMBIGUOUS on=<n> matches=<k> chosen=<serial> policy=most-recent`
followed by the usual TRACE-DISPATCH line. Zero construction calls on
the ambiguity path, so recallok accounting is unchanged.

### Archive-exhaustion discipline

When do_fire must archive a genuinely new version and the archive is
full (8 versions), the mechanism must refuse with an explicit,
learner-observable signal:

- print `TRACE-ARCHIVE-FULL inst=<i> ep=<e>`;
- increment an archive-full event counter (cnt cell 11);
- latch a persistent learner-visible status flag (g cell 5 = 1).

No panic, no out-of-bounds write, no eviction. Justification: silent
eviction would destroy learned structure (cognitive amnesia); an
explicit observable refusal preserves all learned content and gives the
learner a signal it can observe. The discipline is a capacity guard,
not a semantic case.

### Frozen invariants

- The 205-program grammar (build_table and its key helpers) is
  byte-identical to 7a1d3265d. Verified by sha256 of the program-table
  region in both files.
- The base interpreter region (INTERP-BEGIN/END) is byte-identical to
  7a1d3265d.
- Zero new hardcoded semantic cases, zero new modes, zero new bridges,
  zero new task-specific handlers.
- New learner-state structures only: ambiguity record arrays
  am_ser(8)/am_n(1)/am_c(1), ambiguity event counter (cnt,10),
  archive-full event counter (cnt,11), archive-full latch (g,5).

## Frozen predictions

Family A2 (square residual), same steps as v2 FAM1:
- RB-F1a TABLE n=205; RB-F1b hidden 3/3; RB-F1c quadfound=1;
  RB-F1d interp e=25.

Family B2 (alternating regimes), same steps as v2 FAM2:
- RB-F2a creates=2, dispatches=2; RB-F2b archive keys
  V,(A,V,V) and V,(A,V,C4); RB-F2c hidden=3 switch=2 final=1;
  RB-F2d recallok=2/2.

Family AMB (adversary Family C steps, verbatim probes):
- RB-AMB1 creates=3; RB-AMB2 dispatches=2; RB-AMB3 ambiguity events=1;
- RB-AMB4 the ambiguity record reads on=6 matches=2 chosen=3
  policy=most-recent (the most recent version, serial 3, is chosen,
  NOT serial 1 by first-match);
- RB-AMB5 no 4th version is created; probes at n=7,8,9 are direct hits
  on serial 3 with no further dispatch.

Family ARCH (adversary Families D then E, same lifetime):
- RB-ARCH1 creates=8; RB-ARCH2 revisit dispatches once,
  `TRACE-DISPATCH from=8 to=1 on=21`, revisit tally=2;
- RB-ARCH3 the 9th-version attempt emits TRACE-ARCHIVE-FULL, creates
  stays 8, archive-full events=1, and the run exits with code 0.

Determinism: 3/3 byte-identical runs (RB-DET).

## Kill bars

- K1: this prereg committed alone strictly before any implementation.
- K2: the ambiguous probe no longer silently first-matches (explicit
  ambiguity record plus policy resolution, 3/3); the 9th version is
  handled without panic (3/3).
- K3: the 205-program grammar region is byte-identical to v2 (sha256
  diff); zero new semantic cases, modes, or bridges; pure Zag; the
  shell-only dash check passes on all lane files; contaminated paper
  untouched.
