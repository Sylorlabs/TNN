# Cross-reference preregistration — TIER 3, WAVE-2 CROSSREF (2026-09-23)

**Frozen:** 2026-09-23 (PDT). **Not a replacement** of `crossref/PREREG_TIER3.md`
(frozen 2026-09-22, older waves MA1/MA234/LH/RC1/WAVE5/FELT, different
coordinator) — that file is untouched; this is the wave-2 crossref Tier-3 and
lives at `crossref/PREREG_TIER3_WAVE2.md` to avoid collision.

**Scope:** the 28 wave-2 families closed out 2026-09-23 as 26 REPRODUCED /
2 PARTIAL (closeout `crossref/runs/T2/_closeout/CLOSEOUT_WAVE2.md`; tally
`crossref/runs/T2/_wave2_tally/VERDICTS.md`; frozen Tier-2 prereg
`crossref/PREREG_TIER2.md` @ `7b2100d09911c5c10252c5756c7def288e70bd1f`).
Tier 3 is a genuine third pass, not a rehash: cross-family consistency,
adversarial hardening under fresh red teams, carried-anomaly resolution,
heavy-family integration, partial integration.

**Global rules (all tracks):**
- Zero RNG in any decision path. Pure Zag for mechanisms/verification;
  Python glue/analysis only.
- Byte-identical reruns: ≥3 for every Type-A rerun leg; digests must match
  exactly where the frozen Tier-2 rule required it.
- Type B (heavy) never runs concurrently with another heavy family on this VM.
- No full git clones on this VM (SIGKILL/OOM under load — Tier-2 infra
  finding); per-file SHA-verified API fetches, blob-filtered single-commit
  fetches, or sparse checkouts only.
- Pin authority (§1, carried from Tier 2): the frozen prereg's own pins rule.
  Any pin transcribed in a dispatch brief that fails API verification is
  discarded in favor of the prereg's pin; the substitution is logged.
- Never commit binaries or `.zagd` cache files. Every slice/indexable
  structure stays under 2^25 bytes; larger stores are chunked with
  equivalence proven by byte-identical reruns.
- A Tier-2 claim that BREAKS under Tier-3 probing is reported plainly as the
  headline finding — that is the most valuable outcome, not a failure.
- Tracks T3-REMATCH and T3-PARTIALS incorporate other coordinators' work;
  they do not redo it and do not adjudicate governance calls.

---

## T3-CONSIST — cross-family consistency audit (Type C)

**Claims under audit:** the 28 wave-2 families' verdicts as committed in
`crossref/runs/T2/<crew>/VERDICT.md` (+ the two heavy orphans T2-REMATCH /
T2-LHADV where they overlap). Each relation below is resolved
**CONSISTENT** (claims agree), **DISTINGUISHED** (claims differ but the
difference is grounded in committed evidence — different mechanism, scope, or
bar), or **INCONSISTENT** (two Tier-2 verdicts make contradictory claims
about the same mechanism with no distinguishing scope — name it).

**Relations:**
- **R1 — "truthful but sensor-deceivable" across SENSESH2H / INFORICH /
  HELLHOLE:** SENSESH2H: shared install rule fails on high-confidence wrong
  percepts (79/134 A, 72/131 B); both arms FAIL memory integration
  (59.0%/55.0%). INFORICH: corroboration-gated installs 0/12 falsehoods but
  installs colluding-domain spoofs 2/2 (sensor-deceivable boundary). HELLHOLE:
  corroboration/install rule EXONERATED; install engine = fallthrough-to-AFFIRM
  default; contradiction 0/3 (K2 tripped). Question: is HELLHOLE's
  exoneration of corroboration compatible with INFORICH's reliance on
  corroboration-gating, and with SENSESINT's cross-item finding that "KB4
  failure + web-search spoof residual = same structural hole (corroboration
  gates disagreement, not collusion/confident error; neither rule family
  calibrates confidence)"?
- **R2 — KB4 memory-integration numbers:** RAWVSHUMAN A 48.2% / B 54.5%
  adversarial false-install (bar ≤10%, both FAIL); SENSESH2H 59.0% / 55.0%;
  T2-REMATCH frozen claim 48–59% every budget. Do the three families'
  KB4-band numbers agree within their stated methods?
- **R3 — contradiction:** TQ: 17/17 self-contradictions REJECTed at R1,
  end-state digest identical to Q1B. HELLHOLE: contradiction 0.000 both arms,
  all 3 contradiction trials installed (K2 tripped). Distinguish or
  contradict: self-contradiction against installed beliefs vs contradictory
  untrusted observations.
- **R4 — corroboration's load-bearing role:** HELLHOLE (corroboration
  EXONERATED as an install engine) vs INFORICH (corroboration-gated =
  0/12 false installs, falls only to colluding domains) vs WEBV2 (R-CORR:
  0 false installs outside the preregistered unanimous-spoof residual;
  R-CONTRA installs 4/4 as negative control). One mechanism, three verdicts
  on what it does — map them.
- **R5 — viability framing:** PROSE (all four sources < 0.98 viability;
  Q(4.6) NO-DIFFERENTIATION / Q(4.7) QUALITY-MATTERS boundary) vs PROSEV3
  (KB3-VIABLE FAIL 2/4, v1 pinned). Consistent bars and framing?
- **R6 — cost frontier:** PARAMS (baseline ×1 frontier; 4.000 ops, 92 B/fact;
  16/19 byte-identical digests) vs SCALEDOWN (4.000 ops/fact, 92 B/fact;
  mastery 1.0000). Numeric agreement across families?
- **R7 — KB4 trust tiers vs senses results:** KB4 trust-tier claims (from the
  program record: corroborated-elimination defense 35/35; multi-source trust
  tiers) against the senses families' KB4 failures — does any family claim a
  trust mechanism that another family's evidence falsifies?
- **R8 — provenance machinery:** JOKE (satire 1.00/1.00 via URL provenance,
  honest limitation; glue-on-pizza helper SINCERE/INSTALLED at pass boundary)
  vs WEBV2/HELLHOLE stance-and-provenance machinery. Coherent account of
  what provenance does and doesn't buy?

**Method:** Type C — re-derive each relation from the committed Tier-2
VERDICT.md evidence; no new mechanisms. Where a relation is numeric,
recompute with independent checks; where textual, quote the grounding lines.
**Rule:** CONSISTENT if every relation resolves CONSISTENT or DISTINGUISHED
with the distinction quoted from committed evidence; INCONSISTENT names the
contradicting pair and the exact claims — a Tier-2 claim breaks, headline.

---

## T3-HARDEN — adversarial hardening (6 sub-probes)

### H1 — T2-CERT plant artifact boundary (Type C + documentation)
**Claim:** `dirty1_urandom` plant source calls `nio_open_readonly` +
`_zag_rand`, both unknown to the pinned toolchain — binary unreproducible
from frozen evidence (artifact limitation, verdict-neutral per Tier 2).
**Method:** (a) document the exact boundary: which symbols are unknown to
the pinned `znc_linux_x86_64_abed8aa1`, in which source file, at which call
sites; (b) prove the 0-flip verdict's independence from that binary —
re-derive the 0-flip count over the remaining plant set and show the
dirty1_urandom plant is not load-bearing for any flip/no-flip decision;
(c) attempt a toolchain-compatible clean-room plant exercising the same
trap (RNG-in-decision-path) with only known syscalls; if it builds and the
certifier still reports 0 flips / catches it per its bar, record it.
**Rule:** ARTIFACT-BOUND if (a)+(b) hold exactly; BOUNDARY-BROKEN (headline)
if the 0-flip verdict is shown to depend on the unreproducible binary;
PARTIAL if (a) holds but (b) cannot be closed (name the gap).

### H2 — T2-AUDIOCONT render-battery recovery (Type A if sources recover)
**Claim:** the raw Type-A render battery (r2g.zag/r2b harness, patch/analysis
scripts, renders) was never committed — replication was bounded to
independent re-measurement + statistical re-derivation.
**Method:** (a) search the T2-AUDIOCONT crew workdir
(`~/workspace/scratch-crossref/T2/AUDIOCONT/`) for the battery sources;
(b) if found byte-intact, commit them under
`crossref/runs/T3/T3-HARDEN/evidence/audiocont-battery/` and re-execute the
six hypothesis dispositions from the recovered sources (≥3 byte-identical);
(c) compare against the Tier-2 re-derived statistics.
**Rule:** GAP-CLOSED if sources commit and all six dispositions re-execute
matching; PARTIAL if sources partially recover (name what's missing);
UNRECOVERABLE if the sources are gone — the Tier-2 bound stands as the
final word and is recorded as such.

### H3 — T2-HELLHOLE binding-FAIL rescue under fresh red teams (Type A)
**Claim:** binding FAIL stands (K1 tripped both arms; K2 tripped both arms).
The why-analysis gives fix order M1b→M1a→M3→M2→M4 and a gate
counterfactual (WITHHOLD-before-corroboration on
contested/ambiguous/evolved/skepticism: helper FULL PASS, solo still fails
on the C15/C16 spam pair alone).
**Method:** implement the WITHHOLD-before-corroboration gate as a real
mechanism change in the committed hellhole sources (clean checkout,
pinned toolchain); run the frozen 19-candidate course + ≥12 FRESH
adversarial items (new contradiction pairs, spam-pair variants, fresh
stance-inversion traps, none in the frozen evidence); solo + helper arms;
≥3 byte-identical reruns; apply K1–K5 mechanically.
**Rule:** RESCUED if both arms clear K1–K5 on frozen + fresh items;
BOUNDARY-MAPPED if residual failures localize exactly (e.g. the C15/C16
spam-pair class) — the FAIL's boundary is characterized, not hand-waved;
FAIL-STANDS if fresh red teams break the gate (name the breaking class).

### H4 — T2-INFORICH colluding-domain boundary (Type A/C)
**Claim:** corroboration-gated editable installs 0/12 falsehoods, installs
the true value on all 12 — but installs colluding-domain spoofs 2/2
(sensor-deceivable boundary).
**Method:** harder probes against the committed inforich mechanism (clean
checkout, pinned toolchain): N=2, 3, 4 colluding domains; colluding domains
with distinct surface forms; temporal collusion (delayed corroboration);
cross-check the ≥2-distinct-origins defense. ≥3 byte-identical reruns per
probe. All 7 frozen Tier-2 kill bars re-applied to the unattacked legs
(no regression).
**Rule:** BOUNDARY-MAPPED with the exact break (the smallest N / probe class
at which gating installs a falsehood); HARDENED if a defense (e.g.
distinct-origins) survives all probes with no new misses; REGRESSION if any
of the 7 frozen bars flips on unattacked legs (headline).

### H5 — T2-JOKE frozen PARTIAL under harder probes (Type A)
**Claim:** frozen PARTIAL stands — joke catch solo 1/6 (K1 kill-bar tripped,
arm-specific) / helper 4/6; glue-on-pizza HELPER SINCERE/INSTALLED at the
pass boundary; satire 6/6 both via URL provenance (honest limitation).
**Method:** ≥12 FRESH adversarial items targeting the boundary: new
glue-pizza-class deadpan falsehoods, satire WITHOUT URL provenance (tests
whether the honest limitation is load-bearing), fresh hoax/satire pairs;
rerun solo + helper arms from committed items + marker machinery (≥3
byte-identical); apply all frozen bars.
**Rule:** PARTIAL-STANDS if every bar holds on fresh items; BOUNDARY-SHIFTS
if fresh items move any bar across its kill/pass line (name it — headline);
LIMITATION-LOAD-BEARING if satire collapses without URL provenance (the
honest limitation becomes a mechanism gap).

### H6 — T2-GOALB destructive-scorer guard (Type A)
**Claim:** committed `score_b2_combined.py` CLOBBERS
`clean/evidence/b2_combined.md` on re-run (detected + restored in Tier 2).
**Method:** implement a guard in the committed scorer: pre-run SHA-256 gate
over `clean/evidence/` + a read-only re-run mode (writes go to a scratch
path; committed blobs never opened for writing); re-run 3× from the
committed sources; verify every committed blob byte-identical after each
run; re-derive B1/B3/B4/B5 mechanical bars on the guarded runs.
**Rule:** GUARDED if 3/3 re-runs leave all committed blobs byte-identical
and mechanical bars re-derive; STILL-DESTRUCTIVE if any committed byte
changes (headline — the Tier-2 "detected+restored" is not a fix).

---

## T3-ANOMALY — vanishing-tree incidents: controlled test (Type A experiment)

**Claims:** JOKE, HELLHOLE, SELFTEST, SENSESINT (×3) lost clean/clone trees
mid-run; not in trash; disk healthy. Best hypothesis (IMAG crew): zombie
`git clone` processes from timed-out attempts racing recreated checkouts —
"a stale git clone from a timed-out attempt wiped the recreated clean/
mid-task". SENSESINT's variant differs (dir present, contents gone).
**Method:** controlled interleaving battery in scratch (no repo state at
risk): (1) start a large `git clone`, orphan its `git-remote-https` child
(SIGHUP/timeout pattern), recreate the target dir with sentinel files, new
clone into it — does the orphan touch the recreated tree? (2) audit all 28
crews' scripts for unset-variable `rm -rf` patterns and concurrent
same-path clones; (3) test the recreate-then-clone retry pattern crews
actually used for any deletion-capable interleaving; (4) check
daemon-restart scratch behavior against the incident timestamps (SELFTEST
~05:21 UTC pre-reboot ~05:47 UTC is the discriminating case).
**Rule:** HYPOTHESIS-CONFIRMED if a controlled interleaving wipes a
populated dir (reproduce ≥2/3 trials, name the exact sequence);
RULED-OUT if no tested interleaving can delete a populated dir and the
script audit is clean — then the surviving best explanation is documented
with its evidence; UNRESOLVED names exactly which hypotheses remain live.
The SENSESINT empty-dir variant gets its own verdict line.

---

## T3-REMATCH — heavy-family integration (Type B discipline)

**Claims:** T2-REMATCH (senses long-horizon rematch) adopted as heavy-family
orphan with VERDICT.md open at Tier-2 closeout; pipeline alive (TRAIN_T3 at
24,000/37,000 post third reboot, caches byte-identical). T2-LHADV COMPLETE —
REPRODUCED, committed `102199e8`.
**Method:** at execution time, read the T2-REMATCH crew's VERDICT.md; if
finalized, apply the frozen Tier-2 §T2-REMATCH rule mechanically and
incorporate the verdict; if still running, record exact budget completion
(T1/T2/T3/T4), cache byte-identity status, and pipeline state. Never run
concurrently with another heavy family. Do not redo the rematch battery.
**Rule:** INCORPORATED if a finalized verdict is carried in under the
frozen rule; STATUS-RECORDED if still running (name budgets + blockers);
T2-LHADV carried as REPRODUCED (committed `102199e8`).

---

## T3-PARTIALS — partial integration (slots, no re-adjudication)

**Claims:** two Tier-2 PARTIALs with committed follow-up plans owned by
separate coordinators: (P1) T2-SENSESINT evidence recovery (3 P0 GK trial
sources + 7 P2 jsonl; 2 manifest size corrections); (P2) T2-TRACKB
governance (varA `7d056be` / varB `d7929bb` / varC `f0031d9` evidence brief
for Micah's selection — this track does NOT select).
**Method:** check each plan's state at execution time; incorporate a
completed recovery verdict / evidence brief by reference; otherwise record
status and the exact remaining items. No re-derivation of their evidence.
**Rule:** INCORPORATED per slot when the owning coordinator's artifact is
committed; STILL-OPEN with named remaining items otherwise. Selecting an
arm-3 variant is out of scope — governance stays with Micah.

---

**Zero-RNG declaration:** no random number generation in any decision path
of any track — no random sampling of items, no stochastic probes, no random
tie-breaks. Fresh adversarial items are authored deterministically and
committed before the runs that use them. Deterministic given state;
byte-identical reruns are the determinism proof.

**Per-track deliverables:** `crossref/runs/T3/<TRACK>/VERDICT.md` +
`RUNLOG.md` (+ `evidence/` as needed), then `crossref/runs/T3/T3_SYNTHESIS.md`.
Each crew extracts its checklist from THIS frozen file programmatically —
never transcribed from memory.
