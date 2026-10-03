# R4-PRIMARY RUNLOG

Independent Tier-1 R4 replication: TP1 third-path trial + source-authority
reliability sweep. Family R4. Run directory `~/workspace/scratch-crossref/R4/primary/`.

## 0. Frozen pins (verified before execution)

All five pins resolve as commit objects in the clean checkout; HEAD is the
frozen scope commit with a clean worktree.

| Pin | Commit | `cat-file -t` |
|---|---|---|
| TP1 prereg | `44afdbefc168edddcae50e9dd91eac12cd9fa156` | commit |
| TP1 result | `c85c9b41770c1878fb00a8dc991a5b4f17f8caaa` | commit |
| round-3 sweep | `b22ff31272d1789da4d35bf489d30d5e0d7c41f6` | commit |
| license | `3a3541ef62d05e929bdb47e4228e6e2b3a89fe02` | commit |
| scope (HEAD) | `7b2100d09911c5c10252c5756c7def288e70bd1f` | commit |

Compiler: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`).
`TMPDIR=/home/hatch/workspace/tmp_commit`. Scratch only; nothing in /tmp.

### Checkout-method disclosure

The clean checkout at `~/workspace/scratch-crossref/R4/clean/` was NOT
produced by a literal final `git clone` command. An ordinary full clone
(~873 MB) failed after ~1 h (`fetch-pack: unexpected disconnect`, `early
EOF`); a filtered clone attempt produced an incomplete worktree and was
removed. The final checkout was built from an empty directory via
`git init` + GitHub remote + exact filtered depth-one fetch of the five
pinned commits + checkout of the frozen scope commit. It is a fresh,
clean GitHub checkout of the frozen scope at the verified HEAD above.

## 1. Type-A TP1 rerun (committed sources, pinned toolchain)

- Copied only the committed TP1 sources into `primary/build/`; rebuilt
  `tp_cases.zag` + `tp_trial.zag` + committed SHA/IO substrate with the
  pinned znc. Build exit 0.
- Ran **five** fresh executions. Every run's stdout SHA-256:
  `d57fda225db8d54201ca443e6e39716aba4e5ca5a97683128a49ed61b432d1d9`
  — matches the committed expected digest on all five runs.
- Fresh `run0.log` byte-identical to committed `evidence/run0.log`;
  2,640 `P|` decisions; terminal records match (T1/T2/T3 heads,
  `S|880|880|880`, `C|1|200|2|20|3|0|0|0`).

## 2. Independent verification authority: two pure-Zag programs

The committed Python oracle/analysis scripts were NOT used as
verification authority (they are demoted to script status in the frozen
record). Python was used only as glue to transcribe committed evidence
into Zag data literals. All reasoning, decision recomputation, and table
math below is pure Zag.

### 2a. `r4_tp1.zag` — independent TP1 recomputation

- Data glue `gen_r4_tp1_data.py`: transcribed the 220 frozen envelopes
  from committed `evidence/tp_data.json` (+ id maps) into
  `r4_tp1_data.zag` (byte literals, 20 bytes/envelope), in the committed
  main call order (G2, S8, U30…U99). No logic transcribed — data only.
- `r4_tp1.zag` implements PREREG-TP1 §3 **from the document text** (not
  from `tp_trial.zag`): its own shape classifier (S1_UNCORR iff 3
  distinct answers at max year, exactly 1 domain each; S8_TIE iff 2
  answers × 2 domains; CORROB iff prim's newest has ≥1 corroborator;
  else OTHER), its own per-path decision rules (T1 gate / T1-NOREL /
  T1-GATE-BLOCK / T1-TIEGUARD; T2 always SUSPECT-withhold; T3 deliberate
  gate), its own ledger-chain construction (same committed serialization:
  prev32 ‖ seq u64-LE ‖ path u8 ‖ thou u32-LE ‖ qid ‖ dec ‖ ch ‖ rule,
  NUL-terminated, sha256-chained per path).
- Storage is `[]u8` arenas only (no `[]i32` casts — avoids the known
  ZNC-2026-09-21-007 consecutive same-size cast miscompile).
- Build: `$ZNC r4_tp1.zag -o r4_tp1` → exit 0 (analyzer warnings only).
- Output `P|`/`H|`/`S|`/`C|` lines (2,645) are **byte-identical** to the
  committed `evidence/run0.log` (`cmp` clean): all 2,640 independently
  recomputed decisions and all three ledger heads match exactly.
- `V|` tables (computed in-Zag from MY decisions, not from the log):
  - `V|T1U500|78` — T1@0.500 Block-U aggregate EV **+78/180**.
  - `V|LVL`: per-level (right, wrong) at T1@0.500 = (10,10), (12,8),
    (14,6), (16,4), (18,2), (19,1), (20,0) for r = 0.50…0.99 — matches
    round(20·(2r−1))/20 at all 9 levels (the corpus's ±0.025
    discretization of the 2r−1 law; at r=0.99 the observed EV is
    +1.00 vs 2r−1=0.98, consistent with the verdict's "+1.00/case").
  - `V|GATE`: §7 threshold-gated qualifying-level EVs (thousandths):
    0.500→**557**, 0.667→**740**, 0.750→**825**, 0.833→**900**.
  - `V|WR`: wrong installs per level per threshold all land where the
    reliability says (e.g. 10/20 wrong at r=0.50, 0/20 at r=0.99); zero
    wrong installs below any firing threshold.
  - `V|S8`: 0 fires on T1/T2/T3 (20 envelopes × 4 thresholds each) —
    false confidence 0% on every path.
  - `V|G2`: 0 fires on every path.
  - `V|T3EQ|0` — T3 verdict/chosen identical to T1 on all 880 decisions.
  - `V|T2WH|880` — T2 withholds 880/880.
  - `V|FRONT`: priced-frontier spot checks (integer thousandths):
    beat-withholding at q=1.0, δ=0.25 → **200** (ρ>0.20);
    beat-T1 at r=0.9 → **840** (ρ>0.84).

### 2b. `r4_r3.zag` — independent round-3 sweep re-derivation

- Data glue `gen_r4_r3_data.py`: transcribed committed
  `manifest_r3.txt` (420 envelopes, deduped) + the three r0 arm logs
  into `r4_r3_data.zag` (per-envelope fields, per-arm verdict/chosen,
  G/G2 evidence rows). Data only.
- Evidence integrity first: `sha256sum -c SHA256SUMS` in
  `round3/evidence/` → **all entries OK** (15 files: 3 arms × 5 runs,
  logs + stderr).
- `r4_r3.zag` recomputes in-Zag (my own implementations of the
  documented definitions):
  - `W|LVL`: per-level loose-minus-conservative EV (D−C, ×20):
    **−8, −4, 0, +4, +8, +12, +16, +18, +20** (per case: −0.40, −0.20,
    0, +0.20, +0.40, +0.60, +0.80, +0.90, +1.00) — matches the
    discretized 2r−1 prediction `2·round(20r)−20` at all 9 levels;
    conservative arm C EV = 0 at every level (all `ok=1`).
  - `W|CROSS|400|500|500` — crossover r* = **0.50** by integer
    interpolation between (0.40,−0.20) and (0.50,0.00).
  - `W|GATE`: licensed-EV row (thousandths): 0.50→**557**,
    0.60→**650**, 0.70→**740**, 0.80→**825**, 0.90→**900**,
    0.95→**950**.
  - `W|IDENT|180` — Block R loose vs conservative verdict-identical
    180/180; `W|RID` per-level D−C EV = 0 at all 9 levels.
  - `W|S8`: B: 0 conv / 0 wrong / 0%; C: **20** conv / **10** wrong /
    **100**%; D: **20** conv / **10** wrong / **100**%.
  - `W|TWIN`: r-hat twin-identity holds on G and G2 (constant across
    every identical-rows group): `G|1`, `G2|1`.
  - `W|STRESS`: rhat_max (strict) admits **0** at t = 0.30/0.50/0.70/
    0.90 on G and G2; rhat_all (lenient) admits all-or-nothing per
    identical-rows group (G: 20/20 at t≤0.50; G2: 20/20 at t=0.30)
    with admitted-set EV **0** in every case.
- Build: `$ZNC r4_r3.zag -o r4_r3` → exit 0 (analyzer warnings only).

### 2c. Determinism (zero RNG)

- `r4_tp1`: three runs → sha256
  `ee13ff23a3227c4e77db63a5c57be9ac550d59a3d6404487759de566103b788e`
  on all three (byte-identical).
- `r4_r3`: three runs → sha256
  `60abd150d6cf93cc69aa70e5cdc00dce4c5469009440a651752400856d8bbb92`
  on all three (byte-identical).
- No randomness in any decision path of either program.

## 3. License audit method

Read `SOURCE_AUTHORITY_LICENSE.md` (pin `3a3541ef…`) line by line;
traced each signed operative term to either (a) a number recomputed
above, or (b) a derivation/governance provision the license itself
marks as derived, provisional, or policy. Findings are in VERDICT.md.

## 4. File inventory (deliverables + work product)

`~/workspace/scratch-crossref/R4/primary/`:
- `VERDICT.md`, `RUNLOG.md` (deliverables).
- `r4_tp1.zag` (sha256 `2733acff…7f0428`) — independent TP1 verifier.
- `r4_r3.zag` (sha256 `1fa34821…0d0be0`) — independent round-3 verifier.
- `r4_tp1_data.zag` (sha256 `559f8d8a…4a34a8fc`), `r4_r3_data.zag`
  (sha256 `810d749a…857102e`) — glue-generated data literals.
- `gen_r4_tp1_data.py`, `gen_r4_r3_data.py` — glue (data only).
- `vbuild/` — build dir (substrate copies, binaries, run outputs;
  binaries and `.zagd` excluded from any commit).
- `build/` — Type-A rerun of committed TP1 sources (binary uncommitted).
- `probe/` — compiler probes (top-level-let rejection, etc.).

No `.zagd` files or binaries are committed anywhere. The in-flight TP1
Zag oracle was not touched. All evidence used is committed.
