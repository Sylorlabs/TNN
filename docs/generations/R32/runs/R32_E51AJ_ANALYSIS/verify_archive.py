"""Verify exact Actions archive/source identity, then rerun only the frozen parser.

Usage: python3 -B Research/R32_E51AJ_ANALYSIS/verify_archive.py ARCHIVE --run ID --source SHA
The archive contains RUN.json, JOBS.json, ARTIFACTS.json and artifact.zip.
No native cognitive binary is executed by this program.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import runpy
import stat
import subprocess
import zipfile

COMPILER = "498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_member(name):
    p = PurePosixPath(name)
    return bool(name) and not p.is_absolute() and ".." not in p.parts and "\\" not in name


def inspect_zip(archive):
    entries = archive.infolist()
    require(len({item.filename for item in entries}) == len(entries), "duplicate archive members")
    require(sum(item.file_size for item in entries) <= 4*1024**3, "archive size cap")
    for item in entries:
        require(safe_member(item.filename) and not stat.S_ISLNK(item.external_attr >> 16), "unsafe archive member")
        require(item.file_size <= 1024**3, "individual file size cap")
    require(archive.testzip() is None, "archive CRC")
    return entries


def git_bytes(repo, source, path):
    return subprocess.check_output(["git", "show", f"{source}:{path}"],cwd=repo,timeout=20)


def audit(base, repo, expected_run, source):
    run = json.loads((base/"RUN.json").read_text())
    jobs = json.loads((base/"JOBS.json").read_text())["jobs"]
    artifacts = json.loads((base/"ARTIFACTS.json").read_text())["artifacts"]
    require(run["id"] == expected_run and run["head_sha"] == source and run["run_attempt"] == 1, "run/source/attempt mismatch")
    require(run["repository"]["full_name"] == "Sylorlabs/TNN", "repository mismatch")
    require(run["status"] == "completed", "run not terminal")
    require(run["path"] == ".github/workflows/r32-e51aj-native.yml", "workflow mismatch")
    tree = subprocess.check_output(["git","rev-parse",source+"^{tree}"],cwd=repo,timeout=20).decode().strip()
    require(run["head_commit"]["tree_id"] == tree, "source tree mismatch")
    matching_jobs = [job for job in jobs if job["name"] == "execute" and job["run_id"] == expected_run]
    require(len(matching_jobs) == 1, "job identity ambiguous")
    job = matching_jobs[0]
    require(job["head_sha"] == source and job["status"] == "completed", "job source or terminal state")
    matching = [a for a in artifacts if a["name"] == "r32-e51aj-native-"+source]
    require(len(matching) == 1, "artifact missing or duplicated")
    artifact = matching[0]
    require(artifact["workflow_run"]["id"] == expected_run and artifact["workflow_run"]["head_sha"] == source, "artifact lineage")
    data = (base/"artifact.zip").read_bytes()
    require(len(data) == artifact["size_in_bytes"], "archive size mismatch")
    require(artifact["digest"] == "sha256:"+sha(data), "archive digest mismatch")
    out = base/"extracted"
    with zipfile.ZipFile(base/"artifact.zip") as z:
        entries = inspect_zip(z)
        if not out.exists():
            out.mkdir()
            z.extractall(out)
        for item in entries:
            if not item.is_dir():
                require((out/item.filename).read_bytes() == z.read(item), f"extracted bytes changed: {item.filename}")
    require((out/"SOURCE_COMMIT.txt").read_text().strip() == source, "archived source marker")
    require((out/"WORKFLOW_RUN_ID.txt").read_text().strip() == str(expected_run), "archived run marker")
    require((out/"RUN_ATTEMPT.txt").read_text().strip() == "1", "archived attempt marker")
    manifest = json.loads((out/"SOURCE_MANIFEST.json").read_text())
    require(len(manifest["files"]) == 65, "unexpected source input count")
    for entry in manifest["files"]:
        path = entry["path"]
        require(safe_member(path), "source input path")
        frozen = git_bytes(repo,source,path)
        require((out/"inputs"/path).read_bytes() == frozen and sha(frozen) == entry["sha256"], f"source input differs: {path}")
        require((repo/path).read_bytes() == frozen, f"local frozen source changed: {path}")
    pin_path = "Research/R32_E51AJ_SOURCE_PIN.json"
    pin = json.loads(git_bytes(repo,source,pin_path))
    require(sha((out/"SOURCE.zag").read_bytes()) == pin["source_sha256"], "native source pin mismatch")
    compiler = repo/"Research/toolchain/znc_linux_x86_64_abed8aa1"
    require(sha(compiler.read_bytes()) == COMPILER, "local official compiler changed")
    baseline = "Research/R32_E51_BASELINE_V1.json"
    require((repo/baseline).read_bytes() == git_bytes(repo,"09c5fcf63f295b52b6c82299d01ac340d554dd4e",baseline), "immutable baseline changed")
    checker = ".github/scripts/e51aj_verify.py"
    independent = runpy.run_path(str(repo/checker))["verify"](out)
    archived = json.loads((out/"EVIDENCE_CHECK.json").read_text())
    require(independent == archived and independent["verified"] is True, "independent scientific verification differs")
    require(run["conclusion"] == "success" and job["conclusion"] == "success", "workflow did not succeed")
    (base/"LOCAL_EVIDENCE_CHECK.json").write_text(json.dumps(independent,indent=2)+"\n")
    return {"verified":True,"errors":[],"run":expected_run,"attempt":1,"job":job["id"],"workflow":run["workflow_id"],
            "source_commit":source,"source_tree":tree,"artifact_id":artifact["id"],
            "zip_sha256":sha(data),"zip_bytes":len(data),"zip_files_verified":sum(not i.is_dir() for i in entries),
            "source_inputs_verified":65,"immutable_baseline_unchanged":True,
            "outcome":independent["outcome"],"retention_result":independent["retention_result"],
            "probe_episode_rows_verified":independent["probe_episode_rows_verified"],
            "coefficient_rows_verified":independent["coefficient_rows_verified"],
            "sha256":independent["sha256"],"native_runtime":independent["native_runtime"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive",type=Path)
    parser.add_argument("--run",type=int,required=True)
    parser.add_argument("--source",required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    try:
        report = audit(args.archive.resolve(),repo,args.run,args.source)
    except (OSError,ValueError,KeyError,IndexError,TypeError,zipfile.BadZipFile,subprocess.SubprocessError) as exc:
        report = {"verified":False,"errors":[f"{type(exc).__name__}: {exc}"]}
    (args.archive/"IDENTITY_CHECK.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if report["verified"] else 1)
