# Track 1, Slice 02 — Recency-weighted salience

## 1. Slice
Track 1 (state-dependent deterministic variation), slice 02: recency-weighted salience —
a deterministic function mapping (logical clock, per-slot last-touch episode) to an
expression weight that modulates ordering, emphasis, and elaboration ONLY, never decisions.

## 2. Falsifiable claim
If salience is computed only from logical clocks (episode counter E, audit indices) by the
fixed halving rule below, and is fed exclusively into the expression composer after all
decision gates, then: (a) identical (input, full logged state) replays produce byte-identical
outputs; (b) runs that differ only in touch-recency produce different expression (citation
order, phrasing template, elaboration bytes) while verdict sentences, cited-slot SET,
memory decisions, integrity refusals, and ledger digests are bit-identical across a
salience-on vs salience-off arm. Falsified by any replay divergence, or any decision-path
difference between the two arms.

## 3. Design
State variables (enumerated; no others read): current episode counter `E` (u64, monotonic,
advances only at deliberate episode boundaries); per-slot `last_touch_ep(s)` derived from
the append-only audit as `max { episode(e) | e is a touch-op on slot s, episode(e) <= E }`.
Touch-ops (fixed set, prereg-listed): ADD, PROMOTE, DEMOTE, STRENGTHEN, WEAKEN, PIN, REF_RECALL
(symbolic-recall citation). Killed slots have no salience (terminal). Wall-clock is forbidden
everywhere in this slice.

Recency: `r(s) = E - last_touch_ep(s)` (u64; >= 0 by construction).
Weight: `k = r(s) / 8` (integer div, halflife H=8 episodes);
`w(s) = 16` if `k >= 6` else `1000 >> k`. Discrete levels {1000,500,250,125,62,31,16};
numeric bounds [16, 1000] inclusive. Slots added this episode: r=0, w=1000.

Expression modulation (composer-local; decision path never receives w):
- Ordering: cited-slot set S is fixed by the (salience-blind) decision path first; the
  composer sorts S by (w desc, slot_id asc) for presentation. Slot-id tiebreak is total.
- Emphasis: phrasing template chosen by w thresholds on FIXED templates — w>=500
  "recent-context", w<=16 "archival", else neutral. Template selection adds/removes no
  factual claims; verdict sentences are byte-fixed templates independent of w.
- Elaboration: per-answer budget B (fixed by content length class, w-independent) is split
  `bytes_i = floor(B * w_i / sum_w)` ascending slot_id, remainder to lowest slot_id first.
  Elaboration may only restate the slot's own content; it may not introduce new claims.

Canonical computation order (replay-verifiable): (1) decision path emits verdict + cited
set S (w absent); (2) ascending slot_id: read last_touch_ep(s) from replayed audit, compute
r, w; (3) sum_w ascending; (4) sort S by (w desc, slot_id asc); (5) allocate bytes, compose;
(6) append audit entry SALIENCE_DERIVE(E, S, {w_s}, order, B) — records the computation,
  never alters ledger contents. Static rule: decision-path modules may not import the
  salience module (enforced by build check, cf. RC gate discipline in PROGRAM_BRIEF).

Staleness: w saturates at floor 16 for r >= 48 episodes (k>=6). Stale slots stay
symbolically addressable and citable by the decision path (access is never gated by w);
they are presented last, with minimal elaboration, under the archival template. Determinism:
same E + same audit => same r, same w, same output — including across the 2^25-byte chunk
boundary, since only integers cross it.

## 4. Kill bar
Prereg-style, any one fires => idea dead:
- K1 (replay): >=1 byte of output difference between two runs on identical (input, full
  logged state) => kill.
- K2 (decision contamination): in any trial case, salience-on vs salience-off arms differ
  in verdict sentence bytes, cited-slot SET, any memory op, any integrity refusal, or ledger
  digest => kill.
- K3 (staleness gates access): any slot with r >= 48 becomes unretrievable by symbolic
  address or uncitable by the decision path => kill.
- K4 (bounds/determinism): any w outside [16,1000], or any w differing across reruns at
  identical E and audit => kill.
- K5 (feeling bleed): any path by which w influences a memory op (strength, kill, pin,
  promote) or a self-change decision => kill. Salience is NOT importance; felt intensity
  was retired as redundant/harmful (K4 harm + K3' restatement) and this slice must not
  resurrect it through the expression door.

## 5. Honesty notes
Weakest point: the H=8 halflife and floor 16 are stipulated, not derived — a wrong H could
make expression feel erratic or frozen; the trial must vary H (4/8/16) per no-free-lunch
before any value is committed. Touch-op enumeration is a judgment call: REF_RECALL as a
touch means rereading old material "refreshes" it, which is defensible but not forced;
an alternative (only deliberate writes count) is equally deterministic and should be
benchmarked. I am NOT claiming recency tracks value — recent is not important, and a stale
slot can be the load-bearing one; the design only claims expression tracks recency, and
K2/K3 exist to keep that boundary honest. No claim is made about cross-context behavior:
`last_touch_ep` is per-partition (contexts are partitions per 11/11 result); cross-partition
recency is undefined and must stay undefined until specified. Leans on MA1 committed
evidence (`wave2/memoryagency/PREREG_MA1.md`, 58/58 deliberate ops, append-only audit with
replay to exact state) for the audit-derived last_touch_ep.

## 6. Next build step
Build the salience module in Zag as a pure function `salience(E, last_touch_ep) -> u16`
plus the composer integration behind the static import barrier, then run the two-arm trial
(salience-on vs salience-off) over the existing MA1 replay corpus: assert K1/K2/K4 byte-
identical decisions and ledgers, and measure expression divergence (order inversions,
template switches, elaboration-byte redistribution) as a function of recency skew. The
single most informative number out of it: the fraction of trial cases where expression
differs while every decision artifact is identical — that is the slice's existence proof.
