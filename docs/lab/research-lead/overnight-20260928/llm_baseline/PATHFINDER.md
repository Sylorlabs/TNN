# LLM Baseline Pathfinder Report

Date: 2026-09-30 UTC. Investigation only. No implementation.

## Verdict: PATH-BLOCKED

A compliant serious LLM baseline for the frozen CA-2 arena is not achievable
under current authorizations. The precise blocking layer is credentials plus
spend authorization, not the Zag toolchain.

## 1. What the prereg requires

ARENA_PREREG.md section 3.2: the LLM baseline is a frontier-class model via
an OpenAI-compatible chat-completions endpoint, receiving the full briefing,
the same OBSERVE and EXPERIMENT tools with the same budgets, a persistent
file-backed notebook with top-8 retrieval, realistic prompting, and single
attempt per test question (parse failures count as wrong). Model name recorded
per run; tokens in/out taken from API usage fields; cost ledger kept.

Official status: AMEND2 section A2.3 marks the LLM column BLOCKED_BY_TOOLCHAIN.
AMEND3 section A3.4 (CA-2 refreeze): the arena is ready to accept a serious
LLM baseline; the turn protocol and prompt pack are frozen as the interface.

## 2. Finding: the toolchain block misidentifies the layer

Prereg 5.1 specifies the contestant protocol as a line protocol over
stdin/stdout: the harness spawns the contestant process and drives turns. The
LLM adapter was always specified as an external runner that translates prompts
into ACT/ANS lines. It was never required to be a Zag component.

The committed driver (run_arena.sh) already sequences per-turn process
invocations in bash. A bash plus curl adapter implementing the frozen protocol
would not place arena logic in shell and would not violate the pure-Zag rule
governing the committed arena components (world generator, contestant,
scorer). AMEND2 itself concedes the point: "any external runner with TLS
capability can implement the LLM side later against the committed battery and
briefing without changing the arena."

Network egress was verified live: api.anthropic.com and huggingface.co are
reachable through the environment proxy. TLS-capable tooling (curl) exists.

Correction: there is no technical barrier to calling an LLM API from the
arena harness. The block is (a) no API credential on file and (b) no spend
authorization. A future amendment should relabel the status accordingly.

## 3. Credential: none available

The only stored credential in this environment is the GitHub PAT. No LLM API
key exists here; the prereg records this at 4.2 and 9(f). No skill in the
catalog provides LLM inference. I did not go hunting through secret stores;
the documented record is sufficient.

## 4. Spend: not authorized

Standing red line: never spend money. A frontier-class API run costs money.
Obtaining a key independently would require creating an external provider
account, which is contacting outsiders plus a new commitment, both red lines
without explicit direction.

## 5. Alternatives considered and rejected

- Local open-weights model. The machine has 7 GB RAM, no GPU, and 7.5 GB of
  disk. Nothing near frontier-class can run here. A 1 to 3B local model would
  violate prereg 3.2 (frontier-class required) and the rule against a
  crippled baseline. Rejected.
- Agent self-baselining (using this research session's own model as the LLM
  contestant). Circular, non-reproducible, no recorded model name, no API
  usage fields for the cost ledger, and a direct conflict of interest.
  Rejected.
- Free-tier API signup. Requires a new external account. Rejected per
  section 4.

## 6. Cost estimate, to make the ask concrete

The frozen battery: 131 turns (1 brief, 53 expo, 4 observe_result, 72 test,
1 done), about 12 KB total. Per test turn the adapter would send the briefing,
the prompt pack, top-8 notebook notes, and the question: roughly 2 to 4K
input tokens. A full run is on the order of 150 to 300K input tokens with
negligible output (single-line answers). At typical frontier pricing that is
low single-digit dollars per run; three runs plus the blind control stay
under roughly 10 to 20 dollars. Estimate only; actual cost depends on the
model and provider chosen.

## 7. What would unblock it

1. The user supplies an OpenAI-compatible API key through the secure capture
   flow. Never in chat.
2. The user explicitly authorizes the spend, with a stated cap.
3. Then: build the bash plus curl adapter against the frozen stdin/stdout
   protocol, plumbing-test it against a stub per the original 9(f) intent,
   and run the frozen CA-2 battery. No arena changes are needed. The prompt
   pack (world/llm_prompt_pack.txt) and the turn protocol are already frozen
   and committed.

Until both conditions hold, the LLM column stays PENDING/BLOCKED and no
TNN-vs-LLM comparison may be claimed. The current actual-TNN score of 0.573
(39/68) stands alone.
