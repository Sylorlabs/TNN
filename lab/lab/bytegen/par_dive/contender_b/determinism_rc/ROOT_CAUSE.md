# PAR_DIVE Contender-B Determinism Root-Cause Investigation

**Date:** 2026-09-24
**Investigator:** Muse (subagent)
**Frozen prereg:** `~/workspace/bytegen/par_dive/PREREG_PAR_DIVE.md`
**Pinned compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Verdict

**Root cause: (a) B-side provenance — a stale binary from an older source revision, compared against a newer binary. NOT a znc codegen defect. NOT runtime nondeterminism.**

The redteam's "1/11 silent divergence" (147,014 differing samples, first at 2.200 s) was **not** nondeterministic execution. The 07:48 run used a binary built from an older source revision (S1: gap-filling sustain variant, no per-note release for chain-interior notes). All runs from 07:57 onward used a binary built from the reverted source (S2). The binary was swapped between 07:48 and 07:57 without the redteam noticing.

**Proof:** I reconstructed S1 by patching the current source, built it with the pinned compiler, and reproduced the "divergent" file **byte-identically** (1,323,000/1,323,000 samples, SHA-256 `dc124a6e…b51f`).

**B's determinism bar SURVIVES.** The current source + pinned binary produced **124/124 byte-identical runs** (24 sequential + 100 battery). The overthrow verdict on determinism grounds is retracted as a mixed-binary comparison artifact. (Other red-team findings are unaffected.)

**No new znc defect.** No `AGENTS.md` entry required.

---

## 1. Timeline of Evidence

| Time (2026-09-24) | Event | Output hash |
|---|---|---|
| 07:48 | Redteam run 1 (`cas_b_clean.s32`) | `dc124a6e…b51f` (DIVERGENT) |
| 07:57 | B crew `b_clean1.mix` | `d1a6c83b…ac0a6c` (majority) |
| 07:58 | B crew `b_clean2.mix` | `d1a6c83b…ac0a6c` |
| 08:09–08:25 | Redteam runs 2–11 | `d1a6c83b…ac0a6c` (all 10) |
| 08:13 | Current source mtime (`render_b.zag`) | — |
| 08:40 | Shipped binary deleted (redteam RUNLOG) | — |
| 08:47 | Binary rebuilt from current source | `d1a6c83b…ac0a6c` |
| 09:23+ | 24 sequential runs (this investigation) | `d1a6c83b…ac0a6c` (24/24) |
| 09:33+ | 100-run battery (this investigation) | `d1a6c83b…ac0a6c` (100/100) |

**Key inference:** The binary changed between 07:48 and 07:57. The 07:48 output (D) predates the current source (08:13) and the 08:47 rebuild. The B crew's own 07:57–07:58 renders are already the majority hash (Z).

## 2. Divergence Characterization (D vs Z)

- Exactly **147,014** samples differ out of 1,323,000.
- First difference at sample **97,020 = 2.200 s**; last at 1,183,632.
- Differences confined to regions 0, 1, 8 (region = 3 s). Regions 2–7, 9 identical.
- 2.200 s = **exactly** the first motif note's release onset (note starts 2.0 s, dur 0.35 s, rel 0.15 s → release at 2.0 + 0.35 − 0.15 = 2.200 s). 24.200 s is the same for the recurrence.
- Before 2.200 s: outputs are **exactly identical**.
- D does **not** attenuate at per-note releases; sustains a loud voice through 50 ms inter-note gaps.
  - Around first motif: pre-release RMS 16,839 (both); release-window RMS 17,740 (D) vs 12,343 (Z); gap RMS 16,514 (D) vs 7,372 (Z).
- D's gap voice has the preceding note's pitch and stays near full amplitude.

## 3. S1 Reconstruction (Constructive Proof)

The B `DESIGN.md` documents that a "gap-filling sustain variant was built and measured" but reverted (G-PER 0.34 → 0.50). D has exactly that variant's signature.

I patched `render_b.zag` → `recon4.zag` with four changes (the S1 hypothesis):

1. **`span_render`: release disabled for chain-interior notes.** The release branch now applies only when `evg(ev, e, 13) == 1` (chain_end / tail). Interior notes use attack + sustain only.
2. **`span_render`: attack only for non-legato notes.** `if (e_leg == 0 && tr < atk …)`. Legato notes (after a sustained gap) continue at full amplitude (no attack dip).
3. **`gap_render`: voice sustain implemented.** When `sustain != 0` and `t >= R0`, write `voice_sample(…, env)` with carried phase/vibrato, then advance (same convention as current).
4. **Sustain envelope:** raised-cosine fade `env = 32768 + lsin(lut, 256 + x/2)`, `x = (g*1024)/6615`, where `g` = gap offset. (Decays to ~75% over a 2,205-sample gap.)

**Result:** `recon4_bin` output is **byte-identical** to the divergent file:
```
dc124a6edb7921326ca32043692f784f549c3f18f868febad59bfd895840b51f  recon4.mix
dc124a6edb7921326ca32043692f784f549c3f18f868febad59bfd895840b51f  cas_b_clean.s32
```
1,323,000/1,323,000 samples match (verified with `cmp`).

**Why this rules out runtime nondeterminism:** D is not a "glitch." It is a coherent, musically-sensible designed variant (interior sustain + gap fill + tail releases + legato attack-skip). A runtime nondeterminism (uninitialized read, race, allocator fluke) would not produce a structured alternative that exactly matches a documented abandoned design. Combined with 124/124 deterministic runs of the current binary, the stale-binary explanation is conclusive.

## 4. S1 vs S2 Source Differences

| Feature | S1 (07:48 binary, DIVERGENT) | S2 (current source, MAJORITY) |
|---|---|---|
| Release, chain-interior notes | none (sustain) | inverted (collapse + swell) |
| Release, chain-tail notes | inverted | inverted |
| Attack, legato notes | none (full amplitude) | yes (fade-in) |
| Attack, chain heads | yes | yes |
| Gap sustain | yes (fading voice) | no (silence) |

S1 = the documented gap-filling sustain variant. S2 = the reverted source.

## 5. Determinism Verification (Current Source + Pinned Binary)

- **Rebuild provenance:** Rebuilt current source with pinned compiler → byte-identical to shipped binary (`432a55e1…fd20`). Source matches `~/workspace/tnn-lab/bytegen/par_dive/contender_b/src/render_b.zag`.
- **24 sequential runs:** All produced `d1a6c83b…ac0a6c`. 24/24 byte-identical.
- **100-run battery:** 100/100 byte-identical, 0 divergent.
- **Total: 124/124.**

## 6. Source Audit (Current `render_b.zag`)

- **Zero** `as []i32` / `as []u32` / `as []u16` / `as []i64` / `as []u64` casts. (The ZNC-2026-09-21-007 aliasing defect is structurally irrelevant to B.)
- **Zero** `.*` dereferences.
- All dynamic arrays are `[]u8` arenas via `nio_alloc`, which explicitly zeroes every byte.
- Allocation sizes: event arena 8,192 B; LUT 8,192 B; region lists 512 B each; state 144 B; dstat 16 B; mix `nsamp*8+7`; fixture 10,584,007 B; WAV `44+nsamp*2+7`. All below the 32 MiB slice limit.
- Syscalls: read/write/open/close only. No RNG, no clock.
- Compiler analyzer emits two "dead loop" warnings (`w_all`, `file_read`) — both loops increment `at`; false positives, not implicated.

## 7. Toolchain Cast Probe (ZNC-2026-09-21-007, Actual Build)

Probed the pinned compiler with three consecutive 512-byte `as []i32` casts:
- Writing `a[65..67]` changed `b[0..2]` (expected 2000–2002, got 777001–777003).
- Writing `b[65..67]` changed `c[0..2]` (expected 3000–3002, got 888001–888003).
- **Confirmed:** 2nd/3rd arrays' slots 0–2 alias the previous array's slots 65–67 on this build (matches AGENTS.md ADDENDUM 2026-09-24, CERT RV3).
- **B relevance:** None. B contains zero `as []i32` casts. No action needed.

## 8. Incidental Finding: Inverted Release Envelope (S2, Current Source)

The current source's release is **inverted** (likely a bug, but deterministic and out of scope for this RC):
```zag
let x:i64 = (rem * 1024) / rel;
env = 32768 + lsin(lut, 256 + x / 2);
```
- At release onset (`rem = rel`): `x = 1024`, `env = 32768 + lsin(768) = 1` (≈ silent).
- At note end (`rem = 0`): `x = 0`, `env = 32768 + lsin(256) = 65535` (full).
- The note goes **silent at release start, swells to full at note end, then hard-cuts**. A correct release would fade full → silent.
- This affects every note's last 150 ms in the current binary. It is **deterministic** (all runs share it) so it does not affect the determinism verdict, but it is an audio-quality defect the B crew should address separately.
- **Not fixed** in this investigation (out of scope; the divergence RC required no source change).

## 9. Conclusion

| Question | Answer |
|---|---|
| Root cause (a/b/c) | **(a) B-side provenance**: stale S1 binary vs S2 binary, not nondeterminism. (Environmental component: binary swapped mid-campaign.) |
| New znc defect? | **No.** |
| AGENTS.md entry? | **Not required** (no new defect). |
| Source fix needed? | **No** (for the divergence). Current source is deterministic. |
| B's determinism bar | **SURVIVES.** 124/124 byte-identical runs. |
| Overthrow verdict (determinism) | **Retracted** as a mixed-binary comparison artifact. Other red-team findings unaffected. |
| Reproducer | `recon4.zag` (+ this report). Reproduces D byte-exactly from S1 patches. |

## Artifacts

- **Report:** this file.
- **Reproducer source:** `recon4.zag` (S1 reconstruction; see §3 for the four patches).
- **Reproducer build:** `znc_linux_x86_64_abed8aa1 recon4.zag -o recon4_bin && ./recon4_bin plan_v1.txt out.s32 seqmix` → SHA-256 `dc124a6e…b51f`.
- **Hashes:**
  - Divergent (S1): `dc124a6edb7921326ca32043692f784f549c3f18f868febad59bfd895840b51f`
  - Majority (S2): `d1a6c83b0e549507cca92dceb814c1c3698ce92df14f4f65a59015c604ac0a6c`
  - Current binary: `432a55e1169d3dfe83624e68605ee5ed8b756461800719700475fc2d9b59fd20`

## Open Questions / Follow-ups

1. The exact S1→S2 edit (and the binary swap at ~07:48–07:57) should be confirmed from the B crew's shell history / build logs, if available. The reconstruction proves the *what*; the *who/when* of the swap relies on file timestamps.
2. The inverted release envelope (§8) should be fixed by the B crew separately (it is not a determinism issue).
3. The redteam's process should pin the binary hash at campaign start and verify it before each run (provenance hygiene).
