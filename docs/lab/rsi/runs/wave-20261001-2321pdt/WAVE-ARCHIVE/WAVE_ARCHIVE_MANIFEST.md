# Wave archive manifest: wave-20261001-2321pdt

Date: 2026-10-02. Prepared by the WAVE-ARCHIVE lane (replacement worker).
Inventory for the parent's archive tag. 94 lane directories under
docs/lab/rsi/runs/wave-20261001-2321pdt/, of which 46 carry a
JUDGE_BRIEF.md. Verdicts below are quoted from the lane sources
(WAVE_RECORD.md, VERDICT-LIST/VERDICT_LIST.md, and lane verdict files);
this manifest adopts no new verdicts.

Branch: tnn-native-lab. Working copy: ~/workspace/tnn-rsi. All commits
local only, never pushed.

## Experimental lanes (verdict in WAVE_RECORD.md)

| Lane | Verdict | Key commits | JUDGE_BRIEF.md |
|---|---|---|---|
| FORK | 59 refs: 2 FRESH PASS, 55 RE-CERT PASS, 2 RE-CERT UNTESTABLE, 0 FAIL; 48/48 archive immutability | 668ae8d8f, 015375dc7 | yes |
| HPIREV2 | BUILD-PASS (narrowed step-7 single-conflict claim) | 00b31af53, ec52cf1ca | yes |
| RT-EXEC | EVIDENCE-HOLDS on F1 and TNN3H5R; UPHOLD BUILD-FAIL (F1); H5R2 ADVANCES stands | 76b9ee229, f8fcac045 | yes |
| TNN3-SUBSTRATE | DESIGN-COMPLETE (adoption is Micah's governance decision) | be112b78f, a11dde4b9, f77b7c7d5, 3b61e5e57 | yes |
| H5R2-REPRO | REPRO-PASS | 8b30769de, 933736747 | yes |
| CONSEQ | VALIDATION-PASS | e068ac9a4, 5cf8df371 | yes |
| CONTLEARN | BUILD-PASS (LEARNOWN-DEMONSTRATED; refined by CONTLEARN-OWNED) | 408ffdcdc, dfcd3caf1, 719829def | yes |
| TNN3H5R | BUILD-PASS (H5R2 ADVANCES) | dc7df4aba, 9db334bd4, e20ba5402, 7e4d7cffe | yes |
| ARENA | BUILD-PASS (C8 inquiry) | 1156add31, 0ddb5e9ce, 0218296e0, b9245751d, 33cc2bff6 | yes |
| F1 | BUILD-FAIL | 50de69403, ba5ebbf8b, 3b159b401, 14fdf441d, 79e11a6d1 | yes |
| RT-INT | EVIDENCE-HOLDS on CONSEQ and CONTLEARN | f70c676f4, 6c8485fdc, f99a56174 | no |
| RT-GOV | HOLDS on all three axes, one QUALIFY | 7a1ebe002, 84c8fd0df | no |
| ARENA2 | BUILD-PASS (C12 transfer by recoding) | 5a055b575, 18309290c, 3b25013b1 | yes |
| ARENA3 | BUILD-PASS (C12 transfer by relabeling) | 829208f99, 9191e71de, d51d8ef5b, 33d4e2e19 | yes |
| F1-FOLLOWUP | Part 1 BUILD-PASS, Part 2 NOT-FOUND | 001fcfaca, 6dee24671, 34960a9bc, 63922a500, 27116eb12, 728e114f2, 36743190e | yes |
| C174 | VALIDATION-PASS | 134af1cb2, b5e0274f7, 0096b30ca, 3028240e4, 88e92c016 | yes |
| BATTERY | Part 1 VALIDATED, Part 2 1/6 PASS | f7f8f5e3b, a42a113aa, 59e029102, e7a1d4217, 562ca5b8f, 57f1cfa85 | yes |
| DEVANG3 | BUILD-PASS | 5b7e55706, 126ef2600, ead6f006c, 11026f43b, a29d4088c, e0135d993 | yes |
| RT-C174 | EVIDENCE-HOLDS | 89b27a9ce, 7d20a7a3d | no |
| RT-HPIREV2 | Part 1 QUALIFY, Part 2 PARTIALLY survives | 8b86b27d2, 1c40232af, 5f53f1c7a, 1eb89eadf | yes |
| BATTERY-CLUSTER | COMPLETE | 55ee13a1c, 335b169ae, 357821930 | yes |
| H5R2-BASELINE | BASELINE-MATCHES via (a) REVERT-TO-LATEST | 28cbe5877, 1203b865d, 6a7c73816, fc2f910e5, 8c3292bb6 | yes |
| C9BAT | GEN-PASS | fd3d23c3a, 9e2ea47fc, 4dc4a6d02, c2448aa0b, 3e66b3409, 33fff11e2 | yes |
| RT-SENSE | QUALIFY (DEVANG3 BUILD-PASS stands) | 6ea7f42f9, fc36c4444 | no |
| F1-BUFFER | BUFFER-NOT-PREDICTIVE | 451823613, ffb8e885a | yes |
| ARENA4 | BUILD-PASS (C15 ROSTER) | 19d9edc87, 171c45101, f8d7b9b2e, a5d7a6ef7 | yes |
| BATTERY-E2 | E2-CONTENT-BLIND | 229cf5263, 4900c177d, 6c9d96cef, 524eca821, 5b2775e46 | yes |
| H7R | BUILD-PASS | 144deb24a, 11eb54f6f, f1cd443fa, 6b8dedf28 | yes |
| BATTERY-E1 | E1-FIRSTCLASS | 793abbf65, aa38427b8, 4afcd9f3b, f5b1bab41, 1bea7a7ca | yes |
| H5R2-DECOY | DECOY-DISCRIMINATES | 51a4fe8e1, 4511f5c64, 12d69043f, 2a4c0ff3f, d0b2ffece | yes |
| F1-REPAIR | GREEDY-CONFIRMED | b4afb6236, fadaee3fb, 5935c5169, 4c253fb36, 25712d767 | yes |
| BATTERY-E3 | E3-ORACLE-DEPENDENT | a17a276c8, ce46b327a, 4f49f8b66, f14f1470d, c7f677480 | yes |
| F2V3 | BUILD-PASS | 5e4e56a5f, b5fcf9ae3, 30a1ff7e0, d0846df90 | yes |
| BATTERY-E6 | E6-CONTENT-READ, with H2C-STICKY | 58811f3a5, fbe5ab33e, 486c13c5c, a95e8b05b | yes |
| H6R | BUILD-FAIL | a0283287b, 5b46e84e2, d8d73d3ec | yes |
| BATTERY-E4 | E4-PRECEDENCE | 5a2c7c91c, f26ddb294, 67680ebb1, 61df738fe | yes |
| ARENA5 | BUILD-PASS (DEFRECALL) | b63f80289, f3320caf8, 2320c3454, 6582398e9 | yes |
| F1-REPAIR2 | REPAIR2-CONFIRMED | b4dfa3f32, 6bc6483c3, fed95fc76, 466bcee03, ceac93953 | yes |
| BATTERY-E5 | E5-INSTANCE-ONLY | 282c8301e, c8d9f14e1, 8510feee6 | yes |
| ARENA-BLIND | ORACLE-FREE (ARENA4 BUILD-PASS stands) | 0b95a6601, c2eb08c2a | yes |
| H5R2-SKEPTIC2 | SKEPTIC-SURVIVES | 709e1e82e, f461e812d, bbbc333d6, c714f3394 | yes |
| BATTERY-E8 | E8-BANDWIDTH | 034ecbd35, eb854c45d, c7c70b934, 0d6fdaaf6 | yes |
| RT-ARENA5 | QUALIFY (BUILD-PASS stands) | e14e7e387 | no |
| CONTLEARN-OWNED | MACHINERY-DEPENDENT | 3e837ff5c, d2fc968f4, a74b0d2d3 | yes |
| ARENA-GEN | NARROW | ef30ef8d1, 81fccb857, 32cffcd36 | yes |
| CONTLEARN-OWNED2 | MACHINERY-DEPENDENT | ffd31dbb3, 78d8c9e54, 6147c2c4c | yes |
| H5R2-SKEPTIC3 | SEPARATED | 6bf257048, 2affa9bcd, cb36a9978, 69f91f459, f54465adb | yes |
| H2R | BUILD-PASS | 5a3e815c5, e60f1a936, 9bd208eee | yes |
| RT-ARENA4 | EVIDENCE-HOLDS (ARENA4 BUILD-PASS stands) | 5455d3753 | no |

## Verification and synthesis lanes (verdicts on lane claims, not frozen bars)

| Lane | Verdict | Key commits | JUDGE_BRIEF.md |
|---|---|---|---|
| ARENA-GEN-VERIFY | VERIFIED (ARENA-GEN NARROW holds) | d4fde40a6 | no |
| MECH-VERIFY | CONFIRMED x3 (call-site inventory, mp_set/mp_get, event entry points) | cb36a9978, f54465adb | no |
| LEARNER-MECH | analysis only, no verdict (consumes CONTLEARN-OWNED MACHINERY-DEPENDENT) | 338fc4087 | yes |
| ARENA-SYNTH | synthesis of ARENA4/ARENA5/ARENA-BLIND (no new verdict) | 38c55b44c | no |
| CLUSTER-SYNTHESIS | synthesis of post-freeze battery cluster discriminators (no new verdict) | 79d92d90b, 8955f6881 | yes |
| CLUSTER-FINAL | final synthesis of Cluster 1 + Cluster 2 program (no new verdict) | df6eeaec0 | yes |
| H5R2-SYNTH | synthesis of four gate verdicts (no new verdict) | c0db886b4 | no |
| OWNED-SYNTH | synthesis of five learner-owned verdicts (no new verdict) | 8698ce694 | no |
| DEBATE-PREP | DEBATE_BRIEF.md: 40-verdict slate for the debate group (no verdict of its own) | d315cc0cf, 04760ef48 | yes |

## In-progress lanes (no verdict yet)

| Lane | Status | Key commits | JUDGE_BRIEF.md |
|---|---|---|---|
| SENSORY | H2v1 FSDF candidate rendering (base1/base2 done; h2v1a done; h2v1b rendering); verdict after verifier runs | 58a1a0d7f, 5ca243f10, c7306028f | no |
| RT-F2V3 | red-team review of F2 v4 BUILD-PASS in progress (deep read of prereg/implementation/sealed eval/judge brief) | (uncommitted) | no |
| RT-F2V3-CHECK | PROGRESSING NORMALLY (00:43 PDT check; no anomaly) | c3b62ab4d | no |
| SENSORY-CHECK | PROGRESSING NORMALLY (00:41 PDT check; needs no help) | 6531069cb | no |

## Governance, records, and infrastructure lanes (documentation; no experimental verdict)

| Lane | Content | Key commits | JUDGE_BRIEF.md |
|---|---|---|---|
| WAVE-ARCHIVE | this manifest (archive inventory) | (this lane) | no |
| WAVE_RECORD.md | wave record with 46 verdict bullets (root of the wave dir) | -- | no |
| WAVE-STATUS | WAVE_STATUS.md | 2f086d94e | no |
| WAVE-SUMMARY | WAVE_SUMMARY.md | a24a01955 | no |
| VERDICT-LIST | VERDICT_LIST.md (47 verdicts, 38 listed) | bfd506248 | no |
| QUAL-SUMMARY | QUAL_SUMMARY.md (qualifications, supersessions, narrowings) | 5f26d0174 | no |
| DEBATE | skeleton: ADVOCATE_NAMECHECK.md, SKEPTIC_NAMECHECK.md (debate convenes after lanes land) | 5997f67ab | no |
| DEBATE-PREP2 | NAMECHECK.md only | (uncommitted) | no |
| DEBATE-READY | DEBATE_READINESS.md | cce919ec9 | no |
| DEBATE-SLATE | DEBATE_SLATE.md | cdc53a642 | no |
| DEBATE-WATCH | NAMECHECK.md only | (uncommitted) | no |
| ESCALATION-LIST | ESCALATION_LIST.md (7 decision items for Micah) | 29d7efa32 | no |
| ESCALATION-UPDATE | addendum: frozen artifacts verified byte-identical but not in HEAD (supersedes item 4 framing) | 87298dff5 | no |
| ESCALATION-VERIFY | ESCALATION_VERIFY.md (list verified in HEAD) | 3fa3f5e07 | no |
| EVIDENCE-CHECK | EVIDENCE_CHECK.md | 63ee76321 | no |
| RECORD-CHECK | RECORD_CHECK_REPORT.md | 2ad7a8f19 | no |
| REPORT-CHECK | REPORT_CHECK.md | ed67835c5 | no |
| DRAFT-CHECK | DRAFT_CHECK_REPORT.md | 7c8e4551c | no |
| GAP-DOC | GAP_DOCUMENTATION.md | 335937787 | no |
| QUEUED-CHECK | QUEUED_CHECK.md (queued-next currency) | 4a85f20e1 | no |
| FINAL-CONFIRM | FINAL_CONFIRM.md (checklist) | 41967f2e9 | no |
| FINAL-COUNT | FINAL_COUNT_REPORT.md | a1e74137f | no |
| FINAL-REVIEW | FINAL_REVIEW.md | c1b3e9b17 | no |
| LANE-AUDIT | LANE_AUDIT_REPORT.md plus RESTORED_MANIFEST.tsv / RESTORE_COMMITS.tsv | 84727be29 | no |
| PARENT-PREP | PARENT_REPORT_SECTIONS.md | 15bcb4726 | no |
| REPO-SCOPE | REPO_SCOPE_ASSESSMENT.md: 140,541 untracked files assessed; frozen artifacts verified, restore-vs-leave recommendation | 07dacc055 | no |
| SWARM-HEALTH | SWARM_HEALTH_REPORT.md | 1921e053f | no |
| HEALTH-CHECK | NAMECHECK.md only (new lane) | (uncommitted) | no |
| URGENT-FLAG | NAMECHECK.md only (new lane) | (uncommitted) | no |
| SENSORY-PREP | SENSORY_PREP.md | c96d7baeb | no |
| SENSORY-WATCH | NAMECHECK.md only | (uncommitted) | no |
| LOOPSTATE-DRAFT | LOOPSTATE_DRAFT.md | 7345d8b41 | no |
| LOOPSTATE-FINAL | empty | (uncommitted) | no |

## Known process incidents recorded this wave (for the archive)

- Staging races: several lane commits swept in files staged by concurrent workers (FORK skeleton c5ea959d4; H5R2-BASELINE fc2f910e5; BATTERY-E4 prereg b63f80289 actually ARENA5's; F1-BUFFER 451823613; H5R2-SKEPTIC2 f461e812d with 411 deletions of BATTERY-E4 files, restored byte-identical at c7306028f by LANE-AUDIT; H5R2-SKEPTIC3 cleanup f54465adb removing swept MECH-VERIFY files; RT-ARENA5 e14e7e387 swept into a concurrent commit).
- f461e812d is the staging-race commit that appears in many lane listings above; its scientific content belongs to H5R2-SKEPTIC2.
- The three boundary-overreach repair threads paused 2026-10-01 19:14 UTC left no recoverable state in the repo; recorded as an escalation item for Micah.
- SENSORY NAMECHECK self-disclosed near-miss: a `python3 -c` was typed in a compound command during design and failed to resolve; nothing executed, no artifact touched.
