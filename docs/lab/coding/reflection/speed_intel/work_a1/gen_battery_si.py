#!/usr/bin/env python3
"""Build candidate battery_si.json items for the Speed-Intelligence Arm 1 pilot.
12 multi-defect repair seeds (2-3 defects), 6 harder T4 gen items (>=2 KB
patterns), 2 unfixable-by-design. Pilot each at budget 16; freeze only the
seeds that converge in 3-5 iterations and the unfixables that halt honestly.
"""
import json

ALL_PATTERNS = "p_math,p_search,p_slice,p_strrev,p_func,p_loop,p_struct,p_sort,p_argv,p_strcnt,p_slicefill"

def seed(iid, seed_src, tests_stdout, spec="Repair the broken program so it compiles and passes its tests.", demo=""):
    return {"id": iid, "mode": "seed", "spec": spec, "seed": seed_src,
            "patterns": ALL_PATTERNS, "demo": demo, "card": "",
            "tests": [{"args": [], "rc": 0, "stdout": tests_stdout}]}

def gen(iid, spec, stdout, demo=""):
    return {"id": iid, "mode": "gen", "spec": spec, "patterns": ALL_PATTERNS,
            "demo": demo, "card": "",
            "tests": [{"args": [], "rc": 0, "stdout": stdout}]}

items = []

# --- 12 multi-defect repair seeds ---
items.append(seed("S01-syntax-name",
  'fn add(a:i64, b:i64)i64 {\n  return a+b;\n}\nfn main()void {\n  _zag_print(_zag_i64_to_str(ad2(3, 4)));\n  _zag_print("\\n");\n',
  "7\n"))
items.append(seed("S02-arity-type",
  'fn add(a:i32, b:i32)i32 {\n  return a+b;\n}\nfn main()void {\n  let r:i32=add("3", 4, 5);\n  _zag_print(_zag_i64_to_str(r as i64));\n  _zag_print("\\n");\n}\n',
  "7\n"))
items.append(seed("S03-dupfn-name",
  'fn dbl(n:i64)i64 {\n  return n*2;\n}\nfn dbl(n:i64)i64 {\n  return n*2;\n}\nfn main()void {\n  _zag_print(_zag_i64_to_str(dlb(21)));\n  _zag_print("\\n");\n}\n',
  "42\n"))
items.append(seed("S04-syntax-arity",
  'fn add(a:i64, b:i64)i64 {\n  return a+b;\n}\nfn main()void {\n  _zag_print(_zag_i64_to_str(add(3)));\n  _zag_print("\\n");\n',
  "7\n"))
items.append(seed("S05-name-type",
  'fn add(a:i32, b:i32)i32 {\n  return a+b;\n}\nfn main()void {\n  let x:i32=7;\n  x="oops";\n  _zag_print(_zag_i64_to_str(ad2(2, 3)));\n  _zag_print("\\n");\n}\n',
  "5\n"))
items.append(seed("S06-syntax-type-name",
  'fn add(a:i32, b:i32)i32 {\n  return a+b;\n}\nfn main()void {\n  let x:i32=7;\n  x="oops";\n  _zag_print(_zag_i64_to_str(ad2(2, 3)));\n  _zag_print("\\n");\n',
  "5\n"))
items.append(seed("S07-arity-format",
  'fn add(a:i64, b:i64)i64 {\n  return a+b;\n}\nfn main()void {\n  _zag_print(_zag_i64_to_str(add(1, 2, 3)));\n}\n',
  "3\n"))
items.append(seed("S08-name-logic",
  'fn pow2(e:i64)i64 {\n  let r:i64=1;\n  let i:i64=0;\n  while(i<e){r=r*3;i=i+1;}\n  return r;\n}\nfn main()void {\n  _zag_print(_zag_i64_to_str(pwo2(10)));\n  _zag_print("\\n");\n}\n',
  "1024\n",
  spec="T4|GOAL|compute 2 raised to the 10th power", demo="2,10"))
items.append(seed("S09-type-dupfn",
  'fn add(a:i32, b:i32)i32 {\n  return a+b;\n}\nfn add(a:i32, b:i32)i32 {\n  return a+b;\n}\nfn main()void {\n  let r:i32=add("3", 4);\n  _zag_print(_zag_i64_to_str(r as i64));\n  _zag_print("\\n");\n}\n',
  "7\n"))
items.append(seed("S10-syntax-format",
  'fn main()void {\n  _zag_print("42");\n',
  "42\n"))
items.append(seed("S11-arity-name",
  'fn add(a:i64, b:i64)i64 {\n  return a+b;\n}\nfn main()void {\n  _zag_print(_zag_i64_to_str(ad2(1, 2, 3)));\n  _zag_print("\\n");\n}\n',
  "3\n"))
items.append(seed("S12-syntax-type-format",
  'fn main()void {\n  let x:i32=7;\n  x="oops";\n  _zag_print(_zag_i64_to_str(x as i64));\n',
  "7\n"))

# --- 6 harder gen items: T4 GOAL, each needing >=2 KB patterns ---
# count_occ: p_search+p_slice ; sumprimes/fibsum: p_math+p_loop ; selsort: p_sort+p_search
items.append(gen("G05-t4_countocc",
  "T4|GOAL|count how many times 3 appears in the numbers 1,3,5,3,7,3,9",
  "3\n", demo="3,1,3,5,3,7,3,9"))
items.append(gen("G06-t4_sumprimes",
  "T4|GOAL|compute the sum of the prime numbers below 20",
  "77\n", demo="20"))
items.append(gen("G07-t4_fibsum",
  "T4|GOAL|compute the sum of the first 12 fibonacci numbers",
  "376\n", demo="12"))
items.append(gen("G08-t4_selsort",
  "T4|GOAL|sort the numbers 5,3,8,1,4 with selection sort",
  "1 3 4 5 8\n", demo="5,3,8,1,4"))
items.append(gen("G09-t4_countocc2",
  "T4|GOAL|how many times does 7 occur in 7,1,7,2,7,7",
  "4\n", demo="7,7,1,7,2,7,7"))
items.append(gen("G10-t4_sumprimes2",
  "T4|GOAL|compute the sum of the primes below 30",
  "129\n", demo="30"))

# --- 2 unfixable-by-design ---
items.append(gen("X3-unprovable",
  "T4|GOAL|prove that P equals NP",
  "1\n"))
items[-1]["tests"] = [{"args": [], "rc": 0, "stdout": "1\n"}]
items.append(seed("X4-undefloop",
  'fn main()void {\n  let total:i64=0;\n  let i:i64=0;\n  while(i<3){total=total+zzzq;i=i+1;}\n  _zag_print(_zag_i64_to_str(total));\n  _zag_print("\\n");\n}\n',
  "0\n"))

battery = {"name": "speed-intelligence SI battery v1 (PILOT candidates)", "items": items}
with open("battery_si_pilot.json", "w") as f:
    json.dump(battery, f, indent=1, sort_keys=True)
print("wrote battery_si_pilot.json with %d items" % len(items))
