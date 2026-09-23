# TRIAL RESULTS — differentiation (Phase 4, experimental)

Date: 2026-09-19. Runner: `run_diff.sh`. Sources: `diff.zag` (mechanism),
`diff_trial.zag` (driver). Evidence: `evidence_run1.txt`,
`evidence_run2.txt`, `evidence_compile.txt`.

## Runner verdict

**ALL RUNNER CHECKS PASS.** 73/73 DIFF_CHECK lines match; DIFF_FAILURES=0;
two runs byte-identical (sha256
`082f37dfba87c816ddc25e7d736028da1a979dbdfb88e1ea16218de5e79c7240`);
no-RNG static check clean; commit-region exclusion check clean
(commit references no evidence masks, no confirmation counters);
judgment shape 3/6/3 (judgments / refutation citations / UNKNOWNs).

## Prereg criterion disposition (PREREG.md F1–F8)

| Criterion | Result | Key evidence |
|---|---|---|
| F1 identification as judgment | PASS | E1: `(0,1)` refutes BOB+CAROL; commit ALICE; judgment cites both REFUTE entries with entry numbers, bits, values (`e1_refute_bob=1`, `e1_refute_carol=1`, `e1_refute_alice=0`) |
| F2 impostor fail-safe | PASS | E3: name-ALICE + secret-BOB refutes all three; HOLD; `committed=UNKNOWN`; `mem_add → REFUSED_UNKNOWN`; live-slot count unchanged |
| F3 no-evidence abstain | PASS | E4: shared fact K only → 2 survivors → HOLD, UNKNOWN, add refused |
| F4 per-person formation + isolation | PASS | E2+E6: `(100,7)` owner=ALICE, `(100,9)` owner=BOB coexist; `knows(100,ALICE)=7`, `knows(100,BOB)=9`, `knows(100,CAROL)=NOTFOUND`; cross-partition kill → REFUSED_SCOPE; CORE kill → REFUSED_CORE; own-partition kill → OK and only that partition's copy disappears |
| F5 confusion adversarial | PASS | E5: shared content refuted only CAROL (never taught K); provenance `(6,1)` refuted BOB; commit ALICE with honest attribution checks; E5b: shared content alone → HOLD/abstain |
| F6 determinism + replay | PASS | byte-identical reruns; `diff_replay` reconstructs committed speaker, clock, person flags, all slot fields, entry count exactly — over all 6 main episodes (E8) and the scale episode (E7) |
| F7 zero RNG | PASS | static grep clean over both sources |
| F8 two→three speakers + scale | PASS | two-person confusions (E1/E5/E6), three-person episodes (E3/E4), 100-person scale: two observations leave exactly person 57; entries 202 ≤ 464 bound; replay exact |

## What the judgments actually look like

E1: `DIFF_JUDGMENT,person=1,survivors=1` +
`REFUTED,person=2,by_entry=4,obs_bit=0,obs_val=1` +
`REFUTED,person=3,by_entry=4,obs_bit=0,obs_val=1` +
`CONSISTENT,person=1,observes=1`.

E5 (the confusion case): `person=1` +
`REFUTED,person=3,by_entry=17,obs_bit=5,obs_val=1` (shared content) +
`REFUTED,person=2,by_entry=18,obs_bit=6,obs_val=1` (provenance) — the
judgment names which evidence did the discriminating work, derived from
the audit, not from hidden state.

UNKNOWNs: `survivors=-1` (impostor, everyone refuted), `survivors=2`
twice (ambiguity abstentions). Explicit, never a guess.

## Honest notes

- The trial's evidence events are harness-supplied `(bit, value)` pairs.
  The judgment machinery is tested; evidence *extraction* from raw
  conversation is not (see BOUNDARIES.md).
- `must0`-complement in the scale episode is a strong exclusivity
  assumption; the hand-designed episodes use explicit exclusive bits
  (names, secrets, provenance), which is the realistic shape.
- The replay skips REFUTE entries because they are deterministic
  consequences of OBSERVE — re-derived, not re-read. This is documented
  in `diff.zag`, not hidden.
- Refutation is permanent within a session; only `SPK_SESSION_RESET`
  re-activates. There is no graded "maybe" — a deliberate design choice
  (judgment, not scoring), but it means one contradictory observation
  kills a hypothesis even if later evidence would exonerate. The
  exoneration path is a new session, not a revival.
