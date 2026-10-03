"""External compilation/evaluation for native C01 components; no Python cognition."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
import sys

from r33_validate import RESEARCH, ROOT, ContractError, digest, load_json, parse_b000_output, require, validate_pins
from r33_bounded_audit import COMPILER, bounded, utc, write_json
from r33_execution_validate import verify as verify_inherited_execution

SOURCES = ["R33_B001_COMPONENTS.zag", "R33_B001_C01_DRIVER.zag"]
CONFIG = RESEARCH / "R33_B001_C01_CONFIG.json"
FREEZE = RESEARCH / "R33_B001_C01_FREEZE.json"
RUN = RESEARCH / "R33_B001_C01_RUN_PRIMARY_V1"


def expanded_config(config: dict) -> dict:
    """An external mathematical oracle over reported native values, not a codec."""
    result = copy.deepcopy(config)
    for key, spec in result.pop("generated_expected_vectors").items():
        if spec == {"count": 65536, "rule": "UNSIGNED16_TO_SIGNED16_IN_ASCENDING_CODE_ORDER"}:
            result["expected_vectors"][key] = [i if i < 32768 else i - 65536 for i in range(65536)]
        elif spec == {"count": 12288, "rule": "INDEX_TIMES_29_PLUS_11_MOD_256"}:
            result["expected_vectors"][key] = [(i * 29 + 11) % 256 for i in range(12288)]
        else:
            raise ContractError("unrecognized exhaustive oracle")
    return result


def check_inventory() -> dict:
    config = load_json(CONFIG)
    driver = (RESEARCH / SOURCES[1]).read_text()
    metrics = re.findall(r'c01_metric\("([^"\n]+)"', driver)
    vectors = re.findall(r'c01_vector\("([^"\n]+)"', driver)
    require(len(metrics) == len(set(metrics)) and len(vectors) == len(set(vectors)), "duplicate driver key")
    expected = expanded_config(config)
    require(set(metrics) == set(expected["expected_metrics"]), "metric/config inventory differs")
    require(set(vectors) == set(expected["expected_vectors"]), "vector/config inventory differs")
    source = (RESEARCH / SOURCES[0]).read_text()
    require("@import" not in source, "component imports hidden code")
    require(re.findall(r'@import\("([^"]+)"\)', driver) == [SOURCES[0]], "unexpected driver import")
    text = re.sub(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"', " ", source + "\n" + driver, flags=re.S)
    names = re.findall(r"\bfn\s+(\w+)\s*\(", text)
    allowed = {
        "r33_arrays_disjoint", "r33_exact_copy", "r33_pcm16le_decode", "r33_pcm16le_encode",
        "r33_rgb8_ingest", "r33_order_accept", "r33_protected_lru", "r33_reconstruct_exact",
        "r33_commit_logged", "r33_reconstruct_bound", "c01_capacity_edges", "c01_metric", "c01_vector", "c01_fill", "c01_audio",
        "c01_raw_vision", "c01_order_lru", "c01_chunk_trace", "main",
    }
    require(len(names) == len(set(names)) and set(names) == allowed, "unexpected native function inventory")
    calls = set(re.findall(r"\b(\w+)\s*\(", text))
    require(calls <= allowed | {"import", "if", "while", "zalloc_i", "zfree", "_zag_print", "_zag_println", "_zag_i64_to_str"},
            "native call outside reviewed allowlist")
    return {"metrics": len(metrics), "vectors": len(vectors),
            "vector_elements": sum(len(x) for x in expected["expected_vectors"].values())}


def compile_only(number: int) -> dict:
    require(number > 0 and number < 100, "invalid explicit build number")
    check_inventory()
    directory = RESEARCH / ("R33_B001_C01_BUILD_" + str(number).zfill(2))
    require(not directory.exists(), "build already recorded; inspect failure before another explicit build")
    directory.mkdir(mode=0o700)
    for name in SOURCES:
        with (directory / name).open("xb") as output:
            output.write((RESEARCH / name).read_bytes())
    command = [str(COMPILER), str(directory / SOURCES[1]), "--target", "macos-arm64",
               "--no-zagd", "--no-analyze", "--no-foreground-cache", "-o", str(directory / "c01")]
    compilation = bounded(command, directory, "compile", wall=60, cpu=55, output_limit=65536, sandboxed=False)
    result = {"status": "COMPILE_PASS_NOT_EXECUTED" if compilation["exit_code"] == 0 and compilation["termination_reason"] is None else "COMPILE_FAILURE",
              "date": utc(), "directory": str(directory.relative_to(ROOT)), "runtime_executions": 0,
              "compile": compilation, "source_pins": [{"path": str((directory / name).relative_to(ROOT)),
              "sha256": digest(directory / name)} for name in SOURCES], "compiler_sha256": digest(COMPILER)}
    if (directory / "c01").exists():
        result["binary_sha256"] = digest(directory / "c01")
    write_json(directory / "BUILD_RECORD.json", result)
    return result


def parse_saved(path: Path) -> dict:
    parsed = parse_b000_output(path.read_text(), expanded_config(load_json(CONFIG)))
    return {"status": "COMPONENT_CASES_MATCHED" if not parsed["mismatched_keys"] else "COMPONENT_MISMATCH",
            "mismatched_keys": parsed["mismatched_keys"], "metrics": parsed["metrics"],
            "vector_counts": {key: len(value) for key, value in parsed["vectors"].items()},
            "all_vector_values_checked": True, "natural_sensory_qualification": False,
            "durable_state_qualification": False, "learner_capability_qualification": False}


def verify_saved() -> dict:
    freeze = load_json(FREEZE)
    validate_pins(freeze["pins"])
    result = load_json(RUN / "RESULT.json")
    manifest = load_json(RUN / "MANIFEST.json")
    validate_pins(manifest["files"])
    paths = [x["path"] for x in manifest["files"]]
    require(len(paths) == len(set(paths)), "duplicate result artifact")
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        require(path.resolve().parent == RUN.resolve(), "result artifact outside primary directory")
        require(path.stat().st_size == entry["bytes"], "artifact size changed")
    require({p.name for p in RUN.iterdir() if p.is_file()} ==
            {Path(x).name for x in paths} | {"MANIFEST.json"}, "missing or extra run artifact")
    reservation = load_json(RUN / "RESERVATION.json")
    require(reservation["freeze_sha256"] == digest(FREEZE), "execution freeze changed")
    require(result["training_runs"] == 0 and result["fixture_exposures"] in (0, 1), "exposure scope changed")
    for flag in ("canonical_mutated", "learner_authority_granted", "natural_sensory_qualification",
                 "durable_state_qualification", "promotion"):
        require(result[flag] is False, "unqualified component claim")
    if result.get("runtime"):
        require(digest(RUN / "c01") == result["binary_sha256"], "executed binary differs")
        for stream in ("stdout", "stderr"):
            require(digest(RUN / ("native." + stream)) == result["runtime"][stream + "_sha256"], "native stream differs")
        if result.get("parsed_output"):
            require(parse_saved(RUN / "native.stdout") == result["parsed_output"], "external parser reproduction differs")
    if result["status"] == "COMPONENT_CASES_MATCHED":
        runtime = result["runtime"]
        require(result["fixture_exposures"] == 1 and not result["errors"], "success without valid exposure")
        require(runtime["exit_code"] == 0 and runtime["termination_reason"] is None and runtime["stderr_bytes"] == 0,
                "runtime failure mislabeled success")
        for key, maximum in (("wall_seconds", 30), ("cpu_seconds", 20), ("peak_rss_bytes", 268435456), ("stdout_bytes", 8388608)):
            require(0 <= runtime[key] <= maximum, "resource ceiling violated")
    registry = load_json(RESEARCH / "R33_EXPERIMENT_REGISTRY.json")
    batch = next(x for x in registry["experiments"] if x["id"] == "R33-B001-C01")
    consumed = load_json(RESEARCH / "R33_CONSUMED_EVIDENCE_REGISTRY.json")
    fixture = next(x for x in consumed["diagnostic_fixtures"] if x["batch_id"] == "R33-B001-C01")
    require(batch["primary_attempts"] == 1 and batch["native_fixture_exposures"] == result["fixture_exposures"]
            == fixture["primary_executions"], "registry/exposure disagreement")
    require(fixture["fresh_generalization_evidence"] is False, "regression fixtures relabeled fresh")
    return {"status": "PASS", "result_status": result["status"], "artifact_hashes_checked": len(paths),
            "native_exposures": result["fixture_exposures"], "all_r33_complete": False,
            "native_component_inventory": check_inventory()}


def update(status: str, exposures: int, result: dict | None = None) -> None:
    registry = load_json(RESEARCH / "R33_EXPERIMENT_REGISTRY.json")
    state = load_json(RESEARCH / "R33_CURRENT_STATE.json")
    consumed = load_json(RESEARCH / "R33_CONSUMED_EVIDENCE_REGISTRY.json")
    batch = next(x for x in registry["experiments"] if x["id"] == "R33-B001-C01")
    active = "R33-B001-C01" if status == "RUNNING" else None
    registry["active_experiment"] = state["active_experiment"] = active
    batch.update(status=status, primary_attempts=1, native_fixture_exposures=exposures)
    state.update(status="SUBSTRATE_COMPONENT_" + status, r33_native_experiments_executed=1+exposures,
                 next_action="Analyze component evidence; continue actual byte-ingress, provenance and durable state qualification")
    fixture = next(x for x in consumed["diagnostic_fixtures"] if x["batch_id"] == "R33-B001-C01")
    fixture.update(primary_executions=exposures, reserved_primary_attempts=1,
                   status="CONSUMED_COMPONENT_REGRESSION" if exposures else "RESERVED")
    if result is not None:
        batch["result_record"] = "Research/R33_B001_C01_RUN_PRIMARY_V1/RESULT.json"
        batch["result_status"] = result["status"]
    for name, obj in (("R33_EXPERIMENT_REGISTRY.json", registry), ("R33_CURRENT_STATE.json", state),
                      ("R33_CONSUMED_EVIDENCE_REGISTRY.json", consumed)):
        write_json(RESEARCH / name, obj, exclusive=False)


def run() -> dict:
    verify_inherited_execution()
    freeze = load_json(FREEZE)
    require(freeze["status"] == "PREREGISTERED_BEFORE_PRIMARY_EXECUTION", "unfrozen component run")
    validate_pins(freeze["pins"])
    require(freeze["review_disposition"] == "ACCEPTED_FOR_COMPONENT_TEST_ONLY", "review gate incomplete")
    registry = load_json(RESEARCH / "R33_EXPERIMENT_REGISTRY.json")
    state = load_json(RESEARCH / "R33_CURRENT_STATE.json")
    require(state["canonical_system"] == "R27" and not state["promotion_allowed"]
            and not state["canonical_mutated"] and not state["learner_authority_newly_granted"],
            "unexpected canonical or authority state")
    require(registry["active_experiment"] is None, "another experiment active")
    batch = next(x for x in registry["experiments"] if x["id"] == "R33-B001-C01")
    require(batch["status"] == "PREREGISTERED_NOT_EXECUTED" and batch["primary_attempts"] == 0,
            "primary attempt already admitted")
    require(not RUN.exists(), "primary directory exists; no silent repeat")
    build = ROOT / freeze["build_record"]
    record = load_json(build)
    require(record["status"] == "COMPILE_PASS_NOT_EXECUTED", "no successful compile")
    require(digest(COMPILER) == record["compiler_sha256"], "compiler identity changed")
    validate_pins(record["source_pins"])
    for name in SOURCES:
        require(digest(build.parent / name) == digest(RESEARCH / name), "current source differs from compiled source")
    binary = build.parent / "c01"
    require(digest(binary) == record["binary_sha256"], "build binary drift")
    check_inventory()
    RUN.mkdir(mode=0o700)
    write_json(RUN / "RESERVATION.json", {"batch": batch, "date": utc(), "primary_attempt": 1,
               "freeze_sha256": digest(FREEZE), "build_record_sha256": digest(build)})
    result = {"batch_id": "R33-B001-C01", "status": "INFRASTRUCTURE_FAILURE", "errors": [],
              "fixture_exposures": 0, "training_runs": 0, "canonical_mutated": False,
              "learner_authority_granted": False, "natural_sensory_qualification": False,
              "durable_state_qualification": False, "promotion": False}
    try:
        update("RUNNING", 0)
        with (RUN / "c01").open("xb") as output:
            output.write(binary.read_bytes())
        (RUN / "c01").chmod(0o700)
        require(digest(RUN / "c01") == record["binary_sha256"], "copied binary drift")
        validate_pins(freeze["pins"])
        result["binary_sha256"] = digest(RUN / "c01")
        write_json(RUN / "NATIVE_ADMISSION.json", {"date": utc(), "binary_sha256": result["binary_sha256"],
                   "freeze_sha256": digest(FREEZE), "fixture_namespace": load_json(CONFIG)["fixture_namespace"]})
        result["fixture_exposures"] = 1
        update("RUNNING", 1)
        result["runtime"] = bounded([str(RUN / "c01")], RUN, "native", wall=30, cpu=20, output_limit=8388608)
        require(result["runtime"]["exit_code"] == 0 and result["runtime"]["termination_reason"] is None,
                "native runtime failed or resource violation")
        require(result["runtime"]["stderr_bytes"] == 0, "unexpected native stderr")
        result["parsed_output"] = parse_saved(RUN / "native.stdout")
        result["status"] = result["parsed_output"]["status"]
    except Exception as error:
        result["errors"].append(repr(error))
    result["finished_utc"] = utc()
    write_json(RUN / "RESULT.json", result)
    update("COMPLETED" if result["status"] == "COMPONENT_CASES_MATCHED" else "FAILED_REQUIRES_ANALYSIS",
           result["fixture_exposures"], result)
    write_json(RUN / "MANIFEST.json", {"files": [{"path": str(p.relative_to(ROOT)),
               "sha256": digest(p), "bytes": p.stat().st_size} for p in sorted(RUN.iterdir()) if p.is_file()]})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--compile", type=int, metavar="ATTEMPT")
    group.add_argument("--inventory", action="store_true")
    group.add_argument("--run", action="store_true")
    group.add_argument("--parse", type=Path)
    group.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    try:
        result = (compile_only(args.compile) if args.compile else verify_saved() if args.verify else run() if args.run else
                  parse_saved(args.parse) if args.parse else check_inventory())
        print(json.dumps(result, indent=2))
        return 1 if result.get("status") in ("COMPILE_FAILURE", "INFRASTRUCTURE_FAILURE", "COMPONENT_MISMATCH") else 0
    except (ContractError, OSError, ValueError, KeyError, StopIteration) as error:
        print("R33_C01_FAIL: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
