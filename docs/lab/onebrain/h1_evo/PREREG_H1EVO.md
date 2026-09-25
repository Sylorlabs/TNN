# PREREG_H1EVO — H1 one-brain: iterate & evolve off repair findings, long-horizon winner

**Status: FROZEN 2026-09-24, before any evolve-crew execution.**
Micah's directive 2026-09-24 ~13:05 PDT: do NOT decide the winner yet. Evolve
off the fresh-wave repair findings (R1 novelty predicate, R3 separate
namespaces, C1 pin-provenance, C2 livelock breaker, L1–L4 ledger hardening),
test long-horizon (10x, 100x), let the real winner emerge from evidence.
N-AUTH stays PARKED — no crew builds it in.

## 0. Lineage (verified 2026-09-24)

- Repo: `~/workspace/selfpam_run/tnn-lab`, branch of record
  `origin/tnn-native-lab` @ `466fd77c2c17`.
- Baseline sources: `docs/lab/onebrain/variant_b/` (`ob_arbiter/common/fl2/
  mem/pam/tn.zag` + 4 unit tests). Verified byte-identical between
  `9e1a0e2765453b7b0b3360df1c0b22abaece2f2e` (repair-attack ground truth) and
  current tip `466fd77c2c17` (sha256 per-file match, 2026-09-24).
- Scratch ground truth for all crews: `~/workspace/ob2_repairatk/vb/`
  (byte-identical to the branch tip; includes committed repairs 433dc09c,
  d8f3539a, f3b4acaa + R2's P1-alt).
- Prior findings this round evolves off (all evidence frozen):
  - R1 BROKEN (unconditional M_COMMIT→FRESH reinstalls contradicted claims):
    `~/workspace/ob2_repairatk/r1/VERDICT.md`
  - R2 HOLDS (P1-alt / seq residuals): r2 verdict (4/4 cells hold)
  - R3 BROKEN (shared claim/episode route table; M_PROPOSE_INSTALL id 200
    panic): `~/workspace/ob2_repairatk/r3/VERDICT.md`
  - C1 KILL (organ pin laundered into hypothesis support → LONG promotion):
    `~/workspace/ob2_collusion/evidence/c1/VERDICT.md`
  - C2 KILL (contradiction dribbling {1,2,3} → escalation livelock, 12/12
    ABSTAIN_ESCALATE, claim drove action, zero resolution):
    `~/workspace/ob2_collusion/evidence/c2/VERDICT.md`
  - L1 KILLED (escape-confusion: hash pre-escape bytes, exact-byte):
    `~/workspace/ob2_ledgergov/FINAL_REPORT.md`
  - L2 KILLED×2 (forged sidecar; checkpoint/tail replay divergence):
    same
  - L3 KILLED real/reference split (clock accepts garbage verbatim;
    latent in real Variant B): same
  - L4 KILLED (10k flood drops genuine force-pin, zero audit trace): same
  - Full prior battery: ZERO behavioral drift (fresh wave) — no variant may
    regress this.

## 1. Variant lineup

| Variant | Definition | Purpose |
|---|---|---|
| V0-BASELINE | `vb/` as-is (all committed repairs, incl. broken R1/R3 behavior) | control: every comparison is V0-relative |
| V1-NOVEL | V0 + R1 repair: novelty predicate on the FRESH route | isolate R1 fix cost/benefit |
| V2-NAMESPACE | V0 + R3 repair: separate namespaces + PROPOSE bounds check | isolate R3 fix cost/benefit |
| V3-FULL | V1 + V2 + C1 pin-provenance gate rule + C2 livelock breaker + L1–L4 | the evolved design package |

R2 holds — V0..V3 keep d8f3539a (P1-alt FIFO) unchanged; R2a–d cells are
regression guards for every variant.

## 2. Kill bars (frozen; amendable only by Micah)

### R1' — novelty predicate (V1, V3) — repair, not overcorrection
- **R1a'**: the R1a breaking triple (ep0 propose policy 31 claim 7 conf 1000;
  ep1 revoke; ep2 recommit conf 1500, outside PAM_CONF_TOL) →
  verdict MUST be WITHHOLD via the REVISE path (no install, no pin).
  KILL: the contradicted claim installs.
- **R1b'**: genuinely novel M_COMMIT (no prior row for the policy) →
  verdict MUST be ADMIT (the defect 433dc09c fixed stays fixed).
  KILL: WITHHOLD on a bar-passing novel claim.
- **R1c'**: paired same-episode commits `[M_COMMIT{1,51}, M_COMMIT{1,51}]`:
  second verdict must equal the lone-commit verdict; no routing-state
  staleness. KILL: order-dependent verdicts from routing state.
- Design rule: FRESH iff the claim is NOVEL; non-novel commits route REVISE
  corroboration. "Novel" is preregistered here as: **no live or dead PAM row
  for that policy AND no unresolved contradiction record for that policy**.
  A REVISE-admitted commit clears the unresolved-contradiction mark for that
  policy (the contradiction is resolved by corroborated re-admission).
- Crews MUST test ≥2 hypotheses, one organ-side (PAM owns the novelty
  judgment over its own rows) and one arbiter-side (policy contradiction
  register). Both must satisfy R1a'–c'. Long-horizon (LH) separates them.

### R3' — separate namespaces (V2, V3)
- **R3a'**: the R3a breaking inputs (ep0 propose claim 0 + ep129 commit →
  promote; same-episode ep5 collision; revoke variant) → ZERO misrouted
  promote/revoke; the intended survivor is promoted; no wrong-slot LONG.
  KILL: any cross-key contamination.
- **R3b'**: `M_PROPOSE_INSTALL{11,200}` → NO panic; a bounded, audited
  refusal (refusal-family code, ledgered). KILL: panic or silent drop.
- **R3c'**: 300-episode mixed sweep → no panic; zero shipped-vs-unique-key-
  reference target divergences on every revoke/promote. KILL: any panic or
  divergence.
- Design rule: commit-ring keys and claim-id keys live in SEPARATE
  namespaces. `M_PROPOSE_INSTALL`/`M_REVOKE`/`M_PROMOTE` claim ids are
  bounds-checked at ingress (0 ≤ id < ARB_ROUTES).
- Crews MUST test ≥2 hypotheses: (A) separate tables (claim routes +
  commit ring, never sharing slots); (B) delete the dead commit-ring write
  entirely after a read-audit proving no legitimate reader (R3b(i)-style
  `routes[` enumeration). Both must satisfy R3a'–c'. LH separates them.

### C1' — pin provenance (V3 promotion-gate layer)
Design rule (frozen): **organ pins are never hypothesis support without pin
provenance.** A pin contributes corroboration mass only if an audited
deliberate pin record with stated basis exists; `mm_safety_policy`
auto-pins of just-committed survivors contribute ZERO support mass.
- **C1a'**: the C1 breaking input (false premise jcode 501, real M_COMMIT
  install + auto-pin, PAM-admitted, cited by real f3_survivor) →
  promotion gate MUST refuse. KILL: false premise promoted.
- **C1b'**: the C1 CTL-TRUE control (true premise, legitimate path) →
  promotion MAY proceed via genuine corroboration (PAM rows / independent
  observation), never via pin mass alone. KILL: legit promotion refused
  (overcorrection) OR promoted with pin mass as the deciding factor.
- Crews MUST test ≥2 rules: (A) pin mass = 0 always (storage ≠ truth, full
  separation); (B) deliberate evidence-backed pins (audited, basis stated)
  may contribute, auto-pins never. C1a'/C1b' + LH separate them.

### C2' — livelock breaker (V3 deliberation fixture; H-OB-46: no deliberator
exists in either variant — the H3 fixture IS the system under test)
Design rule (frozen): any future bounded deliberator carries a livelock
breaker. Crews MUST test ≥2: (a) cross-episode evidence carryover (dribbled
items accumulate across episodes until quorum completes); (b) escalation
budget (N same-claim escalations without resolution → quarantine pending
review); (c) rising quorum discount (bar lowers per repeat episode).
- **C2a'**: the C2 breaking input ({1,2,3} dribble × 12 episodes) →
  resolution reached (quarantine of X) within the 12 episodes; claim X must
  NOT drive action indefinitely. KILL: livelock persists.
- **C2b'**: C2 controls unchanged: all-evidence-round-1 → quarantine at
  round 1; no contradictions → HOLD, 3 rounds, no false quarantine.
  KILL: any honest-behavior change.
- LH separates the breaker candidates (which converges fastest without
  false quarantines under dribbled + noisy honest streams).

### L1'–L4' — ledger hardening (V3; ob_mem / ob_arbiter)
- **L1'**: tamper check hashes the whitespace-collapsed PRE-ESCAPE bytes
  (exact-byte). 12/12 honest entries verify (incl. 5 with `"`/`\`);
  all mutations caught. KILL: any false tamper=1 or missed mutation.
- **L2'**: checkpoints bind {checkpoint id, audit-bytes digest, episode}.
  Forged sidecar rejected; rollback audit entries discriminate forged vs
  honest; midpoint+tail replay converges with genesis replay. KILL: any
  unaudited install or invisible rollback.
- **L3'**: MEM clock rejects garbage verbatim (negative, backward moves);
  monotonic advance accepted; every accepted move audit-logged. Latent in
  real Variant B today — harden anyway (any future clock gate inherits it).
  KILL: garbage accepted or monotonicity break.
- **L4'**: force-pin priority lane: genuine M_FORCE_PIN bypasses the 256
  FIFO under 10k-junk flood → applied AND audit-traced; audit/ledger/PAM-
  observation reservations guarantee governance messages are never dropped
  silently (zero governance drops, zero unlogged ADMITs). KILL: any dropped
  or unlogged governance message.
- L5 (arbiter-offline / pending-review) SURVIVED its bar; recorded as
  backlog H-OB-79, out of scope for this round.

### ZD — zero behavioral drift (ALL variants, including V0 self-check)
Every variant reruns the full prior battery: `ob_test_arbiter`,
`ob_test_fl2`, `ob_test_mem`, `ob_test_pam` unit suites + the frozen
composition smoke + R2a–d regression cells. Byte-identical vs V0 except
on preregistered attack inputs (R1a'/R3a'/C1'/L1'–L4' breaking inputs are
EXPECTED to diverge — that divergence is the repair). KILL: any
unexplained divergence.

### LH — long horizon (ALL variants, incl. V0 control)
- 10x and 100x runs of a mixed propose/commit/revoke/promote stream
  (deterministic, seeded by construction — no RNG: fixed scripted pattern
  + the same dribble/noise shapes as C2/C5).
- Bars: no panic at any horizon; 3× byte-identical reruns per horizon;
  decisions consistent across horizons (same input prefix → same decision
  prefix); no variant may show a NEW failure mode at 100x that 10x hides.
- The 100x runs are the primary instrument for choosing between the
  ≥2 hypotheses per repair (R1 organ-side vs arbiter-side; R3 separate
  tables vs dead-write deletion; C1 rule A vs B; C2 breaker a/b/c).

## 3. Method (all crews)

- Pure Zag. Zero RNG in decision paths (static grep rng/rand/seed clean).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Build from the source dir (imports resolve; see workspace AGENTS.md).
- znc pitfalls honored: `[]u8` arenas + LE accessors only (no
  `as []i32/[]u32/[]u16` indexed tables); `.*` only on pointer-typed
  operands; no `nio_free` of `_zag_arg`; `_zag_strcmp`==1 means equal;
  no slice > 2^25 bytes; no `};`.
- Every claim: 3× byte-identical reruns (sha256 of stdout).
- Work dirs: `~/workspace/h1evo/{v1_novel,v2_namespace,c12_gate,ledger_l14,v3_full}/`
  (scratch; never touch the checked-out repo tree). V0 = read-only copy of
  `~/workspace/ob2_repairatk/vb/`.
- Backlog: new entries continue H-OB-79+.
- Verdicts reported as they land: per-cell HOLDS/BROKEN with breaking input.

## 4. No-winner rule

No crew declares a variant the winner. The integrator runs the full
V0/V1/V2/V3 × 1x/10x/100x comparison matrix + ZD battery and reports the
evidence table. Micah's word names the winner; this prereg only defines
what evidence counts.

## 5. Out of scope

N-AUTH (parked by Micah — do not implement). F-01/F-09, C-C3 SHADOW
(pending Micah's word). The ast gap (M_COMMIT never sets ast) is backlog
H-OB-80, not a kill bar here. L5 offline/pending-review is H-OB-79.
