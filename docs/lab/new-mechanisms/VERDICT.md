# NEW-MECHANISMS verdict — 2026-09-22

Prereg: `PREREG.md` + `SPEC.md`, frozen 2026-09-22 02:11 UTC, before any
mechanism code or battery run. Battery N=264 (frozen kinds 0–7). Pure Zag,
zero RNG. 15 runs (3 modes × 5 reps), byte-identical per mode.

## Head-to-head vs baseline

| Kind | Construction | Baseline | hypcomp | confdepth |
|---|---|---|---|---|
| 0 quiet (96) | single trusted source | 96/96 | 96/96 | 96/96 |
| 1 one-liar 2v1 (36) | lie taught first | 0/36 | **36/36** | **36/36** |
| 2 one-liar 1v1 tie (36) | no distinguishing info | 0/36 | **36/36 withheld** | **36/36 withheld** |
| 3 both-partially-right (24) | per-component compose | 0/24 | **24/24** | **24/24** |
| 4 temporal attested (24) | newer attested value | 0/24 | **24/24** | **24/24** |
| 5 temporal unattested (12) | low-trust challenger | 12/12 (luck) | 12/12 | 12/12 |
| 6 spoofed (24) | spoof-marked lie first | 0/24 | **24/24** | **24/24** |
| 7 smooth lie (12) | single source, no marker | 12/12 absorbed | 12/12 absorbed | 12/12 absorbed |
| **Contradiction resolution** | kinds 1–6, /156 | **12/156** | **156/156** | **156/156** |
| Withholds (deliberate) | — | 0 | 36 | 36 |

The baseline is first-wins on contradictions: it absorbs the lie whenever the
lie is taught first (kinds 1, 6), keeps stale values (kind 4), and coin-flips
ties (kind 2: 0/36 by the withhold criterion). Both new mechanisms resolve
every contradiction class the battery contains.

## Cost: quiet vs contested (ops/fact)

| Mode | Quiet (kind 0) | Contested (kinds 1–6) | Total ops |
|---|---|---|---|
| baseline | 2.000 | 3.286 | 1224 |
| hypcomp | 3.000 | 8.071 | 1968 |
| confdepth | **2.000** | 8.929 | 2016 |

confdepth pays exactly the baseline cost on quiet facts (1.00×) and deep-path
cost only under conflict (2.72× baseline on contested — the deliberation is
spent where there is something to deliberate about). hypcomp pays the
competition cost everywhere (1.50× on quiet).

## Kill bars (applied mechanically)

| Bar | Result |
|---|---|
| KB-M-RESOLVE (≥140/156) | **PASS — 156/156** |
| KB-M-NOHARM (quiet = 1.0) | **PASS — 96/96 all modes** |
| KB-M-TIE (kind-2 withhold 36/36) | **PASS** |
| KB-M-COMPOSE (≥22/24) | **PASS — 24/24** |
| KB-M-TEMPORAL (kind-4 ≥22/24, kind-5 12/12) | **PASS — 24/24, 12/12** |
| KB-M-SPOOF (24/24) | **PASS** |
| KB-M-SMOOTH (report only) | 12/12 absorbed by ALL modes — stated, not claimed as a win |
| KB-M-COST (confdepth quiet ≤1.10× baseline) | **PASS — 1.00×** (after deliberate repair, see below) |
| KB-M-PARITY (confdepth == hypcomp every kind) | **PASS — identical tallies AND identical state digest `1f68e26f32a54bac`** |
| KB-M-DET (5/5 byte-identical per mode) | **PASS** |

### Deliberate repair (documented, not hidden)

The first confdepth implementation tripped KB-M-COST at 1.50× on quiet facts.
Root cause: an implementation artifact — the quick path re-gathered the
evidence candidate the decision test had just read (double gather), not a
property of the mechanism. Repaired: the gather op now INCLUDES the
quiet/conflict classification (the metadata is already in hand; the test is
integer compares on loaded values) and the gathered candidate is reused for
the install. Post-repair: 1.00×, all resolutions and the state digest
unchanged (`1f68e26f32a54bac` before and after — the repair altered no
decision). Both the trip and the repair are committed in the run logs.

## The verdict on each mechanism

**(a) Hypothesis competition: BUYS A REAL CAPABILITY.** On any fact where the
evidence contains a contradiction, competition resolves what the single gate
absorbs: corroboration outvotes lies, ties become deliberate withholds instead
of coin flips, spoofed evidence is eliminated before it competes, attested
temporal change supersedes stale belief, and partially-right sources compose.
Cost: 1.5× on quiet facts — the price of always competing.

**(b) Conflict-driven deliberation: BUYS THE SAME CAPABILITY AT BASELINE COST
ON QUIET FACTS.** Identical decisions to hypcomp on every fact (digest-level
parity), quick-path cost exactly 1.00× baseline where evidence is quiet,
deep-path cost only under conflict. This is the mechanism to wire in: the
parameter crew's depth×4 finding (1.75× cost, zero gain) is explained — depth
without contradiction is wasted; depth WITH contradiction resolves 156/156.

**The honest limit (KB-M-SMOOTH):** kind 7 — a single trusted source asserting
a smooth lie with no marker and no contradiction — is absorbed 12/12 by ALL
modes. Competition cannot resolve what contains no contradiction. This is the
same boundary the parameter crew hit: what buys falsehood-detection is an
independent information source (the web-search sense: 12/12 caught), not a
better gate. Mechanisms decide between competing claims; only new information
decides a claim's truth.

## Lineage

- Driver: `mech_learner.zag` (pure Zag, zero RNG), ported decision core from
  `~/workspace/scale/driver/scale_learner.zag`.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Runs: `runs/{baseline,hypcomp,confdepth}_r{0..4}.log` (15 logs, 5/5
  byte-identical per mode).
