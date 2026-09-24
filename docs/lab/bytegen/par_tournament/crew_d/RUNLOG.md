# CREW D — tournament RUNLOG (coordinator round)

Date: 2026-09-24. Pinned toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Pure Zag. Zero RNG in every binary. Byte-identical reruns proven by `cmp`/SHA.

Prior: `../par_dive/contender_d/` (PREREG_D.md, RESULTS.md, REDTEAM.md,
VERDICT.md — read before this round). This round re-verifies D1 and D2
through the FULL frozen battery (§2 of `../PREREG_PAR_DIVE.md`, the law),
closes D2's native-measurement gap (native reference binary rebuilt from
frozen source, NATIVE's RT-LONG re-measured directly), runs the §5 red
team, and adds a NEW D scheme D3 (preregistered below BEFORE any build).

Work dir: `~/workspace/tnn-lab/bytegen/par_tournament/crew_d/`
(`src/`, `tests/`, `plans/`, `results/`, `runs/`, `excerpts/`).
D1/D2 sources copied from the dive, SHA-verified against
`par_dive/contender_d/RESULTS.md` frozen SHAs:
- render_d1.zag `d6bcb99c0d1c1b211fcd6ba495656435856e22db3f72b1a80ed35dbe7f3cff88` ✓
- render_d2.zag `5199cd1d071d784538df011d9f2392e8fa852c5ea50229cbe2787efe8f3bebdd` ✓
Fixtures/plans identical between `~/workspace/bytegen/` and
`~/workspace/tnn-lab/bytegen/` (cmp-verified 2026-09-24); instruments
(`tests/gate_bin`, `aud_v10/chop.py`) are the dive's frozen ones at
`~/workspace/bytegen/tests/gate_bin` and `~/workspace/aud_v10/chop.py`.

## D3 preregistration (written 2026-09-24 BEFORE any D3 code exists)

**D3 "PLANHEAL" — PAR render + plan-pure audit + plan-pure restoration.**
Two phases, all pure f(plan, window): (1) forward PAR render verbatim
(voice_q16/bed_q16 from fork_par; RESPOND rendered at the plan nominal,
PAR semantics like D1); (2) audit pass: re-render the mix in fixed
1024-sample blocks plan-pure into scratch and byte-compare each block
against the phase-1 mix — any differing block is overwritten with the
plan-pure scratch bytes (restoration writes only plan-pure bytes; the
audit never changes generation decisions, so there is no
output→content feedback). Deterministic, zero RNG.
**Claim:** D3-C1 clean fixture → mix bit-identical to PAR (audit no-ops;
9/9 bars, CHOP, coherence all tie). D3-C2 frozen RT-CASCADE
(64-sample XOR @ t=3 s): audit detects and restores the corrupted
blocks → **0 differing samples vs clean in-window AND post-cut**
(PAR/D1/D2: 64 in-window diffs persist, 0 post-cut). D3-C3 §2-mandated
EXTENDED fault models — burst (4096 samples @ 10 s), dropout (zeroed
1024-block @ 20 s), DC shift (+10000 over 8192 samples @ 5 s) →
all fully repaired, 0 diffs vs clean under every model; confinement-only
schemes keep in-window damage under all extended models. D3-C4 DET:
byte-identical reruns; seq==rev bit-identical. D3-C5 (honest cost):
audit = a second full render → ~2× PAR wall-clock, documented as the
trade. **§6 framing:** D3 ties the frozen RT-CASCADE metric (post-cut
diffs: 0=0) and the frozen metric is where ties live; the strictly-better
result is total-damage-elimination under the §2 EXTENDED models —
reported as a partial win with the 2× cost documented, NOT a §6
overthrow (cost is a frozen axis and 2× is a regression there).
**Failure modes (preregistered):** F1 audit is blind to faults whose
bytes coincidentally equal the plan-pure bytes (undetectable by
construction). F2 a lying plan renders its lie and the audit passes —
PLANHEAL trusts the plan exactly like PAR (D2's plan-provenance
boundary applies unchanged). F3 the audit pass doubles wall-clock cost.
**Red team (§5):** sustained 1292-block corruption between phase 1 and
the audit (full recovery expected); faults straddling audit-block
boundaries; fault injection between the two passes to prove the audit
has no output→content feedback (it reads the mix only to compare).

## Build

2026-09-24, pinned znc `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`:
- `src/render_d1` ← `src/render_d1.zag` (SHA d6bcb99c…cff88, matches dive pin)
- `src/render_d2` ← `src/render_d2.zag` (SHA 5199cd1d…bebbdd, matches dive pin)
- `src/render_d3` ← `src/render_d3.zag` (NEW, preregistered above before implementation)
- `src/render_native` ← `src/render_native.zag` (= frozen `render_par.zag`,
  diff-identical across both workspace trees)
Rebuilt `render_native` is byte-identical to both pre-existing builds
(`fork_par/render_par`, `fork_par/render_par_fresh`) — binary provenance
uncertainty closed. Binaries are uncommitted artifacts (excluded from git).

## Battery results

Full log: `runs/battery.log` (rc=0). Runner: `tests/run_battery.sh`.

**D1** (all re-verified): DET 4/4 SHA `1823f8fa82af3aca23c598b902c53a0df072315c84e7c5509b26625299427ca4`
(same SHA as the dive's runs — cross-session reproducibility); D1-C1 mix+wav
bit-identical to NATIVE; 9/9 quality bars (numbers identical to the dive);
CHOP 0/0/29-with-0-unexplained; coherence 1.000000 ×4; RT-LONG renders
nominal 880 (ZCR 842.5, −75c disclosed bias); RT-CASCADE 0/64/0;
RT-EDGE bit-identical to NATIVE; seq==rev bit-identical; sustained
82,688 diffs, 100% confined. 15 s extension: hardstop=1 fires;
analyzer A/B (`results/d1_edgeAB.txt`): fade ends 0.0000 FS, nofade ends
0.3142 FS; 214 diffs all inside [n−220,n), 0 outside; frozen CHOP-1 0/0.
§5: `results/d1_redteam_pass3.txt` — T1 hardstop=1 under 41,344 faults;
T2 41,344/0 diff-set (gains index-pure); T3 0/20 LUT mismatches.

**D2** (all re-verified): DET 4/4 same SHA; D2-C1 bit-identical to NATIVE;
quality/CHOP/coherence tie NATIVE. RT-LONG original: LATCHED f0q=28835840
→ 0¢ (ZCR vs 440: 425.0 Hz, −60c disclosed). RT-LONG near-miss: LATCHED
440 → 0¢. Multi-trap: e=4 ABSTAIN code=1, e=5 latch 440, e=6 latch
523.25 (f0q=34291712). RT-CASCADE 0/64/0; sustained → ABSTAIN code=3;
RT-EDGE bit-identical; seq==rev bit-identical. §5: 5 adversarial plans
reproduce (`results/d2_adversarial.txt`); f0lie demo latches 466.16
(f0q=30550261) — plan-provenance boundary mapped (`REDTEAM.md`).

**D3** (new): DET 4/4; D3-C1 mix+wav bit-identical to NATIVE (audit
repaired 0 clean); 9/9/CHOP/coherence tie NATIVE. RT-CASCADE frozen:
0/0/0 (repaired 1,024). Extended: burst 0/0/0 (5,120), dropout 0/0/0
(2,048), DC-shift 0/0/0 (9,216), sustained 0/0/0 (1,323,000). RT-LONG PAR
semantics (renders nominal); RT-EDGE bit-identical; seq==rev bit-identical.

**NATIVE** (gap closed): original renders nominal 880 → 1200.00¢ honest
error (ZCR 842.5, −75c bias); near-miss renders nominal 460 → 76.96¢
(ZCR 441.2, −72c bias). `results/native_rtlong.txt`,
`results/native_rtlong_near.txt`.

**COST** (interleaved, same machine): native 4.35/6.91/6.06 (med 6.06),
d1 3.61/5.86/5.96 (med 5.86), d2 5.98/5.77/8.07 (med 5.98),
d3 7.52/13.45/15.31 (med 13.45 = 2.22× native). Peak RSS ~13 MB all four.
`results/cost_interleaved.txt`.

**Excerpts** (WITHHELD-NOT-FOR-REVIEW, `excerpts/README.md`): re-rendered
with tournament binaries; SHAs in `results/excerpts.sha256`.

**Verdicts** (`VERDICT.md`, frozen §6): D1 TIE (incumbent keeps);
D2 OVERTHROW on audio (caveat closed by direct native measurement);
D3 partial win on extended RT-CASCADE (damage elimination) with 2.22×
cost — NOT a §6 overthrow (cost is a frozen axis). Video/dialogue/image
paths: NOT TESTED.

## Provenance of reference numbers

- PAR baseline, hybrid v2 76.7c near-miss: dive VERDICT.md/RESULTS.md.
- NATIVE audio reference: `fork_par/src/render_par.zag` (identical in
  `~/workspace/bytegen/` and `~/workspace/tnn-lab/bytegen/`, diff-verified
  2026-09-24); rebuilt here as `src/render_native` with the pinned znc —
  NATIVE's RT-LONG measured directly on this binary, closing the dive's
  disclosed caveat.
