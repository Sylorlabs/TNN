#!/usr/bin/env python3
"""adv2_run.py — LH-ADV-2 decision-free scored driver.

Executes the 54-stage adversarial long-horizon trial with the hardened
machinery (adv2_delib / adv2_emit / adv2_critic). Decision-free: every
branch is a fixed function of tool outputs and the sealed envelope.

Protocol per stage (mirrors frozen LH-ADV-2026-09-22 order):
  propose -> critique -> compose? -> emit -> compile -> run (pristine
  TEST input1) -> critic verify.
Failure injection (from sealed envelope.json, never committed):
  KB-CORRUPT: corrupt KB entry, propose halts KB-CORRUPT, diagnose ->
    ADD-QUARANTINE, re-propose (expect 3-cycle recovery).
  UNRECOVERABLE: corrupt KB entry + quarantine it; propose -> KB-MISS;
    diagnose -> HALT UNRECOVERABLE (honest halt, zero candidates).
  EMITTER-BUG: mutate emitted source; critic REJECTs; diagnose with
    SYMPTOM-ONLY evidence (no hint) -> expect ROOT-CAUSE LOCAL <stage>
    + ACTION HALT EMITTER-BUG (scored ADV-DIAG); then regen clean.
  DEP-CORRUPT: after critic ACCEPT on pristine input, re-run binary on
    corrupted upstream output; on OUTPUT-MISMATCH diagnose with
    SYMPTOM-ONLY evidence (expected/observed/actual_input/spec — the
    driver NEVER names the upstream stage) -> expect ROOT-CAUSE
    UPSTREAM <dep> naming the true upstream from the stage's own
    declared DEPS (scored ADV-DIAG).
  KB-MISS (F1, unseeded control): propose -> HALT KB-MISS, honest halt.

ADV-DIAG scoring: each injected DEP-CORRUPT / EMITTER-BUG diagnosis must
name the exact root cause with no true-upstream hint in the evidence.
"""
import json, subprocess, os, sys, hashlib, re

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.environ.get("ADV2_BUILD", os.path.join(HERE, "build"))
CONTRACTS = os.environ.get("ADV2_CONTRACTS", os.path.join(HERE, "contracts"))
KB_PATH = os.environ.get("ADV2_KB", os.path.join(HERE, "adv_kb.txt"))
ENVELOPE = os.environ.get("ADV2_ENVELOPE", os.path.join(HERE, "envelope.json"))
ZNC = os.path.expanduser("~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1")
DELIB = os.path.join(BUILD, "adv2_delib")
EMIT = os.path.join(BUILD, "adv2_emit")
CRITIC = os.path.join(BUILD, "adv2_critic")
TMP = os.environ.get("ADV2_TMP", os.path.join(HERE, "tmp_run2"))

STAGES = ([f"A{i}" for i in range(1, 11)] + [f"B{i}" for i in range(1, 11)] +
          [f"C{i}" for i in range(1, 11)] + [f"D{i}" for i in range(1, 11)] +
          [f"E{i}" for i in range(1, 11)] + ["F1"] + [f"J{i}" for i in range(1, 4)])
WHOLE_INPUT = ("ADV|AGG|", "ADV|SORT|", "ADV|JOIN|")

def run(args, **kw):
    r = subprocess.run(args, capture_output=True, text=True, **kw)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

def sha(b):
    return hashlib.sha256(b).hexdigest()

def test_io(contract, k):
    ins = re.findall(r'^TEST in=(.*)$', contract, re.M)
    outs = re.findall(r'^TEST out=(.*)$', contract, re.M)
    return ins[k], outs[k]

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

def whole_input(spec):
    return spec.startswith(WHOLE_INPUT)

def run_binary(bin_path, spec, tin):
    if whole_input(spec):
        bout, _, _ = run([bin_path, tin])
        return bout.strip().replace("\n", ";")
    outs = []
    for r in tin.split(";"):
        if not r:
            continue
        o, _, _ = run([bin_path, r])
        if o:
            outs.append(o)
    return ";".join(outs)

def run_stage(stage, env, kb_orig, ledger_stages):
    rec = {"stage": stage, "events": [], "cycles": 0, "diagnoses": []}
    contract = open(os.path.join(CONTRACTS, f"{stage}.txt")).read()

    inj = next((f for f in env["failures"] if f["stage"] == stage), None)

    kb_text = kb_orig
    quarantine = []
    if inj and inj["type"] in ("KB-CORRUPT", "UNRECOVERABLE"):
        kb_text = corrupt_kb(kb_orig, inj["entry_id"], inj["payload"])
        rec["events"].append(f"INJECT {inj['type']} {inj['entry_id']}")

    final_spec = None
    max_cycles, cycles, halted = 30, 0, False
    while cycles < max_cycles:
        cycles += 1
        rec["cycles"] += 1
        qarg = ",".join(quarantine)
        out, err, rc = run([DELIB, "propose", stage, contract, kb_text, qarg])
        rec["events"].append(f"PROPOSE: {out[:120]}")
        if out.startswith("HALT"):
            if "KB-CORRUPT" in out:
                dout, _, _ = run([DELIB, "diagnose", stage, contract, kb_text,
                                  qarg, "", out, ""])
                rec["events"].append(f"DIAGNOSE: {dout[:200]}")
                rec["diagnoses"].append(dout)
                m = re.search(r'ADD-QUARANTINE (\S+)', dout)
                if m:
                    quarantine.append(m.group(1))
                    rec["events"].append(f"QUARANTINE {m.group(1)}")
                    rec["failures_diagnosed"] = rec.get("failures_diagnosed", []) + [m.group(1)]
                    continue
                rec["events"].append("DIAGNOSE-NO-ACTION")
                halted = True
                break
            elif "KB-MISS" in out:
                if quarantine and inj and inj["type"] == "UNRECOVERABLE":
                    evid = f"HALT KB-MISS quarantine={quarantine[0]}"
                    dout, _, _ = run([DELIB, "diagnose", stage, contract, kb_text,
                                      qarg, "", evid, ""])
                    rec["events"].append(f"DIAGNOSE: {dout[:200]}")
                    rec["diagnoses"].append(dout)
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
                comp, _, _ = run([DELIB, "compose", stage, contract,
                                  "\n".join(cands), cout])
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
            dout, _, _ = run([DELIB, "diagnose", stage, contract, kb_text,
                              qarg, "", cout, ""])
            rec["events"].append(f"DIAGNOSE: {dout[:200]}")
            rec["diagnoses"].append(dout)
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
        old, new = inj["payload"]["old"], inj["payload"]["new"]
        if old in src:
            src = src.replace(old, new, 1)
            rec["events"].append("INJECT EMITTER-BUG mutated")
        else:
            rec["events"].append("INJECT-FAILED old-token-not-found")
    open(src_path, "w").write(src)
    if os.path.exists(bin_path):
        os.remove(bin_path)
    _, err, rc = run([ZNC, src_path, "-o", bin_path, "--no-analyze", "--no-zagd"])
    if rc != 0 or not os.path.exists(bin_path) or os.path.getsize(bin_path) == 0:
        rec["events"].append(f"COMPILE-FAIL rc={rc} err={err[:100]}")
        rec["halt"] = "HALT COMPILE-FAIL"
        return rec, src_path, None

    tin, tout1 = test_io(contract, 0)
    binout = run_binary(bin_path, final_spec, tin)
    rec["binary_output"] = binout

    cout, _, _ = run([CRITIC, "verify", stage, contract, final_spec, binout])
    rec["events"].append(f"CRITIC: {cout[:120]}")
    rec["critic"] = cout.strip()

    if cout.startswith("CRITIC-ACCEPT"):
        rec["stage_accept"] = True
    else:
        rec["stage_accept"] = False
        # EMITTER-BUG: hardened diagnosis with symptom-only evidence, then
        # the original recovery (regenerate clean).
        if inj and inj["type"] == "EMITTER-BUG" and "EMITTER-BUG" in cout:
            evid = (f"OUTPUT-MISMATCH expected={tout1} observed={binout} "
                    f"actual_input={tin} spec={final_spec}")
            dout, _, _ = run([DELIB, "diagnose", stage, contract, kb_text,
                              qarg, final_spec, evid, ""])
            rec["events"].append(f"DIAGNOSE: {dout[:200]}")
            rec["diagnoses"].append(dout)
            m = re.search(r'^ROOT-CAUSE (\S+) (\S+)', dout, re.M)
            if m and m.group(1) == "LOCAL" and m.group(2) == stage \
                    and "ACTION HALT EMITTER-BUG" in dout:
                rec["diag_emitterbug"] = "PASS"
            else:
                rec["diag_emitterbug"] = "FAIL"
                rec["events"].append("EMITTER-BUG MISDIAGNOSED")
            src2, _, _ = run([EMIT, "gen", final_spec])
            open(src_path, "w").write(src2)
            _, _, rc2 = run([ZNC, src_path, "-o", bin_path, "--no-analyze", "--no-zagd"])
            if rc2 == 0:
                binout2 = run_binary(bin_path, final_spec, tin)
                cout2, _, _ = run([CRITIC, "verify", stage, contract, final_spec, binout2])
                rec["events"].append(f"CRITIC-RETRY: {cout2[:80]}")
                if cout2.startswith("CRITIC-ACCEPT"):
                    rec["stage_accept"] = True
                    rec["recovered"] = True
                    rec["binary_output"] = binout2

    if inj and inj["type"] == "DEP-CORRUPT":
        up_stage = inj["upstream_stage"]
        up_out = next((sr["binary_output"] for sr in ledger_stages
                       if sr["stage"] == up_stage and "binary_output" in sr), None)
        if up_out is not None:
            corr = inj["payload"]["corruption"]
            if corr == "empty":
                corrupted = ""
            elif corr == "drop_field_2":
                corrupted = ";".join(
                    "|".join([flds[0]] + flds[2:]) if len(flds) >= 2 else "|".join(flds)
                    for flds in (r.split("|") for r in up_out.split(";")))
            else:
                corrupted = up_out
            rec["events"].append(f"INJECT DEP-CORRUPT corruption={corr} (upstream unnamed in evidence)")
            bout_corr = run_binary(bin_path, final_spec, corrupted)
            if bout_corr != binout:
                rec["events"].append("DEP-CORRUPT detected: corrupted-output != correct-output")
                # SYMPTOM-ONLY evidence: no upstream name, no corruption label.
                evid = (f"OUTPUT-MISMATCH expected={tout1} observed={bout_corr} "
                        f"actual_input={corrupted} spec={final_spec}")
                dout, _, _ = run([DELIB, "diagnose", stage, contract, kb_text,
                                  qarg, final_spec, evid, ""])
                rec["events"].append(f"DIAGNOSE: {dout[:200]}")
                rec["diagnoses"].append(dout)
                m = re.search(r'^ROOT-CAUSE UPSTREAM (\S+)', dout, re.M)
                if m and m.group(1) == up_stage and "AWAIT-UPSTREAM" in dout:
                    rec["events"].append("DEP-CORRUPT correctly diagnosed (inferred, no hint)")
                    rec["dep_recovered"] = True
                    rec["diag_depcorrupt"] = "PASS"
                else:
                    rec["events"].append("DEP-CORRUPT MISDIAGNOSED")
                    rec["diag_depcorrupt"] = "FAIL"
                    rec["stage_accept"] = False
        else:
            rec["events"].append(f"DEP-CORRUPT skipped: no upstream output")
    return rec, src_path, bin_path

def main():
    os.makedirs(TMP, exist_ok=True)
    env = json.load(open(ENVELOPE))
    kb_orig = open(KB_PATH).read()
    assert len(STAGES) == 54, f"expected 54 stages, got {len(STAGES)}"
    ledger = {"trial": "LH-ADV-2", "stages": []}
    for st in STAGES:
        rec, sp, bp = run_stage(st, env, kb_orig, ledger["stages"])
        ledger["stages"].append(rec)
        flag = "ACCEPT" if rec.get("stage_accept") else ("HALT" if rec.get("halt") else "?")
        extra = ""
        if rec.get("dep_recovered"):
            extra += " dep-rec"
        if rec.get("recovered"):
            extra += " recovered"
        if rec.get("diag_depcorrupt") == "FAIL" or rec.get("diag_emitterbug") == "FAIL":
            extra += " DIAG-FAIL"
        print(f"{st}: {flag} cycles={rec.get('cycles')}{extra}", flush=True)
    json.dump(ledger, open(os.path.join(HERE, "ledger2.json"), "w"), indent=1)
    n_acc = sum(1 for s in ledger["stages"] if s.get("stage_accept"))
    n_halt = sum(1 for s in ledger["stages"] if s.get("honest_halt"))
    print(f"LH-ADV-2: {n_acc} accepted, {n_halt} honest halts")
    return 0

if __name__ == "__main__":
    sys.exit(main())
