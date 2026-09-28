# P4 Implementation — C1′: license gate with PLANE fallback

Frozen prereg: `~/workspace/upscale_r4/PREREG_R4.md` (arm P4 spec). Round-3
context: `r3src/PREREG_R3.md`, `r3src/VERDICT_R3.md`. Implemented 2026-09-27.
Pure Zag, zero RNG, pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

Deliverable: `azgen_p4.zag`
(SHA-256 `8ed57695c1a5316b3867146bde230aae32a4ba2dbe7f3bc6cfaf7bfae14e3be5`,
1580 lines, generated from the verified `azgen_c1.zag`
`a23e717931bec8a7a1a6e6f1068a46b5b4a939d87cc86fac21a854d2dddb0753`
by exact-match script; every replacement anchor asserted to match the
expected count).

## Exact change vs azgen_c1.zag

1. **License gate: untouched.** The predicate `4*keySSD(winner) <= e AND
   keySSD(runner-up) >= 2*keySSD(winner)` → ATOM-STAMP is text-identical.
   Matching, the ≥9/value gain bar, split-vs-take comparisons, commit
   logic, `gshapes_commit`, `g_render_shapes`, `g_render_lines`, and the
   LINES path are text-identical (full-file diff reviewed; all edits are
   additive except the new unlicensed-take branch).
2. **Fallback changed (the only behavioral change):** an unlicensed take
   (`gain_take >= 9·nval` but license fails) is recorded as a PLANE-FIT
   take instead of falling through to C1's REJECT/NO-FIT path. The plane
   is the least-squares fit to the block's observed pixels
   (`g_csq`/`g_pterm`/`g_plane_fit` ported **verbatim** from the committed
   `azgen_c3.zag` `cd5bab26306ae4683eb4882faa864292dbf8130307cff92912d0027d2ca8418f`
   — byte-identical function texts, verified by extraction diff).
   `gplane_commit` (subtract plane at input res, claim pixels) and
   `g_render_planes` (plane evaluated at 2×) are structural ports of C3's
   PLANE commit/render branches. Plane takes live in a separate
   stride-14 `ptakes` array; the atom `takes` array layout is untouched.
3. **Gain accounting is C1-exact:** the unlicensed take credits 0 gain
   (as C1's reject did), so recursion outcomes, split decisions, G/N,
   and the commit decision are behaviorally identical to C1's — only the
   fallback render of unlicensed regions changes. (An earlier draft
   credited `gain_take`; a bridge smoke run showed it changed split
   outcomes — `takes=2` vs C1's `takes=0` — violating the "recursion
   unchanged" clause. Reverted to credit-0 before any scoring.)
4. **Trace:** per-region lines with honest reason strings —
   `R x=.. y=.. bw=.. bh=.. si=.. op=ATOM reason=p4_licensed_atom` and
   `... op=PLANE reason=p4_unlicensed_plane` — plus a `plane_takes=`
   aggregate. Invariant: `plane_takes == unlicensed` (every unlicensed
   take becomes exactly one plane take). Plane pixels are labeled **7**
   (`CONSTRUCTED-PLANE`, cyan in the labelmap) so licensed ATOM regions
   stay label 3 exactly as C1; `GEN_SCORES.txt` census/SSE extended with
   label 7 (arrays resized 56→64 bytes — required, else index 7 is OOB).

## Licensed-path verification (task step 5)

- Unmodified `azgen_c1.zag` was built with the same support files; on
  bridge it reproduces the committed C1 number exactly (**20.00 dB**),
  validating the build.
- Source-level: the licensed-path code is text-identical (diff-proven).
- Runtime, bridge: C1 `takes=0 licensed=0 unlicensed=6` →
  P4 `takes=0 licensed=0 unlicensed=6 plane_takes=6`; P4's `upscale_gen.bmp`
  and `labels_raw.bin` are **byte-identical** to C1's
  (SHA `db006a4e51d13dd0a96724432921c6eb4fbf1a68c20617af441f5e7f20172503`).
  Sky: same — byte-identical outputs
  (SHA `dac4e2aafbbfa53e2c22465727c4ff7efa35ce97cf9fc2f43f97ffcd9d18ee64`),
  `licensed=0 unlicensed=4 plane_takes=4`.
- Honest caveat: on the available dev images (bridge/sky) C1's gate
  licensed **zero** takes (consistent with VERDICT_R3: "the gate refused
  every take" on bridge/sky), so there is no nonzero licensed region to
  pixel-compare. Verification rests on (a) text-identity of all
  licensed-path code, (b) identical lic/unl decision counts, (c)
  identical atom-take sets, (d) byte-identical full outputs.

## Port verification (fallback wiring)

The plane path never renders on bridge/sky (shapes reverted, G=0), so the
wiring was verified by a standalone probe: the six plane functions were
extracted **verbatim** from `azgen_p4.zag` into `probe.zag`, run on a
synthetic 8×8 block, and compared against an independent Python oracle
(trunc-toward-zero division, round-half-away `g_rdiv`): fit coefficients
`na=2025,681,-9 nb=-1353,-9,-663`, commit residual sum 93 with 64/64
claimed, render accsum 89473 with 254/256 label-7 (lab-guard respected on
the 2 pre-marked pixels), spot pixels — **all identical**. `g_csq`,
`g_pterm`, `g_plane_fit` are byte-identical to `azgen_c3.zag`.

## Determinism

P4 on bridge, three runs (two fresh outdirs + one `env -i`):
`upscale_gen.bmp` SHA-256 `db006a4e…2503` **3/3 identical**.

## Sanity PSNRs (per-channel-mean dB, `src/metrics.py`; raw, no tuning)

| image | C1 (fresh binary) | P4 | bicubic column |
|---|---|---|---|
| bridge | 20.00 | 20.00 | 25.89 |
| sky | 26.27 | 26.27 | 33.20 |

R3 reference: baseline bridge 18.47 / sky 22.75; committed C1 bridge 20.00 /
sky 26.27 — the fresh C1 binary reproduces 20.00/26.27 exactly.
P4 ≡ C1 on both images because the gate licensed zero takes and SHAPES
reverted (G=0 < 9N), so the six (bridge) / four (sky) plane takes were
recorded in the trace but correctly discarded — the fallback engages only
on images where takes clear the gain bar (the sealed battery will decide).

## Notes for the coordinator

- No full battery run (per task). Sealed set untouched (never listed).
- Build scratch (binaries, outdirs) was in `/tmp/p4build` and deleted
  after scoring; `impl_p4/` holds only the source + this file.
  Disk was at 100% throughout; every write verified, outdirs removed
  between legs.
- The `nofits` count legitimately differs from C1's (bridge 24→18,
  sky 96→92): unlicensed regions are plane takes now, not nofits.

P4 COMPLETE
