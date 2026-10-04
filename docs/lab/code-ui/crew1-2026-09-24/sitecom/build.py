#!/usr/bin/env python3
"""Site builder for T2. Deterministic assembly of the four ladder sites.

For each site spec:
  - each FRAG block -> generated .task -> bin/learn compose (sitecom/frag.card)
  - each TS block   -> generated .task -> bin/learn compose (sitecom/ts.card)
  - index.html assembled from fragment outputs
  - app.ts assembled from TS outputs -> tsc --strict -> app.js
  - style.css copied from sitecom/css/
Provenance of every piece is recorded in PROVENANCE.md per site.
TS patterns are crew-authored scaffold written in the learned idioms
(non-null getElementById, querySelectorAll, classes); HTML/CSS is the
crew's design brief. selene's structure came from the default-design
procedure (see its DESIGN.md).
"""
import os, re, subprocess, sys, shutil

ROOT = os.path.expanduser("~/workspace/code-ui/ts-teaching")
LEARN = ROOT + "/bin/learn"
TSC = ROOT + "/node_modules/.bin/tsc"
SITECOM = ROOT + "/sitecom"
SITES = os.path.expanduser("~/workspace/code-ui/sites")
JUDGE = os.path.expanduser("~/workspace/code-ui/ui-judgment/NEEDS_JUDGMENT")


def parse_spec(path):
    site, title, frags, tss = None, None, [], []
    cur_kind, cur_name, cur_kv = None, None, {}
    for raw in open(path):
        ln = raw.rstrip("\n")
        if ln.startswith("#") or ln == "":
            continue
        if ln.startswith("SITE="):
            site = ln[5:]
            continue
        if ln.startswith("TITLE="):
            title = ln[6:]
            continue
        if ln.startswith("TOPIC="):
            continue
        if ln.startswith("FRAG "):
            cur_kind, cur_name, cur_kv = "frag", ln[5:].strip(), {}
            continue
        if ln == "ENDFRAG":
            frags.append((cur_name, cur_kv)); cur_kind = None
            continue
        if ln.startswith("TS "):
            cur_kind, cur_name, cur_kv = "ts", ln[3:].strip(), {}
            continue
        if ln == "ENDTS":
            tss.append((cur_name, cur_kv)); cur_kind = None
            continue
        if cur_kind and "=" in ln:
            k, v = ln.split("=", 1)
            cur_kv[k] = v
    return site, title, frags, tss


def compose_piece(workdir, idx, kind, tplname, kv, card):
    """Generate a .task, compose via bin/learn, return the emitted body."""
    os.makedirs(workdir, exist_ok=True)
    tp = os.path.join(workdir, "%s_%d.task" % (kind, idx))
    with open(tp, "w") as f:
        f.write("ID=%s%d\nUNIT=site\nTPL=%s\nFILES=single\nPARAMS:\n" % (kind, idx, tplname))
        for k, v in kv.items():
            f.write("%s=%s\n" % (k, v))
        f.write("ENDPARAMS\n")
    p = subprocess.run([LEARN, "compose", tp, SITECOM, card],
                       capture_output=True, text=True, cwd=ROOT)
    if p.returncode != 0:
        raise RuntimeError("compose failed for %s %s: %s" % (kind, tplname, p.stderr))
    m = re.search(r"@@FILE \S+\n(.*?)@@END", p.stdout, re.S)
    if not m:
        raise RuntimeError("no @@FILE block for %s %s" % (kind, tplname))
    if p.stderr.strip():
        print("  warn %s/%s: %s" % (kind, tplname, p.stderr.strip()))
    return m.group(1)


def build_site(spec_path):
    site, title, frags, tss = parse_spec(spec_path)
    outdir = os.path.join(SITES, site)
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.makedirs(outdir)
    workdir = os.path.join(SITECOM, "work", site)
    if os.path.exists(workdir):
        shutil.rmtree(workdir)
    os.makedirs(workdir)
    print("building site", site)
    html_parts = []
    for i, (tplname, kv) in enumerate(frags):
        body = compose_piece(workdir, i, "frag", tplname, kv, "frag.card")
        html_parts.append(body)
    ts_parts = []
    for i, (tplname, kv) in enumerate(tss):
        body = compose_piece(workdir, i, "ts", tplname, kv, "ts.card")
        ts_parts.append(body)
    index = ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\" />\n"
             "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n"
             "<title>%s</title>\n<link rel=\"stylesheet\" href=\"style.css\" />\n</head>\n<body>\n" % title)
    index += "\n".join(html_parts)
    index += "\n<script src=\"app.js\"></script>\n</body>\n</html>\n"
    open(os.path.join(outdir, "index.html"), "w").write(index)
    app_ts = "\n".join(ts_parts) + "\n"
    open(os.path.join(outdir, "app.ts"), "w").write(app_ts)
    shutil.copy(os.path.join(SITECOM, "css", site + ".css"),
                os.path.join(outdir, "style.css"))
    # strict compile
    p = subprocess.run([TSC, "--strict", "--target", "es2020",
                        "--outDir", outdir, os.path.join(outdir, "app.ts")],
                       capture_output=True, text=True, cwd=ROOT)
    diag = (p.stdout or "") + (p.stderr or "")
    if "error TS" in diag:
        print("TSC ERRORS for", site); print(diag)
        raise RuntimeError("tsc failed for " + site)
    # tsc --outDir with a single file arg puts app.js next to... check
    if not os.path.exists(os.path.join(outdir, "app.js")):
        # tsc may have placed it in outdir/app.js already; else find it
        for dp, dn, fn in os.walk(outdir):
            if "app.js" in fn:
                shutil.move(os.path.join(dp, "app.js"), os.path.join(outdir, "app.js"))
                break
    prov = ["# PROVENANCE — site %s" % site,
            "Built %s by the deterministic site builder (sitecom/build.py)." % site,
            "HTML: crew-authored fragment templates (sitecom/frag.card), content from the site spec.",
            "CSS: crew-authored design (sitecom/css/%s.css)." % site,
            "TS: composed by bin/learn (pure Zag) from sitecom/ts.card scaffold patterns,",
            "    which are written in the learned T1 idioms (non-null getElementById,",
            "    querySelectorAll, classes). tsc --strict clean.",
            "TS pieces: " + ", ".join(t for t, _ in tss)]
    open(os.path.join(outdir, "PROVENANCE.md"), "w").write("\n".join(prov) + "\n")
    print("  ok:", site, "tsc clean")
    return outdir


if __name__ == "__main__":
    which = sys.argv[1:] or ["dawn", "gadget", "grid", "selene"]
    for s in which:
        build_site(os.path.join(SITECOM, "specs", s + ".spec"))
    print("all sites built")
