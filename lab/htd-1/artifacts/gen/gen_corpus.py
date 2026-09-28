#!/usr/bin/env python3
"""HTD-1 R3 frozen artifact generator — corpus-derived batteries.

Reads corpora IN PLACE (never copies them):
  ~/workspace/tnn-lab/corpora/pg100.txt
  ~/workspace/tnn-lab/corpora/sqlite3.c
Writes frozen artifacts to ~/workspace/htd-1/artifacts/.

Deterministic: no randomness anywhere. Re-running must produce
byte-identical files (verified by sha256 comparison after generation).
"""
import hashlib
import json
import os
import re
import sys

CORP_PG = os.path.expanduser("~/workspace/tnn-lab/corpora/pg100.txt")
CORP_SQ = os.path.expanduser("~/workspace/tnn-lab/corpora/sqlite3.c")
ART = os.path.expanduser("~/workspace/htd-1/artifacts")
os.makedirs(ART, exist_ok=True)

pg = open(CORP_PG, "rb").read()
sq = open(CORP_SQ, "rb").read()
print("pg100 bytes:", len(pg), file=sys.stderr)
print("sqlite3.c bytes:", len(sq), file=sys.stderr)
print("pg100 sha256:", hashlib.sha256(pg).hexdigest(), file=sys.stderr)
print("sqlite3.c sha256:", hashlib.sha256(sq).hexdigest(), file=sys.stderr)

CHUNK = 4096

def chunk_bounds(data):
    """Frozen 4KB line-aligned chunking.

    chunk 0 starts at 0. chunk i ends at the first byte AFTER the first
    '\\n' at position >= start_i + 4096 (end-exclusive). Last chunk ends
    at len(data). Returns list of (start, end).
    """
    bounds = []
    s = 0
    n = len(data)
    while s < n:
        target = s + CHUNK
        j = data.find(b"\n", target)
        e = (j + 1) if j != -1 else n
        bounds.append((s, e))
        s = e
    return bounds

PG_CHUNKS = chunk_bounds(pg)
SQ_CHUNKS = chunk_bounds(sq)
print("pg chunks:", len(PG_CHUNKS), "sq chunks:", len(SQ_CHUNKS), file=sys.stderr)

def find_all(data, needle):
    """All byte offsets of needle (half-open [start,end))."""
    out = []
    nb = needle.encode("utf-8")
    i = data.find(nb)
    while i != -1:
        out.append([i, i + len(nb)])
        i = data.find(nb, i + 1)
    return out

def chunks_containing(data, chunks, offsets):
    ids = set()
    for (s, e) in offsets:
        # binary search-free linear scan is fine at this scale
        for ci, (cs, ce) in enumerate(chunks):
            if cs <= s < ce or cs < e <= ce or (s <= cs and ce <= e):
                ids.add(ci)
    return sorted(ids)

# ---------------------------------------------------------------------------
# CORPUS-QA-60
# ---------------------------------------------------------------------------
# Each question: (qid, corpus, kind, question, answer, anchors[list of exact
# corpus strings]). Ground truth is computed, not hand-written: the union of
# chunks containing any anchor occurrence, plus exact anchor byte offsets.
QA = [
 # pg100 lookup (15)
 ("q_pg_l01","pg100","lookup","In which play does the line 'To be, or not to be' appear?","Hamlet",["To be, or not to be"]),
 ("q_pg_l02","pg100","lookup","Which character speaks the line 'All the world\u2019s a stage'?","Jaques, in As You Like It",["All the world\u2019s a stage"]),
 ("q_pg_l03","pg100","lookup","In which play does the line 'Now is the winter of our discontent' appear?","Richard III",["Now is the winter of our discontent"]),
 ("q_pg_l04","pg100","lookup","Which character says 'Friends, Romans, countrymen, lend me your ears'?","Mark Antony, in Julius Caesar",["Friends, Romans, countrymen, lend me your ears"]),
 ("q_pg_l05","pg100","lookup","In which play does the line 'A horse! A horse! My kingdom for a horse!' appear?","Richard III",["My kingdom for a horse"]),
 ("q_pg_l06","pg100","lookup","Who says 'This above all: to thine own self be true'?","Polonius, in Hamlet",["to thine own self be true"]),
 ("q_pg_l07","pg100","lookup","In which play does the line 'Parting is such sweet sorrow' appear?","Romeo and Juliet",["Parting is such sweet sorrow"]),
 ("q_pg_l08","pg100","lookup","Which play contains the line 'Wormwood, wormwood', spoken aside during the play within the play?","Hamlet",["Wormwood, wormwood"]),
 ("q_pg_l09","pg100","lookup","Who says 'Cry \u201cHavoc!\u201d and let slip the dogs of war'?","Mark Antony, in Julius Caesar",["let slip the dogs of war"]),
 ("q_pg_l10","pg100","lookup","In which work does the sonnet opening 'Shall I compare thee to a summer\u2019s day?' appear?","Sonnet 18, in the Sonnets",["Shall I compare thee to a summer\u2019s day"]),
 ("q_pg_l11","pg100","lookup","Which character asks 'But soft, what light through yonder window breaks?'","Romeo, in Romeo and Juliet",["what light through yonder window breaks"]),
 ("q_pg_l12","pg100","lookup","In which play does the chant 'Double, double, toil and trouble' appear?","Macbeth",["Double, double, toil and trouble"]),
 ("q_pg_l13","pg100","lookup","Who says 'All that glisters is not gold'?","The Prince of Morocco, in The Merchant of Venice",["All that glisters is not gold"]),
 ("q_pg_l14","pg100","lookup","In which play does the line 'O Romeo, Romeo! wherefore art thou Romeo?' appear?","Romeo and Juliet",["wherefore art thou Romeo"]),
 ("q_pg_l15","pg100","lookup","Which character says 'The quality of mercy is not strain\u2019d'?","Portia, in The Merchant of Venice",["The quality of mercy is not strain\u2019d"]),
 # pg100 discovery (15)
 ("q_pg_d01","pg100","discovery","Which play opens with a ship at sea in a storm, the stage direction calling for thunder and lightning?","The Tempest",["a tempestuous noise of thunder and lightning"]),
 ("q_pg_d02","pg100","discovery","A murdered king describes poison poured into his ears as he slept in his orchard. Name the play.","Hamlet",["porches of my ears"]),
 ("q_pg_d03","pg100","discovery","Which heroine disguises herself as the page Cesario?","Viola, in Twelfth Night",["Cesario"]),
 ("q_pg_d04","pg100","discovery","A prince holds a jester\u2019s skull and speaks to it by name. Name the play.","Hamlet",["Alas, poor Yorick"]),
 ("q_pg_d05","pg100","discovery","Which play is set in large part in the forest of Arden?","As You Like It",["forest of Arden"]),
 ("q_pg_d06","pg100","discovery","A bond demands a pound of flesh as forfeit. Name the play.","The Merchant of Venice",["pound of flesh"]),
 ("q_pg_d07","pg100","discovery","Which prince claims he will put an antic disposition on after encountering a ghost?","Hamlet",["put an antic disposition on"]),
 ("q_pg_d08","pg100","discovery","The prologue describes 'a pair of star-cross\u2019d lovers' who take their lives. Name the play.","Romeo and Juliet",["star-cross\u2019d lovers take their life"]),
 ("q_pg_d09","pg100","discovery","Three figures chant over a cauldron about toil and trouble. Name the play.","Macbeth",["Double, double, toil and trouble"]),
 ("q_pg_d10","pg100","discovery","A general is warned that jealousy is 'the green-ey\u2019d monster which doth mock the meat it feeds on'. Name the play.","Othello",["monster which doth mock"]),
 ("q_pg_d11","pg100","discovery","An old king, betrayed by his daughters, laments how much sharper than a serpent\u2019s tooth it is to have a thankless child. Name the play.","King Lear",["sharper than a serpent\u2019s tooth"]),
 ("q_pg_d12","pg100","discovery","A fairy king and queen quarrel over a changeling boy. Name the play.","A Midsummer Night\u2019s Dream",["changeling"]),
 ("q_pg_d13","pg100","discovery","A sea-captain tells a young woman her brother may be in Elysium after a shipwreck. Name the play.","Twelfth Night",["in Elysium"]),
 ("q_pg_d14","pg100","discovery","Which history play dramatizes the Battle of Agincourt?","Henry V",["Agincourt"]),
 ("q_pg_d15","pg100","discovery","A character asks 'Hath not a Jew eyes?' in defense of shared humanity. Name the play.","The Merchant of Venice",["Hath not a Jew eyes"]),
 # sqlite3.c lookup (15)
 ("q_sq_l01","sqlite3.c","lookup","Which amalgamation file defines the function sqlite3BtreeOpen?","btree.c",["sqlite3BtreeOpen"]),
 ("q_sq_l02","sqlite3.c","lookup","In which amalgamation file is the SQLITE_CORRUPT result code defined?","sqlite3.h",["#define SQLITE_CORRUPT"]),
 ("q_sq_l03","sqlite3.c","lookup","Name an amalgamation file that defines the function sqlite3PagerOpen.","os-independent: pager.c (also declared in pager.h)",["sqlite3PagerOpen"]),
 ("q_sq_l04","sqlite3.c","lookup","Which amalgamation file defines the function sqlite3VdbeExec?","vdbe.c",["sqlite3VdbeExec"]),
 ("q_sq_l05","sqlite3.c","lookup","Name an amalgamation file that defines the function sqlite3OsOpen.","os_unix.c (also os_win.c)",["sqlite3OsOpen"]),
 ("q_sq_l06","sqlite3.c","lookup","In which amalgamation file is the sqlite3 database-connection struct defined?","sqliteInt.h",["struct sqlite3 {"]),
 ("q_sq_l07","sqlite3.c","lookup","Which amalgamation file defines the function sqlite3_backup_init?","backup.c",["sqlite3_backup_init"]),
 ("q_sq_l08","sqlite3.c","lookup","Which amalgamation file defines the function sqlite3VdbeMakeLabel?","vdbeaux.c",["sqlite3VdbeMakeLabel"]),
 ("q_sq_l09","sqlite3.c","lookup","In which amalgamation file is SQLITE_VERSION defined?","sqlite3.h",["#define SQLITE_VERSION"]),
 ("q_sq_l10","sqlite3.c","lookup","Which amalgamation file defines the function sqlite3_mutex_alloc?","mutex.c",["sqlite3_mutex_alloc"]),
 ("q_sq_l11","sqlite3.c","lookup","In which amalgamation file is SQLITE_OK defined?","sqlite3.h",["#define SQLITE_OK"]),
 ("q_sq_l12","sqlite3.c","lookup","In which amalgamation file is SQLITE_NOMEM defined?","sqlite3.h",["#define SQLITE_NOMEM"]),
 ("q_sq_l13","sqlite3.c","lookup","Which amalgamation file defines the function sqlite3_malloc?","malloc.c",["sqlite3_malloc("]),
 ("q_sq_l14","sqlite3.c","lookup","Which amalgamation file defines the BtCursor struct?","btreeInt.h",["typedef struct BtCursor"]),
 ("q_sq_l15","sqlite3.c","lookup","Which amalgamation file implements the function sqlite3_step?","vdbeapi.c",["sqlite3_step("]),
 # sqlite3.c discovery (15)
 ("q_sq_d01","sqlite3.c","discovery","A single public API translates a SQLite result code into English text. Name it.","sqlite3_errstr",["sqlite3_errstr"]),
 ("q_sq_d02","sqlite3.c","discovery","Which public API opens a database connection given a filename?","sqlite3_open",["sqlite3_open("]),
 ("q_sq_d03","sqlite3.c","discovery","Name the API that destroys a prepared statement and frees its resources.","sqlite3_finalize",["sqlite3_finalize"]),
 ("q_sq_d04","sqlite3.c","discovery","Which internal function acquires a B-tree handle\u2019s mutex before the handle is used?","sqlite3BtreeEnter",["sqlite3BtreeEnter"]),
 ("q_sq_d05","sqlite3.c","discovery","Which pager function performs phase one of a hot-journal commit?","sqlite3PagerCommitPhaseOne",["sqlite3PagerCommitPhaseOne"]),
 ("q_sq_d06","sqlite3.c","discovery","Which VDBE helper appends an opcode to the program under construction?","sqlite3VdbeAddOp",["sqlite3VdbeAddOp"]),
 ("q_sq_d07","sqlite3.c","discovery","Which OS-interface function deletes a database file?","sqlite3OsDelete",["sqlite3OsDelete"]),
 ("q_sq_d08","sqlite3.c","discovery","Name the C function that implements the SQL length() function.","lengthFunc",["lengthFunc"]),
 ("q_sq_d09","sqlite3.c","discovery","Which internal struct represents an open B-tree cursor?","BtCursor",["typedef struct BtCursor"]),
 ("q_sq_d10","sqlite3.c","discovery","Which public API registers a custom SQL function with a database connection?","sqlite3_create_function",["sqlite3_create_function"]),
 ("q_sq_d11","sqlite3.c","discovery","Which public API binds a UTF-8 text value to a prepared-statement parameter?","sqlite3_bind_text",["sqlite3_bind_text"]),
 ("q_sq_d12","sqlite3.c","discovery","Which internal routine appends formatted text to a dynamic string accumulator?","sqlite3_str_appendf",["sqlite3_str_appendf"]),
 ("q_sq_d13","sqlite3.c","discovery","Name the function that initializes the global mutex subsystem.","sqlite3MutexInit",["sqlite3MutexInit"]),
 ("q_sq_d14","sqlite3.c","discovery","Which public API returns the number of rows modified by the most recently completed statement?","sqlite3_changes",["sqlite3_changes"]),
 ("q_sq_d15","sqlite3.c","discovery","Which C function implements the BINARY collation comparison?","binCollFunc",["binCollFunc"]),
]

assert len(QA) == 60
lk = sum(1 for q in QA if q[2] == "lookup")
di = sum(1 for q in QA if q[2] == "discovery")
assert lk == 30 and di == 30, (lk, di)
pgq = [q for q in QA if q[1] == "pg100"]
sqq = [q for q in QA if q[1] == "sqlite3.c"]
assert len(pgq) == 30 and len(sqq) == 30
assert sum(1 for q in pgq if q[2]=="lookup") == 15
assert sum(1 for q in sqq if q[2]=="lookup") == 15

recs = []
failures = []
for (qid, corpus, kind, question, answer, anchors) in QA:
    data = pg if corpus == "pg100" else sq
    chunks = PG_CHUNKS if corpus == "pg100" else SQ_CHUNKS
    all_off = []
    for a in anchors:
        off = find_all(data, a)
        if not off:
            failures.append((qid, a))
        all_off.extend(off)
    all_off.sort()
    cids = chunks_containing(data, chunks, all_off)
    gt_chunks = [[chunks[c][0], chunks[c][1]] for c in cids]
    recs.append({
        "q_id": qid,
        "corpus": corpus,
        "kind": kind,
        "question": question,
        "answer": answer,
        "anchors": anchors,
        "n_anchor_occurrences": len(all_off),
        "gt_anchor_byte_offsets": all_off,
        "gt_chunk_ids": cids,
        "gt_chunk_byte_offsets": gt_chunks,
        "chunk_rule": "4KB line-aligned: chunk i covers [start_i,end_i); start_0=0; end_i = first byte after first '\\n' at position >= start_i+4096 (EOF if none). Offsets are half-open [start,end).",
    })

if failures:
    print("ANCHOR FAILURES:", file=sys.stderr)
    for qid, a in failures:
        print(" ", qid, repr(a), file=sys.stderr)
    sys.exit(1)

with open(os.path.join(ART, "corpus_qa_60.jsonl"), "w", encoding="utf-8") as f:
    for r in recs:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote corpus_qa_60.jsonl (60)", file=sys.stderr)

# ---------------------------------------------------------------------------
# D-P1 — 600 passage-attribution items (4 plays x 150)
# ---------------------------------------------------------------------------
# Play regions: body banner = exact title line with NO leading whitespace.
# Titles are taken from the Contents list (indented lines) so the title set
# is derived from the corpus itself, not hand-written. Region for play P =
# [byte offset of P's body banner line start, byte offset of the NEXT play's
# body banner line start). Attribution rule: enclosing region.
lines = pg.split(b"\n")  # keep \r; offsets computed on raw bytes below
# byte offset of each line start
line_starts = []
pos = 0
for ln in lines:
    line_starts.append(pos)
    pos += len(ln) + 1

# Contents titles: indented (4 spaces), all-caps-ish lines after "Contents"
titles = []
in_contents = False
for ln in lines:
    s = ln.decode("utf-8", "replace")
    if s.strip() == "Contents":
        in_contents = True
        continue
    if in_contents:
        if s.startswith("    ") and s.strip():
            titles.append(s.strip())
        elif s.strip() == "" :
            continue
        else:
            # end of contents block once we've collected some and hit a
            # non-indented non-empty line that is not a title continuation
            if titles and not s.startswith(" "):
                break
print("contents titles:", len(titles), file=sys.stderr)

# body banners: non-indented lines exactly equal to a contents title
banners = []  # (byte_offset, title)
title_set = set(titles)
for i, ln in enumerate(lines):
    s = ln.decode("utf-8", "replace")
    if s and s[0] not in " \t" and s.strip() in title_set:
        banners.append((line_starts[i], s.strip()))
print("body banners found:", len(banners), file=sys.stderr)
for off, t in banners[:5]:
    print("  banner", off, t, file=sys.stderr)

TARGET_PLAYS = ["THE TRAGEDY OF HAMLET, PRINCE OF DENMARK",
                "THE TRAGEDY OF KING LEAR",
                "THE TRAGEDY OF MACBETH",
                "THE TRAGEDY OF OTHELLO, THE MOOR OF VENICE"]
SHORT = {"THE TRAGEDY OF HAMLET, PRINCE OF DENMARK": "HAMLET",
         "THE TRAGEDY OF KING LEAR": "LEAR",
         "THE TRAGEDY OF MACBETH": "MACBETH",
         "THE TRAGEDY OF OTHELLO, THE MOOR OF VENICE": "OTHELLO"}

bmap = {t: off for off, t in banners}
for t in TARGET_PLAYS:
    assert t in bmap, ("missing banner", t)
banners_sorted = sorted(banners)
# region end = next banner start (any play)
region = {}
for idx, (off, t) in enumerate(banners_sorted):
    end = banners_sorted[idx + 1][0] if idx + 1 < len(banners_sorted) else len(pg)
    region[t] = (off, end)

def next_line_start(data, p):
    j = data.find(b"\n", p)
    return (j + 1) if j != -1 else len(data)

def line_end_after(data, p):
    j = data.find(b"\n", p)
    return (j + 1) if j != -1 else len(data)

dp1 = []
iid = 0
for t in TARGET_PLAYS:
    rs, rend = region[t]
    rlen = rend - rs
    stride = (rlen - 500) // 150
    assert stride > 500, (t, stride)
    for i in range(150):
        raw = rs + i * stride
        s = next_line_start(pg, raw)
        # ensure 200..400 chars, line-aligned
        e = line_end_after(pg, s + 200)
        if e - s > 400:
            # too long: back off to last line end <= s+400
            # (guaranteed >= s+200 because lines here are short; assert it)
            j = pg.rfind(b"\n", s, s + 400)
            e = (j + 1) if j != -1 else s + 400
        assert 200 <= e - s <= 400, (t, i, e - s)
        assert e <= rend, (t, i, "crosses region end")
        iid += 1
        dp1.append({
            "item_id": "dp1-%04d" % iid,
            "play": SHORT[t],
            "byte_start": s,
            "byte_end": e,
            "n_bytes": e - s,
            "sha256": hashlib.sha256(pg[s:e]).hexdigest(),
            "attribution_rule": "enclosing play region: body banner (exact non-indented Contents title) to next play's banner",
        })
assert len(dp1) == 600
with open(os.path.join(ART, "d_p1_items.tsv"), "w", encoding="utf-8") as f:
    f.write("item_id\tplay\tbyte_start\tbyte_end\tn_bytes\tsha256\tattribution_rule\n")
    for r in dp1:
        f.write("%(item_id)s\t%(play)s\t%(byte_start)d\t%(byte_end)d\t%(n_bytes)d\t%(sha256)s\t%(attribution_rule)s\n" % r)
print("wrote d_p1_items.tsv (600)", file=sys.stderr)

# ---------------------------------------------------------------------------
# D-P2 — 600 function-definition classification items (8 subsystems x 75)
# ---------------------------------------------------------------------------
# Function-definition rule (frozen, deterministic):
#   * line at column 0 (no leading whitespace), non-empty
#   * does not start with '#', '/', '*'
#   * stripped line does NOT end with ';' (excludes prototypes/declarations)
#   * contains '(' with no '=' before the first '(' (excludes initializers)
#   * last identifier-before-'(' on the line is the name; not a C keyword
#   * first token not a control keyword
# Subsystem = frozen filename->subsystem table below; files not listed -> other.
# Body range: from signature line start; brace-depth scan (naive '{'/'}'
# counting, documented limitation) until depth returns to 0 at a line end.
# byte_end = end of that line (line-aligned, end-exclusive).
SUBSYS_FILES = {}
def _reg(files, s):
    for f in files:
        SUBSYS_FILES[f] = s
_reg(["btree.c","btree.h","btreeInt.h","btmutex.c","backup.c"], "btree")
_reg(["pager.c","pager.h","pcache.c","pcache.h","pcache1.c","wal.c","wal.h","memjournal.c"], "pager")
_reg(["os.c","os.h","os_common.h","os_setup.h","os_unix.c","os_win.c","os_win.h","os_kv.c","hwtime.h","msvc.h","vxworks.h"], "os")
_reg(["vdbe.c","vdbe.h","vdbeInt.h","vdbeapi.c","vdbeaux.c","vdbeblob.c","vdbemem.c","vdbesort.c","vdbetrace.c","vdbevtab.c","opcodes.c","opcodes.h"], "vdbe")
_reg(["parse.c","parse.h","tokenize.c","keywordhash.h"], "parser")
_reg(["util.c","utf.c","printf.c","random.c","hash.c","hash.h","bitvec.c","rowset.c","treeview.c","status.c","ctime.c","global.c","fault.c","threads.c"], "util")
_reg(["mem0.c","mem1.c","mem2.c","mem3.c","mem5.c","malloc.c","memdb.c"], "mem")
# every other amalgamation file -> "other"

sq_lines = sq.split(b"\n")
sq_starts = []
_p = 0
for _ln in sq_lines:
    sq_starts.append(_p); _p += len(_ln) + 1

C_KW = {"if","for","while","switch","return","sizeof","typedef","do","else"}
_name_re = re.compile(rb"([A-Za-z_][A-Za-z0-9_]*)\s*\(")
_file_re = re.compile(rb"Begin file ([A-Za-z0-9_.\/-]+)")

_cur = None
_funcs = []  # (sig_line_idx, name, file, sig_text)
for _i, _ln in enumerate(sq_lines):
    _m2 = _file_re.search(_ln)
    if _m2:
        _cur = _m2.group(1).decode()
        continue
    _s = _ln.decode("utf-8", "replace")
    if not _s or _s[0] in " \t":
        continue
    _st = _s.strip()
    if not _st or _st[0] in "#/*" or _st.endswith(";"):
        continue
    if "(" not in _st:
        continue
    _par = _st.find("("); _eq = _st.find("=")
    if _eq != -1 and _eq < _par:
        continue
    _ms = list(_name_re.finditer(_ln))
    if not _ms:
        continue
    _name = _ms[-1].group(1).decode()
    if _name in C_KW:
        continue
    if _st.split()[0] in C_KW:
        continue
    # signature span: lines until paren depth returns to 0
    _depth = 0; _close = None; _span_txt = []
    for _j in range(_i, min(_i + 60, len(sq_lines))):
        _t = sq_lines[_j].decode("utf-8", "replace")
        _span_txt.append(_t)
        _depth += _t.count("(") - _t.count(")")
        if _depth == 0 and ")" in _t:
            _close = _j
            break
    if _close is None:
        continue
    _span = "".join(_span_txt)
    # prototype/declaration if ';' appears before any '{' in the span
    _semi = _span.find(";"); _brace = _span.find("{")
    if _semi != -1 and (_brace == -1 or _semi < _brace):
        continue
    # definition: '{' in span after final ')' OR next non-blank line starts with '{'
    _ok = _brace != -1
    if not _ok:
        for _j in range(_close + 1, min(_close + 4, len(sq_lines))):
            _t2 = sq_lines[_j].decode("utf-8", "replace").strip()
            if not _t2:
                continue
            _ok = _t2.startswith("{")
            break
    if not _ok:
        continue
    _funcs.append((_i, _name, _cur, _st[:120]))

_by_sub = {}
for (_li, _name, _f, _sig) in _funcs:
    _by_sub.setdefault(SUBSYS_FILES.get(_f, "other"), []).append((_li, _name, _f, _sig))

for _k in sorted(_by_sub):
    print("subsystem", _k, len(_by_sub[_k]), file=sys.stderr)

ORDER = ["btree","pager","os","vdbe","parser","util","mem","other"]
PER = 75
dp2 = []
_iid = 0
for _sub in ORDER:
    _lst = sorted(_by_sub[_sub], key=lambda t: t[0])
    assert len(_lst) >= PER, (_sub, len(_lst))
    _stride = len(_lst) / PER
    for _k in range(PER):
        _li, _name, _f, _sig = _lst[int(_k * _stride)]
        # body end by brace depth
        _depth = 0; _seen = False; _end_li = _li
        for _j in range(_li, min(_li + 20000, len(sq_lines))):
            _t = sq_lines[_j].decode("utf-8", "replace")
            _depth += _t.count("{") - _t.count("}")
            if "{" in _t:
                _seen = True
            if _seen and _depth == 0:
                _end_li = _j
                break
        assert _seen, ("no body brace", _name, _sig)
        _bs = sq_starts[_li]
        _be = sq_starts[_end_li] + len(sq_lines[_end_li]) + 1
        _iid += 1
        dp2.append({
            "item_id": "dp2-%04d" % _iid,
            "func_name": _name,
            "file": _f,
            "subsystem": _sub,
            "byte_start": _bs,
            "byte_end": _be,
            "n_bytes": _be - _bs,
            "sha256": hashlib.sha256(sq[_bs:_be]).hexdigest(),
            "sig_line": _sig,
        })
assert len(dp2) == 600
with open(os.path.join(ART, "d_p2_items.tsv"), "w", encoding="utf-8") as f:
    f.write("item_id\tfunc_name\tfile\tsubsystem\tbyte_start\tbyte_end\tn_bytes\tsha256\tsig_line\n")
    for _r in dp2:
        _sig1 = _r["sig_line"].replace("\t", " ")
        f.write("%(item_id)s\t%(func_name)s\t%(file)s\t%(subsystem)s\t%(byte_start)d\t%(byte_end)d\t%(n_bytes)d\t%(sha256)s\t" % _r + _sig1 + "\n")
print("wrote d_p2_items.tsv (600)", file=sys.stderr)

# ---------------------------------------------------------------------------
# Frozen parameter grids + E-DE1 taxonomy + E-DE4 relevance declarations
# ---------------------------------------------------------------------------
esp_params = {
    "E-SP": {
        "tau_grid": [0, 1, 2, 3, 4, 5, 6],
        "tau_semantics": "minimum signature-overlap score (|query-hashes ∩ partition signature|) for a partition to wake; score computed per partition",
        "region_size": 8,
        "region_semantics": "partitions per similarity region; sweep consults region signatures (hash histograms) before partitions",
        "tau_selection_rule": "per corpus, argmax net_savings subject to measured miss_rate <= 0.05; ties broken by lowest tau; selection runs on the frozen relevance-labeled real-workload episodes",
        "note": "miss = relevant partition not woken. net_savings = 1 - (partitions_woken/total_partitions) minus signature overhead share",
    },
    "E-LG2": {
        "K_grid": [16, 64, 256],
        "K_semantics": "checkpoint interval: snapshot ledger state every K episodes; snapshot = full state at episode boundaries",
    },
    "E-LG3": {
        "H_grid": [64, 128, 256],
        "H_semantics": "hot-tier depth: last H episodes kept in full entry detail; older episodes one summary record each",
        "status": "PARKED per frozen prereg (fenced experimental arm only); grid frozen here for that arm",
    },
}
with open(os.path.join(ART, "esp_params.json"), "w") as f:
    json.dump(esp_params, f, indent=2)
    f.write("\n")
print("wrote esp_params.json", file=sys.stderr)

ede1_taxonomy = {
    "note": "Frozen task-class -> deliberation budget caps (max_depth, max_evidence_rounds). Class set derived from D-P1/D-P2/D-P3/G-CM1 proxy tasks. Values are preregistered initial caps; E-DE1 KB bars govern whether they hold.",
    "classes": {
        "ATTRIBUTE_PASSAGE":   {"task": "D-P1: attribute a 200-400 char passage to one of 4 plays", "max_depth": 3, "max_evidence_rounds": 2},
        "CLASSIFY_FUNCTION":   {"task": "D-P2: classify a function definition into one of 8 subsystems", "max_depth": 4, "max_evidence_rounds": 3},
        "ELIMINATE_HYPOTHESES":{"task": "D-P3: eliminate hypotheses under adversarial evidence ordering", "max_depth": 5, "max_evidence_rounds": 4},
        "VERIFY_CLAIM":        {"task": "G-CM1: verify a constructed claim at the promotion gate", "max_depth": 2, "max_evidence_rounds": 2},
        "REVISE_MEMORY":       {"task": "deliberate memory revision (weaken/justify/kill)", "max_depth": 3, "max_evidence_rounds": 3},
        "PLAN_ELABORATION":    {"task": "G-CM1: commit an elaboration plan for constructed-mode composition", "max_depth": 4, "max_evidence_rounds": 2},
    },
    "flat_budget_arm": {"note": "head-to-head control arm: identical caps for every class", "max_depth": 4, "max_evidence_rounds": 3},
}
with open(os.path.join(ART, "ede1_taxonomy.json"), "w") as f:
    json.dump(ede1_taxonomy, f, indent=2)
    f.write("\n")
print("wrote ede1_taxonomy.json", file=sys.stderr)

# E-DE4 relevance declarations, WITH partition provenance fields
# (amendment 2026-09-21 §A R7: relevance declarations must carry partition
# provenance; E-DE4 cache keys MUST include partition provenance, tested by
# KB-CM-CACHE1 50-planted contradiction replay).
PARTITIONS = {
    "P-CORPUS-CHUNKS":   {"provenance": "WORLD_RECORD", "address_range": "corpus chunk table [0, n_chunks) per corpus", "contents": "4KB line-aligned corpus chunks (frozen chunking rule)"},
    "P-FEATURE-TABLES":  {"provenance": "WORLD_RECORD", "address_range": "derived feature store", "contents": "identifier stems, called-function names, play-region index (deterministic scans)"},
    "P-HYPOTHESIS-SLOTS":{"provenance": "BELIEF", "address_range": "working deliberation state", "contents": "live candidate hypotheses under consideration"},
    "P-EVIDENCE-LOG":    {"provenance": "BELIEF", "address_range": "deliberation ledger", "contents": "evidence entries cited by the eliminative run"},
    "P-BELIEF-STORE":    {"provenance": "BELIEF", "address_range": "committed memory", "contents": "committed belief entries incl. promotion-gate records"},
    "P-CONSTRUCTED-STORE":{"provenance": "CONSTRUCTED", "address_range": "constructed partition (disjoint addresses)", "contents": "constructed-mode elaborations, tagged CONSTRUCTED"},
    "P-PROMOTION-GATE":  {"provenance": "BELIEF", "address_range": "gate ledger", "contents": "promotion proposals, verification records, VERIFICATION_PASSED entries"},
}
ede4 = {
    "declaration_version": 1,
    "frozen": "2026-09-21",
    "amendment": "AMENDMENT_2026-09-21_CONSTRUCTED_MODE.md §A R7: every relevant-partition entry carries partition provenance; cache keys must include it (KB-CM-CACHE1)",
    "partitions": PARTITIONS,
    "declarations": {
        "ATTRIBUTE_PASSAGE": {
            "relevant_partitions": [
                {"partition_id": "P-CORPUS-CHUNKS", "provenance": "WORLD_RECORD", "address_range": "corpus chunk table [0, n_chunks) per corpus", "rationale": "passage bytes live in corpus chunks"},
                {"partition_id": "P-FEATURE-TABLES", "provenance": "WORLD_RECORD", "address_range": "derived feature store", "rationale": "play-region index maps offsets to plays"},
                {"partition_id": "P-HYPOTHESIS-SLOTS", "provenance": "BELIEF", "address_range": "working deliberation state", "rationale": "four candidate plays held as live hypotheses"},
            ],
            "irrelevant_partitions": ["P-CONSTRUCTED-STORE", "P-PROMOTION-GATE"],
        },
        "CLASSIFY_FUNCTION": {
            "relevant_partitions": [
                {"partition_id": "P-CORPUS-CHUNKS", "provenance": "WORLD_RECORD", "address_range": "corpus chunk table [0, n_chunks) per corpus", "rationale": "function definition bytes live in corpus chunks"},
                {"partition_id": "P-FEATURE-TABLES", "provenance": "WORLD_RECORD", "address_range": "derived feature store", "rationale": "identifier stems and called-function names from deterministic scans"},
                {"partition_id": "P-HYPOTHESIS-SLOTS", "provenance": "BELIEF", "address_range": "working deliberation state", "rationale": "eight candidate subsystems held as live hypotheses"},
            ],
            "irrelevant_partitions": ["P-CONSTRUCTED-STORE", "P-PROMOTION-GATE"],
        },
        "ELIMINATE_HYPOTHESES": {
            "relevant_partitions": [
                {"partition_id": "P-HYPOTHESIS-SLOTS", "provenance": "BELIEF", "address_range": "working deliberation state", "rationale": "candidate set under elimination"},
                {"partition_id": "P-EVIDENCE-LOG", "provenance": "BELIEF", "address_range": "deliberation ledger", "rationale": "evidence stream entries with elimination effects"},
                {"partition_id": "P-BELIEF-STORE", "provenance": "BELIEF", "address_range": "committed memory", "rationale": "prior committed findings constrain elimination"},
            ],
            "irrelevant_partitions": ["P-CONSTRUCTED-STORE", "P-CORPUS-CHUNKS"],
        },
        "VERIFY_CLAIM": {
            "relevant_partitions": [
                {"partition_id": "P-CORPUS-CHUNKS", "provenance": "WORLD_RECORD", "address_range": "corpus chunk table [0, n_chunks) per corpus", "rationale": "corpus ground truth is the world record for verification"},
                {"partition_id": "P-BELIEF-STORE", "provenance": "BELIEF", "address_range": "committed memory", "rationale": "contradiction scan runs against committed beliefs"},
                {"partition_id": "P-PROMOTION-GATE", "provenance": "BELIEF", "address_range": "gate ledger", "rationale": "prior gate decisions and verification records"},
            ],
            "irrelevant_partitions": ["P-CONSTRUCTED-STORE"],
            "provenance_rule": "evidence cited at the gate must NOT be subset of CONSTRUCTED entries (self-verification ban, KB-CM-PROM2)",
        },
        "REVISE_MEMORY": {
            "relevant_partitions": [
                {"partition_id": "P-BELIEF-STORE", "provenance": "BELIEF", "address_range": "committed memory", "rationale": "the memory under revision"},
                {"partition_id": "P-EVIDENCE-LOG", "provenance": "BELIEF", "address_range": "deliberation ledger", "rationale": "contradicting world observations"},
                {"partition_id": "P-HYPOTHESIS-SLOTS", "provenance": "BELIEF", "address_range": "working deliberation state", "rationale": "keep vs kill candidates"},
            ],
            "irrelevant_partitions": ["P-CONSTRUCTED-STORE"],
        },
        "PLAN_ELABORATION": {
            "relevant_partitions": [
                {"partition_id": "P-CONSTRUCTED-STORE", "provenance": "CONSTRUCTED", "address_range": "constructed partition (disjoint addresses)", "rationale": "elaboration output lands here by construction"},
                {"partition_id": "P-CORPUS-CHUNKS", "provenance": "WORLD_RECORD", "address_range": "corpus chunk table [0, n_chunks) per corpus", "rationale": "source traces the plan may draw on (via ledgered IMPORT only)"},
                {"partition_id": "P-HYPOTHESIS-SLOTS", "provenance": "BELIEF", "address_range": "working deliberation state", "rationale": "plan under deliberate construction"},
            ],
            "irrelevant_partitions": ["P-BELIEF-STORE"],
            "provenance_rule": "elaboration writes MUST NOT address P-BELIEF-STORE (R2 structural separation); IMPORT is the only BELIEF<-CONSTRUCTED path and is ledgered",
        },
    },
}
with open(os.path.join(ART, "ede4_relevance.json"), "w") as f:
    json.dump(ede4, f, indent=2)
    f.write("\n")
print("wrote ede4_relevance.json", file=sys.stderr)

# ---------------------------------------------------------------------------
# G-CO2 — 200 out-of-corpus abstention probes
# ---------------------------------------------------------------------------
_TEMPLATES = ["Explain {t}.", "What is {t}?", "Describe how {t} works.", "Give an overview of {t}."]
_TECH = ["a quantum computer","a jet engine","a lithium-ion battery","a GPS satellite","neural network training","a 5G antenna","a solar panel","a nuclear reactor","a submarine","a helicopter rotor","a touchscreen","a fiber optic cable","a blockchain","CRISPR gene editing","an mRNA vaccine","a wind turbine","an electric motor","the refrigerator cycle","airplane wing lift","radar","sonar","an LED","a transistor","microchip fabrication","a 3D printer","a camera drone","autonomous car lidar","a smartwatch heart sensor","a digital camera sensor","a wifi router","bluetooth pairing","a hard disk drive","a solid-state drive","a QR code","a barcode scanner","an elevator","an escalator","traffic light timing","a hydroelectric dam","desalination","carbon capture","a hydrogen fuel cell","a geothermal plant","tidal power","a maglev train","supersonic flight","a space station orbit","rocket staging","a parachute","the diesel engine"]
_GEO = ["the capital of Burkina Faso","the fall of Rome","the building of the pyramids","the Silk Road","the Ming dynasty","the Inca empire","the Viking voyages","the Ottoman empire","the French Revolution","the Panama Canal","the construction of the Eiffel Tower","the Great Wall of China","Machu Picchu","the Colosseum","the Parthenon","the Taj Mahal","Angkor Wat","Petra","the Moai statues of Easter Island","the terracotta army","Pompeii","the Library of Alexandria","the Hanseatic League","the Crusades","the Hundred Years\u2019 War","the Meiji Restoration","the Scramble for Africa","the Suez Canal","the Trans-Siberian Railway","the California Gold Rush","the Dust Bowl","the Industrial Revolution","the printing press","the Black Death","the Renaissance","the Reformation","the Age of Exploration","the triangular trade","the Opium Wars","the Boxer Rebellion","the Russian Revolution","trench warfare in WWI","the Treaty of Versailles","the Great Depression","the Marshall Plan","the Cuban Missile Crisis","the Apollo program","the partition of India","the Berlin Airlift","the voyages of Zheng He"]
_SCI = ["photosynthesis","mitosis","the water cycle","plate tectonics","evolution by natural selection","the Big Bang","black holes","DNA replication","the immune system","neurons firing","the Krebs cycle","ocean tides","the seasons","solar eclipses","the greenhouse effect","ocean currents","volcanoes","earthquakes","hurricanes","tornadoes","the periodic table","chemical bonds","acids and bases","the laws of thermodynamics","Newton\u2019s laws of motion","relativity","quantum entanglement","the electromagnetic spectrum","sound waves","the Doppler effect","gravity assists","the Coriolis effect","osmosis","diffusion","enzymes","hormones","blood clotting","the carbon cycle","the nitrogen cycle","food webs","symbiosis","camouflage","animal migration","hibernation","metamorphosis","pollination","seed dispersal","fermentation","the rock cycle","erosion"]
_ART = ["the rules of cricket","the rules of rugby","tennis scoring","the offside rule in soccer","how a marathon is run","Olympic swimming strokes","castling in chess","poker hand rankings","bridge bidding basics","baking sourdough bread","brewing coffee with a French press","changing a tire","tying a bowline knot","reading sheet music","tuning a guitar","how a piano makes sound","how oil paint dries","perspective in drawing","how animation frames work","how a film projector works","haiku structure","limerick structure","jazz improvisation basics","how a symphony orchestra is seated","ballet positions","camera aperture in photography","developing film in a darkroom","folding an origami crane","knitting stitches","how to play sudoku","crossword conventions","Scrabble scoring","Monopoly rules","juggling three balls","swimming freestyle","doing a push-up properly","the yoga sun salutation","breathing meditation","keeping a sourdough starter alive","espresso extraction","tea grading","wine tasting","aging cheese","tempering chocolate","preparing sushi rice","extruding pasta","yeast fermentation in bread","the rules of badminton","how a compass works","knot tying for sailing"]
assert len(_TECH) == 50 and len(_GEO) == 50 and len(_SCI) == 50 and len(_ART) == 50
_cats = [("technology", _TECH), ("geography/history", _GEO), ("science", _SCI), ("arts/sport/everyday", _ART)]
gco2 = []
for _ci, (_cat, _topics) in enumerate(_cats):
    for _ti, _t in enumerate(_topics):
        _n = _ci * 50 + _ti
        _tmpl = _TEMPLATES[_n % 4]
        gco2.append({
            "probe_id": "gco2-%04d" % (_n + 1),
            "category": _cat,
            "prompt": _tmpl.format(t=_t),
            "expected_verdict": "ABSTAIN",
            "coverage_note": "out-of-corpus topic: zero corpus chunks relevant in pg100.txt or sqlite3.c",
        })
assert len(gco2) == 200
with open(os.path.join(ART, "gco2_abstention_200.jsonl"), "w", encoding="utf-8") as f:
    for _r in gco2:
        f.write(json.dumps(_r, ensure_ascii=False) + "\n")
print("wrote gco2_abstention_200.jsonl (200)", file=sys.stderr)
print("GEN_CORPUS DONE", file=sys.stderr)
