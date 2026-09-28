# DESIGN — ledger-gating: `il_check` as the commit gate for the hypothesis-state substrate

Date: 2026-09-19. Wave-5 investigator, slug `ledger-gating`.
Preregistered in PREREG.md (written before this file's implementation
section was acted on; the design below is the preregistered mechanism).

## 1. What is being wired to what

- **The substrate** (`hss.zag`, wave-3, byte-identical): hypotheses are
  slots with defining-claim bitmasks; observations refute by direct
  contradiction; commit iff exactly one hypothesis is active. Its claim
  path is `hss_commit`.
- **The checker** (`il_core.zag`, wave-4, byte-identical): `il_check`
  over an append-only ledger; fires on ledger contradiction,
  empty/phantom/trivial provenance, cheat-jumps; silent on honest
  chains (24/24).
- **The gate** (`lg.zag`, new): the claim path. A hypothesis may commit
  only when `il_check` passes on its evidence chain. A failed check
  blocks the commit and routes to audited HOLD — never a silent drop.

## 2. The evidence-chain mapping (HSS events → IL ledger ops)

Item `Q` = the problem id (which question is being answered). The claim
is always `CLAIM(Q, s)` = "slot `s` is the sole surviving hypothesis for
`Q`".

| HSS / driver event | IL ledger entry | Role in the chain |
|---|---|---|
| `hss_observe(index, bit)` (driver-recorded) | `OBSERVE(Q, index*2+bit)` | raw reading; audited, **uncited** by the claim |
| rival slot `r` refuted by the observation | `REFUTE(Q, r)` | evidence refuting value `r` for `Q` (wave-4 `REFUTE(item,val)` semantics); **cited** (first two) |
| sole survivor `s` emerges | `HYP(Q, s)` | deliberate hypothesis "slot `s` answers `Q`", formed at elimination; **cited** |
| gate runs the check | `VERIFY(Q, s)` | deliberate verification = the sole-survivor check itself; **cited** |
| gate states the claim | `CLAIM(Q, s, [ref_a, ref_b, hyp, ver])` | the stated claim; checked by `il_check` |

Why the claim cites the **elimination record** rather than the raw
readings: the claim "s is the sole survivor" is evidenced by what
eliminated the rivals (the REFUTEs), the deliberate hypothesis, and the
verification. Raw readings are one level down — the material *behind*
the refutations. This mirrors wave-4 S6, where the eliminative route
passes rule 6 via cited REFUTEs. Rule-by-rule, for an honest chain:

- Rule 1 (empty): 4 citations. Rule 2 (phantom): all indices `< head`.
  Rule 3 (trivial): all four are evidence-grade (REFUTE/HYP/VERIFY).
- Rule 4 (cited contradiction): cited `REFUTE(Q,r)` has `r ≠ s`;
  cited `HYP(Q,s)`/`VERIFY(Q,s)` have `v == s`. No OBSERVE is cited, so
  the OBSERVE-supersession sub-rule never engages — by construction,
  not by luck.
- Rule 5 (committed contradiction): the `VERIFY(Q,s)` appended by the
  gate is the latest `VERIFY(Q,*)` before the claim. ✓
- Rule 6 (chain shape): ≥1 cited REFUTE on `Q` precedes the cited
  `HYP(Q,s)` (elimination genuinely precedes the judgment). ✓

## 3. The gate function

```
// The system's ONLY commit op. Returns LG_OK (committed) or
// LG_BLOCKED_<v> (blocked; HOLD audited with aux = 1000+v).
fn lg_attempt_commit(active, capacity, committed, step, abuf, acount,
                     il, item, ref_a, ref_b) i32
```

1. Scan `active[]`. If the survivor count ≠ 1 → delegate to `hss_commit`
   (the ordinary HOLD path; the gate has nothing to check because there
   is no claim).
2. Sole survivor `s`: append `HYP(Q,s)`, `VERIFY(Q,s)`,
   `CLAIM(Q,s,[ref_a,ref_b,hyp_idx,ver_idx])`. If any append hits
   `IL_AUDIT_FULL` → fail closed: HOLD with `aux = 1999`, no commit.
3. `v = il_check(il, claim_idx)`.
4. `v == IL_OK` → `hss_commit(...)` (COMMIT audited, `committed = s`).
5. `v != IL_OK` → **blocked**: `hss_commit` is NOT called, `committed`
   untouched, one `HOLD` audit entry with `aux = 1000 + v`. The blocked
   CLAIM stays in the ledger as evidence of the attempt.

Cheat probes use the lower boundary directly: `lg_claim_and_check`
(appends a CLAIM with adversary-chosen provenance, returns the
verdict) + `lg_block` (audits the HOLD). The adversary controls the
chain; the check-then-HOLD routing is what blocks them.

## 4. HOLD encoding (audited, never silent)

- Ordinary HOLD (non-uniqueness / empty): `HOLD` audit entry,
  `aux` = active count (substrate behavior, unchanged).
- Gate-block HOLD: `HOLD` audit entry, `aux = 1000 + v` where `v` is the
  `il_check` verdict (1101–1106 for the six violation codes).
- Chain-construction failure (ledger full): `aux = 1999`, fail closed.
Every failed check therefore leaves exactly one auditable HOLD whose
`aux` names the violated rule. No path drops a failed check silently.

## 5. Belief revision under the gate

Only `VERIFY` commits belief (wave-4 law, preserved). Revision works
because `il_check` rule 5 tracks the **latest** `VERIFY(Q,*)`:

- Episode A verifies `Q → s1` (committed). Episode B refutes `s1`
  (HSS UNCOMMIT; ledger `REFUTE(Q,s1)`), re-eliminates, verifies
  `Q → s2`. The new claim cites the new chain; rule 5 sees the fresh
  `VERIFY(Q,s2)` → `IL_OK`. The gate permits the revision.
- A stale `CLAIM(Q,s1)` citing episode A's chain hits rule 5: latest
  `VERIFY(Q,*)` is `v=s2 ≠ s1` → `IL_LIE_COMMITTED` → blocked. The gate
  refuses to smuggle the old belief back.
- Outgrown raw readings: old `OBSERVE(Q,·)` entries uncited by a new
  claim are invisible to every rule (rules 4–6 scan cited entries;
  rule 5 scans VERIFYs only). The gate stays silent — the wave-4 S8
  principle survives gating. Every honest episode deliberately contains
  an outgrown noisy reading to prove this continuously.

## 6. Where the gate and the eliminative logic can disagree

The eliminative logic says "sole survivor → commit". The gate says
"commit only if `il_check` passes". Disagreements are exactly the
events "sole survivor exists ∧ gate blocks", each adjudicated from the
ledger by its verdict code + cited-entry dump:

- B1 `IL_LIE_CITED`: the cited VERIFY's recorded val differs from the
  claim — the ledger shows the contradiction directly.
- B2 `IL_CHEAT_PHANTOM`: a cited index ≥ head — the ledger shows the
  head; the citation points past it.
- B3 `IL_CHEAT_EMPTY` / `IL_CHEAT_NOSHAPE`: no (or no genuine) chain —
  the claim entry's provenance slots are empty / evidence-free.
- B4 `IL_CHEAT_TRIVIAL`: the cited entry's op is CLAIM/REFUSED —
  the ledger shows the non-evidence op.
- B5/B6 and the C2 stale probe `IL_LIE_COMMITTED` / `IL_LIE_CITED`:
  the ledger's latest VERIFY / cited REFUTE contradicts the claim.

The reverse disagreement (gate passes ∧ substrate holds) cannot occur:
the gate only fires on a sole survivor. Every disagreement is therefore
a block of something the substrate would have committed — the integrity
layer doing its job — and the ledger says exactly why.

## 7. Structural trust assumptions (stated, not hidden)

- The gate trusts the driver's ledger writes (honest-ledger assumption,
  inherited from wave-4; forgery is out of scope).
- The integrity claim is conditional on the claim path going through
  the gate: in the trial the driver can still call `hss_commit`
  directly; a deployed wiring makes `hss_commit` gate-internal.
- Provenance width 4 (inherited): episodes with >2 rivals cite the
  first two REFUTEs; rule 6 needs evidence + judgment, not the full
  forensic trail (wave-4 honest boundary #6).
- Re-verification amnesty (inherited): a later `VERIFY(Q,v')`
  supersedes an earlier `VERIFY(Q,v)` without the checker asking why.
  Making VERIFY cite its superseding evidence is the wave-4-recommended
  follow-up, out of scope here.

## 8. Scale dimension (program law)

Per-gate cost: one `il_check` = O(provenance × head) worst case,
O(provenance + head-scan-for-latest-VERIFY) in practice; provenance ≤ 4
is constant. Per-commit work adds one O(capacity) survivor scan.
The shared-ledger leg (A2, 90 entries, 10 sequential claims on one
item) is the mini-scale demonstration: rule-5 tracking stays exact
across claims. 100x ledgers change nothing structurally — the check is
per-claim with no cross-claim accumulators. The binding scale
constraints remain the ones wave-3/4 stated (hypothesis generation,
audit-segment sealing), not the gate.
