"""Package verified E51AJ identity, analysis and reproduction hashes; no fitting.

Usage: python3 -B Research/R32_E51AJ_ANALYSIS/package.py ARCHIVE_DIRECTORY
All derived tables must already exist and match independent regeneration.
"""
from pathlib import Path
import argparse
import hashlib
import json
import runpy


def require(condition, message):
    if not condition:
        raise ValueError(message)


def package(archive, repo):
    analysis = repo/"Research/R32_E51AJ_ANALYSIS"
    routines = runpy.run_path(str(analysis/"derive.py"))
    read_json = routines["read_json"]
    identity = read_json(archive/"IDENTITY_CHECK.json")
    scientific = read_json(archive/"LOCAL_EVIDENCE_CHECK.json")
    summary, generated = routines["derive"](archive)
    generated["TABLES.md"] = runpy.run_path(str(analysis/"tables.py"))["tables"](summary)
    for name, content in generated.items():
        require((analysis/name).read_bytes() == content, "stored table differs: "+name)
    run = read_json(archive/"RUN.json")
    jobs = read_json(archive/"JOBS.json")["jobs"]
    artifacts = read_json(archive/"ARTIFACTS.json")["artifacts"]
    job = next(item for item in jobs if item["id"] == identity["job"])
    artifact = next(item for item in artifacts if item["id"] == identity["artifact_id"])
    code = ("derive.py", "package.py", "tables.py", "verify_archive.py", "validate_delivery.py",
            "test_derive.py", "test_archive.py", "test_tables.py")
    file_names = sorted(generated) + list(code) + ["PREEXECUTION_REVIEW.md", "POSTEXECUTION_REVIEW.md"]
    return {
        "schema_version": 1, "experiment": "R32_E51AJ",
        "state": "COMPLETED_VERIFIED_EXPLORATORY_DIAGNOSTIC",
        "lane": "EXPLORATORY_LONGITUDINAL_DIAGNOSTIC",
        "scientific_outcome": scientific["outcome"],
        "retention_result": scientific["retention_result"],
        "no_final_behavioral_tradeoff": scientific["no_final_behavioral_tradeoff"],
        "canonical_system": "R27", "promotion_allowed": False,
        "run_metadata": {k:run[k] for k in ("id","workflow_id","run_attempt","head_sha","status","conclusion","created_at","updated_at")},
        "job_metadata": {k:job[k] for k in ("id","status","conclusion","started_at","completed_at")},
        "artifact_metadata": {k:artifact[k] for k in ("id","name","size_in_bytes","digest","created_at","expires_at")},
        "source_tree": run["head_commit"]["tree_id"],
        "source_pin": "Research/R32_E51AJ_SOURCE_PIN.json",
        "preregistration_sha256": hashlib.sha256((repo/"Research/R32_E51AJ_REPLAY_ORDER_DOSE_PREREG.md").read_bytes()).hexdigest(),
        "compiler_sha256": "498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef",
        "local_archive_directory": str(archive.relative_to(repo)),
        "archive_identity_check": identity,
        "frozen_scientific_verifier": {
            "path": ".github/scripts/e51aj_verify.py", "source_commit": routines["SOURCE"],
            "archived_report": "extracted/EVIDENCE_CHECK.json",
            "independent_report": "LOCAL_EVIDENCE_CHECK.json",
            "reports_match_exactly": True,
            "report_sha256": hashlib.sha256((archive/"extracted/EVIDENCE_CHECK.json").read_bytes()).hexdigest(),
            "probe_episode_rows_verified": scientific["probe_episode_rows_verified"],
            "coefficient_rows_verified": scientific["coefficient_rows_verified"],
            "source_inputs_verified": scientific["source_inputs_verified"],
        },
        "independent_descriptive_analysis": summary,
        "exposure": {
            "replicas": 3, "training_stages": [[119,120,121,122],[127,128,129,130],[135,136,137,138]],
            "development_probe_stages": [[123,124,125,126],[131,132,133,134],[139,140,141,142]],
            "unique_training_trajectories": 6480, "unique_probe_trajectories": 6480,
            "common_preparation_blocks_per_replica": 4, "continuing_blocks_per_replica": 32,
            "arms_per_replica": 5, "trainable_arms_per_replica": 4,
            "lineage_presentations_per_trained_arm_per_replica": 38880,
            "lineage_presentations_per_static_arm_per_replica": 4320,
            "physical_training_record_presentations": summary["physical_record_presentations"],
            "native_probe_episode_rows": 1101600, "coefficient_rows": 67860,
            "validation_executed": 0, "confirmation_executed": 0,
        },
        "analysis_file_sha256": {name:hashlib.sha256((analysis/name).read_bytes()).hexdigest() for name in file_names},
        "metadata_file_sha256": {name:hashlib.sha256((archive/name).read_bytes()).hexdigest() for name in ("RUN.json","JOBS.json","ARTIFACTS.json")},
        "review_boundary": "Pre-execution design review and a separate post-execution interpretation audit completed on ChatGPT Web. Neither substitutes for compiler/archive verification. Main task independently checked archive identity, frozen scientific report and raw-row bitset arithmetic. The post-execution counterfactual suggestion was not executed.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = package(args.archive.resolve(), repo)
    output = repo/"Research/R32_E51AJ_EVIDENCE.json"
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"file":str(output),"retention_result":result["retention_result"],
                      "independent_analysis_passed":True,
                      "sha256":hashlib.sha256(output.read_bytes()).hexdigest()},indent=2))
