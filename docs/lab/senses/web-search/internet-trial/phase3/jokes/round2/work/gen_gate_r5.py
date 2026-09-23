#!/usr/bin/env python3
"""Round-5 gate fixture + classifier generator (TRANSPORT ONLY).

Reads the FROZEN round-2 held-out corpus + blind helper judgments, verifies
their SHAs against corpus/HELDOUT_SHA256.txt / HELPER_SHA256.txt, verifies
every helper cited marker is a verbatim substring of the folded item text,
and emits per-config build trees:

  ~/workspace/r5_build/<cfg>/g_corpus.zag   (folded texts/urls, 64 items)
  ~/workspace/r5_build/<cfg>/g_helper.zag   (blind helper intents+markers)
  ~/workspace/r5_build/<cfg>/g_intent.zag    (contradiction-first classifier)
  ~/workspace/r5_build/<cfg>/r5_r6.zag       (R6 composition bridge)
  + copies of j_ledger.zag, g_trial.zag, R33_NATIVE_IO_V1.zag,
    R33_NATIVE_SHA256_V2.zag (frozen round-1 infrastructure, unchanged)

and work/gate_manifest_r5.json for the Python scorer.

Configs:
  A: all 32 patterns, all 323 phrases.
  B: only patterns with >=4 distinct training groups (P_DA3E); all phrases.
  C: training-provenance-only: 14 (T) patterns, 275 phrases (48 H dropped).

The classifier (pure Zag, zero RNG, deterministic):
  1. whole-word phrase->code matching on folded text (j_has_word)
  2. contradiction patterns (conjunctions) in table order, first fire wins
  3. R6 bridge (r5_r6.zag, r6_apply semantics verbatim from
     repairs/src/r6.zag): CONTRADICTS->JOKING overrides evidence;
     SUPPORTS cannot install; UNKNOWN defers to evidence (SAT>=2 -> SATIRE,
     TROPE>=1 -> JOKING, else UNCERTAIN). SINCERE/DECEPTIVE never emitted.
Python never touches a decision path: it only generates sources and scores.
"""
import json, re, os, sys, hashlib, shutil, copy

HERE = os.path.dirname(os.path.abspath(__file__))
R2 = os.path.dirname(HERE)
JOKES = os.path.dirname(R2)
BUILD = os.path.expanduser("~/workspace/r5_build")

INTENT_CODE = {"SINCERE": 1, "JOKING": 2, "SATIRE": 3, "DECEPTIVE": 4,
               "UNCERTAIN": 5}

SAT = ("area sources confirm says experts inside resident details developing "
       "press weigh study finds local time report full man woman peer pending "
       "review story nobody").split()
TROPE = "free ram upgrade ama findings joke pet downloaded traveler".split()

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def fold(s):
    s = s.lower()
    out = [ch if 32 <= ord(ch) <= 126 else " " for ch in s]
    return re.sub(r"\s+", " ", "".join(out)).strip()

def zag_esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')

def emit_str_fn(lines, prefix, name, vals):
    lines.append(f"fn {prefix}{name}(i:i32)[]u8 {{")
    for idx, v in enumerate(vals):
        lines.append(f'    if(i=={idx}){{return "{zag_esc(v)}";}}')
    lines.append('    return "";')
    lines.append("")
    lines.append("}")

def emit_int_fn(lines, prefix, name, vals):
    lines.append(f"fn {prefix}{name}(i:i32)i32 {{")
    for idx, v in enumerate(vals):
        lines.append(f"    if(i=={idx}){{return {v};}}")
    lines.append("    return 0;")
    lines.append("}")

def main():
    hp = os.path.join(R2, "corpus", "heldout.json")
    ep = os.path.join(R2, "corpus", "helper.json")
    hs = sha256_file(hp)
    es = sha256_file(ep)
    frozen_h = open(os.path.join(R2, "corpus", "HELDOUT_SHA256.txt")).read().strip()
    frozen_e = open(os.path.join(R2, "corpus", "HELPER_SHA256.txt")).read().strip()
    assert hs == frozen_h, f"heldout SHA mismatch: {hs} vs {frozen_h}"
    assert es == frozen_e, f"helper SHA mismatch: {es} vs {frozen_e}"
    print(f"frozen inputs verified: heldout {hs[:16]}... helper {es[:16]}...")

    held = json.load(open(hp, encoding="utf-8"))["items"]
    helpj = json.load(open(ep, encoding="utf-8"))["judgments"]
    assert len(held) == 64 and len(helpj) == 64
    hmap = {j["id"]: j for j in helpj}
    assert [it["id"] for it in held] == [j["id"] for j in helpj], "id order mismatch"

    flags = json.load(open(os.path.join(HERE, "provenance_flags.json"), encoding="utf-8"))
    phrases_all = json.load(open(os.path.join(HERE, "phrases_r4.json"), encoding="utf-8"))
    patterns_all = json.load(open(os.path.join(HERE, "patterns_r2.json"), encoding="utf-8"))

    configs = {}
    # A: everything
    configs["A"] = (copy.deepcopy(phrases_all), list(patterns_all.keys()))
    # B: support rule
    configs["B"] = (copy.deepcopy(phrases_all), list(flags["configB_patterns"]))
    # C: training provenance only
    phc = copy.deepcopy(phrases_all)
    hph = set(flags["H_phrases"])
    for grp in ("actions", "facts"):
        for code in phc[grp]:
            phc[grp][code] = [p for p in phc[grp][code] if p not in hph]
    configs["C"] = (phc, [p for p in patterns_all if p not in flags["H_patterns"]])

    manifest = []
    texts, urls, cats, ids = [], [], [], []
    for it in held:
        t, u = fold(it["text"]), fold(it["url"])
        texts.append(t); urls.append(u); cats.append(it["arm"]); ids.append(it["id"])
        manifest.append({"id": it["id"], "arm": it["arm"], "sub": it["sub"],
                         "text": t, "url": u, "label": it["label"]})
    with open(os.path.join(HERE, "gate_manifest_r5.json"), "w", encoding="utf-8") as f:
        json.dump({"items": manifest}, f, indent=1)
    print("wrote work/gate_manifest_r5.json")

    # helper fixture (shared across configs)
    bad = []
    intents, markers = [], []
    for it in held:
        j = hmap[it["id"]]
        m = fold(j["cited"])
        if m not in fold(it["text"]):
            bad.append((it["id"], j["cited"]))
        intents.append(INTENT_CODE[j["helper_intent"]])
        markers.append(m)
    if bad:
        for b in bad:
            print(f"MARKER NOT SUBSTRING: {b}", file=sys.stderr)
        sys.exit("FATAL: helper marker(s) not verbatim substrings of folded text")
    print(f"helper markers verified: {len(markers)} substrings OK")

    frozen_src = ["j_ledger.zag", "g_trial.zag",
                  "R33_NATIVE_IO_V1.zag", "R33_NATIVE_SHA256_V2.zag"]
    for cfg, (phrases, active) in configs.items():
        d = os.path.join(BUILD, cfg)
        os.makedirs(d, exist_ok=True)
        for fn in frozen_src:
            shutil.copy(os.path.join(JOKES, "src", fn), os.path.join(d, fn))
        # g_corpus.zag
        L = ["// GENERATED by round2/work/gen_gate_r5.py — frozen round-2 corpus; do not hand-edit.", ""]
        L.append(f"fn g_nitems()i32 {{ return {len(held)}; }}")
        L.append("")
        emit_str_fn(L, "g_", "id", ids)
        emit_str_fn(L, "g_", "cat", cats)
        emit_str_fn(L, "g_", "text", texts)
        emit_str_fn(L, "g_", "url", urls)
        open(os.path.join(d, "g_corpus.zag"), "w", encoding="utf-8").write("\n".join(L))
        # g_helper.zag
        L = ["// GENERATED by round2/work/gen_gate_r5.py — frozen blind helper; do not hand-edit.", ""]
        L.append(f"fn g_h_n()i32 {{ return {len(held)}; }}")
        L.append("")
        emit_int_fn(L, "g_", "h_intent", intents)
        emit_str_fn(L, "g_", "h_marker", markers)
        open(os.path.join(d, "g_helper.zag"), "w", encoding="utf-8").write("\n".join(L))
        # r5_r6.zag — R6 composition bridge (r6_apply verbatim from repairs/src/r6.zag)
        L = [
            "// r5_r6.zag — R6 mechanistic-layer composition bridge (pure Zag).",
            "// r6_apply is VERBATIM from phase3/repairs/src/r6.zag (r6_logic's seeded",
            "// C15/C16 verdicts are claim-domain and do not apply here; the joke domain",
            "// supplies its own logic verdict from contradiction detection).",
            "// Semantics: CONTRADICTS(2) overrides evidence; SUPPORTS(1) cannot override",
            "// a WITHHOLD gate; UNKNOWN(0) defers to the evidence disposition.",
            "",
            "fn r6_apply(logic_verdict:i32,gated:i32,evidence_disp:i32)i32{",
            "    if(logic_verdict==2){",
            "        return 3;",
            "    }",
            "    if(logic_verdict==1){",
            "        if(gated!=0){return 4;}",
            "        return evidence_disp;",
            "    }",
            "    return evidence_disp;",
            "}",
            "",
            "// Joke-domain adapter. logic: 2=contradiction fired, 1=marker evidence,",
            "// 0=none. ev: evidence intent (3=SATIRE,2=JOKING,5=UNCERTAIN).",
            "// gated=1 always: the install gate (SINCERE->INSTALL else WITHHOLD) is",
            "// separate and the classifier never emits SINCERE, so marker SUPPORTS",
            "// can never install — the R6 'SUPPORTS cannot override WITHHOLD' property.",
            "fn r5_dispose(logic:i32,ev:i32)i32{",
            "    if(logic==2){return 2;}",
            "    let d:i32=r6_apply(logic,1,ev);",
            "    if(d==4){return ev;}",
            "    return d;",
            "}",
            "",
        ]
        open(os.path.join(d, "r5_r6.zag"), "w", encoding="utf-8").write("\n".join(L))
        # g_intent.zag — contradiction-first classifier
        L = [f"// GENERATED by round2/work/gen_gate_r5.py — config {cfg}; do not hand-edit.",
             f"// Config {cfg}: {len(active)} active patterns, "
             f"{sum(len(v) for g in ('actions','facts') for v in phrases[g].values())} phrases.",
             "// Rule: contradiction pattern -> JOKING (R6 CONTRADICTS overrides);",
             "// elif SAT>=2 -> SATIRE; elif TROPE>=1 -> JOKING; else UNCERTAIN.",
             "// SINCERE(1)/DECEPTIVE(4) never emitted. Pure Zag; zero RNG.",
             "",
             '@import("j_ledger.zag")',
             '@import("r5_r6.zag")',
             "",
             "fn g_codes_append(codes:[]u8,tok:[]u8)void {",
             "    let n:i32=j_cstrlen(codes);",
             "    if(n>0){codes[n]=43;n=n+1;}",
             "    let i:i32=0;",
             "    while(i<tok.len){codes[n+i]=tok[i];i=i+1;}",
             "    codes[n+tok.len]=0;",
             "    return;",
             "}",
             "",
             "fn g_markers_append(markers:[]u8,mk:[]u8)void {",
             "    let n:i32=j_cstrlen(markers);",
             "    let i:i32=0;",
             "    while(i<mk.len){markers[n+i]=mk[i];i=i+1;}",
             "    markers[n+mk.len]=126;",
             "    markers[n+mk.len+1]=0;",
             "    return;",
             "}",
             "",
             "fn g_classify(text:[]u8,url:[]u8,codes:[]u8,markers:[]u8)i32 {",
             "    let t:[]u8=j_tolower(text);"]
        # per-code phrase matching
        for grp in ("actions", "facts"):
            for code, plist in phrases[grp].items():
                L.append(f"    let n_{code}:i32=0;")
                for p in plist:
                    pf = fold(p)
                    assert pf and all(32 <= ord(c) <= 126 for c in pf), pf
                    pe = zag_esc(pf)
                    L.append(f'    if(j_has_word(t,"{pe}")!=0){{n_{code}=n_{code}+1;g_markers_append(markers,"{pe}");}}')
        # contradiction patterns, first fire wins
        L.append("    let contra:i32=0;")
        for idx, pname in enumerate(patterns_all.keys(), start=1):
            if pname not in active:
                continue
            when = patterns_all[pname]["when"]
            cond = "&&".join([f"n_{c}>=1" for c in when])
            L.append(f'    if(contra==0){{if({cond}){{contra={idx};g_codes_append(codes,"{pname}");}}}}')
        # SAT / TROPE evidence
        L.append("    let ns:i32=0;")
        for w in SAT:
            L.append(f'    if(j_has_word(t,"{w}")!=0){{ns=ns+1;g_markers_append(markers,"{w}");}}')
        L.append("    let nt:i32=0;")
        for w in TROPE:
            L.append(f'    if(j_has_word(t,"{w}")!=0){{nt=nt+1;g_markers_append(markers,"{w}");}}')
        L += [
            "    let ev:i32=5;",
            "    if(ns>=2){ev=3;g_codes_append(codes,\"R_SATIRE\");}",
            "    if(ev==5){",
            "        if(nt>=1){ev=2;g_codes_append(codes,\"R_TROPE\");}",
            "    }",
            "    if(ev==5){",
            "        if(contra==0){g_codes_append(codes,\"R_NO_PATTERN\");}",
            "    }",
            "    let logic:i32=0;",
            "    if(contra!=0){logic=2;}",
            "    if(logic==0){",
            "        if(ev!=5){logic=1;}",
            "    }",
            "    let intent:i32=r5_dispose(logic,ev);",
            "    return intent;",
            "}",
            "",
        ]
        open(os.path.join(d, "g_intent.zag"), "w", encoding="utf-8").write("\n".join(L))
        nph = sum(len(v) for g in ("actions", "facts") for v in phrases[g].values())
        print(f"config {cfg}: {d} ({len(active)} patterns, {nph} phrases)")

if __name__ == "__main__":
    main()
