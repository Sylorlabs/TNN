# F4-DEFEND build notes (2026-09-23)

## Toolchain (pinned)

- Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Language: pure Zag; no foreign code, no RNG anywhere in the program.

## Sources in this directory (the F4 fork)

- `dialogue.zag` — the repair fork (canonical `dialogue/` untouched).
- `kb.txt`, `gaz.txt` — byte-identical copies of the canonical data:
  - KB SHA256 `3ef27296c147a101eea0f093940cdbe1bb8be9fe58c21118119646aec6889be1`
  - gazetteer SHA256 `b75fd113dc7e2b3812d7a2b8819641ed2844926c64f33c74adc4ef8e5c85255a`
- `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag` — required at build time:
  the SHA256 module `@import`s the IO module, so both must sit next to the
  source at compile time. The initial build failed with
  "cannot read 'substrate/R33_NATIVE_SHA256_V2.zag'" until `R33_NATIVE_IO_V1.zag`
  was copied in.

## Build

```sh
cd ~/workspace/tnn-lab/dialogue/round2_repair/f4_defend
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 dialogue.zag -o dialogue_bin
```

Compiles with 0 errors. The resulting `dialogue_bin` is a local build artifact
and is NOT committed (see repo policy; do not commit binaries or `.zagd`/
`.zag-cache` artifacts).

## Running a battery

```sh
mkdir -p /tmp/run && cd /tmp/run
cp <this-dir>/kb.txt <this-dir>/gaz.txt <this-dir>/<battery>.txt .
mv <battery>.txt battery.txt
<this-dir>/dialogue_bin > run.log 2>&1
```

The binary reads `kb.txt`, `gaz.txt`, `battery.txt` from the working directory
and writes `SECTION <name> <pass>/<total>` lines plus a `DIGEST` over A-lines
to stdout.

## Changes in this fork vs canonical (all in `dialogue.zag` only)

1. **Stopwords (§2a of PREREG_F4.md).** `a`, `i`, `you` added as required, plus
   the documented pronoun/function-word family (`me my mine we us our ours he
   him his she her hers they them their theirs your yours` + reflexives +
   `about`). Each is documented inline with the reason it pollutes keys.
   `no`/`not` deliberately NOT stopped (negation carriers).
2. **Challenge defense.** Utterance-type patterns (`are you sure`, `you sure`,
   `are you certain`, `sure about that`, `is that true`, `is that right`,
   `really`, `i doubt`) dispatch before composition; the defense reasserts the
   previous retrieved fact, extracts a conflicting number generically from the
   challenge, and appends `I was taught that.` Example:
   `Yes. Herman Melville was born in 1819, not 1818. I was taught that.`
3. **Provenance.** Patterns (`how do you know`, `how did you learn`,
   `where did you learn`, `who told you`, `who taught you`, `why do you think`,
   `how can you be sure`) produce `I was taught that <fact>` — entity-bearing
   questions resolve a fact from their entities, bare ones reuse the previous
   retrieved fact. No external source is ever claimed.
4. **Ellipsis gate.** The existing ellipsis (carry the previous question's
   shape when the turn has no content words) now requires the previous turn to
   have used pronoun binding (`pv[32] > 0`). Rationale: stopping `about` makes
   every "What about X?" content-free; without the gate, "What about Pride
   and Prejudice?" after "Who wrote Moby Dick?" wrongly carries the "who
   wrote" shape (TOPIC regressions TO-02/07/12). With the gate, a "What
   about X?" after a complete question is a topic shift (direct retrieval),
   while after a follow-up ("How tall is it?") it continues the follow-up
   (REFERENT RE-03/08/13 stay fixed). General mechanism, no per-case code.
5. **Stale-fact guard.** Composed responses (`-1` turns) now clear `pv.ans`,
   so a later challenge cannot defend a retrieved fact the composed answer
   already superseded.

All new code is utterance-type patterns plus generic machinery — no entity
names, fact texts, or digits appear in the repair code (verified by scan).
