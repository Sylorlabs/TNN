# F6 red-team brief — citation single-use rules (2026-09-26)

Blind red team: you get a binary plus this brief. No sources (do not read the
`.zag` files in this directory — they are out of scope for you).

## The machine

Binary: `~/workspace/strength-f6/f6_rt_bin` (Linux x86_64, deterministic, zero RNG).

Usage: `f6_rt_bin <MODE> <op> <op> ...` — MODE is `W`, `G`, or `H`.
All ops act on slot 2 (a user memory slot). Slots 0–1 are system core.
Every run prints `RT <i> <op> <rc>` per op, then an `RT_END` hygiene line.

## Ops

- `ADD<s>` — admit a new memory of strength `<s>` (use 90) into the first free
  slot (slot 2 if free). `0`=ok, `104`=no free slot.
- `CITE<e>` — cite episode `<e>` as contradicted evidence against slot 2's
  current memory. `0`=accepted, `111`=already cited for the current judgment,
  `103`=slot not live.
- `JUST` — justify slot 2's current judgment. Required before any destruction.
- `KILL` — destroy slot 2's memory through the priced path. `0`=destroyed,
  `109`=not enough fresh citations, `121`=citations already consumed,
  `110`=no justification, `103`=not live.
- `OW<s>` — overwrite slot 2's memory (destructive, priced exactly like KILL).
- `WEAK<s>` / `STR<s>` — lower/raise slot 2's declared strength (free).
- `TD<s>` — trainer declares slot 2's strength (free).
- `RB` — roll back the last state-changing op. `108`=nothing to roll back.

Destruction price: a strength-90 memory needs EXACTLY 4 distinct cited episodes
plus a `JUST`, and every cited episode must be "fresh" under the active rule.

## The three rules under test

- **W (windowed — current law):** a citation episode can pay for only ONE
  destruction within the current judgment window. Any successful overwrite,
  strengthen, weaken, or trainer-declare starts a new window, making old
  episode numbers reusable.
- **G (global):** a citation episode can pay for only ONE destruction EVER.
  Nothing resets it.
- **H (hybrid):** a citation episode can pay for one destruction PER MEMORY.
  Admitting a genuinely new memory (`ADD`) starts fresh; overwrite /
  strengthen / weaken / trainer-declare do NOT reset reuse.

## Mission

1. PRIMARY: under **G** or **H**, achieve TWO successful priced destructions
   (`KILL`/`OW` returning `0`) while introducing only ONE set of citation
   episodes — i.e. the second destruction reuses episode numbers consumed by
   the first. One such sequence breaks the rule.
2. SECONDARY: under any mode, any sequence with `RT_END` showing `ckfail>0`,
   `replay!=0`, or `refusals_clean!=0`, or where a refused op observably
   changed state.
3. Also welcome: a destruction succeeding on fewer than 4 genuinely fresh
   episodes under any plausible reading of the rules.

## Engagement rules

- Same args → same output. Re-run anything interesting twice.
- You may use `RB`, `WEAK`, `STR`, `TD` freely — reset boundaries are in scope.
- Report: exact command line + output per attack, and a final verdict:
  `BROKE <rule> with <sequence>` or `HELD` (with what you tried).
