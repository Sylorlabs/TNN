# PREREG — ledger-gating (Wave-5 investigator, slug `ledger-gating`)

**Status: preregistered 2026-09-19, BEFORE any implementation or trial
run.** No gate source has been written and no trial binary compiled at the
time of writing. Any deviation will be recorded as an amendment, not
silently absorbed.

## Question

Can the integrity-ledger checker (`il_check`, wave-4, 24/24) be wired as a
**gate on the hypothesis-state substrate's claim path** (wave-3,
commit-iff-exactly-one-survives) so that a hypothesis may commit **only**
when `il_check` passes on its evidence chain — with a failed check
blocking the commit and routing to an **audited HOLD** (never a silent
drop) — without punishing honest chains or legitimate belief revision?

## Mechanism under test (the gate)

New native Zag module `lg.zag` (imports the unmodified `il_core.zag` and
`hss.zag`; byte-identity of both verified in the runner). The claim path:

1. The driver records every evidence event to BOTH the HSS audit (via the
   real `hss_*` ops) and the IL ledger: each HSS observation
   `obs(index,bit)` → `OBSERVE(Q, index*2+bit)`; each refuted rival slot
   `r` → `REFUTE(Q, r)` (evidence refuting value `r` for item `Q` —
   wave-4 `REFUTE(item,val)` semantics).
2. `lg_attempt_commit(...)` is the system's ONLY commit op:
   - Count active slots. If ≠ 1 → plain `hss_commit` (standard HOLD path,
     unchanged).
   - If exactly one survivor `s`: append `HYP(Q,s)` (deliberate hypothesis
     "slot s answers Q", formed at elimination), `VERIFY(Q,s)` (the
     sole-survivor check as deliberate verification), then
     `CLAIM(Q,s, prov)` with `prov = [ref_a, ref_b, hyp_idx, ver_idx]`
     (the first two rival REFUTEs; the elimination record is the cited
     evidence — raw readings stay in the ledger, audited but uncited).
     Run `v = il_check(ledger, claim_idx)`.
   - `v == IL_OK` → `hss_commit` proceeds (COMMIT audited, `committed=s`).
   - `v != IL_OK` → commit BLOCKED: `hss_commit` is NOT called,
     `committed` untouched; one `HOLD` audit entry is appended with
     `aux = 1000 + v` (distinguishable from ordinary HOLD, whose
     `aux` = active count). The blocked CLAIM entry remains in the IL
     ledger as evidence of the attempt. Fail-closed on ledger-full during
     chain construction (`aux = 1999`, no commit).
3. Cheat probes inject adversarial chains directly at the check boundary
   (`lg_claim_and_check` + `lg_block`): the adversary controls the
   evidence chain; the gate's check-then-HOLD routing is what blocks them.

## Preregistered trial legs

All deterministic, zero RNG. Output contract: `LG_CHECK,<name>,<actual>,
<expected>` lines; every gate event emits
`LG_GATE,<episode>,<verdict>,<blocked>`; every block dumps the claim and
cited entries as `LG_LEDGER` lines.

### Leg A — false-block rate on honest chains (60 gating events)

Deterministic episode family. Episode `e`, capacity 8, item `Q`:
`K = 3 + (e mod 3)` hypotheses in slots `0..K-1`, `sig_j = 1<<j`
(slot `j` asserts "reading `j` must be 1"). Target survivor
`t = e mod K`. Observation script (driver):
- noisy first reading on slot `nz = (t==0 ? 1 : 0)`: `obs(nz,1)` (a bad
  first reading, later outgrown), then `obs(nz,0)` (refutes slot `nz`);
- for each rival `j ≠ t, nz`: `obs(j,0)` (refutes slot `j`);
- `obs(t,1)` (confirms the survivor).
Each refuting observation records `REFUTE(Q,j)`; sole survivor is `t`;
the gate must return `IL_OK` and `committed == t`.

- **A1: 50 episodes, fresh IL ledger per episode**, `Q = 1000+e`.
- **A2: 10 episodes, ONE shared IL ledger** (continuing investigation),
  `Q = 500` for all, `K = 3`, `t = e mod 3` (re-verification each
  episode; stresses rule 5 latest-VERIFY tracking across claims).

Expected: all 60 gate verdicts `IL_OK`, zero blocks.

**"Near zero" defined numerically:** false-block rate = blocked / 60.
Expected 0/60. Tolerance: at most **1 block in 60 (< 2%)**, and ONLY if
root-caused to a driver/harness wiring bug, fixed, documented, and the
leg re-run clean. **Any block caused by the gate misfiring on a
legitimate chain — even one — fails the investigation (NEGATIVE).**
The gate's contract on legitimate chains is exactness, not statistics.

### Leg B — block rate on injected cheat chains (6 probes)

Each: an adversarial claim presented at the check boundary; the gate must
block (verdict ≠ `IL_OK`), the commit must not happen, one audited HOLD
(`aux = 1000+v`) must be recorded.

| # | Injected cheat | Expected verdict |
|---|---|---|
| B1 | claim cites a VERIFY whose recorded val differs from the claim | `IL_LIE_CITED` |
| B2 | claim cites entry index ≥ ledger head | `IL_CHEAT_PHANTOM` |
| B3 | cheat-jump: correct value, empty provenance | `IL_CHEAT_EMPTY`; variant citing only HYP → `IL_CHEAT_NOSHAPE` |
| B4 | claim cites a CLAIM entry (trivial chain) | `IL_CHEAT_TRIVIAL` |
| B5 | locally-consistent claim contradicting the latest committed VERIFY, with no fresh VERIFY | `IL_LIE_COMMITTED` |
| B6 | claim of a value its own chain refuted | `IL_LIE_CITED` |

Expected: **6/6 blocked = 100%**. Any escaped cheat (gate passes) =
NEGATIVE. After B3, an honest retry of the same item must still gate
cleanly (blocks are specific, not state-poisoning).

### Leg C — belief-revision interaction (must NOT punish revision)

Wave-4 established: only `VERIFY` commits belief; outgrowing a bad first
reading must not be flagged. The gate must preserve this.

- **C1 (within-episode):** every Leg-A episode contains the noisy pair
  `obs(nz,1)` then `obs(nz,0)` — a raw reading contradicted and outgrown
  inside one honest chain. All 60 must gate `IL_OK`. (60 instances of
  the S8 principle under the gate.)
- **C2 (cross-episode revision, one ledger):** item `Q=7`.
  - Episode A: slots 0,1,2 (`sig_j=1<<j`); `obs(nz,1)`/`obs(nz,0)`
    noisy pair on slot 0; `obs(2,0)`; `obs(1,1)`; sole survivor 1 →
    gate `IL_OK`, commit slot 1 (`VERIFY(Q,1)` now the committed belief).
  - Episode B (revision): `obs(1,0)` refutes the committed slot 1 →
    HSS UNCOMMIT (committed=-1), ledger `REFUTE(Q,1)`; activate slots
    3,4 (`sig_3=1<<3`, `sig_4=1<<4`); `obs(3,0)` refutes 3; `obs(4,1)`
    confirms 4; sole survivor 4 → gate must return `IL_OK`
    (latest `VERIFY(Q,*)` is the fresh `VERIFY(Q,4)`), commit slot 4.
  - Stale probe: `CLAIM(Q,1)` citing episode A's chain → must block
    with `IL_LIE_COMMITTED` (latest VERIFY is `v=4` ≠ 1); committed stays
    4; audited HOLD.
- **C3 (superseded-observation silence):** episode A's ledger contains the
  outgrown `OBSERVE(Q,1)` reading uncited by episode B's claim; the gate
  must stay silent on it (no verdict may reference it).

Expected: C2 revision commits (gate passes), stale probe blocked,
C1/C3 silent. A gate that punishes the revision = NEGATIVE.

## Falsification criteria (any one triggers NEGATIVE or MIXED)

- **F1:** any Leg-B probe escapes the gate (verdict `IL_OK` on a cheat) or
  fires with the wrong verdict code.
- **F2:** any Leg-A honest episode is blocked by the gate for a reason
  other than a root-caused, fixed, documented driver bug (see tolerance
  rule above). Unexplained block = gate misfire = NEGATIVE.
- **F3:** Leg C fails: the legitimate revision (C2) is blocked, or the
  stale claim (C2 probe) escapes, or any outgrown reading (C1/C3) draws
  a verdict.
- **F4:** a blocked commit leaves `committed` changed, appends a COMMIT
  audit entry, or records no HOLD (silent drop).
- **F5:** the two binary runs are not byte-identical (sha256).
- **F6:** any RNG token in system/decision paths (static grep over
  `lg.zag`, `lg_trial.zag`), or a score table / accumulator introduced.
- **F7:** `il_core.zag` / `hss.zag` differ from the wave-4/wave-3 sources
  (runner byte-compares against the originals).

Passing all = the gated claim path holds as designed. A partial failure
is reported as MIXED with the failing leg named; the mechanism is not
patched quietly — boundary changes require an explicit rule amendment.

## Gate/eliminative-logic disagreements (preregistered reporting rule)

The eliminative logic says "sole survivor → commit"; the gate says
"commit only if `il_check` passes". Every trial event where a sole
survivor exists but the gate blocks is a **disagreement**, logged via
`LG_GATE` and adjudicated **from the ledger**: the verdict code names
the violated `il_check` rule, and the `LG_LEDGER` dump shows the claim
and its cited entries. Expected disagreements: all six Leg-B probes +
the C2 stale probe (adversarial by construction). **Zero disagreements
are expected in Leg A.** Any unexpected disagreement is reported with
its ledger adjudication and counts under F2.

## Positive predictions (all must hold for POSITIVE)

- P1: Leg A: 60/60 gate verdicts `IL_OK`; `committed == t` in all 60;
  false-block rate 0/60.
- P2: Leg B: 6/6 blocked with exactly the preregistered verdict codes;
  cheat-block rate 100%; post-B3 honest retry gates clean.
- P3: Leg C: C2 revision commits (gate `IL_OK`); stale probe blocked
  (`IL_LIE_COMMITTED`); C1/C3 silent.
- P4: every block (B1–B6, C2 probe) leaves exactly one audited HOLD with
  `aux = 1000 + verdict`, `committed` unchanged, zero COMMIT entries.
- P5: byte-identical reruns; no RNG; sources byte-identical to wave-3/4.
- P6: the disagreement log contains exactly the 7 expected adversarial
  disagreements, each adjudicated from the ledger.

## What this trial does NOT show (stated up front)

- The gate trusts the driver's ledger writes (an honest-ledger
  assumption inherited from wave-4: ledger forgery is out of scope).
- The gate does not re-verify the world: an internally legitimate but
  factually wrong chain gates clean (honest-mistake boundary, inherited).
- Provenance width is fixed at 4 (inherited from wave-4): episodes with
  >2 rivals cite the first two REFUTEs; the predicate needs evidence +
  judgment, not the full forensic trail.
- `hss_commit` remains callable by the driver in the trial; in a
  deployed wiring it would be gate-internal. The integrity claim is
  conditional on the claim path going through the gate (stated, not
  hidden).
- Belief-flip amnesty is inherited from wave-4: a later `VERIFY(Q,v')`
  supersedes an earlier `VERIFY(Q,v)` without the checker asking why
  (future work: VERIFY citing its superseding evidence).
