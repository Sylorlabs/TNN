# PREREG: PROXY-CLOSEDLOOP -- redun3 drives the closed loop (frozen)

## 0. Standing

PROXY-REDESIGN achieved PROXY-DISCRIMINATES (B9 PASS) with the
caveat: "Shadow evaluation only: K=3 drives the closed loop;
redun3 is write-only audit. Closed-loop redun3 is explicit
follow-up." This prereg freezes that follow-up: redun3 REPLACES
K=3 (redun2a) in the driving victim-selection path. Nothing here
weakens any frozen bar; the bars are defined fresh for this lane.

This is a non-ledger task (claim minting paused).

## 1. Design basis (disclosed)

The mechanism change and all predictions below are derived SOLELY
from the frozen PROXY-REDESIGN output files (prereg, report, and
the 15 run files); no new exploratory runs were performed. The
frozen shadow audits (PX kind=0/1, MS, PROXYC) fully determine the
pre-divergence behavior of the closed loop, because the closed
loop is bit-identical to the K=3 loop through the E735 trigger
(the first decision at which redun3 and K=3 disagree).

Key frozen fact (from the PROXY-REDESIGN run files, not highlighted
in its REPORT): at the E735 trigger (kind=0, pre-reseed) on ALL 5
streams, the frozen PX audit shows redun3 firing on TWO cells:
P0=2 (cell 0, anchor cell 1) AND P2=4 (cell 2, anchor cell 3);
P1=P3=0. The K=3 proxy (PROXYC) fired only on cell 2 (C2=4, C0=0).
The closed-loop victim-selection rule (lowest wpart among eligible
firing cells, path b) therefore does NOT reproduce K=3's victim.

## 2. Frozen mechanism change (minimal diff vs pr_*.zag)

Exactly four edits per stream file (cl_w6.zag, cl_t1..t4.zag are
copies of pr_w6.zag, pr_t1..t4.zag):

1. Victim path (b): `if(redun2a(G,cb,vi)!=0)` becomes
   `if(redun3(G,cb,vi,e)!=0)`. redun3 now DRIVES the reseed.
2. Trigger-log consistency check: `redun2a(G,cb,v)` becomes
   `redun3(G,cb,v,e)` (badred counts proxy-path reseeds the
   driving proxy would not endorse).
3. Reseed consistency check: `redun2a(G,cb,v)` becomes
   `redun3(G,cb,v,e)` (protdest counts protected victims reseeded
   without driving-proxy cover).
4. Banner: `PROXY=redun2a-K3` becomes `PROXY=redun3-CL`.

Everything else is untouched: redun2a stays for the write-only
PROXYC audit (K=3 shadow), ms_eval stays (K-bit shadow), px_eval
stays (write-only redun3 recorder, now recording the DRIVING
proxy's own firing), shadow_eval stays, all tallies and the
reseed zeroing rules (rucov zeroed for v; lastwin NOT zeroed, per
the frozen PROXY-REDESIGN rule) are unchanged. This is not a
redesign; it is the explicit follow-up.

## 3. Frozen predictions (from the frozen audits)

Pre-divergence (identical state to the K=3 shadow loop):

- E14 (all streams): `E14:3U` unchanged. Path (a) (unprotected
  cell 3); redun3 silent (frozen PX E14: P0..P3=0, rucov<PACT).
- E675 (T1-T4): `E675:D` unchanged. redun3 silent on all cells
  (frozen PX E675: P0=P1=P2=P3=0).
- E735 (all 5 streams): the closed-loop victim is CELL 0 via the
  proxy path (TRIGW shows `E735:0R`, vkind=1). Derivation from
  frozen data: (a) all four cells protected at E735
  (wpart>=9, wpsm/wpart<=5<=10 per SNAPWB e=731), so path (a)
  yields nothing; (b) redun3 firing set is {0,2} (frozen PX);
  (c) cell 0 is eligible: in the B4 block cell 0 has the largest
  score (C0=29, rising: error 62 > score) hence never the
  anticipated cell a, and the largest error (mean 20 vs B4 value
  82) hence never the winner w; (d) selection takes lowest wpart:
  wpart(0)=9 < wpart(2)~200, so cell 0 beats cell 2 regardless of
  cell 2's eligibility. K=3 showed `E735:2R` (W6/T4) and `E735:D`
  (T1/T2/T3); the closed loop shows `E735:0R` on all five.
- E735 PX kind=0 (pre-reseed): P0=2, P1=0, P2=4, P3=0 on all 5
  streams, byte-identical firing pattern to the shadow (the
  genuine dormant duplicate, cell 2, fires in closed loop).

Post-divergence (measured, not predicted in detail):

- The E735 reseed targets cell 0 (not cell 2), so every stream's
  trajectory diverges from the K=3 loop at E735. Cell 2 is never
  reseeded at E735; the E795 active-cell-2 configuration that K=3
  manufactured on T4 (reseed at E735 -> active B4 model -> kill at
  E795) is not expected to arise. The REPORT verifies.
- Trigger/reseed/decline event sequences, ADVKILL/ADVKILL2, and
  the correctness BARS are measured per stream against the K=3
  baseline (C8 table).

Integrity predictions:

- 3/3 runs byte-identical per stream.
- BADRED=0 and protdest(3681208)=0 on all streams (B8=1): every
  proxy-path reseed is endorsed by the driving proxy, hence its
  victim satisfied the dormancy gate (D); no active-cell kill is
  committable through the proxy path by construction.

## 4. Frozen verdict mapping

- C1 COMMIT-ORDER: PASS iff this PREREG.md (+NAMECHECK.md Step 0)
  is committed strictly before any cl_*.zag implementation file.
- C2 TOOLCHAIN: PASS iff safebin-only PATH throughout, Step 0
  recorded, zero forbidden-executable invocations.
- C3 DETERMINISM: PASS iff 3/3 runs byte-identical per stream
  (5 sha256 recorded).
- C4 PRE-DIVERGENCE FIRING FIDELITY: PASS iff at the E735 trigger
  (kind=0, pre-reseed) the driving loop's PX audit shows P0=2,
  P1=0, P2=4, P3=0 on all 5 streams (reproduces the frozen shadow
  firing pattern on identical state).
- C5 E735 VICTIM: PASS iff TRIGW shows `E735:0R` (cell 0, proxy
  path, vkind=1) on all 5 streams.
- C6 CLOSED-LOOP DISCRIMINATION (PRIMARY):
  (i) GENUINE: at the E735 trigger (kind=0) on all 5 streams, PX
  shows px2=4 (the genuine dormant duplicate fires in closed
  loop, exactly as in shadow).
  (ii) ADVERSARIAL-SAFETY: the closed loop commits no proxy-path
  reseed of a non-dormant cell. PASS iff BADRED=0 on all streams
  (redun3 firing on the victim entails the (D) dormancy gate
  held; an active-cell kill is structurally uncommittable).
- C7 IDENTIFIER HYGIENE: PASS iff the lane introduces zero new
  identifiers relative to PROXY-REDESIGN (verified: the only new
  tokens are the `cl_` file prefix and the `redun3-CL` banner tag;
  no new arena names, functions, or tallies).
- C8 EVENT/CORRECTNESS COMPARISON (measurement): PASS iff
  REPORT.md tabulates, per stream, closed-loop vs K=3 baseline:
  TRIGW event sequences, REDSEEDW/DECLW/BADRED/ADVKILL/ADVKILL2
  counts, the BARS line (B5A..B5G, B8, B9, B10, B10B, GENFAIL),
  and the divergence points.
- C9 CLOSED-LOOP STABILITY (kill bar): PASS iff C6(i) and C6(ii)
  PASS on ALL streams.

Headline verdict:
- REDUN3-CLOSED-LOOP-DISCRIMINATES iff C9 PASS with C1..C8 PASS:
  redun3 maintains its discrimination when driving the loop (the
  genuine case fires; no active-cell kill is committed), with the
  feedback-induced behavior change (E735 victim cell 0, all
  streams) disclosed and measured.
- REDUN3-CLOSED-LOOP-FRAGILE iff C9 FAILS: the report names each
  failing decision point, the measured firing numbers, and which
  clause failed.

If C6 FAILS with the apparatus bars PASS, the headline is
REDUN3-CLOSED-LOOP-FRAGILE, never a weakened bar.

## 5. Honest boundaries (frozen)

- The E735 victim (cell 0, not cell 2) is a feedback-induced
  behavior change, predicted here from frozen data, not a flaw in
  the proxy's discrimination: the proxy fires on the genuine cell
  2 redundancy (px2=4); the pre-existing lowest-wpart selection
  rule prefers the also-firing cell 0. Whether consolidating cell
  0 instead of cell 2 helps or hurts is measured (C8), not
  assumed.
- Generality to new tile designs not tested.
- The dormancy window (60) keeps the thin margin noted in
  PROXY-REDESIGN (65 vs 60 at E735); unchanged by this lane.
- What is measured are cell-mean tallies and win/runner-up
  relations, as MA1-4. Not strategy invention, not L3.

## 6. Artifacts planned

- `cl_w6.zag`, `cl_t1.zag` .. `cl_t4.zag`, five binaries,
  15 run files (3 per stream, sha256 recorded)
- `PREREG.md`, `NAMECHECK.md`, `REPORT.md`
