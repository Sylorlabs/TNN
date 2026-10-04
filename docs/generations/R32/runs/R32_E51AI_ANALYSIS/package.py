"""Package verified E51AI evidence and cross-check independent retention arithmetic.

Usage: python3 -B Research/R32_E51AI_ANALYSIS/package.py ARCHIVE_DIRECTORY
This only reads existing experiment results; it does not run or fit a learner.
"""
import argparse
import hashlib
import json
from pathlib import Path
import runpy


def require(condition, message):
    if not condition:
        raise ValueError(message)


def independent_retention(archive):
    """Recompute using episode-key sets, independently of derive.retention()."""
    import csv
    hits = {}
    updates = {arm: 0 for arm in range(4)}
    with (archive / "extracted/RAW.log").open() as stream:
        for row in csv.reader(stream):
            if row and row[0] == "e51ai_episode":
                cp, snapshot, arm, cohort, ep, hit, *_ = map(int, row[1:])
                if snapshot == 0:
                    hits.setdefault((cp, arm, cohort), set())
                    if hit:
                        hits[(cp, arm, cohort)].add(ep)
            elif row and row[0] == "e51ai_fit":
                _, arm, _, accepted, *_ = map(int, row[1:])
                updates[arm] += accepted
    require(len(hits) == 33 * 4 * 4, "incomplete independent checkpoint set")
    results = {}
    shared = {}
    for arm in range(4):
        total = dict(anchor_successes=0, ever_lost=0, never_lost=0,
                     regained_at_final=0, missing_at_final=0)
        for cohort in range(4):
            anchor = hits[(cohort + 1, arm, cohort)]
            lost = set().union(*(anchor - hits[(cp, arm, cohort)] for cp in range(cohort + 2, 33)))
            final = hits[(32, arm, cohort)]
            values = [len(anchor), len(lost), len(anchor - lost), len(lost & final), len(anchor - final)]
            for key, value in zip(total, values):
                total[key] += value
        results[str(arm)] = total
    for arm in (1, 3):
        total = dict(anchor_successes=0, ever_lost=0, never_lost=0,
                     regained_at_final=0, missing_at_final=0)
        for cohort in range(4):
            anchor = hits[(cohort + 1, 1, cohort)] & hits[(cohort + 1, 3, cohort)]
            lost = set().union(*(anchor - hits[(cp, arm, cohort)] for cp in range(cohort + 2, 33)))
            final = hits[(32, arm, cohort)]
            values = [len(anchor), len(lost), len(anchor - lost), len(lost & final), len(anchor - final)]
            for key, value in zip(total, values):
                total[key] += value
        shared[str(arm)] = total
    return results, shared, updates


def package(archive, repo):
    analysis = repo / "Research/R32_E51AI_ANALYSIS"
    identity = json.loads((archive / "IDENTITY_CHECK.json").read_text())
    scientific = json.loads((archive / "LOCAL_EVIDENCE_CHECK.json").read_text())
    summary = json.loads((analysis / "SUMMARY.json").read_text())
    require(identity["verified"] is True and scientific["verified"] is True, "unverified experiment")
    regenerated, files = runpy.run_path(str(analysis / "derive.py"))["derive"](archive)
    require(summary == regenerated, "stored analysis summary changed")
    for name, data in files.items():
        require((analysis / name).read_bytes() == data, f"stored analysis differs: {name}")
    independent, shared, updates = independent_retention(archive)
    for arm, total in independent.items():
        for key, value in total.items():
            require(summary["arms"][arm]["first_encounter_retention"][key] == value,
                    f"independent retention mismatch: arm {arm}, {key}")
        require(summary["arms"][arm]["accepted_coordinate_updates"] == updates[int(arm)], "update count mismatch")
        require(summary["arms"][arm]["training_record_presentations"] == 34560, "wrong exposure")
    require(shared == summary["shared_first_encounter_replay_contrast"], "shared-anchor mismatch")
    run = json.loads((archive / "RUN.json").read_text())
    jobs = json.loads((archive / "JOBS.json").read_text())
    artifacts = json.loads((archive / "ARTIFACTS.json").read_text())
    artifact = next(item for item in artifacts["artifacts"] if item["id"] == identity["artifact_id"])
    job = next(item for item in jobs["jobs"] if item["id"] == identity["job"])
    file_names = sorted(files) + ["derive.py", "verify_archive.py", "package.py", "test_derive.py", "test_archive.py"]
    return {
        "schema_version": 1, "experiment": "R32_E51AI",
        "state": "COMPLETED_VERIFIED_EXPLORATORY_DIAGNOSTIC",
        "lane": "EXPLORATORY_LONGITUDINAL_DIAGNOSTIC",
        "scientific_outcome": scientific["outcome"],
        "interpretation": "Completed 32-block measurement; frozen history-preserving signal absent; replay retention tradeoff observed.",
        "canonical_system": "R27", "promotion_allowed": False,
        "run_metadata": {key: run[key] for key in ("id", "workflow_id", "run_attempt", "head_sha", "status", "conclusion", "created_at", "updated_at")},
        "job_metadata": {key: job[key] for key in ("id", "status", "conclusion", "started_at", "completed_at")},
        "source_tree": run["head_commit"]["tree_id"],
        "artifact_metadata": {key: artifact[key] for key in ("id", "name", "size_in_bytes", "digest", "created_at", "expires_at")},
        "local_archive_directory": str(archive.relative_to(repo)),
        "archive_identity_check": identity,
        "frozen_scientific_verification": scientific,
        "descriptive_analysis": summary,
        "independent_set_based_retention_check": {"passed": True, "arms": independent, "shared_anchors": shared},
        "exposure": {"blocks": 32, "cycles": 8, "training_stages": [111,112,113,114],
                     "development_probe_stages": [115,116,117,118], "unique_training_trajectories": 2160,
                     "unique_probe_trajectories": 2160, "training_record_presentations_per_arm": 34560,
                     "native_probe_episode_rows": 293760, "checkpoint_coefficients": 17160,
                     "validation_executed": 0, "confirmation_executed": 0},
        "compiler_sha256": "498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef",
        "preregistration_sha256": "cf3ab1ae1fef2acbac855a462c6379f7fb7efb682ec14934ac7f3be91bd8d469",
        "analysis_file_sha256": {name: hashlib.sha256((analysis / name).read_bytes()).hexdigest() for name in file_names},
        "metadata_file_sha256": {name: hashlib.sha256((archive / name).read_bytes()).hexdigest()
                                  for name in ("RUN.json", "JOBS.json", "ARTIFACTS.json")},
        "review_boundary": "Main-task source and evidence audit completed. No verdict from the separately launched ChatGPT Web reviewer was retrieved during this continuation; no approval is inferred.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = package(args.archive.resolve(), repo)
    output = repo / "Research/R32_E51AI_EVIDENCE.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"file": str(output), "independent_retention_passed": True,
                      "sha256": hashlib.sha256(output.read_bytes()).hexdigest()}, indent=2))
