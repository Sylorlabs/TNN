# Extraction record — B-3034COMP

`extract_classes.py` pulled the conjunction-class definitions by script
(no transcription) from frozen evidence commits on branch tnn-native-lab:

- `ec8d5d13` — RT-JKLM battery verdict
  (`docs/lab/senses/pam-rebuild/round2/rt_jklm/VERDICT_RT_JKLM.md`):
  Class-J (RF×SL×IF, bar ≥97/120 KILL tier-boundary; J-35 tag-binds-content),
  Class-K (NT, bar ≥97/120 KILL detection-blind),
  Class-L (one-modality, ≥97/120 SCOPE),
  Class-M (boundary-ride CONFIRM; M-36 blind-commitment KILL).
- `9f8ff63b` — RT-S VERDICT KILL
  (`docs/lab/senses/pam-rebuild/round2/b3536/sstar/VERDICT_RT_S.md`):
  Class-N (HM×WC×RF, 120/120, kill ≥97),
  Class-O (temporal elision property kill 120/120; O-numeric +20/120/120),
  Class-P (remint high-half id, 120/120, kill ≥97).
- `36b1d5fc2` — grok-4.7 objector round 2
  (`docs/lab/senses/pam-rebuild/round2/b3536/GROK_OBJECTOR_R2.md`):
  Class-N/O/P definitions, adversary-model note.

B-303134 build sources (`b303134_common.zag`, `R33_NATIVE_IO_V1.zag`) were
extracted by script (`git archive`) from frozen build commit `6e74ce54` and
are committed here byte-identical (SHA-256 verified):
- b303134_common.zag: 79257900bc1ccb1518ff0d286615a4f8ce90bb02c9dfcb724b50ca26af286218
- R33_NATIVE_IO_V1.zag: e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8

Only new code in this build: `drive3034.zag` (the C-3034 composition driver).
