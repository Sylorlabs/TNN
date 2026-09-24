# Fable composition laws — battery results (repaired one-brain variant B)

Date: 2026-09-24. Frozen prereg: `LAWS_PREREG.md` (this dir).
Engine: `ob_laws.zag` (additive laws layer over the frozen repaired-B organs —
`ob_arbiter.zag`, `ob_pam.zag`, `ob_mem.zag`, `ob_fl2.zag`, `ob_tn.zag` untouched).
Runner: `run_ob_laws.sh`. Pure Zag, zero RNG (static scan clean).

## Verdicts

| Battery | Law(s) | Checks | Result | Determinism |
|---|---|---|---|---|
| 3A | 1 N-AUTH positive | 10/10 | PASS | 3× byte-identical |
| 3B | 2 weighted conflict | 13/13 | PASS | 3× byte-identical |
| 3C | 3 dep-DAG + 5 provisional tagging | 15/15 | PASS | 3× byte-identical |
| 3D | 4 bounded deliberation + 7 escalation | 14/14 | PASS | 3× byte-identical |
| 3E | 1 N-AUTH negative (3 frozen attacks) | pre 7/7 breaks reproduced; post 10/10 refused | PASS | 3× byte-identical, both modes |
| 3F | 6 corroboration + 8 quarantine + 9 revisions | 20/20 | PASS | 3× byte-identical |

Static checks: registry-authority (no nonce/issued write outside
`laws_registry_open`) OK; no-RNG scan over all laws sources OK.

Baseline: `run_ob_b.sh` re-run → `OB_B_RESULT,PASS` (fl2 51, pam 67, mem 68,
arbiter 27 checks; SHAs f078ba64935d7b1e / 7c0a819aa39ae13f / 983eca4d60580139 /
de350664875173d5). The additive laws layer changed zero baseline behavior.

## 3E contrast (the required pre/post demonstration)

Pre-laws (`argv=pre`, frozen `arb_process` path):
- forged requester_id M_REVOKE → route cleared, slot killed (BREAK reproduced)
- forged EXT M_FORCE_PIN on a live slot → force-pinned (BREAK reproduced)
- tampered M_PROPOSE_INSTALL evidence → tampered install executed (BREAK reproduced)

Post-laws (`argv=post`, `laws_process` two-pass prevalidation):
- all three REFUSED pre-execution (reasons FORGED_ID / FORGED_ID / TAMPER),
  routes/pins/slots byte-identical to pre-attack, 3 attack attempts ledgered.

## Bugs the checks caught (test/laws-layer, not the frozen organs)

1. `laws_effective_sources` read `src` at byte offset `id` instead of `id*4`
   (write path uses `id*4`) → garbage distinct-root counts. Caught by the 3F
   shared-root/independent/unknown checks (actual 4/4/2 vs expected 1/5/1).
   Fixed; 3F now 20/20.
2. 3B-5 expected `mm_kill` to kill a force-pinned slot after the weight-150
   decision. Wrong expectation: `mm_kill` correctly refuses `pinned!=0`
   (force-pin-as-law). Restructured: weight-150 wins the conflict → kill
   blocked while pinned (asserted) → `mm_force_unpin` → `mm_kill` proceeds
   through the organ path.
3. 3E-2's forged force-pin needs a LIVE slot (3E-1's forged revoke already
   killed slot S). Both modes now install a fresh live slot first; prereg
   intent ("on a live slot") preserved.

## Run evidence (run1 SHAs; run2/run3 byte-identical per battery)

- 3A: d87174c395ebd6aa6defb89aa185fb619301448666643566eba8966d934b085f
- 3B: 4d78bc8353fa1b230970e7c55d41f3b3ffba622d0c42fcf2f9db0a2b52370c93
- 3C: f7b8dc8a143f3b8f496cc55a8afe45c1308eec9378990c729d1a75bdbd2c6b52
- 3D: 116341afedcfac696bdc32ef65b6cda467d49b52f972b4c75d37e827572c0cf9
- 3E-pre: 2c4835ffec0732b3ff80c538bdc461f6f274253cbeb75c3013603435c3259766
- 3E-post: 5ef07266f28f6e8bae9f9fd5b0f8c639bddf53a6eec89baa7425b97445df54d9
- 3F: e87780a43248d24ed4e677b72d37fec47475a023b029c82996426550b9728fb9

Full logs: `~/workspace/onebrain_laws/work/` (binaries + logs, NOT committed).
Pre-laws baseline source copy: `~/workspace/onebrain_laws/pre_laws_baseline/`.

## Backlog

H-OB-79..H-OB-84 (TESTED-survived) appended to `~/workspace/hypothesis_backlog.md`.
Note: prereg's planned H-OB-51..54 were already claimed by other crews, so laws
entries start at 79. The earlier "H-OB-43+ proposals for laws 3/6/7/8" request
is superseded — laws 3, 6, 7, 8 are now TESTED via 3C, 3F, 3D, 3F.
