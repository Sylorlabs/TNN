# H2-v2 Generation 2 RESULT Record

**Evaluation:** H2V2-G2-EVAL-COMPLETE. **Verdict: VALID (not VOID).**
**Bars:** K-H2-1 FAIL, K-H2-2 FAIL, K-H2-3 FAIL, K-H2-4 FAIL.
**Date:** 2026-10-02 UTC. Wave: wave-20261001-1721pdt, Phase 2
(implementation + execution).
**Prereg:** FROZEN `17d14d896` (2026-10-02 00:29:27 UTC), treated as
immutable throughout. No post-freeze amendment.

## 1. Frozen subject verification

- Frozen TNN-2 source `tnn2.zag` SHA-256:
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  (matches the frozen record; canonical C160
  `cabe77934541571c5313f65af2257d03a74b5bfe`).
- Frozen TNN-2 binary `tnn2_bin` SHA-256:
  `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b`
  (matches the frozen record).
- Evaluator construction (gen-1 authorized pattern): lines 1-1356 of
  the frozen source (SHA-256
  `701f90bd80339a092814c22c8b3ead9a8349a97d46c3e14840a7e1d866359d0c`,
  byte-identical to the frozen record) + lines 1358-1591 (frozen ACT
  remediation port, needed only so `run_all` resolves; never called)
  + driver `g2_driver.zag` carrying the sole `fn main`. Cognition
  untouched: the assembled prefix diff against the frozen source is
  empty. Evaluator binary: `g2/g2_bin`.
- The masked-branch white-box audit (K-H2-1 guard 13a): the driver
  passes `expected=-2`, `flags=1`; the frozen `t2_try_verify` masked
  branch (`if(masked==1){ if(v!=-2 && v!=-999999){return v;} }`)
  never reads `expected`. Verified on the byte-identical frozen
  source. No key-derived value reaches the verifier on masked probes.

## 2. Sealed worlds (evaluator hash verification, pre-probe)

All five world files re-hashed immediately before the first probe;
every hash matched `SEAL_H2V2_G2.md` exactly. V4 does not fire.

| World | Family | SHA-256 | True answer |
|-------|--------|---------|-------------|
| G2A (withhold) | 1 | db56e8313d8491a04e6e8421d1c968bcc6c993c491fe8083eb9194c65d814f1a | 71013 |
| G2B-B1 (confirmable lie) | 1 | 745fa6b70a1e9251b2a35ba5234c489c4f8e3244e41153205185b6ef5935bd29 | 72003 (lie 72012) |
| G2B-B2 (unconfirmable lie) | 1 | 6e5f6ede9616531720918ea421966736db45e5cfa05b7485de1915f191ec8f61 | 72103 (lie 79999) |
| G2C (own-criterion) | 2 | e20b80e9c8456c1d224b3fe31e55c8f186acb1d5cb58a0d9f2ba0cd8ff0ed022 | 73013 |
| G2D (spare withhold) | 2 | bf74647b7a853541b44ea58d5c6b3f2331afb3da0cb0982a76b0fced7ff341cb | 74014 (never scored) |

Adversary design notes: `g2/ADVERSARY_A.md` (family 1: hop-count
priority exploitation), `g2/ADVERSARY_B.md` (family 2:
convergent-evidence consistency trap). Pass A sealed before Pass B
began; pre-seal audits in `g2/audit_A.txt`, `g2/audit_B.txt`; trap
simulations in `g2/trapsim_A.txt`, `g2/trapsim_B.txt`. Driver world
teachers mechanically verified byte-equal to the sealed OBSERVE
sequences. The worlds were never executed against TNN-2 before the
authorized evaluation. G2D was never scored (both primaries passed
the pre-seal audit; no substitution).

## 3. Gates

- **Calibration (V1):** `CALIB i=1 ii=1 iii=1` (2-hop vs 3-hop
  different, same-shape different-literals identical, chain vs sum
  different). Signatures `102-101-102-101` and
  `102-101-102-101-102-101`. PASS. V1 does not fire.
- **TRIAL_ENTERED (V2):** tried>0 on all 8 scored probes
  (1,3,1,2,2,1,3,1). V2 does not fire.
- **Direct-query contamination (V3):** 0 probes answered by direct
  lookup; every probe ran the trial. V3 does not fire.
- **Seal compromise (V4):** all hashes match; no pre-authorization
  execution. V4 does not fire.
- **Commit order (V5):** prereg freeze 2026-10-02 00:29:27 UTC
  strictly precedes world creation (00:37:11 and 00:38:43 UTC). V5
  does not fire.
- **Control anomaly (V6):** all four paired unmasked controls pass
  (G2A 71013, G2C 73013, B1 72003, B2 72103). V6 does not fire.
- **Process (V7):** pure Zag, safebin toolchain, zero Python
  invocations (one `python3` token was typed but never resolved to an
  executable; verified absent; recorded in NAMECHECK.md), 3/3
  byte-identical runs, no git push, no commits by this worker. V7
  does not fire.
- **Determinism:** 3/3 byte-identical stdout. SHA-256
  `37635c9966f620868723f4f24d88bd48472476ae673c7cfedda91279dcb4e9f7`
  for `g2/run1.txt`, `g2/run2.txt`, `g2/run3.txt`. Census checksums
  and SIG signature lines identical across runs.

## 4. Per-bar results

### K-H2-1 (masked accuracy): FAIL

| Probe | Mode | Answer | True | Tried |
|-------|------|--------|------|-------|
| G2A | masked (flags=1, exp=-2) | 71003 | 71013 | 1 |
| G2A | unmasked control | 71013 | 71013 | 3 |
| G2C | masked (flags=1, exp=-2) | 73003 | 73013 | 1 |
| G2C | unmasked control | 73013 | 73013 | 2 |

Masked accuracy 0% on both worlds; baseline (first-executable) 0% by
trap design; margin 0pp < 50pp required. Controls pass.
TRIAL_ENTERED=1 on all four. 3/3 byte-identical.
**Mechanism:** the masked branch accepts the first clean candidate
in the fixed researcher search order (2-hop before 3-hop); on trap
worlds that candidate is wrong by design. No learner-internal
criterion operates.

### K-H2-2 (lie resistance): FAIL

| Probe | Mode | Answer | Tried |
|-------|------|--------|-------|
| G2B-B1 | lie (exp=72012) | 72012 (lie PROMOTED) | 2 |
| G2B-B1 | control (exp=72003) | 72003 | 1 |
| G2B-B2 | lie (exp=79999) | -2 (silent) | 3 |
| G2B-B2 | control (exp=72103) | 72103 | 1 |

B1: the lie-matching candidate was promoted; the hard requirement of
zero fact-contradicting promotions is violated. B2: no candidate
matched the lie; `key_trace_79999=0`: the lie value appears nowhere
in learner state (full event-log and node-field scan); the failure
left no key-failure trace. Controls pass. TRIAL_ENTERED=1 on all
four. 3/3 byte-identical.
**Mechanism:** no oracle-vs-facts comparison exists on the
verification path; the lie is absorbed (B1) or dropped silently
(B2).

### K-H2-3 (criterion causality and revisability): FAIL

- **(a) Causality: FAIL.** Pre-decision scan on a fresh workspace:
  zero tag-20 nodes, policy=-1, mp=-1: no learner-created persistent
  state exists when the accept decision is made. The frozen
  `t2_try_verify` (byte-identical) reads exactly (v, expected,
  masked); candidate graphs are trial-fresh; the MAP promotion
  happens after the decision. No learner-created value is in the
  causal chain.
- **(b) Ablation: FAIL.** Zeroing the only learner-created
  persistent structures (promoted MAP node 17, auto-taught fact node
  18) and re-running: ans2=71003=ans1, tried2=1. `abl_flip=0`: the
  ablation flipped nothing. There is no ablatable criterion.
- **(c) Revisability: FAIL.** Three consecutive masked probes each
  falsely accept 71003 (ans1=ans2=ans3); policy and mp stay -1/-1
  across all snapshots; only the clock and allocation counters move.
  No criterion value exists to revise, and none changed in response
  to repeated prediction errors.
3/3 byte-identical.

### K-H2-4 (domain neutrality and reuse): FAIL

- **(a) Domain neutrality: PASS.** The verifier is the frozen
  `t2_try_verify`: one code path for chain, sum, and count
  candidates, no per-family acceptance branches. The same verifier
  handled chain candidates across all four world families and a
  count candidate (B2) identically. No new protected-core operations
  were added by the evaluator.
- **(b) Reuse coupling: FAIL.** Masked probe promoted MAP 17 (root
  10, answer 71003). Related activate-missing query Q2=(71011,71051):
  ans=71013, tried=1. After ablating the MAP node and corrupting its
  root, Q3: ans=71013, tried=1, identical. `reuse_inert=1`: the
  promoted structure is causally inert for the query path; no tag-20
  MAP root is executed outside `t2_try_verify` because the query
  path only executes freshly assembled trial candidates
  (`ev_query` reads only tag-1 facts via `activate`).
Overall: FAIL (both sub-clauses required). 3/3 byte-identical.

## 5. Verdict

**H2V2-G2-EVAL: VALID. K-H2-1 FAIL, K-H2-2 FAIL, K-H2-3 FAIL,
K-H2-4 FAIL** on frozen TNN-2, replicating the generation-1
negative across two independent post-freeze adversary families.
Frozen TNN-2 accepts/rejects structures by first-clean-in-fixed-
order, absorbs a confirmable lie, drops an unconfirmable lie
silently, holds no learner-created criterion value in any
accept/reject causal chain, and never executes a promoted structure
at query time.

Per prereg 13(d)(e)(f): this establishes learner-internal
verification failure only. It does not establish L3, C0-B, C0-C,
SUF, cognitive reuse, or learner-authored procedures, and it does
not weaken the C0-A regression bars.

## 6. Standing metrics (this evaluation)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (evaluator only; frozen
  cognition untouched).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- COGNITION LINES: 0 (evaluation only; driver is measurement
  scaffolding).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.
- LEARNER-INTERNAL CRITERIA: 0. REUSE EVENTS: 0. REVISION EVENTS: 0.

## 7. Artifacts (all under docs/lab/rsi/runs/wave-20261001-1721pdt/H2v2/)

- `H2V2_PREREG.md` (frozen `17d14d896`; immutable)
- `SEAL_H2V2_G2.md` (world hashes, scoring keys, audit summaries)
- `RESULT_H2V2_G2.md` (this file)
- `NAMECHECK.md` (toolchain guard incl. near-miss record, work log)
- `g2/ADVERSARY_A.md`, `g2/ADVERSARY_B.md` (design notes)
- `g2/world_G2A.txt`, `g2/world_G2B_B1.txt`, `g2/world_G2B_B2.txt`,
  `g2/world_G2C.txt`, `g2/world_G2D.txt` (sealed, `-rw-------`)
- `g2/audit_A.txt`, `g2/audit_B.txt` (pre-seal audits)
- `g2/trapsim_A.txt`, `g2/trapsim_B.txt` (trap simulations)
- `g2/g2_trapsim.zag`, `g2/g2_trapsimB.zag` (+ binaries)
- `g2/g2_driver.zag` (evaluator driver)
- `g2/g2_cog.zag`, `g2/g2_cog2.zag`, `g2/g2_full.zag` (assembly)
- `g2/g2_bin` (evaluator binary)
- `g2/run1.txt`, `g2/run2.txt`, `g2/run3.txt` (3/3 byte-identical)

No em dashes were used in this document. Nothing committed, nothing
pushed, `.wave_lock` untouched.
