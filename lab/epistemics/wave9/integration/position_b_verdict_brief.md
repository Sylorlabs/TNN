# INT-1 C5-Redesign Council — Verdict Brief, Position B: Verdict-Aware Composition

## 1. Exact design

**Tag propagation.** At compose time, `seam4_compose` queries every backing claim's O2 verdict
(CONFIRMED=4 / OPEN=0 / SUSPECT=9 / REFUTED=5) and computes a **composite verdict flag**:
REFUTED-bit = OR over backing REFUTEDs; SUSPECT-bit = OR over backing SUSPECTs. Alongside the
flag, the composite record stores a **per-trace verdict vector** (fixed cap, claim-id + verdict
code pairs — deterministic, no allocation games). The flag is the fast consumer signal; the
vector is what the checker recomputes. O4's trace arrays gain two tag columns; the COMPOSE
ledger entry gains the flag in `b1` and a follow-on `LG_OP_COMPOSE_TAG` entry carrying the
vector (the 16-word entry layout has no room).

**Where it lives.** The tag computation lives in the seam (like `c5_strict`), never in O4 — the
same trust boundary the repair already established. O4 stays verdict-blind; the seam attaches
the verdict.

**Refusal condition (operational).** Define `SILENT(t)` for any composite `t` with rc=0: let
`B(t)` = backing claims ledgered at compose time, `V(c, ep)` = O2 verdict of `c` at the compose
episode. `SILENT(t)` iff ∃c ∈ B(t) with V(c, ep)=REFUTED **and** t's stored flag lacks the
REFUTED-bit. `seam4_compose` computes the flag itself, so silence can only occur if the tag-write
path is lesioned or bypassed — and the seam refuses (new code `SEAM_REFUSED_SILENT`) any compose
that would emit rc=0 with a flag/vector mismatch, verified by re-reading the written tag before
returning. "Silent inclusion" = a successful composite whose own record denies refuted backing;
it is a ledger-checkable predicate, not a vibe.

## 2. The hard case: deliberate composition OF refuted material

This is where B beats strict-refusal. MA3 taught us the cost of not being able to think about
what's wrong: it lost the adversarial curriculum precisely because it could not express negative
judgments about memories. Deliberate counterfactual work — "explain why claim 7 is wrong,"
"compose the refuted chain to show the flaw," the false-knowledge TNN revising 18 false claims
through deliberate representation — *requires* refuted material as first-class input.

Mechanism, precisely: a compose may declare intent `EXPLAIN` with a cited claim id. The
composite is produced, tagged REFUTED-bit=1, and its vector names the refuted claims. It may be
*served to the learner* (apply path) and *shown*. It may **never** back a CONSOLIDATE candidacy
(O3's gate rejects any candidate whose verdict-vector has REFUTED-bit=1 — a static, checkable
rule) and may never be cited as CONFIRM evidence (O2's evidence-citation path checks the flag).
The quarantine is enforced at consumption, not at production. Explaining a refutation is then
allowed, first-class, and auditable; smuggling one into the trusted path is a checkable
violation.

## 3. The C5 bar under B — falsifiable

Re-run criterion for the killed-only arm:

- **≥1 composite with REFUTED-bit=1** (the arm was exercised, not starved — no
  unfalsifiable-pass).
- **0 SILENT composites**, where the independent checker verifies on the ledger alone: for every
  COMPOSE/APPLY/CONSOLIDATE entry with rc=0, read the verdict vector, replay O2's VERDICT
  entries to reconstruct V(c, ep_compose), recompute the flag, and compare. Any mismatch →
  SILENT → FAIL.
- **0 quarantine breaches**: no EXPLAIN-flagged composite appears as CONSOLIDATE backing or
  CONFIRM-cited evidence. Checker-verified from ledger linkage.
- **Positive control**: a variant with the tag-write path lesioned (tags dropped) MUST produce
  SILENT>0 and trip the checker; a variant marking everything EXPLAIN MUST trip the quarantine
  check. If either fails to fire, the instrument is re-blocked, not passed.

## 4. Capability impact

- **C2**: untouched — O4 still composes; the gate is a pre-check in the same seam slot as
  `c5_strict`. Verification-at-compose (G4) is orthogonal to tagging.
- **Stage gates**: DC-2/DC-4 composite-verification rates count tagged composites as composites;
  tagging never bypasses verification. The P4 race probe (M5) is *strengthened*: the verdict
  vector gives the probe a precomputed backing set instead of a claim-pointer hunt, and a
  post-compose REFUTE of a backing claim is detectable as vector-drift (REFUTED is terminal —
  `o2_observe` — so drift is monotonic and checkable).
- **P1–P10**: P5 (verdict rot) gains an observable — refuted-tagged composites still served ≥5
  episodes post-REFUTE are now nameable, not inferable. P7 unaffected.
- **New-machinery risk**: the flag is cheap (one `o2_verdict` query per backing claim, pure
  function). The vector is storage per trace and a new ledger op. The gameable surface is the
  EXPLAIN intent flag — mitigated only by the quarantine rule holding at O2/O3, which pushes
  enforcement one hop downstream. If O3's gate doesn't reject REFUTED-bit candidates, the tag is
  decorative: **B's guarantee is exactly as strong as its downstream consumers.**

## 5. Falsification of B

- **Laundering through multi-hop**: composite A (REFUTED-tagged) → input to composite B → B's
  tag drops the bit. Falsified if trace→tag lineage can't be ledgered: `o4_compose` today takes
  `need_id`, not an input-trace list, and the COMPOSE entry names only `claim_cid` in `a1` —
  multi-hop tag propagation is *uncomputable* in the current seam signature without listing
  inputs. If input listing can't be added within the 16-word budget, min-verdict transitively is
  a slogan, not a mechanism, and B fails on its own terms.
- **Checker unverifiability**: if V(c, ep) can't be reconstructed (verdict entries incomplete),
  "tags propagate" is vibe. The ledger already records VERDICT entries with episodes, so this
  is believed-checkable — but must be demonstrated, not assumed.
- **Behavioral**: killed-only arm yields 0 tagged composites (starvation) or the tag-lesioned
  positive control fails to trip the checker.

## 6. Honest weaknesses

**Laundering, answered straight.** If composite A becomes input to composite B, the tag survives
only if (a) B's compose ledgers A's trace id and tag, and (b) tag(B) = min(tag(A), fresh
backing). Min-verdict propagates transitively — that is my answer. The cost: every compose needs
its input list (seam signature change), O4 trace records need tag columns, composites of
composites are *permanently tainted* (REFUTED is terminal in O2, so taint can never wash by
verdict change — only by rebuilding from scratch), and the quarantined pool grows monotonically.
One wrong REFUTE permanently poisons every composite downstream of it. Position A (strict
refusal) pays this cost too, but only at compose time; B pays it forever in storage and pool
shrinkage. This is the real price of my position.

**Second weakness: complexity of the trusted surface.** A's guarantee is one gate, one check
("refused all"). B's guarantee is a tag-write path, a vector store, a quarantine rule at O2, a
quarantine rule at O3, and a checker that replays verdicts. More moving parts = more places to
be subtly wrong, and the no-rescue rule cuts against me: B is *less* simple than strict. My
honest defense is only this: strict cannot do the job the program needs — a mind that cannot
deliberately compose refuted material cannot explain, cannot counterfactualize, and (MA3's
lesson) cannot win adversarially. A must either ban a load-bearing capability or leave it
untagged; the current intact path does the latter. B is the only position that keeps the
capability *and* makes its misuse checkable.
