# Graded refutation — mechanism design

Investigator: Wave-5, slug `differentiation-robustness`, part (a).
Date: 2026-09-19. Status: PROPOSED (preregistered in PREREG.md, untested
at time of writing).

This design attacks wave-4 differentiation boundary #4
("refutation is all-or-nothing within a session ... brittle to a single
mis-extracted evidence event"). It replaces instant elimination with
**explicit, ledgered uncertainty**: person-hypotheses carry doubt
records, and refutation requires *corroborated* contradiction.

## 1. The honest tension, stated first

Wave-4's law was "judgment, not scoring": no weights, no thresholds, the
commit rule was pure logic (exactly one survivor). Graded refutation
cannot be built without *some* aggregation rule — making refutation
non-atomic requires deciding when accumulated contradiction is enough.
This design therefore introduces, deliberately and preregistered:

- a fixed per-kind reliability map (KIND_RELIABILITY, §3),
- one fixed integer bound (DOUBT_LIMIT = 4, §4).

These are not learned, not adaptive, not tuned per episode: they are
constants, audited everywhere they are used, identical in replay. The
COMMIT rule itself stays pure logic (exactly one *clean* survivor, §5).
What changed is the *elimination* path, which now carries explicit
uncertainty instead of pretending every evidence event is infallible.
The alternative — keeping all-or-nothing — is what the poisoning trial
(G3) shows to be gullible.

## 2. Person hypotheses with doubt

```
person[i]: { id, must1, must0, active, refuted,
             doubt:i32,            // weighted sum of contradiction reliabilities
             doc:i32,              // raw count of contradiction events
             kmask:u8 }            // bitmask of evidence kinds that contradicted
```

`must1`/`must0` are unchanged (defining evidence claims). `doubt`,
`doc`, `kmask` are the explicit uncertainty. Every contradiction appends
a ledgered **DOUBT record**:

```
DOUBT entry: (person_id, bit, rc=OK, rel, kind, obs_step)
```

citing the observation's ledger step. Doubt is never silent: the trial's
judgment printer derives all doubt records from the audit, and a person
with doubt > 0 can never be committed (§5).

## 3. Per-event reliability (KIND_RELIABILITY)

Each evidence event carries `(bit, value, kind)` and a per-event
reliability `rel ∈ {1,2,3}`. The extractor (part b) assigns reliability;
the mechanism trusts the tag (the trust boundary is explicit — §7).
The default map, preregistered and fixed:

| kind | meaning                          | rel | rationale (preregistered, not derived) |
|------|----------------------------------|-----|----------------------------------------|
| 0    | name claim ("i am alice")        | 2   | deliberate but cheap to utter          |
| 1    | secret demonstration (verbatim)  | 3   | exclusive knowledge, hardest to fake  |
| 2    | episode recall / behavioral mark | 2   | provenance-grade, medium strength      |
| 3    | fact assertion                   | 1   | public content, weakest signal         |

The extractor may *downgrade* one level on hedging ("maybe", "i think",
...) to a floor of 1. Reliability is never upgraded.

## 4. The graded observe rule (the only elimination path)

On evidence event `(bit, value, kind, rel)`, for each active,
non-refuted person p:

```
expected = bit ∈ must1 ? 1 : (bit ∈ must0 ? 0 : none)
if expected != none && value != expected:
    append DOUBT(p, bit, rel, kind, obs_step)   // ledgered
    p.doubt += rel; p.doc += 1; p.kmask |= (1<<kind)
    if p.doubt >= DOUBT_LIMIT(4) AND popcount(p.kmask) >= 2:
        REFUTE p (ledgered, permanent within session)
else: consistent (no state change)
```

**Refutation requires corroborated contradiction**: enough accumulated
doubt (≥ 4) **and** contradiction from **≥ 2 distinct evidence kinds**.
Since max single-event reliability is 3, **no single event can ever
refute** — the brittleness boundary is addressed uniformly, with no
carve-outs for "strong" channels. Two same-kind contradictions (2+2=4,
one kind) do NOT refute: corroboration means independent channels, not
repetition (trialed in G7).

## 5. The graded commit rule (sticky doubt)

```
// GCOMMIT-REGION — sees only active/refuted flags, doubt, ids.
// Never references must1/must0 (runner statically checks).
if exactly one active non-refuted survivor AND survivor.doubt == 0:
    COMMIT to that speaker (audited, judgment cites DOUBT+REFUTE records)
else:
    HOLD -> committed = UNKNOWN (audited)
```

Any unresolved doubt blocks attribution. A session where the true
speaker accumulated even 1 doubt abstains rather than attributes. This is
the "tolerance must not become gullibility" clause: the graded scheme
trades decisiveness for safety — doubt is sticky within a session, and
exoneration is a new session (same as wave-4's no-revival rule, now
extended from refutation to doubt).

## 6. Worked examples (predictions; trialed in PREREG G1–G3)

Masks (bits 0..10; 8=alice signoff, 9=bob catchphrase, 10=carol "hmm."):
- ALICE must1={0,3,5,6,8}=361, must0={1,2,4,7,9,10}=1686
- BOB   must1={1,4,5,9}=562,   must0={0,2,3,6,7,8,10}=1485
- CAROL must1={2,7,10}=1156,   must0={0,1,3,4,5,6,8,9}=891

**G2 — impostor trap (Alice's name + Bob's secret):**
`(0,1,k0,r2)`: BOB doubt 2 {k0}, CAROL doubt 2 {k0}. ALICE consistent.
`(4,1,k1,r3)`: ALICE doubt 3 {k1} (secret S_B is must0 for her);
CAROL doubt 2+3=5 {k0,k1} → REFUTED. BOB consistent (his secret).
Survivors: ALICE (doubt 3), BOB (doubt 2) → 2 survivors → HOLD →
UNKNOWN, zero slots created. The trap still resolves to UNKNOWN —
tolerance did not become gullibility. (Note: under graded, the trap
yields "ambiguous with doubt on everyone" rather than wave-4's
"everyone refuted"; both map to the same fail-safe.)

**G3 — single-event poisoning (the wave-4 gullibility case):**
`(1,0,k0,r2)` "not bob": BOB doubt 2 {k0}; ALICE and CAROL consistent.
`(5,0,k3,r1)` poisoned "fact K denied": ALICE doubt 1 {k3} (fact K is
must1 for her); BOB doubt 2+1=3 {k0,k3}; CAROL consistent (must0).
Nobody refuted; 3 survivors → HOLD → UNKNOWN.
Under wave-4 the same bit sequence refutes BOB, then ALICE — leaving
exactly CAROL → **COMMIT CAROL** (misattribution on one poisoned
event). The graded scheme absorbs the poison and abstains. The wave-4
baseline is run natively as a comparative check (w4baseline.zag), labeled
as a NEW adversarial criterion, not a wave-4 prereg failure.

## 7. Trust boundaries and honest limitations

- **The mechanism trusts the event's reliability tag.** Assigning
  reliability is the extractor's job (part b). A lying extractor can
  inject doubt=3 per event — still never a single-event refutation, and
  sticky doubt still forces abstain, never misattribution. The tag is
  audited per event so a bad tagger is visible in the ledger.
- **Hard-channel trust is not eliminated, only bounded.** A
  mis-extracted kind-1 event injects 3 doubt; the system tolerates it
  (abstains via sticky doubt) rather than dying from it.
- **No within-session exoneration.** Doubt only grows; a session reset
  clears it. Same shape as wave-4's no-revival rule.
- **Kind-diversity is a design choice, not a theorem.** Two
  same-channel contradictions (r2+r2) do not refute here; whether
  repetition should corroborate is an open question, recorded not
  resolved.
- **The DOUBT_LIMIT=4 constant is preregistered, not derived.** Its
  justification is structural: it is the smallest integer strictly
  greater than max single-event reliability (3), which is exactly the
  "no single event refutes" property. Any larger value would demand more
  corroboration at the cost of decisiveness; that tradeoff is not
  trialed here.
- Partitions, memory ops, audit substrate, and replay discipline are
  inherited from wave-4 unchanged in shape (field names prefixed
  `gdiff_`).
