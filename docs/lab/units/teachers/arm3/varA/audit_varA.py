#!/usr/bin/env python3
"""audit_varA.py — independent auditor for arm-3 varA teacher tapes.

Re-implements from the frozen spec (not from teacher.zag):
  * TST-1 framing, sha256 tape chain, footer binding
  * §P wire decode (magic/version/counts/checksum) + iron field validation
  * TEACHER_MSG / STUDENT_DECISION pairing and seq monotonicity
  * decision stream == script D lines
  * independent cumulative §C tripwire replay (conservative variant)
  * stdout VARA_PROP lines == tape TEACHER_MSG contents

Usage: audit_varA.py <tape> <script> <stim_len> <stdout_file> [--expect-ok|--expect-halt CODE]
Exit 0 iff every check passes.
"""
import struct
import sys
import hashlib

FNV_OFFSET = 14695981039346656037
FNV_PRIME = 1099511628211
M64 = 0xFFFFFFFFFFFFFFFF


def fnv1a64(data):
    h = FNV_OFFSET
    for b in data:
        h ^= b
        h = (h * FNV_PRIME) & M64
    return h


def parse_tape(path):
    data = open(path, "rb").read()
    off = 0
    events = []
    while off + 5 <= len(data):
        etype = data[off]
        plen = struct.unpack_from("<I", data, off + 1)[0]
        payload = data[off + 5:off + 5 + plen]
        if len(payload) != plen:
            raise ValueError("truncated event at offset %d" % off)
        events.append((etype, payload))
        off += 5 + plen
    if off != len(data):
        raise ValueError("trailing bytes after last event")
    return events


def check(cond, msg, fails):
    if not cond:
        fails.append(msg)
        print("AUDIT_FAIL," + msg)


def decode_wire(w):
    """Returns dict or raises."""
    if len(w) < 54:
        raise ValueError("wire too short")
    if struct.unpack_from("<I", w, 0)[0] != 0x54505250:
        raise ValueError("bad magic")
    if struct.unpack_from("<H", w, 4)[0] != 1:
        raise ValueError("bad version")
    ac = w[43]
    go = 44 + ac * 16
    if len(w) < go + 1:
        raise ValueError("wire truncated at ground count")
    gc = w[go]
    if ac > 8 or gc > 8:
        raise ValueError("counts exceed 8")
    want = 54 + ac * 16 + gc * 16
    if len(w) != want:
        raise ValueError("wire length mismatch")
    co = go + 1 + gc * 16
    if fnv1a64(w[:co + 1]) != struct.unpack_from("<Q", w, co + 1)[0]:
        raise ValueError("checksum mismatch")
    aux = []
    for i in range(ac):
        s, e = struct.unpack_from("<QQ", w, 44 + i * 16)
        aux.append((s, e))
    ground = []
    for i in range(gc):
        s, e = struct.unpack_from("<QQ", w, go + 1 + i * 16)
        ground.append((s, e))
    return {
        "teacher_id": struct.unpack_from("<I", w, 6)[0],
        "session_id": struct.unpack_from("<Q", w, 10)[0],
        "seq": struct.unpack_from("<Q", w, 18)[0],
        "kind": w[26],
        "span": (struct.unpack_from("<Q", w, 27)[0],
                 struct.unpack_from("<Q", w, 35)[0]),
        "conf": w[co],
        "aux": aux,
        "ground": ground,
    }


def parse_script_dlines(path):
    d = []
    for line in open(path):
        line = line.strip()
        if line.startswith("D "):
            t = line.split()
            d.append((int(t[1]), t[2], t[3:]))
    return d


def main():
    tape_path, script_path = sys.argv[1], sys.argv[2]
    stim_len = int(sys.argv[3])
    stdout_path = sys.argv[4]
    expect = sys.argv[5] if len(sys.argv) > 5 else "--expect-ok"
    expect_code = int(sys.argv[6]) if len(sys.argv) > 6 else None
    fails = []

    events = parse_tape(tape_path)
    check(len(events) >= 2, "tape has <2 events", fails)
    check(events[-1][0] == 9, "last event is not TAPE_FOOTER", fails)

    # --- chain verification (independent sha256) ---
    chain = bytes(32)
    for etype, payload in events[:-1]:
        link = chain + bytes([etype]) + struct.pack("<I", len(payload)) + payload
        chain = hashlib.sha256(link).digest()
    fp = events[-1][1]
    fcount = struct.unpack_from("<Q", fp, 8 + 32)[0]
    vlen = struct.unpack_from("<I", fp, 8 + 32 + 8)[0]
    verdict = fp[8 + 32 + 8 + 4:8 + 32 + 8 + 4 + vlen].decode()
    check(fp[8:8 + 32] == chain, "footer chain mismatch", fails)
    check(fcount == len(events) - 1, "footer event_count mismatch", fails)

    # --- early-exit tapes: [INTEGRITY, FOOTER] only, no header/stimulus ---
    # (script rejected before any session state existed; still logged, still
    # chained, still zero TEACHER_MSG)
    if events[0][0] == 7 and len(events) == 2 and events[-1][0] == 9:
        icode = struct.unpack_from("<i", events[0][1], 0)[0]
        check(expect == "--expect-halt", "early-exit tape but expected ok", fails)
        check(icode == expect_code, "early-exit INTEGRITY code %d != %d" % (icode, expect_code), fails)
        check(verdict.startswith("HALTED"), "early-exit footer verdict not HALTED: %s" % verdict, fails)
        nprop = sum(1 for line in open(stdout_path) if line.startswith("VARA_PROP,"))
        check(nprop == 0, "early-exit stdout has %d VARA_PROP" % nprop, fails)
        print("AUDIT %s: %s" % ("PASS" if not fails else "FAIL", "; ".join(fails) if fails else "early-exit ok"))
        sys.exit(1 if fails else 0)
    check(len(events) >= 3, "tape has <3 events", fails)

    # --- header / stimulus ---
    hp = events[0][1]
    check(events[0][0] == 1, "first event not TAPE_HEADER", fails)
    check(hp[:4] == b"TST1", "header magic", fails)
    sid = struct.unpack_from("<Q", hp, 6)[0]
    arm = struct.unpack_from("<I", hp, 14)[0]
    check(arm == 3, "header arm_id != 3", fails)
    descr = hp[58:58 + struct.unpack_from("<I", hp, 54)[0]].decode()
    check(descr.startswith("arm3-varA"), "header descriptor", fails)
    check(events[1][0] == 2, "second event not STIMULUS_REF", fails)
    sp = events[1][1]
    check(struct.unpack_from("<Q", sp, 8)[0] == 0, "stimulus r0", fails)
    check(struct.unpack_from("<Q", sp, 16)[0] == stim_len, "stimulus r1 != stim_len", fails)

    # --- proposal / decision pairing ---
    tmsgs = []   # (event_idx, wire_dict)
    decs = []    # (event_idx, dict)
    integrities = []
    turns = 0
    for idx, (etype, payload) in enumerate(events):
        if etype == 3:
            try:
                tmsgs.append((idx, decode_wire(payload)))
            except ValueError as e:
                check(False, "TEACHER_MSG %d undecodable: %s" % (len(tmsgs), e), fails)
        elif etype == 12:
            ps, v = struct.unpack_from("<Q", payload, 0)[0], payload[8]
            rsn = struct.unpack_from("<H", payload, 9)[0]
            rs, re = struct.unpack_from("<QQ", payload, 11)
            decs.append((idx, {"seq": ps, "verdict": v, "reason": rsn, "rs": rs, "re": re}))
        elif etype == 7:
            integrities.append(struct.unpack_from("<I", payload, 0)[0])
        elif etype == 8:
            turns += 1

    n_prop = len(tmsgs)
    # seqs strictly 0..n-1 in tape order
    for i, (idx, wmsg) in enumerate(tmsgs):
        check(wmsg["seq"] == i, "proposal seq not monotonic at %d" % i, fails)
        check(wmsg["teacher_id"] == 3, "proposal teacher_id", fails)
        check(wmsg["session_id"] == sid, "proposal session_id", fails)
        check(1 <= wmsg["kind"] <= 5, "proposal kind range", fails)
        s, e = wmsg["span"]
        check(0 <= s < e <= stim_len, "proposal span range %d,%d" % (s, e), fails)
        check(1 <= wmsg["conf"] <= 254, "proposal conf not selective (got %d)" % wmsg["conf"], fails)
        for (a, b) in wmsg["aux"] + wmsg["ground"]:
            check(0 <= a < b <= stim_len, "aux/ground span range", fails)

    # pairing: every proposal except possibly the last has its decision next...
    # exact rule: decisions appear in order, each right after its proposal
    # except the final proposal may be undecided (exhaustion) — but in our
    # authored scripts every emission is decided, so require exact pairing.
    # pairing: every proposal has its decision immediately after it, except that
    # in halt mode the final (triggering) proposal may be undecided.
    allow_undecided_tail = expect != "--expect-ok"
    check(len(decs) == n_prop or (allow_undecided_tail and len(decs) == n_prop - 1),
          "decision count %d != proposal count %d" % (len(decs), n_prop), fails)
    di = 0
    for i, (idx, wmsg) in enumerate(tmsgs):
        if di < len(decs) and decs[di][0] == idx + 1 and decs[di][1]["seq"] == i:
            d = decs[di][1]
            check(1 <= d["verdict"] <= 4, "decision verdict range", fails)
            if d["verdict"] == 2:
                check(d["reason"] in (1, 2, 3, 4, 5), "revise reason range", fails)
                check(0 <= d["rs"] < d["re"] <= stim_len, "revise span", fails)
            elif d["verdict"] == 3:
                check(1 <= d["reason"] <= 6, "reject reason range", fails)
                check(d["rs"] == 0 and d["re"] == 0, "reject has rev span", fails)
            else:
                check(d["reason"] == 0, "adopt/defer reason nonzero", fails)
                check(d["rs"] == 0 and d["re"] == 0, "adopt/defer has rev span", fails)
            di += 1
        else:
            if allow_undecided_tail and i == n_prop - 1 and di == len(decs):
                continue  # halted on the triggering proposal before its decision
            check(False, "proposal %d not immediately followed by its decision" % i, fails)
    # no decision may reference a nonexistent proposal
    for _, d in decs:
        check(0 <= d["seq"] < n_prop, "decision references missing proposal", fails)

    # --- decisions == script D lines (prefix in halt mode: trailing/seq-bad
    # D lines are never consumed, so the tape holds only the consumed prefix)
    script_d = parse_script_dlines(script_path)
    if expect == "--expect-ok":
        check(len(script_d) == len(decs), "script D count %d != tape decisions %d" % (len(script_d), len(decs)), fails)
    else:
        check(len(script_d) >= len(decs), "script D count %d < tape decisions %d" % (len(script_d), len(decs)), fails)
    vmap = {"ADOPT": 1, "REVISE": 2, "REJECT": 3, "DEFER": 4}
    for (sseq, sv, srest), (_, d) in zip(script_d, decs):
        check(sseq == d["seq"] and vmap[sv] == d["verdict"], "script/tape decision mismatch at seq %d" % sseq, fails)
        if sv == "REVISE":
            check(int(srest[0]) == d["reason"] and int(srest[1]) == d["rs"] and int(srest[2]) == d["re"],
                  "script/tape revise fields at seq %d" % sseq, fails)
        elif sv == "REJECT":
            check(int(srest[0]) == d["reason"], "script/tape reject reason at seq %d" % sseq, fails)

    # --- stdout VARA_PROP lines match tape ---
    stdout_props = []
    for line in open(stdout_path):
        line = line.strip()
        if line.startswith("VARA_PROP,"):
            t = line.split(",")
            stdout_props.append((int(t[1]), int(t[2]), int(t[3]), int(t[4]), int(t[5])))
    check(len(stdout_props) == n_prop, "stdout proposal count", fails)
    for (sq, k, s, e, c), (idx, wmsg) in zip(stdout_props, tmsgs):
        check((sq, k, s, e, c) == (wmsg["seq"], wmsg["kind"], wmsg["span"][0], wmsg["span"][1], wmsg["conf"]),
              "stdout/tape proposal mismatch at seq %d" % sq, fails)

    # --- independent cumulative §C tripwire replay (conservative variant) ---
    # Mirrors tw_propose/tw_decide/tw_fire1: per proposal, update hi/coverage,
    # check dump leg (code 2) then smuggle leg (code 1); per decision, update
    # dec/acc and recheck the smuggle leg.
    def smuggle_leg(cov, nd, na, nh):
        return (stim_len > 0 and cov * 100 >= stim_len * 95 and nd > 0
                and na * 100 >= nd * 95 and nh * 100 >= nd * 90)

    covered = []  # merged intervals, cumulative
    cov_n = 0
    n_dec = n_acc = n_hi = 0
    fired = None
    for i, (idx, wmsg) in enumerate(tmsgs):
        s, e = wmsg["span"]
        if wmsg["conf"] == 255:
            n_hi += 1
        covered.append((s, e))
        covered.sort()
        merged = []
        for a, b in covered:
            if merged and a <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], b))
            else:
                merged.append((a, b))
        covered = merged
        cov_n = sum(b - a for a, b in covered)
        if wmsg["conf"] == 255 and (e - s) * 100 > stim_len * 5:
            fired = ("dump", i)
            break
        if smuggle_leg(cov_n, n_dec, n_acc, n_hi):
            fired = ("smuggle", i)
            break
        if i < len(decs):
            d = decs[i][1]
            n_dec += 1
            if d["verdict"] == 1:
                n_acc += 1
            if smuggle_leg(cov_n, n_dec, n_acc, n_hi):
                fired = ("smuggle", i)
                break
    if expect == "--expect-ok":
        check(fired is None, "tripwire replay fired: %s" % (fired,), fails)
        check(len(integrities) == 0, "INTEGRITY events on clean run: %s" % integrities, fails)
        check(verdict == "OK", "footer verdict not OK: %s" % verdict, fails)
    else:
        check(len(integrities) == 1, "expected exactly 1 INTEGRITY, got %d" % len(integrities), fails)
        check(integrities and integrities[0] == expect_code, "INTEGRITY code %s != %s" % (integrities, expect_code), fails)
        check(verdict.startswith("HALTED"), "footer verdict not HALTED: %s" % verdict, fails)
        # the independent replay must fire on the same leg the teacher reported
        # (only for tripwire codes 1/2; script-error halts have no §C leg)
        if expect_code in (1, 2):
            want_leg = {1: "smuggle", 2: "dump"}.get(expect_code)
            check(fired is not None and fired[0] == want_leg,
                  "replay leg %s != teacher code %s" % (fired, expect_code), fails)

    # proposal sequence digest (for history-sensitivity comparison)
    seq = [(w["seq"], w["kind"], w["span"][0], w["span"][1], w["conf"],
            tuple(w["aux"]), tuple(w["ground"])) for _, w in tmsgs]
    print("AUDIT_OK" if not fails else "AUDIT_FAIL")
    print("AUDIT_PROPOSALS,%d" % n_prop)
    print("AUDIT_DECISIONS,%d" % len(decs))
    print("AUDIT_VERDICT,%s" % verdict)
    import json
    print("AUDIT_SEQ," + json.dumps(seq))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
