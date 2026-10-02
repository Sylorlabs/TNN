# AMENDMENT A3 to CA-1 prereg: CA-1 void; clean refreeze protocol (CA-2)

Date: 2026-09-30 UTC. Committed alone before any refreeze code, seed, or
world artifact exists. Authority: research-director order 2026-09-29
(pure-Zag rule restored literally: no Python anywhere, including harnesses
and no-ops; violation is void-on-sight; disclosure does not cure).

## A3.1 CA-1 wave is VOID

The CA-1 pilot report (CA1_PILOT_REPORT.md) records two Python invocations
during the CA-1 wave, quoted verbatim:

1. A no-op `python3 - <<'EOF' ... EOF` heredoc (empty body, no files created)
   launched during a spot-check of the earlier Python deletion.
2. A no-op `python3 -c "print('no')"` launched inadvertently during a later
   editing step.

Both were no-ops that produced no artifacts and touched no arena logic. The
rule is literal regardless. The CA-1 wave is therefore VOID. No number from
the CA-1 pilot (scores, costs, determinism checks) may be cited as an arena
result. CA-1 is preserved as development history only: commit `bd60dc9ed`
and CA1_PILOT_REPORT.md.

## A3.2 Retired seed

Seed 20260929 was viewed during discarded Python development and is
exploratory only. It is retired and must not seed any arena world. Active
sources are re-pointed under A3.3. Historical documents (ARENA_PREREG.md,
ARENA_PREREG_AMEND2.md, CA1_PILOT_REPORT.md) keep their text unchanged as
history; the retired seed string must not appear in any active source after
substitution.

## A3.3 Clean refreeze protocol (CA-2)

1. Seed derivation: 6 bytes from /dev/urandom, interpreted as one unsigned
   integer, written directly to `SEALED_SEED.txt` by shell redirection. The
   refreeze worker must not view the value at any point; only the file's
   sha256 is reported for verification.
2. Seed installation: the seed is baked into `world_gen.zag` (replacing the
   retired constant) by shell substitution through a variable, verified by
   count and pattern only, never displayed. `arena.zag` report strings are
   updated the same way. Proof headers regenerate from the new constant.
3. Allowed tooling only: znc, bash, git, cmp, sha256sum, od, tr, head, and
   shell redirection. No Python at any point, including no-ops, heredocs,
   and one-liners. Any Python invocation voids the CA-2 wave the same way.
4. Determinism bars (frozen): the world generator is run twice from the
   sealed seed and every artifact must be byte-identical (cmp). The full
   contestant pilot is run three times from fresh state and every reply
   sequence must be byte-identical. The scorer is run on the final pilot.
5. Post-substitution check: the retired seed string occurs zero times in
   active sources (grep count 0; historical docs excluded).

## A3.4 Reference contestant scope

The hand-authored `tnn_contestant.zag` is an infrastructure self-test ONLY.
It validates sealed generation, turn sequencing, state persistence across
process restarts, scoring, and cost accounting. It is not evidence that TNN
scores 16/16 and must never be cited that way. A clean CA-2 run makes the
arena ready to accept (1) the actual developmental TNN and (2) a serious LLM
baseline, whose capability curves and costs are then measured.

## A3.5 LLM baseline: BLOCKED_BY_TOOLCHAIN re-confirmed 2026-09-30

The znc toolchain exposes `_zag_raw_syscall` but no socket, TLS, or HTTP
builtins and links no TLS library. Implementing TCP plus TLS 1.3 plus HTTP
in Zag inside this program is infeasible, and no Python HTTP client is
permitted. There is therefore still no mechanism in this environment by
which a pure-Zag arena can call an LLM API. The frozen contestant turn
protocol (prereg section 5) and `llm_prompt_pack.txt` remain the interface
for a future external runner with TLS capability. No LLM results are
claimed or implied.

No other prereg terms change. All frozen bars stand, including C11
Criterion 0 (the reference contestant must answer UNKNOWN where no
representational expansion occurred).
