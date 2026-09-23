#!/usr/bin/env python3
"""ref_dsl.py — independent Python reference for the policy DSL.

Takes a policy (.zpol text) and a battery CSV (fields only), simulates the
frozen §1.5 semantics, and emits one JSON object per line:
  {"id":..,"key":..,"verdict":"NEW|OLD|WITHHOLD","consulted":0|1,"ops":..}

Malformed policy -> exit nonzero, no stdout (mirrors the Zag engine's
refusal contract). Used for differential testing against policy_engine.

This is an INDEPENDENT reimplementation of the Appendix B grammar and the
§1.1/§1.4/§1.5/§1.6 semantics; it does not import translate_policy.py.
"""
import csv
import json
import re
import sys

# ---- grammar (Appendix B), reimplemented independently ----
ATOMS = {"pre_is": 1, "chan_present": 2, "chan_silent": 3, "sm_le": 4,
         "sm_ge": 5, "sm_eq": 6, "dir_is": 7, "sn_ge": 8, "so_ge": 9,
         "caval_eq_vold": 10, "caval_eq_vnew": 11, "post_is": 12,
         "psm_le": 13, "psm_ge": 14, "psm_eq": 15}
ACTIONS = {"force_consult": 1, "block_consult": 2, "force_withhold": 3,
           "force_install": 4, "recompute_only": 5}
STAGE_OF = {1: 1, 2: 1, 3: 2, 4: 2, 5: 4}
S2_ONLY = {12, 13, 14, 15}
XMAP = {"HOLD": 0, "NEW": 1, "OLD": 2}
DMAP = {"TIE": 0, "NEW_LEAD": 1, "OLD_LEAD": 2}
NIMAP = {"NEW": 1, "OLD": 2}


class Bad(Exception):
    pass


def strict_int(s, lo, hi):
    if not re.fullmatch(r"-?(0|[1-9][0-9]*)", s):
        raise Bad(f"int {s!r}")
    v = int(s)
    if not lo <= v <= hi:
        raise Bad(f"int {s!r} range")
    return v


def parse_atom(t):
    m = re.fullmatch(r"([a-z_]+)(?:\(([^()]*)\))?", t)
    if not m:
        raise Bad(f"atom {t!r}")
    name, arg = m.groups()
    if name not in ATOMS:
        raise Bad(f"atom {name!r}")
    aid = ATOMS[name]
    if name in ("pre_is", "post_is"):
        if arg not in XMAP:
            raise Bad(f"X {arg!r}")
        return (aid, XMAP[arg])
    if name == "dir_is":
        if arg not in DMAP:
            raise Bad(f"D {arg!r}")
        return (aid, DMAP[arg])
    if name in ("sm_le", "sm_ge", "sm_eq", "psm_le", "psm_ge", "psm_eq"):
        if arg is None:
            raise Bad(f"{name} param")
        return (aid, strict_int(arg, -6, 6))
    if name in ("sn_ge", "so_ge"):
        if arg is None:
            raise Bad(f"{name} param")
        return (aid, strict_int(arg, -3, 3))
    if arg is not None:
        raise Bad(f"{name} no-param")
    return (aid, None)


def parse_action(t):
    m = re.fullmatch(r"([a-z_]+)(?:\(([^()]*)\))?", t)
    if not m:
        raise Bad(f"action {t!r}")
    name, arg = m.groups()
    if name not in ACTIONS:
        raise Bad(f"action {name!r}")
    aid = ACTIONS[name]
    if name == "force_install":
        if arg not in NIMAP:
            raise Bad(f"NI {arg!r}")
        return (aid, NIMAP[arg])
    if name == "recompute_only":
        if arg is None:
            raise Bad("mask param")
        return (aid, strict_int(arg, 0, 7))
    if arg is not None:
        raise Bad(f"{name} no-param")
    return (aid, None)


def parse_policy(text):
    if len(text.encode()) > 2048:
        raise Bad(">2048 bytes")
    if text == "":
        return []  # empty policy: no rules (base behavior)
    lines = text.split("\n")
    if len(lines) < 3 or lines[-1] != "" or lines[-2] != "END":
        raise Bad("END")
    if not re.fullmatch(r"POLICY ([A-Za-z][A-Za-z0-9_]{0,31})", lines[0]):
        raise Bad("header")
    body = lines[1:-2]
    if not 1 <= len(body) <= 8:
        raise Bad("rule count")
    rules = []
    for i, line in enumerate(body, 1):
        m = re.fullmatch(r"RULE ([1-8]) IF (.+) THEN (.+)", line)
        if not m or int(m.group(1)) != i:
            raise Bad(f"rule {i}")
        atoms = [parse_atom(a) for a in m.group(2).split(" AND ")]
        if any(a == "" for a in m.group(2).split(" AND ")):
            raise Bad(f"rule {i} empty atom")
        aid, ap = parse_action(m.group(3))
        stage = STAGE_OF[aid]
        if stage in (1, 4) and any(a[0] in S2_ONLY for a in atoms):
            raise Bad(f"rule {i} stage")
        rules.append((stage, atoms, aid, ap))
    return rules


# ---- engine semantics (§1.1/§1.5/§1.6) ----
def sat(v, a, op):
    return (v == a) if op == 0 else (v < a if op == 1 else v > a)


def rel_score(v, a, op):
    return 1 if sat(v, a, op) else -1


def atom_true(aid, ap, ctx):
    so, sn, pre, sm = ctx["so"], ctx["sn"], ctx["pre"], ctx["sm"]
    ci, caval, vold, vnew = ctx["ci"], ctx["caval"], ctx["vold"], ctx["vnew"]
    if aid == 1:
        return pre == ap
    if aid == 2:
        return ci != -1
    if aid == 3:
        return ci == -1
    if aid == 4:
        return sm <= ap
    if aid == 5:
        return sm >= ap
    if aid == 6:
        return sm == ap
    if aid == 7:
        return (sm > 0 and ap == 1) or (sm < 0 and ap == 2) or (sm == 0 and ap == 0)
    if aid == 8:
        return sn >= ap
    if aid == 9:
        return so >= ap
    if aid == 10:
        return ci != -1 and caval == vold
    if aid == 11:
        return ci != -1 and caval == vnew
    # S2-only (post-consult context)
    so2, sn2, post, psm = ctx["so2"], ctx["sn2"], ctx["post"], ctx["psm"]
    if aid == 12:
        return post == ap
    if aid == 13:
        return psm <= ap
    if aid == 14:
        return psm >= ap
    if aid == 15:
        return psm == ap
    raise Bad("aid")


def decide(row, rules):
    vold, vnew = row["vold"], row["vnew"]
    rels = [(row["a1"], row["op1"]), (row["a2"], row["op2"]), (row["a3"], row["op3"])]
    ci, caval = row["cidx"], row["caval"]

    def pick_score(p):
        v = vnew if p == 1 else vold
        return sum(rel_score(v, a, op) for a, op in rels)

    so, sn = pick_score(0), pick_score(1)
    sm = sn - so
    pre = 1 if sn > so else (2 if so > sn else 0)

    # per-relation pre contributions (for S4 scope reuse)
    pre_contrib = []
    for (a, op) in rels:
        co = rel_score(vold, a, op)
        cn = rel_score(vnew, a, op)
        pre_contrib.append((co, cn))

    # S1
    consult = (pre != 1)
    for stage, atoms, aid, ap in rules:
        if stage != 1:
            continue
        ctx = {"so": so, "sn": sn, "pre": pre, "sm": sm, "ci": ci,
               "caval": caval, "vold": vold, "vnew": vnew,
               "so2": 0, "sn2": 0, "post": 0, "psm": 0}
        if all(atom_true(a[0], a[1], ctx) for a in atoms):
            consult = (aid == 1)  # force_consult=1 -> True; block=2 -> False
            break

    if not consult:
        # no-consult path: verdict = pre (HOLD -> WITHHOLD)
        v = pre  # 0=HOLD->WITHHOLD, 1=NEW, 2=OLD
        ops = 7
        return ("WITHHOLD" if v == 0 else ("NEW" if v == 1 else "OLD"), 0, ops)

    # S4: scope
    scope = 7
    for stage, atoms, aid, ap in rules:
        if stage != 4:
            continue
        ctx = {"so": so, "sn": sn, "pre": pre, "sm": sm, "ci": ci,
               "caval": caval, "vold": vold, "vnew": vnew,
               "so2": 0, "sn2": 0, "post": 0, "psm": 0}
        if all(atom_true(a[0], a[1], ctx) for a in atoms):
            scope = ap
            break

    # recompute with scope + channel override
    so2 = sn2 = 0
    for r in range(3):
        if (scope >> r) & 1:
            a = caval if (ci == r) else rels[r][0]
            op = rels[r][1]
            so2 += rel_score(vold, a, op)
            sn2 += rel_score(vnew, a, op)
        else:
            co, cn = pre_contrib[r]
            so2 += co
            sn2 += cn
    psm = sn2 - so2
    post = 1 if sn2 > so2 else (2 if so2 > sn2 else 0)

    # S2
    v = post
    for stage, atoms, aid, ap in rules:
        if stage != 2:
            continue
        ctx = {"so": so, "sn": sn, "pre": pre, "sm": sm, "ci": ci,
               "caval": caval, "vold": vold, "vnew": vnew,
               "so2": so2, "sn2": sn2, "post": post, "psm": psm}
        if all(atom_true(a[0], a[1], ctx) for a in atoms):
            if aid == 3:
                v = 0
            elif aid == 4:
                v = ap  # 1=NEW, 2=OLD
            break

    ops = 7 + 4 + 4 * bin(scope).count("1")
    vstr = "WITHHOLD" if v == 0 else ("NEW" if v == 1 else "OLD")
    return (vstr, 1, ops)


def main():
    if len(sys.argv) != 3:
        print("usage: ref_dsl.py <policy.zpol> <battery.csv>", file=sys.stderr)
        sys.exit(2)
    with open(sys.argv[1]) as f:
        ptext = f.read()
    try:
        rules = parse_policy(ptext)
    except Bad as e:
        print(f"REFUSE: {e}", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[2]) as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ("vold", "vnew", "a1", "op1", "a2", "op2", "a3", "op3",
                  "cidx", "caval"):
            r[k] = int(r[k])
        v, cons, ops = decide(r, rules)
        print(json.dumps({"id": int(r["id"]), "key": int(r["key"]),
                          "verdict": v, "consulted": cons, "ops": ops}))


if __name__ == "__main__":
    main()
