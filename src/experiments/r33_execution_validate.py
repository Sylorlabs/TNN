"""Read-only R33 execution lifecycle checks, separate from frozen B000 authoring.

Verifies original registration and current run evidence as different objects.
Never rewrites the frozen validator, source, result or registry to obtain PASS.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

from r33_validate import (
    ROOT, RESEARCH, REQUIRED_FILES, ContractError, digest, load_json,
    parse_b000_output, require, validate_batch, validate_b000_source,
    validate_pins, validate_registries, validate_repository, validate_reviews,
    validate_schema_definition,
)

RUN = RESEARCH / "R33_B000_RUN_PRIMARY_V1"


def lifecycle(state: dict[str, Any], registry: dict[str, Any], consumed: dict[str, Any],
              execution: dict[str, Any], result: dict[str, Any] | None) -> None:
    require(state["canonical_system"] == registry["canonical_system"] == "R27", "canonical changed")
    require(state["canonical_development_step"] == 60423 and state["canonical_newborn_restarts"] == 0,
            "continuity changed")
    for obj in (state, registry):
        require(obj["promotion_allowed"] is False, "unqualified promotion")
    require(state["canonical_mutated"] is False and state["learner_authority_newly_granted"] is False,
            "unqualified mutation/authority")
    require(state["all_r33_research_complete"] is False, "audit mistaken for completed R33")
    require(state["scientifically_qualified_r33_milestone"] is None, "audit grants milestone")
    require(not registry["large_training_campaign_allowed"], "training gate unexpectedly open")
    require(consumed["unknown_identity_policy"] == "QUARANTINE_NOT_FRESH", "freshness policy relaxed")
    require(not consumed["new_scientific_allocations"] and not consumed["new_scientific_exposures"],
            "boundary audit allocated scientific evidence")
    require(consumed["legacy_guard"]["guarded_stage_range"] == [1, 142], "historical guard changed")
    ids = [x["id"] for x in registry["experiments"] + registry["proposed_batches"]]
    require(len(ids) == len(set(ids)), "duplicate experiment IDs")
    batch = next(x for x in registry["experiments"] if x["id"] == "R33-B000")
    fixture = next(x for x in consumed["diagnostic_fixtures"] if x["batch_id"] == "R33-B000")
    require(fixture["fresh_generalization_evidence"] is False, "known fixture called fresh")
    require(batch["status"] == execution["status"], "status disagreement")
    require(batch["primary_attempts"] == execution["primary_execution_attempts"], "attempt disagreement")
    require(batch["primary_attempts"] in (0, 1), "primary repeated")
    require(execution["native_fixture_exposures"] in (0, 1), "fixture repeated")
    require(execution["native_fixture_exposures"] == fixture["primary_executions"], "exposure disagreement")
    require(state["r33_native_experiments_executed"] >= execution["native_fixture_exposures"], "missing native count")
    require(state["r33_training_runs_executed"] == execution["training_runs"] == 0, "audit counted as training")
    for flag in ("training", "scientific_world_allocation", "canonical_mutation", "learner_authority_granted"):
        require(batch[flag] is False, "audit scope expanded: " + flag)
    for flag in ("canonical_mutated", "learner_authority_granted", "sensory_qualification", "promotion"):
        require(execution[flag] is False, "execution claims unsupported qualification")
    require(state["active_experiment"] == registry["active_experiment"], "active state disagreement")
    if batch["status"] == "PREREGISTERED_NOT_EXECUTED":
        require(batch["primary_attempts"] == execution["native_fixture_exposures"] == 0,
                "unexecuted attempt count")
        require(result is None and execution["observed_witness_results"] is None, "invented result")
    elif batch["status"] == "RUNNING":
        require(state["active_experiment"] == "R33-B000" and batch["primary_attempts"] == 1,
                "unadmitted active audit")
        require(result is None, "terminal result presented as running")
    else:
        require(batch["status"] in ("COMPLETED", "FAILED_REQUIRES_ANALYSIS"), "unknown lifecycle state")
        require(state["active_experiment"] != "R33-B000" and batch["primary_attempts"] == 1,
                "terminal audit still active or unadmitted")
        require(result is not None, "terminal audit missing result")
        require(result["fixture_exposures"] == execution["native_fixture_exposures"], "result exposure disagreement")
        for flag in ("canonical_mutated", "learner_authority_granted", "sensory_qualification", "promotion"):
            require(result[flag] is False, "result claims unsupported qualification")
        require(result.get("parsed_output") == execution["observed_witness_results"], "parsed result mismatch")
        if batch["status"] == "COMPLETED":
            require(result["status"] == "EXPECTED_WITNESSES_MATCHED" and not result["errors"], "false audit success")
            require(execution["native_fixture_exposures"] == 1, "success without execution")
            runtime = result["runtime"]
            require(runtime["native_process_started"] and runtime["exit_code"] == 0
                    and runtime["termination_reason"] is None, "successful result has failed runtime")
            for key, cap in (("wall_seconds", 30), ("cpu_seconds", 20), ("peak_rss_bytes", 268435456),
                             ("stdout_bytes", 65536)):
                require(isinstance(runtime[key], (int, float)) and not isinstance(runtime[key], bool)
                        and 0 <= runtime[key] <= cap, "missing or excessive resource: " + key)
            require(runtime["stderr_bytes"] == 0, "successful audit has stderr")
            require(result["parsed_output"]["status"] == "EXPECTED_WITNESSES_MATCHED"
                    and not result["parsed_output"]["mismatched_keys"], "success conceals observation mismatch")


def verify() -> dict[str, Any]:
    if not RUN.exists():
        return {"phase": "PRE_EXECUTION", "frozen_authoring": validate_repository(), "status": "PASS"}
    for name in REQUIRED_FILES:
        require((RESEARCH / name).is_file(), "missing hierarchy: " + name)
    objects = {p.name: load_json(p) for p in sorted(RESEARCH.glob("R33*.json"))}
    snapshot = load_json(RUN / "REGISTRATION_SNAPSHOT.json")
    baseline_state = snapshot["R33_CURRENT_STATE.json"]
    baseline_registry = snapshot["R33_EXPERIMENT_REGISTRY.json"]
    baseline_consumed = snapshot["R33_CONSUMED_EVIDENCE_REGISTRY.json"]
    validate_registries(baseline_state, baseline_registry, baseline_consumed)
    original_batch = next(x for x in baseline_registry["experiments"] if x["id"] == "R33-B000")
    validate_batch(original_batch, objects["R33_INDEPENDENT_REVIEWS.json"])
    validate_reviews(objects["R33_INDEPENDENT_REVIEWS.json"])
    validate_pins(objects["R33_AUDIT_SCOPE.json"]["pinned_files"])
    validate_pins(objects["R33_B000_LAUNCH_FREEZE.json"]["pins"])
    validate_b000_source((RESEARCH / "R33_B000_SOURCE.zag").read_text(),
                         (RESEARCH / "tnn_r32_epistemic_chunking.zag").read_text())
    validate_schema_definition(objects["R33_TELEMETRY_SCHEMA.json"], objects["R33_TELEMETRY_SCHEMA.json"])
    state, registry, consumed, execution = (objects[name] for name in (
        "R33_CURRENT_STATE.json", "R33_EXPERIMENT_REGISTRY.json", "R33_CONSUMED_EVIDENCE_REGISTRY.json",
        "R33_B000_EXECUTION_STATUS.json"))
    result = load_json(RUN / "RESULT.json") if (RUN / "RESULT.json").exists() else None
    lifecycle(state, registry, consumed, execution, result)
    current_batch = next(x for x in registry["experiments"] if x["id"] == "R33-B000")
    require(current_batch["source_pins"] == original_batch["source_pins"], "preregistration pin history rewritten")
    require(consumed["records"] == baseline_consumed["records"], "historical evidence rewritten")
    require(consumed["legacy_guard"] == baseline_consumed["legacy_guard"], "historical guard rewritten")
    reservation = load_json(RUN / "RESERVATION.json")
    require(digest(RUN / "REGISTRATION_SNAPSHOT.json") == reservation["registration_snapshot_sha256"],
            "original registration snapshot drift")
    require(digest(RESEARCH / "R33_B000_LAUNCH_FREEZE.json") == reservation["freeze_sha256"], "launch freeze drift")
    artifact_count = 0
    if result is not None:
        manifest = load_json(RUN / "MANIFEST.json")
        pins = manifest["files"]
        require(len(pins) == len({x["path"] for x in pins}), "duplicate artifact pin")
        for pin in pins:
            path = ROOT / pin["path"]
            require(path.resolve().parent == RUN.resolve(), "artifact outside run directory")
            require(path.stat().st_size == pin["bytes"], "artifact size drift")
        validate_pins(pins)
        artifact_count = len(pins)
        require({p.name for p in RUN.iterdir() if p.is_file()} ==
                {Path(x["path"]).name for x in pins} | {"MANIFEST.json"}, "unmanifested or missing artifact")
        if result.get("runtime") is not None:
            require(digest(RUN / "b000") == result["binary_sha256"], "wrong executed binary")
            for name in ("stdout", "stderr"):
                require(digest(RUN / ("native." + name)) == result["runtime"][name + "_sha256"], "runtime log drift")
            if result.get("parsed_output") is not None:
                parsed = parse_b000_output((RUN / "native.stdout").read_text(), objects["R33_B000_CONFIG.json"])
                require(parsed == result["parsed_output"], "parser reproduction differs")
    links = 0
    for path in sorted(RESEARCH.glob("R33*.md")):
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
            target = target.split("#", 1)[0].strip("<>")
            if target and not re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                require((path.parent / target).is_file(), "broken link: " + target)
                links += 1
    return {"status": "PASS", "phase": current_batch["status"], "hierarchy_files": len(REQUIRED_FILES),
            "local_markdown_links": links, "original_preregistration_pins": len(original_batch["source_pins"]),
            "run_artifacts_checked": artifact_count, "native_fixture_exposures": execution["native_fixture_exposures"],
            "training_runs": 0, "canonical": "R27", "all_r33_research_complete": False,
            "validation_scope": "ORIGINAL_REGISTRATION_PLUS_CURRENT_B000_EXECUTION_NOT_FULL_R33_QUALIFICATION"}


if __name__ == "__main__":
    try:
        print(json.dumps(verify(), indent=2))
    except (ContractError, OSError, ValueError, KeyError, StopIteration) as error:
        print("R33_EXECUTION_VALIDATION_FAIL: " + str(error), file=sys.stderr)
        raise SystemExit(1)
