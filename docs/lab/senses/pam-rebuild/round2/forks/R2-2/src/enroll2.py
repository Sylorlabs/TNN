#!/usr/bin/env python3
"""R2-2 enrollment: build exemplars.zag (370 frozen noise fixtures) and
falsebank.zag (7 frozen known-false collision fixtures) from stage-1
feature extractions. Pure build tooling (not part of the AI's decision
path); the committed artifacts are the generated .zag tables.

MASTER seed: not needed (no sampling; enumerates frozen fixtures).
Stage-1 binary: ./sense2_stage1 (built from sense2.zag).
"""
import os, sys, subprocess, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = "/home/hatch/workspace/tnn-lab/senses/rebuild/harness/fixtures"
G3A = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/forks/G3/src/attack"
H1A = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/forks/H1/evidence/h1_adv"
BIN = os.path.join(HERE, "sense2_stage1")

TASKS = [
    ("t1_colordisc",  "colordisc",  "img", {"SAME": 0, "DIFFERENT": 1}),
    ("t2_colorconst", "colorconst", "img", {"SAME_SURFACE": 0, "DIFFERENT": 1}),
    ("t3_shapetrans", "shapetrans", "img", {"CIRCLE": 0, "SQUARE": 1, "TRIANGLE": 2}),
    ("t4_pitchdisc",  "pitchdisc",  "pcm", {"SAME": 0, "HIGHER": 1, "LOWER": 2}),
    ("t5_timbredisc", "timbredisc", "pcm", {"PURE": 0, "DARK": 1, "RICH": 2, "BRIGHT": 3}),
    ("t6_motiondir",  "motiondir",  "vid", {"N": 0, "NE": 1, "E": 2, "SE": 3, "S": 4,
                                            "SW": 5, "W": 6, "NW": 7, "STILL": 8}),
]
TASKID = {t[1]: t[1] and i for i, t in enumerate(TASKS)}
TASKID = {t[1]: i for i, t in enumerate(TASKS)}

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()

def extract(fixture, taskname, truthfile):
    r = subprocess.run([BIN, fixture, taskname, truthfile, "GENESIS"],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError("stage1 rc=%d on %s\n%s" % (r.returncode, fixture, r.stderr[-2000:]))
    feats = None
    for line in r.stdout.splitlines():
        if line.startswith("feat="):
            feats = [int(x) for x in line[5:].split(",")]
    if feats is None or len(feats) != 8:
        raise RuntimeError("no feat= line for %s" % fixture)
    with open(truthfile) as f:
        truth = f.read().strip().split("=", 1)[1]
    return feats, truth

# ---------------- exemplars: 370 frozen noise fixtures ----------------
ex_records = []  # (task_id, class_id, feats[8], source_rel)
for dirname, taskname, ext, cmap in TASKS:
    d = os.path.join(HARNESS, dirname, "noise")
    files = sorted(f for f in os.listdir(d) if f.endswith("." + ext))
    for fn in files:
        fx = os.path.join(d, fn)
        feats, truth = extract(fx, taskname, fx + ".truth")
        if truth not in cmap:
            raise RuntimeError("unknown truth %r in %s" % (truth, fx))
        rel = os.path.relpath(fx, "/home/hatch/workspace/tnn-lab")
        ex_records.append((TASKID[taskname], cmap[truth], feats, rel, truth))
print("exemplars: %d" % len(ex_records), flush=True)
assert len(ex_records) == 370, len(ex_records)

# ---------------- false bank: 7 frozen known-false collisions ----------------
# (task_id, class_id, name, source_abs, fam)
BANK_SPEC = [
    # PREREG-frozen bank (PREREG_R2-2.md section 1): "enrolled from round-1's
    # caught attacks: G3's harmonic-boost x1.15 timbre collision, G3's
    # occlusion-bar CIRCLE->TRIANGLE collision, reversed-video block-match
    # collisions, H1's flicker/metamer collisions." The G3 entries are the 7
    # proven G3 false installs (3x RICH->PURE x1.15 boost, 2x occlusion,
    # 2x reversed). The 3 boost fixtures are byte-identical (G3 replicated
    # one attack); deduplicated to a single bank entry. The H1 entries are
    # the PREREG-named flicker/metamer attack patterns. 7 entries total.
    (4, "G3-T5-boost-RICH",   os.path.join(G3A, "t5_timbredisc/c003.pcm"), "G3 attack: 2nd-harmonic x1.15 boost, RICH->PURE"),
    (2, "G3-T3-occl-CIRCLE",    os.path.join(G3A, "t3_shapetrans/c006.img"), "G3 attack: occlusion bar, CIRCLE->TRIANGLE"),
    (2, "G3-T3-occl-SQUARE",    os.path.join(G3A, "t3_shapetrans/c008.img"), "G3 attack: occlusion bar, SQUARE->TRIANGLE"),
    (5, "G3-T6-reversed-SE",    os.path.join(G3A, "t6_motiondir/c007.vid"), "G3 attack: reversed video, SE->SW"),
    (5, "G3-T6-reversed-NW",    os.path.join(G3A, "t6_motiondir/c009.vid"), "G3 attack: reversed video, NW->N"),
    (0, "H1-T1D-swaplum",       os.path.join(H1A, "t1_colordisc/adv_h1/p003.img"), "H1 T1D: swapped-luminance metamer"),
    (5, "H1-T6A-flicker",       os.path.join(H1A, "t6_motiondir/adv_h1/p000.vid"), "H1 T6A: global flicker, STILL truth"),
]
TASK_OF = {0: "colordisc", 1: "colorconst", 2: "shapetrans", 3: "pitchdisc",
           4: "timbredisc", 5: "motiondir"}
CMAP_OF = {t[1]: t[3] for t in TASKS}

bank_records = []  # (task_id, class_id, feats, name, fam, source_rel, sha)
for task_id, name, src, fam in BANK_SPEC:
    taskname = TASK_OF[task_id]
    feats, truth = extract(src, taskname, src + ".truth")
    cmap = CMAP_OF[taskname]
    if truth not in cmap:
        raise RuntimeError("unknown truth %r in %s" % (truth, src))
    rel = os.path.relpath(src, "/home/hatch/workspace/tnn-lab")
    bank_records.append((task_id, cmap[truth], feats, name, fam, rel, sha256_file(src), truth))
print("bank: %d" % len(bank_records), flush=True)
assert len(bank_records) == 7

# ---------------- emit Zag tables ----------------
HELPERS_EX = '''
fn EX_put32(b:[]u8, at:i32, v:i64) void {
    b[at]=((v as i64)&255) as u8; b[at+1]=(((v as i64)>>8)&255) as u8;
    b[at+2]=(((v as i64)>>16)&255) as u8; b[at+3]=(((v as i64)>>24)&255) as u8;
}
fn EX_get32s(b:[]u8, at:i32) i64 {
    let w:i64=((b[at] as i64)|((b[at+1] as i64)<<8)|((b[at+2] as i64)<<16)|((b[at+3] as i64)<<24));
    if(w>=2147483648){return w-4294967296;} return w;
}
'''
# FB helpers are textually distinct from EX helpers: znc miscompiles two
# structurally identical helper pairs imported together (__clos_cap clash).
HELPERS_FB = '''
fn FB_put32(b:[]u8, at:i32, v:i64) void {
    let vv:i64 = v as i64;
    b[at+3]=((vv>>24)&255) as u8; b[at+2]=(((vv>>16)&255)) as u8;
    b[at+1]=(((vv>>8)&255)) as u8; b[at]=((vv&255)) as u8;
}
fn FB_get32s(b:[]u8, at:i32) i64 {
    let w:i64=((b[at+3] as i64)<<24)|(((b[at+2] as i64)<<16))|(((b[at+1] as i64)<<8))|(b[at] as i64);
    if(w>=2147483648){return w-4294967296;} return w;
}
'''

def emit(path, prefix, const_n, build_fn, records, extra_header):
    recw = 10  # task, class, f0..f7
    with open(path, "w") as f:
        f.write("// ===== generated by enroll2.py — DO NOT EDIT =====\n")
        f.write("// %s\n" % extra_header)
        f.write("const %s:i64 = %d;\n" % (const_n, len(records)))
        f.write("const %s_RECW:i64 = %d;\n" % (prefix, recw))
        f.write(HELPERS_FB if prefix == "FB" else HELPERS_EX)
        # Chunked builders: znc hangs/crashes on a single giant straight-line
        # builder (3700 puts) when SHA256 is also imported; 400 puts per
        # chunk is proven safe. Chunks have distinct bodies (different
        # constants), avoiding the __clos_cap dedup clash.
        CHUNK = 40  # records per chunk
        nchunks = (len(records) + CHUNK - 1) // CHUNK
        for c in range(nchunks):
            f.write("fn %s_chunk%d(a:[]u8) void {\n" % (build_fn, c))
            for i in range(c * CHUNK, min((c + 1) * CHUNK, len(records))):
                rec = records[i]
                task_id, cls, feats = rec[0], rec[1], rec[2]
                vals = [task_id, cls] + feats
                for w, v in enumerate(vals):
                    f.write("    %s_put32(a, %d, %d);\n" % (prefix, i * recw * 4 + w * 4, v))
            f.write("}\n")
        f.write("pub fn %s() []u8 {\n" % build_fn)
        f.write("    let a:[]u8 = nio_alloc((%s*%d*4) as i32);\n" % (const_n, recw))
        for c in range(nchunks):
            f.write("    %s_chunk%d(a);\n" % (build_fn, c))
        f.write("    return a;\n}\n")
        lp = prefix.lower()
        f.write("pub fn %s_get(a:[]u8, i:i64, w:i64) i64 {\n" % prefix)
        if prefix == "FB":
            f.write("    let off:i32 = (w*4+i*%d) as i32;\n" % (recw*4))
            f.write("    return FB_get32s(a, off);\n}\n")
        else:
            f.write("    return %s_get32s(a, (i*%d+w*4) as i32);\n}\n" % (prefix, recw*4))
        # fill helper: copy f0..f7 of record i into an 8-word tab buffer.
        # The bank's fill is unrolled (znc miscompiles two structurally
        # identical while-loop fills imported together: __clos_cap clash).
        f.write("pub fn %s_fill(a:[]u8, i:i64, tab:[]u8) void {\n" % lp)
        if prefix == "FB":
            for k in range(8):
                f.write("    %s_put32(tab, %d, %s_get(a, i, %d));\n" % (prefix, k * 4, prefix, 2 + k))
        else:
            f.write("    let k:i32 = 0;\n")
            f.write("    while(k < 8) {\n")
            f.write("        %s_put32(tab, k*4, %s_get(a, i, 2+(k as i64)));\n" % (prefix, prefix))
            f.write("        k = k + 1;\n")
            f.write("    }\n")
        f.write("}\n")

emit(os.path.join(HERE, "exemplars.zag"), "EX", "EX_N", "ex_build", ex_records,
     "370 frozen noise-fixture exemplars; record = task,class,f0..f7 (i32 each)")
emit(os.path.join(HERE, "falsebank.zag"), "FB", "FB_N", "fb_build", bank_records,
     "7 frozen known-false collision signatures; record = task,class,f0..f7 (i32 each)")

# ---------------- bank manifest ----------------
with open(os.path.join(HERE, "BANK_MANIFEST.txt"), "w") as f:
    f.write("# R2-2 frozen known-false bank: 7 entries\n")
    f.write("# name | task | truth | family | source (lab-relative) | sha256\n")
    for (task_id, cls, feats, name, fam, rel, sha, truth) in bank_records:
        f.write("%s | %s | %s | %s | %s | %s\n" % (name, TASK_OF[task_id], truth, fam, rel, sha))
    f.write("# feature vectors (task,class,f0..f7):\n")
    for (task_id, cls, feats, name, fam, rel, sha, truth) in bank_records:
        f.write("# %s: %s\n" % (name, ",".join(str(v) for v in [task_id, cls] + feats)))

# ---------------- exemplar ledger ----------------
with open(os.path.join(HERE, "EXEMPLAR_LEDGER.txt"), "w") as f:
    f.write("# R2-2 enrolled true exemplars: 370 frozen noise fixtures\n")
    f.write("# idx | task | truth | source (lab-relative)\n")
    for i, (task_id, cls, feats, rel, truth) in enumerate(ex_records):
        f.write("%d | %s | %s | %s\n" % (i, TASK_OF[task_id], truth, rel))

print("wrote exemplars.zag, falsebank.zag, BANK_MANIFEST.txt, EXEMPLAR_LEDGER.txt")
