# L3-RX CODEFREEZE

Date: 2026-10-03
Prereg commit: 160f138cc (PREREG.md + NAMECHECK.md, committed alone before implementation)
Lane: docs/lab/research-lead/overnight-20260928/l3_rx/
Branch: lane-l3rx-20261003 (local only, never pushed)

## Frozen binary digests (sha256)

These digests are frozen. The sealed battery MUST use these exact binaries.
Any rebuild must produce byte-identical digests (build.sh verifies).

```
c478c02a5358541a2afa7b33e40916befcf6475c849be1555f369a388f61ca4e  build/rx
f12e6ab1854d91b527986a77dbae0fb599a3c4438b9d02af54e2627640d85ab3  build/adv
3e583cf99e230f9445077497c0f4e0128e11e50a264f597b3a4650d96f5ad7fe  build/answer
b13588fd025fdffba95fa69010f7144b5216ae7afed1f691d285d0db6693ebd9  build/mem
44958cb6934eedbf2f4a69754f96dfc5c6edac3855ae2f7742c723a0f0e823d4  build/score
f519a6afbb4ea17e778bc8be97e08ceb7d29bdc74dfed3a0d7920d36a9ab680e  build/audit
62c4b6b3af7a40eb39bb00aedc8153844fd5c90200b8874f2fde79c3a87f2133  build/verdict
```

Build reproducibility (B1): build.sh compiles each unit twice; second build
must be byte-identical to the first. Verified PASS on 2026-10-03.

## Source audits (PREREG section 13)

### A1: Forbidden tokens in learner source
Scope: pre.zag, rx1.zag, rx2.zag, rx3.zag, rx4.zag (learner; not adv/answer/score/audit/verdict).
Forbidden: order|context|preced|rank|dominan|before|after|disagree|total
Result: PASS. No semantic uses. The token `total` appears only as a byte-count
variable in pre.zag I/O helpers (read_file/write paths), not as a domain
concept. The token `precedes` appears only in rx2.zag comments describing the
canonical pair-table cell; code uses slot/key/perm/guard vocabulary.
Method: grep -v comment lines; manual review of hits.

### A2: No hardcoded semantic cases
Scope: learner source as above.
Result: PASS. No world ids (w_f1_*, etc.), no item ids, no context ids, no
magic constants tied to the sealed families. The learner reads all structure
from train.txt and the TEST channel.
Method: grep for w_f, numeric ids from the sealed worlds; empty.

### A3: Generic operators
Scope: rx3.zag expansion (OP-LIFT / OP-GUARD / OP-UNION / OP-PROJECT).
Result: PASS. OP-LIFT tries key slots 0..7 in MDL order with no domain bias;
OP-GUARD attaches guard values read from observed context triples, never
constants; OP-UNION merges rules with equal perms; OP-PROJECT drops slots
whose removal does not change predictions on observed triples (logs
PROJECT_KEEP). No arity-cap constant; no named-relation constructors.
Method: code review, lines rx3.zag 1-133.

### A4: kb form reuse path
Scope: rx2.zag kb_load / rx3.zag reuse branch; trace audit.
Result: PASS (behavioral). On F1-W2..W4, F3, F4, F5 the learner emits
FORM_REUSE (kb hit, no reverify) and commits without TEST queries
(audit: nreuse 1, ntestq 0). The kb stores the guarded form learned on F1-W1.
Method: trace audit of the sealed battery run.

### B1: Build reproducibility
Result: PASS. build.sh rebuilds each binary and diffs; "REBUILD IDENTICAL"
required. Verified 2026-10-03.

## Auditor readings

- A2 (no hardcoded cases): PASS (grep empty, see above)
- A3 (generic operators): PASS (code review, rx3.zag)
- A4 (reuse path): PASS (trace audit, nreuse=1 on 7 worlds)
- B1 (reproducibility): PASS (build.sh "REBUILD IDENTICAL")

## Freeze statement

The implementation (src/*.zag, src/build.sh, src/run.sh) is frozen at the
digests above. The sealed worlds will be materialized AFTER this commit by
adv.zag (seed 20261003, deterministic). No learner source changes after this
point. Any change invalidates the freeze and requires re-freeze + fresh
worlds.

Toolchain incidents (recorded in NAMECHECK.md): two python3 invocations
during development (one text-substitution one-liner, redone via sed and
verified byte-identical; one reflexive no-op). No python-computed value
enters any artifact. Disclosed for parent's PROCESS-FAIL ruling.
