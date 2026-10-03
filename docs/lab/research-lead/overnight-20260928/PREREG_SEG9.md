# PREREG H-SEG9 FROZEN

**Date:** 2026-09-29 (PDT)
**Researcher:** H-SEG9 Frontier Researcher (subagent)
**Parent:** H-SEG8 SURVIVES (4/4), builder result `5923f16af`,
builder prereg `44cee8122`. H-SEG8 red team SURVIVES all 4 attacks
(X-SG8-1..X-SG8-4), result `40038b13f`, adversary prereg `79b324819`.
**Status:** FROZEN. This document is committed alone before any
implementation edit, build, or test run. No Python at any stage.
No em dashes in loop documentation.

## Targeted residuals

Two claims survived H-SEG8 and its red team only by inspection,
never by measurement or adversarial test:

1. **The inherited H-SEG5 sat/no==999 path.** `run_exp` prints the
   exact big-int count only when `sat[n]==1`; when `no==999` and
   `sat[n]==0` it prints the i32 `no`, justified by the H-SEG5
   proof sketch that `sat[n]==1` iff the true count `T_n >= 1000`.
   The H-SEG8 red team explicitly did not re-open this path
   ("the inherited H-SEG5 sat/no==999 path, which this red team
   did not re-open"). No experiment has ever placed `T_n` just
   below and just above 1000 to check the branch flips exactly
   where the proof says it must.

2. **The nd_final memory bound.** The red team verified by code
   inspection only that the adaptive loop exits with
   `nd_final <= 2x` the true digit count, noting "`nd` is not
   printed". The exactness certificate (`ovf==0` at exit) is
   measured; the cost of exactness (final budget, iteration
   count) is not.

H-SEG9 closes both: it makes the saturation branch observable
and adversarially sweeps it across the 1000 boundary, and it
exposes the final digit budget and iteration count as measured
diagnostics with frozen assertions.

Pre-prereg calibration (scratch `/tmp/sg9`, SEG8 mechanism
unmodified, pure Zag): on the H1 table, `"ab" x k` gives
`T = 2^(k-1)` exactly for k=2..14 (K02 NOPT 2 ... K10 NOPT 512,
K11 NOPT 1024, K12 2048, K13 4096, K14 8192; H1-T 2^29
confirmed). The 1000 boundary falls between k=10 (512, i32 path)
and k=11 (1024, big-int path: a value above 999 cannot come from
the capped i32). This family is therefore a sharp instrument for
residual 1.

## Repair (frozen, exact)

`seg9_learn.zag` = `seg8_learn.zag` at `5923f16af` copied verbatim
(cmp-verified) plus exactly these edits:

**R9a: NDINFO diagnostic (observability, no algorithm change).**
In `run_exp`:
- declare `let iters:i32=0;` beside `let nd:i32=0;`;
- increment `iters=iters+1;` once per adaptive-loop iteration
  (first statement of the `while(ovf==1)` body);
- after the NOPT `emit("\n");` and before `if(no==1){`, emit:

```
  emit(tag); emit(" NDINFO sat="); emit(i32s(get32(sat,n*4)));
  emit(" nd="); emit(i32s(nd));
  emit(" iters="); emit(i32s(iters)); emit("\n");
```

For the `sat[n]==0` path the line reads `sat=0 nd=0 iters=0`
(the accumulation never runs). Exactly one NDINFO line per
`run_exp` call. The DP, accumulation, and print logic are
untouched.

**R9b: sat-boundary sweep fixtures.** In `main()`, after the
SG9-XL block and before the SENT60 block, insert:

```
  // SG9-KSWEEP: "ab" x k for k=2..14 on the H1 table (frozen
  // K-SG9-1). T = 2^(k-1): the sat/no==999 boundary is crossed
  // between k=10 (512, i32 path) and k=11 (1024, big-int path).
  let skx:[]u8=z_alloc(29);
  let skk:i32=2;
  while(skk<=14){
    let sq:i32=0;
    while(sq<skk){ skx[sq*2]=97 as u8; skx[sq*2+1]=98 as u8; sq=sq+1; }
    let skd:i32=skk/10;
    let sko:i32=skk-skd*10;
    let skt:[]u8=z_alloc(8);
    skt[0]=83 as u8; skt[1]=71 as u8; skt[2]=57 as u8; skt[3]=45 as u8;
    skt[4]=75 as u8;
    skt[5]=(48+skd) as u8; skt[6]=(48+sko) as u8;
    run_exp(skt[0..7], cth1, unh1, nh1, skx[0..skk*2]);
    skk=skk+1;
  }
```

Tags are `SG9-K02`..`SG9-K14` (7 chars: 'S','G','9','-','K',d1,d0).
`skt` is 8 bytes; only `[0..7]` is used.

**R9c: banners, tags, header.** `H-SEG8 SEG-LEX-H` becomes
`H-SEG9 SEG-LEX-I`; `H-SEG8 COMPLETE` becomes `H-SEG9 COMPLETE`;
`SG8 ADD-UNIT` becomes `SG9 ADD-UNIT`; fixture tags `SG8-BIG`,
`SG8-HUGE`, `SG8-XL` become `SG9-BIG`, `SG9-HUGE`, `SG9-XL`;
in-code `H-SEG8:` mechanism comments become `H-SEG9:`;
`SEG-LEX-H` becomes `SEG-LEX-I`. The header comment block is
rewritten to describe SEG-LEX-I = SEG-LEX-H plus R9a/R9b, and
names this prereg. `seg8_learn.zag` untouched.

**R9d (part of R9c):** the honest-limit comment in the header is
updated: the nd_final bound is now measured (K-SG9-2), and the
H-SEG5 sat/no==999 path is now directly tested (K-SG9-1).

## Correctness argument (frozen)

- R9a is instrumentation only: `iters` is write-only counting,
  `nd` is read at print time, and the emitted line cannot alter
  DP, accumulation, or control flow. The SEG8 exactness
  certificate is unaffected.
- R9b adds fixtures only; the trained H1 table (`cth1/unh1/nh1`)
  and every pre-existing fixture are unchanged.
- K-SG9-1 tests the H-SEG5 equivalence `sat[n]==1` iff
  `T_n >= 1000` at its sharpest point. The family law
  `T("ab" x k) = 2^(k-1)` was verified in pre-prereg scratch;
  the frozen bar re-verifies it against an independent
  repeated-doubling reference (different code path: no DP, no
  chunk table, no saturation logic), so a family-law surprise
  fails loudly instead of passing silently.
- K-SG9-2 asserts the measured (nd, iters) pairs, which are
  deterministic consequences of the frozen algorithm:
  SG9-BIG (2^957, 289 digits, 33 base-1e9 digits <= 64):
  iters=1, nd=64. SG9-HUGE (2^1914, 577 digits, 65 > 64):
  iters=2, nd=128. SG9-XL (2^3999, 1204 digits, 134 > 128):
  iters=3, nd=256. SG9-K11..K14 (1024..8192, <= 2 base-1e9
  digits): iters=1, nd=64. For every fixture with iters > 1
  the general bound holds: doubling to `nd` happened only
  because the `nd/2` iteration dropped a top carry, i.e. some
  partial sum reached 1e9^(nd/2), so the true digit count
  D satisfies nd <= 2*ceil(D/9): HUGE 128 <= 2*ceil(577/9)=130;
  XL 256 <= 2*ceil(1204/9)=268. For iters=1 the budget is the
  disclosed constant initial 64, not a doubling outcome.

## Frozen kill bars

Independent reference (pure Zag, /tmp scratch, never committed):
repeated-doubling big-int (own doubling routine, no DP, no chunk
table, no saturation logic). Prints `2^(k-1)` for k=2..14, one
decimal value per line in k order.

- **K-SG9-1 (sat-boundary sweep):** For k=2..14, the SG9-K<k>
  NOPT value is byte-equal to the reference line for 2^(k-1).
  Zero FAIL lines in the full output. NDINFO reports `sat=0`
  for k=2..10 and `sat=1` for k=11..14. (A misplaced flip or a
  misprinted count KILLS: the H-SEG5 path would be broken.)
- **K-SG9-2 (measured memory bound):** NDINFO (nd, iters) equal
  the frozen pairs: SG9-BIG (64,1); SG9-HUGE (128,2);
  SG9-XL (256,3); SG9-K11..K14 (64,1) each. The inequality
  nd <= 2*ceil(D/9) holds for both doubled fixtures (HUGE, XL),
  with D read off the printed NOPT digit count.
- **K-SG9-3 (regression):** Let T be SEG8_RAW_OUTPUT.txt with
  `SG8`->`SG9`, `H-SEG8`->`H-SEG9` applied mechanically. Every
  line of T except the two banner lines appears byte-identical
  in the SEG9 output. Every SEG9 output line not in T is either
  an NDINFO line or belongs to an SG9-K02..SG9-K14 section.
  U1/U2/U3 print PASS; zero FAIL lines.
- **K-SG9-4 (determinism):** 3 consecutive full runs
  byte-identical (cmp), md5 recorded, exit 0, zero stderr.

**Verdict rule:** H-SEG9 SURVIVES iff all four bars PASS.
Classification: bounded L2 structural-learning repair
(observability plus inherited-path closure). Not L3: no
representational invention; the counting remains mechanical.

## Honest limits (frozen)

1. Count capacity was already unconditional at H-SEG8; H-SEG9
   does not extend it further. It measures what the adaptive
   loop costs (nd_final, iters) and closes the last unexamined
   inherited path (H-SEG5 sat/no==999).
2. The exact-999 case (`no==999, sat[n]==0`) is approached from
   both sides (512 and 1024) rather than constructed exactly;
   constructing a corpus with `T_n` exactly 999 remains open.
3. The per-position move-list cap (8, in `mv_add`) and the
   5-candidate enumeration cap (in `enum_bwd`) are unchanged and
   not targeted; they bound VERDICT/CAND output, never NOPT.
4. Counts above 2^19999 remain untested (machine memory bound,
   inherited from the H-SEG8 red team).
5. All other H-SEG8 honest limits unchanged.

## Governance (frozen)

- Prereg committed alone before any implementation edit, build,
  or run; strict ancestry (`git merge-base --is-ancestor`) checked
  at result time.
- Pure Zag: implementation, fixtures, builds, runs, greps, md5,
  cmp, diff, reference. No Python anywhere.
- Only H-SEG9-owned files staged, via pathspec-restricted adds.
  No binaries committed (builds in /tmp/sg9 only).
- `seg8_learn.zag` and all prior evidence untouched.
- No em dashes in loop documentation (byte-checked).
