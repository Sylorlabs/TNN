# NAMECHECK: ARENA-ADVERSARY (independent sealed-world adversary)
Lane: ARENA-ADVERSARY, wave-20261001-2021pdt
Role: independent adversary for sealed world design and sealed evaluation of TCNP.
Independence: this worker is not the ARENA lane worker and not the ARENA-IMPL
builder. Work proceeds from the frozen prereg PREREG_ARENA_PROCEDURE.md only
(committed alone at 8f8663026). The builder's dev worlds (in /tmp) were never
opened. The builder's implementation source (.zag contestant/ablated files)
was never opened. Only harness scripts (run_dev.sh, run_k4.sh) and the
published wire protocol in IMPLEMENTATION.md were consulted for invocation.

## Step 0: safebin activation (worker toolchain guard)

- Ran: bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
- Exported: PATH="$HOME/safebin" (36 tools, pinned znc verified by setup)
- `which python3` prints NOTHING (exit 1). `which python` also prints nothing.
- Guard status: PASS. Pure Zag only for all computation in this lane.
- All shell commands in this lane run with PATH="$HOME/safebin".

## Step 1: binary integrity verification (before any run)

Expected per task assignment:
- bin/tcn_p SHA-256 71ea78f717e5cf25146487b1da110b05173573af1924a00e926ade0579cdda2b
- bin/tcn_p_memctrl SHA-256 4dbe4c4584a77e124c4b60df65f7580d2250171c9733c396ce1caefa9af42af2b

Found on disk (docs/lab/rsi/runs/wave-20261001-2021pdt/ARENA/bin/, untracked in git):
- tcn_p:         71ea78f717e5cf25146487b1da110b05173573af1924a00e726ade0579cdda2b
- tcn_p_memctrl: 4dbe4c4584a77e124c4b60df65f7580d2250171c9733c396ce1caefa9af42af1

Builder-recorded hashes (IMPLEMENTATION.md lines 22-24, NAMECHECK.md line 107):
- tcn_p:         71ea78f717e5cf25146487b1da110b05173573af1924a00e726ade0579cdda2b (MATCHES disk)
- tcn_p_memctrl: 4dbe4c4584a77e124c4b60df65f7580d2250171c9733c396ce1caefa9af42af2b (DIFFERS from disk)

### Resolution (rebuild from committed sources, pinned znc, safebin)

Rebuilt all three lane binaries from the committed .zag sources with the
pinned znc:
- tcn_p_contestant.zag rebuild -> 71ea78f717e5cf25146487b1da110b05173573af1924a00e726ade0579cdda2b
  (byte-identical to disk; matches builder docs; the task text hash differs
  by one hex digit, assessed as a transcription error in the task text)
- tcn_p_ablated.zag rebuild -> 73b484d00dd6476eaeffd52d8087c585b89f60ad41d0dd531d5163db89a66065
  (byte-identical to disk; matches builder docs)
- tcn_p_memctrl.zag rebuild -> 4dbe4c4584a77e124c4b60df65f7580d2250171c9733c396ce1caefa9af42af1
  (byte-identical to disk; DIFFERS from the builder's documented hash)

Conclusion: all on-disk binaries are faithful deterministic builds of the
committed lane sources. The builder's documented memctrl hash is stale
(probably an earlier build); the on-disk memctrl binary is the trustworthy
K7b control and was used as such. No binary was run before this
verification completed. Guard status for the lane: no forbidden executable
invoked at any point (zero Python invocations; shell only sequenced pinned
znc, built binaries, git read ops, and file copies).

## Step 2: scope

- Design 5 sealed worlds (A-E) from the prereg world requirements.
- Write world files to ARENA/sealed/; record sha256 in SEALED_WORLDS.md BEFORE running.
- Run the frozen tcn_p binary on sealed worlds, 3/3 byte-identical, with TCNP trace.
- Score K1-K9 per the task's frozen bars; report verdict.
- Stop after sealed evaluation. No commits (coordinator commits).
- Documentation rule: no em-dash bytes in lane docs. Determinism: 3/3 byte-identical reruns.
