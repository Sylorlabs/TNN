#!/usr/bin/env python3
"""translate_policy.py — L1: policy text -> bytecode (strict, no repair).

Normative grammar: Appendix B of design_subject_loop.md (frozen).

Usage: translate_policy.py <policy.zpol>
  On success: prints bytecode to stdout, exit 0.
  On refusal: prints NOTHING to stdout, logs reason to stderr, exit nonzero.

Bytecode: rule (";" rule)* ; rule := stage "," atoms "," action
  stage := "1"|"2"|"4" (inferred from action)
  atoms := atom ("+" atom)* ; atom := atomid ["=" param]
  action := actionid ["=" param]

Atom/action IDs: see Appendix A of design_subject_loop.md (frozen).
"""
import re
import sys

ATOM_ID = {
    "pre_is": 1, "chan_present": 2, "chan_silent": 3,
    "sm_le": 4, "sm_ge": 5, "sm_eq": 6,
    "dir_is": 7, "sn_ge": 8, "so_ge": 9,
    "caval_eq_vold": 10, "caval_eq_vnew": 11,
    "post_is": 12, "psm_le": 13, "psm_ge": 14, "psm_eq": 15,
}
ACTION_ID = {
    "force_consult": 1, "block_consult": 2, "force_withhold": 3,
    "force_install": 4, "recompute_only": 5,
}
# action -> stage ("1","2","4")
ACTION_STAGE = {1: "1", 2: "1", 3: "2", 4: "2", 5: "4"}
# atoms legal only in S2 rules (stage "2")
S2_ONLY_ATOMS = {12, 13, 14, 15}

X_VAL = {"HOLD": 0, "NEW": 1, "OLD": 2}
D_VAL = {"TIE": 0, "NEW_LEAD": 1, "OLD_LEAD": 2}
NI_VAL = {"NEW": 1, "OLD": 2}


class Refuse(Exception):
    pass


def parse_int(s, lo, hi, what):
    # strict: no leading zeros (except "0" itself), no plus sign
    if not re.fullmatch(r"-?(0|[1-9][0-9]*)", s):
        raise Refuse(f"bad integer literal for {what}: {s!r}")
    v = int(s)
    if not (lo <= v <= hi):
        raise Refuse(f"{what} out of range [{lo},{hi}]: {s!r}")
    return v


def parse_atom(text):
    # returns (atomid, param_or_None)
    m = re.fullmatch(r"([a-z_]+)(?:\(([^()]*)\))?", text)
    if not m:
        raise Refuse(f"bad atom syntax: {text!r}")
    name, arg = m.group(1), m.group(2)
    if name not in ATOM_ID:
        raise Refuse(f"unknown atom: {name!r}")
    aid = ATOM_ID[name]
    if name in ("pre_is", "post_is"):
        if arg not in X_VAL:
            raise Refuse(f"bad X param for {name}: {arg!r}")
        return aid, X_VAL[arg]
    if name == "dir_is":
        if arg not in D_VAL:
            raise Refuse(f"bad D param for dir_is: {arg!r}")
        return aid, D_VAL[arg]
    if name in ("sm_le", "sm_ge", "sm_eq", "psm_le", "psm_ge", "psm_eq"):
        if arg is None:
            raise Refuse(f"missing param for {name}")
        return aid, parse_int(arg, -6, 6, name)
    if name in ("sn_ge", "so_ge"):
        if arg is None:
            raise Refuse(f"missing param for {name}")
        return aid, parse_int(arg, -3, 3, name)
    if name in ("chan_present", "chan_silent", "caval_eq_vold", "caval_eq_vnew"):
        if arg is not None:
            raise Refuse(f"{name} takes no param")
        return aid, None
    raise Refuse(f"unhandled atom: {name!r}")


def parse_action(text):
    m = re.fullmatch(r"([a-z_]+)(?:\(([^()]*)\))?", text)
    if not m:
        raise Refuse(f"bad action syntax: {text!r}")
    name, arg = m.group(1), m.group(2)
    if name not in ACTION_ID:
        raise Refuse(f"unknown action: {name!r}")
    aid = ACTION_ID[name]
    if name == "force_install":
        if arg not in NI_VAL:
            raise Refuse(f"bad NI param for force_install: {arg!r}")
        return aid, NI_VAL[arg]
    if name == "recompute_only":
        if arg is None:
            raise Refuse("missing param for recompute_only")
        return aid, parse_int(arg, 0, 7, "recompute_only mask")
    if arg is not None:
        raise Refuse(f"{name} takes no param")
    return aid, None


def translate(text):
    if len(text.encode("utf-8")) > 2048:
        raise Refuse("policy exceeds 2048 bytes")
    lines = text.split("\n")
    # POLICY <name>\n ... \nEND\n  -> split gives [..., "END", ""]
    if len(lines) < 3 or lines[-1] != "" or lines[-2] != "END":
        raise Refuse("policy must end with 'END\\n'")
    m = re.fullmatch(r"POLICY ([A-Za-z][A-Za-z0-9_]{0,31})", lines[0])
    if not m:
        raise Refuse(f"bad POLICY header: {lines[0]!r}")
    body = lines[1:-2]
    if not (1 <= len(body) <= 8):
        raise Refuse(f"rule count must be 1..8, got {len(body)}")
    rules = []
    for idx, line in enumerate(body, start=1):
        m = re.fullmatch(r"RULE ([1-8]) IF (.+) THEN (.+)", line)
        if not m:
            raise Refuse(f"bad RULE line {idx}: {line!r}")
        n = int(m.group(1))
        if n != idx:
            raise Refuse(f"rule numbers must be sequential from 1; "
                         f"line {idx} has N={n}")
        trig_text, act_text = m.group(2), m.group(3)
        # trigger: ATOM (" AND " ATOM)* — split on " AND " exactly
        atom_texts = trig_text.split(" AND ")
        if any(a == "" for a in atom_texts):
            raise Refuse(f"empty atom in rule {idx}")
        atoms = [parse_atom(a) for a in atom_texts]
        aid, aparam = parse_action(act_text)
        stage = ACTION_STAGE[aid]
        # stage legality: S2-only atoms (12-15) refused in S1/S4 rules
        if stage in ("1", "4"):
            for atomid, _ in atoms:
                if atomid in S2_ONLY_ATOMS:
                    raise Refuse(f"S2-only atom {atomid} in stage-{stage} "
                                 f"rule {idx}")
        atom_strs = [str(aid_) if p is None else f"{aid_}={p}"
                     for aid_, p in atoms]
        act_str = str(aid) if aparam is None else f"{aid}={aparam}"
        rules.append(f"{stage}," + "+".join(atom_strs) + f",{act_str}")
    return ";".join(rules)


def main():
    if len(sys.argv) != 2:
        print("usage: translate_policy.py <policy.zpol>", file=sys.stderr)
        sys.exit(2)
    with open(sys.argv[1], "r") as f:
        text = f.read()
    try:
        bc = translate(text)
    except Refuse as e:
        print(f"REFUSE: {e}", file=sys.stderr)
        sys.exit(1)
    # success: bytecode ONLY on stdout
    sys.stdout.write(bc + "\n")


if __name__ == "__main__":
    main()
