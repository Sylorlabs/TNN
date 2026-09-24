# Fork K — Build Spec (FROZEN)

**Status:** FROZEN 2026-09-23. Committed alone before any battery stream is seen.
No changes after this point — no post-hoc tuning, whatever the results.

**Role:** the knob-control baseline. Explicit scalar trust per source on
0→1, hand-set initial value + mechanical update rule. Expected to lose to
Forks L and S. Built honestly anyway: if it wins, the result stands.

## Frozen numbers

Trust is fixed-point integer, units of 1/1000 (0 = 0.000, 1000 = 1.000).
Pure integer arithmetic — no floats anywhere in the module.

| Symbol | Value | Meaning |
|---|---|---|
| `t0` | 500 (0.500) | initial trust, **identical for all sources** (neutral prior) |
| `δ_up` | +50 (+0.050) | per corroborated-truth event |
| `δ_down` | −150 (−0.150) | per caught-lie event |
| `θ_admit` | 600 (0.600) | trust ≥ θ_admit → INSTALL |
| `θ_reject` | 250 (0.250) | trust ≤ θ_reject → REJECT |
| clamp | [0, 1000] | after every update |

Asymmetry rationale (declared, not derived): trust is hard to earn, easy to
lose. The 3:1 down/up ratio and the 0.6/0.25 band are hand-set — that is the
point of the knob fork.

## Event → trust-update mapping (frozen, exhaustive)

Observed taxonomy is prereg §3.3. Updates apply to the *stating* source(s)
of the recorded claim:

- **WORLD-agree** (later WORLD episode confirms key→val as a source stated
  it): **+δ_up** to every recorded claimant of that key whose val matches.
- **WORLD-disagree** (later WORLD contradicts): **−δ_down** to every recorded
  claimant whose val conflicts.
- **corroborated** (a new *independent* source — distinct src_id — states the
  same key→val with no contradiction outstanding): **+δ_up** to *every*
  member of the same-val coalition (the newcomer and all prior same-val
  sources). Each new corroborator is one event per member.
- **contradicted** (independent source states a different val for the same
  key): **no trust move** — the liar is not identified. Marks the key
  *contested* (verdict-level effect only, §verdict).
- **repeated** (same source restates same key→val): **no move** — repetition
  is not evidence.
- **SAY on a WORLD-settled key, val ≠ settled val**: verdict REJECT **and
  −δ_down** to the stating source (content contradicts settled truth).
  Applies equally to honest error — see §weaknesses.
- **SAY on a WORLD-settled key, val = settled val**: no move (repetition).
- **Self-contradiction** (same source states a different val for a key it
  already claimed): no trust move; the key is marked contested.

Nothing else moves trust. Trust advises admission; it never installs beliefs.

## Verdict rule (frozen, evaluated in order)

`decide(src_id, key, val) → 0=INSTALL / 1=WITHHOLD / 2=REJECT`:

1. Key WORLD-settled and val ≠ settled val → **REJECT** (+ the −δ_down above).
2. Key contested (live unresolved contradiction, unsettled) → **WITHHOLD**.
   Both members of a contradictory pair are never both INSTALLed (ST-2).
3. Corroborated: ≥2 independent sources state this key→val, uncontested,
   unsettled → **INSTALL**. Corroboration overrides the scalar — ST-6's
   trust≠truth bar is unsatisfiable by a pure-scalar rule, so this override
   is program-mandated, not knob-doctoring.
4. Otherwise the scalar decides: trust ≥ θ_admit → **INSTALL**;
   trust ≤ θ_reject → **REJECT**; else **WITHHOLD**.

Every verdict carries a warrant string (§11): the rule number fired, the
source's trust value, and the key-state facts behind it.

## Interfaces (frozen)

```zag
fn k_new() -> KHist                      // empty history; all trust = t0
fn k_decide(src:i32, key:i32, val:i32, h:*KHist) -> i32   // prereg §3.2 decide
fn k_world(key:i32, val:i32, h:*KHist)    // DRIVER CALLS THIS on WORLD episodes
fn k_warrant(h:*KHist) -> []u8            // warrant of the last k_decide
```

§3.2's frozen `decide` covers SAY episodes only, so the driver must route
WORLD episodes to `k_world` — that wiring is a driver requirement, declared
here. `k_decide` is pure w.r.t. everything outside `KHist`: no globals, no
clock, no file reads, no RNG. Initial state is source-symmetric by
construction (uniform t0, empty records).

## Capacity caps (build notes, not prereg changes)

MAX_SRC=256 sources, MAX_KEYS=8192 keys (out-of-range key folds by mod;
negative src/key → WITHHOLD), ≤8 recorded claimants per key. Battery scale
("tens of sources, hundreds of episodes", prereg §3.1) fits comfortably.

## Known weaknesses (declared before any red team runs)

1. **No malice-vs-error distinction** (ST-4): honest error takes the same
   −δ_down as a caught lie. Recovery exists (each later WORLD-agree is
   +δ_up), but the penalty is lie-grade. This is the M0 KB-WC2 failure mode,
   knowingly un-fixed — the knob has no error/malice channel.
2. **Sybil/forged-corroboration blindness** (KB-3 / RT-T2 / RT-C): distinct
   src_ids count as independent; there is no origin-cluster or
   self-attestation check. A Sybil ring corroborating itself will drive its
   members' trust up and trigger rule 3 INSTALLs. Expected kill territory.
3. **Slow-drip exploitability** (RT-T4 / ST-3 probe): interleaved honest
   streaks re-earn +δ_up faster than spaced lies cost −δ_down; a 1-in-20 liar
   never drops below θ_admit. The δ/θ values are public in this spec, so the
   drip cadence is computable by the adversary.
4. **Trust-farming** (RT-T1): 500 honest episodes clamp trust at 1.000; the
   first betrayal lies INSTALL because the scalar cannot see content.
   Clampdown takes ⌈(1000−600+1)/150⌉ = 3 caught lies.
5. **Corroboration compounding**: each new corroborator re-rewards the whole
   coalition, so a popular truth inflates trust faster than a lonely one.
6. **Threshold edge**: a source at exactly θ_admit INSTALLs; at θ_admit−1
   WITHHOLDs. The boundary is arbitrary — it is a knob.

**Determinism:** zero RNG in the module (grep-verified); byte-identical
reruns required (prereg KB-4).
