"""Read-only R33 documentation/telemetry checks; never executes learner code.

Python 3.10+, standard library only. The schema checker deliberately implements
only the explicitly allowlisted JSON Schema keywords used by this project. It
rejects unknown keywords rather than claiming general Draft 2020-12 support.
This is an authoring aid, not the protected native authority supervisor.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "Research"
KEYWORDS = {
    "$schema", "$id", "$defs", "$ref", "title", "description", "oneOf",
    "type", "const", "enum", "required", "properties", "additionalProperties",
    "items", "minItems", "uniqueItems", "minLength", "pattern", "minimum",
    "exclusiveMinimum",
}
REQUIRED_FILES = (
    "R33_PROGRAM_CHARTER.md", "R33_MASTER_PLAN.md", "R33_ARCHITECTURE_CONTRACT.md",
    "R33_TRAINER_INTERFACE_AND_TELEMETRY.md", "R33_WHITE_BOX_OBSERVABILITY_CONTRACT.md",
    "R33_AUTHORITY_MILESTONE_LADDER.md", "R33_SENSOR_QUALIFICATION_PLAN.md",
    "R33_BIRTH_SUBSTRATE_HARDCODING_PLAN.md", "R33_PARAMETER_SCALING_PLAN.md",
    "R33_TRAINING_TECHNIQUE_TOURNAMENT.md", "R33_HAND_HOLDING_WITHDRAWAL_PLAN.md",
    "R33_MEMORY_AUTONOMY_PLAN.md", "R33_STRUCTURAL_PLASTICITY_PLAN.md",
    "R33_EFFICIENCY_AND_SPARSE_COMPUTE_PLAN.md", "R33_SELF_MODEL_CONSCIOUSNESS_RESEARCH_PLAN.md",
    "R33_SCENARIO_BATTERY.md", "R33_ARCHITECTURE_COMPARISON_BENCHMARK.md",
    "R33_EXPERIMENT_REGISTRY.json", "R33_CONSUMED_EVIDENCE_REGISTRY.json",
    "R33_EXECUTION_JOURNAL.md", "R33_CURRENT_STATE.json", "R33_HANDOFF.md",
)
COPIED_HELPERS = (
    "abs_i32", "trace_emit", "core_relational_signature8", "acoustic_window_distance",
    "lru_evict_candidate", "r31_chunk_match", "r31_segment", "r31_reconstruct",
)
B000_DRIVERS = (
    "b000_metric", "b000_vector", "b000_visual", "b000_audio", "b000_trace",
    "b000_lru", "b000_chunk", "main",
)


class ContractError(ValueError):
    """An invalid or unsupported contract, identity or telemetry record."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def load_json(path: Path) -> Any:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            require(key not in out, f"duplicate JSON key: {key} in {path}")
            out[key] = value
        return out

    def reject_constant(value: str) -> None:
        raise ContractError(f"non-finite JSON constant {value} in {path}")

    value = json.loads(path.read_text(), object_pairs_hook=pairs, parse_constant=reject_constant)
    check_finite(value)
    return value


def check_finite(value: Any) -> None:
    """Also reject exponent overflow and non-finite values in opaque payloads."""
    if isinstance(value, float):
        require(math.isfinite(value), "non-finite numeric value")
    elif isinstance(value, dict):
        for child in value.values(): check_finite(child)
    elif isinstance(value, list):
        for child in value: check_finite(child)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def schema_check(value: Any, schema: dict[str, Any], root: dict[str, Any], at: str = "$") -> None:
    """Validate the project's supported JSON Schema subset, fail-closed."""
    require(not (set(schema) - KEYWORDS), f"{at}: unsupported schema keywords {set(schema) - KEYWORDS}")
    if "$ref" in schema:
        ref = schema["$ref"]
        require(ref.startswith("#/$defs/"), f"{at}: only local definition references supported")
        target: Any = root
        for part in ref[2:].split("/"):
            require(isinstance(target, dict) and part in target, f"{at}: unresolved reference {ref}")
            target = target[part]
        schema_check(value, target, root, at)
    if "oneOf" in schema:
        matches = 0
        for alternative in schema["oneOf"]:
            try:
                schema_check(value, alternative, root, at)
                matches += 1
            except ContractError:
                pass
        require(matches == 1, f"{at}: expected exactly one schema branch, got {matches}")
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        checks = {
            "object": isinstance(value, dict), "array": isinstance(value, list),
            "string": isinstance(value, str), "boolean": isinstance(value, bool),
            "integer": isinstance(value, int) and not isinstance(value, bool),
            "number": isinstance(value, (int, float)) and not isinstance(value, bool)
            and (not isinstance(value, float) or math.isfinite(value)),
            "null": value is None,
        }
        require(all(t in checks for t in types), f"{at}: unsupported type")
        require(any(checks[t] for t in types), f"{at}: wrong type, expected {types}")
    if "const" in schema:
        require(type(value) is type(schema["const"]) and value == schema["const"], f"{at}: wrong constant")
    if "enum" in schema:
        require(any(type(value) is type(x) and value == x for x in schema["enum"]), f"{at}: invalid enum")
    if isinstance(value, dict):
        require(set(schema.get("required", [])) <= set(value), f"{at}: missing required fields")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            require(set(value) <= set(properties), f"{at}: unexpected fields {set(value) - set(properties)}")
        for key, child in value.items():
            if key in properties:
                schema_check(child, properties[key], root, f"{at}.{key}")
    if isinstance(value, list):
        require(len(value) >= schema.get("minItems", 0), f"{at}: too few items")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(x, sort_keys=True, allow_nan=False) for x in value]
            require(len(set(encoded)) == len(encoded), f"{at}: duplicate items")
        if "items" in schema:
            for index, child in enumerate(value):
                schema_check(child, schema["items"], root, f"{at}[{index}]")
    if isinstance(value, str):
        require(len(value) >= schema.get("minLength", 0), f"{at}: string too short")
        if "pattern" in schema:
            require(re.search(schema["pattern"], value) is not None, f"{at}: pattern mismatch")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema:
            require(value >= schema["minimum"], f"{at}: below minimum")
        if "exclusiveMinimum" in schema:
            require(value > schema["exclusiveMinimum"], f"{at}: below exclusive minimum")


def validate_schema_definition(schema: dict[str, Any], root: dict[str, Any]) -> None:
    """Check every declared branch, including unused ones; not a general metaschema."""
    require(isinstance(schema, dict), "schema must be an object")
    require(not (set(schema) - KEYWORDS), "unsupported schema definition keyword")
    if "$ref" in schema:
        ref = schema["$ref"]
        require(isinstance(ref, str) and ref.startswith("#/$defs/"), "nonlocal schema reference")
        require(ref[8:] in root.get("$defs", {}), "unresolved schema definition")
    if "additionalProperties" in schema:
        require(isinstance(schema["additionalProperties"], bool), "schema-valued additionalProperties unsupported")
    for key in ("$defs", "properties"):
        for child in schema.get(key, {}).values():
            validate_schema_definition(child, root)
    for child in schema.get("oneOf", []):
        validate_schema_definition(child, root)
    if "items" in schema:
        validate_schema_definition(schema["items"], root)


def validate_record(record: dict[str, Any], schema: dict[str, Any]) -> None:
    validate_schema_definition(schema, schema)
    check_finite(record)
    schema_check(record, schema, schema)
    if record["record_type"] == "COMPETENCY_SNAPSHOT":
        if record["qualification_status"] == "PASSED_BOUNDED_CONTRACT":
            require(bool(record["source_event_ids"]), "qualified snapshot has no evidence")
            for key in ("fresh_performance", "delayed_retention", "changed_example_transfer", "help_dependence"):
                require(record["metrics"][key]["status"] in ("MEASURED", "DERIVED"), f"unmeasured qualification criterion: {key}")
        return
    actor = record["actor"]
    authority = record["authority"]
    if actor["kind"] == "SOFTWARE_TEACHING_AID":
        require(bool(actor.get("delegating_human_actor_id")), "teaching aid lacks human delegation")
    if record["event_kind"] == "GRANT":
        require(actor["kind"] in ("HUMAN", "HUMAN_GROUP", "PROTECTED_SUPERVISOR"), "learner/aid cannot grant authority")
    if authority["effective_milestone"] is not None:
        require(authority["grant_status"] == "AUTHENTICATED" and bool(authority["grant_id"]), "effective authority lacks authenticated grant")
    if record["event_kind"] == "ASSESSMENT":
        require(record["visibility"] != "LEARNER_ADMITTED", "assessment leaks into learner-admitted stream")
    coverage = record["coverage"]
    if coverage["status"] == "COMPLETE_WITHIN_DECLARED_SCOPE":
        require(not coverage["missing_fields"] and coverage["dropped_events"] == 0, "complete coverage hides a gap")
    help_record = record["assistance"]
    if help_record["input_event_ids"] or help_record["human_interventions"] or help_record["software_aid_interventions"]:
        require(help_record["assisted"], "help hidden in an unassisted event")
    if record["event_kind"] == "UPDATE":
        require(bool(record["mutations"]), "update has no state-delta attribution")
    require(record["event_id"] not in record["parent_event_ids"], "event is its own parent")


def extract_function(text: str, name: str) -> str:
    """Bound an allowlisted Zag function; skip quoted text/comments when counting braces."""
    matches = list(re.finditer(r"(?m)^fn " + re.escape(name) + r"\(", text))
    require(len(matches) == 1, f"nonunique or missing function: {name}")
    start = matches[0].start()
    depth = 0
    opened = False
    for token in re.finditer(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|[{}]', text[start:], re.S):
        part = token.group()
        if part == "{":
            depth += 1
            opened = True
        elif part == "}":
            depth -= 1
            if opened and depth == 0:
                return text[start:start + token.end()]
    raise ContractError(f"unclosed function: {name}")


def validate_b000_source(source: str, original: str) -> None:
    for name in COPIED_HELPERS:
        require(extract_function(source, name) == extract_function(original, name), f"copied helper differs: {name}")
    for name, value in (("TRACE_CAP", 8192), ("VIEW_DIM", 8), ("R31_CHUNK_LEN_MAX", 16)):
        declaration = f"const {name}:i32={value};"
        require(source.count(declaration) == 1 and original.count(declaration) == 1, f"changed constant: {name}")
    stripped = re.sub(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"', " ", source, flags=re.S)
    require("@import" not in stripped, "audit must not import a historical entrypoint")
    names = re.findall(r"\bfn\s+(\w+)\s*\(", stripped)
    require(len(names) == len(set(names)), "duplicate audit function")
    allowed = set(COPIED_HELPERS + B000_DRIVERS)
    require(set(names) == allowed, "unexpected or missing audit function")
    calls = set(re.findall(r"\b(\w+)\s*\(", stripped))
    require(calls <= allowed | {"if", "while", "zalloc_i", "zfree", "_zag_print", "_zag_println", "_zag_i64_to_str"}, "audit call outside allowlist")


def parse_b000_output(text: str, config: dict[str, Any]) -> dict[str, Any]:
    """Parse native output only. Never runs or simulates the native helper code."""
    require(len(text.encode()) <= config["resources"]["stdout_bytes_ceiling"], "audit output cap exceeded")
    metrics: dict[str, int] = {}
    vectors: dict[str, dict[int, int]] = {}
    for row in csv.reader(io.StringIO(text)):
        require(bool(row) and row[0] in ("M", "V"), "unknown/empty audit record")
        require(len(row) == (3 if row[0] == "M" else 4), "malformed audit record")
        key = row[1]
        for number in row[2:]:
            require(re.fullmatch(r"-?(0|[1-9][0-9]*)", number) is not None, "noninteger audit field")
            require(-(2**31) <= int(number) < 2**31, "audit integer out of i32 range")
        if row[0] == "M":
            require(key in config["expected_metrics"] and key not in metrics, "unknown/duplicate audit metric")
            metrics[key] = int(row[2])
        else:
            require(key in config["expected_vectors"], "unknown audit vector")
            index, value = int(row[2]), int(row[3])
            require(0 <= index < len(config["expected_vectors"][key]), "audit vector index out of bounds")
            values = vectors.setdefault(key, {})
            require(index not in values, "duplicate audit vector index")
            values[index] = value
    require(set(metrics) == set(config["expected_metrics"]), "missing audit metric")
    require(set(vectors) == set(config["expected_vectors"]), "missing audit vector")
    ordered: dict[str, list[int]] = {}
    for key, expected in config["expected_vectors"].items():
        require(set(vectors[key]) == set(range(len(expected))), f"incomplete audit vector: {key}")
        ordered[key] = [vectors[key][i] for i in range(len(expected))]
    mismatches = [key for key, value in metrics.items() if value != config["expected_metrics"][key]]
    mismatches += [key for key, value in ordered.items() if value != config["expected_vectors"][key]]
    require(metrics["audit.completed"] == 1, "audit completion marker missing")
    return {"status": "EXPECTED_WITNESSES_MATCHED" if not mismatches else "OBSERVATION_MISMATCH_REQUIRES_ANALYSIS",
            "mismatched_keys": sorted(mismatches), "metrics": metrics, "vectors": ordered,
            "sensory_or_authority_contract_satisfied": False}


def validate_reviews(document: dict[str, Any]) -> None:
    require(document["status"] == "COMPLETED_AND_INTEGRATED", "reviews not integrated")
    reviews = document["reviews"]
    completed = [r for r in reviews if r["status"] == "COMPLETED"]
    require({r["role"] for r in completed} >= {"architecture", "training", "safety"}, "independent reviews incomplete")
    require(len({r["agent_id"] for r in completed}) == len(completed), "reviewer identities not independent")
    for review in completed:
        for key in ("strongest_criticism", "missing_experiment", "confound", "falsification_test", "recommended_change", "what_not_to_claim", "disposition", "scope", "integration_paths"):
            require(bool(review.get(key)), f"review lacks {key}")


def validate_pins(pins: list[dict[str, str]], root: Path = ROOT) -> None:
    names = [pin["path"] for pin in pins]
    require(len(set(names)) == len(names), "duplicate preregistration pin")
    for pin in pins:
        path = (root / pin["path"]).resolve()
        require(path.is_relative_to(root.resolve()), "preregistration path escapes repository")
        require(re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]) is not None, "invalid pin digest")
        require(digest(path) == pin["sha256"], f"preregistered file changed: {pin['path']}")


def validate_batch(experiment: dict[str, Any], reviews: dict[str, Any], root: Path = ROOT) -> None:
    validate_reviews(reviews)
    require(experiment["id"] == "R33-B000" and experiment["kind"] == "ISOLATED_NATIVE_BOUNDARY_AUDIT", "unexpected first batch")
    require(experiment["status"] == "PREREGISTERED_NOT_EXECUTED", "unexpected execution status")
    for flag in ("training", "canonical_mutation", "scientific_world_allocation", "learner_authority_granted"):
        require(experiment[flag] is False, f"audit scope expanded: {flag}")
    pins = experiment["source_pins"]
    names = [pin["path"] for pin in pins]
    require(len(set(names)) == len(names), "duplicate preregistration pin")
    required = {
        "Research/R33_B000_SOURCE.zag", "Research/R33_B000_CONFIG.json",
        "Research/R33_B000_PREREGISTRATION.md", "Research/R33_B000_SOURCE_MAP.json",
        "Research/R33_INDEPENDENT_REVIEWS.json", "Research/R33_TELEMETRY_SCHEMA.json",
        "Research/R33_AUTHORITY_MILESTONE_LADDER.md", "Research/r33_validate.py",
        "Research/toolchain/znc_macos_arm64_7cacbfc0",
    }
    require(required <= set(names), "incomplete preregistration freeze")
    validate_pins(pins, root)
    require(set(experiment["artifact_paths"]) >= {
        "preregistration", "source_config_identity", "changed_variable_ledger", "trainer_input_ledger",
        "hardcoding_ledger", "authority_level_and_grant", "evidence_identity", "execution_status",
        "full_result_including_negatives", "analysis_reproduction", "resource_report",
        "consumed_evidence_update", "architecture_diff", "next_step_rationale", "handoff_current_state_update",
    }, "missing experiment artifact mapping")
    for path in experiment["artifact_paths"].values():
        require((root / path.split("#", 1)[0]).is_file(), f"missing run artifact or pending-status record: {path}")


def validate_registries(state: dict[str, Any], registry: dict[str, Any], consumed: dict[str, Any]) -> None:
    require(state["canonical_system"] == registry["canonical_system"] == "R27", "canonical authority changed")
    require(state["canonical_development_step"] == 60423 and state["canonical_newborn_restarts"] == 0, "canonical continuity changed")
    require(state["promotion_allowed"] is False and registry["promotion_allowed"] is False, "unqualified promotion")
    require(state["active_experiment"] == registry["active_experiment"], "active experiment disagreement")
    require(state["canonical_mutated"] is False, "initialization mutated canonical state")
    require(registry["large_training_campaign_allowed"] is False, "training gate unexpectedly open")
    require(consumed["unknown_identity_policy"] == "QUARANTINE_NOT_FRESH", "freshness must fail closed")
    records = consumed["records"]
    require(len({r["id"] for r in records}) == len(records), "duplicate evidence ID")
    experiments = registry["experiments"]
    proposed = registry["proposed_batches"]
    ids = [x["id"] for x in experiments + proposed]
    require(len(set(ids)) == len(ids), "duplicate registered/proposed experiment ID")
    require(not consumed["new_scientific_exposures"], "initialization unexpectedly consumed scientific evidence")
    fixtures = consumed.get("diagnostic_fixtures", [])
    require(len({x["id"] for x in fixtures}) == len(fixtures), "duplicate diagnostic fixture identity")
    for fixture in fixtures:
        require(fixture["primary_executions"] == 0 and fixture["fresh_generalization_evidence"] is False, "fixture exposure or freshness misreported")
    lo, hi = consumed["legacy_guard"]["guarded_stage_range"]
    for allocation in consumed["new_scientific_allocations"]:
        require(not any(lo <= stage <= hi for stage in allocation.get("stages", [])), "allocation overlaps guarded historical stages")
        require(all(key in allocation for key in consumed["freshness_required_identity_fields"]), "allocation lacks full freshness identity")
    aj = next(r for r in records if r["id"] == "R32-E51AJ")
    require(set(aj["training_stages"]).isdisjoint(aj["probe_stages"]), "AJ train/probe overlap")
    require(set(aj["training_stages"] + aj["probe_stages"]) == set(range(119, 143)), "AJ consumed identity incomplete")
    require(aj["unique_training_episodes"] == aj["unique_probe_episodes"] == 6480, "AJ exposure count mismatch")


def validate_repository() -> dict[str, Any]:
    for name in REQUIRED_FILES:
        require((RESEARCH / name).is_file(), f"missing R33 hierarchy file: {name}")
    paths = sorted(RESEARCH.glob("R33*.json"))
    objects = {p.name: load_json(p) for p in paths}
    state = objects["R33_CURRENT_STATE.json"]
    registry = objects["R33_EXPERIMENT_REGISTRY.json"]
    consumed = objects["R33_CONSUMED_EVIDENCE_REGISTRY.json"]
    validate_registries(state, registry, consumed)
    audit = objects["R33_AUDIT_SCOPE.json"]
    for pin in audit["pinned_files"]:
        require(digest(ROOT / pin["path"]) == pin["sha256"], f"frozen source changed: {pin['path']}")
    links = 0
    for path in sorted(RESEARCH.glob("R33*.md")):
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
            target = target.split("#", 1)[0].strip("<>")
            if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            require((path.parent / target).is_file(), f"broken link in {path.name}: {target}")
            links += 1
    for path in (ROOT / "README.md", RESEARCH / "NEXT_AGENT_START_HERE.md",
                 RESEARCH / "TNN_ARCHITECTURE_ROLES_AND_CONNECTIONS.md",
                 RESEARCH / "TNN_MEGA_PLAN_WHITE_BOX_DEVELOPMENTAL_ARCHITECTURE.md"):
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text()):
            if Path(target).name.startswith("R33"):
                require((path.parent / target).is_file(), f"broken R33 entry link in {path.name}: {target}")
                links += 1
    schema = objects["R33_TELEMETRY_SCHEMA.json"]
    validate_schema_definition(schema, schema)
    require(len(schema["$defs"]["competency_metrics"]["required"]) == 17, "competency metric inventory incomplete")
    require(len(schema["$defs"]["resources"]["required"]) == 12, "resource inventory incomplete")
    for key in ("competency_metrics", "resources"):
        definition = schema["$defs"][key]
        require(set(definition["required"]) == set(definition["properties"]), f"optional required telemetry in {key}")
    if "R33_INDEPENDENT_REVIEWS.json" in objects:
        validate_reviews(objects["R33_INDEPENDENT_REVIEWS.json"])
        for review in objects["R33_INDEPENDENT_REVIEWS.json"]["reviews"]:
            for target in review["integration_paths"]:
                require((ROOT / target).is_file(), f"missing review integration path: {target}")
    if (RESEARCH / "R33_B000_SOURCE.zag").exists():
        validate_b000_source((RESEARCH / "R33_B000_SOURCE.zag").read_text(), (RESEARCH / "tnn_r32_epistemic_chunking.zag").read_text())
    if "R33_B000_SOURCE_MAP.json" in objects:
        mapping = objects["R33_B000_SOURCE_MAP.json"]
        require(mapping["copied_functions"] == list(COPIED_HELPERS), "source-map helper inventory changed")
        require(mapping["imports"] == [] and mapping["continuing_brain_loaded"] is False, "source-map scope changed")
        for path_key, hash_key in (("original_source", "original_sha256"), ("audit_source", "audit_source_sha256"), ("configuration", "configuration_sha256")):
            require(digest(ROOT / mapping[path_key]) == mapping[hash_key], f"source-map identity changed: {path_key}")
        validate_pins([mapping["compiler"]])
    for experiment in registry["experiments"]:
        require("R33_INDEPENDENT_REVIEWS.json" in objects, "preregistration lacks completed reviews")
        validate_batch(experiment, objects["R33_INDEPENDENT_REVIEWS.json"])
        execution = objects["R33_B000_EXECUTION_STATUS.json"]
        require(execution["status"] == experiment["status"], "batch execution status disagreement")
        require(execution["primary_execution_attempts"] == execution["native_fixture_exposures"] == 0, "unrecorded primary audit exposure")
        require(execution["observed_witness_results"] is None, "unexecuted audit has invented results")
        require(execution["compile_only_check"]["binary_executed"] is False, "compile-only evidence became native execution")
    if state.get("first_deliverable_complete") is True:
        require(state["review_status"] == "COMPLETED_AND_INTEGRATED", "completed state lacks reviews")
        require(state["all_r33_research_complete"] is False, "foundations mislabeled as completed R33 research")
        require(len(registry["experiments"]) == 1, "completed first deliverable lacks preregistration")
        require(state["active_experiment"] is None and state["r33_native_experiments_executed"] == 0 and state["r33_training_runs_executed"] == 0, "first-deliverable status implies unrecorded execution")
        require(state["learner_authority_newly_granted"] is False and state["scientifically_qualified_r33_milestone"] is None, "unqualified authority grant")
    return {
        "status": "PASS", "required_hierarchy_files_checked": len(REQUIRED_FILES),
        "json_files_parsed": len(paths), "local_markdown_links_checked": links,
        "frozen_source_hashes_checked": len(audit["pinned_files"]),
        "preregistration_hashes_checked": sum(len(x["source_pins"]) for x in registry["experiments"]),
        "completed_independent_reviews": len(objects.get("R33_INDEPENDENT_REVIEWS.json", {}).get("reviews", [])),
        "competency_metric_categories": 17, "resource_categories": 12,
        "schema_validation_scope": "PROJECT_ALLOWLISTED_KEYWORD_SUBSET_AND_SEMANTIC_CONTRACTS",
        "native_cognition_executed": False, "scientific_evidence_consumed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, help="Check one telemetry JSON record; read-only")
    parser.add_argument("--audit-output", type=Path, help="Parse saved B000 native stdout; never executes a binary")
    args = parser.parse_args()
    try:
        report = validate_repository()
        if args.record:
            validate_record(load_json(args.record), load_json(RESEARCH / "R33_TELEMETRY_SCHEMA.json"))
            report["record_validation"] = "PASS"
        if args.audit_output:
            report["boundary_audit_output"] = parse_b000_output(args.audit_output.read_text(), load_json(RESEARCH / "R33_B000_CONFIG.json"))
        print(json.dumps(report, indent=2, allow_nan=False))
        return 0
    except (ContractError, OSError, ValueError, KeyError, TypeError, StopIteration) as error:
        print(f"R33_VALIDATION_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
