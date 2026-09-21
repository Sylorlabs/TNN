#!/usr/bin/env python3
"""Assemble the class3-standardized driver per source corpus.

For each source in (grok, sol, step, swe):
  src/driver_<src>.zag = HEADER + q2s_trial.zag (import -> corpus_<src>.zag)
                         + s37_step.zag
The only difference between the four drivers is the corpus import.
Reruns of this script are byte-identical.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "src")

SOURCES = ["grok", "sol", "step", "swe"]

with open(os.path.join(SRC, "q2s_trial.zag")) as f:
    body = f.read()
with open(os.path.join(SRC, "s37_step.zag")) as f:
    step = f.read()

HEADER = """\
// driver_<src>.zag — class3-standardized championship driver (ASSEMBLED — do not edit;
// edit src/q2s_trial.zag, src/s37_step.zag, or build/build_driver.py).
//
// Standardized class-3: complete D2 teacher (all 240 facts, q2_phase1_complete)
// teaches a fresh arm-B learner via s37_teach3c (teacher id 20). Identical
// procedure and battery for all four sources; only the corpus import differs.
// Mode (argv[1]): teach3c <label> <rep>. Exit code = failed internal checks.
// N=5 runs of any mode must be byte-identical. Pure Zag, zero RNG.
"""

# import block: the corpus + Q1 §B.7 sources (same set as the step37 driver)
old_imp = '@import("q2_corpus.zag")'
if body.count(old_imp) != 1:
    # the body may already carry a corpus import from the step37 tree; find it
    import re
    m = re.search(r'@import\("(?:s37_corpus|q2_corpus)\.zag"\)', body)
    assert m, "corpus import anchor not found"
    old_imp = m.group(0)

new_imp_template = ('@import("corpus_{src}.zag")\n'
           '@import("q1_types.zag")\n'
           '@import("q1_proposal_s37.zag")\n'
           '@import("q1_tape.zag")\n'
           '@import("q1_tripwire.zag")\n'
           '@import("q1_flawscore.zag")\n'
           '@import("q1_world.zag")\n'
           '@import("q1_learner.zag")')

for src in SOURCES:
    b = body.replace(old_imp, new_imp_template.format(src=src))
    out = HEADER.replace("<src>", src) + b + "\n" + step
    out_path = os.path.join(SRC, f"driver_{src}.zag")
    with open(out_path, "w") as f:
        f.write(out)
    print(f"wrote {out_path} ({os.path.getsize(out_path)} bytes)")
