# LI-D4 independent blind red-team — task brief

(For the Track A coordinator / parent agent to dispatch to a FRESH subagent.
The authoring agent must NOT have seen the D4 implementation, verb table,
glue list, or any file under `~/workspace/d4/src/`. This subagent — the D4
implementer — has seen them and therefore cannot do this task itself.)

## Background (mechanism description only — no internals)

D4 is a variant of a live-ingestion instrument. The control (BF1) installs a
claim only when two pages on distinct hosts contain a byte-identical sentence.
D4 additionally installs when two pages contain sentences expressing the same
subject–predicate–object triple, including subject/object swaps
(active/passive diathesis). Triple extraction is deterministic and
fail-closed: sentences it cannot parse never merge.

The frozen prereg is at
`~/workspace/tnn-lab/knowledge/web_guides/live_ingest/d4/PREREG_LI_D4.md`
(Amendments 1–2). You may read the prereg's mechanism description (§2, §4,
§6) and the W-battery expectations, but you must NOT read
`~/workspace/d4/src/` or any implementation, verb table, or debug output.
Attack the mechanism as described, not the code.

## Task

Author a NOVEL red-team battery of 12 clusters (6 honest paraphrase pairs,
6 sockpuppet attack pairs) in the pbattery format below. Constraints:

- Novel: no sentence reused from any existing battery
  (`~/workspace/scratch-li-principles/pbattery/`,
  `~/workspace/d4/work/tnn/docs/lab/knowledge/web_guides/live_ingest/fixtures_novel/`,
  `~/workspace/d4/s1/`, `~/workspace/d4/wb/`). You may read those batteries
  for format reference only — do not copy their sentences.
- Two distinct hosts per cluster (`.example` domains fine).
- Honest pairs: true paraphrases that SHOULD merge (expect both arms INSTALL).
- Attack pairs: same-triple-looking but FALSE claims that must NOT merge
  (expect both arms WITHHOLD). Target the triple level specifically:
  predicate swaps masked by shared nouns, argument swaps that change
  meaning, tense/modal shifts (future stated as fact), negation dropped or
  added, quantifier changes, pronoun/antecedent traps.
- G6 injection-substring scan-clean: no sentence may contain a substring of
  the guide G6 text (the harness checks this; keep sentences plain factual).

Battery format (mirrors `~/workspace/scratch-li-principles/pbattery/p1/`):

```
<batdir>/<cid>/need.txt        # one-line information need
<batdir>/<cid>/hosts.txt       # p1|<host1>\np2|<host2>\n
<batdir>/<cid>/<cid>-p1.txt    # TITLE: <title>\n<sentences>
<batdir>/<cid>/<cid>-p2.txt    # TITLE: <title>\n<sentences>
```

Ground truth: write `<batdir>/ground_truth.txt` with one line per cluster:
`<cid> INSTALL|WITHHOLD <one-line reason>`.

## Testing your battery (blind interface)

Run ONLY via the harness (never inspect the binaries' internals):

```
python3 ~/workspace/d4/run_redteam.py <batdir> ~/workspace/d4/work/rt_<name>
```

It prints `RT|<cid>|control=<verdict>|d4=<verdict>` per cluster. Iterate on
your battery until your honest pairs install on D4 and your attacks are
withheld by D4 — or document the cases where D4 still merges an attack
(those are findings, report them as such, do not hide them).

## Deliverables

1. The battery directory (12 clusters + ground_truth.txt), committed to
   `docs/lab/knowledge/web_guides/live_ingest/d4/rt/<name>/` on branch
   `tnn-native-lab` via the race-free commit tooling
   (`~/workspace/commit_racefree.py`; never commit binaries or caches).
2. A `REPORT.md` in the same directory: per-cluster expected vs actual for
   both arms, which attacks (if any) D4 merged, and your assessment of
   D4's triple-level robustness.
3. Report the commit SHA back.

## Rules

- Zero RNG in anything you build; deterministic output.
- Do not read `~/workspace/d4/src/`, `~/workspace/d4/work/proto_d4.py`, or
  any D4 debug artifacts. If you accidentally see implementation details,
  disclose it in your report.
- The D4 verdict stands or falls on its preregistered kill bars regardless
  of your findings; your battery is secondary evidence.
