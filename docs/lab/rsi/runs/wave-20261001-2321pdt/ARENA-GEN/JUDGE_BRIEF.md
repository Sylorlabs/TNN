# JUDGE BRIEF: ARENA-GEN (wave-20261001-2321pdt)

RENDER_SHA: (filled at commit; the sha of the commit that
first renders this file)
FIRST_RENDERED_WAVE: wave-20261001-2321pdt
COMPONENT_LINEAGE: ARENA5 BUILD-PASS DEFRECALL (implementation
commit 2320c3454; sealed eval commit 6582398e9)
NEW_KNOWLEDGE_CLAIM: DEFRECALL's default action enumerates the
entity roster for every bare prompt with no specific handler,
including prompts where enumeration is semantically
inappropriate, so it is extensionally a bare-prompt handler
rather than a discriminating general default.

## Verdict: NARROW

Tested ARENA5's DEFRECALL on a fresh multi-bare-prompt
battery (7 items: "listnames", "recall", "who",
"whattime", bare "invent", "invent|notation", "foo|bar")
plus a fresh-seed 68-item battery for regression.

Results:
- AG-1 PASS: C15 = 0.947 >= 0.900 on the fresh 68-item
  battery (seed 71503461337033).
- AG-2 FAIL (5/7): "listnames", "recall", "who" correctly
  enumerate the 9-entity roster (set F1 1.000 each);
  "invent|notation" and "foo|bar" correctly reply UNKNOWN;
  but "whattime" and bare "invent" enumerate the roster
  instead of replying UNKNOWN. White-box trace shows five
  defrecall firings, one per bare prompt, regardless of
  semantic appropriateness.
- AG-3 PASS: zero regressions on the fresh 68-item battery
  (all 15 non-target caps byte-identical to the v6
  baseline; total 0.808 vs 0.794).
- AG-4 PASS: 3/3 byte-identical stripped reply streams.
- AG-5 PASS: pure Zag; no interpreter invocations.

The mechanism is not a listnames handler (zero goal-string
branches, structural trigger; ARENA5's intensional claim
stands). But it does not discriminate across bare prompts:
it is extensionally a "bare-prompt handler". ARENA5's dev
generality demonstration was one-sided (only prompts where
enumeration is appropriate); this lane supplies the
negative cases. The generality claim is qualified, not
refuted.

Full evidence: EVAL_REPORT.md in this lane directory.
Frozen prereg: PREREG_MULTIBARE.md (commit ef30ef8d1).
No mechanism source was modified; evaluation only. No L3
claim. The canonical 0.573 is not moved.
