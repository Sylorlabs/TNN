# Recovery debate: F3a3 step 4 (independent reproduction) COMPLETE

Parent-agent inline, 2026-09-30. Wave 20260930-2321pdt died on the
descendant-subagent runtime defect (eleventh kill) before convening
its debate, but its hpi_rev2_repro lane completed and committed the
step-4 independent reproduction (6d778b960) before dying. This record
debates the narrow claim: 11-step pipeline step 4 for F3a3 is
complete.

## Advocate

The lane is a genuine independent reproduction: a different worker
from the 11:21 evidence producer, source extracted via git cat-file
from 847a8f10f into /tmp only, built with the pinned safebin znc,
never touching the working tree. Three runs with argv[1]=v, all exit
0, empty stderr, all byte-identical to the committed evidence
(sha256 b5389d713357d37bd5ca9c05b781e80d57a3a764f3cac60ebe1cd17de9527c8e).
K-F3-1..4 bar markers re-checked on the reproduction output with
fixed-string grep: all present. Prereg 53256838f verified as strict
ancestor of evidence d1b6ec51f. Pure Zag, zero Python, NAMECHECK
guard recorded. REPRO-PASS.

## Skeptic

Provenance probe: the reproducer is a loop worker, not an outside
party; "independent" here means independent of the evidence
producer, which the /tmp-only build and git cat-file extraction
support. The skeptic's press: step 4 reproduces the EVIDENCE, but
the evidence itself was produced under the third-draft bar text
(the 11:21 M1 caveat stands and is not cured by reproduction).
Reproduction confirms determinism and integrity, not bar fairness.
Also: the reproducer used the same pinned znc binary; a compiler
bug would reproduce identically. That is a shared-infrastructure
limit, not a flaw in this lane.

## Judge

Step 4 is COMPLETE. The parent independently verified the three
load-bearing claims: (1) all three repro run files share one sha256;
(2) prereg 53256838f is a strict ancestor of evidence d1b6ec51f;
(3) the committed evidence blob from d1b6ec51f hashes to the same
sha256 as the repro runs. The skeptic's caveats are adopted into
the record: reproduction confirms integrity and determinism, not
bar fairness (the M1 third-draft caveat stands); the shared-compiler
limit is noted. F3a3 pipeline status: steps 1 (prereg), 2
(implementation), 3 (sealed evaluation), 4 (independent
reproduction) complete. Step 5 (simple-baseline comparison) is next
in the queue.
