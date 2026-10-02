#!/usr/bin/env python3
"""CLN-1 blind judging driver. 14 specs x 2 judges, sequential, deterministic.
Parses each response; retries once with a format reminder if unparseable.
Raw responses saved verbatim to work/judge_raw/<judge>/<spec>.txt."""
import os, re, subprocess, sys

BASE = os.path.expanduser("~/workspace/tnn-lab/coding/reflection/cleanliness")
WORK = os.path.join(BASE, "work")
PROMPTS = os.path.join(WORK, "judge_raw", "prompts")

SPECS = ["CLN-G1", "CLN-G2", "CLN-G3", "CLN-G4", "CLN-G5", "CLN-G6",
         "CLN-G8", "CLN-R1", "CLN-R2", "CLN-R5", "CLN-R6", "CLN-T1",
         "CLN-T2", "CLN-T4"]

LINE = re.compile(
    r"^(W|X|Y|Z)\s*:\s*T1\s*=\s*([0-2])\s+T2\s*=\s*([0-2])\s+T3\s*=\s*([0-2])\s+T4\s*=\s*([0-2])\s+AUTHOR\s*=\s*(human programmer|TNN AI coding agent|LLM assistant A|LLM assistant B)\s*$",
    re.IGNORECASE)

REMINDER = ("Your previous response was not machine-parseable. Output ONLY "
    "four lines, one for each of W, X, Y, Z, in this exact format:\n"
    "W: T1=<0/1/2> T2=<0/1/2> T3=<0/1/2> T4=<0/1/2> AUTHOR=<one of: human programmer | TNN AI coding agent | LLM assistant A | LLM assistant B>\n"
    "X: T1=<0/1/2> T2=<0/1/2> T3=<0/1/2> T4=<0/1/2> AUTHOR=<one of: human programmer | TNN AI coding agent | LLM assistant A | LLM assistant B>\n"
    "Y: ...\nZ: ...\nNo other text whatsoever.")

def parseable(text):
    got = set()
    for line in text.strip().splitlines():
        m = LINE.match(line.strip())
        if m:
            got.add(m.group(1).upper())
    return got == {"W", "X", "Y", "Z"}

def call_sol(prompt, max_tokens=4000):
    p = subprocess.run([sys.executable,
        os.path.expanduser("~/workspace/skills/unorouter/bin/sol.py"),
        prompt, str(max_tokens)],
        capture_output=True, text=True, timeout=400)
    return p.stdout, p.returncode, p.stderr

def call_grok(prompt):
    p = subprocess.run([sys.executable,
        os.path.expanduser("~/workspace/skills/unorouter/bin/unorouter.py"),
        "chat", prompt, "--model", "grok-4.6"],
        capture_output=True, text=True, timeout=400)
    return p.stdout, p.returncode, p.stderr

def run_one(judge, spec, prompt):
    fn = call_sol if judge == "sol" else call_grok
    outdir = os.path.join(WORK, "judge_raw", judge)
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, spec + ".txt")
    out, rc, err = fn(prompt)
    raw = out if rc == 0 else f"[CALL FAILED rc={rc}]\nSTDERR:\n{err}\nSTDOUT:\n{out}"
    retries = 0
    if rc == 0 and not parseable(raw):
        retries = 1
        out2, rc2, err2 = fn(REMINDER)
        raw2 = out2 if rc2 == 0 else f"[RETRY FAILED rc={rc2}]\nSTDERR:\n{err2}\nSTDOUT:\n{out2}"
        raw = raw + "\n\n===== RETRY (format reminder) =====\n\n" + raw2
    open(path, "w").write(raw)
    status = "OK" if parseable(raw) else ("OK-after-retry" if retries else "UNPARSEABLE")
    if retries and not parseable(raw):
        status = "RETRY-UNPARSEABLE"
    elif retries:
        status = "PARSEABLE-after-retry"
    return status

def main():
    results = {}
    for spec in SPECS:
        prompt = open(os.path.join(PROMPTS, spec + ".txt")).read()
        for judge in ("sol", "grok"):
            st = run_one(judge, spec, prompt)
            results[(judge, spec)] = st
            print(f"{judge:5s} {spec}: {st}", flush=True)
    print("\nSUMMARY")
    ok = sum(1 for v in results.values() if v in ("OK", "PARSEABLE-after-retry"))
    print(f"parseable: {ok}/28")
    for k, v in results.items():
        if "UNPARSEABLE" in v:
            print(f"  MISSING: {k[0]}/{k[1]} ({v})")

if __name__ == "__main__":
    main()
