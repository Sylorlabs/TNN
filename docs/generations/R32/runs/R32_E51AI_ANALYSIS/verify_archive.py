"""Verify the exact E51AI archive and frozen scientific checker; never run cognition.

Usage: python3 -B Research/R32_E51AI_ANALYSIS/verify_archive.py ARCHIVE_DIRECTORY
The archive directory must contain RUN.json, JOBS.json, ARTIFACTS.json and artifact.zip.
Repository identities and the scientific verifier are pinned to the executed source.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import runpy
import stat
import subprocess
import zipfile

SOURCE = "c46fbbf67e1b7d5a19dee7ca1164fc4c5b0eec22"
TREE = "03cf947e05765875ec63131e802d444f1490f2c4"
RUN = 33949274757
JOB = 101260866273
SOURCE_SHA = "20916b1836b15fa591d204766f3eadf8f62a2e23ab4203e717ff279fb078bb61"
PREREG_SHA = "cf3ab1ae1fef2acbac855a462c6379f7fb7efb682ec14934ac7f3be91bd8d469"
COMPILER_SHA = "498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef"


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_member(name):
    path = PurePosixPath(name)
    return bool(name) and not path.is_absolute() and ".." not in path.parts and "\\" not in name


def audit(base, repo):
    run = json.loads((base / "RUN.json").read_text())
    jobs = json.loads((base / "JOBS.json").read_text())["jobs"]
    artifacts = json.loads((base / "ARTIFACTS.json").read_text())["artifacts"]
    require(run["id"] == RUN and run["run_attempt"] == 1 and run["workflow_id"] == 350732604,
            "run/attempt/workflow mismatch")
    require(run["repository"]["full_name"] == "Sylorlabs/TNN" and run["head_sha"] == SOURCE,
            "repository/source mismatch")
    require(run["head_commit"]["tree_id"] == TREE and run["status"] == "completed", "tree mismatch or run not terminal")
    job = next(item for item in jobs if item["id"] == JOB)
    require(job["run_id"] == RUN and job["head_sha"] == SOURCE, "job identity mismatch")
    matching = [item for item in artifacts if item["name"] == f"r32-e51ai-native-{SOURCE}"]
    require(len(matching) == 1, "missing/duplicate artifact")
    artifact = matching[0]
    require(artifact["workflow_run"]["id"] == RUN and artifact["workflow_run"]["head_sha"] == SOURCE,
            "artifact lineage mismatch")
    data = (base / "artifact.zip").read_bytes()
    require(len(data) == artifact["size_in_bytes"], "artifact size mismatch")
    require(artifact.get("digest") == "sha256:" + digest(data), "GitHub artifact digest mismatch")
    out = base / "extracted"
    with zipfile.ZipFile(base / "artifact.zip") as archive:
        entries = archive.infolist()
        require(len({item.filename for item in entries}) == len(entries), "duplicate archive members")
        require(sum(item.file_size for item in entries) < 1024 * 1024 * 1024, "unexpected uncompressed archive size")
        for item in entries:
            require(safe_member(item.filename) and not stat.S_ISLNK(item.external_attr >> 16), "unsafe member or symlink")
        require(archive.testzip() is None, "CRC failure")
        if not out.exists():
            out.mkdir()
            archive.extractall(out)
        for item in entries:
            if not item.is_dir():
                require((out / item.filename).read_bytes() == archive.read(item), f"extracted bytes differ: {item.filename}")
    require((out / "SOURCE_COMMIT.txt").read_text().strip() == SOURCE, "source marker mismatch")
    require((out / "WORKFLOW_RUN_ID.txt").read_text().strip() == str(RUN), "run marker mismatch")
    require((out / "RUN_ATTEMPT.txt").read_text().strip() == "1", "attempt marker mismatch")
    require(digest((out / "SOURCE.zag").read_bytes()) == SOURCE_SHA, "assembled-source pin mismatch")
    manifest = json.loads((out / "SOURCE_MANIFEST.json").read_text())
    require(len(manifest["files"]) == 53, "unexpected source-input count")
    for entry in manifest["files"]:
        path = entry["path"]
        require(safe_member(path), "unsafe source manifest path")
        saved = (out / "inputs" / path).read_bytes()
        frozen = subprocess.check_output(["git", "show", f"{SOURCE}:{path}"], cwd=repo, timeout=20)
        require(saved == frozen and digest(saved) == entry["sha256"], f"frozen source differs: {path}")
        blob = hashlib.sha1(b"blob " + str(len(saved)).encode() + b"\0" + saved).hexdigest()
        require(blob == entry["git_blob"], f"Git blob mismatch: {path}")
    require(digest((out / "inputs/Research/R32_E51AI_LONGITUDINAL_CONTEXT_PREREG.md").read_bytes()) == PREREG_SHA,
            "preregistration pin mismatch")
    compiler = repo / "Research/toolchain/znc_linux_x86_64_abed8aa1"
    require(digest(compiler.read_bytes()) == COMPILER_SHA, "persisted official compiler mismatch")
    require((out / "COMPILER_SHA256SUMS.txt").read_text().split()[0] == COMPILER_SHA, "run compiler mismatch")
    baseline = "Research/R32_E51_BASELINE_V1.json"
    baseline_bytes = subprocess.check_output(
        ["git", "show", f"09c5fcf63f295b52b6c82299d01ac340d554dd4e:{baseline}"], cwd=repo, timeout=20)
    require((repo / baseline).read_bytes() == baseline_bytes, "immutable baseline changed")
    checker = repo / ".github/scripts/e51ai_verify.py"
    require(checker.read_bytes() == (out / "inputs/.github/scripts/e51ai_verify.py").read_bytes(),
            "local checker differs from frozen run checker")
    independent = runpy.run_path(str(checker))["verify"](out)
    archived = json.loads((out / "EVIDENCE_CHECK.json").read_text())
    require(independent == archived and independent["verified"], "independent and archived scientific checks differ")
    (base / "LOCAL_EVIDENCE_CHECK.json").write_text(json.dumps(independent, indent=2) + "\n")
    require(run["conclusion"] == "success" and job["conclusion"] == "success", "workflow did not finish successfully")
    return {"verified": True, "errors": [], "run": RUN, "job": JOB, "source_commit": SOURCE,
            "artifact_id": artifact["id"], "zip_sha256": digest(data), "zip_bytes": len(data),
            "zip_files_verified": sum(not item.is_dir() for item in entries), "source_inputs_verified": 53,
            "native_runtime_seconds": int((out / "RUNTIME_SECONDS.txt").read_text()),
            "native_exit_code": int((out / "EXIT_CODE.txt").read_text()),
            "independent_scientific_verifier_passed": True, "immutable_baseline_unchanged": True,
            "outcome": independent["outcome"], "final_metrics": independent["final_metrics"],
            "history_preserving_signal": independent["history_preserving_signal"], "longevity": independent["longevity"],
            "sha256": independent["sha256"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    base = args.archive.resolve()
    try:
        report = audit(base, args.repo.resolve())
    except (OSError, ValueError, KeyError, IndexError, StopIteration, TypeError,
            zipfile.BadZipFile, subprocess.SubprocessError) as exc:
        report = {"verified": False, "errors": [f"{type(exc).__name__}: {exc}"]}
    (base / "IDENTITY_CHECK.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["verified"] else 1)
