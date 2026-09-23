# BUILD.md — F5-ROUTER fork build notes

## Toolchain (pinned)

`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Layout

`dialogue/round2_repair/f5_router/` is a cleanroom fork:
- `dialogue.zag` — the repaired program (only file with code changes)
- `kb.txt`, `gaz.txt` — byte-identical copies of the canonical inputs
- `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag` — import deps
  (dialogue.zag `@import`s the SHA256 module, which imports the IO module)
- `probes/` — scaffold + held-out batteries and all run logs

The canonical `dialogue/` tree was never edited.

## Build

```
cd dialogue/round2_repair/f5_router
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 dialogue.zag -o dialogue_f5_bin
```

Pre-existing analyzer warnings only (dead-loop note in `gaz_scan`,
ignored `proc_sentence` return values — all present in the canonical
source too). No new warnings from the F5 code.

## Run a battery

The binary reads `battery.txt`, `kb.txt`, `gaz.txt` from the CWD:

```
cp probes/scaffold_battery.txt battery.txt
./dialogue_f5_bin > probes/run_scaffold_N.log 2>&1
```

`T <id> <turn> PASS/FAIL` lines score each `U` against its `E` line;
`A <response>` lines show the actual output. `battery.txt` is scratch
(copies live in `probes/`) and the binary is NOT committed.

## What changed in dialogue.zag (only change vs canonical)

1. `tok_has` — token-level literal match on the lowercased input buffer.
2. `is_mem_q` — memory-question detector: `remember`/`recall` tokens, or
   self-referential past speech (`i`/`my` + ask/asked/say/said/tell/told/
   question/questions).
3. `utter_type` — dispatcher: 3=forget (`forget`/`forgot`/`forgotten`),
   1=joke (`joke`/`jokes`), 2=memory, 0=other. Precedence forget>joke>memory.
4. `mem_ord` — ordinal token scan via the existing number-word table.
5. `mem_answer` — reads kind-0 hist rows (all but the current turn),
   selects by ordinal (`first`→oldest, `last`/`previous`/`latest`→newest,
   number-words→nth, default→newest), quotes the turn.
6. Step 0 at the top of `do_turn`: if `utter_type>0`, answer with the
   type's strategy (`I don't know any jokes.` / `You asked: ...` /
   `I can't forget.`), update salience/pv like compose, return -1.
   Type 0 falls through to the untouched pipeline.

No KB, gazetteer, retrieval, or scoring code was touched.
