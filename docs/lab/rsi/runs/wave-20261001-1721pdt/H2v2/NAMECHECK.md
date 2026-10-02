# NAMECHECK: H2-v2 (generation 2) Phase-2 worker (implementation + execution), wave-20261001-1721pdt

Lane: docs/lab/rsi/runs/wave-20261001-1721pdt/H2v2/
Role: Phase 2 implementation and execution. Prereg is frozen (17d14d896); treated as immutable.

## Step 0: Toolchain guard (mandatory, executed before any other work)

1. Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   Output (tail):
   ```
   safebin: /home/hatch/safebin
   linked: 36 tools
   znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
   verify: python3 absent from safebin PATH (OK)
   verify: python absent from safebin PATH (OK)
   SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
   ```
2. Exported PATH="$HOME/safebin" for every subsequent exec invocation.
3. `which python3` returned nothing. `which python` returned nothing.
   Confirmed absent.

Guard status: ACTIVE. No forbidden executable will be invoked. Pure Zag
plus safebin coreutils only. A forbidden-executable invocation would make
this wave PROCESS-FAIL; none occurred.

## Role note

Phase 1 was prereg writing only (subagent, before this lane). This lane is
Phase 2: world building (two independent adversary passes), sealing,
evaluation against the frozen TNN-2 binary, scoring, RESULT record. No
git commit, no git push, no .wave_lock changes, per the Phase-2 task.

## Step 0 addendum (near-miss, no violation)

During Pass B setup the worker typed a `python3 -c` token inside a
compound shell command out of habit. With the safebin PATH active,
`python3` does not resolve (`which python3` exit 1; no python entry
in ~/safebin), so bash never executed any interpreter: the token
failed at command resolution and no Python code ran. Verified above.
No forbidden executable was invoked; the guard stands ACTIVE. The
worker will not type bare interpreter names again.

## Step 1: Context recovered before work

## Step 2: Phase-2 work record (implementation + execution)

**Frozen subject verified before any run:**
- Frozen TNN-2 source sha256
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  (matches frozen record).
- Frozen TNN-2 binary sha256
  `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b`
  (matches frozen record).
- Cognition prefix (lines 1-1356) sha256
  `701f90bd80339a092814c22c8b3ead9a8349a97d46c3e14840a7e1d866359d0c`
  (matches gen-1 frozen-prefix record; assembled prefix diff empty).

**Adversary Pass A (family 1):** design notes `g2/ADVERSARY_A.md`
(rationale: hop-count priority exploitation). Worlds `world_G2A.txt`,
`world_G2B_B1.txt`, `world_G2B_B2.txt` (created 2026-10-02 00:37:11
UTC, after prereg freeze 00:29:27 UTC). Pre-seal audit
`g2/audit_A.txt` (all checks pass; check3 refined once: QUERY
expected field may be -2 or a lie claim). Trap simulation
`g2/g2_trapsim.zag` -> `g2/trapsim_A.txt` (structural only, no TNN-2
execution). Sealed: hashes recorded in `SEAL_H2V2_G2.md`, chmod 600.

**Adversary Pass B (family 2):** design notes `g2/ADVERSARY_B.md`
(rationale: convergent-evidence consistency trap; different
rationale, id sub-blocks, and structures from Pass A). Worlds
`world_G2C.txt`, `world_G2D.txt` (created 2026-10-02 00:38:43 UTC).
Pre-seal audit `g2/audit_B.txt` (all pass). Trap simulation
`g2/g2_trapsimB.zag` -> `g2/trapsim_B.txt`. Sealed: hashes appended
to `SEAL_H2V2_G2.md`, chmod 600. Pass A files unmodified (mtimes
verified). G2D is a spare; never scored.

**Evaluator:** hash-verified all five sealed worlds pre-probe (all
match). Driver `g2/g2_driver.zag` (t2_sig_v2, calibration, 8 scored
probes, K-H2-3/K-H2-4 white-box traces); teachers mechanically
verified byte-equal to sealed OBSERVE sequences. Assembled
`g2/g2_full.zag` = frozen cognition (byte-identical) + driver sole
main; compiled with the pinned znc to `g2/g2_bin`.

**Execution:** 3/3 byte-identical runs, SHA-256
`37635c9966f620868723f4f24d88bd48472476ae673c7cfedda91279dcb4e9f7`
(`g2/run1.txt`, `g2/run2.txt`, `g2/run3.txt`).

**Verdict: VALID evaluation. K-H2-1 FAIL, K-H2-2 FAIL, K-H2-3 FAIL,
K-H2-4 FAIL** on frozen TNN-2. Full record: `RESULT_H2V2_G2.md`.

**Governance:** no git commit, no git push, `.wave_lock` untouched.
No forbidden executable invoked (one unresolvable `python3` token
typed; verified never executed; recorded in Step 0 addendum). Pure
Zag throughout; znc quirk honored (u8-backed cells, ig/is style
helpers only in the trap simulator; no `as *i32` slice construction
in functions). No em dashes in any lane documentation
(byte-verified).

## Original Phase-1 context record (retained below)

[Original Phase-1 context record retained below; Phase-2 context follows.]

## Step 0: Toolchain guard (mandatory, executed before any other work)

1. Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   Output (tail):
   ```
   linked: 36 tools
   znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
   verify: python3 absent from safebin PATH (OK)
   verify: python absent from safebin PATH (OK)
   SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
   ```
2. Exported PATH="$HOME/safebin". Resulting PATH: `/home/hatch/safebin`
3. `which python3` returned nothing (exit code 1). Confirmed absent.

Guard status: ACTIVE. No forbidden executable (python3/python/C/node/rust)
was invoked at any point in this lane's work. All subsequent work in this
lane used only safebin tools (coreutils, grep, ls, mkdir).

## Step 1: Context recovered before writing

Prior H2 records and weak K-LT-5 records were read from the repo before
writing the prereg (see lineage section of the prereg):

- H2 prereg frozen `c15a47d63`; H2 evaluation `72173fe11`: H2-EVAL-VOID
  (t2_sig calibration property (ii) failed; trial never ran because
  direct-query facts let activate() short-circuit). VOID preserved.
- H2-v2 generation 1: prereg frozen `84a2a4ddf`; run `8778f1d0b`:
  VALID evaluation, K-H2-1..4 all FAIL on frozen TNN-2 (valid negative
  result; TRIAL_ENTERED=1 on all 8 probes; t2_sig_v2 calibration passed;
  3/3 byte-identical). Recorded honest limitation: worlds normatively
  specified in the prereg from a single design source; the two-family
  post-freeze adversary diversity requirement was NOT met.
- Weak K-LT-5: prereg frozen
  (docs/lab/research-lead/overnight-20260928/weak_klt5/WEAK_KLT5_PREREG.md);
  evaluation `c040e5fde`: WEAK-KLT5-VOID (budget wall invalidates
  protocol; frozen control showed R_frozen = 7.50, killing
  discrimination). VOID terminal.
- H3-lite Node 2: NODE2-REACHABILITY-COMPLETE with verdict UNREACHABLE
  (default never changed from 30). Preserved as a negative finding.

No world files, sealed assets, or prior run outputs were opened or
reused in this lane.

## Step 2: Files written in this lane (Phase 1 only)

- `H2V2_PREREG.md`: fresh H2-v2 generation 2 preregistration (DRAFT).
- `NAMECHECK.md`: this file.

No implementation files were created. No .zag files, no binaries, no
world files, no run outputs, no shell scripts. No git commit, no git
push, no changes to .wave_lock.

## Work plan completed

Phase 1 (prereg writing) is complete. Phase 2 (freeze), Phase 3 (world
building by independent post-freeze adversaries), Phase 4 (evaluation),
and Phase 5 (verdict) are out of scope for this lane.
