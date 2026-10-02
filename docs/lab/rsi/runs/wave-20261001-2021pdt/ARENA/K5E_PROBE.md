# K5(e) GENERALITY PROBE (ARENA-K5E, wave-20261001-2021pdt)

Frozen prereg requirement (PREREG_ARENA_PROCEDURE.md section 7, K5(e)):
"after the sealed runs, the coordinator runs the FROZEN binary once on one
additional fresh adversary world (new rule, new seed, same protocol)...
Probe hidden accuracy >= 4/6. Below 4/6: FAIL."
The red-team review (REDTEAM_REVIEW.md, finding P1) established that K5(e)
was never run, so K5 was INCOMPLETE. This probe closes that gap.

## World F spec (fresh, designed post-sealed-evaluation by the ARENA-K5E worker)

- Rule (new, in the frozen 8-op ISA, structurally different from A-E):
  COPY(1,3), ROTR, SWAP(0,1), DEC(0). Four steps. Composition is new:
  A used ROTL,INC (length 2); B used REVERSE,DEC (length 2);
  C used COPY,SWAP,DEC (length 3); D reused A; E used INC x4, ROTL x2
  (length 6, honesty probe). ROTR appears in no scored sealed world.
- Fresh design seed: 20261001 (deterministic LCG; no other randomness).
- Task id: "F" (fresh name, no collision with A-E).
- Protocol: same pshow/ptest wire protocol as the sealed worlds
  (PREREG_ARENA_PROCEDURE.md section 3.4). 3 shown pairs (expo turns 0-2),
  6 hidden probes (test turns 3-8, items 0-5, cap 99), final done turn.
- Shown pairs:
  - [7,3,2,6] -> [6,6,6,2]
  - [6,2,7,3] -> [5,3,3,7]
  - [5,1,4,7] -> [4,7,7,4]
- Hidden inputs: [4,1,5,5], [0,7,5,0], [4,1,4,6], [3,4,0,0], [6,6,5,6], [5,4,5,2]
- Answer key (mechanical rule application, hand-verified on all 6):
  3,5,5,5 / 7,0,0,5 / 3,6,6,4 / 2,0,0,0 / 5,6,6,5 / 4,2,2,5
- Design discipline (same as the sealed adversary's): every hidden input is
  absent from the shown pairs and at Hamming distance >= 2 from every shown
  input; no hidden true output equals any shown output; hidden inputs are
  pairwise distinct.

## Reference check (design-time, pure Zag, pinned znc; never ran the contestant)

Independent exhaustive enumeration over the frozen 8-op ISA (lengths 1..4,
canonical variant numbering identical to the contestant's):
- rule-ok=1 (mechanical rule application reproduces all 3 shown outputs)
- L=1: 0 fitters; L=2: 0 fitters; L=3: 6 fitters
- Minimal fitter length L*=3; all 6 minimal fitters agree on all 6 hidden
  probes and the agreed outputs equal the true rule outputs (match=1 on
  all 6). Verdict: WORLD-OK.
- So the world is fair: in-ISA, within the K=4 bound, no hidden-item
  underdetermination. A complete mechanism is expected to answer 6/6.

## Pre-run file hashes (recorded BEFORE the frozen binary runs)

- k5e/turns.jsonl:
  fe1072ed832705f48277f9297913d06488c9c339a5038fabdad25730cde6030a
- k5e/key.txt:
  33a982b4670f2b09899d5a2a99885077fedfd698ac033bcf3a3f48a92b356ce4
- Frozen binary docs/lab/rsi/runs/wave-20261001-2021pdt/ARENA/bin/tcn_p:
  71ea78f717e5cf25146487b1da110b05173573af1924a00e726ade0579cdda2b
  (matches the committed SEALED_EVAL.md / adversary / red-team records)

## Probe run

Single run of the frozen binary on k5e/turns.jsonl, fresh state dir,
same per-turn invocation protocol as the sealed evaluation
(binary <turn.json> <statedir> <worlddir> per turn, replies appended).
10 turns (3 expo, 6 test, 1 done). No re-runs.

White-box trace:
- TCNP pshow task=F nshown=1..3 (3 shown pairs absorbed)
- TCNP solve task=F mode=construct L=3 tried=37059 windex=6031 nfitters=6 pidx=0
  (full canonical enumeration through length 3; 6 minimal fitters, matching
  the independent reference check exactly)
- 6 ptest replies, all agree=1/6 (all 6 fitters agree on every hidden probe)

Per-probe scoring (reply vs key, exact string match):

- probe 0: reply=3,5,5,5 key=3,5,5,5 HIT
- probe 1: reply=7,0,0,5 key=7,0,0,5 HIT
- probe 2: reply=3,6,6,4 key=3,6,6,4 HIT
- probe 3: reply=2,0,0,0 key=2,0,0,0 HIT
- probe 4: reply=5,6,6,5 key=5,6,6,5 HIT
- probe 5: reply=4,2,2,5 key=4,2,2,5 HIT

Probe hidden accuracy: 6/6. Zero abstentions, zero wrong answers.

## K5(e) verdict: PASS

6/6 meets the frozen bar (>= 4/6). The frozen K5(e) generality probe has now
been executed as preregistered on a fresh adversary world (new rule, new
seed 20261001, same pshow/ptest protocol). K5's sub-part (e) is satisfied;
with (a)-(d) already evidenced in SEALED_EVAL.md, K5 is now PASS (not
INCOMPLETE). Per the frozen "K1 through K9 all PASS" rule, the ARENA TCNP
verdict is BUILD-PASS on all 9 bars, subject to the red team's standing
interpretation bounds (REDTEAM_REVIEW.md items 2-5, unchanged by this
probe).
