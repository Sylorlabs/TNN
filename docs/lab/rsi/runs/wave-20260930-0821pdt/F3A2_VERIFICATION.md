# F3A2_VERIFICATION.md

Wave: wave-20260930-0821pdt. Subject: H-PI-REV2 F3a2 (second adversary
byte 'v') evidence vs frozen prereg 97d58e38e and frozen implementation
847a8f10f.

## (a) Commit-order self-check

- Prereg commit 97d58e38e (2026-09-30 12:24:51 UTC, "Prereg:
  H-PI-REV2-F3a2 corrected re-freeze (FROZEN; committed alone)")
  contains exactly two files: docs/lab/rsi/runs/wave-20260930-0521pdt/
  RUN_START_PIN.txt and docs/lab/rsi/runs/wave-20260930-0521pdt/prereg/
  PREREG_PI_REV2_F3a2.md. Confirmed by git show --name-only. PASS.
- Evidence file mtimes: all three EVIDENCE_F3A2_run{1,2,3}.txt at
  2026-09-30 12:27:16 UTC, strictly after the prereg commit
  (12:24:51). PASS.
- No implementation file committed after the prereg: git log
  97d58e38e..HEAD over docs/lab/rsi/runs/wave-20260929-2321pdt/pi_rev2/
  returns zero commits. The implementation blob at 847a8f10f
  (docs/lab/rsi/runs/wave-20260929-2321pdt/pi_rev2/proc_revise2.zag,
  840 lines) is unmodified since the freeze. PASS.
- CAVEAT (strict reading): the implementation commit 847a8f10f
  (2026-09-30 06:32:23 UTC) predates the prereg commit (12:24:51).
  The prereg itself declares this is an evaluation-only re-freeze
  ("Frozen implementation ... NOT modified this wave. This prereg is
  an evaluation freeze only.") under judge authority from the
  wave-20260930-0221pdt debate (motion M5 AMEND: re-freeze F3a with
  corrected K-F3-4 text and a byte from {k,m,r,v}, then re-run). The
  strict standing rule (prereg must strictly precede implementation)
  is therefore not literally met by the re-freeze design; the
  mitigations are the three verified facts above plus the anti-tuning
  audit below. The judge must rule whether the re-freeze authority
  cures the ordering.

## (b) Evidence determinism and trace vs K-F3-1

- cmp: run1/run2/run3 byte-identical (2282 bytes each). PASS.
- All three report "=== RESULT fails=0 ===" and "BUILD-PASS". PASS.
- K-F3-1 trace match, item by item:
  - COUNTEREXAMPLE_DETECTED(vab): present. PASS.
  - DIAGNOSIS pos=0 byte=118 conflicts=0: present. PASS.
  - PRIMITIVE-CONSTRUCTED pos=0 byte=118: present. PASS.
  - alt = index 2 (C0 broadcast-first): the trace carries
    "CHECK P8-F2-alt-C0: PASS", which certifies alt2==2 in the frozen
    binary (check("P8-F2-alt-C0", alt2==2, fails)). Substance PASS;
    the literal text "alt = index 2" is not printed.
  - v4 ACTIVE with parent v3: GAP. The trace shows "VERSION v3
    ACTIVE (parent v2)". The frozen binary's P8 interface runs a
    single adversary phase per execution; v4 is unreachable in this
    binary. The K-F3-1 text describes a cumulative execution the
    frozen implementation cannot produce. Bar-design error in the
    prereg text.
  - "vab"->"vvv": present ("PREDICT vab -> vvv [ok]"). PASS.
  - priors unchanged ("xab"->"xxx", "abc"->"ccc", "xy"->"xx",
    "defg"->"gggg"): all present. PASS.
  - "wab"->"www": GAP. Absent; "wab" belongs to the F3a ('w') run,
    not to this fresh F3a2 execution. Bar-design error (cumulative
    framing).
  - reuse "vqv"->"vvv" with no new revision: PARTIAL. The trace
    shows "PREDICT vqw -> vvv [ok]" and "CHECK
    P8-F2-reuse-no-revision: PASS". The binary constructs the reuse
    probe as adversary-byte + "qw" ("vqw"), not "vqv"; the K-F3-1
    text's "vqv" is a bar-design typo. No new revision occurred.
  - R cell 8/8 after F3a2: substance present, label absent. The 8
    R retention probes (zag, 12, q, hello, ptc, s, eghjjupazbnf, q)
    all report [ok] in the P8 section after the revision; the trace
    never prints the literal "R 8/8".

## (c) K-F3-3 anti-tuning

Grep audit of the committed implementation blob
(847a8f10f:docs/lab/rsi/runs/wave-20260929-2321pdt/pi_rev2/
proc_revise2.zag):
- char literal 'v': 0 occurrences.
- string literals "vab", "vvv", "vqv": 0 each.
- numeric literal 118: 0 occurrences; no 0x76/==118 variants.
- The byte reaches the machinery only through the argv data flow
  (allowed-set membership check against "ijklmnortuvw", f2in/f2out
  construction from adv[0]). PASS.

## (d) K-F3-4 disjointness

- Frozen fixture input strings (all loadseq/pcheck/rcell literals:
  T: abc/cba, def/fed, xy/yx, hello/olleh, abc/abc, xy/xy; F1: abc,
  xy, defg, xab, xqw, hello, ptc, s, q, eghjjupazbnf, 12, zag; R:
  zag, 12, q, hello, ptc, s, eghjjupazbnf, q): zero contain byte
  0x76. PASS.
- Executed F2 adversary fixtures ('i' family): byte 'i', disjoint
  from 'v'. PASS.
- Executed F3a adversary fixtures ("wab", "wqw", "www"): no 0x76.
  PASS.
- The 'v' occurrences in the F2/F3a evidence files (19 each) are all
  trace labels ("v1", "v2", "v3" version identifiers, "discovery",
  "revision", "verification", check names), not fixture inputs.
  The allowed-set gate string "ijklmnortuvw" contains 'v' by design
  (it is the admission whitelist, not a training fixture; 'v' is the
  selected byte). Neither violates the bar, which names fixture
  inputs. PASS.

## Recommendation: BUILD-FAIL on K-F3-1 bar text (mechanism evidence clean)

K-F3-2 PASS, K-F3-3 PASS, K-F3-4 PASS. K-F3-1 as written is not
satisfied: the trace shows v3-parent-v2 where the text demands
v4-parent-v3, vqw where the text demands vqv, and wab->www where no
such prior exists in a fresh execution. These are bar-design errors
in the re-freeze text (cumulative-learner framing applied to a
single-execution frozen binary), not mechanism failures: the white
box did exactly the intended work on the second adversary byte
(detected vab, diagnosed byte 118 from data, constructed the
primitive, revised to a new active version, reused vqw->vvv with no
new revision, 8/8 R retention post-revision, ablation rollback
destroys the new behavior, 3/3 byte-identical, zero tuning).

Under the standing rule (never weaken a frozen kill bar to force a
pass; never count a preregistered threshold as achieved before
frozen execution), the literal K-F3-1 text was not met. This mirrors
the F3a precedent exactly: F3a was killed on K-F3-4 bar text
(bar-design, not mechanism), then re-frozen with corrected text and
re-run. Recommended path: judge kills F3a2 on K-F3-1 bar text,
orders a re-freeze of K-F3-1 with corrected text (v3 ACTIVE parent
v2; vqw reuse probe; drop wab; name the 8 R-probe retention
explicitly), then re-run on the same frozen binary. The (a) ordering
caveat is also for the judge: the re-freeze authority from the
0221pdt debate motion M5 is the claimed cure.

No em-dashes in this documentation.
