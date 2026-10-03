# T-ADV5 RE-EVALUATION RESULT: Sealed Re-run on the Fixed Bridge

Status: EVALUATION-COMPLETE. No SURVIVES claim.
Prereg: `tadv5_reeval/PREREG_TADV5_REEVAL.md` (commit `66aed6805`). Frozen before evaluation.
Fix design: `bridge_fix/BRIDGE_FIX_DESIGN.md` (commit `791388384`).
Fix build: `bridge_fix_impl/BRIDGE_FIX_IMPL_RESULT.md` (commit `d920af162`).
Original design: `bridge_adv/T_ADV5_DESIGN.md` (commit `c36e61d3f`).
Original evaluation: `bridge_adv/T_ADV5_RESULT.md` (commit `d06d2d8e1`), verdict FAIL.

## Verdict: TADV5-ACCEPTABLE

## Kill bars

- K1: PASS. Prereg frozen at `66aed6805` before any evaluation commit.
  Verified: prereg commit is an ancestor of this result commit, and the
  evaluation harness did not exist at the prereg commit.
- K2: PASS. Evaluation implemented under the sealed protocol: mechanism
  code byte-identical to `d920af162` (F-RADV5-SEAL verified by diff; only
  the two family-13 dispatch additions and the replaced `main()` differ),
  fresh state, standard discovery protocol, 3 runs.
- K3: PASS. Pure Zag (shell, git, znc, diff, grep only; zero Python at any
  stage including verification); no em dashes or en dashes in loop
  documentation; deterministic (3/3 byte-identical, md5
  `036a3fcb334c66c43f6d6e73e662a978`, exit 0, zero stderr bytes).

## Evaluation method

Created `tadv5_reeval/tadv5_reeval.zag` by copying `bridge.zag` from commit
`d920af162` verbatim, with three surgical additions mirroring the original
evaluation:
1. `fam_base`: added `if(f==13){return 13000;}`.
2. `true_obj`: added family 13 case (1 for i<10, 0 for i<20, 1 for i>=20).
3. Replaced `main()` with the T-ADV5 harness running family 13 fresh
   (run_family, emit_trace, node/EQ counts, held-out check on promotion).

F-RADV5-SEAL holds: diff of the harness against `d920af162` shows only the
three permitted changes. No mechanism code touched.

## Measured outcome (3/3 identical)

From `TADV5_RE_RUN1.txt`:

```
BRIDGE MOVE li=0 op=2 p=13010 gain=1 nc=4
BRIDGE MOVE li=3 op=2 p=13011 gain=1 nc=7
INV SEARCH fam=13 n=40 built=0 nodes=7 scost=28
INV HONESTFAIL fam=13 n=40
TR TADV5 fam=13 cost=68 adopted=-1 V=14 refit=-1 inv_event=0 inv_promoted=0 uses3=0 strikes3=0
TADV5-NODES nc=7 eqnodes=0
TADV5 adopted=-1 promoted=0
```

- cost=68
- adopted=-1, promoted=0
- inv_event=0 (inventor FIRED on the 40-point buffer)
- inv_promoted=0
- nc=7, eqnodes=0 (search terminated with a 7-node unpromoted tree)
- Clean HONESTFAIL trace (INV HONESTFAIL fam=13 n=40)

## What happened

The fixed protocol behaved exactly as the design intended:

1. Early homogeneous segments could still adopt menu CONST on the first
   segment, but every VERIFY strike now retained its evidence (D1/D2), so
   no menu form could be re-adopted once the buffer was mixed.
2. n reached 40 on the complete episode-global (1,0,1) buffer with no menu
   form fitting it. R4 fired: the inventor ran construct_search on the
   full 40-point deceptive buffer (inv_event=0, vs inv_event=-1 in the
   original FAIL).
3. The greedy search (op codes: 0=CONST, 1=LT, 2=EQ, 3=internal) applied
   two EQ isolations (+1 gain each: EQ at 13010, then EQ at 13011) while
   every LT split gained 0. No positive-gain move remained, the 8-node cap
   was not reached, and exact fit was not achieved. The search terminated
   without exact fit: HONESTFAIL.
4. Per R7 there was no live invented form to strike, so the episode ended
   as HONESTFAIL with cost 68, within the 108 ceiling.

The deceptive search landscape the adversary designed was confronted by
the inventor for the first time. The mechanism recognized its greedy
myopia (EQ +1 vs LT 0) and failed honestly, exactly as the design's worked
prediction anticipated (predicted cost approximately 84; measured 68).

## Verdict against the frozen bars

- STRONG PASS: not met (adopted=3/promoted=1 required; measured
  adopted=-1/promoted=0).
- ACCEPTABLE: met. adopted=-1, promoted=0 (HONESTFAIL); cost 68 <= 108;
  no constraint violations (nothing promoted; nc=7 within the 8-node cap;
  0 EQ nodes promoted); clean HONESTFAIL trace.
- FAIL: no falsifier fires.
  - F-DECEPT-COST: not fired (68 <= 108).
  - F-DECEPT-DEGENERATE: not fired (no promoted tree).
  - F-DECEPT-NODECAP: not fired (no promoted tree; nc=7 <= 8).
  - F-DECEPT-MEMORIZE: not fired (no promoted tree).
  - F-DECEPT-WRONG: not fired (no promoted tree; held-out check moot).
  - F-DECEPT-PREEMPT: not fired. The original failure mode (menu CONST
    adoption with the inventor never firing) does not recur: the inventor
    fired on the 40-point global buffer (inv_event=0).

## Interpretation

The fix resolves the protocol blind spot T-ADV5 exposed. The inventor now
confronts the deceptive buffer by construction. The resulting HONESTFAIL
exposes greedy search myopia as the mechanism's honest boundary, which is
precisely the dimension the adversary designed T-ADV5 to test. This is one
data point for C0-C on the fixed protocol; it does not close C0-C and
starts no SURVIVES claim. C0-D (cognitive reuse) remains open.

## Files

- `tadv5_reeval/PREREG_TADV5_REEVAL.md`: frozen prereg (`66aed6805`).
- `tadv5_reeval/tadv5_reeval.zag`: evaluation harness (fixed mechanism
  verbatim + family 13 dispatch + T-ADV5 main).
- `tadv5_reeval/tadv5_reeval_bin`: compiled binary (build artifact).
- `tadv5_reeval/BUILD.err`: compiler log.
- `tadv5_reeval/TADV5_RE_RUN1.txt`, `_RUN2.txt`, `_RUN3.txt`:
  byte-identical outputs (md5 `036a3fcb334c66c43f6d6e73e662a978`).
- `tadv5_reeval/TADV5_RE_RUN1.err`, `_RUN2.err`, `_RUN3.err`: empty.
- `tadv5_reeval/T_ADV5_REEVAL_RESULT.md`: this file.
