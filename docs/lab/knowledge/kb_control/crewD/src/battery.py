#!/usr/bin/env python3
"""Crew D silent-overwrite red-team battery.

Runs the frozen attack families (F1..F5 + validity GATE) against a kbctl
target binary, with the oracle checking K1..K4 after every attack.

Usage:
  battery.py <kbctl> <mode> <variant> <chunk_bytes> <rundir>
             [--legs GATE,F1,F2,F3,F4,F5] [--run N] [--genuine-n N]

Deterministic: no RNG, no wall clock in evidence. The canonical model is
updated only on rc=0 ops. Every op is chunk-snapshotted before/after and
checked against the universal append-only K1 rule.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fixtures import (keygen, textgen, bulk_tlen, record_sha,
                      simulate_layout, HDR_LEN)
from oracle import (Model, parse_verify, snapshot_chunks,
                    chunk_diff_violations, HashChain, sha_file)

TIMEOUT = 600
IG_MAX_TEXT = 4096  # target silently truncates longer texts; model mirrors it


def cap_text(data: bytes) -> bytes:
    return data[:IG_MAX_TEXT]


class Battery:
    def __init__(self, kbctl, mode, variant, chunk, rundir, run_idx,
                 genuine_n=0):
        self.kbctl = kbctl
        self.mode = mode
        self.variant = variant
        self.chunk = chunk
        self.rundir = rundir
        self.run_idx = run_idx
        self.genuine_n = genuine_n
        self.evdir = os.path.join(rundir, variant, "run%d" % run_idx)
        os.makedirs(self.evdir, exist_ok=True)
        self.store = os.path.join(self.evdir, "store")
        self.seq = 0
        self.model = Model()
        self.findings = []          # oracle verdicts
        self.ops = []               # op log (deterministic fields only)
        self.chain = None
        self.textdir = os.path.join(self.evdir, "texts")
        os.makedirs(self.textdir, exist_ok=True)
        self._textseq = 0

    # ------------------------------------------------------------ harness
    def run_op(self, args, expect_rc=None):
        """Run kbctl, log deterministically, return (rc, stdout)."""
        cmd = [self.kbctl] + args
        p = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=TIMEOUT)
        rc, out = p.returncode, p.stdout
        self.seq += 1
        # redact the run-specific directory so reruns are byte-identical
        rargv = [a.replace(self.evdir, "<R>") for a in args]
        self.ops.append({"seq": self.seq, "argv": rargv, "rc": rc,
                         "stdout": out,
                         "stdout_sha": hashlib.sha256(
                             out.encode()).hexdigest()})
        if expect_rc is not None and rc != expect_rc:
            self.findings.append({"seq": self.seq, "type": "unexpected_rc",
                                  "argv": rargv, "rc": rc,
                                  "expected": expect_rc})
        return rc, out

    def write_text(self, data: bytes) -> str:
        self._textseq += 1
        path = os.path.join(self.textdir, "t%04d.txt" % self._textseq)
        with open(path, "wb") as fh:
            fh.write(data)
        return path

    def snap(self):
        return snapshot_chunks(self.store)

    def check_k1(self, pre, post, label):
        viol = chunk_diff_violations(pre, post)
        if viol:
            self.findings.append({"seq": self.seq, "type": "K1_clobber",
                                  "label": label, "violations": viol})
        return viol

    def do_verify(self, label):
        rc, out = self.run_op(["verify", self.store])
        with open(os.path.join(self.evdir,
                               "verify_%04d.txt" % self.seq), "w") as fh:
            fh.write(out)
        slots, summary = parse_verify(out)
        # K2 / K3 from the summary
        if summary["offset_mismatches"]:
            self.findings.append({"seq": self.seq, "type": "K2_offset",
                                  "label": label,
                                  "count": summary["offset_mismatches"]})
        if summary["unreadable"]:
            self.findings.append({"seq": self.seq, "type": "K3_unreadable",
                                  "label": label,
                                  "count": summary["unreadable"]})
        if summary["chunk_corrupt"]:
            self.findings.append({"seq": self.seq, "type": "K1_chunk_corrupt",
                                  "label": label,
                                  "count": summary["chunk_corrupt"]})
        # per-slot content comparison against the model (readable slots)
        for fid in self.model.live_ids():
            if fid in slots:
                exp = self.model.expected_sha(fid)
                if slots[fid]["sha"] != exp:
                    self.findings.append(
                        {"seq": self.seq, "type": "K1_content",
                         "label": label, "id": fid,
                         "expected": exp, "got": slots[fid]["sha"]})
                f = self.model.facts[fid]
                if slots[fid]["keylen"] != len(f["key"]) or \
                   slots[fid]["textlen"] != len(f["text"]):
                    self.findings.append(
                        {"seq": self.seq, "type": "K1_len",
                         "label": label, "id": fid})
        return rc, slots, summary

    # ------------------------------------------------------------ setup
    def setup_bulkfill(self, n, maxtextlen):
        rc, _ = self.run_op(["bulkfill", self.store, str(n),
                             str(maxtextlen)], expect_rc=0)
        assert rc == 0, "bulkfill failed"
        for i in range(n):
            tlen = bulk_tlen(i, maxtextlen)
            self.model.put(i, keygen(i), textgen(i, 0, tlen))
        return n

    def setup_puts(self, n, maxtextlen):
        rc, _ = self.run_op(["init", self.store, "--mode=" + self.mode],
                            expect_rc=0)
        assert rc == 0, "init failed"
        for i in range(n):
            tlen = bulk_tlen(i, maxtextlen)
            key, text = keygen(i), textgen(i, 0, tlen)
            tp = self.write_text(text)
            pre = self.snap()
            rc, _ = self.run_op(["put", self.store, str(i), key.decode(),
                                 tp, "--mode=" + self.mode], expect_rc=0)
            assert rc == 0, "put %d failed" % i
            self.check_k1(pre, self.snap(), "setup_put_%d" % i)
            self.model.put(i, key, text)
        return n

    def fresh(self):
        shutil.rmtree(self.store, ignore_errors=True)
        self.model = Model()

    # ------------------------------------------------------------ ops
    def op_revise(self, fid, text, label):
        text = cap_text(text)
        tp = self.write_text(text)
        pre = self.snap()
        rc, _ = self.run_op(["revise", self.store, str(fid), tp,
                             "--mode=" + self.mode])
        viol = self.check_k1(pre, self.snap(), label)
        if rc == 0:
            self.model.revise(fid, text)
        return rc, viol

    def op_delete(self, fid, label):
        pre = self.snap()
        rc, _ = self.run_op(["delete", self.store, str(fid)])
        viol = self.check_k1(pre, self.snap(), label)
        if rc == 0:
            self.model.delete(fid)
        return rc, viol

    def op_put(self, fid, text, label, key=None):
        text = cap_text(text)
        key = key or keygen(fid)
        tp = self.write_text(text)
        pre = self.snap()
        rc, _ = self.run_op(["put", self.store, str(fid), key.decode(),
                             tp, "--mode=" + self.mode])
        viol = self.check_k1(pre, self.snap(), label)
        if rc == 0:
            self.model.put(fid, key, text)
        return rc, viol

    # ------------------------------------------------------------ legs
    def bulk_cfg(self):
        # (n, maxtextlen): enough facts for >=2 chunk rollovers.
        # At genuine scale the slot-table arena (48B/slot) and the 2^25
        # slice limit bound the fact count, so use larger (still
        # observed-range, <=467) texts to reach two rollovers.
        if self.chunk >= 1 << 20 and self.genuine_n:
            return self.genuine_n, 467
        maxtextlen = 100
        n = max(300, int(self.chunk * 2.2 / 70))
        return n, maxtextlen

    def bulk_n(self, maxtextlen):
        # enough facts for >=2 chunk rollovers at any chunk geometry
        n = max(300, int(self.chunk * 2.2 / 70))
        if self.chunk >= 1 << 20 and self.genuine_n:
            n = self.genuine_n
        return n

    def leg_GATE(self):
        """Battery-validity gate: reproduce the known G3 failure on T-FAST.

        bulkfill to >=2 rollovers, revise the pre-boundary fact of the first
        boundary. T-FAST must report revise rc=0 AND show chunk clobber
        (bytes changed inside live data). Otherwise the battery is VOID.
        """
        self.fresh()
        n, maxtextlen = self.bulk_cfg()
        self.setup_bulkfill(n, maxtextlen)
        recs, bounds = simulate_layout(n, self.chunk, maxtextlen)
        assert len(bounds) >= 2, "need >=2 rollovers for GATE"
        ch0, last0, tail0 = bounds[0]
        target = last0 - 1  # pre-boundary fact
        old = dict(self.snap())
        rc, out = self.run_op(["revise", self.store, str(target),
                               self.write_text(b"GATE-REVISED"),
                               "--mode=" + self.mode])
        viol = self.check_k1(old, self.snap(), "GATE_revise_pre_boundary")
        gate_ok = (rc == 0 and len(viol) > 0)
        self.findings.append({"seq": self.seq, "type": "GATE",
                              "target": target, "rc": rc,
                              "violations": len(viol),
                              "reproduced": gate_ok})
        if rc == 0:
            self.model.revise(target, b"GATE-REVISED")
        self.do_verify("GATE")
        return gate_ok

    def leg_F1(self):
        """Boundary / pre-boundary / last-slot revises."""
        self.fresh()
        n, maxtextlen = self.bulk_cfg()
        self.setup_bulkfill(n, maxtextlen)
        recs, bounds = simulate_layout(n, self.chunk, maxtextlen)
        for bi, (ch, last, tail) in enumerate(bounds[:4]):
            for fid, tag in ((last, "boundary"), (last - 1, "pre_boundary"),
                             (last + 1, "post_boundary")):
                if 0 <= fid < n:
                    self.op_revise(fid, b"F1-%s-b%d" % (tag.encode(), bi),
                                   "F1_%s_b%d" % (tag, bi))
        self.op_revise(n - 1, b"F1-last-slot", "F1_last_slot")
        self.do_verify("F1")

    def f2_find_n0(self, name, rel):
        """Find a filler count placing the chunk tail for the crafted
        record. Simulates once (O(n)) and scans for the first valid n0,
        identical to the incremental search."""
        keylen = 7
        max_reclen = HDR_LEN + keylen + IG_MAX_TEXT
        # single simulation pass, recording tail after each filler count
        tails = {}
        off = 0
        i = 0
        # upper bound: enough fillers to wrap the chunk several times
        limit = max(20000, int(self.chunk * 4 / 70) + 100)
        while i < limit:
            tlen = 1 + ((i * 7919 + 13) % 100)
            rl = HDR_LEN + keylen + tlen
            if off + rl > self.chunk:
                off = 0
            off += rl
            i += 1
            tails[i] = off
            if i >= 10:
                rem = self.chunk - off
                if rel == "span":
                    if 0 < rem < max_reclen:
                        return i
                else:
                    t = rem + rel - HDR_LEN - keylen
                    if 1 <= t <= IG_MAX_TEXT:
                        return i
        raise AssertionError((name, "no valid geometry"))

    def leg_F2(self):
        """Exact / +-1 / spanning boundary-size facts, then revise.

        The target caps text at IG_MAX_TEXT=4096 (model mirrors it), so the
        driver searches filler counts that place the chunk tail where the
        crafted record exactly fills (rel=0), misses by one (rel=-1), or is
        guaranteed to span (max-size record with <4114 bytes remaining).
        """
        keylen = 7
        for name, rel in (("exact", 0), ("minus1", -1), ("span", "span")):
            self.fresh()
            n0 = self.f2_find_n0(name, rel)
            # bulkfill for the fillers (in-process, fast); the crafted
            # boundary fact itself goes through the per-op put path.
            self.setup_bulkfill(n0, 100)
            recs, _ = simulate_layout(n0, self.chunk, 100)
            T = recs[-1]["inoff"] + recs[-1]["reclen"]
            fid = n0
            if rel == "span":
                self.op_put(fid, textgen(fid, 7, IG_MAX_TEXT),
                            "F2_%s_put" % name)
                target = n0 - 1  # last pre-rollover fact
            else:
                tlen = (self.chunk - T) + rel - HDR_LEN - keylen
                self.op_put(fid, textgen(fid, 7, tlen),
                            "F2_%s_put" % name)
                target = fid
            self.op_revise(target, b"F2-attack-" + name.encode(),
                           "F2_%s_revise" % name)
            self.do_verify("F2_" + name)

    def leg_F3(self):
        """Deterministic interleaved append+revise+delete schedule."""
        self.fresh()
        n0 = 120
        self.setup_puts(n0, 100)
        next_id = n0
        pattern = ["put", "put", "revise", "delete",
                   "revise", "put", "delete", "revise"]
        steps = 240
        for s in range(steps):
            op = pattern[s % len(pattern)]
            live = self.model.live_ids()
            if op == "put":
                fid = next_id
                next_id += 1
                tlen = 40 + ((s * 131 + 7) % 428)  # 40..467
                self.op_put(fid, textgen(fid, 3, tlen), "F3_put_%d" % s)
            elif op == "revise" and live:
                fid = live[(s * 37) % len(live)]
                tlen = 40 + ((s * 57 + 11) % 428)
                self.op_revise(fid, textgen(fid, 5, tlen), "F3_rev_%d" % s)
            elif op == "delete" and live:
                fid = live[(s * 23 + 5) % len(live)]
                self.op_delete(fid, "F3_del_%d" % s)
            if s % 40 == 39:
                self.do_verify("F3_step_%d" % s)
        self.do_verify("F3_final")

    def leg_F4(self):
        """Crash matrix: power loss at every write stage, then recover.

        Each (op, stage) runs in a FRESH store: a crashed op leaves an
        orphan record at the tail, and a subsequent op in the same store
        would benignly overwrite that dead orphan (no slot references it).
        Isolating stages keeps the K1 oracle free of orphan false
        positives; accumulation is covered by F1/F3.
        """
        # crashput stages
        for si, stage in enumerate(("data", "meta")):
            self.fresh()
            self.setup_puts(30, 100)
            fid = 100 + si
            tp = self.write_text(b"F4-crashput-" + stage.encode())
            pre = self.snap()
            rc, _ = self.run_op(["crashput", self.store, str(fid),
                                 keygen(fid).decode(), tp,
                                 "--mode=" + self.mode,
                                 "--fail-after=" + stage], expect_rc=99)
            self.check_k1(pre, self.snap(), "F4_crashput_" + stage)
            rc2, _ = self.run_op(["recover", self.store], expect_rc=0)
            # adopt observed state into the model (fail-closed either way)
            rc3, out3 = self.run_op(["get", self.store, str(fid)])
            if rc3 == 0:
                self.model.put(fid, keygen(fid),
                               b"F4-crashput-" + stage.encode())
            self.do_verify("F4_crashput_" + stage)
            self.check_k4_crash("crashput", stage, fid)
        # crashrevise stages
        for stage in ("data", "ovr", "meta"):
            self.fresh()
            self.setup_puts(30, 100)
            fid = 5
            newtext = b"F4-crashrevise-" + stage.encode()
            tp = self.write_text(newtext)
            pre = self.snap()
            rc, _ = self.run_op(["crashrevise", self.store, str(fid), tp,
                                 "--mode=" + self.mode,
                                 "--fail-after=" + stage], expect_rc=99)
            self.check_k1(pre, self.snap(), "F4_crashrevise_" + stage)
            rc2, _ = self.run_op(["recover", self.store], expect_rc=0)
            rc3, out3 = self.run_op(["get", self.store, str(fid)])
            if rc3 == 0 and out3.splitlines()[-1].encode() == newtext:
                self.model.revise(fid, newtext)
            self.do_verify("F4_crashrevise_" + stage)
            self.check_k4_crash("crashrevise", stage, fid)

    def check_k4_crash(self, op, stage, fid):
        """K4: after recover, the affected slot reads as full-old or
        full-new; no other live slot's content may have changed."""
        # other-slot stability is covered by check_k1 + do_verify model
        # comparison; here we record the observed outcome class.
        rc, out = self.run_op(["get", self.store, str(fid)])
        self.findings.append({"seq": self.seq, "type": "K4_crash_outcome",
                              "op": op, "stage": stage, "id": fid,
                              "get_rc": rc})

    def leg_F5(self):
        """Padding geometry across the observed 40..467-byte fact range."""
        self.fresh()
        rc, _ = self.run_op(["init", self.store, "--mode=" + self.mode],
                            expect_rc=0)
        assert rc == 0
        tlens = [40, 467]
        t = 41
        while t < 467:
            tlens.append(t)
            t += 13
        fid = 0
        for tlen in sorted(set(tlens)):
            self.op_put(fid, textgen(fid, 9, tlen), "F5_tlen_%d" % tlen)
            fid += 1
        self.do_verify("F5")

    # ------------------------------------------------------------ run
    def run(self, legs):
        seed = ("CREWD-BATTERY-v1|" + self.kbctl + "|" + self.mode + "|"
                + self.variant + "|" + str(self.chunk)).encode()
        self.chain = HashChain(seed)
        results = {}
        for leg in legs:
            leg_start_findings = len(self.findings)
            fn = getattr(self, "leg_" + leg)
            ret = fn()
            # chain over the leg's evidence
            ev = b""
            for root, _, files in os.walk(self.evdir):
                for fnm in sorted(files):
                    p = os.path.join(root, fnm)
                    ev += fnm.encode() + b":" + sha_file(p).encode() + b"\n"
            st = self.chain.step(leg, ev)
            results[leg] = {"chain": st,
                            "findings": len(self.findings) - leg_start_findings,
                            "returned": ret}
        with open(os.path.join(self.evdir, "ops.jsonl"), "w") as fh:
            for o in self.ops:
                fh.write(json.dumps(o, sort_keys=True) + "\n")
        with open(os.path.join(self.evdir, "findings.json"), "w") as fh:
            json.dump(self.findings, fh, indent=1, sort_keys=True)
        # directory manifest (O6)
        man = []
        for root, _, files in os.walk(self.evdir):
            for fnm in sorted(files):
                p = os.path.join(root, fnm)
                man.append((os.path.relpath(p, self.evdir), sha_file(p)))
        with open(os.path.join(self.evdir, "manifest.txt"), "w") as fh:
            for rel, sha in sorted(man):
                fh.write("%s  %s\n" % (sha, rel))
        with open(os.path.join(self.evdir, "CHAIN.txt"), "w") as fh:
            fh.write("final_chain %s\n" % self.chain.state)
            for leg in legs:
                fh.write("%s %s\n" % (leg, results[leg]["chain"]))
        with open(os.path.join(self.evdir, "results.json"), "w") as fh:
            json.dump(results, fh, indent=1, sort_keys=True)
        return results


def main():
    kbctl, mode, variant, chunk = sys.argv[1:5]
    rundir = sys.argv[5]
    legs = ["GATE", "F1", "F2", "F3", "F4", "F5"]
    run_idx = 0
    genuine_n = 0
    i = 6
    while i < len(sys.argv):
        if sys.argv[i] == "--legs":
            legs = sys.argv[i + 1].split(",")
            i += 2
        elif sys.argv[i] == "--run":
            run_idx = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--genuine-n":
            genuine_n = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1
    b = Battery(kbctl, mode, variant, int(chunk), rundir, run_idx,
                genuine_n=genuine_n)
    results = b.run(legs)
    print(json.dumps(results, indent=1, sort_keys=True))
    # exit code: 0 if no K-findings, 1 if any K1..K4 fired, 2 if VOID
    kills = [f for f in b.findings
             if f["type"].startswith("K1") or f["type"].startswith("K2")
             or f["type"].startswith("K3") or f["type"].startswith("K4")]
    gate = [f for f in b.findings if f["type"] == "GATE"]
    if gate and not gate[0]["reproduced"] and mode == "fast":
        print("BATTERY VOID: gate did not reproduce the known failure")
        return 2
    if kills:
        print("KILL: %d kill-bar findings" % len(kills))
        return 1
    print("PASS: no kill-bar findings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
