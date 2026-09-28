#!/usr/bin/env python3
"""Adapter contract for the WS3-B popularity-bias adversarial battery.

Copy this file and implement judge(). The harness (run_battery.sh) imports
your module and calls judge() once per probe in probes.jsonl file order.

Contract (frozen, see PREREG_WS3B.md section 7):
  1. ISOLATION: the probe dict is the complete input. No external knowledge,
     no web, no background KB lookups. Present the claim cold (fresh instance
     or explicit probe mode).
  2. INDEPENDENCE: no cross-probe memory. Judging probe N must not depend on
     probes 1..N-1.
  3. DETERMINISM: same probe -> byte-identical output. The harness runs the
     full battery twice and diffs; any difference fails the run on procedure.

Input probe fields: probe_id, family, claim, exposure (int), evidence (list
of {"kind","strength","detail"}), near_miss (bool), synthetic (bool),
pair_id (str or null).

Return: {"verdict": "ACCEPT"|"REJECT"|"UNDECIDED", "credence": float in [0,1]}.

Document any deviation from 1-3 in your run report; the scorer grants no
allowances.
"""


def judge(probe: dict) -> dict:
    raise NotImplementedError("implement judge() for the mechanism under test")
