#!/usr/bin/env python3
"""P5 verification (reads existing state, no re-pend)."""
import os, sys, hashlib
sys.path.insert(0, os.path.expanduser("~/workspace/pending-run"))
from harness import *

import harness
harness.set_passdir("pass1")
from harness import log, check, save_checks
sd = os.path.join(harness.PASSDIR, "p5")

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

ncap = 333165
pend_lines = [l for l in open(os.path.join(sd, "pending.txt")) if l.startswith("PENDING|")]
stored = len(pend_lines)
shed_path = os.path.join(sd, "shed_ledger.txt")
shed_lines = [l for l in open(shed_path) if l.strip()] if os.path.exists(shed_path) else []
shed = len(shed_lines)
shed_seqs = []
for l in shed_lines:
    parts = l.split("|")
    if len(parts) >= 2 and parts[0] == "SHED":
        try: shed_seqs.append(int(parts[1]))
        except ValueError: pass
shed_seqs.sort()
res_path = os.path.join(sd, "resolutions.txt")
if os.path.exists(res_path):
    res_all = [l for l in open(res_path) if l.startswith("RESOLVE|")]
    # SHED resolutions are the shed ledger duplicate; exclude from "resolved"
    res_lines = [l for l in res_all if "|SHED|" not in l]
    shed_res = len(res_all) - len(res_lines)
else:
    res_lines = []; shed_res = 0
resolved = len(res_lines)
rej_path = os.path.join(sd, "rejections.txt")
refused = len([l for l in open(rej_path) if l.startswith("REJ|")]) if os.path.exists(rej_path) else 0

log(f"presented={ncap} stored={stored} shed={shed} resolved={resolved} refused={refused} (shed_res={shed_res})")
check("p5-accounting", ncap == stored + shed + resolved + refused,
      f"{ncap} == {stored}+{shed}+{resolved}+{refused}")
check("p5-shed-res-match", shed_res == shed, f"shed resolutions={shed_res} shed={shed}")
if shed > 0:
    expect = list(range(1, shed + 1))
    check("p5-oldest-first", shed_seqs == expect,
          f"shed 1..{shed}, got 1..{shed_seqs[-1] if shed_seqs else 0}")
    check("p5-ledgered", len(shed_seqs) == shed, f"{len(shed_seqs)}=={shed}")
    stored_seqs = []
    for l in pend_lines:
        parts = l.split("|")
        if len(parts) >= 2:
            try: stored_seqs.append(int(parts[1]))
            except ValueError: pass
    stored_seqs.sort()
    expect_stored = list(range(shed + 1, ncap + 1))
    check("p5-no-reuse", stored_seqs == expect_stored,
          f"stored {len(stored_seqs)}, expect {shed+1}..{ncap}")
else:
    check("p5-shed-happened", False, "no shedding")

kb_sha_after = sha(os.path.join(sd, "knowledge.txt"))
# knowledge.txt should have 12 KB lines (no installs during P5)
nkb = len([l for l in open(os.path.join(sd, "knowledge.txt")) if l.startswith("KB|")])
check("p5-kb-count", nkb == 12, f"KB lines={nkb}")
init_log = open(os.path.join(sd, "pending_init.log")).read()
budget = int([l.split("|")[1] for l in init_log.split("\n") if l.startswith("PENDING_BUDGET_BYTES|")][0])
stored_bytes = os.path.getsize(os.path.join(sd, "pending.txt"))
check("p5-budget", stored_bytes <= budget, f"{stored_bytes} <= {budget}")
log(f"budget={budget} stored_bytes={stored_bytes}")
save_checks("p5-")
