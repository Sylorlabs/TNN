#!/usr/bin/env python3
"""adv_ret_det.py — LH-ADV-2026-09-22 dedicated ADV-RET / ADV-DET runs.

Result-side, decision-free measurement tooling (NOT trial machinery).
Executes the per-stage pipeline from machinery/adv_driver.py VERBATIM
(copied block, same call order, same envelope application) against the
FROZEN committed artifacts:

  ADV-RET: re-run 10 stages (incl. all 5 recovered/injected cases) under
           identical conditions and require final_spec + binary_output
           BYTE-IDENTICAL to the frozen committed ledger.json (9e6a926b5e13).
           10/10 required. (Source/binary have no ledger reference; their
           byte-identity is covered by ADV-DET's cross-rep check.)
  ADV-DET: 5 stages x 5 reps (incl. a recovered stage, D3), identical
           conditions each rep; final spec, emitted source, compiled
           binary, and binary output must be byte-identical across reps.

Pure decision-free harness: no choices, no heuristics, no RNG.
The sealed envelope (envelope.json) is read locally and NEVER committed.
"""
import json, subprocess, os, sys, hashlib, re, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.environ.get("ADV_BUILD", os.path.join(HERE, "build"))
CONTRACTS = os.environ.get("ADV_CONTRACTS", os.path.join(HERE, "pkg", "contracts"))
KB_PATH = os.environ.get("ADV_KB", os.path.join(HERE, "pkg", "adv_kb.txt"))
REF_LEDGER = os.environ.get("ADV_REF_LEDGER", os.path.join(HERE, "pkg", "ledger.json"))
ENVELOPE = os.environ.get("ADV_ENVELOPE",
    "/home/hatch/workspace/tnn-lab/coding/reflection/long_horizon_adv/envelope.json")
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
DELIB = os.path.join(BUILD, "adv_delib")
EMIT = os.path.join(BUILD, "adv_emit")
CRITIC = os.path.join(BUILD, "adv_critic")
TMP = os.environ.get("ADV_TMP", os.path.join(HERE, "tmp_rd"))

RET_STAGES = ["B2", "D3", "C5", "E8", "A7", "A1", "A5", "C1", "J1", "E9"]
DET_STAGES = ["D3", "A1", "A5", "J2", "E9"]
DET_REPS = 5

def run(args, **kw):
    r = subprocess.run(args, capture_output=True, text=True, **kw)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

def sha(b):
    return hashlib.sha256(b).hexdigest()

def corrupt_kb(kb_text, entry_id, payload):
    text = kb_text
    if "swap_op" in payload:
        pat = re.compile(r'(ID:\s*' + re.escape(entry_id) + r'[^\n]*\nOP:\s*)(\S+)')
        text, n = pat.subn(r'\g<1>' + payload["swap_op"], text, count=1)
        assert n == 1, f"KB swap failed for {entry_id}"
    if "inject" in payload:
        pat = re.compile(r'(ID:\s*' + re.escape(entry_id) + r')([^\n]*)')
        text, n = pat.subn(r'\g<1>' + payload["inject"] + r'\g<2>', text, count=1)
        assert n == 1, f"KB inject failed for {entry_id}"
    return text

def run_stage(stage, env, kb_orig, ledger_stages):
    """Per-stage pipeline COPIED VERBATIM from adv_driver.py main loop.
    Returns (rec, src_path, bin_path). ledger_stages is the live list used
    for the DEP-CORRUPT upstream lookup (mirrors the driver's ledger)."""
    rec = {"stage": stage, "events": [], "cycles": 0}
    contract = open(os.path.join(CONTRACTS, f"{stage}.txt")).read()

    inj = None
    for f in env["failures"]:
        if f["stage"] == stage:
            inj = f
            break

    kb_text = kb_orig
    quarantine = []

    if inj and inj["type"] in ("KB-CORRUPT", "UNRECOVERABLE"):
        kb_text = corrupt_kb(kb_orig, inj["entry_id"], inj["payload"])
        rec["events"].append(f"INJECT {inj['type']} {inj['entry_id']}")

    final_spec = None
    max_cycles = 30
    cycles = 0
    halted = False

    while cycles < max_cycles:
        cycles += 1
        rec["cycles"] += 1
        qarg = ",".join(quarantine)
        out, err, rc = run([DELIB, "propose", stage, contract, kb_text, qarg])
        rec["events"].append(f"PROPOSE: {out[:120]}")

        if out.startswith("HALT"):
            if "KB-CORRUPT" in out:
                evid = out
                dout, _, _ = run([DELIB, "diagnose", stage, contract, kb_text, qarg, "", evid, ""])
                rec["events"].append(f"DIAGNOSE: {dout[:200]}")
                m = re.search(r'ADD-QUARANTINE (\S+)', dout)
                if m:
                    qid = m.group(1)
                    quarantine.append(qid)
                    rec["events"].append(f"QUARANTINE {qid}")
                    rec["failures_diagnosed"] = rec.get("failures_diagnosed", []) + [qid]
                    continue
                else:
                    rec["events"].append("DIAGNOSE-NO-ACTION")
                    halted = True
                    break
            elif "KB-MISS" in out:
                if quarantine and inj and inj["type"] == "UNRECOVERABLE":
                    evid = f"HALT KB-MISS quarantine={quarantine[0]}"
                    dout, _, _ = run([DELIB, "diagnose", stage, contract, kb_text, qarg, "", evid, ""])
                    rec["events"].append(f"DIAGNOSE: {dout[:200]}")
                    if "HALT UNRECOVERABLE" in dout:
                        rec["halt"] = dout.strip()
                        rec["honest_halt"] = True
                        halted = True
                        break
                if stage == "F1" and "KB-MISS" in out:
                    rec["halt"] = out.strip()
                    rec["honest_halt"] = True
                    halted = True
                    break
                rec["halt"] = out.strip()
                halted = True
                break
            else:
                rec["halt"] = out.strip()
                halted = True
                break

        cands = [l for l in out.split("\n") if l.startswith("CAND")]
        if not cands:
            rec["events"].append("NO-CANDS")
            halted = True
            break

        cout, _, _ = run([DELIB, "critique", stage, contract, "\n".join(cands)])
        rec["events"].append(f"CRITIQUE: {cout[:120]}")
        rec["cycles"] += 1

        if cout.startswith("ACCEPT"):
            accept_line = cout.split("\n")[0]
            adv_idx = accept_line.find("ADV|")
            if adv_idx >= 0:
                final_spec = accept_line[adv_idx:].strip()
            else:
                comp, _, _ = run([DELIB, "compose", stage, contract, "\n".join(cands), cout])
                rec["events"].append(f"COMPOSE: {comp[:120]}")
                rec["cycles"] += 1
                for l in comp.split("\n"):
                    if "ADV|" in l:
                        idx = l.find("ADV|")
                        final_spec = l[idx:].strip()
                        break
            if final_spec:
                rec["events"].append(f"SPEC: {final_spec[:80]}")
                break
        else:
            dout, _, _ = run([DELIB, "diagnose", stage, contract, kb_text, qarg, "", cout, "\n".join(cands)])
            rec["events"].append(f"DIAGNOSE: {dout[:200]}")
            rec["cycles"] += 1
            halted = True
            rec["halt"] = "HALT NO-ACCEPT-recovery-unimplemented"
            break

    src_path = os.path.join(TMP, f"{stage}_gen.zag")
    bin_path = os.path.join(TMP, f"{stage}_bin")

    if halted:
        return rec, None, None

    if not final_spec:
        rec["halt"] = "HALT NO-FINAL-SPEC"
        return rec, None, None

    rec["final_spec"] = final_spec

    src, _, _ = run([EMIT, "gen", final_spec])
    rec["events"].append(f"EMIT {len(src)} bytes")

    if inj and inj["type"] == "EMITTER-BUG":
        old = inj["payload"]["old"]
        new = inj["payload"]["new"]
        if old in src:
            src = src.replace(old, new, 1)
            rec["events"].append(f"INJECT EMITTER-BUG {old}->{new}")
        else:
            rec["events"].append(f"INJECT-FAILED old-token-not-found")

    open(src_path, "w").write(src)
    if os.path.exists(bin_path):
        os.remove(bin_path)
    _, err, rc = run([ZNC, src_path, "-o", bin_path, "--no-analyze", "--no-zagd"])
    if rc != 0 or not os.path.exists(bin_path) or os.path.getsize(bin_path) == 0:
        rec["events"].append(f"COMPILE-FAIL rc={rc} err={err[:100]}")
        rec["halt"] = "HALT COMPILE-FAIL"
        return rec, src_path, None

    m = re.search(r'^TEST in=(.*)$', contract, re.M)
    tin = m.group(1) if m else ""
    if final_spec.startswith("ADV|AGG|") or final_spec.startswith("ADV|SORT|") or final_spec.startswith("ADV|JOIN|"):
        bout, _, _ = run([bin_path, tin])
        binout = bout.strip().replace("\n", ";")
    else:
        recs = tin.split(";")
        outs = []
        for r in recs:
            o, _, _ = run([bin_path, r])
            if o:
                outs.append(o)
        binout = ";".join(outs)

    rec["binary_output"] = binout

    cout, _, _ = run([CRITIC, "verify", stage, contract, final_spec, binout])
    rec["events"].append(f"CRITIC: {cout[:120]}")
    rec["critic"] = cout.strip()

    if cout.startswith("CRITIC-ACCEPT"):
        rec["stage_accept"] = True
    else:
        rec["stage_accept"] = False
        if inj and inj["type"] == "EMITTER-BUG" and "EMITTER-BUG" in cout:
            rec["events"].append("CRITIC-REJECTED-BUG regenerating-clean")
            src2, _, _ = run([EMIT, "gen", final_spec])
            open(src_path, "w").write(src2)
            _, _, rc2 = run([ZNC, src_path, "-o", bin_path, "--no-analyze", "--no-zagd"])
            if rc2 == 0:
                if final_spec.startswith("ADV|AGG|") or final_spec.startswith("ADV|SORT|") or final_spec.startswith("ADV|JOIN|"):
                    bout2, _, _ = run([bin_path, tin])
                    binout2 = bout2.strip().replace("\n", ";")
                else:
                    outs2 = []
                    for r in tin.split(";"):
                        o2, _, _ = run([bin_path, r])
                        if o2:
                            outs2.append(o2)
                    binout2 = ";".join(outs2)
                cout2, _, _ = run([CRITIC, "verify", stage, contract, final_spec, binout2])
                rec["events"].append(f"CRITIC-RETRY: {cout2[:80]}")
                if cout2.startswith("CRITIC-ACCEPT"):
                    rec["stage_accept"] = True
                    rec["recovered"] = True

    dep_inj = None
    if inj and inj["type"] == "DEP-CORRUPT":
        up_stage = inj["upstream_stage"]
        up_out = None
        for sr in ledger_stages:
            if sr["stage"] == up_stage and "binary_output" in sr:
                up_out = sr["binary_output"]
                break
        if up_out is not None:
            corr = inj["payload"]["corruption"]
            if corr == "empty":
                corrupted = ""
            elif corr == "drop_field_2":
                recs = up_out.split(";")
                corrupted_recs = []
                for r in recs:
                    fields = r.split("|")
                    if len(fields) >= 2:
                        fields = [fields[0]] + fields[2:]
                    corrupted_recs.append("|".join(fields))
                corrupted = ";".join(corrupted_recs)
            else:
                corrupted = up_out

            rec["events"].append(f"INJECT DEP-CORRUPT upstream={up_stage} corruption={corr}")

            if final_spec.startswith("ADV|AGG|") or final_spec.startswith("ADV|SORT|") or final_spec.startswith("ADV|JOIN|"):
                bout_corr, _, _ = run([bin_path, corrupted])
                bout_corr = bout_corr.strip().replace("\n", ";")
            else:
                outs_corr = []
                for r in corrupted.split(";"):
                    if r:
                        o, _, _ = run([bin_path, r])
                        if o:
                            outs_corr.append(o)
                bout_corr = ";".join(outs_corr)

            if bout_corr != binout:
                rec["events"].append(f"DEP-CORRUPT detected: corrupted-output != correct-output")
                evid = f"OUTPUT-MISMATCH upstream={up_stage} input-corrupted"
                dout, _, _ = run([DELIB, "diagnose", stage, contract, kb_text, qarg, final_spec, evid, f"upstream={up_stage}"])
                rec["events"].append(f"DIAGNOSE: {dout[:200]}")
                if up_stage in dout and "AWAIT-UPSTREAM" in dout:
                    rec["events"].append(f"DEP-CORRUPT correctly diagnosed: upstream={up_stage}")
                    rec["dep_recovered"] = True
                else:
                    rec["events"].append(f"DEP-CORRUPT MISDIAGNOSED")
                    rec["stage_accept"] = False
        else:
            rec["events"].append(f"DEP-CORRUPT skipped: no upstream output for {up_stage}")

    return rec, src_path, bin_path

def artifacts(rec, src_path, bin_path):
    """Return the four compared artifacts (spec, source-bytes, binary-sha, output)."""
    a = {}
    a["spec"] = rec.get("final_spec", "")
    a["output"] = rec.get("binary_output", "")
    a["source_sha"] = sha(open(src_path, "rb").read()) if src_path and os.path.exists(src_path) else None
    a["binary_sha"] = sha(open(bin_path, "rb").read()) if bin_path and os.path.exists(bin_path) else None
    return a

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "ret"
    os.makedirs(TMP, exist_ok=True)
    env = json.load(open(ENVELOPE))
    kb_orig = open(KB_PATH).read()
    ref = json.load(open(REF_LEDGER))
    ref_by = {s["stage"]: s for s in ref["stages"]}
    out = {"mode": mode, "stages": [], "pass": False}

    if mode == "ret":
        # For DEP-CORRUPT stages, run the upstream stage cleanly first so the
        # driver's upstream lookup finds live outputs (verbatim behavior).
        ledger_stages = []
        upstreams = {}
        for st in RET_STAGES:
            inj = next((f for f in env["failures"] if f["stage"] == st), None)
            if inj and inj["type"] == "DEP-CORRUPT" and inj["upstream_stage"] not in upstreams:
                urec, _, _ = run_stage(inj["upstream_stage"], env, kb_orig, ledger_stages)
                ledger_stages.append(urec)
                upstreams[inj["upstream_stage"]] = urec
        ok = 0
        for st in RET_STAGES:
            rec, sp, bp = run_stage(st, env, kb_orig, ledger_stages)
            ledger_stages.append(rec)
            r = ref_by[st]
            spec_match = rec.get("final_spec") == r.get("final_spec")
            out_match = rec.get("binary_output") == r.get("binary_output")
            accept_match = rec.get("stage_accept") == r.get("stage_accept")
            cycles = rec.get("cycles")
            m = spec_match and out_match and accept_match
            ok += 1 if m else 0
            out["stages"].append({
                "stage": st, "match": m, "spec_match": spec_match,
                "output_match": out_match, "accept_match": accept_match,
                "cycles": cycles, "injected": st in [f["stage"] for f in env["failures"]],
            })
            print(f"RET {st}: {'MATCH' if m else 'MISMATCH'} "
                  f"(spec={spec_match} out={out_match} accept={accept_match} cycles={cycles})")
        out["ret_n"], out["ret_ok"] = len(RET_STAGES), ok
        out["pass"] = (ok == len(RET_STAGES))
        print(f"ADV-RET: {ok}/{len(RET_STAGES)} byte-identical -> {'PASS' if out['pass'] else 'FAIL'}")

    elif mode == "det":
        ok_stages = 0
        for st in DET_STAGES:
            reps = []
            for i in range(DET_REPS):
                ledger_stages = []
                rec, sp, bp = run_stage(st, env, kb_orig, ledger_stages)
                reps.append(artifacts(rec, sp, bp))
            agree = all(r == reps[0] for r in reps[1:])
            ok_stages += 1 if agree else 0
            out["stages"].append({"stage": st, "reps": DET_REPS, "agree": agree,
                                  "spec": reps[0]["spec"][:60],
                                  "source_sha": reps[0]["source_sha"][:16],
                                  "binary_sha": reps[0]["binary_sha"][:16]})
            print(f"DET {st}: {'IDENTICAL x5' if agree else 'DIVERGED'} "
                  f"bin={reps[0]['binary_sha'][:16] if reps[0]['binary_sha'] else None}")
        out["det_n"], out["det_ok"] = len(DET_STAGES), ok_stages
        out["pass"] = (ok_stages == len(DET_STAGES))
        print(f"ADV-DET: {ok_stages}/{len(DET_STAGES)} stages identical x5 -> {'PASS' if out['pass'] else 'FAIL'}")

    json.dump(out, open(os.path.join(HERE, f"result_{mode}.json"), "w"), indent=1)

if __name__ == "__main__":
    main()
