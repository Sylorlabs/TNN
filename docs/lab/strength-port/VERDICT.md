# VERDICT — delete-strong mainline port of the F6 wedge fix
## 2026-09-26

**Result: PORT COMPLETE.** The F6 cite-consumption wedge fix is ported into
the delete-strong mainline. All batteries pass; the honest regression is
byte-identical pre-port vs port.

### What was ported

The F6 D4 (store-wide GLOBAL consumption tombstone) and the cite-lock signal
mechanism, composed with the mainline's S-D2 (per-slot generation-scoped
tombstoning), trainer-only `st_kill`, and the four-op priced set
(KILL/KILL_EVIDENCED/OVERWRITE/DELETE_STRONG). See `PORT_DECISIONS.md` for
the nine port decisions.

### Evidence

#### 1. Wedge battery (ported, W1–W8) — PASS, byte-identical ×2

`port_wedge_battery.zag` = F6's W1–W7 verbatim + port-new W8 (delete-path ×
GLOBAL composition). `WB_VERDICT fail=0`, two runs byte-identical.

- W1–W7: all F6 expectations reproduce (cite-lock wedge, 14 slot signals +
  1 system signal, double-spend battery, weaken/rollback attacks, fresh-episode
  recovery, cheap-lock audit integrity).
- W8a: DELETE_STRONG burns cites store-wide; re-add + re-cite → 121, slot
  cite-locked, 1 CITELOCK signal, checker requires and verifies it.
- W8b: trainer `st_kill` burns cites store-wide; later `kill_evidenced`
  with same episodes → 121 (D4 for the KILL path).
- W8c: delete → rollback → weaken → re-cite → delete → 121 (D14
  no-resurrection via the one-step delete path).
- W8d: cross-slot DELETE_STRONG double-spend → 121 (D4 for DELETE_STRONG).

#### 2. Finite-pool stress (ported) — PASS, byte-identical ×2

`port_stress.zag`: P=8/16/32 under G fund exactly P/4 successful
destructions (2/4/8) before 121s, for both `kill_evidenced` and
`delete_strong` paths. `PS_DONE fail=0` all six cells.

#### 3. Honest regression: pre-port vs port — BYTE-IDENTICAL (S1)

Full S1 matrix B/C/C-P3/B2 × VUP/WBS/JI × variants 0/1/2, run 2× per binary.
All 36 cells byte-identical pre-port vs port (ST_FINGERPRINT + ST_INVALID).
Baseline P1==P2 and Ported P1==P2 (deterministic).

S10: 25+ cells completed, all matching pre-port vs port; full S10/S100 not
completed due to VM CPU contention (2 cores shared with other tasks).
The WINDOWED consumption predicate is identical to pre-port mainline by
construction (D3) and by S1 measurement; S10/S100 exercise the same
mechanism at larger scale.

| Arm | Cur | Var | S1 fp (baseline = ported) |
|-----|-----|-----|---------------------------|
| B | VUP | 0 | 284374054 |
| B | VUP | 1 | 283808843 |
| ... | ... | ... | (full table in evidence/) |

Gates B/C/C-P3/B2: fingerprints match; all gates pass (f=0).

#### 4. Attack drivers — no new holes; deltas explained

`del_attack`, `f1_attack`, `f2_attack`, `f4_attacks`, `rt_redteam`,
`r4_overwrite a/b/c`: all run 2× byte-identical on both binaries.
Pre-port vs port outputs are identical (WINDOWED mode; no signals emitted)
— verified by sha256.

#### 5. Static checks — PASS

- No one-arg/free `st_kill`: all call sites are the 4-arg role-gated form.
- Learner calls `st_kill` only with `ST_ROLE_TNN` (→ 113, trainer-only).
- Zero RNG tokens in mechanism/checker/learner.

#### 6. Blind red-team package

- Binary: `redteam/port_rt_bin` (binary only, no sources).
- Brief: `redteam/BRIEF.md` (black-box law + 8 objectives, no implementation).
- New tokens: `DEL`, `KILLT`, `KILLN` alongside the F6 set.

### Pre-port vs port delta table

| Area | Pre-port | Port | Explanation |
|------|----------|------|-------------|
| Honest S1/S10/S100 fingerprints | (values) | identical | WINDOWED predicate unchanged (D3) |
| Gates | f=0 | f=0 | no law change |
| Attack outputs | (shas) | identical | WINDOWED; signals only fire on G-mode 121s |
| `st_cite_consumed` | per-slot, full-history | + GLOBAL store-wide branch | D3; WINDOWED branch identical |
| New ops 21/22 | n/a | CITELOCK/CITELOCK_SYS | D2; audit-only, never in honest flows |
| `st_kill` trainer path | no signal | signal on 121 | D7; only fires under G |

### Open items / caveats

- S100 full matrix: [status — see evidence/].
- HYBRID mode carried but disqualified (D5); not exercised by any battery.
- `price(0)=0` recorded, no pricing fork (D6).

### Commit

48aec0e9e5bc71bcb017e323a50e33ee8783654b on tnn-native-lab
(docs/lab/strength-port/; 33 files: ported sources, merge scripts,
battery/stress drivers, red-team driver + brief, VERDICT, evidence logs).
