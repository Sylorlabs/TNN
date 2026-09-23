#!/usr/bin/env python3
"""dirty_inject.py: deterministic, semantics-preserving dirt injection for the
CLN-1 self-critique probe. Inserts (1) an uncalled function before fn main and
(2) an unused local as the first statement of main. Glue only."""
import sys, pathlib

BASE = pathlib.Path.home() / "workspace/tnn-lab/coding/reflection/cleanliness"

DEADFN = "fn tnn_unused_probe(x:i64)i64 {\n  return x+x;\n}\n"
UNUSED = "  let tnn_unused_local:i64=12345;\n"

def main():
    sid = sys.argv[1]
    src = (BASE / "sources" / sid / "tnn.zag").read_text()
    assert "fn main()void {" in src, "no main found"
    # (1) uncalled fn before main
    src = src.replace("fn main()void {", DEADFN + "fn main()void {", 1)
    # (2) unused local as first statement of main body
    src = src.replace("fn main()void {\n", "fn main()void {\n" + UNUSED, 1)
    outdir = BASE / "work" / "selfcrit"
    outdir.mkdir(exist_ok=True)
    (outdir / f"{sid}_dirty.zag").write_text(src)
    print(f"wrote work/selfcrit/{sid}_dirty.zag")

if __name__ == "__main__":
    main()
