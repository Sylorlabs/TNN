# Pending battery (frozen S8 protocols)

Authored blind: from PREREG_PENDING.md (commit
22695f27b8132bab69ed3d753c4cee81b1b7a3d8) SS7-S8 only. The pending
implementation was not read during authoring. The KB fixture format was
mirrored from
knowledge/web_guides/live_ingest/knowledge/battery/ (format only).

## Manifest

| class  | cases | dirs                                              | kill bar              |
|--------|-------|---------------------------------------------------|-----------------------|
| HON    | 8     | hon/hon-01..hon-08                                | P3: 8/8 promote       |
| REFUTE | 4     | ref/ref-01..ref-04                                | P3: 4/4 demote        |
| TESTC  | 4     | tst/tst-01..tst-04                                | P4: provenance        |
| RECALL | 24    | rec/rec-01..rec-24                                | P1: 0/24 installed    |
| LAUND  | 18    | lau/lau-a-01..05, lau-b-01..05, lau-c-01..04,      | P2: 0/18 succeed      |
|        |       | lau-d-01..lau-d-04                                |                       |
| CAP    | fill  | cap/ + gen_cap.py                                 | P5: capacity          |

58 functional cases + CAP fill. Each case runs twice (P6: byte-identical
passes, fully deterministic).

## Page format

Mirrors the KB fixtures plus the frozen `HOST:` line (S4c, S8): a `TITLE:`
line, a `HOST:` line, one claim sentence, two generic filler sentences.
Per case dir: `hosts.txt` (one `stem|host` line per page), `kind.txt`
(`FACT`), `need.txt` (the probe question, or the attack description for
LAUND). `claim.txt` holds the canonical claim line used for `kbpend` input
(p1's sentence is byte-identical to it). All hosts are fictional `.example`
domains.

## Authoring decisions (frozen-spec precedence)

1. CAP claim text carries no `|` prefix. Prereg S8 sketches
   `CAP|<i>|The marker stone <i> stands <i> meters tall.`, but the frozen S3
   claim-text field rule forbids `|` in claim text and the parse gate
   rejects such lines. Committed text: `The marker stone <i> stands <i>
   meters tall.` (digits exact, parse-gate clean).
2. DELIBERATE provenance records no host, so S5a step 4 (host independence)
   is vacuous for `kbpend`-held claims. The honest HON corroborations rely
   on this reading; lau-b-05 and lau-c exercise the HELD-provenance clause
   where hosts are recorded.
3. `kbpend` accepts near-duplicates of pending claims: S4a rejects
   DUPLICATE-KNOWN only against committed knowledge.txt, never against the
   pending partition. The lau-a/b attacks depend on this -- the plant step is
   legal, and guard 5 is what refuses the laundering. Tested as written.
4. RECALL probes run while the HON claims are pending (see
   ground_truth_rec.md): after promotion the paraphrases would legitimately
   bind installed knowledge.
5. Bind math used in ground truth: AGREE-bind = token overlap >= 2/3 under
   both min- and max-normalization AND equal digit multisets;
   CONTRADICT-bind = overlap >= 2/3, >= 1 digit, digit multisets differ.
   Checked by verify_battery.py (approximation documented there).
6. The S6 RESOLVE template for test-FAIL is followed literally: kind
   `CONTRADICTED` with the proto-id carried in the detail; the REJ reason is
   exactly `TEST-FAILED:<proto-id>`.

## Battery tools (committed)

- `gen_cap.py` -- frozen CAP generator (seed-free; count derived from
  /proc/meminfo; `--count` override; loud failure without meminfo).
- `verify_battery.py` -- authoring-time self-consistency checker: page
  format, host rules, bind math, digit preservation, the proto registry,
  and the check programs' exit codes. Exit 0 = all pass.
- `testproto.txt` -- frozen test-protocol registry (4 protos).
- `tst/checks/` -- the 4 deterministic check programs; per-case
  `fixture_input.txt` files are the committed fixtures.

## Run-sequencing notes for the driver

- HON: fresh state; kbpend the 8 claims; kbcorroborate each seq with p2.
- REFUTE: fresh state (or continued seqs); kbpend the 4 claims; kbrefute
  each seq with its p3.
- TESTC: fresh state; kbpend the 4 claims; run the check programs; kbtest
  each seq with the observed PASS/FAIL and its proto-id.
- RECALL: state with the 8 HON claims pending (before HON corroboration).
- LAUND: each case self-contained on a fresh state; follow the per-case
  setup in ground_truth_lau.md exactly.
- CAP: fresh state; `python3 gen_cap.py --out cap_claims.txt`; kbpend;
  assert P5; rerun for P6 (pin --count for the two passes).
