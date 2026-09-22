#!/usr/bin/env python3
"""Shared sealed battery logic for the Sol-vs-Grok duel.
No RNG: every value is a closed-form function of (relation, entity) indices.
A CONFIG dict supplies vocabulary; two configs exist: calib (visible) and
scored (sealed until build freeze).
"""
import json, os

def typo(w):
    i = len(w) // 2
    c = 'z' if w[i] != 'z' else 'q'
    return w[:i] + c + w[i+1:]

def build(cfg, out):
    os.makedirs(out, exist_ok=True)
    RELATIONS = cfg["relations"]
    ENT_MAIN = cfg["ent_main"]
    ENT_NEG = cfg["ent_neg"]
    ENT_HEDGE = cfg["ent_hedge"]
    ENT_CONTR = cfg["ent_contr"]
    ENT_DISTR = cfg["ent_distr"]
    DISTR_RELS = cfg["distr_rels"]
    V0, VMUL_R, VMUL_E, VMOD, Y0, YMOD = cfg["value_params"]

    def value(ri, ei):
        if ri == cfg["year_rel"]:
            return Y0 + (ri * VMUL_R + ei * VMUL_E) % YMOD
        return V0 + (ri * VMUL_R + ei * VMUL_E) % VMOD

    teach, probes, expected = [], [], {}
    def T(i, text): teach.append((i, text))
    def P(i, text, cls, verdict):
        probes.append((i, text, cls))
        expected[i] = {"verdict": verdict, "class": cls}

    for ri, (ra, rb) in enumerate(RELATIONS):
        for ei, e in enumerate(ENT_MAIN):
            v = value(ri, ei)
            T(f"T{ri:02d}{ei:02d}a", f'The {ra} of "{e}" is {v}.')
            T(f"T{ri:02d}{ei:02d}b", f'The {rb} of "{e}" is {v}.')
            T(f"T{ri:02d}{ei:02d}c", f'{v} is the {ra} of "{e}".')
            P(f"P{ri:02d}{ei:02d}0", f'What is the {ra} of "{e}"?', "canon", f"VALUE:{v}")
            P(f"P{ri:02d}{ei:02d}1", f'What is the {rb} of "{e}"?', "heldout", f"VALUE:{v}")
            if (ri + ei) % 2 == 0:
                P(f"X{ri:02d}{ei:02d}", f'What is the {ra} of "{e}" today?', "extra", f"VALUE:{v}")
            else:
                w0, rest = ra.split(" ", 1)
                P(f"Y{ri:02d}{ei:02d}", f'What is the {typo(w0)} {rest} of "{e}"?', "typo", f"VALUE:{v}")

    for k, e in enumerate(ENT_NEG):
        for j in range(3):
            ri = (k + j * 4) % 12
            ra, _ = RELATIONS[ri]
            v = value(ri, k)
            T(f"N{k:02d}{j}", f'The {ra} of "{e}" is not {v}.')
            P(f"PN{k:02d}{j}", f'What is the {ra} of "{e}"?', "neg", f"NOT-VALUE:{v}")

    for k, e in enumerate(ENT_HEDGE):
        for j in range(3):
            ri = (k + 1 + j * 4) % 12
            ra, _ = RELATIONS[ri]
            v = value(ri, k)
            T(f"H{k:02d}{j}", f'The {ra} of "{e}" might be {v}.')
            P(f"PH{k:02d}{j}", f'What is the {ra} of "{e}"?', "hedge", f"NOT-VALUE:{v}")

    for k, e in enumerate(ENT_CONTR):
        for j in range(3):
            ri = (k + 2 + j * 4) % 12
            ra, _ = RELATIONS[ri]
            v1 = value(ri, k)
            v2 = v1 + cfg["contr_delta"]
            T(f"C{k:02d}{j}", f'The {ra} of "{e}" is {v1}. The {ra} of "{e}" is {v2}.')
            P(f"PC{k:02d}{j}", f'What is the {ra} of "{e}"?', "contr", "CONTRADICTION")

    for k, e in enumerate(ENT_DISTR):
        for j in range(3):
            ri = (k + j * 5) % 12
            ra, _ = RELATIONS[ri]
            P(f"DE{k:02d}{j}", f'What is the {ra} of "{e}"?', "distr", "UNKNOWN")
    for k, e in enumerate(ENT_MAIN):
        for j, dr in enumerate(DISTR_RELS):
            P(f"DR{k:02d}{j}", f'What is the {dr} of "{e}"?', "distr", "UNKNOWN")

    for i in range(24):
        e = ENT_MAIN[i % 8]
        ria = i % 12
        rib = (i + 5) % 12
        raa, _ = RELATIONS[ria]
        rab, _ = RELATIONS[rib]
        v1 = value(ria, i % 8)
        v2 = value(rib, i % 8)
        T(f"M{i:02d}", f'The {raa} of "{e}" is {v1}. It has a {rab} of {v2}.')
        P(f"PM{i:02d}", f'What is the {rab} of "{e}"?', "multi", f"VALUE:{v2}")

    with open(os.path.join(out, "teach_sg.txt"), "w") as f:
        for i, t in teach:
            f.write(f"{i}\t{t}\n")
    with open(os.path.join(out, "probe_sg.txt"), "w") as f:
        for i, t, c in probes:
            f.write(f"{i}\t{t}\t{c}\n")
    with open(os.path.join(out, "expected_sg.json"), "w") as f:
        json.dump(expected, f, indent=1, sort_keys=True)
    return len(teach), len(probes)
