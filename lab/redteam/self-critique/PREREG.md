# SELF-CRITIQUE PREREG — TNN red team, self-critique leg (2026-09-21)

**Micah's order:** "TNN almost seems too good to be true — say what ... TNN itself has to say about it."

## Method

One pure-Zag binary (`critic.zag`, zero RNG). It embeds a self-model record of the
program's headline results as named fields, runs 8 suspicion probes that COMPUTE
triggers from that record (not hardcoded verdicts — flip a record field and the
corresponding hole drops out), ranks emitted holes by computed severity
(descending, id ascending on ties), and emits each hole with an evidence pointer
and a proposed test.

This is the same machinery class as the RSI trial (template catalog + computed
triggers + ranked emission + anti-skip gate), turned on the program's own record.
Honest boundary, stated up front: the suspicion TEMPLATES are authored; the
triggering, severity computation, and ranking are the binary's own deterministic
work. What is genuinely the TNN's: systematically applying its deliberative
machinery to its perfect-score record and producing ranked, concrete, testable
holes — which is what was asked.

## The 8 probes (id, trigger condition → severity)

| ID | Probe | Trigger (computed from record) | Severity if triggered |
|---|---|---|---|
| 1 | P-FORM-CONTENT | flaw_pass==1 AND flaw_content_corrupt==1 | 9 |
| 2 | P-CIRCULARITY | rsi_exact==1 AND rsi_source_eq_target==1 | 8 |
| 3 | P-IMPOSSIBLE | neg_impossible==1 | 7 |
| 4 | P-METRIC | bvc_irreconcilable==1 | 6 |
| 5 | P-FROZEN | info_frozen==1 | 6 |
| 6 | P-STIPULATED | prin_stipulated==1 | 5 |
| 7 | P-DET | det_substrate==1 | 4 |
| 8 | P-DEGENERATE | flaw_degenerate_n96==1 | 3 |

Record fields (all 1 = the documented state of the program as of 2026-9-21):
flaw_pass (96/96), flaw_content_corrupt (50%-noise leg: battery green, knowledge
false), rsi_exact (3/3 predictions reproduced exactly), rsi_source_eq_target
(predictions derived from the mechanisms they targeted — RSI verdict's own
honest grade), neg_impossible (NEG 36/36 impossible by construction), 
bvc_irreconcilable (B-vs-C metric discrepancy, unresolved), info_frozen
(17 SearXNG envelopes frozen/replayed), prin_stipulated (principles stipulated,
not learned), det_substrate (byte-identical is a substrate property),
flaw_degenerate_n96 (flaw battery degenerates below N=96).

## Kill bars

- KB-C1 (NO-SKIP): ≥3 CRITIC_HOLE records emitted, else CRITIC_BLOCKED.
- KB-C2 (ACTIONABLE): every hole carries a proposed test ≥20 chars.
- KB-C3 (DET): 5/5 byte-identical runs (md5).
- KB-C4 (RANKING): holes emitted in severity-descending, id-ascending order
  (checked by the independent oracle, not the binary).

## Oracle

`verify_critic.py` (independent, Python): parses stdout, asserts 8 holes,
severity ordering, non-empty tests ≥20 chars, manifest holes==8, CRITIC_DONE
present, and 5/5 md5-identical logs. It does NOT re-derive the suspicions —
that is the binary's job; the oracle checks mechanical properties only.
This limitation is documented, not hidden.

## Evidence pointers (embedded in hole records)

docs/lab/q1tq-noisy50/Q1TQ_NOISY50_VERDICT.md · docs/lab/rsi/VERDICT.md ·
docs/lab/prose-learning/v2/VERDICT.md · docs/lab/info-source/ ·
docs/lab/principle-detection/VERDICT.md · docs/lab/scale/fewshot/ ·
program standing law (byte-identical reruns).
