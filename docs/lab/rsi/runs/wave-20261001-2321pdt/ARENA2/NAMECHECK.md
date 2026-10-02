# NAMECHECK: ARENA2 lane, wave-20261001-2321pdt

Replacement builder for the ARENA lane family. Task: pick one zero
capability other than INQUIRY (C8, taken by the sibling ARENA lane),
freeze a prereg with kill bars, implement in pure Zag, run sealed
evaluation plus the full capability regression, report BUILD-PASS or
BUILD-FAIL.

## Step 0: toolchain guard (2026-10-01 ~23:35 PDT)

Ran from ~/workspace/tnn-rsi:
  sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  export PATH="$HOME/safebin"

Setup output:
  safebin: /home/hatch/safebin
  linked: 36 tools
  znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
  verify: python3 absent from safebin PATH (OK)
  verify: python absent from safebin PATH (OK)
  SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)

Verification:
  $ which python3
  (no output; exit code 1)

`which python3` prints nothing. Pure Zag only for this lane. Any
forbidden-interpreter invocation is PROCESS-FAIL and voids the verdict.

## Capability pick (recorded before prereg freeze)

Zeros in the v6 refreeze (54/68 = 0.794, 16 capabilities): C8 (n=4),
C9 (n=3), C12 (n=6), C15 (n=1). C8 is taken by the sibling ARENA lane
(PREREG_ARENA_INQUIRY.md); not duplicated here.

C9 (causal) was examined first per the recommendation. Finding: C9 as
implemented is unpassable by any genuine causal mechanism, so it is
REJECTED as the pick. Evidence:
  - The 12 causal expo turns are {"t":"c","x":b,"y":b,"z":b} with
    x==y==z in every observation (world_gen.zag CHECK 1 enforces it).
    The chain permutation is observationally unidentifiable from this
    evidence by construction ("observationally indistinguishable by
    design for capability 9", ARENA_PREREG.md line 95).
  - The battery contains zero intervention turns; the original C9
    protocol (choose a discriminating intervention, observe, eliminate)
    was never implemented.
  - The implemented items are discrim|<chain>|<alt> where the TRUE
    chain is ALWAYS the first candidate (world_gen.zag lines 487-517:
    the emission loop writes the chain first, then an alternative),
    and the key is chain[0]. The only 3/3 mechanism is "parse the
    first candidate, emit its first variable", which uses zero
    experience, builds zero causal structure, and is a
    benchmark-format exploit, rejected under the no-gaming rule.
  - The honest causal answer (UNKNOWN, direction unidentifiable)
    scores 0. A genuine causal-model mechanism therefore cannot meet
    a C9=3/3 kill bar.
This is reported as a negative finding (battery defect: recommend the
world generator randomize candidate order and add real intervention
turns). It is not built here.

C15 (goal, n=1, "listnames") rejected: single item, narrow
enumeration mechanism, ordering-fragile, low information gain.

C12 (transfer, n=6) SELECTED. Justification:
  - Genuinely zero in the v6 refreeze (0.000, verified in
    REFREEZE_RECORD.md, wave-20261001-1721pdt).
  - Genuinely passable: remap_prod asks for the learned Zem transform
    output under a question-given value permutation; remap_class asks
    whether a remapped triple matches the learned template under the
    same permutation. Both are solved by composing the learner's own
    exposure-learned templates (the same structures behind v6's
    C10/C16 1.000) with the permutation parsed from the question.
    No sealed values, no hardcoded answers, no experience-free
    parsing trick: the mechanism reuses learned structure under a
    novel encoding, which is what transfer means here.
  - 6 items, so the gain is material (54/68 -> 60/68 = 0.882 if all
    pass), and the mechanism generalizes to any permutation and any
    learned template.
  - Adjacent to the composition frontier: learned-structure times
    novel-encoding composition, the same X+Y->Z shape as the
    composition mechanisms, but in the transfer family.

## Lane log

- 2026-10-01 ~23:35 PDT: Step 0 toolchain guard recorded. Safebin
  active, python3 absent. Lane directory created.
