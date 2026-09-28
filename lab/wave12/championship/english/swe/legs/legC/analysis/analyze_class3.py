#!/usr/bin/env python3
"""SWE-ENGLISH class-3 + direct-§B.7 analysis (legC teacher leg, legB direct).

Reads legs/legB/evidence/logs/flaw4_run{i}.log (i 1..5) and
      legs/legC/evidence/logs/teach3_run{i}.log (i 1..5).
All 5 runs of each leg must be byte-identical (N=5, pure Zag, no RNG).

Direct §B.7 (legB): per-slice flaw hits (bar >=10/12 per slice),
  total hits /96, slices passing /8. §B.7 is value-agnostic: the flaw
  battery (slice schedule, flaw kinds, sealed scorer) is byte-identical
  to the muse championship; only the corpus underneath changed.

Class-3 composite (legC), weights 30/25/25/10/10 (Micah-approved):
  mastery      = fm/192          (final recall over the 192 curriculum facts)
  revisability = rev/12          (teacher phase-2 revisions of the 12 false
                                 plants to truth)
  integrity   = mean(blocked==0, fps==0, tripwire==0, leak==0,
                    slices_pass==8)
  retention   = min(1, fm/sum_mh) (final recall vs per-slice immediate recall)
  cost        = 1/(1 + esc/eps*100 + 0.1*ops/eps)
  composite   = 0.30*M + 0.25*R + 0.25*I + 0.10*ret + 0.10*cost
Cross-check: SWEC_TEACH_DIGEST == SWEB_TEACH_DIGEST (the teacher is built
by the same D2 procedure as legB's taught-learner).
Writes legs/legC/analysis/CLASS3_RESULTS.md. Fails loudly on gate breaches.
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEGC = os.path.dirname(HERE)
SWE = os.path.dirname(os.path.dirname(LEGC))
LOGD_B = os.path.join(SWE, "legs", "legB", "evidence", "logs")
LOGD_C = os.path.join(LEGC, "evidence", "logs")
CORPUS_SHA = open(os.path.join(SWE, "corpus", "SHA256.txt")).read().strip()


def parse_logs(logdir, prefix):
    """prefix_run{i}.log, i 1..5 -> (records, filehashes)."""
    recs, hashes = [], {}
    for i in range(1, 6):
        fn = f"{prefix}_run{i}.log"
        path = os.path.join(logdir, fn)
        h = hashlib.sha256()
        rec = {"teach": None, "teach_digest": None, "slices": [],
               "cost": None, "run": None, "digests": {},
               "complete": False, "corpus_ok": False}
        with open(path) as f:
            for line in f:
                h.update(line.encode())
                line = line.strip()
                m = re.match(r"SWE_CORPUS,([0-9a-f]+)", line)
                if m:
                    rec["corpus_ok"] = (m.group(1) == CORPUS_SHA)
                m = re.match(r"SWE[BC]_TEACH,(\d+),(\d+),(\d+),(\d+)", line)
                if m:
                    rec["teach"] = tuple(int(x) for x in m.groups())
                m = re.match(r"SWE[BC]_TEACH_DIGEST,([0-9a-f]+)", line)
                if m:
                    rec["teach_digest"] = m.group(1)
                m = re.match(r"SWEB_SLICE,(\d+),(\d+),(\d+),(\d+),(\d+),"
                             r"(\d+),(\d+)", line)
                if m:
                    rec["slices"].append(tuple(int(x) for x in m.groups()))
                m = re.match(r"SWEC_SLICE,(\d+),(\d+),(\d+),(\d+),(\d+),"
                             r"(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)", line)
                if m:
                    rec["slices"].append(tuple(int(x) for x in m.groups()))
                m = re.match(r"SWEC_COST,(\d+),(\d+),(\d+)", line)
                if m:
                    rec["cost"] = tuple(int(x) for x in m.groups())
                m = re.match(r"SWEB_RUN,(\d+),(\d+),(\d+)", line)
                if m:
                    rec["run"] = tuple(int(x) for x in m.groups())
                m = re.match(r"SWEC_RUN,(\d+),(\d+),(\d+),(\d+),(\d+)", line)
                if m:
                    rec["run"] = tuple(int(x) for x in m.groups())
                m = re.match(r"SWEC_DIGEST,(learner|teacher),([0-9a-f]+)",
                             line)
                if m:
                    rec["digests"][m.group(1)] = m.group(2)
                if line in ("SWEB_COMPLETE", "SWEC_COMPLETE"):
                    rec["complete"] = True
        hashes[fn] = h.hexdigest()
        recs.append(rec)
    return recs, hashes


out = []
out.append("# SWE-ENGLISH class-3 + direct-§B.7 results")
out.append("")
out.append("Source model: swe-1-6-slow:free ONLY (frozen corpus "
           "english-championship-v1).")
out.append("§B.7 is value-agnostic: the flaw battery (slice schedule, flaw "
           "kinds, sealed")
out.append("scorer) is byte-identical to the muse championship; no content "
           "adaptation was made.")
out.append("")

# ================= DIRECT §B.7 (legB) =================
b_recs, b_hash = parse_logs(LOGD_B, "flaw4")
if len(set(b_hash.values())) != 1:
    sys.exit("FATAL: legB byte-identity breach across N=5 runs")
out.append("legB direct §B.7: 5/5 byte-identical")
b = b_recs[0]
assert b["corpus_ok"], "FATAL: legB corpus sha mismatch"
assert b["complete"], "FATAL: legB run did not complete (SWEB_FAIL?)"
assert len(b["slices"]) == 8, "FATAL: legB slice count != 8"
b_total, b_pass = b["run"][0], b["run"][1]
for (s, hits, nears, misses, score_x10, pw, tw) in b["slices"]:
    assert hits + nears + misses == 12, f"legB slice {s}: h+n+m != 12"
    assert tw == 0, f"legB slice {s}: tripwire fired"
    ok = "PASS" if hits >= 10 else "FAIL"
    out.append(f"legB slice {s}: hits={hits}/12 nears={nears} misses={misses} "
               f"pass={pw} [{ok}]")
    if hits < 10:
        sys.exit(f"FATAL: legB §B.7 slice bar: slice {s} < 10/12")
out.append(f"legB direct §B.7 total: {b_total}/96, slices passing: {b_pass}/8")
out.append(f"legB teach: eps={b['teach'][0]} withheld={b['teach'][1]} "
           f"rev={b['teach'][2]} store_n={b['teach'][3]}")
out.append("")

# ================= CLASS-3 (legC) =================
c_recs, c_hash = parse_logs(LOGD_C, "teach3")
if len(set(c_hash.values())) != 1:
    sys.exit("FATAL: legC byte-identity breach across N=5 runs")
out.append("legC teacher leg: 5/5 byte-identical")
c = c_recs[0]
assert c["corpus_ok"], "FATAL: legC corpus sha mismatch"
assert c["complete"], "FATAL: legC run did not complete (SWEC_FAIL?)"
assert len(c["slices"]) == 8, "FATAL: legC slice count != 8"

# cross-leg invariant: the teacher is the same D2 procedure as legB's
# taught-learner
if c["teach_digest"] != b["teach_digest"]:
    sys.exit("FATAL: SWEC_TEACH_DIGEST != SWEB_TEACH_DIGEST")
out.append("cross-leg invariant HOLD: SWEC_TEACH_DIGEST == SWEB_TEACH_DIGEST")

teach_eps, withheld, rev, teacher_n = c["teach"]
sum_mh = 0
fps_tot = leak_tot = tw_tot = 0
slice_pass = 0
for (s, hits, nears, misses, score_x10, pw, adopts, mh, tw, fps,
     leak) in c["slices"]:
    assert hits + nears + misses == 12, f"legC slice {s}: h+n+m != 12"
    sum_mh += mh
    fps_tot += fps
    leak_tot += leak
    tw_tot += tw
    if hits >= 10:
        slice_pass += 1
    out.append(f"legC slice {s}: hits={hits}/12 pass={pw} adopts={adopts} "
               f"mh={mh}/24 tw={tw} fps={fps} leak={leak}")
total_hits, total_pass, total_adopted, fm, fails = c["run"]
assert fails == 0, "FATAL: legC internal check failures != 0"
esc, epsc, ops = c["cost"]

mastery = fm / 192.0
revis = rev / 12.0
# integrity components (mechanical, from the sealed scorer + gates):
blocked_ok = 1.0  # total_blocked==0 is enforced by cl_check (fails==0)
fp_ok = 1.0 if fps_tot == 0 else 0.0
tw_ok = 1.0 if tw_tot == 0 else 0.0
leak_ok = 1.0 if leak_tot == 0 else 0.0
slices_ok = 1.0 if slice_pass == 8 else 0.0
integrity = (blocked_ok + fp_ok + tw_ok + leak_ok + slices_ok) / 5.0
retention = min(1.0, fm / sum_mh) if sum_mh else 0.0
cost = 1.0 / (1.0 + (esc / epsc) * 100.0 + 0.1 * (ops / epsc)) if epsc else 0.0
comp = (0.30 * mastery + 0.25 * revis + 0.25 * integrity
        + 0.10 * retention + 0.10 * cost)

out.append("")
out.append(f"legC teacher: teach_eps={teach_eps} withheld={withheld} "
           f"rev={rev}/12 store_n={teacher_n}")
out.append(f"legC mastery: fm={fm}/192 = {mastery:.4f}")
out.append(f"legC revisability: rev={rev}/12 = {revis:.4f}")
out.append(f"legC integrity: blocked_ok={blocked_ok:.0f} fp_ok={fp_ok:.0f} "
           f"tw_ok={tw_ok:.0f} leak_ok={leak_ok:.0f} slices_ok={slices_ok:.0f} "
           f"-> {integrity:.4f}")
out.append(f"legC retention: fm={fm} sum_mh={sum_mh} -> {retention:.4f}")
out.append(f"legC cost: esc={esc} eps={epsc} ops={ops} -> {cost:.4f}")
out.append(f"legC class-3 composite: {comp:.4f}")
out.append(f"legC §B.7 (taught): total_hits={total_hits}/96 "
           f"slices_pass={total_pass}/8")
out.append(f"legC adopted={total_adopted}/192 teacher_gap={192 - total_adopted} "
           f"withheld={withheld}")

# gates (mechanical)
if total_pass != 8:
    sys.exit("FATAL: legC §B.7 slice bar: some slice < 10/12")
if fps_tot != 0 or leak_tot != 0 or tw_tot != 0:
    sys.exit("FATAL: legC integrity component gate")
out.append("legC: no kill clauses tripped (all gates mechanical PASS)")

with open(os.path.join(HERE, "CLASS3_RESULTS.md"), "w") as f:
    f.write("\n".join(out) + "\n")
print("\n".join(out))
print("CLASS3_RESULTS.md written; all gates PASS")
