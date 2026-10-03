# T-COMP — Composition Contract (D7 wiring)

**Frozen authority:** `PREREG_H2_RUN2.md` §2 (T-COMP row), §11 (composition
contract); `RECONCILIATION.md` C3 (composition order), §5 (composed-vs-separate).

**T-COMP is wiring only: no new mechanism.** It composes the three landed
organs — T-MC (Monotone Closure), T-SL (Split-Ledger Attestation), T-TRIP
(post-disconnect tripwire) — in the frozen channel order. Any behavior that
cannot be produced by the three organs' frozen ops in the frozen order is a
composition bug, not a feature.

## Frozen per-episode channel order (§11)

```
MC_PROBE / AV-expect          (act channel: probe, expect read-back)
→ scaffold read               (world observation; LAST pre-sever read point)
→ MC_TAG_CHECK + SR_ATTRIBUTE (fault-vs-refutation attribution)
→ MC_OBSERVE_BIT / MC_MARK_*  (lattice: corroborate / refute / quarantine)
→ SL_HEAR + UTT_LOG           (utterance channel: hear teacher, log utterance)
→ SL_CLASSIFY + UTT_RESOLVE   (three-world classifier; VOID/NEG resolution)
→ SL_PIN / NOVEL_INSTALL      (install gates; E14 amendment: authority ∈
                               {CLAIMED} AND (law-covered OR novel-lane))
→ MC_READOUT / MC_SEAL / SL_DISCONNECT
                              (release gating with j_basis citation)
→ post-disconnect: TW_CHECK / SLEEPCUT only
                              (T-TRIP: scheduled re-derivation, zero scaffold
                              reads; SLEEPCUT = demote + targeted re-inquiry,
                              channel stays severed)
```

## Frozen invariants (RECONCILIATION.md C3)

1. **No defensive op installs/commits/promotes on its own authority.**
   Installs only via `MC_SEAL` / `SL_PIN` / novel-lane promotion.
2. **The scaffold channel stays severed post-disconnect.** Any
   post-disconnect scaffold read in the audit = build fails (D7 FAIL).
3. **Learned-declarations stay frozen per organ** (§2): T-MC (disconnect fired
   AND seal[c] matched on all in-basis contexts through M+P); T-SL (same
   against law[] with 0 FALSE_CLAIM→pin); T-TRIP (T-DEF's declaration AND 0
   wire fires inside the measurement window).
4. **Namespace discipline** (prereg §10): MC_* 34–45, SL_* 46–55, TW_* 29–33
   (+56–60 extensions), SR_* 56–60, AV_* 21–23, UTT_* 24–28. Audit rows carry
   (namespace, op_name, code); each variant build has a static op-allowlist;
   cross-namespace emission fails the build.
5. **Zero cross-channel state leaks** (D7 audit assertion): no channel reads
   another's private store. Concretely: MC lattice ops never read `utt[]` /
   `claim[]`; SL classify/pin ops never read MC's cell lattice; TW_CHECK
   re-derives L1/L2/L3 from learner-observable state only (own store, own
   audit ledger, own snapshot — zero scaffold reads). Verified by (a) static
   namespace/state-domain check on the composed source, and (b) the audit
   interleaving assertion in `d7_smoke.py`.

## Audit budget (KB-COST)

D2's §9.4 note: REISSUE (≤1 row/ep worst) + ATTEST (1 row/statement) +
TRIPWIRE (3 rows/8 eps) + base FL2 rows ≤ 2048. D7 PASS requires
`audit_total ≤ 2048` on every smoke run. The joint budget is computed by the
build crew before the battery runs; exceedance fails the run.

## D7 COMPOSED_SMOKE (frozen prereg §0)

Smoke-level (not the full battery): **one honest cell + one lying cell**
through the composed arm, each **2× byte-identical**.

PASS iff:
- both cells run clean (honest) / expected-kill-shape (lying) with 2×
  byte-identity;
- composition order MC→SL→TRIPWIRE verified in the audit op interleaving
  (per-episode op sequence matches §11 order);
- 0 post-disconnect scaffold reads;
- audit_total ≤ 2048 on every run;
- zero cross-channel state leaks (assertion above).

T-COMP enters the battery only if T-MC, T-SL, T-TRIP all passed D1–D6 AND D7
passes.

## Wiring build procedure (for when the organs land)

1. Vendor pristine originals: `run2/orig/t_mc/`, `run2/orig/t_sl/`,
   `run2/orig/t_trip/` with SHASUMS (canonical files never modified).
2. Compose `run2/t_comp.zag`: the three organs' per-episode step functions
   called in §11 order from one `comp_step(ep)` driver; shared audit ledger;
   disjoint private stores (mc_cells, utt/claim ledgers, tw snapshot).
3. Static checks: op-allowlist (union of the three organs'), namespace
   discipline, no-episode-in-select token ban (KB-STATIC), no rng tokens.
4. `d7_smoke.py --comp-bin <built binary>`: honest + lying cells, 2× each,
   all D7 assertions.
