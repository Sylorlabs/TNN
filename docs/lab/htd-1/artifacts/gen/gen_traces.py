#!/usr/bin/env python3
"""HTD-1 R3 — real deliberative-episode trace artifact.

Episode boundary rules (frozen, source-backed):
  DEBATE (wave8 debate.zag, wave10 debate_nr.zag):
    one episode = one session. The source emits TR_SESSION at the start of
    db_session() and TR_SESSION_DONE at its end; per-topic loops run INSIDE
    the session and there are NO per-topic start/end markers (TR_Q marks R3
    interrogation questions, not deliberation boundaries). Each session is one
    complete bounded deliberative run: fresh learners -> seeding -> multi-round
    debate (assert/discourse/world/verify/revise/concede) -> interrogation ->
    spectator verdicts -> done.
  DR (wave5/wave6 dr.zag dr_block_system):
    one episode = one block. The block is the bounded deliberative run:
    dr_block_system(&s,b,...) with per-block audit range [n0,n1) and a
    DR_CURVE summary record. Episode span = the DR_CURVE line's bytes.

Dedup: byte-identical reruns (_a/_b) and mirrored copies (run_* vs out_*)
are counted ONCE (first file in canonical order). wave5 dr_10x_a.log ==
wave6 dr_intact_a.log (sha256-identical): counted once.

Honest count: 13033 = 33 debate sessions (wave8 11 + wave10-A 11 + wave10-B 11)
+ 13000 DR blocks.
"""
import hashlib
import json
import os
import sys

ART = os.path.expanduser("~/workspace/htd-1/artifacts")
LAB = os.path.expanduser("~/workspace/tnn-lab")

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

episodes = []

def add(ep):
    ep["episode_id"] = "rt-%06d" % (len(episodes) + 1)
    episodes.append(ep)

# --- debate logs: (path, source_tag) ---------------------------------------
debate_logs = [
    ("wave8/debate/out_small_a.txt", "debate-wave8"),
    ("wave8/debate/out_scale_a.txt", "debate-wave8"),
    ("wave10/debate-norecord/run_A_small_a.txt", "debate-norecord-A"),
    ("wave10/debate-norecord/run_A_scale_a.txt", "debate-norecord-A"),
    ("wave10/debate-norecord/run_B_small_a.txt", "debate-norecord-B"),
    ("wave10/debate-norecord/run_B_scale_a.txt", "debate-norecord-B"),
]

for rel, stag in debate_logs:
    path = os.path.join(LAB, rel)
    data = open(path, "rb").read()
    lines = data.split(b"\n")
    offs = []
    o = 0
    for ln in lines:
        offs.append(o)
        o += len(ln) + 1
    sess_starts = [i for i, ln in enumerate(lines) if ln.startswith(b"TR_SESSION,")]
    sess_ends = [i for i, ln in enumerate(lines) if ln.startswith(b"TR_SESSION_DONE")]
    assert len(sess_starts) == len(sess_ends) == len(sess_starts), (rel,)
    for si, s0 in enumerate(sess_starts):
        s1 = sess_ends[si]
        start, end = offs[s0], offs[s1] + len(lines[s1]) + 1
        span = data[start:end]
        counts = {}
        for ln in lines[s0:s1 + 1]:
            tag = ln.split(b",")[0].decode("utf-8", "replace")
            if tag.startswith("TR_"):
                counts[tag] = counts.get(tag, 0) + 1
        hdr = lines[s0].decode("utf-8").split(",")
        add({
            "kind": "debate_session",
            "source": stag,
            "log_file": rel,
            "session_idx": int(hdr[1]),
            "session_tag": ",".join(hdr[2:]),
            "byte_start": start,
            "byte_end": end,
            "sha256": sha(span),
            "marker_counts": counts,
            "boundary_rule": "TR_SESSION .. TR_SESSION_DONE inclusive, half-open bytes",
        })

# --- DR logs: (path, source_tag) -------------------------------------------
dr_logs = [
    ("wave5/deliberative-refusal/evidence/dr_10x_a.log", "dr-wave5"),
    ("wave5/deliberative-refusal/evidence/dr_100x_a.log", "dr-wave5"),
    ("wave5/deliberative-refusal/evidence/dr_variant1_100x.log", "dr-wave5"),
    ("wave5/deliberative-refusal/evidence/dr_variant2_100x.log", "dr-wave5"),
    ("wave5/deliberative-refusal/evidence/dr_variant3_100x.log", "dr-wave5"),
    ("wave5/deliberative-refusal/evidence/dr_variant4_100x.log", "dr-wave5"),
    ("wave5/deliberative-refusal/evidence/dr_nc1_100x.log", "dr-wave5"),
    ("wave5/deliberative-refusal/evidence/dr_nc2_10x.log", "dr-wave5"),
    ("wave5/deliberative-refusal/evidence/dr_nc3_10x.log", "dr-wave5"),
    ("wave5/deliberative-refusal/evidence/dr_nc4_10x.log", "dr-wave5"),
    ("wave6/attribution-ablation/logs/dr_leg/dr_myopic_a.log", "dr-wave6-myopic"),
]
seen_hashes = set()
for rel, stag in dr_logs:
    path = os.path.join(LAB, rel)
    data = open(path, "rb").read()
    fh = sha(data)
    assert fh not in seen_hashes, ("duplicate DR run counted twice", rel)
    seen_hashes.add(fh)
    header = data.split(b"\n")[0].decode("utf-8")
    # header: DR_LEG,10x,blocks,200,variant,0
    hp = header.split(",")
    leg, nblocks, variant = hp[1], int(hp[3]), int(hp[5])
    lines = data.split(b"\n")
    offs = []
    o = 0
    for ln in lines:
        offs.append(o)
        o += len(ln) + 1
    n = 0
    for li, ln in enumerate(lines):
        if ln.startswith(b"DR_CURVE,"):
            f = ln.decode("utf-8").split(",")
            block = int(f[1])
            start, end = offs[li], offs[li] + len(ln)
            add({
                "kind": "dr_block",
                "source": stag,
                "log_file": rel,
                "leg": leg,
                "variant": variant,
                "block_idx": block,
                "byte_start": start,
                "byte_end": end,
                "sha256": sha(data[start:end]),
                "curve": {"hold_pm": int(f[2]), "takes": int(f[3]),
                          "s1": int(f[4]), "s2": int(f[5]),
                          "s3": int(f[6]), "s4": int(f[7]),
                          "net": int(f[8]), "thr": int(f[9])},
                "boundary_rule": "DR_CURVE block summary record, half-open bytes; block bounds audit range [n0,n1) per dr.zag dr_block_system",
            })
            n += 1
    assert n == nblocks, (rel, n, nblocks)

kinds = {}
for e in episodes:
    kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
print("episodes:", len(episodes), kinds, file=sys.stderr)
assert len(episodes) == 13033, len(episodes)

with open(os.path.join(ART, "real_traces.jsonl"), "w", encoding="utf-8") as f:
    for e in episodes:
        f.write(json.dumps(e) + "\n")
print("wrote real_traces.jsonl (13033)", file=sys.stderr)
