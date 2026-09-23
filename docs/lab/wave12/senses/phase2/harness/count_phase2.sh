#!/bin/bash
# Counting reporter for TNN senses phase 2.
# Usage: count_phase2.sh <audio_log> <vision_log> <crosscut_log>...
#
# Counts the 155 preregistered checks against the proposed qual bar:
#   A32 / B18 / C20 / D48 / E24 (modality tracks, manifest-driven)
#   F2 / G2 / H4 / I5 (cross-cutting harness)
# Manifests (manifest_audio.tsv, manifest_vision.tsv) list the exact counted
# check names per sibling frozen prereg; only those names count toward a
# section tally. Supplemental setup/gate lines (e.g. se2a-a-refusals,
# se2v-d-records-48) are reported as informational, never as failures.
# Log check names are NUL-stripped before matching: vision §E names carry a
# trailing NUL from a 16-byte name buffer (cosmetic; names stay unique).
# Verdict is MEETS-PROPOSED-BAR or DOES-NOT-MEET, exit 0/1. Stdout never
# contains the Q-word: the proposed bar is unsigned; only Micah can qualify
# a modality.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
[ $# -ge 3 ] || { echo "usage: $0 <audio_log> <vision_log> <crosscut_log>..."; exit 2; }
AUDIO_LOG="$1"; VISION_LOG="$2"; shift 2

python3 - "$HERE" "$AUDIO_LOG" "$VISION_LOG" "$@" <<'EOF'
import sys

here, audio_log, vision_log, crosscut_logs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]

def load_manifest(path):
    out = []  # (section, name)
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        sec, name = line.split("\t")
        out.append((sec, name))
    return out

def parse_log(path):
    occ = {}  # name -> [(act, exp)]
    total = 0
    with open(path, "rb") as f:
        for raw in f.read().split(b"\n"):
            if not raw.startswith(b"CL_CHECK,"):
                continue
            parts = raw.split(b",")
            if len(parts) < 4:
                continue
            name = parts[1].replace(b"\x00", b"").decode("utf-8", "replace")
            occ.setdefault(name, []).append((parts[2].decode(), parts[3].decode()))
            total += 1
    return occ, total

def count_expected(occ, expected, label):
    # expected: [(section, name)]; returns (per_section dict, failures, conflicts, missing)
    per = {}
    failures, conflicts, missing = [], [], []
    for sec, name in expected:
        hits = occ.get(name, [])
        if not hits:
            missing.append((sec, name))
            continue
        vals = set(hits)
        if len(vals) > 1:
            conflicts.append((sec, name, sorted(vals)))
            continue
        act, exp = hits[0]
        if act != exp:
            failures.append((sec, name, act, exp))
            continue
        per[sec] = per.get(sec, 0) + 1
    return per, failures, conflicts, missing

def unlisted(occ, expected_names):
    return sorted(set(occ) - set(expected_names))

audio_man = load_manifest(f"{here}/manifest_audio.tsv")
vision_man = load_manifest(f"{here}/manifest_vision.tsv")
crosscut_expected = [
    ("F", "se2f-build-hash"), ("F", "se2f-replay-runs"),
    ("G", "se2g-no-banned"), ("G", "se2g-no-computed-strength"),
    ("H", "se2h-audit-complete"), ("H", "se2h-no-silent-admit"),
    ("H", "se2h-fresh-state"), ("H", "se2h-refusals"),
    ("I", "se2i-records"), ("I", "se2i-slots"), ("I", "se2i-audit"),
    ("I", "se2i-audio-twins"), ("I", "se2i-vision-twins"),
]

audio_occ, audio_total = parse_log(audio_log)
vision_occ, vision_total = parse_log(vision_log)
cc_occ = {}
cc_total = 0
for p in crosscut_logs:
    o, t = parse_log(p)
    cc_total += t
    for k, v in o.items():
        cc_occ.setdefault(k, []).extend(v)

results = {}
problems = []
for label, occ, man in (("audio", audio_occ, audio_man), ("vision", vision_occ, vision_man)):
    per, failures, conflicts, missing = count_expected(occ, man, label)
    for sec in "ABCDE":
        results[sec] = results.get(sec, 0) + per.get(sec, 0)
    for sec, name, act, exp in failures:
        problems.append(f"FAIL [{label}] {name}: actual={act} expected={exp}")
    for sec, name, vals in conflicts:
        problems.append(f"CONFLICT [{label}] {name}: {vals}")
    for sec, name in missing:
        problems.append(f"MISSING [{label}] §{sec} {name}")
    extra = unlisted(occ, [n for _, n in man])
    print(f"info [{label}]: {audio_total if label=='audio' else vision_total} CL_CHECK lines, "
          f"{len(extra)} supplemental (uncounted): {', '.join(extra[:8])}{'...' if len(extra)>8 else ''}")

per, failures, conflicts, missing = count_expected(cc_occ, crosscut_expected, "crosscut")
for sec in "FGHI":
    results[sec] = per.get(sec, 0)
for sec, name, act, exp in failures:
    problems.append(f"FAIL [crosscut] {name}: actual={act} expected={exp}")
for sec, name, vals in conflicts:
    problems.append(f"CONFLICT [crosscut] {name}: {vals}")
for sec, name in missing:
    problems.append(f"MISSING [crosscut] §{sec} {name}")
extra = unlisted(cc_occ, [n for _, n in crosscut_expected])
print(f"info [crosscut]: {cc_total} CL_CHECK lines, {len(extra)} supplemental (uncounted): "
      f"{', '.join(extra[:8])}{'...' if len(extra)>8 else ''}")

expect = {"A": 32, "B": 18, "C": 20, "D": 48, "E": 24, "F": 2, "G": 2, "H": 4, "I": 5}
ok = True
total_p = 0
for s in "ABCDEFGHI":
    p, e = results.get(s, 0), expect[s]
    total_p += p
    mark = "ok" if p == e else "SHORT"
    if p != e:
        ok = False
    print(f"  §{s}: {p}/{e}  {mark}")
print(f"TOTAL: {total_p}/155")
for pr in problems:
    print(pr)
    ok = False
if ok:
    print("VERDICT: MEETS-PROPOSED-BAR")
    sys.exit(0)
print("VERDICT: DOES-NOT-MEET")
sys.exit(1)
EOF
