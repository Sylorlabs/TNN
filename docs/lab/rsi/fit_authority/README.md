# FIT instrument authority path (never prune)

Directive D1, adopted by the wave-20260925-1421pdt debate (JUDGE_RULINGS.md):
the frozen tnn_chat probe instruments live here so that no future run-dir
pruning can remove them. Precondition (2) of the standing FIT carry-over
rule requires the frozen chain inputs to be extractable read-only from a
durable path; the 09-23 run-dir pruning broke that precondition on three
consecutive archive branches (0221pdt, 0821pdt, 1121pdt), forcing fresh
re-runs. This directory is the repair. NEVER PRUNE the files below.

## Frozen sources

- tnn_chat.zag (baseline instrument)
  sha256: c0776ad6957e6fff62bdb62569594ca3e2ec2fb18f3cb369ab51f639ed03218c
  frozen built binary sha: 1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c
- tnn_chat_decline.zag (decline-gate instrument)
  sha256: a87011fe10dbc5bac5b0d6e36391033974acfcc46b852618989e3e800cbc3e4b
  frozen built binary sha: 20273a99215680b5e3e42bbdbbfed105c7109d15ba189c903cf0d88db54418e7

## Provenance

Both files were extracted read-only (git show, no checkout) from branch
tnn-native-lab-wave-archive-20260923-2321pdt, paths
docs/lab/rsi/runs/wave-20260923-0834pdt/tnn_chat.zag and
docs/lab/rsi/runs/wave-20260923-1121pdt/tnn_chat_decline.zag, on
2026-09-25 during wave-20260925-1421pdt. The copies here are
byte-identical to the frozen shas above. Both files were grepped for
em-dashes before freezing: zero found. Per standing rule S9, these are
inherited byte-identical sources; they are never edited post-hoc.

## Rest of the frozen chain (reference)

The remaining FIT chain inputs are: the two R33 support sources (under
docs/lab/bytegen/authority_law/dialogue/), the canonical kb.txt and
gaz.txt, the pinned znc (src/tools/toolchain/znc_linux_x86_64_abed8aa1,
sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef),
and the three probe fixtures. Residual: kb.txt and gaz.txt are not yet
in a named authority path; a future wave may extend this directory or an
equivalent to cover them.

## Scope

These instruments certify the 38-fact closed-book probe chain only.
No runnable interactive TNN exists on this branch beyond these frozen
probe instruments. This is not a candidate verdict and it is not merge
review of merged-in work.
