# REVERIFY.md — blind red-team findings, fix verification (2026-09-26)

Fix workdir: `~/workspace/strength-port-fix/` (donor port
`~/workspace/strength-port/` untouched). Pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Every check below ran twice; outputs byte-identical unless noted.

## Provenance: both findings pre-existing, NOT port-introduced

Both attack shapes reproduce byte-identically on the F6 donor binary
`~/workspace/strength-f6-wedgefix/f6_wedgefix_rt_bin` (built 2026-09-26
from the F6 workstream):
- `G ADD90 CITE0 CITE4294967296` → `RT 2 CITE4294967296 111` (donor)
- `G ADD90 CITE2147483648` → `RT 1 CITE2147483648 2001` (donor)
- `G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST KILL` → `RT 7 KILL 109` (donor)

The donor driver (`f6_rt.zag`) parses CITE suffixes into `i32`, and the
mainline core takes `cite_ep:i32` — the truncation predates the port.

## Finding 1 — 64-bit episode identity (u32 aliasing): FIXED

Mechanism: EVIDENCE/STRENGTHEN/WEAKEN now carry the cite episode as a
signed-56 integer across aux (lo32) and aux2 (`(hi24<<8)|code`); entry
range `0..2^55-1` (else 2001), `-1` = no-citation. All matching —
duplicate detection, collect/count, consumption, spent-set keys, checker
kill/delete/overwrite verification, `last_cite`, replay, P3 math — uses
the full 56-bit identity. Driver parses CITE decimals as unsigned 64-bit.

Verification (fixed `fix_rt_bin`, mode G):
- `ADD90 CITE0 CITE4294967296` → `0, 0` (distinct; was `0, 111`)
- `ADD90 CITE4294967296 CITE4294967296` → `0, 111` (exact-64 dup caught)
- `ADD90 CITE2147483648` → `0` (was 2001); `CITE4294967295` → `0` (was 2001)
- `ADD90 CITE4294967296 CITE8589934592` → `0, 0` (2^32 vs 2^33 distinct)
- `CITE36028797018963967` (2^55-1) → `0`; `CITE36028797018963968` → `2001`
- Cross-slot: spend `{2^32..2^32+3}` via KILL, re-ADD, cite `{0..3}` →
  all `0`, KILL `0` (was 121 on the re-cite path)
- Spent stays spent: re-cite the same `{2^32..2^32+3}` after the KILL →
  cites accepted, KILL `121`

## Finding 2 — over-cite bricking: FIXED

Mechanism (design (a), see FIX_DECISIONS.md): `st_evidence` refuses a fresh
CITE with `ST_REFUSED_CITEFULL` (122) once the epoch already holds
`price = n(high-water)` fresh cites. The destroy law keeps exact-price
(`cnt==need`); spent cites don't count toward fullness; the P3 baseline
path (already `>= 1`) needs no refusal; a later high-water increase
re-opens citing.

Verification (fixed `fix_rt_bin`, mode G):
- `ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST KILL` → cites `0,0,0,0,122`,
  `JUST 0`, `KILL 0` (was: 5th cite `0`, then `KILL 109` forever)
- Same shape with `DEL`, `KILLT`, `OW95` → 5th cite `122`, destruction `0`
- `... CITE4 RB ...` → `RB 108` (still cannot undo a CITE), then
  `JUST/KILL 0`
- Refusal re-opens: `... CITE4(122) STR95 CITE4` → `0` (price grew 4→8)
- Spent-then-fresh: 8 fresh cites at price 8 → 9th `122`, `KILL 0`
- Base shape `ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL` unchanged: all `0`

## Regression: honest behavior preserved

- S1 honest matrix (36 cells: B/C/C-P3/B2 × VUP/WBS/JI × 0/1/2):
  two fixed runs byte-identical; all 36 byte-identical vs pre-fix
  (14 vs committed `evidence/ported/`, 22 vs pre-fix `trial_bin` regen —
  the port's committed evidence covered only 28 files).
- Gates (B/C/C-P3/B2): two runs byte-identical; all 4 byte-identical vs
  pre-fix `trial_bin`.
- W1–W8 wedge battery: `WB_VERDICT fail=0`, two runs byte-identical
  (`evidence/reverify/wbattery_p1.txt`, `wbattery_p2.txt`).
- Focused probes (17): `pass=17 fail=0`, twice byte-identical
  (`evidence/reverify/probes_p1.txt`, `probes_p2.txt`).
- Static: zero RNG tokens in mechanism/checker/learner/trial/drivers
  (only "No RNG" comments); all `st_kill` call sites the 4-arg role-gated
  form; learner calls `st_kill` only with `ST_ROLE_TNN` (→ 113).

## Delivered

- Fixed sources: `strength_core.zag`, `strength_checker.zag`,
  `strength_learner.zag` (i64 `st_last_cite` boundary casts),
  `redteam/fix_rt.zag` (u64 CITE parser).
- `FIX_DECISIONS.md` (designs + rejected alternatives), this file,
  `evidence/` (fixed S1 p1/p2, gates p1/p2, battery p1/p2, probes p1/p2).
- Fresh blind binary (UNCOMMITTED): `redteam/fix_rt_bin` + `redteam/BRIEF.md`
  (same eight objectives; the two fixed shapes listed as regression probes,
  no implementation exposed).
- Not committed: binaries, `.zagd`, `.zag-cache`, regenerable intermediates.
