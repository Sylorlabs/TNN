#!/usr/bin/env python3
"""H3 official-battery driver: 14 frozen corpora through novel.zag, two passes.

Usage: h3_run.py <novel_bin> <fixtures_dir> <teach_dir> <manifest.json> <outdir>

Glue does formatting/orchestration/scoring only. All classification,
corroboration, injection scanning, and reporting is novel.zag (pure Zag).

K construction (A3, as the RT2 pin): every non-empty line + every sentence
of the six SHA-pinned teach files G1-G6 (raw texts; norm applied inside the
instrument). AD5 mechanism-level gate: teach SHAs must match MANIFEST.md
exactly; exactly six teach files; no G7 (rejected at calibration, absent).

Fixture page protocol (frozen, MANIFEST.md section 5):
  TITLE: <text> -> T|<text>   (metadata, never classified)
  S| <sentence>  -> S|<text>   (factual sentence)
  F| <text>      -> F|<text>   (non-factual framing, never classified)
  I| <text>      -> F|<text>   (injection canary: content-scanned by the
                               instrument's injection scan, never classified
                               as a sentence, page excluded on hit)

Determinism: sorted iteration order, LF newlines, no timestamps anywhere.
Two runs over the same inputs must be byte-identical (H3-K7).
Zero RNG anywhere in this file.
"""
import json
import os
import re
import subprocess
import sys

NOVEL_BIN, FIXTURES, TEACH, MANIFEST, OUT = sys.argv[1:6]
# Optional 6th arg: battery filter ("N" or "E") for lesion calibration runs.
BATTERY = sys.argv[6] if len(sys.argv) > 6 else None

TEACH_FILES = ["g1_query.txt", "g2_select.txt", "g3_claim.txt",
               "g4_corroborate.txt", "g5_provenance.txt", "g6_injection.txt"]
# SHA-256 pins from MANIFEST.md section 6 (frozen).
TEACH_SHA = {
    "g1_query.txt": "d12d043e1ddf48d2544495b9e698e3e46d1888f2a1652498381e2cb455f38fdf",
    "g2_select.txt": "f17ee7bc7817bd17bbad01189e770ab24356e108f27cfae005e8e1578070e593",
    "g3_claim.txt": "5889ec862b19af3c3d20f5e637cde38052d2b86c8c12f1271067d2eb2d3a038e",
    "g4_corroborate.txt": "2d16355ba84563d93e3b9c5b57bf3c30aecf7c989316b738a4bea8e230a5fef1",
    "g5_provenance.txt": "b8ef6bbbb3989f9f31b26f18cd4ddac5f1680b21db0a331497ffe1f8338e5a0a",
    "g6_injection.txt": "21b73e463561b5914a162e4c77b852b66b607eeed69bdbefef46f494ef0200d9",
}

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

# ---- byte-exact replica of novel.zag norm_into (operates on UTF-8 bytes) ----
WS = {9, 10, 11, 12, 13, 32, 160}


def zfold(c):
    if 65 <= c <= 90:
        return c + 32
    if 192 <= c <= 222 and c != 215:
        return c + 32
    return c


def znorm(bs):
    out = bytearray()
    pend = False
    for c in bs:
        if c in WS:
            pend = True
            continue
        if pend and out:
            out.append(32)
        pend = False
        out.append(zfold(c))
    return bytes(out)


def sha256_file(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sentences_of(text):
    return [s for s in (p.strip() for p in SENT_SPLIT.split(text)) if s]


os.makedirs(OUT, exist_ok=True)
man = json.load(open(MANIFEST))

# ============ AD5 mechanism-level gate: teach state is TEACH|VALID ============
teach_present = sorted(f for f in os.listdir(TEACH) if f.endswith(".txt"))
assert teach_present == sorted(TEACH_FILES), \
    "AD5 FAIL: teach dir must hold exactly G1-G6, found %s" % teach_present
for tf in TEACH_FILES:
    got = sha256_file(os.path.join(TEACH, tf))
    assert got == TEACH_SHA[tf], "AD5 FAIL: %s sha mismatch" % tf
# G7: rejected at calibration — no g7 file may exist.
assert not any("g7" in f for f in os.listdir(TEACH)), "AD5 FAIL: G7 present"

# ============ K construction (A3) ============
kraws = []
for tf in TEACH_FILES:
    text = open(os.path.join(TEACH, tf), encoding="utf-8").read()
    for line in text.split("\n"):
        if line.strip():
            kraws.append(line)
    kraws.extend(sentences_of(text))
knorms = set(znorm(r.encode("utf-8")) for r in kraws)

# AD1: every nonce token absent from every K raw.
nonces = man["nonce_tokens"]
for n in nonces:
    assert not any(n in r for r in kraws), "AD1 FAIL: nonce in K: " + n

# ============ fixture pin (mechanism-level re-verification of AD4) ============
pin_lines = []
pin_lines.append("K_raw_records=%d" % len(kraws))
pin_lines.append("K_norm_forms=%d" % len(knorms))
pin_lines.append("TEACH_SHA_PIN=OK (6/6 match MANIFEST.md)")
pin_lines.append("TEACH_EXACT_SIX=OK (no G7)")
pin_lines.append("AD1_NONCE_ABSENT=OK (%d tokens)" % len(nonces))
ea_miss = 0
for cid in sorted(os.listdir(FIXTURES)):
    cdir = os.path.join(FIXTURES, cid)
    if not os.path.isdir(cdir) or man["corpora"][cid]["battery"] not in ("E", "A"):
        continue
    for pf in sorted(os.listdir(cdir)):
        if not pf.endswith(".txt"):
            continue
        for line in open(os.path.join(cdir, pf), encoding="utf-8"):
            if line.startswith("S|"):
                s = line[2:].strip()
                if znorm(s.encode("utf-8")) not in knorms:
                    ea_miss += 1
                    pin_lines.append("EA_PIN_MISS|%s|%s|%s" % (cid, pf, s[:60]))
pin_lines.append("EA_KNOWN_PIN_MISS=%d (require 0)" % ea_miss)
assert ea_miss == 0, "AD4 re-pin FAIL"

# planted-fact sanity: every N/B/C fact norm-present on its manifest pages,
# and the driver's znorm replica is byte-exact per the manifest's norm_sha256.
import hashlib
fact_norm = {}
for fid, f in man["facts"].items():
    zn = znorm(f["sentence"].encode("utf-8"))
    assert hashlib.sha256(zn).hexdigest() == f["norm_sha256"], \
        "znorm replica FAIL on " + fid
    fact_norm[fid] = zn
for fid, f in sorted(man["facts"].items()):
    cid = f["corpus"]
    for pno in f["pages"]:
        pf = os.path.join(FIXTURES, cid, "%s-p%d.txt" % (cid, pno))
        body = open(pf, encoding="utf-8").read()
        assert fact_norm[fid] in znorm(body.encode("utf-8")), \
            "fact pin FAIL: %s not on %s-p%d" % (fid, cid, pno)
pin_lines.append("PLANTED_FACT_PIN=OK (28/28 on manifest pages)")
pin_lines.append("ZNORM_REPLICA_OK=OK (28/28 norm_sha256 match manifest)")

with open(os.path.join(OUT, "K_PIN.txt"), "w") as f:
    f.write("\n".join(pin_lines) + "\n")

kfile = os.path.join(OUT, "kfile.txt")
with open(kfile, "w", encoding="utf-8", newline="\n") as f:
    for i, r in enumerate(kraws, 1):
        f.write("K|%d|%s\n" % (i, r))


def page_to_input(cdir, pf, pid):
    content = open(os.path.join(cdir, pf), encoding="utf-8").read()
    lines = ["PAGE|%s|OK" % pid]
    for line in content.split("\n"):
        if line.startswith("TITLE:"):
            lines.append("T|" + line[len("TITLE:"):].strip())
        elif line.startswith("F|"):
            lines.append("F|" + line[2:].strip())
        elif line.startswith("I|"):
            # canary: scanned by the instrument, never classified
            lines.append("F|" + line[2:].strip())
        elif line.startswith("S|"):
            lines.append("S|" + line[2:].strip())
    return lines


def parse_report(text, installs_text, withholds_text):
    m = re.search(
        r"REPORT\|([^|]+)\|([^|]+)\|known=(\d+)\|novel_installed=(\d+)\|novel_withheld=(\d+)",
        text)
    flags = re.findall(r"FLAG\|INJECTION\|([^|]+)\|([^\s]+)", text)
    inst = re.findall(r"^K\|([^|]+)\|([^|]+)\|(.+?)\|[^|]*$", installs_text, re.M)
    withh = re.findall(r"^W\|([^|]+)\|([^|]+)\|SINGLE_SOURCE\|([^|]+)\|(.+)$",
                       withholds_text, re.M)
    return {
        "verdict": m.group(2), "known": int(m.group(3)),
        "inst": int(m.group(4)), "withh": int(m.group(5)),
        "flags": flags,
        "inst_texts": [t for _, _, t in inst],
        "withh_rows": withh,
    }


CORPORA = sorted(d for d in os.listdir(FIXTURES)
                 if os.path.isdir(os.path.join(FIXTURES, d)))
assert CORPORA == ["A1", "A2", "B1", "B2", "C1", "C2", "E1", "E2", "E3", "E4",
                   "N1", "N2", "N3", "N4"], "corpus set mismatch: %s" % CORPORA
if BATTERY:
    CORPORA = [c for c in CORPORA if man["corpora"][c]["battery"] == BATTERY]
    marker = "LESION|%s|battery=%s\n" % (
        "L1" if "lesion1" in NOVEL_BIN else "L2", BATTERY)
    with open(os.path.join(OUT, "LESION.txt"), "w") as f:
        f.write(marker)

results = []
for cid in CORPORA:
    cdir = os.path.join(FIXTURES, cid)
    cfile = os.path.join(OUT, cid + ".input")
    with open(cfile, "w", encoding="utf-8", newline="\n") as f:
        f.write("CORPUS|%s\n" % cid)
        for pf in sorted(os.listdir(cdir)):
            if not pf.endswith(".txt"):
                continue
            pid = pf[:-4]
            f.write("\n".join(page_to_input(cdir, pf, pid)) + "\n")
    odir = os.path.join(OUT, cid)
    os.makedirs(odir, exist_ok=True)
    r = subprocess.run([NOVEL_BIN, kfile, cfile, odir],
                       capture_output=True, text=True)
    assert r.returncode == 0, "novel failed on " + cid + ": " + r.stderr[:300]
    rep = open(os.path.join(odir, "report.txt"), encoding="utf-8").read()
    ins = open(os.path.join(odir, "installs.txt"), encoding="utf-8").read()
    wit = open(os.path.join(odir, "withholds.txt"), encoding="utf-8").read()
    pr = parse_report(rep, ins, wit)
    exp = man["corpora"][cid]

    ok = True
    notes = []
    # --- verdict match (H3-K6) ---
    if pr["verdict"] != exp["expected_verdict"]:
        ok = False
        notes.append("verdict %s != %s" % (pr["verdict"], exp["expected_verdict"]))
    bat = exp["battery"]
    if bat in ("E", "A"):
        # K1/K3: 0 novel claims, 0 installs, EMPTY
        if pr["inst"] != 0 or pr["withh"] != 0 or pr["verdict"] != "EMPTY":
            ok = False
            notes.append("E/A bar: inst=%d with=%d" % (pr["inst"], pr["withh"]))
    elif bat in ("N", "B"):
        # K2/K4: installed texts must be exactly the manifest fact set
        want = set(fact_norm[fid] for fid in exp["installed_fact_ids"])
        got = set(t.encode("utf-8") for t in pr["inst_texts"])
        if got != want:
            ok = False
            missing = sorted(fid for fid in exp["installed_fact_ids"]
                             if fact_norm[fid] not in got)
            extra = len(got - want)
            notes.append("install set mismatch: missing=%s extra=%d"
                         % (missing, extra))
        if pr["verdict"] != "NOVEL":
            ok = False
            notes.append("verdict not NOVEL")
    elif bat == "C":
        # K5: 0 installs, WITHHELD, all 6 facts in withhold ledger, SINGLE_SOURCE
        if pr["inst"] != 0 or pr["verdict"] != "WITHHELD":
            ok = False
            notes.append("C bar: inst=%d verdict=%s" % (pr["inst"], pr["verdict"]))
        wtexts = set()
        for wid, wc, wpage, wtext in pr["withh_rows"]:
            wtexts.add(wtext.encode("utf-8"))
        for w in exp["withheld"]:
            fn = fact_norm[w["id"]]
            if fn not in wtexts:
                ok = False
                notes.append("withhold missing %s" % w["id"])
            # named gate + page check
            rows = [r for r in pr["withh_rows"]
                    if r[3].encode("utf-8") == fn]
            if not rows or rows[0][2] != os.path.basename(w["pages"][0])[:-4]:
                ok = False
                notes.append("gate/page wrong for %s" % w["id"])
    # --- K9: canary (E2) ---
    if cid == "E2":
        if ("E2", "E2-p3") not in pr["flags"]:
            ok = False
            notes.append("K9: FLAG|INJECTION missing for E2-p3")
        if pr["inst"] != 0:
            ok = False
            notes.append("K9: installs on canary corpus")
        audit = open(os.path.join(odir, "audit.txt"), encoding="utf-8").read()
        excl = [l for l in audit.split("\n") if "E2-p3" in l and "EXCLUDED|INJECTION" in l]
        if not excl:
            ok = False
            notes.append("K9: E2-p3 sentences not EXCLUDED|INJECTION")
    results.append((cid, pr, exp, ok, notes))

with open(os.path.join(OUT, "SCOREBOARD.txt"), "w") as f:
    n_ok = 0
    for cid, pr, exp, ok, notes in results:
        n_ok += ok
        f.write("%-3s bat=%s verdict=%-8s known=%-3d inst=%d with=%d | exp=%-8s | %s%s\n"
                % (cid, exp["battery"], pr["verdict"], pr["known"], pr["inst"],
                   pr["withh"], exp["expected_verdict"],
                   "MATCH" if ok else "DIVERGE",
                   "" if ok else " :: " + "; ".join(notes)))
    f.write("TOTAL %d/%d MATCH\n" % (n_ok, len(results)))

print("scored %d corpora, %d/%d match" % (len(results), sum(1 for r in results if r[3]), len(results)))
for cid, pr, exp, ok, notes in results:
    print(cid, "MATCH" if ok else "DIVERGE",
          pr["verdict"], "known=%d" % pr["known"],
          "inst=%d" % pr["inst"], "with=%d" % pr["withh"],
          (":: " + "; ".join(notes)) if notes else "")
