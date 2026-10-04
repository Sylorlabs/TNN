# Boundary audit — Phase A2 wiring (PREREG_LH K-W5)

## The rule
"Only WAV bytes + intent/question descriptor cross into the deliberation
binary. Any measured value or feature sidecar crossing the boundary =
BOUNDARY-BREACH, run void."

## Architecture and what crosses each boundary

The evidence pipeline is two pure-Zag binaries chained by a shell harness:

```
session_run <session.txt> <intent> <mode>  →  journal (stdout)
       │ (journal piped)
render_act <outdir>  →  epNN.wav per episode
```

### Stage 1+2: `session_run` (hear + reason, one binary)
**Inputs crossing the process boundary:**
- `session.txt`: list of WAV file paths (not audio bytes, not features).
- `intent`: `survey` | `monitor` | `attend` (frozen vocabulary).
- `mode`: `live` | `ablate-constant` | `ablate-shuffle` (harness control).

**Inside the binary:** it opens each WAV, runs the frozen organ DSP + the
low-F0 guard, produces the descriptor vector, deliberates over it with
persistent in-memory state, and journals. The descriptor vector NEVER crosses
a process boundary — it is created and consumed inside `session_run`.

**Audit:** no measured sidecar enters. The WAV bytes are read by the binary
itself from the paths in the session file. Intent and mode are harness
controls, not measurements. ✓ CLEAN under both the strict and loose readings.

### Stage 3: `render_act` (act)
**Inputs:** the journal (ACTION + HEARD lines), `<outdir>`.
**Audit:** the action descriptor is the deliberation's own output, not an
external measurement. The heard F0 echoed in RECALL renders comes from the
journal (the system's own perception). ✓ CLEAN.

### Diagnostic tools (NOT in the evidence path)
- `emit_desc`: WAV → descriptor line on stdout. Used for F0 characterization
  and debugging only. Its output never feeds `session_run`.
- `deliberate`: descriptor lines → journal. Standalone diagnostic; the
  evidence runs use `session_run`'s internal deliberation (same logic).

## K-W3 (no Python in per-episode path)
The per-episode path is `session_run` → (pipe) → `render_act`, both native
Zag binaries. The shell harness only chains them and prepares intents.
Python is used offline afterward (scorer on committed journals). ✓

## Verdict
BOUNDARY-CLEAN. No measured sidecar crosses into deliberation; the organ's
descriptors are produced inside the deliberation binary itself.
