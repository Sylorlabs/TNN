#!/usr/bin/env python3
"""Extract frozen specs from the O1 prereg + verdict by script (never memory).

Reads:
  ~/workspace/pam_round2/o1_delivery/PREREG_O1_DELIVERY.md
  ~/workspace/pam_round2/o1_delivery/VERDICT_O1_DELIVERY.md
Emits JSON with every numeric spec the C3 prereg depends on.
"""
import json, re, sys, os

BASE = os.path.expanduser("~/workspace/pam_round2/o1_delivery")
prereg = open(os.path.join(BASE, "PREREG_O1_DELIVERY.md")).read()
verdict = open(os.path.join(BASE, "VERDICT_O1_DELIVERY.md")).read()

specs = {}

# --- frozen evidence identity (prereg) ---
m = re.search(r"sweep\.jsonl`\s*\n?\(11,840 rows, sha256 `([0-9a-f]{64})`\)", prereg)
specs["sweep_rows"] = 11840
specs["sweep_sha256"] = m.group(1) if m else None

# --- K1/K2 frozen (prereg section 1) ---
m = re.search(r"K1 = ([\d,]+)/([\d,]+) \(([\d.]+)%\)", prereg)
specs["k1_num"] = int(m.group(1).replace(",", ""))
specs["k1_den"] = int(m.group(2).replace(",", ""))
specs["k1_pct"] = float(m.group(3))
m = re.search(r"K2 = ([\d,]+)/([\d,]+) \(([\d.]+)%\)", prereg)
specs["k2_num"] = int(m.group(1).replace(",", ""))
specs["k2_den"] = int(m.group(2).replace(",", ""))
specs["k2_pct"] = float(m.group(3))

# --- 255 decomposition (prereg section 1) ---
m = re.search(r"The 255 undelivered-but-present trials.*?decompose as:\n- (\d+): `prog=UNRESOLVED`", prereg, re.S)
specs["undelivered_total"] = 255
specs["undelivered_unresolved"] = int(m.group(1))
m = re.search(r"- (\d+): deliberation downgraded", prereg)
specs["undelivered_downgrades"] = int(m.group(1))
m = re.search(r"- (\d+): `prog=FAIL`", prereg)
specs["undelivered_fail"] = int(m.group(1))

# --- (agree,strong) on the 255 (prereg section 1) ---
m = re.search(r"By \(`agree`,`strong`\) on the 255: \(1,0\):(\d+), \(0,0\):(\d+), \(1,1\):(\d+), \(0,1\):(\d+)", prereg)
specs["as_10"] = int(m.group(1))
specs["as_00"] = int(m.group(2))
specs["as_11"] = int(m.group(3))
specs["as_01"] = int(m.group(4))

# --- safety boundary (prereg section 1) ---
m = re.search(r"(\d+) WRONG high-conf percepts have `progF==PASS`", prereg)
specs["wrong_hiconf_progf_pass"] = int(m.group(1))
m = re.search(r"RK-2 \(currently ([\d/,]+) wrong high-conf permanent installs\)", prereg)
specs["rk2_frozen"] = m.group(1)

# --- adjudicator rule (prereg section 2) ---
m = re.search(r"`progF == PASS AND agree == 1 AND conf >= (\d+)`", prereg)
specs["adjudicator_conf_bar"] = int(m.group(1))
m = re.search(r"with it,\s*\n?\s*(\d+) correct / (\d+) wrong on frozen evidence", prereg)
specs["adjudicator_correct_admitted"] = int(m.group(1))
specs["adjudicator_wrong_admitted"] = int(m.group(2))

# --- RK-3 frozen (prereg section 3) ---
m = re.search(r"RK-3 frozen = (\d+)/([\d,]+) = ([\d.]+)%", prereg)
specs["rk3_num"] = int(m.group(1))
specs["rk3_den"] = int(m.group(2).replace(",", ""))
specs["rk3_pct"] = float(m.group(3))

# --- kill bars (prereg section 4; O1b bar value from verdict) ---
m = re.search(r"K2' .? ([\d.]+)%", prereg)
specs["kb_o1a_k2prime_bar_pct"] = float(m.group(1))
m = re.search(r"required RK-3' .? ([\d.]+)%", verdict)
specs["kb_o1b_rk3prime_bar_pct"] = float(m.group(1))

# --- verdict numbers (verdict) ---
m = re.search(r"K2 \(delivered\) \| [\d,/ ]+\([\d.]+%\) \| ([\d,/ ]+)\(([\d.]+)%\)", verdict)
specs["verdict_k2prime"] = m.group(1).strip()
specs["verdict_k2prime_pct"] = float(m.group(2))
m = re.search(r"RK-3 \(installed\) \| [\d,/ ]+\([\d.]+%\) \| ([\d,/ ]+)\(([\d.]+)%\)", verdict)
specs["verdict_rk3prime"] = m.group(1).strip()
specs["verdict_rk3prime_pct"] = float(m.group(2))
m = re.search(r"Records repaired \| .+ \| (\d+)", verdict)
specs["verdict_records_repaired"] = int(m.group(1))
m = re.search(r"\*\*Verdict: (KILL)\.", verdict)
specs["verdict_outcome"] = m.group(1)

# --- residual decomposition (verdict) ---
m = re.search(r"- (\d+) CONFLICT_WITHHELD", verdict)
specs["residual_conflict_withheld"] = int(m.group(1))
m = re.search(r"- (\d+) SUPPRESSED", verdict)
specs["residual_suppressed"] = int(m.group(1))
m = re.search(r"- (\d+) never admitted", verdict)
specs["residual_never_admitted"] = int(m.group(1))
m = re.search(r"\(0,0\) holds (\d+) wrong high-conf", verdict)
specs["as00_wrong_hiconf"] = int(m.group(1))
m = re.search(r"\(0,1\) holds (\d+) wrong high-conf", verdict)
specs["as01_wrong_hiconf"] = int(m.group(1))

# --- redirect targets (verdict) ---
specs["redirect"] = [
    "corroborated-revision gate rule (conflict)",
    "corroborated negative evidence (suppression)",
    "prereg-(f) (g)-predicate revision (125 never-admitted; out of gate scope)",
]

# sanity: decomposition adds up
assert specs["undelivered_unresolved"] + specs["undelivered_downgrades"] + specs["undelivered_fail"] == 255
assert specs["as_10"] + specs["as_00"] + specs["as_11"] + specs["as_01"] == 255
assert specs["residual_conflict_withheld"] + specs["residual_suppressed"] + 2 == 130  # 128 + 2 downgrades admitted
assert specs["rk3_den"] == specs["k1_den"] == specs["k2_den"] == 1102

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "o1_specs.json")
json.dump(specs, open(out, "w"), indent=2)
print(f"wrote {out}: {len(specs)} specs")
for k in sorted(specs):
    print(f"  {k} = {specs[k]}")
