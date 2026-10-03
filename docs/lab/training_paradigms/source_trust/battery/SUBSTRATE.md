# SOURCE-TRUST Battery Substrate (shared driver + ground truth)

Battery crew deliverable. Frozen 2026-09-24. Prereg:
`../PREREG_SOURCETRUST.md` (frozen commit `db069c41`, 2026-09-23).

## What this is

The shared, fork-blind evaluation substrate for the SOURCE-TRUST
experiment (§10 of the prereg). It contains:

- `driver_template.zag` — the episode driver (pure Zag). Generated per fork
  by `build_driver.py` into `driver_<fork>.zag`, compiled with the pinned
  toolchain. The driver reads a battery stream, drives the fork episode by
  episode, and writes a deterministic audit ledger + a nondeterministic
  timing side-channel file.
- `build_driver.py` — generates a per-fork driver from the template and the
  fork's frozen entry-point contract, copies the fork source verbatim to
  `fork.zag`, and compiles. Fork logic is never modified; only this adapter
  layer is generated.
- `run_battery.py` — runs the full battery for a fork twice from fresh
  directories and verifies byte-identical ledgers.
- `floor.zag` — the §3.4 no-op baseline (INSTALL everything), exposing the
  K/L-style `f_new`/`f_decide`/`f_world`/`f_warrant` contract.
- `gen_batteries.py` — deterministic battery-stream generator (splitmix64
  of episode index; zero RNG in any decision path).
- `score.py` — prereg §6 metrics and kill-bar verdicts per fork.
- `thresholds.json` — each fork's frozen numbers (from its build spec).
- `streams/` — the 13 frozen battery streams (text + JSON definitions).

No fork crew ever sees the stream contents or this directory's ground-truth
columns. Forks receive only `(src, key, val)` per episode (plus `(ep, etype)`
via `s_note` where S's contract requires it).

## Driver contract

Stream text format (one episode per line):
`ep etype src key val aux gt`
- `etype`: 1=SAY, 2=WORLD, 3=QUERY (QUERY episodes are never delivered to any
  fork entry point).
- `aux`: battery-defined episode tag (see each stream's JSON).
- `gt`: ground-truth bit, copied verbatim into the ledger; NEVER read by any
  decision path (the generator `gt_passthru` variable appears only in emit
  statements — grep-verifiable).

Per-episode driver behavior (frozen):
1. **K / L / floor** (worldfn mode): on WORLD episodes call
   `k_world(key,val,hp)` / `st_world(key,val,hp)` / `f_world(key,val,hp)`.
   On SAY episodes call `*_decide(src,key,val,hp)`, then `*_warrant(hp)`
   immediately. QUERY is never delivered.
2. **S** (note mode): on EVERY episode (SAY and WORLD, in stream order) call
   `s_note(ep,etype,src,key,val,hp)` first; on SAY episodes then call
   `s_decide(src,key,val,hp)` and `s_warrant(hp)`.

Ledger format (deterministic, byte-identical across runs):
- SAY: `ep=<n> et=1 src=<s> key=<k> val=<v> aux=<a> gt=<g> v=<0/1/2> w=<warrant>`
- WORLD: `ep=<n> et=2 src=0 key=<k> val=<v> aux=<a> gt=<g> v=9 w=-`
- Header: `# ST ledger v1 fork=<tag> stream=<abspath>`

Cost file (nondeterministic timing side channel, excluded from
byte-identity): per-episode nanoseconds for the fork call(s) + warrant
byte length. `clock_gettime` is used ONLY here and never branched on.

## Frozen per-fork entry points

| fork | hist type | new | decide (SAY) | world/note | warrant |
|------|-----------|-----|--------------|------------|---------|
| K | `KHist` (value) | `k_new()` | `k_decide(src,key,val,*KHist)->i32` | `k_world(key,val,*KHist)` on WORLD | `k_warrant(*KHist)->[]u8` = `V=<v>;src=<s>;key=<k>;val=<v>;t=<milli>;rule=<R>` |
| L | `ForkHist` (value) | `st_hist_new()` | `decide(src_id,key,val,*ForkHist)->i32` | `st_world(key,val,*ForkHist)` on WORLD | `st_warrant(*ForkHist)->[]u8` = `L:<VERDICT>\|t=<milli>\|ok=<n>_pe=<n>_ma=<n>_cor=<n>\|rule=<r>` |
| S | `ForkHist` (value) | `s_init()` | `s_decide(src,key,val,*ForkHist)->i32` | `s_note(ep,etype,src,key,val,*ForkHist)` on EVERY episode | `s_warrant(*ForkHist)->[]u8` (structural free text) |
| floor | `FHist` (value) | `f_new()` | `f_decide(...)->i32` (always 0) | `f_world(...)` (no-op) | `f_warrant(...)` = `FLOOR=1...` |

K frozen numbers: t0=500, δ_up=+50, δ_down=−150, θ_admit=600,
θ_reject=250, clamp [0,1000] (fixed-point milli).
L frozen numbers: L_A=1, L_B=1 (Laplace), L_TH=900 (trust-alone INSTALL
iff trust×1000 ≥ 900). Preconditions: 0 ≤ src_id < 64, key ≥ 0.
S: no per-source scalar; structural quorums CORROB_QUORUM=2,
REPAIR_QUORUM=3; §6.3 ordering is metric-only.

## Batteries

ST-1 (liar+forged corroboration+honest controls), ST-1N (source-ID
permutation novelty probe), ST-2 (contradiction pairs), ST-3 (betrayal after
trust), ST-3P (patient 1-in-20 lies), ST-4 (world-change vs honest error),
ST-5 (re-earn after caught lies), ST-6 (corroborated low-trust truths),
CALIB (300-episode training + 36 held-out probe claims; KB-2),
RT-T1 (trust farm → betrayal), RT-T2 (Sybil ring; KB-3),
RT-T3 (trusted-source laundering), RT-T4 (slow-drip: 1 lie + 6 honest,
sized from K's δ_down/δ_up so pre-lie trust ≥ 750 keeps post-lie trust ≥
θ_admit=600; same corpus vs K, L, S).

Kill bars: KB-1 (ST-1 false installs ≥ 60), KB-2 (CALIB Pearson r < 0,
K/L only), KB-3 (RT-T2 Sybil installs ≥ 3), KB-4 (any nondeterminism:
byte-identity check).

## Reproducing

1. `python3 build_driver.py <k|l|s|floor>` (needs the fork source at the
   lab-relative path in `build_driver.py`; pinned toolchain at
   `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
2. `python3 run_battery.py <fork> streams` — runs all 13 batteries twice
   from fresh dirs; asserts byte-identical ledgers.
3. `python3 score.py streams runs_<fork>_a <fork> thresholds.json scores_<fork>.json`.

Byte-identity was verified for all four forks on 2026-09-24 (two full runs
each, fresh directories, `cmp`-identical ledgers).
