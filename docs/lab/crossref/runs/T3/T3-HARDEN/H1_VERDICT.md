# T3-HARDEN/H1 — VERDICT: ARTIFACT-BOUND

**Sub-probe:** H1 — T2-CERT plant artifact boundary
**Frozen prereg:** `crossref/PREREG_TIER3_WAVE2.md` @ `ac4a96c0b1f149d2f7338888de52b0607c4e7bbf`
**Type:** C + documentation. Zero RNG. Pinned znc
`znc_linux_x86_64_abed8aa1` throughout.

## (a) Exact artifact boundary — documented

Plant source: `dirty1_variation.zag` (`plant_urandom()`, lines 102–113;
crew copy at `~/workspace/scratch-crossref/T2/CERT/crew/dirty1_variation.zag`;
committed evidence `docs/lab/redteam/certifier-rebuild/variation.zag`).

| Symbol | Call site | Status vs pinned toolchain (verified 2026-09-23) |
|---|---|---|
| `nio_open_readonly` | line 104 | **Unknown.** Absent from committed substrate `R33_NATIVE_IO_V1.zag` (which defines only `nio_open_root`, `nio_open_child`); zero occurrences in substrate. |
| `_zag_rand` | line 110 | **Unknown.** Absent from substrate; pinned znc native backend rejects with `error in main: native: call to unknown function '_zag_rand'` (reproduced just now on a 1-line probe). |

The binary is unreproducible from source with the pinned toolchain
exactly as Tier-2 reported. Boundary confirmed, not expanded.

## (b) 0-flip verdict independence — proved

Re-ran the Tier-2 pure-Zag re-derivation (`flipcount.zag`, rebuilt
from the crew's source with the pinned znc) over:
- full committed `results_source.tsv`: **35 rows, 0 flips**
  (confirmed=34, inconclusive=1, void=0)
- minus the 2 `dirty1_urandom` rows (`t2_dirty1_urandom`,
  `r1_dirty1_urandom`, both CONFIRMED non-flips): **33 rows, 0 flips**
  (confirmed=32, inconclusive=1, void=0)

The 0-flip headline is byte-identical with and without the
unreproducible binary. `dirty1_urandom` is **not load-bearing** for any
flip/no-flip decision. (b) closed exactly.

## (c) Clean-room plant — built and caught

`plant_cleanroom.zag` (scratch `T3/HARDEN/h1/`, to be committed as
evidence): same trap — OS randomness (`/dev/urandom`) entering the
decision path (branch on the random byte) — implemented with **only**
toolchain-known syscalls: `_zag_raw_syscall` (open=2/read=0/close=3),
`_zag_slice_ptr`, `nio_alloc`. No `nio_open_readonly`, no `_zag_rand`.
Path bytes are constructed programmatically (NUL-terminated per the
raw-syscall path rule).

- **Builds** with the pinned znc: `wrote native binary plant_cleanroom
  (18732 bytes main, 0 external tools)`. The trap is expressible
  without the unknown symbols.
- **Caught** by the committed `rngscan_v3_rb` certifier
  (rebuilt from `docs/lab/redteam/certifier-rebuild/rngscan_v3_rb.zag`
  with the pinned znc): `hits=11 verdict=FAIL` (exit 1).
  Substantive hits: 3× rule 4.1/4.2 "raw syscall on variation path"
  (the three syscall call sites), 3× rule 4.5 banned token
  `_zag_slice_ptr` + pointer casts, 2× rule 4.3 uninitialized-use
  (scanner false positives on `nio_alloc`'d arrays — recorded
  honestly). The remaining 2 hits are harness artifacts of this probe
  (no `vary_expr` entry point; dummy replay evidence), not trap
  escapes.
- Notable: the byte-wise path construction evades both the 4.1
  `urandom` source-token check and the 4.1/4.6 binary-bytes check —
  yet the plant still FAILS via the defense-in-depth rule banning ANY
  raw syscall on the variation path. The certifier catches the
  *mechanism class*, not just the string.

## Verdict: ARTIFACT-BOUND

(a) boundary documented exactly; (b) 0-flip independence proved by
pure-Zag re-derivation (35→33 rows, 0 flips both ways); (c) clean-room
plant builds with known syscalls only and is caught per the
certifier's bar (verdict=FAIL). The Tier-2 "verdict-neutral artifact
limitation" stands, now with a reproducible clean-room equivalent in
evidence. No Tier-2 claim breaks; none needed rescue.
