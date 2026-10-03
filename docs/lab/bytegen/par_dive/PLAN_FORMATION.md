# PLAN FORMATION PARALLELISM — §4 verdict (PAR_DIVE prereg)

**Question (Micah's framing):** "left to right but it first plans parallelly" —
is PLAN FORMATION itself parallel? Instrumented where plans come from in each
of the four modalities, built a pure-Zag prototype that forms the same plan
two ways (sequential elaboration vs order-free/independent computation),
diffed the plans byte-for-byte, and quantified the end-to-end win.

**Headline:** plan formation is order-free (parallelizable) in **all four
modalities**. The only sequential elements anywhere are (a) argmax reductions
with first-wins tiebreak — reproducible order-free via an index tiebreak — and
(b) dialogue's depth-2 entity-resolution chains + first-match template
priority. No modality's formation carries output-dependent sequential state.
But formation is *cheap* relative to render in audio/video/dialogue, so the
end-to-end win from parallel formation is large in exactly one modality:
**image** (formation 19× render). Contender A should shard candidate scoring.

All timings are CPU user+sys seconds, min-of-N, pinned
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, zero RNG.
The VM has 2 CPUs and ran at load ~20 during measurement, so wall batches are
reported but projections assume an unloaded machine (CPU time is
load-independent; shard work provably splits evenly — measured below).

## 1. Audio — PARALLEL (search: map+reduce; v2: constructive)

**Where the plan comes from.** `f3_synth` (field.zag:932) consumes an arena
plan. The plan is formed two ways in the lab's history:

- **v1 `ig_gen_a1`** (imagine.zag:961–1012): enumerates 8⁴ pitch × 2⁴ duration
  = 65,536 candidates; each candidate is installed (`ig_a1_install`, which does
  `ig_clear` then places 4 events — each event's params a pure function of its
  pitch/duration digits) and scored by `ig_taste_audio` (imagine.zag:585), a
  **pure function of the arena** (contour + consonance + regularity terms, no
  cross-candidate state). Selection is a global argmax with strict `>`
  (first-best-wins). The nested loops are just an enumeration order; every
  candidate's score is independent. **Embarrassingly parallel map + deterministic
  reduce.** `ig_gen_a2` (1039–1080) is the same shape (8³×2³).
- **v2 `j2_gen_a1`** (imagine.zag:2682–2700): six direct `j2_place` calls with
  literal args — each event a pure function of (brief, mode); placement order
  only fixes slot order. **Order-free by construction.**

**Measurement (real code):** built a throwaway driver against the import-safe
`scenes_inc.zag` closure and timed the real `ig_gen_a1`: **0.008 s CPU** for
both modes (65,536 candidates; the anchor+monotonicity filters prune hard and
`taste` on 4 events is trivial). Audio render (`imagine_bin_v2 wav m`, 4
briefs incl. v2 formation): **0.030 s CPU** total (~7.5 ms/brief). Formation ≪
render.

**Verdict: PARALLEL.** No sequential state in formation.

## 2. Dialogue — MIXED (parallel slot fills; sequential branch priority + depth-2 resolution chains)

**Where the plan comes from.** `do_compose` (dialogue.zag:1302–1457) fills
response-template slots from fact memory. Per branch:

- `"was the author of"` (1303): `author_of(work)` → `year_of(author," born ")`
  and `year_of(entity," built ")` → compare. The two `year_of` lookups are
  **independent pure scans** over `fm` (lowest-fid-wins; dialogue.zag:1249);
  only the entity identities (`au`, `ent`) must resolve first — a **depth-2
  data-dependency chain**, not output feedback.
- `"which is taller"` (1323): `h1`/`h2` independent `year_of` lookups, then a
  comparison reduction.
- `"did X write"` (1358): entity resolution then one `wrote_rel` lookup.
- `"birth year"` (1395): person resolution → `born_fact_of` (1270).

**Sequential elements (real, but small):** template branch selection is a
first-match `if` chain (1303/1323/1358/1395 + fallthrough `return 0`) — branch
*priority* is semantic and order matters. (The predicates themselves are pure,
so branch *matching* parallelizes; the reduce must preserve first-match
priority, exactly like the argmax index-tiebreak.) Final assembly (`rclr` +
`rput`s + comparison) is a pure reduction.

**Measurement:** structural — KB is 38 facts (`kb.txt`); each lookup is a few
linear scans of ~40-byte fact rows. Formation is sub-millisecond; there is no
heavy render (the "render" is `rput` into the response buffer). Formation ≈ the
whole pipeline, and it is tiny.

**Verdict: MIXED, parallel-dominant.** Independent fan-out of fact lookups
within a branch; depth-2 resolution chains and first-match branch priority are
the only sequentiality.

## 3. Image — PARALLEL (search: map+reduce), and formation DOMINATES end-to-end

**Where the plan comes from.** The "plan" is the theme: `theme_v1`
(screens.zag:418) installs the winner of `v1_winner()` (407–417), an argmax
with strict `>` (first-best-wins) over **224 candidates**, each scored by
`score_candidate(idx)` (322–405) — a **pure function of idx** that builds three
full screen spec-lists and scores contrast/economy/regularity/alignment/symmetry.
`theme_candidate(th, idx)` (99–114) derives every theme word from idx digits
(rad/sp/pal/sh/bo) — pure. Theme → pixels (`scr_library` etc.) is the render.

**Measurement (real binaries):** `render_bin score` (224 candidates):
**0.290 s CPU**. `render_bin render v2 lib` (one 360×640 screen):
**0.015 s CPU**. **Formation is 19× render** — the only modality where plan
formation dominates end-to-end.

**Verdict: PARALLEL**, and the highest-value parallelization target in §4.

## 4. Video — PARALLEL (per-frame plans independent)

**Where the plan comes from.** `o_emit_frame(f, …)` (ocean.zag:650–869): the
frame's plan is `o_scene(f)` (234–239) — `{vwx, vwz, rot}` as pure functions
of the frame index (value-noise of `f`). Every pixel's color is
f(plan=`{f,vwx,vwz,rot}`, x, y) via `o_height`/`o_sky`/`o_shade_*`/`o_spire`.
Frame f's plan never touches frame f−1. **Frames are independent — formation
parallelizes across frames trivially.** (Intra-frame render has bounded
neighbor dependencies — 1-column height stencil via `hsp`, and the y-buffer
occlusion accumulation — but that is *render*, not plan formation, and §4
scopes to formation.)

**Measurement:** built `ocean.zag` → one 1024×1024 frame: **1.96 s CPU**
(min-of-3). `o_scene` is microseconds. Formation/render ≈ 0.

**Verdict: PARALLEL** (across frames).

## 5. Prototype: byte-diff proof (pure Zag, pinned znc, zero RNG)

`proto/planform.zag` models both formation shapes found above:

- **SEARCH** (audio-v1 `ig_gen_a1` / image `v1_winner`): N=65,536 candidates,
  digits packed from idx (like `theme_candidate`), anchor+monotonicity filters,
  pure scorer (consonance ratio tests + duration regularity + image-like
  12-cell spec term — mirroring `ig_taste_audio` and `score_candidate`),
  strict-`>` argmax.
- **CONSTRUCT** (audio-v2 `j2_place` / dialogue slot fill / video `o_scene`):
  32 plan events, each a **pure function of (winner_idx, slot)** — including
  motif recurrence (slots 16–23 restate 0–7, like `plan_v1.txt` MOTIF-A).

Paths: `seq` (in-order scan, events emitted slot 0→31) vs `shard s S`
(strided scan, local best with (score desc, idx asc) tiebreak) + `assemble`
(**order-free reduce** of shard bests, events emitted in **reverse** slot
order 31→0). `render` is a deterministic synth from the plan file
(formation/render split + DET).

`proto/run.sh` results (this run):

| check | result |
|---|---|
| `cmp plan_seq.bin plan_par.bin` | **byte-identical** |
| `cmp plan_par.bin plan_par_scr.bin` (shard bests fed in scrambled order) | **byte-identical** |
| winner seq vs par | agree (3800, score 1026) |
| seq rerun `cmp` | byte-identical |
| par pipeline rerun `cmp` | byte-identical |
| render(seq-plan) vs render(par-plan) `cmp` | byte-identical |
| render rerun `cmp` | byte-identical |

Shard work splits evenly (load-independent CPU): shard0=0.005 s,
shard1=0.004 s vs seq=0.010 s (each ≈ T_SEQ/2) — **linear shard scaling of
formation work confirmed**; assemble (reduce+emit) = 0.001 s.

Prototype timings (CPU s, min-of-N): formation seq **0.010**, render **0.138**.

## 6. Quantified parallelism opportunity

Per-modality end-to-end (formation + render), measured CPU seconds:

| modality | formation (CPU) | render (CPU) | formation shape | E2E win from parallel formation |
|---|---|---|---|---|
| audio v1 search | 0.008 | ~0.0075/brief | map+reduce, parallel | ~1.0× (negligible) |
| audio v2 construct | ~0 | ~0.0075/brief | order-free | ~1.0× |
| **image theme search** | **0.290** | **0.015** | map+reduce, parallel | **S=2: 1.9×, S=8: 5.5×** (0.305→0.055) |
| dialogue compose | ~0.0001 | ~0.0001 | mixed (depth-2 chains) | ~1.0× |
| video frame plan | ~0 | 1.96/frame | per-frame parallel | ~1.0× (frames parallelize instead) |

Prototype projections (unloaded machine, T_form/S + T_assemble + T_render):
S=2 → formation 1.67×, E2E 1.03×; S=8 → formation 4.44×, E2E 1.06×;
S=64 → formation 8.65×, E2E 1.06× (prototype's render dominates, like audio).

**Exactly what contender A should exploit:**

1. **Shard the candidate-scoring map phase.** In every search-based formation
   (audio-v1, image), >99% of formation work is independent per-candidate
   scoring. Shard the index space (strided or contiguous), score in parallel,
   reduce with the **(score desc, index asc) tiebreak** — this reproduces the
   sequential first-best-wins argmax bit-for-bit (proven by the prototype's
   byte-diff, including scrambled shard order). The reduce+emit is ~1 ms.
2. **Emit constructive plans in any order.** Where events are pure functions
   of (seed, slot) — audio-v2 placements, dialogue slot fills, video
   per-frame params, motif recurrences — compute each event independently and
   assemble by slot index. The prototype's reverse-order emission producing a
   byte-identical plan is the proof.
3. **Spend the win where formation dominates: image.** Theme search is 19× its
   render; parallel formation alone buys ~5.5× end-to-end at S=8 there. For
   audio/video/dialogue, formation parallelism is correct but buys ~nothing
   end-to-end — A's win on those paths must come from **render** parallelism
   (already established by fork_par), not formation.
4. **Memoize repeated subplans.** Motif recurrence (plan_v1.txt MOTIF-A at
   2.0 s and 24.0 s; prototype slots 16–23 = f(slots 0–7)) is a pure function
   of (winner, slot) — identical subplans are computable once. A formation
   cache keyed by (candidate, slot) is free speedup wherever plans repeat.
5. **Dialogue: parallelize branch matching, keep priority in the reduce.**
   The four template predicates are pure over the utterance; evaluate them in
   parallel and reduce by branch priority (first-match) — same tiebreak trick
   as the argmax. The depth-2 entity chains (`author_of`→`year_of`) stay
   sequential within a branch; they are microseconds.

**What A should NOT expect:** parallel formation does not change any plan
bit (that is the point — byte-identical), so it cannot improve quality bars;
it is purely a COST play, and only where formation is a real fraction of
end-to-end (image today; any future taste-based search at scale).

## 7. Reproducibility

- Prototype: `proto/planform.zag` (pure Zag, no imports), built with the
  pinned znc; `proto/run.sh` runs the full battery (build, seq, S=2 parallel
  shards, normal+scrambled assemble, all `cmp` proofs, DET reruns, render,
  timings → `proto/results/timings.txt`).
- Real-code measurements: `render_bin score` / `render_bin render v2 lib`
  (image); throwaway `/tmp/a1time.zag` driver vs `scenes_inc.zag` closure
  (audio-v1 formation — /tmp scratch, not committed); `imagine_bin_v2 wav m`
  (audio render); `ocean.zag` → `ocean_bin f` (video frame).
- Code cites: imagine.zag:961 (`ig_gen_a1`), :585 (`ig_taste_audio`),
  :2682 (`j2_gen_a1`), field.zag:932 (`f3_synth`); dialogue.zag:1302
  (`do_compose`), :1249 (`year_of`), :1270 (`born_fact_of`);
  screens.zag:322 (`score_candidate`), :407 (`v1_winner`), :99
  (`theme_candidate`); ocean.zag:234 (`o_scene`), :650 (`o_emit_frame`).

## 8. Caveats

- Timings on a 2-CPU VM at load ~20: CPU-seconds (min-of-N) are
  load-independent; wall-batch numbers are noisy and reported as such;
  S=8/64 are projections for an unloaded machine, not measurements.
- The prototype models the *shape* of the real formations (same N=65,536,
  same filter→score→argmax structure, same pure-event construction), not
  their exact constants; the per-modality table in §6 uses the real measured
  numbers.
- Dialogue's mixed verdict: branch-matching parallelism is proven safe by
  predicate purity (code inspection), not by a prototype run — the
  prototype covers the search and constructive patterns, which subsume
  dialogue's slot fills.
