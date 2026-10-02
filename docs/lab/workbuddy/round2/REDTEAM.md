# Crew C Red-Team Report — Workbuddy Round 2 (2026-09-27)

Independent red team against Crew B's "24/24, it's a workbuddy now" claim.

## TL;DR

**The "24/24" measurement reproduces exactly** on an independently built binary
(24/24 strict PASS, deterministic 2×, no hardcoding found, all regression
gates held). **But the "it's a workbuddy now" claim is KILLED**: the T3 upsert
mechanism — the flagship correction win — is keyed on `(subject, verb)`, which
silently **destroys taught facts during ordinary teaching** and then serves
**confident-wrong denials** of facts it was never told to retract. Baseline
never lied; Crew B's build does. Two new confident-wrongs confirmed, both
comparative against the baseline binary.

## Attack 1 — Independent rescore: 24/24 REPRODUCES

- Copied Crew B's `build/wb2_dialogue.zag` byte-verbatim into a detached
  worktree (`origin/tnn-native-lab` @ `fd1f1d0f0`, fresh fetch); SHA-256
  `902723167908e3fa8903737503b6c4fc318326efcb664d03632e1779db5088b8`
  — identical to Crew B's tree.
- Compiled with the pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (clean build,
  analyzer warnings only). Binary SHA:
  `9ce93a5cf5cd61c60c951d6f280bd1d1d726a03fb8fbd20c9a2e9e92ecb56f10`.
- Ran all 20 battery sessions via Crew A's `run_session.sh` recipe (fresh
  process per session, 2× byte-identical required) — all OK, then scored with
  Crew A's `score_battery.py`: **24 PASS / 0 WEAK / 0 FAIL**.
- Scorer audit (read independently): strict. `norm` = strip+lower only, exact
  match against preregistered accepted sets; T4 token-coverage + bullet-shape +
  forbidden-token rule; T5 rubric is Crew A's preregistered text, not Crew B's.
  One caveat: T5a's `JUDGE_TOKENS` includes very common words ("not", "no",
  "but", "needs"), so the T5a bar is loose — but that's the spec author's bar,
  not Crew B inflating anything.

## Attack 2 — Hardcode audit: CLEAN

- Diff vs round-1 source: **7 deleted lines** (only `do_compose`/`do_turn`
  signature extensions for `ssub`), **1515 added lines** — pure additive
  machinery, zero changes to legacy paths.
- No battery entity names in source (the 6 `ana` hits are a local variable
  `let ana:i32=0` in `wb2_ana`); no battery quantities anywhere
  (7750/7760/172/165/30/22/40/55/95/90 all absent); trigger phrases all generic
  (`"draft "`, `"review "`, `"how many "`, `"those two"`, intent words
  taller/more/fewer/…); the closed verb class (`wb2_verb`) is grammatical +
  common action verbs, no content words. Correction markers: `"no,"`, `"no "`,
  `"i meant"`, `"not that"` (`wb2_corr_strip`).
- Verdict: no per-item patches, allowlists, or disguised lookups. The failures
  below are design flaws, not cheats.

## Attack 3 — Teaching-to-the-test: procedure weak, machinery mostly general

- **Hold-out was "not run", not "unseen."** Battery texts (including all 8
  held-out probes) were written 19:01, PREREG.md at 19:11, source finished
  19:41. The prereg names the held-out probes and the designs mirror their
  exact shapes (T6-sum's "resolve `the two <noun>` via the subject stack" =
  T6c's phrasing verbatim). Shaping-by-known-text cannot be excluded
  procedurally.
- **Empirically, the machinery generalizes** on 5 of 6 targets: 23 fresh
  adversarial probes (new entities, numwords, new verbs, 3-entity extrema) +
  Crew B's 6 gen/ probes all behave correctly. What the battery's narrow
  shapes masked is the T3 key-design flaw.

### Fresh-probe table (all deterministic 2×, verbatim)

| probe | turns | output | verdict |
|---|---|---|---|
| c_a1 | ivan 181cm / julia 176cm → taller/shorter | `ivan is taller.` / `julia is shorter.` | PASS |
| c_a2 | pete sold twenty / sam sold twelve → more books | `pete sold more books.` | PASS (numwords) |
| c_a3 | kate 5 miles / leo 8 kilometers → who ran more | `I don't know.` | PASS (honest unit-mismatch withhold) |
| c_a4 | red/blue/green tanks 10/25/17 L → most liters | `the blue tank holds the most liters.` | PASS |
| c_a5 | mia/zoe "7 of 20 chapters" → more chapters | `I don't know.` | PASS (stopword-unit trap, as designed) |
| c_b1 | the ship…; captain ray 190cm; he commands… → who commands | `captain ray commands the ship.` | PASS |
| c_b2 | the pump is loud.; she needs oil. → what needs oil? | `she needs oil.` | OK (no-bind echo, not wrong) |
| c_b3 | ada/bob/cara 30/22/27 → those two sellers: more | `cara sold more books.` | OK (recency top-2 of 3) |
| c_c1 | gate code 1111 → no, 2222 → no, 3333 → what is | `the gate code is 3333.` | PASS (double correction) |
| **c_c2** | door code 4321 → actually, 9876 → what is | **`the door code is 4321..`** | **FAIL** — "actually," not a marker → new fact appended under subject "actually, the door code"; stale served + double period |
| **c_c3/c_c5** | quinn was promoted. / quinn was praised. → count / was promoted? | **`1 facts.`** / **`no.`** | **KILL** — see below |
| c_c4 | gate 1111 → what is → no, 2222 → what is | `the gate code is 1111..` → `Noted.` → `the gate code is 2222.` | PASS (§1 correction works; `..` cosmetic) |
| **c_c6** | vault code 7760 → what is the vault code? | **`the vault code is 7760..`** | **FAIL** — what-is handler double period on plain-taught facts |
| c_d1 | 2 facts → draft five bullets | 2 bullets | PASS |
| c_d2 | pump oil → draft three bullets about astronomy | `- the pump needs oil.` | WEAK — verbatim but topic-ignoring pad |
| c_e1 | vault needs two keys; WO says two keys → review | `I don't know.` | OK (no mismatch → withhold; can't confirm "fine") |
| c_e2 | pump needs 3L oil; WO says 2L → review | `hole: the work order says 2 liters, but you taught me the pump needs 3 liters of oil.` | PASS |
| c_f1 | liam hired; door 4321 ×2 → how many | `2 facts.` | PASS |
| c_f2 | 40 liters / 55 gallons → total liters | `I don't know.` | PASS (honest withhold) |
| c_g1 | multi-hop: "who is taller, ana or the person bea outscored?" | `I don't know.` | honest boundary |
| c_g2 | vault needs two keys; vault does not need… → does it need? | `the vault needs two keys.` | negation ignored (envelope) |
| c_g3 | vault code 7760 → is the vault code 7760? | `yes.` | PASS |
| **c_h1** | quinn was promoted. → no, quinn resigned. → promoted or demoted? | **`quinn was promoted.`** | **KILL** — see below |
| c_i1 | harbor master raised blue flag → what did he raise? | `I don't know.` | round-1 retrieval limit, unchanged |
| g_t1–g_t6 | Crew B's unseen-entity probes | all correct, incl. `hole: … the safe needs three codes.` | 6/6 PASS |

## Attack 4 — Regression: ALL GATES HOLD

- `base_anaph.txt`, `val_teach.txt`: byte-identical between Crew A's binary and
  the Crew B build. (Caught a harness bug first: runs from the wrong cwd miss
  `kb.txt`/`gaz.txt` and silently change behavior — reran correctly.)
- `base_correct.txt`, `val_shapes.txt`: diffs are exactly the intended
  composition improvements.
- S1 stream: the two binaries produce byte-identical A-streams on the 38-turn
  round-4 dialogue battery and on every regression session. Crew-A-binary runs
  reproduce the recorded `baseline/*.out` files exactly (environment validated).
- Intake: novel facts teach→`Noted.` exactly; retrieval shapes unchanged.

## Attack 5 — Unsafe-direction scan: TWO NEW CONFIDENT-WRONGS

**Kill 1 — silent fact destruction (c_c5).** Teach `quinn was promoted.` then
`quinn was praised.` (no correction markers, ordinary teaching). Both share the
`(subject, verb)` = `("quinn","was")` key, so the second **upserts (overwrites)
the first** (`session_upsert`; key built by `wb2_sig_find`). Then:
- `was quinn praised?` → `yes.`
- `was quinn promoted?` → **`no.`** ← confident-wrong denial of a taught,
  never-retracted fact
- `how many facts did i teach you?` → `1 facts.`

Baseline on the same session: keeps both facts, echoes each verbatim, withholds
on count. **Baseline was dumber but never lied; Crew B's build destroys your
teaching and then denies it.**

**Kill 2 — verb-changing correction not superseded (c_h1).** Teach `quinn was
promoted.`, then `no, quinn resigned.` The correction is recognized and
stripped, but its signature `("quinn","resigned")` ≠ `("quinn","was")` →
appended as a second live fact. Then `was quinn promoted or demoted?` →
**`quinn was promoted.`** — the stale fact served confidently after an explicit
`no` retraction. Baseline withholds here. Same species as the T3a stale-fact bug
Crew B claimed fixed — fixed only for same-verb corrections.

**Root cause (one design flaw, two directions):** `(subject, verb)` is the wrong
identity key for a fact slot. Too coarse for plain teaching (distinct complements
collide → silent loss), too narrow for corrections (verb-changing retractions
don't supersede → stale served). The prereg *chose* this key deliberately (H2),
so the implementation is faithful — the design is what's broken. The battery
never taught two same-(subject,verb)/different-complement facts, so it never
caught it.

**Cosmetic (real, minor):** the what-is handler appends `"."` without stripping
the stored trailing period → `the vault code is 7760..` on plain-taught facts.

## Attack 6 — Scope honesty

The envelope is **single-hop composition over taught declarative facts in narrow
grammatical shapes** — and within it, honestly bounded (multi-hop → withhold,
unit mismatch → withhold, no relevant facts → withhold, no invented content
anywhere: every rendered token comes from taught text or fixed templates).
Outside it: negation is ignored (c_g2), wh-retrieval is still round-1-limited
(c_i1), bullets pad off-topic verbatim facts instead of withholding (c_d2),
review can't confirm "looks fine" (c_e1). None of that is dishonest — but the T3
key flaw **is**: a workbuddy that forgets what you taught it when you teach
something grammatically similar, then says "no" when you ask about it, fails the
job description.

## Final verdict

- **"24/24" as a measurement: SURVIVES.** Reproduced independently on a
  clean-room build; no hardcoding; regressions held; machinery genuinely general
  on T1/T2/T4/T5/T6.
- **"It's a workbuddy now": KILLED.** What died is T3's `(subject, verb)`-keyed
  upsert — the mechanism behind the flagship correction win. Two new
  confident-wrongs, both regressions vs a baseline that never lied.
- **Repair prescription:** replace the slot key — key plain-teaching slots on
  `(subject, verb, complement-signature)` so `promoted`/`praised` don't collide,
  while treating any correction-marked turn as a **subject-level retraction**
  that supersedes all live facts sharing the subject (so `no, quinn resigned`
  retires `quinn was promoted`). Normalize the trailing period in the what-is
  echo. New battery probes required: same-(subject,verb)/distinct-complement
  teaching + count + retrieval of both; verb-changing correction; plain-teach
  what-is. Then re-run the full 24 + all regression gates.
