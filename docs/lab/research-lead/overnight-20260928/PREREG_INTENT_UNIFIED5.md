# PREREG: H-INTENT-UNIFIED5 Repair (FROZEN)

## Hypothesis

H-INTENT-UNIFIED5 closes both H-INTENT-UNIFIED4 red-team downgrades at the
mechanism level:

- X-IU4-1a: truncated-vs-truncated blind spot. When both intent records are
  truncated (true npairs > 16) and both candidates have em=0 for the query,
  the R4 guard never fires and the decision falls through to score gap,
  silently resolving a genuine training-data contradiction.
- X-IU4-2b: sq(64) fixed buffer. bridge_learn Step 1 allocates
  `sq:[]u8=z_alloc(64)` (16 i32s) while pextract writes out_len i32s;
  a training pair with a >16-char output writes past the buffer and
  panics ("slice index out of bounds", exit 1). The 64-byte per-pair
  seqbase slots carry the same 16-char assumption.

Both repairs are minimal, faithful extensions of existing mechanisms.
Classification target: bounded L2 integration repair. No L3 claimed.

## Frozen kill bars

### K-IU5-1: X-IU4-1a closed (both-truncated guard)

Fixture (exact, from IU4-ADV):

- Proc learn: `abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;qrs>srq;tuv>vut;xab>bax`
  (17 reverse pairs; `xab>bax` is the 17th, unrecorded). Expect direct
  discovery, slot>=0, rc<1000. Record true npairs=17 (truncated).
- Bridge learn: `xcd>xxx;xef>xxx;xgh>xxx;xij>xxx;xkl>xxx;xmn>xxx;xop>xxx;xqr>xxx;qab>baq;wab>baw;eab>bae;rab>bar;tab>bat;yab>bay;uab>bau;iab>bai;xab>xxx`
  (17 pairs; first 16 induce IF input[0]=='x' THEN const-0 ELSE reverse;
  `xab>xxx` is the 17th, unrecorded). Expect rc>=1000. Record true
  npairs=17 (truncated).
- Query: `xab`. Direct application confirms genuine disagreement:
  proc_answer=`bax`, bridge_answer=`xxx`.

Two learn orders, each on a fresh W:

- Order A (proc-first): proc learn, then bridge learn, then query.
- Order B (bridge-first): bridge learn, then proc learn, then query.

PASS iff in BOTH orders: kind=-2 AND the diagnostic line reads
`INTENT TRUNCATED-CONFLICT-POSSIBLE: both records truncated with different answers; WITHHOLD AMBIGUOUS`.

FAIL: any other kind in either order, the verbatim-vs-truncated
diagnostic text, or a silent resolution (kind>=0 with an answer).

### K-IU5-2: X-IU4-2b closed (16-char extraction cap)

Fixture (exact, from IU4-ADV):

- Learn: `abcdefghijklmnopqrst>tsrqponmlkjihgfedcba;ABCDEFGHIJKLMNOPQRST>TSRQPONMLKJIHGFEDCBA`
  (two 20-char reverse pairs; each output char appears exactly once in
  its input, so pextract would return out_len=20 rather than -1).
  Routes PROC_LEARN.

PASS iff: process exits 0 (no panic), the honest-cap diagnostic
`exceeds 16-char extraction capacity` appears (once per excluded pair),
and the learn outcome is the honest `ULEARN FAIL: no program and no bridge`
(rc=-1).

FAIL: panic, non-zero exit, silent acceptance (rc>=0), or missing
diagnostic.

### K-IU5-3: no regression (all K-IU4-1..K-IU4-4 still PASS)

- K-IU4-1: proc 17-pair `abc>cba;...;tuv>vut;xab>bax` + bridge
  `xab>xxx;xcd>xxx;abc>ccc;def>fff;abcde>eeeee`; query `xab` -> kind=-2
  with the UNCHANGED diagnostic
  `INTENT TRUNCATED-CONFLICT-POSSIBLE: verbatim candidate meets truncated record with different answer; WITHHOLD AMBIGUOUS`.
  The verbatim-vs-truncated branch must keep precedence (it requires
  em=1 on one side; the new branch requires em=0 on both).
- K-IU4-2: 129-pair build_big_line fixture -> rc=-1,
  `bridge: WORK area too small for npairs=129; need 9288 bytes; honest failure`,
  exit 0, no panic. The WORK guard precedes Step 1 and is unaffected by R7.
- K-IU4-3: unified_learn.zag main() -> 20/20, output byte-identical to
  frozen IU4 evidence (md5 904de9f83a2873c7a8862b71804a9065).
  intent_learn.zag main() -> 10/10, output byte-identical to frozen IU4
  evidence (md5 98315faec8faea24e75533892c0b240d).
- K-IU4-4: determinism (covered by K-IU5-4).

### K-IU5-4: determinism

iu5_verify binary run 3 times -> byte-identical output.
unified_learn.zag main() run 3 times -> byte-identical.
intent_learn.zag main() run 3 times -> byte-identical.

## Frozen repair specifications

### R6: both-truncated guard (X-IU4-1a)

In `intent_winner`, in the truncated-conflict guard block, extend the
`check` computation:

- Keep: `if(em_top==1 && em_second==0 && trunc_second==1){check=1;}`
- Keep: `if(em_second==1 && em_top==0 && trunc_top==1){check=1;}`
- Add: `if(em_top==0 && em_second==0 && trunc_top==1 && trunc_second==1){check=1; both_trunc=1;}`

On answer disagreement (kind-dispatched proc_apply/bridge_apply, byte
comparison over qlen, same as the existing guard): if both_trunc==1,
emit `INTENT TRUNCATED-CONFLICT-POSSIBLE: both records truncated with different answers; WITHHOLD AMBIGUOUS`;
else emit the existing verbatim-vs-truncated diagnostic text unchanged.
Then `set32(res,0,-2); set32(res,4,-1); return;`.

On answer agreement, fall through to existing rules (no over-broad
withholding). Guard precedence is structural: the verbatim guard needs
em=1 on both sides; the verbatim-vs-truncated branches need em=1 on one
side; the both-truncated branch needs em=0 on both sides. The three are
mutually exclusive by construction.

### R7: 16-char extraction cap (X-IU4-2b)

In `bridge_learn` Step 1, before `pextract`:

- If out_len > 16: emit `bridge: pair <i> output length <out_len> exceeds 16-char extraction capacity; excluded (honest cap)`,
  `set32(W, statbase+i*4, 0)`, `allok=0`, and skip extraction for that pair.
- Else: run the existing extraction path unchanged.

This bounds every `sq` write and every seqbase-slot write to at most 16
i32s by construction (sl <= out_len <= 16). Per-pair exclusion mirrors
the existing pextract-failure path exactly (stat=0, allok=0, continue);
if no extractable pair remains, Step 3 finds no split and the function
returns -1 through the existing honest-failure path.

R6 and R7 are applied IDENTICALLY in `unified_learn.zag` and
`intent_learn.zag`. Faithfulness invariant (frozen): all 8 intent
functions (intent_record_inputs, intent_record_proc, intent_record_br,
intent_exact_match, intent_qscore, intent_winner, intent_trace_emit,
intent_init) remain byte-identical between the two files, verified by
per-function extraction and cmp. The bridge_learn Step 1 change is
present in both files.

## Frozen methodology

1. This prereg committed alone before any implementation edit, build,
   or run. Commit order verified by `git merge-base --is-ancestor`.
2. Implementation: identical R6/R7 edits in both .zag files.
3. Harness: iu5_verify.zag = mechanism region of the NEW
   unified_learn.zag (everything before `fn main`), cmp-verified
   byte-identical; only main() replaced with the K-IU5-1..K-IU5-3
   kill-bar tests above.
4. Raw evidence: IU5_VERIFY_RAW.txt (md5 recorded, 3/3 byte-identical),
   plus fresh 20/20 and 10/10 suite outputs with md5s.
5. Pure Zag throughout: prereg, implementation, harness, builds, runs,
   greps, md5, cmp. No Python at any stage.
6. Toolchain: znc 2026.07.0-dev (edition 2026), pinned.
7. Only researcher-owned paths staged. No em dashes in loop docs.

## Falsification criteria

- K-IU5-1 yields kind != -2 in either order -> R6 insufficient -> KILLED.
- K-IU5-2 panics or exits non-zero -> R7 insufficient -> KILLED.
- Any K-IU4 bar breaks -> regression -> KILLED (the bar stands; the
  repair is narrowed, never the bar).
- 20/20 or 10/10 md5 differs from the frozen hashes -> silent behavior
  change -> KILLED.

## Boundaries (frozen, disclosed)

- The both-truncated guard carries the same precision cost as R4: two
  truncated records whose procedures merely generalize differently
  will withhold with an honest "POSSIBLE" diagnostic even when the
  unrecorded training pairs do not contradict. The diagnostic says
  POSSIBLE, not CERTAIN. This is disclosed, not a bug.
- The 16-char extraction cap is a loud per-pair exclusion. Outputs
  longer than 16 chars can never participate in extraction; this is a
  documented mechanism capacity, not a silent limit. Enlarging the seq
  representation is future work, not this repair.
- The guard only considers the top two ranked candidates, as before.
  Conflicts involving lower-ranked candidates are out of scope.
- Classification: bounded L2 integration repair. Not L3.
