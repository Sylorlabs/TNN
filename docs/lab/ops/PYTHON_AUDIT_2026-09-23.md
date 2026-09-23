# Python-Use Audit — 2026-09-23

Micah's order: "i think some groups might be running python so redirect if needed and document results."
Standing law: TNN's decision paths, mechanisms, learners, and verification are pure Zag.
Python is allowed ONLY as glue or analysis — never deciding anything for TNN,
never in the learning/inference path.

## Method

- Enumerated all 716 `.py` files under `~/workspace/tnn-lab` (excluding venvs/site-packages).
- Read the docstring/head of every file in a decision-adjacent role across
  senses, imagination_discovery, knowledge, ops, dialogue, rsi, kb, epistemics,
  scale, info-source, brain.
- Inspected all 4 python processes currently running on the VM.
- Grepped for ML-library imports (torch/tensorflow/sklearn/jax/transformers/gym):
  **zero hits** anywhere in the lab.
- Grepped every `.zag` file for python shell-outs: 3 hits, all benign
  (a "python" language mode in `units/wide/charz.zag`; a "regenerate with
  python3 gen_course.py" header comment in `ht_course.zag`; a "verify the LUT
  with python math.sin" comment in `imagination/src/sin_lut.zag`).
- Checked the 1GB-ingestion and web_real python for install-decision logic: none
  ("install" appears only in kill-bar comments; the verdict core is a Zag binary).

## Verdict: 0 forbidden instances

No python sits in any TNN decision path, mechanism, learner, or live verification.
Nothing TNN treats as knowledge or behavior is produced by a python decision.
No rewrites required; no crews needed redirecting.

## What the python IS doing (all allowed)

1. **Harness orchestration (glue)** — the bulk. Run frozen Zag binaries via
   subprocess, parse `key=value` stdout, hash outputs, diff reruns for
   byte-identity. Examples: `senses/rebuild/harness/run.py`,
   `senses/pam-rebuild/forks/*/eval/*.py` (stream_h3, b6_single_scan,
   det_h2), `rsi/composer_build/driver/driver.py`,
   `imagination_discovery/aud/b_gamma/render_verify.py`,
   `rsi/autonomous_run_2/src/loop_driver.py`.
   Currently-running processes (`run_iso.py`, `b6_single_scan.py`, crossref
   `run.py`) are all in this class.

2. **Analysis / scoring (analysis)** — numpy/PIL waveform and image metrics,
   log parsing, trial score tables, plots. Examples:
   `imagination_discovery/vid/r4/score_mech.py`, `aud/*/.../analyze_*.py`,
   `kb/autopsy/channels2/score_*.py`, `epistemics/*/score_pl*.py`.
   Micah's ears/eyes still outrank these metrics by standing rule.

3. **Corpus and battery generation (teacher-side data prep, glue)** — wikitext
   extraction (`knowledge/ingest_1gb/extract/wiki.py`, `wikt.py`, `wn.py`),
   frozen battery CSVs (`dialogue/gen_dialogue.py`, `kb/autopsy/probes/gen_probes.py`,
   `knowledge/chunking/gen_battery.py`), negative-control fixtures
   (`ingest_1gb/extract/make_bad.py`), adversarial fixture builders.
   This is teacher-authored content prep, not TNN deciding. The extraction
   scripts stream deterministic dump order; no quality-judging of facts.

4. **Codegen (build glue)** — generate `.zag` sources/includes from frozen
   inputs. Examples: `imagination_discovery/img/r10/gen_beauty.py`
   (string-patches the frozen r8b renderer — the renderer itself is Zag),
   `rsi/autonomous_run_2/apparatus/work/gen_engine.py` and
   `translate_policy.py` (policy DSL -> bytecode; the policy ENGINE that
   decides is pure Zag), `info-source/gen_is.py` (emits `is_cases.zag`).

5. **Transport (glue)** — HTTP fetch bridges for web search
   (`senses/web-search/v2/transport/ws_bridge2.py`,
   `knowledge/web_real/bridge/fetch.py`). Explicitly no deciding, no judging,
   no filtering, no installing; wall-clock is kept on the python side and
   never enters the Zag ledger (reruns stay byte-identical). The verdict,
   quarantine, corroboration-counting, and install/withhold judgments are all
   in pure-Zag binaries. (Known scope limit, already documented in the
   FIRST-CRAWL report: corroboration fetching is still harness-driven;
   independent-source discovery is phase 2.)

6. **Independent recompute oracles (test scaffolding)** — python re-derives a
   result to cross-check the Zag implementation (e.g. `det_h2.py`'s ledger
   recompute, `verify_ledger.py`, the sin-LUT math.sin check). These check the
   implementation; they are not TNN's own verification.

7. **Calibration (allowed by standing rule)** — `senses/rematch/code/fit.py`
   sweeps preregistered threshold grids on cached binary records with
   deterministic tie-breaks; fitted constants are frozen INTO the Zag sense
   binaries. Stubs/calibration only, never headline evidence.

## Boundary items (not forbidden — conditions to honor)

- `senses/youtube_ingest/gate.py` implements the install/withhold memory rule
  in python — BUT only as a simulation scaffold: vision verdict is GATED, no
  real memory is touched, outputs are logged install-intents only.
  **Condition: if vision readiness ever flips to READY, this rule must be
  ported to pure Zag BEFORE any live install.**
- `senses/rebuild/harness/score.py`'s `apply_memory_rule` is the trial scorer's
  shared rule for comparing approaches — not TNN's memory path. The canonical
  memory rule lives in the Zag learner and the S5 store.
- Historical dirs (`wave3`–`wave12`, `coding`, `units`, `prose-learning`) hold
  ~400 more analysis scripts from completed trials; same classification
  (analysis/glue), none in any live path.

## Bottom line

Micah's suspicion was reasonable — python is everywhere in the lab — but it is
all harness, analysis, data-prep, codegen, transport, and test scaffolding.
The intelligence itself (senses, memory rule, verdict cores, learners, renderers,
dialogue binary, composer, RSI policy engine) is pure Zag. Nothing to rewrite.
