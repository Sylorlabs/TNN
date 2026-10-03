# REPORT: MA4c -- Learner-driven redundancy proxy (frozen)

## 0. Verdict

**PROXY-LEARNER-DRIVEN.** All frozen bars PASS. The learner-driven proxy
(redun2a, K=3) matches RDDM=10 on the genuine E735 redundancy (still
consolidated: TRIGW E735:2R, REDSEEDW=1, BADRED=0) and beats it on the
adversarial E795 conflation (reseed declined: TRIGW E795:D, DECLW=1;
the B4 model survives: WBLKC2=`0 0 0 37 0`). No researcher-supplied
distance threshold in the decision. MA4b's tripwire is intact
(SHADOWADV=1: the old proxy + tripwire still see the kill pattern).

## 1. What changed vs MA4b (frozen, one mechanism)

- New learner state: `xerr[16]`/`xcnt[16]` at 3683244/3683308.
  Every episode, from revealed values only: for all j,
  xerr[j*4+w] += err_j and xcnt[j*4+w] += 1 (w = winner, err_j the
  per-episode error already computed for scoring). Row/column v
  zeroed on reseed of v.
- `redun2a(G,cb,i)` (returns anchor+1 or 0) replaces the
  researcher-supplied RDDM=10 proxy in victim rule (b) and the
  redundancy logging. Cell i redundant given protected j iff:
  (G) xcnt[j][i] >= 5 (PACT); (A) wpart[j] >= wpart[i];
  (R) xerr[j][i]*wpart[i] <= 3*wpsm[i]*xcnt[j][i] (K=3).
- `redun_old` (original RDDM=10) is called ONLY from write-only
  `shadow_eval`; the real decision never consults it.
- New write-only audits (W only): PROXYC (redun2a bits per candidate
  per W trigger) and SHADOWPAIR/SHADOWADV (old-proxy rule (b) +
  current-band tripwire, proving the detector still sees the kill).
- X/Y/Z, tiles, seeds, and all non-proxy logic frozen as MA4b.

## 2. Frozen predictions vs observations (all confirmed)

| Prediction (PREREG.md) | Observed |
|---|---|
| X/Y/Z byte-identical to MA4b | IDENTICAL (cmp) |
| TRIGW n=3 E14:3U E735:2R E795:D | `E14:3U F=1 E735:2R F=15 E795:D F=15` |
| PROXYC E14 V3 K0 all C=0 | confirmed |
| PROXYC E735 V2 K1 C2=4 | confirmed |
| PROXYC E795 V-1 K0 all C=0 | confirmed |
| REDSEEDW=1 BADRED=0 PROTDEST=0 DECLW=1 | all confirmed |
| PAIR2 n=1, ADVKILL2=0 | confirmed |
| SHADOWPAIR n=2: E735 VC=1, E795 VC=3 A3=2; SHADOWADV=1 | confirmed |
| WBLKC2 `0 0 0 37 0` | confirmed |
| 3/3 byte-identical | sha256 `3cf22a2b42b86cb71eb7da16d8e26133385e63d27db145cfa3cc49b04417a971` |

W diverges from MA4b exactly at the E795 evaluation (first diff:
SNAPWB5 cell-2 tallies; B5-block winners redistributed since cell 2
stays a B4 model). RWB5=4 (mechanism-determined, reported not
predicted). No post-E795 trigger occurred.

## 3. Frozen bar results

- B1 COMMIT-ORDER: PASS. PREREG_DIAG (blobs in 984e4d29, 10:46:41
  UTC), PREREG_DIAG2 (32b5f0869), PREREG.md (3432ee8f1) each strictly
  predate their implementations. The sweep incident is disclosed in
  NAMECHECK.md; substance preserved.
- B2 TOOLCHAIN: PASS. safebin-only PATH, Step 0 in NAMECHECK.md,
  zero forbidden invocations.
- B3 DETERMINISM: PASS. 3/3 byte-identical, sha256 above.
- B4 NOVELTY: PASS. W tiles unchanged (same 5 bands as MA4b).
- B5a RECOVERY: PASS (RX=7, 1<=7<=99; X identical).
- B5b BASELINE-REPLICATION: PASS (RZ=624 >= 500; Z identical).
- B5c COST: PASS (COSTXY=1022 < 4690; X/Y identical).
- B5d SHIFT-BACK: PASS (RXB2=4, 1<=4<=30; X identical).
- B5e APPARATUS: PASS (GENFAIL=0; X/Y identical to MA4b which passed).
- B5f STREAM-VALIDITY: PASS (PARID=1, XDISJ=1).
- B5g MANIPULATION: PASS (b5gok=3).
- B6 NO-RESEARCHER-RULE: PASS. xerr/xcnt are revealed-value-derived
  tallies; redun2a reads only revealed values and derived tallies;
  redun_old called only from write-only shadow_eval (grep: 1 call
  site); no block labels reach cells; no mean distance in redun2a.
- B7 OPAQUE-IDS: PASS. 29-word grep empty in ma4c.zag.
- B8 NO-UNIQUE-DESTRUCTION: PASS (PROTDEST=0).
- B9C REDUNDANCY-CONSOLIDATION: PASS. REDSEEDW=1 >= 1, BADRED=0,
  TRIGW shows E735:2R.
- B10C LEARNER-PROXY-DISCRIMINATION (PRIMARY): PASS. (i) PROXYC
  C2=4 at E735, E735:2R; (ii) PROXYC all C=0 at E795, E795:D,
  DECLW=1; (iii) WBLKC2=`0 0 0 37 0` (cell 2 never reseeded after
  E735; B4 model survives).
- B10D SHADOW-TRIPWIRE-INTACT: PASS. SHADOWADV=1, SHADOWPAIR E735
  VC=1 (no fire), E795 VC=3 A3=2 (fire).

Headline: **PROXY-LEARNER-DRIVEN.**

## 4. Honest boundaries (as preregistered)

- K=3 is exploratory: unique integer separating measured ratios
  (2.94 vs 3.42) on one W6 stream. E735 margin thin (1.9%).
  Multi-stream validation required before any generality claim.
  The direction (self-measured takeover cost, dimensionless) is the
  principled contribution.
- Guard constant 5 is PACT (architecture's own frozen
  minimum-evidence standard), disclosed.
- What is learned are cell means, as MA1-4. Not strategy invention,
  not L3. The proxy is tally-driven (inputs self-measured), not
  learner-invented.
- One W6 scenario, one frozen seed set; X/Y/Z seeds reused for
  direct comparability.

## 5. Artifacts

- `ma4c.zag` (frozen source), `ma4c_bin`, `run1.txt`, `run2.txt`,
  `run3.txt` (sha256 `3cf22a2b…`)
- `PREREG.md` (frozen, 3432ee8f1), `PREREG_DIAG.md`,
  `PREREG_DIAG2.md`, `NAMECHECK.md`, this `REPORT.md`
- Superseded diagnostics: `ma4c_diag.zag`, `ma4c_diag2.zag`
  (+ their bins/runs)
