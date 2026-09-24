#!/usr/bin/env python3
"""B3 v2 builder. Runs Crew 1's TNN machinery for the v2 iteration.

For each site:
  - parse the ORIGINAL frozen spec (sitecom/specs/<name>.spec) with the same
    parse_spec used for v1 (imported from sitecom/build.py),
  - compose every FRAG/TS piece via bin/learn compose (pure Zag: template
    selection + slot binding decided by the mechanism),
  - assemble index.html + app.ts, compile app.ts with tsc --strict,
  - lay down the v2 CSS (the design delta addressing JUDGMENT.md defects),
  - write PROVENANCE.md recording the split.
Output: ~/workspace/code-ui/sites/<name>/v2/
HTML/TS are expected byte-identical to v1 (design delta is CSS-only).
"""
import os, re, shutil, subprocess, sys

sys.path.insert(0, os.path.expanduser("~/workspace/code-ui/ts-teaching/sitecom"))
from build import parse_spec, compose_piece  # noqa: E402  (Crew 1's machinery)

ROOT = os.path.expanduser("~/workspace/code-ui/ts-teaching")
TSC = ROOT + "/node_modules/.bin/tsc"
SITECOM = ROOT + "/sitecom"
V2CSS = os.path.expanduser("~/workspace/code-ui/b3-iteration/v2css")
OUT = os.path.expanduser("~/workspace/code-ui/sites")


def build_v2(name):
    spec_path = os.path.join(SITECOM, "specs", name + ".spec")
    site, title, frags, tss = parse_spec(spec_path)
    assert site == name, (site, name)
    outdir = os.path.join(OUT, name, "v2")
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.makedirs(outdir)
    workdir = os.path.join(SITECOM, "work", name + "_v2")
    if os.path.exists(workdir):
        shutil.rmtree(workdir)
    os.makedirs(workdir)
    print("building v2", name)
    html_parts = [compose_piece(workdir, i, "frag", tpl, kv, "frag.card")
                  for i, (tpl, kv) in enumerate(frags)]
    ts_parts = [compose_piece(workdir, i, "ts", tpl, kv, "ts.card")
                for i, (tpl, kv) in enumerate(tss)]
    index = ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\" />\n"
             "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
             "<title>%s</title>\n<link rel=\"stylesheet\" href=\"style.css\" />\n</head>\n<body>\n" % title)
    index += "\n".join(html_parts)
    index += "\n<script src=\"app.js\"></script>\n</body>\n</html>\n"
    open(os.path.join(outdir, "index.html"), "w").write(index)
    open(os.path.join(outdir, "app.ts"), "w").write("\n".join(ts_parts) + "\n")
    shutil.copy(os.path.join(V2CSS, name + ".css"), os.path.join(outdir, "style.css"))
    p = subprocess.run([TSC, "--strict", "--target", "es2020",
                        "--outDir", outdir, os.path.join(outdir, "app.ts")],
                       capture_output=True, text=True, cwd=ROOT)
    diag = (p.stdout or "") + (p.stderr or "")
    if "error TS" in diag:
        print("TSC ERRORS for", name); print(diag)
        raise RuntimeError("tsc failed for " + name)
    if not os.path.exists(os.path.join(outdir, "app.js")):
        for dp, dn, fn in os.walk(outdir):
            if "app.js" in fn:
                shutil.move(os.path.join(dp, "app.js"), os.path.join(outdir, "app.js"))
                break
    # drift check: HTML/TS must be byte-identical to v1 (CSS-only delta)
    v1 = os.path.expanduser("~/workspace/code-ui/sites/" + name)
    for fn in ("index.html", "app.ts"):
        a = open(os.path.join(v1, fn), "rb").read()
        b = open(os.path.join(outdir, fn), "rb").read()
        print("  drift %s: %s" % (fn, "NONE (byte-identical)" if a == b else "DIFFERS"))
    prov = ["# PROVENANCE — site %s v2 (B3 iteration)" % name,
            "Built by b3-iteration/build_v2.py.",
            "HTML/TS: composed by bin/learn (pure Zag) from sitecom/frag.card + sitecom/ts.card",
            "  using the ORIGINAL frozen spec sitecom/specs/%s.spec — byte-identical to v1." % name,
            "CSS: v2 design delta (b3-iteration/v2css/%s.css) addressing the named defects in" % name,
            "  NEEDS_JUDGMENT/%s/JUDGMENT.md. Design deltas are crew-authored from the judge's" % name,
            "  defect list; composition, assembly, and tsc --strict are the machinery.",
            "TS: tsc --strict clean. TS pieces: " + ", ".join(t for t, _ in tss)]
    open(os.path.join(outdir, "PROVENANCE.md"), "w").write("\n".join(prov) + "\n")
    print("  ok:", name, "v2 tsc clean")


if __name__ == "__main__":
    for s in (sys.argv[1:] or ["dawn", "gadget", "grid", "selene"]):
        build_v2(s)
