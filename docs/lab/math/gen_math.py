#!/usr/bin/env python3
"""MATH CREW independent oracle: generates battery.txt + expected.json.

Uses Python Fractions (exact rationals). The Zag learner never reads
expected.json (verified by grep before scoring). Formatting rule shared with
the learner spec: integers plain; terminating decimals as decimals;
non-terminating as exact reduced fractions n/d.
"""
import json
from fractions import Fraction

def fmt(fr):
    fr = Fraction(fr)
    n, d = fr.numerator, fr.denominator
    if d == 1:
        return str(n)
    dd = d
    while dd % 2 == 0: dd //= 2
    while dd % 5 == 0: dd //= 5
    if dd == 1:
        neg = n < 0
        n = abs(n)
        ip, rem = divmod(n, d)
        digs = []
        while rem:
            rem *= 10
            q, rem = divmod(rem, d)
            digs.append(str(q))
        s = str(ip) + ("." + "".join(digs) if digs else "")
        return ("-" if neg else "") + s
    return f"{n}/{d}"

items = []  # (id, text, mode, answer)

def add(i, text, mode, ans):
    items.append((i, text, mode, fmt(ans)))

# ---------------- B1 ARITH ----------------
B1 = [
    ("B1-01", "EXPR: 12345 + 67890", Fraction(80235)),
    ("B1-02", "EXPR: 999999 + 1", Fraction(1000000)),
    ("B1-03", "EXPR: 0 + 0", Fraction(0)),
    ("B1-04", "EXPR: 456789 + 123456", Fraction(580245)),
    ("B1-05", "EXPR: 1000000 + 2000000", Fraction(3000000)),
    ("B1-06", "EXPR: 100000 - 1", Fraction(99999)),
    ("B1-07", "EXPR: 50 - 80", Fraction(-30)),
    ("B1-08", "EXPR: 0 - 123", Fraction(-123)),
    ("B1-09", "EXPR: 987654 - 123456", Fraction(864198)),
    ("B1-10", "EXPR: 1000 - 1000", Fraction(0)),
    ("B1-11", "EXPR: 1234 * 5678", Fraction(7006652)),
    ("B1-12", "EXPR: 999 * 999", Fraction(998001)),
    ("B1-13", "EXPR: 0 * 12345", Fraction(0)),
    ("B1-14", "EXPR: 25 * 40", Fraction(1000)),
    ("B1-15", "EXPR: 123 * 456", Fraction(56088)),
    ("B1-16", "EXPR: 144 / 12", Fraction(12)),
    ("B1-17", "EXPR: 1000 / 8", Fraction(125)),
    ("B1-18", "EXPR: 10 / 3", Fraction(10, 3)),
    ("B1-19", "EXPR: 7 / 2", Fraction(7, 2)),
    ("B1-20", "EXPR: 1 / 4", Fraction(1, 4)),
    ("B1-21", "EXPR: 1/2 + 1/3", Fraction(5, 6)),
    ("B1-22", "EXPR: 3/4 - 1/6", Fraction(7, 12)),
    ("B1-23", "EXPR: 2/3 * 9/4", Fraction(3, 2)),
    ("B1-24", "EXPR: 5/6 / 2/3", Fraction(5, 4)),
    ("B1-25", "EXPR: 1/2 + 1/4 + 1/8", Fraction(7, 8)),
    ("B1-26", "EXPR: 7/3 - 1/2", Fraction(11, 6)),
    ("B1-27", "EXPR: 15% of 240", Fraction(36)),
    ("B1-28", "EXPR: 7.5% of 200", Fraction(15)),
    ("B1-29", "EXPR: 50% of 99", Fraction(99, 2)),
    ("B1-30", "EXPR: 200% of 35", Fraction(70)),
    ("B1-31", "EXPR: 12.5% of 80", Fraction(10)),
    ("B1-32", "EXPR: 2 + 3 * 4", Fraction(14)),
    ("B1-33", "EXPR: (2 + 3) * 4", Fraction(20)),
    ("B1-34", "EXPR: 100 - 4 * 5 + 2", Fraction(82)),
    ("B1-35", "EXPR: (10 - 2) * (3 + 4) / 7", Fraction(8)),
    ("B1-36", "EXPR: 48 / 6 / 2", Fraction(4)),
    ("B1-37", "CONVERT: 3.5 km to m", Fraction(3500)),
    ("B1-38", "CONVERT: 2 hours to seconds", Fraction(7200)),
    ("B1-39", "CONVERT: 1500 m to km", Fraction(3, 2)),
    ("B1-40", "CONVERT: 90 seconds to minutes", Fraction(3, 2)),
]
for i, t, a in B1:
    add(i, t, "COMPUTE", a)

# ---------------- B2 WORD (14 base + 6 paraphrase) ----------------
W = [
    ("W-01", "A baker makes 48 loaves. She sells 17 in the morning and 19 in the afternoon. How many loaves remain?", Fraction(12)),
    ("W-02", "A train travels at 90 kilometers per hour for 4 hours. How far does it travel?", Fraction(360)),
    ("W-03", "A shop buys 25 boxes at 6 coins each. It sells them all for 220 coins. What is the profit?", Fraction(70)),
    ("W-04", "A tank holds 500 liters. One quarter is drained. How many liters remain?", Fraction(375)),
    ("W-05", "A worker earns 18 coins per hour and works 7 hours. She spends half her earnings. How much does she keep?", Fraction(63)),
    ("W-06", "A farmer has 120 apples. He gives 30 to his neighbor and 45 to his sister. How many apples are left?", Fraction(45)),
    ("W-07", "A car drives 240 kilometers in 3 hours. What is its speed in kilometers per hour?", Fraction(80)),
    ("W-08", "A school has 600 students. 40 percent of them are girls. How many girls are there?", Fraction(240)),
    ("W-09", "A recipe needs 2 cups of flour for 8 pancakes. How many cups are needed for 20 pancakes?", Fraction(5)),
    ("W-10", "Tom has 85 marbles. He buys 3 bags with 12 marbles each. How many marbles does he have now?", Fraction(121)),
    ("W-11", "A phone costs 800 coins. The price drops by 25 percent. What is the new price?", Fraction(600)),
    ("W-12", "A garden is 12 meters long and 8 meters wide. What is its area in square meters?", Fraction(96)),
    ("W-13", "Lisa reads 45 pages per day. How many pages does she read in 2 weeks?", Fraction(630)),
    ("W-14", "A bottle contains 2 liters of juice. 5 glasses of 300 milliliters each are poured. How many milliliters remain?", Fraction(500)),
    ("P-01", "A baker bakes 48 loaves. Customers buy 17 loaves in the morning and 19 loaves later in the day. How many loaves are left?", Fraction(12)),
    ("P-02", "A train goes 90 kilometers each hour and keeps going for 4 hours. What distance does it cover?", Fraction(360)),
    ("P-03", "A shop purchases 25 boxes for 6 coins apiece, then sells every box for a total of 220 coins. What is the profit?", Fraction(70)),
    ("P-04", "600 students attend a school, and 40 percent are girls. How many girls attend?", Fraction(240)),
    ("P-05", "Tom owns 85 marbles. He then buys 3 bags, each holding 12 marbles. How many marbles does he own now?", Fraction(121)),
    ("P-06", "Lisa reads 45 pages every day. After 2 weeks, how many pages has she read?", Fraction(630)),
]
for i, t, a in W:
    add(i, t, "COMPUTE", a)

# ---------------- B3 EIFFEL ----------------
ALPHA = Fraction(12, 1000000)
def thermal(L0, T0, T):
    return L0 * (1 + ALPHA * (T - T0))
E = [
    ("E-01", "The Eiffel Tower is 330 meters tall at 20 degrees Celsius. Iron expands 12 millionths per degree Celsius. It is 35 degrees Celsius at 3pm in August. How tall is the tower at 3pm?", "COMPUTE", thermal(Fraction(330), 20, 35)),
    ("E-02", "It is minus 2 degrees Celsius at 6am in January. How tall is the Eiffel Tower?", "COMPUTE", thermal(Fraction(330), 20, -2)),
    ("E-03", "The Eiffel Tower measures 330.0594 meters. The tower is 330 meters at 20 degrees Celsius. Iron expands 12 millionths per degree Celsius. What is the temperature?", "COMPUTE", Fraction(35)),
    ("E-04", "What is the height of the Eiffel Tower at 20 degrees Celsius?", "RETRIEVE", Fraction(330)),
    ("E-05", "In what year was the Eiffel Tower built?", "RETRIEVE", Fraction(1889)),
    ("E-06", "The Oak Street bridge is an iron bridge, 100 meters long at 20 degrees Celsius. It is 40 degrees Celsius at noon. How long is the bridge?", "COMPUTE", thermal(Fraction(100), 20, 40)),
    ("E-07", "It is 20 degrees Celsius. How tall is the Eiffel Tower?", "COMPUTE", Fraction(330)),
    ("E-08", "The Eiffel Tower is 330 meters tall at 20 degrees Celsius. Iron expands 12 millionths per degree Celsius. It is 10 degrees Celsius at midnight. How tall is the tower at midnight?", "COMPUTE", thermal(Fraction(330), 20, 10)),
    ("E-09", "At 3pm the tower is 330.0594 meters tall. At 6am the tower is 329.91288 meters tall. How much taller is the tower at 3pm than at 6am?", "COMPUTE", Fraction(3300594, 10000) - Fraction(32991288, 100000)),
    ("E-10", "A steel rod is 2 meters long at 20 degrees Celsius. Steel expands 12 millionths per degree Celsius. It is 70 degrees Celsius. How long is the rod?", "COMPUTE", thermal(Fraction(2), 20, 70)),
    ("E-11", "What is the expansion coefficient of iron?", "RETRIEVE", ALPHA),
    ("E-12", "The Eiffel Tower is 330 meters tall at 20 degrees Celsius. It is 35 degrees Celsius. How tall is the tower?", "COMPUTE", thermal(Fraction(330), 20, 35)),
]
for i, t, m, a in E:
    add(i, t, m, a)

# ---------------- B4 MODE ----------------
M = [
    ("M-01", "What is the height of the Eiffel Tower at 20 degrees Celsius?", "RETRIEVE", Fraction(330)),
    ("M-02", "How tall is the Eiffel Tower at 35 degrees Celsius?", "COMPUTE", thermal(Fraction(330), 20, 35)),
    ("M-03", "In what year was the Eiffel Tower built?", "RETRIEVE", Fraction(1889)),
    ("M-04", "What is 15 percent of 240?", "COMPUTE", Fraction(36)),
    ("M-05", "What is the expansion coefficient of iron?", "RETRIEVE", ALPHA),
    ("M-06", "A baker makes 48 loaves and sells 17. How many loaves remain?", "COMPUTE", Fraction(31)),
    ("M-07", "How long is the Oak Street bridge at 20 degrees Celsius?", "RETRIEVE", Fraction(100)),
    ("M-08", "How long is the Oak Street bridge at 30 degrees Celsius?", "COMPUTE", thermal(Fraction(100), 20, 30)),
    ("M-09", "What is 7 divided by 2?", "COMPUTE", Fraction(7, 2)),
    ("M-10", "What is the capital of France?", "ABSTAIN", "ABSTAIN"),
    ("M-11", "The Eiffel Tower is 330 meters tall at 20 degrees Celsius. It is 20 degrees Celsius. How tall is the tower?", "EITHER", Fraction(330)),
    ("M-12", "How many meters are in 3.5 kilometers?", "COMPUTE", Fraction(3500)),
]
for i, t, m, a in M:
    items.append((i, t, m, "ABSTAIN" if a == "ABSTAIN" else fmt(a)))

with open("battery.txt", "w") as f:
    for i, t, m, a in items:
        f.write(f"{i}\t{t}\n")
with open("expected.json", "w") as f:
    json.dump({i: {"mode": m, "answer": a} for i, t, m, a in items}, f, indent=1)

print(f"{len(items)} items")
for i, t, m, a in items:
    if i.startswith("E-") or i.startswith("M-"):
        print(i, m, a)
