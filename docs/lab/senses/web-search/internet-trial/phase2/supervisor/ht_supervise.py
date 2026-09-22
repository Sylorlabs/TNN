#!/usr/bin/env python3
"""
ht_supervise.py — Phase-2 session supervisor (TRANSPORT + LEDGER ONLY).

All epistemic decisions are in the Zag binaries (ht_next_bin, ht_decide_bin).
This script owns: transport (live fetch), the hash-chained event ledger,
session state files, helper invocation plumbing, and replay verification.

Usage:
  ht_supervise.py init <session_dir> <arm>      # arm: solo | helper
  ht_supervise.py step <session_dir>           # one deliberation step
  ht_supervise.py run <session_dir> [max]      # loop until DONE
  ht_supervise.py consult <session_dir> <seq>  # ingest recorded helper response (helper arm)
  ht_supervise.py replay <session_dir> <n>    # N deterministic replays, check byte-identical
"""
import json, os, sys, subprocess, hashlib, datetime

WORK = os.path.expanduser("~/workspace/ht_p2_work")
LAB = os.path.expanduser("~/workspace/tnn-lab")
BUILD = os.path.join(WORK, "build")
HT_NEXT = os.path.join(BUILD, "ht_next_bin")
HT_DECIDE = os.path.join(BUILD, "ht_decide_bin")
TRANSPORT = os.path.join(LAB, "senses/web-search/v2/transport")
sys.path.insert(0, TRANSPORT)
import ws_bridge2 as bridge

def esc(s):
    return str(s).replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")

def run_bin(path, stdin_text):
    p = subprocess.run([path], input=stdin_text, capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        raise RuntimeError(f"{path} failed rc={p.returncode}\nSTDOUT:{p.stdout[-3000:]}\nSTDERR:{p.stderr[-3000:]}")
    return p.stdout

# ---------- ledger ----------
def ledger_append(sess, etype, fields):
    """Append a hash-chained event. fields: list of (k,v). Returns the event line."""
    log_path = os.path.join(sess, "session.htsv")
    prev = "0" * 64
    seq = 0
    if os.path.exists(log_path):
        with open(log_path) as f:
            lines = [l.rstrip("\n") for l in f if l.strip()]
        if lines:
            last = lines[-1].split("\t")
            seq = int(last[1]) + 1
            prev = last[3]  # event hash is at index 3 (0=EVT,1=seq,2=prev,3=hash,4=type)
    kvs = "\t".join(f"{k}={esc(v)}" for k, v in fields)
    body = f"{etype}\n{kvs}"
    h = hashlib.sha256(f"{prev}\n{body}".encode("utf-8")).hexdigest()
    line = f"EVT\t{seq}\t{prev}\t{h}\t{etype}\t{kvs}\n"
    with open(log_path, "a") as f:
        f.write(line)
    return line, seq, h

def read_log(sess):
    path = os.path.join(sess, "session.htsv")
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [l.rstrip("\n") for l in f if l.strip()]

# ---------- transport ----------
def fetch_live_envelope(query, n_results=6):
    res = bridge.search(query, max_results=n_results, backend="lumy")
    results = []
    for r in res["results"]:
        url = r["url"]
        body, status, note = b"", 0, ""
        try:
            body, status, _ = bridge.fetch(url, timeout=25)
            if status != 200:
                note = f"http_{status}"
        except Exception as e:
            note = f"fetch_failed:{type(e).__name__}"
        results.append({
            "rank": r["rank"], "url": url, "domain": r["domain"],
            "title": r["title"], "snippet": r["snippet"],
            "result_hash": r["result_hash"],
            "body_bytes": len(body),
            "body_sha256": hashlib.sha256(body).hexdigest() if body else "",
            "body_note": note,
        })
    env = {
        "query": query,
        "retrieved_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "backend": res.get("backend", "lumy"),
        "n_requested": n_results,
        "n_returned": len(results),
        "results": results,
    }
    return env

def write_envelope_files(sess, seq, env):
    with open(os.path.join(sess, "envelopes", f"{seq:03d}.json"), "w") as f:
        json.dump(env, f, ensure_ascii=False, sort_keys=True)
    lines = [f"Q\t{esc(env['query'])}", f"N\t{len(env['results'])}"]
    for r in env["results"]:
        lines.append("R\t" + "\t".join([esc(r["domain"]), esc(r["title"]), esc(r["snippet"]),
                                         esc(r["url"]), esc(r["body_sha256"]), str(r["body_bytes"])]))
    with open(os.path.join(sess, "envelopes", f"{seq:03d}.htsv"), "w") as f:
        f.write("\n".join(lines) + "\n")

# ---------- session state ----------
def load_state(sess):
    p = os.path.join(sess, "state.json")
    if os.path.exists(p):
        return json.load(open(p))
    return {"visits": [], "consults_used": 0, "installed": {}}

def save_state(sess, st):
    with open(os.path.join(sess, "state.json"), "w") as f:
        json.dump(st, f, sort_keys=True)

# ---------- commands ----------
def cmd_init(sess, arm):
    for d in ("envelopes", "helper"):
        os.makedirs(os.path.join(sess, d), exist_ok=True)
    with open(os.path.join(sess, "arm.txt"), "w") as f:
        f.write(arm + "\n")
    save_state(sess, {"visits": [], "consults_used": 0, "installed": {}})
    ledger_append(sess, "SESSION_START", [("arm", arm), ("sense_rule", "R-CORR"), ("sense_mode", "READ-AND-EDITABLE")])
    print(f"initialized {sess} arm={arm}")

def ht_next_input(st):
    lines = [f"HIST\t{len(st['visits'])}"]
    for v in st["visits"]:
        lines.append(f"V\t{v['cand']}\t{v['disp']}\t{v['followups']}")
    return "\n".join(lines) + "\n"

def parse_next(out):
    line = out.strip().splitlines()[0]
    parts = line.split("\t")
    if parts[0] == "DONE":
        return {"done": True, "reason": parts[1] if len(parts) > 1 else ""}
    return {"done": False, "cand": int(parts[1]), "query": parts[2].replace("\\t", "\t"),
            "followup": int(parts[3])}

def ht_decide_input(cand, query, results, helper=None):
    # Note: CAND searched field is 0. The binary ignores it and always runs a fresh
    # cycle with searched=0, because frozen ws_gate returns NO_SEARCH when searched!=0,
    # which would force every decision to WITHHOLD. The trial tests the sense's
    # evaluation (not its search-initiation gate); transport is supervisor-owned.
    lines = [f"CAND\t{cand}\t0", f"NRES\t{len(results)}"]
    for r in results:
        lines.append("R\t" + "\t".join([esc(r["domain"]), esc(r["title"]), esc(r["snippet"]), esc(r["url"])]))
    if helper:
        lines.append("HELPER\t1")
        lines.append(f"H\t{helper['stance']}\t{esc(helper['text'])}")
    else:
        lines.append("HELPER\t0")
    return "\n".join(lines) + "\n"

def parse_decide(out):
    d = {"stances": {}}
    for line in out.strip().splitlines():
        parts = line.split("\t")
        if parts[0] == "STANCE":
            d["stances"][int(parts[1])] = int(parts[2])
        elif parts[0] in ("SIGNAL", "DISP", "CONSULT", "DEVIATION"):
            d[parts[0].lower()] = int(parts[1])
        elif parts[0] == "HEAD":
            d["head"] = parts[1]
    return d

def log_observation(sess, seq, cand, query, followup, env, dec):
    ledger_append(sess, "QUERY_ISSUED", [("seq", str(seq)), ("cand", str(cand)),
        ("query", query), ("followup", str(followup))])
    for i, r in enumerate(env["results"]):
        stance = dec["stances"].get(i, 0)
        ledger_append(sess, "PAGE_OBSERVED", [("cand", str(cand)), ("domain", r["domain"]),
            ("url", r["url"]), ("result_hash", r["result_hash"]), ("body_sha256", r["body_sha256"])])
        ledger_append(sess, "CLAIM_EXTRACTED", [("cand", str(cand)), ("domain", r["domain"]),
            ("stance", str(stance))])
    ledger_append(sess, "SENSE_DECIDED", [("cand", str(cand)), ("signal", str(dec["signal"])),
        ("disposition", str(dec["disp"])), ("sense_head", dec["head"]),
        ("deviation", str(dec["deviation"]))])
    if dec["disp"] == 5:
        ledger_append(sess, "REVISE", [("cand", str(cand)), ("note", "corroborated contradiction of installed prior")])
    if dec["deviation"]:
        ledger_append(sess, "PROCEDURE_DEVIATION", [("cand", str(cand)), ("kind", "sense_tamper_or_wire_refused")])

def cmd_step(sess):
    st = load_state(sess)
    nxt = parse_next(run_bin(HT_NEXT, ht_next_input(st)))
    if nxt["done"]:
        ledger_append(sess, "SESSION_END", [("reason", nxt["reason"])])
        print("DONE:", nxt["reason"])
        return False
    cand, query, followup = nxt["cand"], nxt["query"], nxt["followup"]
    # seq = number of QUERY_ISSUED so far
    seq = sum(1 for v in st["visits"] for _ in [1])  # visits count = queries so far
    seq = len([l for l in read_log(sess) if "\tQUERY_ISSUED\t" in l])
    print(f"[step {seq}] cand={cand} followup={followup}: {query[:80]}", flush=True)
    env = fetch_live_envelope(query)
    write_envelope_files(sess, seq, env)
    print(f"  fetched {env['n_returned']} results", flush=True)
    dec = parse_decide(run_bin(HT_DECIDE, ht_decide_input(cand, query, env["results"])))
    log_observation(sess, seq, cand, query, followup, env, dec)
    # update state
    if followup:
        st["visits"][-1]["followups"] += 1
        st["visits"][-1]["disp"] = dec["disp"]
    else:
        st["visits"].append({"cand": cand, "disp": dec["disp"], "followups": 0})
    save_state(sess, st)
    print(f"  disp={dec['disp']} consult={dec['consult']} deviation={dec['deviation']}", flush=True)
    arm = open(os.path.join(sess, "arm.txt")).read().strip()
    if dec["consult"] and arm == "helper":
        print(f"CONSULT_NEEDED seq={seq} cand={cand}", flush=True)
    elif dec["consult"]:
        ledger_append(sess, "CONSULT_WARRANTED_NO_HELPER", [("cand", str(cand)), ("seq", str(seq))])
    return True

def cmd_consult(sess, seq):
    """Ingest the recorded helper response for seq (helper arm)."""
    seq = int(seq)
    st = load_state(sess)
    hpath = os.path.join(sess, "helper", f"{seq:03d}.htsv")
    with open(hpath) as f:
        parts = f.read().strip().split("\t")
    helper = {"stance": parts[1], "text": parts[2].replace("\\t", "\t")}
    env = json.load(open(os.path.join(sess, "envelopes", f"{seq:03d}.json")))
    # find the visit to get cand
    cand = None
    for v in st["visits"]:
        # seq maps to visit index; visits are in order
        pass
    # simpler: read cand from the QUERY_ISSUED event with seq
    for line in read_log(sess):
        if "\tQUERY_ISSUED\t" in line and f"seq={seq}\t" in line:
            for kv in line.split("\t")[5:]:
                if kv.startswith("cand="):
                    cand = int(kv[5:])
    assert cand is not None, "cand not found"
    ledger_append(sess, "CONSULT", [("cand", str(cand)), ("seq", str(seq)), ("reason", "withhold_uncertainty")])
    ledger_append(sess, "HELPER_OBSERVED", [("cand", str(cand)), ("stance", helper["stance"])])
    dec = parse_decide(run_bin(HT_DECIDE, ht_decide_input(cand, env["query"], env["results"], helper)))
    ledger_append(sess, "SENSE_DECIDED", [("cand", str(cand)), ("signal", str(dec["signal"])),
        ("disposition", str(dec["disp"])), ("sense_head", dec["head"]),
        ("deviation", str(dec["deviation"])), ("with_helper", "1")])
    if dec["disp"] == 5:
        ledger_append(sess, "REVISE", [("cand", str(cand)), ("note", "corroborated contradiction after helper")])
    st["consults_used"] += 1
    # update the visit's disp to the post-helper disposition
    # (find visit by cand; the last visit with this cand)
    for v in reversed(st["visits"]):
        if v["cand"] == cand:
            v["disp"] = dec["disp"]
            break
    save_state(sess, st)
    print(f"consult done: disp={dec['disp']}", flush=True)

def cmd_run(sess, max_steps=60):
    for _ in range(max_steps):
        if not cmd_step(sess):
            break
    else:
        print("MAX STEPS REACHED")

def cmd_replay(sess, n):
    """Deterministic replay: re-derive every decision from recorded envelopes."""
    # Read recorded data
    env_files = sorted([f for f in os.listdir(os.path.join(sess, "envelopes")) if f.endswith(".json")])
    helper_files = {f: os.path.join(sess, "helper", f) for f in os.listdir(os.path.join(sess, "helper")) if f.endswith(".htsv")}
    arm = open(os.path.join(sess, "arm.txt")).read().strip()
    # We'll rebuild the event log from scratch and compare to session.htsv
    outputs = []
    for rep in range(n):
        lines = []
        prev, seq = "0" * 64, 0
        def emit(etype, fields):
            nonlocal prev, seq
            kvs = "\t".join(f"{k}={esc(v)}" for k, v in fields)
            body = f"{etype}\n{kvs}"
            h = hashlib.sha256(f"{prev}\n{body}".encode()).hexdigest()
            lines.append(f"EVT\t{seq}\t{prev}\t{h}\t{etype}\t{kvs}")
            prev, seq = h, seq + 1
        emit("SESSION_START", [("arm", arm), ("sense_rule", "R-CORR"), ("sense_mode", "READ-AND-EDITABLE")])
        visits = []
        # iterate in seq order; re-derive next each time
        for ef in env_files:
            fseq = int(ef.split(".")[0])
            env = json.load(open(os.path.join(sess, "envelopes", ef)))
            # re-derive next
            hist_in = f"HIST\t{len(visits)}\n" + "".join(f"V\t{v['cand']}\t{v['disp']}\t{v['followups']}\n" for v in visits)
            nxt = parse_next(run_bin(HT_NEXT, hist_in))
            assert not nxt["done"], "replay: unexpected DONE"
            cand, query, followup = nxt["cand"], nxt["query"], nxt["followup"]
            emit("QUERY_ISSUED", [("seq", str(fseq)), ("cand", str(cand)), ("query", query), ("followup", str(followup))])
            dec = parse_decide(run_bin(HT_DECIDE, ht_decide_input(cand, query, env["results"])))
            for i, r in enumerate(env["results"]):
                stance = dec["stances"].get(i, 0)
                emit("PAGE_OBSERVED", [("cand", str(cand)), ("domain", r["domain"]), ("url", r["url"]),
                    ("result_hash", r["result_hash"]), ("body_sha256", r["body_sha256"])])
                emit("CLAIM_EXTRACTED", [("cand", str(cand)), ("domain", r["domain"]), ("stance", str(stance))])
            emit("SENSE_DECIDED", [("cand", str(cand)), ("signal", str(dec["signal"])),
                ("disposition", str(dec["disp"])), ("sense_head", dec["head"]), ("deviation", str(dec["deviation"]))])
            if dec["disp"] == 5:
                emit("REVISE", [("cand", str(cand)), ("note", "corroborated contradiction of installed prior")])
            # replicate cmd_step: solo arm logs CONSULT_WARRANTED_NO_HELPER when the
            # decide binary requests a consult (helper arm handles it via helper files)
            if dec["consult"] and arm != "helper":
                emit("CONSULT_WARRANTED_NO_HELPER", [("cand", str(cand)), ("seq", str(fseq))])
            # helper consult?
            hf = f"{fseq:03d}.htsv"
            if hf in helper_files:
                with open(helper_files[hf]) as f:
                    parts = f.read().strip().split("\t")
                helper = {"stance": parts[1], "text": parts[2].replace("\\t", "\t")}
                emit("CONSULT", [("cand", str(cand)), ("seq", str(fseq)), ("reason", "withhold_uncertainty")])
                emit("HELPER_OBSERVED", [("cand", str(cand)), ("stance", helper["stance"])])
                dec2 = parse_decide(run_bin(HT_DECIDE, ht_decide_input(cand, query, env["results"], helper)))
                emit("SENSE_DECIDED", [("cand", str(cand)), ("signal", str(dec2["signal"])),
                    ("disposition", str(dec2["disp"])), ("sense_head", dec2["head"]),
                    ("deviation", str(dec2["deviation"])), ("with_helper", "1")])
                if dec2["disp"] == 5:
                    emit("REVISE", [("cand", str(cand)), ("note", "corroborated contradiction after helper")])
                disp = dec2["disp"]
            else:
                disp = dec["disp"]
            if followup:
                visits[-1]["followups"] += 1
                visits[-1]["disp"] = disp
            else:
                visits.append({"cand": cand, "disp": disp, "followups": 0})
        # SESSION_END: re-derive via ht_next (should be DONE)
        hist_in = f"HIST\t{len(visits)}\n" + "".join(f"V\t{v['cand']}\t{v['disp']}\t{v['followups']}\n" for v in visits)
        nxt_end = parse_next(run_bin(HT_NEXT, hist_in))
        reason = nxt_end.get("reason", "replay") if nxt_end["done"] else "replay_unexpected_not_done"
        emit("SESSION_END", [("reason", reason)])
        outputs.append("\n".join(lines) + "\n")
        print(f"replay {rep+1}: {len(outputs[-1])} bytes sha={hashlib.sha256(outputs[-1].encode()).hexdigest()[:16]}", flush=True)
    h0 = hashlib.sha256(outputs[0].encode()).hexdigest()
    same = all(hashlib.sha256(o.encode()).hexdigest() == h0 for o in outputs)
    print("BYTE-IDENTICAL" if same else "MISMATCH — NONDETERMINISM")
    # compare to live session.htsv
    live_text = "\n".join(read_log(sess)) + "\n"
    match = (outputs[0] == live_text)
    print("MATCHES_LIVE" if match else "DIFFERS_FROM_LIVE")
    with open(os.path.join(sess, f"replay_n{n}.htsv"), "w") as f:
        f.write(outputs[0])
    return same and match

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "init":
        cmd_init(sys.argv[2], sys.argv[3])
    elif cmd == "step":
        cmd_step(sys.argv[2])
    elif cmd == "run":
        cmd_run(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 60)
    elif cmd == "consult":
        cmd_consult(sys.argv[2], sys.argv[3])
    elif cmd == "replay":
        ok = cmd_replay(sys.argv[2], int(sys.argv[3]))
        sys.exit(0 if ok else 1)
