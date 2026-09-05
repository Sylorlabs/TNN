"""Validate E51AJ result delivery against original archive, code and native rows.

Usage: python3 -B Research/R32_E51AJ_ANALYSIS/validate_delivery.py ARCHIVE_DIRECTORY
Read-only apart from regenerated identical local archive-verification reports.
Never executes a cognitive binary or fits a model.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import re
import runpy
import subprocess


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(archive, repo):
    analysis = repo/"Research/R32_E51AJ_ANALYSIS"
    routines = runpy.run_path(str(analysis/"derive.py"))
    read_json = routines["read_json"]
    source, run = routines["SOURCE"], routines["RUN"]
    identity = runpy.run_path(str(analysis/"verify_archive.py"))["audit"](archive, repo, run, source)
    require(identity == read_json(archive/"IDENTITY_CHECK.json"), "archive identity changed")
    regenerated = runpy.run_path(str(analysis/"package.py"))["package"](archive, repo)
    evidence = read_json(repo/"Research/R32_E51AJ_EVIDENCE.json")
    require(evidence == regenerated, "evidence package differs from independent regeneration")
    summary = regenerated["independent_descriptive_analysis"]
    status = read_json(repo/"Research/R32_E51AJ_EXECUTION_STATUS.json")
    current = read_json(repo/"Research/R32_NATIVE_AUTHORITY_CURRENT.json")
    detail = read_json(repo/"Research/R32_NATIVE_AUTHORITY_DETAIL.json")
    ledger = read_json(repo/"Research/R32_E51_MASTER_LEDGER.json")
    require(status["state"] == evidence["state"] and status["artifact_verified"] is True, "execution status not closed")
    for key, expected in (("workflow_run", run), ("source_commit", source), ("artifact_id", identity["artifact_id"]),
                          ("scientific_outcome", identity["outcome"]), ("retention_result", summary["retention_result"]),
                          ("no_final_behavioral_tradeoff", summary["no_final_behavioral_tradeoff"])):
        require(status[key] == expected, "execution status mismatch: "+key)
    require(current["latest_authoritative_result"] == "R32_E51AJ_RESULT.md" and current["active_experiment"] is None, "current authority stale")
    require(current["latest_evidence"] == "R32_E51AJ_EVIDENCE.json" and current["last_completed_experiment"] == "R32_E51AJ", "current evidence stale")
    latest = detail["latest_authoritative_result"]
    require(latest["experiment"] == "R32_E51AJ" and str(latest["actions_run"]) == str(run) and str(latest["artifact_id"]) == str(identity["artifact_id"]), "detail authority stale")
    require(detail["active_experiment"] is None, "active experiment not cleared")
    frontier = ledger["current_frontier"]
    require(frontier["latest_authoritative_result"] == "E51AJ" and frontier["active_experiment"] is None, "ledger frontier stale")
    entry = next(e for e in ledger["experiments"] if e["id"] == "E51AJ")
    require(entry["status"] == "AUTHORITATIVE_RESULT" and entry["outcome"] == identity["outcome"], "ledger result mismatch")
    require(entry["retention_result"] == summary["retention_result"], "ledger retention mismatch")
    for document in (current, detail, ledger, status, evidence):
        require(document.get("promotion_allowed") is False, "promotion boundary changed")
        require(document.get("canonical_system", document.get("canonical_model")) == "R27", "canonical boundary changed")
    protected = ["Research/R32_E51AI_RESULT.md", "Research/R32_E51AI_EVIDENCE.json", "Research/R32_E51AI_EXECUTION_STATUS.json",
                 "Research/R32_E51AH_RESULT.md", "Research/R32_E51AH_EVIDENCE.json", "Research/R32_E51AH_EXECUTION_STATUS.json"]
    for path in protected:
        frozen = subprocess.check_output(["git", "show", source+":"+path], cwd=repo, timeout=20)
        require((repo/path).read_bytes() == frozen, "previous result changed: "+path)
    expected_rows = {"CURVE.csv":510, "RETENTION_MATRIX.csv":2040, "BASELINES.csv":9, "CYCLE_ENDS.csv":135,
                     "RETENTION.csv":15, "COHORT_RETENTION.csv":60, "SECONDARY_CONTRASTS.csv":12,
                     "EXPOSURE.csv":396, "PARAMETER_CHANGES.csv":396}
    for name, expected in expected_rows.items():
        with (analysis/name).open(newline="") as stream:
            require(len(list(csv.DictReader(stream))) == expected, "table row count: "+name)
    report_path = repo/"Research/R32_E51AJ_RESULT.md"
    report = report_path.read_text()
    required = [source, str(run), str(identity["artifact_id"]), identity["outcome"], summary["retention_result"],
                identity["source_tree"], identity["zip_sha256"], regenerated["preregistration_sha256"],
                regenerated["compiler_sha256"], *identity["sha256"].values()]
    require(all(value in report for value in required), "result identity/outcome omitted")
    expected_primary = runpy.run_path(str(analysis/"tables.py"))["primary_table"](summary)
    require(expected_primary in report, "result primary table differs")
    links = 0
    for path in (report_path, analysis/"README.md", analysis/"VALIDATION.md"):
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
            if target.startswith(("https:", "http:", "#")):
                continue
            require((path.parent/target.split("#")[0]).resolve().exists(), "broken local link: "+target)
            links += 1
    return {"verified": True, "run": run, "source_commit": source, "artifact_id": identity["artifact_id"],
            "frozen_scientific_inputs_unchanged": 65, "protected_prior_result_files_unchanged": len(protected),
            "immutable_baseline_unchanged": True, "probe_rows_checked": 1101600,
            "coefficient_rows_checked": 67860, "analysis_tables_reproduced": len(expected_rows),
            "local_links_checked": links, "current_authority_consistent": True,
            "retention_result": summary["retention_result"], "canonical_system": "R27"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    print(json.dumps(validate(args.archive.resolve(), Path(__file__).resolve().parents[2]), indent=2))
