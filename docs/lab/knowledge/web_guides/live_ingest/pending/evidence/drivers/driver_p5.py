#!/usr/bin/env python3
"""P5 driver: CAP fill + memory budget + oldest-first shedding.

Uses ONE kbpend call with all CAP claims. Verifies:
- presented = stored + shed + resolved + refused
- shed set is exactly oldest unresolved seqs {1..k}
- every shed claim is ledgered in shed_ledger.txt
- knowledge.txt SHA unchanged
"""
import os, sys, hashlib, subprocess
sys.path.insert(0, os.path.expanduser("~/workspace/pending-run"))
from harness import *

set_passdir(sys.argv[1])

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def main():
    log("=== P5: capacity and shedding ===")
    sd = init_state("p5", hold=False)
    kb_sha_before = sha(os.path.join(sd, "knowledge.txt"))
    log(f"  knowledge.txt SHA before: {kb_sha_before[:16]}...")

    # Bulk kbpend of all CAP claims in chunks (file size limit per call)
    import glob
    chunk_files = sorted(glob.glob(os.path.expanduser("~/workspace/pending-run/cap_chunks/chunk_*")))
    ncap = 0
    for cf in chunk_files:
        ncap += sum(1 for _ in open(cf))
    log(f"  kbpend {ncap} CAP claims in {len(chunk_files)} chunks...")
    for idx, cf in enumerate(chunk_files):
        rc, out, err = run("kbpend", cf, sd)
        if rc != 0:
            log(f"  chunk {idx} rc={rc} out={out.strip()[:200]}")
            break
    log(f"  kbpend done rc={rc}")
    # Count HELD lines in output (last chunk)
    held_out = [l for l in out.split("\n") if l.startswith("PENDING|HELD|")]
    log(f"  HELD lines in last chunk output: {len(held_out)}")
    if rc != 0:
        log(f"  stderr: {err[:500]}")
        log(f"  stdout tail: {out[-500:]}")

    # Read state
    pend_lines = [l for l in open(os.path.join(sd, "pending.txt")) if l.startswith("PENDING|")]
    stored = len(pend_lines)
    shed_path = os.path.join(sd, "shed_ledger.txt")
    shed_lines = [l for l in open(shed_path) if l.strip()] if os.path.exists(shed_path) else []
    shed = len(shed_lines)
    # Parse shed seqs
    shed_seqs = []
    for l in shed_lines:
        # SHED|<seq>|<claim>|BATCH|<n>
        parts = l.split("|")
        if len(parts) >= 2 and parts[0] == "SHED":
            try:
                shed_seqs.append(int(parts[1]))
            except ValueError:
                pass
    shed_seqs.sort()

    res_path = os.path.join(sd, "resolutions.txt")
    res_lines = [l for l in open(res_path) if l.startswith("RESOLVE|")] if os.path.exists(res_path) else []
    resolved = len(res_lines)
    rej_path = os.path.join(sd, "rejections.txt")
    rej_lines = [l for l in open(rej_path) if l.startswith("REJ|")] if os.path.exists(rej_path) else []
    refused = len(rej_lines)

    log(f"  presented={ncap} stored={stored} shed={shed} resolved={resolved} refused={refused}")
    # Accounting: presented = stored + shed + resolved + refused
    # (resolved/refused are 0 here since we only pended; but check the identity)
    check("p5-accounting", ncap == stored + shed + resolved + refused,
          f"{ncap} == {stored}+{shed}+{resolved}+{refused}")

    # Shed set is exactly oldest {1..k}
    if shed > 0:
        expect = list(range(1, shed + 1))
        check("p5-oldest-first", shed_seqs == expect,
              f"shed seqs 1..{shed}, got 1..{shed_seqs[-1] if shed_seqs else 0}")
        # Every shed claim ledgered (we have the lines; verify count matches)
        check("p5-ledgered", len(shed_seqs) == shed,
              f"ledgered seqs={len(shed_seqs)} shed={shed}")
        # Stored seqs are the newest (no gaps, no reuse)
        stored_seqs = []
        for l in pend_lines:
            parts = l.split("|")
            if len(parts) >= 2:
                try:
                    stored_seqs.append(int(parts[1]))
                except ValueError:
                    pass
        stored_seqs.sort()
        # Stored should be {shed+1 .. ncap} (all newer than shed)
        expect_stored = list(range(shed + 1, ncap + 1))
        check("p5-no-reuse", stored_seqs == expect_stored,
              f"stored {len(stored_seqs)} seqs, expect {shed+1}..{ncap}")
    else:
        check("p5-shed-happened", False, "no shedding occurred; budget not exceeded?")

    # knowledge.txt unchanged
    kb_sha_after = sha(os.path.join(sd, "knowledge.txt"))
    check("p5-kb-unchanged", kb_sha_before == kb_sha_after,
          f"{kb_sha_before[:16]}... vs {kb_sha_after[:16]}...")

    # Budget respected: stored bytes <= budget
    init_log = open(os.path.join(sd, "pending_init.log")).read()
    budget = int([l.split("|")[1] for l in init_log.split("\n")
                  if l.startswith("PENDING_BUDGET_BYTES|")][0])
    stored_bytes = os.path.getsize(os.path.join(sd, "pending.txt"))
    check("p5-budget", stored_bytes <= budget,
          f"stored {stored_bytes} <= budget {budget}")
    log(f"  budget={budget} stored_bytes={stored_bytes}")

    save_checks("p5-")

if __name__ == "__main__":
    main()
