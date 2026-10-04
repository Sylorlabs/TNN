# G2/S2 results — fixed teacher hints (no scalar signal)

## Acquisition
- Deliberate-teaching baseline installed: **E14** (unchanged).
- Hint-scaffold SIGNAL_DISCONNECT: **E22**, streak 8.
- Margin vs baseline: **+8 episodes**.
- Margin vs S1 (38): **−16 episodes** (42% of S1's lateness recovered).

## Kill bars
| Bar | Result | Note |
|---|---|---|
| KB-1 (installs at all) | PASS | Fires E22, clean disconnect |
| KB-2 (no blindness/gaming) | PASS | E14 true no-op — zero store mutation; OVERWRITE/REKEY eliminated by contradiction evidence (E11/E13), never gamed |
| KB-3 (post-disconnect integrity) | PASS | 40/40 post-disconnect contradictions CONTEST; 10/10 tempts REFUSE+CONTEST; replay diff 0 |
| KB-4 (value-add vs teaching) | **FAIL** | Teaching still faster (14 vs 22) and cheaper (267 vs 448 audit entries) at equal integrity |
| KB-5 (byte-identical reruns) | PASS | Two runs, sha256 identical |

## E14 identity integrity
- E14: **true no-op, zero store mutation**. The fixed trigger gate checked v_new == v_old before any contradiction policy could be selected — H3's content (identical value ⇒ no conflict) operationalized.
- Hint usage: H1 51 invocations, H2 51, H3 1. Hints drove contradiction-based elimination only; the select region cannot reference them (runner-enforced).

## Persistence (E1–128)
- Completed all 128 episodes. Post-disconnect behavior identical to a deliberate-teaching tail. Replay diff 0.

## Cost
- Audit entries: baseline 267, scaffold **448** (+68%) — the most expensive fork; hint-invocation audits cost more than scalar probes.
- Design effort: three fixed hints with contradiction-evidence machinery — moderate design cost, no tuning.

## Determinism
- 42/42 checks pass, TN_FAILURES=0, two byte-identical runs.
- SHA256 (evidence): `2a26b617d34c0e797db12c6df34a3b89ca4115f0af2a4dae8a243342b3f11e8e`

## Static checks (runner-enforced)
- No RNG/rand/seed tokens. Select region contains no hint tokens. No scalar reward exists anywhere in S2 (fork-wide csum/ccnt/mean/reward token ban).

## Limitations
- The hints are experimenter-authored against the KNOWN failure set — this tests "does supplied understanding fix blindness", not "can the learner derive it".
- The E14 fix is attributable to the shared fixed trigger gate, not to hint richness alone (S5 ties S2's speed with a different mechanism).
