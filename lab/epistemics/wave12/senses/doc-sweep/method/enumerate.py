#!/usr/bin/env python3
"""Recursively enumerate the Drive TNN folder; collect document files.
Checkpointed in the workspace so a restart can resume.
Writes OUT/docs.json at the end; OUT/checkpoint.json incrementally.
Read-only: no Drive modifications."""
import json, os, subprocess, sys

CLI = "hatch_gws_cli"
ROOT = "13279S7nBlFewa8sGZtRWO3fUpxJKl0WF"  # My Drive / TNN
OUT = os.path.expanduser("~/workspace/tnn-lab/wave12/senses/doc-sweep")
os.makedirs(OUT, exist_ok=True)
CKPT = f"{OUT}/checkpoint.json"

DOC_EXTS = (".md", ".markdown", ".txt", ".doc", ".docx", ".rtf", ".pdf", ".tex", ".org")
GDOC_MIMES = {
    "application/vnd.google-apps.document": ".gdoc",
    "application/vnd.google-apps.spreadsheet": ".gsheet",
    "application/vnd.google-apps.presentation": ".gslides",
}
FOLDER = "application/vnd.google-apps.folder"

def drive_list(q, page_token=None):
    params = {"q": q, "pageSize": 1000,
              "fields": "nextPageToken,files(id,name,mimeType,size,modifiedTime,parents)"}
    if page_token:
        params["pageToken"] = page_token
    cmd = [CLI, "drive", "files", "list", "--params", json.dumps(params)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"list failed: {r.stderr[:300]}")
    return json.loads(r.stdout)

def children(folder_id):
    out = []
    tok = None
    while True:
        d = drive_list(f"'{folder_id}' in parents and trashed=false", tok)
        out.extend(d.get("files", []))
        tok = d.get("nextPageToken")
        if not tok:
            break
    return out

def is_doc(name, mime):
    ln = name.lower()
    return ln.endswith(DOC_EXTS) or mime in GDOC_MIMES

def save_ckpt(state):
    tmp = CKPT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f)
    os.replace(tmp, CKPT)

def main():
    if os.path.exists(CKPT):
        with open(CKPT) as f:
            state = json.load(f)
        print(f"resuming: {state['folders']} folders, {state['files_total']} files, {len(state['docs'])} docs", flush=True)
    else:
        state = {"stack": [[ROOT, "TNN"]], "seen": [], "docs": [],
                 "folders": 0, "files_total": 0}
    seen = set(state["seen"])
    stack = state["stack"]
    docs = state["docs"]
    folders = state["folders"]
    files_total = state["files_total"]
    while stack:
        fid, path = stack.pop()
        if fid in seen:
            continue
        seen.add(fid)
        folders += 1
        try:
            kids = children(fid)
        except RuntimeError as e:
            print(f"WARN {path}: {e}", file=sys.stderr, flush=True)
            continue
        for k in kids:
            mt = k.get("mimeType", "")
            nm = k.get("name", "")
            if mt == FOLDER:
                stack.append([k["id"], f"{path}/{nm}"])
            else:
                files_total += 1
                if is_doc(nm, mt):
                    docs.append({
                        "id": k["id"], "name": nm, "mimeType": mt,
                        "size": k.get("size"), "modifiedTime": k.get("modifiedTime"),
                        "path": f"{path}/{nm}",
                    })
        if folders % 25 == 0:
            state.update({"stack": stack, "seen": sorted(seen), "docs": docs,
                          "folders": folders, "files_total": files_total})
            save_ckpt(state)
            print(f"... {folders} folders, {files_total} files, {len(docs)} docs", flush=True)
    docs.sort(key=lambda d: d["path"].lower())
    with open(f"{OUT}/docs.json", "w") as f:
        json.dump(docs, f, indent=1)
    state.update({"stack": [], "seen": sorted(seen), "docs": docs,
                  "folders": folders, "files_total": files_total, "done": True})
    save_ckpt(state)
    print(f"DONE folders={folders} files={files_total} docs={len(docs)}")
    from collections import Counter
    c = Counter()
    for d in docs:
        n = d["name"].lower()
        ext = "gdoc" if d["mimeType"] in GDOC_MIMES else os.path.splitext(n)[1]
        c[ext] += 1
    print(dict(c))

if __name__ == "__main__":
    main()
