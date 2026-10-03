# REPORT: Hybrid Widening -- Verdict HYBRID MATCHES BEST

Date: 2026-10-02. Worker: hybrid-widen (coverage-directed widening follow-up).
Battery: 6 problems (D0-D3 replayed from WIDEN-COMP, D4/D5 new), 3 arms
(F fidelity, C fidelity, H hybrid), pure Zag, pinned znc.
Prereg committed alone before implementation (6c944a53b).

## Verdict: HYBRID MATCHES BEST

All kill bars K1-K8 pass exactly as frozen, 3/3 byte-identical per arm. The
hybrid inherits C's selective wins and F's blind robustness, and pays only
the preregistered D2 spurious price that Section 3b of the prereg proved
unavoidable for the first-miss trigger family.

## Results

Format: ANS / TRIES / WIDEN / WTRIG / INTER ; WBACK in parentheses for H.

| Prob | F observed (predicted) | C observed (predicted) | H observed (predicted) |
|------|------------------------|------------------------|------------------------|
| D0 | 2/3/0/0/34 (2/3/0/0/34) | 2/3/0/0/34 (2/3/0/0/34) | 2/3/0/0/34 (0) |
| D1 | 2/7/1/1/44 (2/7/1/1/44) | 2/2/1/2/44 (2/2/1/2/44) | 2/2/1/2/44 (0) |
| D2 | 2/3/0/0/-1 (2/3/0/0/-1) | 2/5/1/2/-1 (2/5/1/2/-1) | 2/5/1/2/-1 (0) |
| D3 | 44/2/1/1/44 (44/2/1/1/44) | -2/1/0/0/-1 (-2/1/0/0/-1) | 44/2/1/1/44 (1) |
| D4 | 47/10/1/1/47 (47/10/1/1/47) | -2/1/0/0/-1 (-2/1/0/0/-1) | 47/10/1/1/47 (1) |
| D5 | 2/13/1/1/44 (2/13/1/1/44) | 2/6/1/2/44 (2/6/1/2/44) | 2/6/1/2/44 (0) |

Every cell matches its frozen prediction exactly, including WBACK.

## Kill bar results

- K1 REPLAY: PASS. H on D0-D3 = (2,3,0,0,34), (2,2,1,2,44),
  (2,5,1,2,-1), (44,2,1,1,44) with WBACK=1 on D3 only. F and C on D0-D3
  reproduce the WIDEN-COMP frozen values exactly (fidelity of this lane's
  copies confirmed).
- K2 NEW PROBLEMS: PASS. D4: F (47,10,1,1,47), C (-2,1,0,0,-1),
  H (47,10,1,1,47) with WBACK=1. D5: F (2,13,1,1,44), C (2,6,1,2,44),
  H (2,6,1,2,44) with WBACK=0. Tried-sets, WADD lines, and INTER sequences
  all as frozen: D4's backstop tries 9 rejected pairs in id order
  (INTER 44,44,44,-2,-2,-2,47,47,47) succeeding at (2,3); D5's R1 admits
  WADD=(2,0),(2,1),(2,3) on the try-3 X miss and succeeds at the third.
- K3 MATCH-BEST: PASS. H's try count equals the better pure arm's on D0
  (3=3), D1 (2, C), D3 (2, F), D4 (10, F), D5 (6, C); on D2 H equals C
  (5 tries; the preregistered Section 3b price). H's ANS is correct on all
  six problems (F is 6/6, C is 4/6, H is 6/6).
- K4 BACKSTOP LOAD-BEARING: PASS. WBACK=1 appears on D3 and D4 and on no
  other problem. On D3/D4 the successful pair (X,Y)/(2,3) is filter-rejected:
  X's teach-time outmask is {2} (visible in C's D4 CENSUS: m2 outmask=2,
  n=1, no success growth since C failed there), contradicting kout=1, so X
  is never admitted in any position and the pair is tried only because the
  backstop's condition (filter-rejected and untried) selected it. C's -2 on
  D3/D4 verifies that without R2 the hybrid fails there. The backstop is
  therefore observable and load-bearing, not dead code; "just C-with-retries"
  is falsified.
- K5 LEDGER: PASS. F ledgers all zero on all problems. C ledgers: D1 m0
  out=1; D2 m0 out=1; D5 m2 out=1; else zero. H ledgers: D1 m0 out=1;
  D2 m0 out=1; D5 m2 out=1; D0/D3 zero; D4 m2 out=1 AND m3 in=2 out=2
  (backstop-phase misses recorded while R1 was disarmed, exactly as
  frozen: the (0,3) trial recorded (Y,in,2),(Y,out,2); the (2,0) trial
  recorded (X,out,1)).
- K6 DETERMINISM: PASS. 3/3 byte-identical whole-output per arm.
  Run digests: F f2045ba1d73c6d806716d7d5c321d1f75bcc4fcef8694f843ea3f9593ace560c,
  C b842ae66ae18f3d4e5c69dafd718c38b87210eae313a3cec343b464cace3b862,
  H 19b05a215833c0b8ba6d7576837416d92e6f13ba60a0cad006e300ca85b6ef66.
  Binary digests: F 09406df1a139fdb44f224fe74ec7f27d93eb6d1696e6dfd51ef9085aa792e95f,
  C 0f4c0c243bbd26d02f19238c6f0605f48b52020df62233e4a1d18ceb7a929d23,
  H dfde4fcbf74a844b7fca2e29704285e5d77f8833936d7a39df351a2d1c80ef9a.
- K7 NO-MODE AUDIT: PASS. One composer in h_hyb.zag; R1 fires on (failed
  trial AND new miss bit AND backstop not engaged), R2 fires on
  (admitted-exhaustion AND no success AND not yet engaged). No identifier
  selecting widening policies exists in code (grep for policy/mode/arm over
  non-comment lines: zero hits). The wom call-site constant (1 in the
  admitted sequence, 0 inside widening/backstop) is structural, as disclosed
  in WIDEN-COMP, and the backstop disarm rides on it.
- K8 HYGIENE: PASS. Zero em/en dash bytes in all docs (byte-verified);
  safebin guard attested in NAMECHECK.md Step 0 (which python3/python return
  NOTHING); pure Zag for all scientific computation; pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1.

## The decomposition theorem, confirmed empirically

The prereg's Section 3b predicted the hybrid's behavior exactly, and all 18
cells confirm it:

- Where C succeeds (D0, D1, D2, D5), H's trace is byte-comparable to C's:
  identical tried-sets, try counts, WTRIG=2, WADD lines, and Phase-S ledgers.
  R2 never engages (WBACK=0).
- Where C fails (D3, D4), H's try count equals F's exactly (2 and 10):
  |H| = |A|+|S|+|B| with S empty and B = R, so H = F's admitted phase plus
  F's blind retry, with WBACK=1 marking the handoff.
- D2 is the preregistered price: H = C = 5 tries vs F = 3. The D1/D2
  indistinguishability argument stands: no first-miss-triggered selective
  rule can take D1's win (7 to 2) without paying D2's cost, and delaying the
  trigger collapses the win. This is a property of the trigger family, not
  an implementation defect.

Consequences: the hybrid is never worse than the worse pure arm on any
problem, matches the better pure arm on 5 of 6, and is correct on 6/6 where
C manages 4/6. HYBRID WINS was preregistered as unreachable and was not
observed (no cell shows H strictly better than both arms), consistent with
the theorem rather than against the hybrid.

## Why this matters

WIDEN-COMP left the two widening policies as alternatives with complementary
failure modes. The hybrid shows they compose without interference: the
selective rule handles the observable-evidence regime, the blind backstop
handles the unobservable-evidence regime, and the handoff condition
(admitted-exhaustion) is itself learner-observable. The backstop fired
exactly where the prereg said it must (D3, D4) and nowhere else, which is
the observable signature that the hybrid is genuinely two mechanisms rather
than C with a vestigial retry.

## Architecture accounting

- Cognition lines added: ~335 (h_base.zag, mostly the WIDEN-COMP base plus
  D4/D5 setups and the wback field) + ~99 (h_fail.zag) + ~196 (h_cov.zag)
  + ~230 (h_hyb.zag, the hybrid composer: R1 selective widening plus the
  R2 backstop).
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- Researcher-owned: behavior implementations, world facts/teaching, the two
  trigger rules (the variable under test), the six frozen problems.
- Learner-owned: kind-set contracts, missbits ledger (including
  backstop-phase misses), admitted/widened/tried sets per query, grown
  contracts on success.

## Honest limitations

- Six problems discriminate the widening policy; they do not establish
  generality of the hybrid.
- missbits is per-query; cross-query learning uses only the shared
  Amendment-2 success-recording. A persistent coverage ledger is untested.
- The D2 spurious price is proved unavoidable only for the first-miss
  trigger family; other trigger families (e.g. confidence-weighted) are
  untested.
- Expected-answer verification still used (canonical boundary).
- The fidelity arms F and C are copies extended to D4/D5; their D0-D3
  outputs reproduce WIDEN-COMP exactly, confirming the copies are faithful.

## Follow-ups (not claimed)

1. Adversarial worlds where R1 fires and R2 also engages in one query
   (selective widening fails, backstop succeeds): the event ordering
   WTRIG=2 then WBACK=1 is implemented but untested.
2. Persistent missbits across queries: does the ledger become learner-owned
   long-term knowledge that changes admission on later queries?
3. Characterize when selectivity helps vs hurts as a function of contract
   shape (D2 generalized), to bound the spurious-price regime.
