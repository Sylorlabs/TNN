# FORK L — BUILD SPEC (frozen)

**Date:** 2026-09-23. **Status:** FROZEN — no tuning after any results.
**Program:** SOURCE-TRUST FORKS (prereg `PREREG_SOURCETRUST.md`, commit `db069c41`).
**Design:** learned trust — no hand-set per-source value; the scalar emerges from a
per-source track record. Per-source TABLE (not learned-function-over-features):
per debate §7 Q4, L makes **no Sybil-resistance claim** from the trust
representation and accepts K's Sybil analysis.

## 1. Record schema (per source; source-symmetric, zero-initialized)

- **Outcome ring:** last 1024 outcome codes (`0=OK`, `3=PEND`; `DELETED` markers
  for expunged entries). The ring IS the record the scalar derives from.
- **Regime:** the trust-relevant suffix of the ring — outcomes after the most
  recent `MAL`/`PEND` (a refutation or confirmed defiance starts a new regime).
- **Key slots:** 64 × `(key, stated_val, world_val, flags, pend_idx)` — which
  claims are awaiting disposition, for correction/defiance detection.
- **Ever-counters** (audit only, never in the trust formula):
  `n_ok, n_pend, n_mal, n_corrected`.
- **Global (source-neutral):** world table (2048 keys, latest WORLD wins);
  claim ring (16384 recent `(src,key,val,ep,verdict)` for corroboration /
  contradiction / taint scans).

## 2. Record-update rules (source-blind; WORLD is the only teacher)

`st_world(key,val)` (WORLD episode; WORLD is authoritative, §3.1):
- New/changed value → insert. Every live source-claim on `key` with
  `stated≠val` becomes **PEND** (appended; regime resets — the tripwire).
  Claims matching `val` earn **OK** (once per source/key).
- A PEND resolves by the source's own later behavior, never by trust:
  **correction** (source states the world value) → PEND expunged (`DELETED`;
  regime restored — honest error fully forgiven); **defiance** (source restates
  the refuted value or contradicts the world value again) → PEND rewritten to
  **MAL** (confirmed; never expunged). World flip-flopping back vindicates
  (PEND→OK). Silence leaves the PEND standing (presumed-malice until answered).

`decide(src,key,val)` (SAY episode) records claims into the claim ring and key
slots; outcomes are appended ONLY for world-anchored events (above). Corroboration
never mints outcomes — the training signal is world-derived, never
trust-derived (bootstrap answer: no circularity; debate §7 Q5 candidate law —
a distrusted source's corroborated truth is admitted on the corroboration
while its distrust is untouched).

## 3. Emergence rule (the scalar is a pure function of the ring)

Over the current regime (`n_ok` OK outcomes, `n_tot` total non-deleted outcomes):

```
trust1000(src) = 1000 * (n_ok + L_A) / (n_tot + L_A + L_B)
```

Integer arithmetic only. Fresh source: `1000*1/2 = 500`. One unresolved
refutation after any history: regime = `[PEND]` → `333` — the collapse is
**discontinuous** (tripwire, not gradient). 17 confirmed OKs after a MAL
rebuild to `900`. Same ring → same trust, always (recomputed from the stored
ring on every call; no hidden per-source state).

## 4. Admission mapping (trust advises; structure constrains)

On `decide(src_id,key,val,hist) -> 0/1/2` (INSTALL/WITHHOLD/REJECT):
1. **World known:** `val==world` → INSTALL (+OK; resolves PEND→corrected).
   `val≠world` → REJECT (+PEND; PEND→MAL if restating a refuted value).
2. **Contradiction:** another source has a live INSTALL-verdict claim on `key`
   with different val and no world resolution → WITHHOLD (ST-2: never
   double-install a contradictory pair).
3. **Taint:** `(key,val)` was previously asserted by a source with current
   trust < L_TH → WITHHOLD unless ≥2 asserters have trust ≥ L_TH
   (frozen taxonomy §3.3's "≥2 independent sources"; RT-T3: a trusted repeater
   alone never installs a liar-originated claim).
4. **Trust:** trust ≥ L_TH → INSTALL; else ≥2 established asserters → INSTALL
   (ST-6; no OK minted — trust≠truth); else WITHHOLD. Low trust alone never
   REJECTs.

Every verdict stores a warrant in hist
(`L:<verdict>|t=<trust1000>|ok=<n> ma=<n> pe=<n> cor=<n>|rule=<name>`);
`st_warrant(hist)` returns it; `st_trust(src,hist)` returns trust×1000 (§6.3).

## 5. Hard cases

- **First-seen source:** trust 500 < 900 → novel uncorroborated claims WITHHOLD
  (declared initial policy: 0% admitted on reputation alone; strangers are
  held, not believed — the 1GB/60-60 finding forbids optimism). Trust is earned
  only via world-anchored OKs.
- **Long-honest-then-lying (ST-3):** lie #1 installs (no evidence exists yet —
  information-theoretically unavoidable in production mode; the bar is read as
  0 installs *after the first caught lie*). First WORLD-disagree → PEND →
  regime reset → trust 333 → subsequent lies WITHHOLD. Patient 1-in-20 drip:
  PENDs never resolve → trust pinned at 333 → every lie withholds.
- **Wrong-but-honest (ST-4/H4):** world-change PEND → honest update expunges it
  → regime (and trust) fully restored; the corrected claim INSTALLs on
  world-agreement. No MAL is ever written without defiance. "True when stated"
  claims cost nothing once corrected. Chronic uncorrected mislabels sit at
  PEND (caution, not conviction); ~17 confirmed truths recover.
- **Reformed (ST-5):** MALs never expunge, but the regime moves on: ~17
  world-confirmed honest episodes rebuild to 900. Recovery is possible,
  never instant, never impossible.

## 6. Tunables (frozen; source-blind; 3 ≤ K's 5)

| # | Name | Value | Class |
|---|------|-------|-------|
| 1 | `L_A` | 1 | substrate-general: Laplace prior pseudocount (good). Symmetric no-evidence arithmetic. |
| 2 | `L_B` | 1 | substrate-general: Laplace prior pseudocount (bad). |
| 3 | `L_TH` | 900 | decision policy: trust-alone INSTALL iff trust×1000 ≥ 900. The trinary gate needs one cutoff (debate Sol-A); declared behaviorally. |

No "betrayal hurts X" constant exists — severity is structural (regime reset).
Capacities are not tunables (verdict-invariant at battery scale): 64 sources,
1024 outcomes/source, 64 key slots/source, 16384 claim ring, 2048 world keys.

## 7. Anti-knob posture (§7.1)

1. No per-source constants: `src_id` is used ONLY as an array index; zero
   branches on its value; zero per-source initializers.
2. Source-symmetric initial state: all-zero records → trust 500 for every
   source; proven behaviorally by the `src_id` swap test (deliverable
   `st_test.zag`: permuted stream ⇒ byte-identical verdicts/warrants).
3. 3 source-blind tunables, declared above.
4. Record primacy: trust recomputed from the outcome ring on every call.

## 8. Interface notes for the battery driver

Frozen: `decide(src_id,key,val,hist) -> i32`. Additionally the driver MUST call
`st_world(key,val,hist)` on WORLD episodes (the §3.3 taxonomy is unobservable
otherwise) and may call `st_trust(src_id,hist)->i32` (§6.3) and
`st_warrant(hist)->[]u8` (§11). Preconditions: `0 ≤ src_id < 64`, `key ≥ 0`.
Origin-cluster tags are not deliverable through the frozen interface, so
"independent" := distinct `src_id`; Sybil defense rests on the
established-source gate (§5), not identity. Known limitation (debate §7 Q4):
farmed-to-established colluders with no world evidence are indistinguishable
from honest convergence — consequence-free collusion without world evidence is
outside this fork's scope. Retroactive re-valuation is not performed in the
production-mode admission path (§12); the record (per-source claim history +
key slots) supports a backward walk, which is documented but unbuilt.

## 9. Debate must-address (§9, condensed)

1. Constant inventory: §6 (3 constants, classified). 2. Initial policy: §5
   (0% on reputation; defended by the 1GB finding + conscious-KB law).
   3. Bootstrap: §2 (world-anchored signals only; corroboration never trains
   trust). 4. Sleeper tripwire: §3 (PEND/MAL resets the regime —
   discontinuous 998→333 collapse; one-off error vs. changed circumstance vs.
   long con discriminated by the source's own correction/defiance/silence).
   5. Per-source table: no Sybil-resistance claim (debate Q4 accepted).
   6. L≠S-with-cache: the scalar is fixed-form arithmetic over a
   verdict-annotated record (no deliberation to memoize); admission ALSO reads
   structure directly (contradiction/taint/corroboration scans).
