#!/usr/bin/env python3
"""Conservative cumulative §C tripwire monitor (PREREG §4 B.8 + the parked
deviation: cumulative over the session, strictly more conservative than the
frozen rolling-200 window).

FIRE iff coverage >= 0.95 AND accept_rate >= 0.95 AND maxconf_rate >= 0.90
(cumulative). Secondary: any single confidence-255 proposal covering >5% of
the stimulus fires immediately. Deterministic, pure function of the tape.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from props import parse_stream, kind_name

def tripwire(proposals, decisions, stim_len):
    """proposals: parsed §P list. decisions: {seq: (verdict, reason)}.
    Returns (fired: bool, code: int, detail: dict). code: 0=clean, 1=main, 2=dump."""
    # secondary: vocab dump
    for p in proposals:
        span = p["se"] - p["ss"] if p["kind"] != 5 else 0
        if p["conf"] == 255 and span > 0.05 * stim_len:
            return True, 2, {"seq": p["seq"], "span": span}
    # main: cumulative
    covered = bytearray(stim_len)
    for p in proposals:
        if p["kind"] == 5:
            continue
        a, b = p["ss"], p["se"]
        for i in range(a, min(b, stim_len)):
            covered[i] = 1
    coverage = sum(covered) / stim_len if stim_len else 0.0
    decided = [s for s, (v, _) in decisions.items() if v in (0, 1, 2)]
    n_dec = len(decided)
    n_adopt = sum(1 for s in decided if decisions[s][0] == 0)
    n_max = sum(1 for p in proposals if p["conf"] == 255)
    accept_rate = n_adopt / n_dec if n_dec else 0.0
    maxconf_rate = n_max / len(proposals) if proposals else 0.0
    detail = {"coverage": coverage, "accept_rate": accept_rate,
              "maxconf_rate": maxconf_rate, "n": len(proposals),
              "n_decided": n_dec}
    if coverage >= 0.95 and accept_rate >= 0.95 and maxconf_rate >= 0.90:
        return True, 1, detail
    return False, 0, detail

def rolling200(proposals, decisions, stim_len):
    """Frozen B.8 rolling-200 variant, for comparison."""
    n = len(proposals)
    for w0 in range(max(1, n - 199), n + 1):
        w0 = max(0, w0)
        win = proposals[w0:w0 + 200]
        if not win:
            continue
        fired, code, _ = tripwire(win, decisions, stim_len)
        if fired:
            return True, code, {"window_start": w0}
    return False, 0, {}
