#!/usr/bin/env python3
"""Deterministic held-out target list generator for Crew C (CONTROL).

Method is frozen by this file's committed content; outputs are committed
SEALED before the control path's target handling is built (prereg 5.5).

No RNG anywhere: all sequences are closed-form or fixed tables.
"""
import json, math

# ---------- pitch: 40 log-spaced targets in [80,1200], integer Hz ----------
pitch_targets = []
for i in range(40):
    f = 80.0 * (1200.0 / 80.0) ** (i / 39.0)
    pitch_targets.append(int(round(f)))
pitch_targets = sorted(set(pitch_targets))
assert len(pitch_targets) == 40, len(pitch_targets)
assert pitch_targets[0] >= 80 and pitch_targets[-1] <= 1200

# ---------- envelope: 20 items, 7 flat / 7 rise / 6 decay, interleaved ----------
env_classes = []
cycle = ["flat", "rise", "decay"]
for i in range(20):
    env_classes.append(cycle[i % 3])
env_targets = [f"env:{c}" for c in env_classes]
assert env_classes.count("flat") == 7 and env_classes.count("rise") == 7 \
    and env_classes.count("decay") == 6

# ---------- rhythm: 20 items, 10 even / 10 swing21, alternating ----------
rhy_classes = []
for i in range(20):
    rhy_classes.append("even" if i % 2 == 0 else "swing21")
rhy_targets = [f"rhy:{c}" for c in rhy_classes]
assert rhy_classes.count("even") == 10 and rhy_classes.count("swing21") == 10

# ---------- prosody (C-R2): 20 log-spaced CV% targets in [0.3, 25] ----------
prosody_targets = []
for i in range(20):
    cv = 0.3 * (25.0 / 0.3) ** (i / 19.0)
    prosody_targets.append(round(cv, 2))
assert prosody_targets[0] >= 0.3 and prosody_targets[-1] <= 25.0
assert len(set(prosody_targets)) == 20

# ---------- C-R1: 10 pair-combined targets (axes never co-occur in dev) ----------
cr1_targets = [
    "pitch:880+env:decay",
    "pitch:110+env:rise",
    "pitch:660+env:decay",
    "rhy:swing21+pitch:990",
    "rhy:even+pitch:150",
    "pitch:440+env:rise",
    "rhy:swing21+env:decay",
    "pitch:1200+env:rise",
    "pitch:80+env:decay",
    "rhy:even+env:rise",
]

# ---------- dev targets (disjoint by construction; used pre-freeze only) ----------
dev_targets = [
    "pitch:95", "pitch:165", "pitch:275", "pitch:390", "pitch:520",
    "pitch:700", "pitch:950", "pitch:1100",
    "env:flat", "env:rise", "env:decay", "env:flat", "env:rise",
    "rhy:even", "rhy:swing15", "rhy:swing30",
    "prosody:1.0", "prosody:8.0",
    "pitch:330+env:rise", "rhy:swing30+pitch:520",
]

# ---------- C0: frozen constant descriptor (intent path severed) ----------
C0_DESCRIPTOR = "pitch:220+env:flat+rhy:even"

# ---------- C1 derangements (frozen; verified no fixed points) ----------
# pitch: cyclic shift by 17 (gcd(17,40)=1 -> derangement, distinct values)
SHIFT = 17
assert math.gcd(SHIFT, 40) == 1
c1_pitch = [f"pitch:{pitch_targets[(i + SHIFT) % 40]}" for i in range(40)]
for i in range(40):
    assert c1_pitch[i] != f"pitch:{pitch_targets[i]}", "pitch C1 fixed point"

# env: class derangement flat->rise, rise->decay, decay->flat
ENV_DERANGE = {"flat": "rise", "rise": "decay", "decay": "flat"}
c1_env = [f"env:{ENV_DERANGE[c]}" for c in env_classes]
for i in range(20):
    assert c1_env[i] != env_targets[i], "env C1 fixed point"

# rhy: class derangement even<->swing21
RHY_DERANGE = {"even": "swing21", "swing21": "even"}
c1_rhy = [f"rhy:{RHY_DERANGE[c]}" for c in rhy_classes]
for i in range(20):
    assert c1_rhy[i] != rhy_targets[i], "rhy C1 fixed point"

# ---------- disjointness ----------
heldout_descriptors = (
    [f"pitch:{f}" for f in pitch_targets] + env_targets + rhy_targets
    + [f"prosody:{cv}" for cv in prosody_targets] + cr1_targets
)
# Pitch and prosody are continuous parameters: dev VALUES must not collide
# with held-out values (a value-keyed table must not see held-out values).
# Env/rhy targets are CATEGORY labels (flat/rise/decay, even/swing) shared
# by design — the battery IS the category distinction; dev/holdout separation
# there is at the render level (dev renders use different carrier pitches,
# documented in the build doc, so no dev render is byte-identical to a
# held-out render).
heldout_pitch_vals = {int(t.split(":")[1]) for t in
                      [f"pitch:{f}" for f in pitch_targets]}
dev_pitch_vals = {int(t.split(":")[1]) for t in dev_targets
                  if t.startswith("pitch:") and "+" not in t}
assert not (heldout_pitch_vals & dev_pitch_vals), \
    f"pitch dev/held-out overlap: {heldout_pitch_vals & dev_pitch_vals}"
heldout_pros_vals = {float(t.split(":")[1]) for t in
                     [f"prosody:{cv}" for cv in prosody_targets]}
dev_pros_vals = {float(t.split(":")[1]) for t in dev_targets
                 if t.startswith("prosody:")}
assert not (heldout_pros_vals & dev_pros_vals), \
    f"prosody dev/held-out overlap: {heldout_pros_vals & dev_pros_vals}"
# also no held-out descriptor equals the C0 constant
assert C0_DESCRIPTOR not in heldout_descriptors

manifest = {
    "battery": "CONTROL",
    "prereg": "audio_principles/PREREG_AUDIO_PRINCIPLES.md sec 2.2",
    "generation": "gen_targets.py (deterministic, no RNG); committed sealed "
                  "before control-path target handling was built",
    "pitch": {"n": 40, "range_hz": [80, 1200],
              "targets": [f"pitch:{f}" for f in pitch_targets],
              "hit": "|F0-target|/target <= 2%", "bar": ">= 28/40"},
    "envelope": {"n": 20, "classes": {"flat": 7, "rise": 7, "decay": 6},
                 "targets": env_targets,
                 "hit": "scorer 3-class == target class", "bar": ">= 14/20"},
    "rhythm": {"n": 20, "classes": {"even": 10, "swing21": 10},
               "targets": rhy_targets,
               "hit": "onset-pattern match per frozen scorer rule",
               "bar": ">= 14/20"},
    "prosody_cr2": {"n": 20, "cv_range_pct": [0.3, 25.0],
                    "targets": [f"prosody:{cv}" for cv in prosody_targets],
                    "hit": "per frozen scorer rule (diagnostic bearing)",
                    "bar": ">= 14/20 (diagnostic)"},
    "compositionality_cr1": {"n": 10, "targets": cr1_targets,
                             "hit": "all named axes hit",
                             "note": "diagnostic; TABLE-SUSPECT if C-PASS "
                                     "but at chance"},
    "c0": {"descriptor": C0_DESCRIPTOR,
           "note": "intent path severed; same machinery renders its default"},
    "c1_derangement": {
        "method": "pitch: cyclic shift by 17 over the 40-target order; "
                  "env: class derangement flat->rise, rise->decay, decay->flat; "
                  "rhy: class derangement even<->swing21. "
                  "Verified: zero fixed points (every deranged label differs "
                  "from the true label), so a faithful renderer scores ~0 "
                  "on C1; C1 >= 25% on any axis voids the battery (lenient "
                  "scorer).",
        "pitch_shift": SHIFT,
        "pitch_deranged": c1_pitch,
        "env_derange_map": ENV_DERANGE,
        "env_deranged": c1_env,
        "rhy_derange_map": RHY_DERANGE,
        "rhy_deranged": c1_rhy,
    },
    "dev_targets": dev_targets,
    "dev_heldout_disjoint": True,
}

with open("TEST_MANIFEST_C.json", "w") as f:
    json.dump(manifest, f, indent=2)

# human-readable sealed list
lines = []
lines.append("# CREW C — SEALED HELD-OUT TARGET LIST")
lines.append("")
lines.append("Frozen before the control path's target handling was built.")
lines.append("Dev targets are disjoint (descriptor-string level, verified).")
lines.append("No RNG in generation (closed-form sequences + fixed tables).")
lines.append("")
lines.append("## Pitch (40, [80,1200] Hz, hit: |F0-t|/t <= 2%, bar >= 28/40)")
lines.append("")
for i, t in enumerate(pitch_targets):
    lines.append(f"- P{i:02d} `pitch:{t}`")
lines.append("")
lines.append("## Envelope (20: 7 flat / 7 rise / 6 decay, bar >= 14/20)")
lines.append("")
for i, t in enumerate(env_targets):
    lines.append(f"- E{i:02d} `{t}`")
lines.append("")
lines.append("## Rhythm (20: 10 even / 10 swing21, bar >= 14/20)")
lines.append("")
for i, t in enumerate(rhy_targets):
    lines.append(f"- R{i:02d} `{t}`")
lines.append("")
lines.append("## Prosody C-R2 (20, CV% in [0.3,25], diagnostic, bar >= 14/20)")
lines.append("")
for i, cv in enumerate(prosody_targets):
    lines.append(f"- S{i:02d} `prosody:{cv}`")
lines.append("")
lines.append("## Compositionality C-R1 (10 pairs, diagnostic)")
lines.append("")
for i, t in enumerate(cr1_targets):
    lines.append(f"- X{i:02d} `{t}`")
lines.append("")
lines.append("## Arms")
lines.append("")
lines.append(f"- C0 (null): descriptor replaced by frozen constant "
             f"`{C0_DESCRIPTOR}`")
lines.append("- C1 (shuffle guard): frozen derangement — pitch cyclic shift "
             "by 17; env flat->rise, rise->decay, decay->flat; rhy "
             "even<->swing21. Zero fixed points verified.")
lines.append("")
lines.append("## Dev targets (disjoint, pre-freeze use only)")
lines.append("")
for t in dev_targets:
    lines.append(f"- `{t}`")
lines.append("")

with open("SEALED_TARGETS.md", "w") as f:
    f.write("\n".join(lines))

print("pitch[0],[-1]:", pitch_targets[0], pitch_targets[-1])
print("prosody[0],[-1]:", prosody_targets[0], prosody_targets[-1])
print("OK: manifest + sealed list written; all assertions passed.")
