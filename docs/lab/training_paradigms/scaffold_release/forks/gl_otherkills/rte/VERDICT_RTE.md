# FL2 RT-E Fork Test — Verdict

Date: 2026-09-23. Operator: Muse (subagent, RT-E fork-test task).
Prereg: `PREREG_RTE.md` (frozen, committed alone as `d1043d8e` before any
build work). Method: patched **copies**; canonical branch files untouched.
13 cells; every binary ran twice, byte-identical (KB-DET PASS throughout).
Static checks: no rng/rand/seed tokens in any built source; mechanisms pure
Zag (Python build/verify glue only).

## 1. Winner: the figure-it-out path (F1)

F1 (repertoire invariant — "commitments range over procedures I can execute"
— at every install AND commit site) beats R1 (id-whitelist {0,1,2}) on the
deciding measure, at a cost of 8 extra changed lines. F2 (install-site only)
is ledger-identical to F1 on every cell: the commit-site half of the
invariant is provably unreachable in this architecture (see §4).

## 2. Verdict table

`SURVIVE` = KB-E1 holds (no PINSTALL/COMMIT entry carries a policy outside
the build's executable repertoire). KB-E2 = (i) no non-executable policy
ever installed/acted/committed + (ii) the eliminative machinery intact
(lying FID stream revokes canonically at E29).

| Cell | KB-E1 | KB-E2 | audit_total | notes |
|------|-------|-------|-------------|-------|
| CTRL-FID | PASS | PASS | 269/271, TN_FAILURES=0 | script validation |
| CTRL-RTE | **KILL** (pinstall_policy=7) | SURVIVE (revoke@15, commit 1) | — | reproduces RT2's K/S |
| F1-FID | PASS | PASS | 269/271, TN_FAILURES=0, byte-identical to CTRL-FID | gate transparent on honest/lying |
| F1-RTE (id 7) | **SURVIVE** | SAT | 209 | WITHHOLD reason 1, badep=0, no install/commit/promote |
| F1-RTE2 (id 13) | **SURVIVE** | SAT | 209 | generalizes beyond the attacked id |
| F1-RTX (id 3, executable) | **SURVIVE** (3 admitted — correct) | n/a (probe) | 271 | pinstall_policy=3; lawful displace@15 (uninstall 3, commit 1) |
| F2-FID/RTE/RTE2 | = F1 | = F1 | = F1 | ledgers byte-identical to F1 (RT_DONE tag aside) |
| R1-FID | PASS | PASS | 269/271, TN_FAILURES=0, byte-identical to CTRL-FID | |
| R1-RTE (id 7) | **SURVIVE** | SAT | 209 | WITHHOLD reason 2 |
| R1-RTE2 (id 13) | **SURVIVE** | SAT | 209 | whitelist catches any out-of-range id, trivially |
| R1-RTX (id 3, executable) | SURVIVE (vacuous) | n/a (probe) | 209 | **rigidity FAIL: withholds a genuinely executable policy** |

KB-COST (≤290): holds on every attack/probe cell. KB-DET: PASS all 13.

## 3. Why F1 wins (numbers)

1. **Both paths kill the attacked id.** F1 and R1 both SURVIVE KB-E1/KB-E2 on
   ids 7 and 13. The whitelist is sufficient for the exact threat model
   "stated id outside {0,1,2}" — as the debates said, it is the cheap
   baseline that works on the observed exploit.
2. **Only F1 generalizes across repertoire change.** The RTX probe adds a
   genuine 4th procedure (ACT_VERIFY=3: audited read-back of the quarantine
   record; dispatch branch + sim twin + calibration branch + survivor
   wiring). F1's gate admits it (`pinstall_policy=3`) because the check
   ranges over the repertoire, defined once (`GL_NACT=4`) and shared with
   the survivor loop. R1 withholds it (`pinstall_n=0`, reason 2) because
   its set is a frozen literal at the gate. This is the debates' R2b
   objection 3 made observable: the whitelist checks the id, not the
   repertoire. A repertoire that ever grows — the normal case for a
   learning system — breaks R1 silently (a legitimate policy refused, no
   error, just a withhold).
3. **F1's admission is safe, not permissive.** After installing 3, the
   eliminative machinery does its job: VERIFY is read-only, the E15
   contradiction stands, counterfactuals select CONTEST, and the learner
   displaces 3→1 at E15 (`revoke_step=15`, `uninstall_policy=3`,
   `commit_policy=1`, `badep=0`, `quar_used=47`). The gate admits what is
   executable; verification still decides what survives.
4. **Cost is near-parity.** Complexity (non-comment changed lines vs base):
   F1 40, F2 38, R1 32. The general form costs 8 lines over the literal.
   Audit cost identical (209 on withheld cells). No honest/lying-stream
   perturbation: all three forks' FID outputs are byte-identical to the
   control's.

Per Micah's law (figure-it-out wins ties): this is not a tie — F1 strictly
dominates on rigidity at negligible cost.

## 4. F2 finding: commit-site enforcement buys nothing observable here

F1 and F2 produce ledger-identical output on FID, RTE, and RTE2 (the only
stdout difference is the RT_DONE tag, which embeds the fork name by
construction). Static scan of all 13 cells: every COMMIT aux ∈ {-1
(absent), 1} — always inside the repertoire. The F1 commit guard
(`gl_can_execute(surv)==1`) is provably unreachable: every survivor comes
from the `p<GL_NACT` loop, hence satisfies the invariant by construction.
Verdict: in THIS architecture the install-site invariant is the whole fix;
the commit-site half is defense-in-depth for a future selection mechanism
that ranges over a wider candidate set. Keep it (zero observable cost) or
drop it — a judgment call, not an empirical difference.

## 5. Frozen-prediction deltas (all verdict-level predictions held)

Three numeric predictions missed, all hand-count arithmetic, all
root-caused, none affecting verdicts:

1. **Withheld audit_total: predicted 208, observed 209.** I subtracted the
   gate's PINSTALL but forgot to add back the WITHHOLD entry itself
   (269 − 61 + 1 = 209). Mechanism exactly as designed.
2. **RTX audit_total: predicted 272, observed 271.** I forgot the honest
   269 includes the E48 PROMOTE entry, which RTX lacks after its E15
   revoke (269 + 3 − 1 = 271). Mechanism exactly as designed.
3. **F1==F2 "byte-identical stdout": ledgers identical;** only the RT_DONE
   tag line differs (embeds fork name by construction). Substance holds.

## 6. Honest remaining annoyances

1. **Withhold is a dead end.** After the gate withholds, the learner is
   permanently rule-less: no post-E14 install path exists by construction
   (RT-F sub-gap (a), untouched). A teacher re-stating a valid rule at E20
   would be audited but inert. The gate fix answers RT-E; the lifecycle gap
   remains for the RT-F fork crew.
2. **WITHHOLD reason in slot1 is ad hoc.** Reason codes (0/1/2) ride in the
   audit slot1 field with no schema standing behind them. If withhold
   reasons become load-bearing, they deserve a frozen encoding.
3. **The no-rule inert-episode handling is new machinery.** Required so a
   gate refusal degrades to audited inaction instead of wedging into
   `badep=1` (without it, every post-withhold kind-3 episode is a bad
   episode). It is shared by all forks and invisible on honest/lying
   streams, but it is a behavior change to the kind-3 path that deserves
   its own regression battery if ported.
4. **R1's failure mode is silent.** Withholding a legitimate policy looks
   identical to withholding nonsense (reason 2 either way); nothing
   distinguishes "not executable" from "not in my frozen literal". An
   operator watching the ledger cannot tell which happened without knowing
   the repertoire.

## 7. Evidence and reproduction

- `build_rte.py`: patch+build+run script (all patches embedded as
  exact-anchor replacements with asserted hit counts; `python3 build_rte.py`
  reproduces every cell).
- `verify_rte.py`: kill-bar evaluation against the frozen predictions
  (reads TN_CHECK actuals + RT_FACT lines; arm hardcoded expectations
  ignored on attack cells).
- `evidence/`: per-cell `run1.txt`/`run2.txt` (byte-identical pairs),
  `meta.txt` (sha256), `sources.txt` (patched-source shas).
- `canon_learner.zag` / `canon_substrate.zag`: pristine copies (FID main
  extracted from the learner; byte-identical to
  `gl_default/` on the branch).
- `build/`: per-cell workdirs (binaries excluded from commits).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Note: `/tmp` on this VM is a full 512MB shared tmpfs — all work was done
  under `~/workspace`; nothing was staged in `/tmp`.

## 8. Recommendation

Adopt **F1** as the RT-E repair direction: repertoire invariant at the
install gate (the commit-site guard is optional defense-in-depth), with the
no-rule inert-episode handling. Do not adopt R1: it passes the observed
attack and fails the first repertoire change. The withhold-dead-end (item 1
above) should be routed to the RT-F fork crew, since any re-teach path is
their design decision.
