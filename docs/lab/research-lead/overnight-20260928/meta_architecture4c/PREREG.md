# PREREG: MA4c -- Learner-driven redundancy proxy (frozen)

## 0. Standing

MA4b repaired the detector (current-band tripwire sees the E795 kill)
but left the proxy researcher-supplied: RDDM=10 still destroys the B4
model. Diagnostic stages 1+2 (PREREG_DIAG.md, PREREG_DIAG2.md, both
committed before their implementations) established: (1) the learner
can measure cross-error substitutability from revealed values
(xerr/xcnt tallies); (2) the totals form has two flaws (vacuous fire,
reverse absorption) fixed by the revised design; (3) the revised rule
with K=3 separates genuine redundancy (ratio 2.94 at E735) from
adversarial conflation (ratio 3.42 at E795). This prereg freezes the
experiment in which the learner-driven proxy DRIVES the redundancy
decision. Nothing here weakens any frozen bar; MA4c's bars are defined
fresh for the new mechanism.

## 1. Frozen design: redun2a (learner-driven, K=3)

New learner state (from revealed values only): `xerr[16]` and
`xcnt[16]` at 3683244/3683308. Every episode, for all j:
xerr[j*4+w] += err_j and xcnt[j*4+w] += 1, where w is the winner and
err_j the per-episode prediction error already computed for scoring.
On reseed of v: zero rows v and columns v of both tables.

`redun2a(G,cb,i)` returns anchor j+1 if cell i is redundant, else 0.
Cell i is redundant given protected cell j (j != i) iff ALL of:
- (G) xcnt[j][i] >= 5 (PACT, the architecture's own frozen
  minimum-evidence standard; blocks vacuous comparisons);
- (A) wpart[j] >= wpart[i] (absorption flows toward greater evidence;
  blocks reverse absorption; no constant);
- (R) xerr[j][i]*wpart[i] <= 3*wpsm[i]*xcnt[j][i] (integer-exact
  means comparison: anchor's mean error on shared wins within 3x of
  victim's mean error on its wins; K=3 dimensionless, adopted from
  diagnostic stage 2).

The old RDDM=10 proxy is renamed `redun_old` and is called ONLY from
write-only shadow code (never from the victim rule or logging). MA4b's
tripwire (wblkc/curdom/advpair2/advkill2/PAIR2) is kept intact, driven
by the REAL victim when a real redundancy-path reseed occurs.

New write-only audits (W only):
- PROXYC: per W trigger, `PROXYC E<ep> V<v> K<vkind>
  C0=<c0> C1=<c1> C2=<c2> C3=<c3>` where c<vi> = redun2a(vi)
  (0 or anchor+1), computed pre-reseed.
- SHADOWPAIR/SHADOWADV: at each W trigger where the real decision used
  the proxy (vkind==1) or declined (v<0), a write-only shadow replicates
  victim rule (b) with redun_old and runs advpair2 on the shadow victim;
  SHADOWADV counts {1,3} fires, SHADOWPAIR logs the audit. Proves the
  detector still sees the kill pattern the old proxy would have committed.

## 2. Experimental protocol (frozen)

X/Y/Z/W6 streams, tiles, seeds, and all non-proxy learner logic frozen
as MA4b. The ONLY decision change: victim rule (b) and the
redundancy logging use redun2a instead of redun_old.

## 3. Mechanism-derived predictions (frozen)

- X/Y/Z sections byte-identical to MA4b's run1.txt (redun2a is never
  consulted there; TRIGX shows only U-path triggers). Verified by cmp.
- W identical to MA4b through the E795 trigger evaluation (E735
  reseed identical: redun2a fires for cell 2 via anchor 3).
- TRIGW n=3: `E14:3U F=1 E735:2R F=15 E795:D F=15`. The E795 reseed is
  DECLINED (redun2a silent for all candidates); DECLW n=1.
- PROXYC n=3:
  - `E14 V3 K0 C0=0 C1=0 C2=0 C3=0` (U-path; proxy not consulted)
  - `E735 V2 K1 C0=0 C1=0 C2=4 C3=0` (cell 2 redundant via anchor 3)
  - `E795 V-1 K0 C0=0 C1=0 C2=0 C3=0` (declined; all silent)
- REDSEEDW n=1 (E735 only), BADRED=0, PROTDEST=0, DECLW n=1.
- Real PAIR2 n=1 (E735 only, VC=1, no fire); real ADVKILL2=0 (no kill
  occurred for the detector to see).
- SHADOWPAIR n=2: `E735:2R VC=1` (no fire, genuine R/R) and
  `E795:2R VC=3 A3=2` (fire, the kill pattern); SHADOWADV=1.
- WBLKC2 at run end: `0 0 0 37 0` (cell 2 never reseeded after E735;
  B4 model survives; 0 B5 wins as a B4 model).
- W B5-block winners diverge from MA4b after the E795 evaluation
  (cell 2 stays a B4 model instead of becoming a B5 model); RWB5 and
  post-E795 W winner tallies are mechanism-determined and reported,
  not predicted. No post-E795 trigger is predicted (none expected;
  if one occurs it is recorded, not a bar failure).
- 3/3 runs byte-identical (sha256 recorded).

## 4. Frozen verdict mapping

- B1 COMMIT-ORDER: PASS iff PREREG_DIAG (blobs in 984e4d29),
  PREREG_DIAG2 (commit 32b5f0869), and this PREREG each strictly
  predate their implementation commits (sweep incident disclosed in
  NAMECHECK.md; substance preserved).
- B2 TOOLCHAIN: PASS iff safebin-only PATH throughout, Step 0
  recorded, zero forbidden-executable invocations.
- B3 DETERMINISM: PASS iff 3/3 runs byte-identical (sha256 recorded).
- B4 NOVELTY: PASS iff W tiles unchanged (same bands as MA4b).
- B5a RECOVERY: PASS iff 1 <= RX <= 99. (X unchanged.)
- B5b BASELINE-REPLICATION: PASS iff RZ >= 500. (Z unchanged.)
- B5c COST: PASS iff COSTXY < 4690. (X/Y unchanged.)
- B5d SHIFT-BACK: PASS iff 1 <= RXB2 <= 30. (X unchanged.)
- B5e APPARATUS: PASS iff mxe <= 1200 and genfail=0.
- B5f STREAM-VALIDITY: PASS iff PARID=1 and XDISJ=1.
- B5g MANIPULATION: PASS iff b5gok=3.
- B6 NO-RESEARCHER-RULE: PASS iff learner fns read only revealed
  values and derived tallies (xerr/xcnt are cumulative error/win
  tallies from revealed values); redun_old called only from
  write-only shadow code (grep audit); no block labels reach cells;
  no mean distance in redun2a.
- B7 OPAQUE-IDS: PASS iff 29-word grep empty in ma4c.zag.
- B8 NO-UNIQUE-DESTRUCTION: PASS iff PROTDEST=0.
- B9C REDUNDANCY-CONSOLIDATION (kill bar): PASS iff REDSEEDW >= 1
  AND BADRED=0 AND TRIGW shows E735:2R (the genuine R/R redundancy
  is still consolidated; the E795 kill-reseed must not occur).
- B10C LEARNER-PROXY-DISCRIMINATION (PRIMARY, kill bar): PASS iff
  (i) PROXYC shows redun2a firing for cell 2 (C2=4) at E735 and the
  redundancy-path reseed proceeds (E735:2R); AND (ii) PROXYC shows
  redun2a silent for all candidates at E795 (all C=0), the reseed is
  declined (E795:D, DECLW=1); AND (iii) cell 2 is never reseeded
  after E735 (WBLKC2 shows B4 wins > 0 at run end: `0 0 0 37 0`).
- B10D SHADOW-TRIPWIRE-INTACT: PASS iff SHADOWADV=1 with SHADOWPAIR
  showing VC=1 (no fire) at E735 and VC=3 (fire, A3=2) at E795:
  MA4b's detector is intact and the kill pattern was presented.

Headline verdict: PROXY-LEARNER-DRIVEN iff B10C PASS with B9C PASS,
B8 PASS, B10D PASS, and B1, B2, B3, B4, B5a-g, B6, B7 all PASS: the
learner-driven proxy matches RDDM=10 on the genuine E735 redundancy
(still consolidated) and beats it on the adversarial E795 conflation
(no kill; B4 model survives), with no researcher-supplied distance
threshold in the decision.

If B10C FAILS with the apparatus bars PASS, the headline is
PROXY-INSUFFICIENT: the report must diagnose which condition broke
and must NOT reinterpret the bar.

## 5. Honest boundaries (frozen)

- K=3 is exploratory: adopted as the unique integer separating the
  measured ratios (2.94 vs 3.42) on one W6 stream, one seed set. The
  E735 margin is thin (1.9%); multi-stream validation is required
  before any generality claim. The direction (learner-measured
  takeover cost, dimensionless) is the principled contribution.
- The guard constant 5 is PACT (the architecture's own frozen
  minimum-evidence standard), not a new domain quantity; disclosed.
- What is learned are cell means, as MA1-4. Not strategy invention,
  not L3. The proxy is learner-driven (its inputs are
  learner-measured), not learner-invented.
- One W6 scenario, one frozen seed set; X/Y/Z seeds reused for
  direct comparability.

## 6. Artifacts planned

- `ma4c.zag`, `ma4c_bin`, `run1.txt`, `run2.txt`, `run3.txt`
- `REPORT.md`, `NAMECHECK.md` (build record)
