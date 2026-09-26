# FIX_DECISIONS.md — blind red-team findings, F6 wedge-fix port

Date: 2026-09-26. Fix workdir: `~/workspace/strength-port-fix/`
(donor port: `~/workspace/strength-port/`, untouched).
Both findings recorded by the blind red team 2026-09-26 against the port's
`port_rt_bin`. Both reproduced on the F6 donor binary
(`~/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin`) → **pre-existing,
not port-introduced**.

## F1 — 64-bit episode identity (u32 aliasing). Status: FIXED.

Attack shapes (pre-fix): `ADD90 CITE0 CITE4294967296` → second CITE 111
(wrapped to 0, collided with episode 0); `CITE2147483648`/`CITE4294967295`
→ 2001 (parsed into i32, failed the `cite_ep<0` guard); spending
`{2^32..2^32+3}` then citing `{0..3}` cross-slot → 121 (consumed-set
matched the truncated low word).

Root cause (end-to-end, not display-level): the driver parsed every CITE
suffix into `i32`; `st_evidence(..., cite_ep:i32)`; the audit ledger stored
the episode in aux (word 2) as one `i32`; duplicate matching, collect/count,
consumption, spent-set keys, checker genuineness, and `last_cite` all used
the truncated word. The F6 donor (`f6_rt.zag`: `let v:i32=0` parse) and the
mainline core (`st_evidence cite_ep:i32`) show the same truncation, so the
bug predates the port.

### Chosen design: signed-56 wire, checked at entry
- EVIDENCE/STRENGTHEN/WEAKEN carry the cite episode as a SIGNED 56-bit
  integer across aux (word 2 = lo 32 bits) and aux2 (word 3 =
  `(hi24<<8)|code`, justification code in the low 8 bits).
- Valid: `0..2^55-1`; `-1` = "no citation" (STRENGTHEN/WEAKEN only).
  `>= 2^55` is refused at entry (`2001`, never truncated).
- Reader sign-extends bit 55, so `-1` and `2^32-1` (both with lo32 =
  `0xFFFFFFFF`) decode distinctly.
- When hi24=0, word3 == code exactly → pre-fix honest EVIDENCE ledgers are
  byte-identical in every fingerprinted word (fingerprint covers
  0,1,2,4,11,17 — never word 3). STRENGTHEN/WEAKEN "no citation" entries
  differ in word 3 only (not fingerprinted, not printed).
- All comparisons use the full 56-bit identity: duplicate matching,
  `st_collect_cites`, `st_cite_consumed`/`st_consumed_list`,
  `st_count_spent_cites`, checker kill/delete/overwrite verification,
  `last_cite` (now `i64[slot_cap]`), replay `last_cite` reconstruction, and
  the P3 last-cite math.
- Driver parses CITE decimals as unsigned 64-bit (exact < 2^64, saturates
  at 2^64-1); ordinary honest episodes keep hi=0, so honest behavior and
  output are unchanged.

### Rejected alternatives
- (a) Widen aux to a second word and break the 21-word audit layout —
  rejected: layout is load-bearing for every tool that reads the ledger.
- (b) `i64` episode as two's-complement 64-bit across two words —
  rejected: only 56 bits are free beside the code byte; 56 bits
  (≈7.2e16 episodes) exceeds any curriculum scale by orders of magnitude.
- (c) Refuse `>= 2^31` at entry — rejected: it would bless the truncation
  instead of fixing it, and the red team explicitly probed `2^31..2^32-1`.

## F2 — over-cite bricking. Status: FIXED.

Attack shape (pre-fix): `ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST` → the
5th CITE accepted; then KILL/DEL/KILLT/OW all 109, RB 108, no un-cite op
exists → liveness lost with integrity intact.

Root cause: the destroy law demands EXACTLY `price` fresh cites
(`cnt==need`); `st_evidence` accepted unlimited distinct cites, so the
(price+1)-th fresh cite made the exact price permanently unpayable.

### Chosen design: (a) refuse the over-cite at CITE time — 122
`st_evidence` refuses a fresh CITE with `ST_REFUSED_CITEFULL` (122) once
the current judgment epoch already has `need = n(high-water)` FRESH cites
attached. The destroy law keeps its exact-price rule (`cnt==need` —
unchanged); the refusal happens before the brick, not after.
- Counts FRESH cites (`total - spent`), not attached cites: after a
  destruction consumed the epoch's cites, the trainer may cite a fresh
  replacement set (mixed stale/fresh recovery keeps working — W5 green).
- The gate uses the exact price `n(high-water)` WITHOUT the P3-baseline
  relaxation: under baseline the destroy rule is already `>= 1`, so no
  exact-price brick exists there and no refusal is needed.
- A later genuine high-water price increase re-opens citing (the refused
  extra cite may be retried once `need` grows).
- Price 0: a cite on a 0-strength judgment is refused as cite-full. No
  honest flow cites at price 0 (the learner kills 0-price judgments with
  zero cites; the C-P3 gate cites once on strength 90).

### Rejected alternatives
- (b) Relax the destroy rule to `cnt >= need` — rejected: it weakens the
  priced-destruction law the whole wedge-fix exists to enforce, and it
  changes every honest destroy's verification semantics.
- (c) Add an un-cite op — rejected: a new mutating op expands the attack
  surface (replay binding, consumption windows, checker coverage) for a
  problem preventable at entry.
- (d) Leave it (integrity intact) — rejected: liveness loss on a
  trainer-reachable path is a real denial-of-service on the judgment.

## Regression probes added (fix battery + driver shapes)
- `0` vs `2^32` vs `2^33` distinct; exact-64-bit duplicate → 111; low
  halves with bit 31 set (`2^31`, `2^32-1`) accepted; `>= 2^55` → 2001.
- High-ID spend then low-ID reuse: accepted (no 121 alias); spent cites
  stay spent; cross-slot reuse of a spent cite still → 121.
- Over-cite: 5th fresh cite → 122 on all four priced paths' setups;
  destruction then succeeds (0); RB still cannot undo CITE (108).
- Fresh-cite replacement after a spent destruction accepted.

## Verification
- Exact red-team failure sequences, re-run post-fix: all fixed (see
  `evidence/reverify/`).
- S1 honest matrix (36 cells) byte-identical vs pre-fix port outputs.
- W1–W8 battery: `fail=0`, two runs byte-identical.
- Trial/gate outputs byte-identical vs pre-fix.
- Static checks: no TNN kill path, zero RNG (grep), deterministic rerun.
