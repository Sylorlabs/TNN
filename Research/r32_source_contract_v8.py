#!/usr/bin/env python3
"""Generate the deterministic R32 source contract V8 on stdout.

The contract is intentionally fail closed.  Static semantics, non-test call
sites, evaluator-label isolation, a complete entry point, and source-bound
native qualification evidence must all be present before ``pass`` can become
true.  No wall-clock time or file modification time enters the result.

Usage:
    python3 Research/r32_source_contract_v8.py
    python3 Research/r32_source_contract_v8.py --check

``--check`` compares the generated object with R32_SOURCE_CONTRACT_V8.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tarfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


RESEARCH = Path(__file__).resolve().parent
CORE_PATH = RESEARCH / "tnn_r32_e45_investigation_core.zag"
HARNESS_PATH = RESEARCH / "tnn_r32_e45_native_qualification.zag"
LEGACY_PATH = RESEARCH / "tnn_r32_epistemic_chunking.zag"
V7_GENERATOR_PATH = RESEARCH / "r32_source_contract_v7.py"
V7_ARTIFACT_PATH = RESEARCH / "R32_SOURCE_CONTRACT_V7.json"
V8_ARTIFACT_PATH = RESEARCH / "R32_SOURCE_CONTRACT_V8.json"
PROVENANCE_PATH = RESEARCH / "toolchain" / "R32_ZNC_PROVENANCE_2026-08-23.json"
PREIMPLEMENT_CHECKPOINT_PATH = (
    RESEARCH / "checkpoints" / "R32_E45_PREIMPLEMENT_2026-08-23.tar.gz"
)

# These are the frozen sources audited for V8. Regenerating the JSON against a
# different source cannot silently preserve a passing contract; changing either
# hash requires an explicit V8 audit revision.
AUDITED_CORE_SHA256 = "6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0"
AUDITED_HARNESS_SHA256 = "b404223658f51dc95cc20a76af515e8a3bc828a373e3a244d12a2cd7fb3d9f1e"

REQUIRED_RUNTIME_ASSERTIONS = {
    "oracle_no_unique_prevalence_gate": 1,
    "no_unique_d_cells_checked": 60,
    "no_unique_d_cells_passed": 60,
    "no_unique_d_cell_safety_gate": 1,
    "no_unique_d_partition_gate": 1,
    "no_unique_d_unknown_choice_gate": 1,
    "no_unique_d_wrong_commit_gate": 1,
    "known_truth_wrong_commit_gate": 1,
    "evaluator_label_inside_policy_call_graph": 0,
    "fixed_evidence_count_stopping": 0,
    "remaining_horizon_feature": 0,
    "budget_overspend_allowed": 0,
    "core_gate_sum": 4,
}

CORE_PRIMITIVES = (
    "r32e45_source_weight",
    "r32e45_temporal_observe",
    "r32e45_option_begin",
    "r32e45_option_record",
    "r32e45_per_step_value",
    "r32e45_option_value_generic",
    "r32e45_option_value_logical",
    "r32e45_option_value_full",
    "r32e45_option_continue",
    "r32e45_terminal_choose",
)

DECISION_SINKS = {
    "r32e45_per_step_value",
    "r32e45_option_value_generic",
    "r32e45_option_value_logical",
    "r32e45_option_value_full",
    "r32e45_option_continue",
    "r32e45_terminal_choose",
}

# Evaluator-only facts must not be arguments to cognition or feature values.
EVALUATOR_LABEL_RE = re.compile(
    r"\b(?:evaluator_(?:mode|regime|resource)|mode_label|resource_label|"
    r"answer_label|oracle(?:_\w+)?|grounded_outcome|ground_truth|truth|seed|"
    r"trial(?:_\w+)?|episode_id|safety_cap)\b",
    re.IGNORECASE,
)

# Counts may exist as audit/evaluator state.  They may not enter feature values,
# policy arguments, or policy control conditions as a stopping rule.
COUNT_STOP_RE = re.compile(
    r"\b(?:probe_count|max_probes|remaining(?:_\w+)?|fixed_duration|"
    r"option_duration|observations|observation_count|step_count|steps_taken|"
    r"trial_count|stage_count|countdown|remaining_to_\w+|E45_TAPE|tape_index)\b",
    re.IGNORECASE,
)

POLICY_NAME_RE = re.compile(
    r"(?:policy|decid|cho(?:ose|ice)|option_value|continue|initiat|terminal_action)",
    re.IGNORECASE,
)

FEATURE_ROOT_RE = re.compile(
    r"(?:fill|mask|resource).*features",
    re.IGNORECASE,
)

PREDICTION_ROOTS = {
    "e45_linear_predict",
    "e45_shadow_predict",
    "e45_hazard_predict",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_record(path: Path) -> dict:
    if not path.is_file():
        return {"path": path.name, "present": False}
    data = path.read_bytes()
    record = {
        "path": path.relative_to(RESEARCH).as_posix(),
        "present": True,
        "bytes": len(data),
        "sha256": sha256_bytes(data),
    }
    if path.suffix in {".zag", ".py", ".json", ".log", ".txt"}:
        record["lines"] = len(data.decode("utf-8", errors="replace").splitlines())
    return record


def _spaces_preserving_newlines(match: re.Match[str]) -> str:
    return "".join("\n" if char == "\n" else " " for char in match.group(0))


def strip_comments_and_strings(source: str) -> str:
    """Blank comments and strings while retaining offsets and line numbers."""
    source = re.sub(r"/\*.*?\*/", _spaces_preserving_newlines, source, flags=re.DOTALL)
    source = re.sub(r"//[^\n]*", _spaces_preserving_newlines, source)
    source = re.sub(r'"(?:\\.|[^"\\])*"', _spaces_preserving_newlines, source)
    return source


def balanced_end(source: str, opening: int, left: str, right: str) -> int | None:
    if opening >= len(source) or source[opening] != left:
        return None
    depth = 0
    for index in range(opening, len(source)):
        char = source[index]
        if char == left:
            depth += 1
        elif char == right:
            depth -= 1
            if depth == 0:
                return index
    return None


def split_top_level(arguments: str) -> list[str]:
    values: list[str] = []
    start = 0
    round_depth = square_depth = brace_depth = 0
    for index, char in enumerate(arguments):
        if char == "(":
            round_depth += 1
        elif char == ")":
            round_depth -= 1
        elif char == "[":
            square_depth += 1
        elif char == "]":
            square_depth -= 1
        elif char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth -= 1
        elif char == "," and round_depth == square_depth == brace_depth == 0:
            values.append(arguments[start:index].strip())
            start = index + 1
    tail = arguments[start:].strip()
    if tail:
        values.append(tail)
    return values


def parameter_names(signature: str) -> list[str]:
    names: list[str] = []
    for parameter in split_top_level(signature):
        match = re.match(r"\s*([A-Za-z_]\w*)\s*:", parameter)
        if match:
            names.append(match.group(1))
    return names


@dataclass(frozen=True)
class Function:
    name: str
    file: str
    line: int
    parameters: tuple[str, ...]
    signature: str
    body: str
    body_offset: int


@dataclass(frozen=True)
class Call:
    caller: str
    callee: str
    file: str
    line: int
    arguments: tuple[str, ...]


def parse_functions(path: Path) -> tuple[dict[str, Function], list[Call], str]:
    if not path.is_file():
        return {}, [], ""
    raw = path.read_text(encoding="utf-8")
    source = strip_comments_and_strings(raw)
    functions: dict[str, Function] = {}
    cursor = 0
    header_re = re.compile(r"\bfn\s+([A-Za-z_]\w*)\s*\(")
    while True:
        match = header_re.search(source, cursor)
        if not match:
            break
        name = match.group(1)
        open_paren = source.find("(", match.start())
        close_paren = balanced_end(source, open_paren, "(", ")")
        if close_paren is None:
            cursor = match.end()
            continue
        open_brace = source.find("{", close_paren + 1)
        next_fn = header_re.search(source, close_paren + 1)
        if open_brace < 0 or (next_fn and next_fn.start() < open_brace):
            cursor = close_paren + 1
            continue
        close_brace = balanced_end(source, open_brace, "{", "}")
        if close_brace is None:
            # An incomplete function must not hide the earlier complete ones.
            cursor = close_paren + 1
            continue
        signature = source[open_paren + 1 : close_paren]
        line = source.count("\n", 0, match.start()) + 1
        functions[name] = Function(
            name=name,
            file=path.name,
            line=line,
            parameters=tuple(parameter_names(signature)),
            signature=signature,
            body=source[open_brace + 1 : close_brace],
            body_offset=open_brace + 1,
        )
        cursor = close_brace + 1

    calls: list[Call] = []
    call_re = re.compile(r"\b([A-Za-z_]\w*)\s*\(")
    ignored = {"if", "while", "for", "switch", "return", "sizeof", "fn"}
    for function in functions.values():
        body = function.body
        for match in call_re.finditer(body):
            callee = match.group(1)
            if callee in ignored:
                continue
            open_paren = body.find("(", match.start())
            close_paren = balanced_end(body, open_paren, "(", ")")
            if close_paren is None:
                continue
            absolute = function.body_offset + match.start()
            line = source.count("\n", 0, absolute) + 1
            calls.append(
                Call(
                    caller=function.name,
                    callee=callee,
                    file=path.name,
                    line=line,
                    arguments=tuple(split_top_level(body[open_paren + 1 : close_paren])),
                )
            )
    return functions, calls, source


def call_label(call: Call) -> str:
    return f"{call.file}:{call.line}:{call.caller}->{call.callee}"


def non_test_call_sites(calls: Iterable[Call], primitive: str) -> list[str]:
    return sorted(
        call_label(call)
        for call in calls
        if call.callee == primitive
        and not re.search(r"(?:test|gate|probe)", call.caller, re.IGNORECASE)
    )


def transitive_reachable(roots: set[str], graph: dict[str, set[str]]) -> set[str]:
    seen: set[str] = set()
    pending = list(sorted(roots))
    while pending:
        name = pending.pop()
        if name in seen:
            continue
        seen.add(name)
        pending.extend(sorted(graph.get(name, set()) - seen))
    return seen


def indexed_assignment_violations(function: Function) -> tuple[list[dict], list[dict]]:
    evaluator_violations: list[dict] = []
    count_violations: list[dict] = []
    assignment_re = re.compile(r"\b([A-Za-z_]\w*)\s*\[[^\]]+\]\s*=\s*([^;]+)")
    for match in assignment_re.finditer(function.body):
        rhs = match.group(2)
        line = function.body[: match.start()].count("\n") + function.line
        record = {
            "site": f"{function.file}:{line}:{function.name}",
            "target": match.group(1),
            "expression": " ".join(rhs.split()),
        }
        if EVALUATOR_LABEL_RE.search(rhs):
            evaluator_violations.append(record)
        if COUNT_STOP_RE.search(rhs):
            count_violations.append(record)
    return evaluator_violations, count_violations


def json_truth_for_keys(value: object, keys: set[str]) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in keys and child is True:
                return True
            if json_truth_for_keys(child, keys):
                return True
    elif isinstance(value, list):
        return any(json_truth_for_keys(child, keys) for child in value)
    return False


def json_strings(value: object) -> set[str]:
    strings: set[str] = set()
    if isinstance(value, str):
        strings.add(value)
    elif isinstance(value, dict):
        for key, child in value.items():
            strings.add(str(key))
            strings.update(json_strings(child))
    elif isinstance(value, list):
        for child in value:
            strings.update(json_strings(child))
    return strings


def executable_format(path: Path) -> str | None:
    if not path.is_file():
        return None
    magic = path.read_bytes()[:4]
    if magic == b"\x7fELF":
        return "ELF"
    if magic in {b"\xcf\xfa\xed\xfe", b"\xfe\xed\xfa\xcf"}:
        return "Mach-O"
    return None


def scalar_log_values(text: str) -> dict[str, int]:
    """Read the harness's stable ``name,integer`` evidence rows."""
    values: dict[str, int] = {}
    for raw_line in text.splitlines():
        parts = raw_line.strip().split(",")
        if len(parts) != 2:
            continue
        try:
            values[parts[0]] = int(parts[1])
        except ValueError:
            continue
    return values


def runtime_assertion_record(path: Path, bound_strings: set[str]) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    values = scalar_log_values(text)
    missing = sorted(key for key in REQUIRED_RUNTIME_ASSERTIONS if key not in values)
    mismatched = {
        key: {"expected": expected, "actual": values.get(key)}
        for key, expected in REQUIRED_RUNTIME_ASSERTIONS.items()
        if key in values and values[key] != expected
    }
    gate_result = "MISSING"
    if "TNN_R32_E45_NATIVE_QUALIFICATION_GATE=PASS" in text:
        gate_result = "PASS"
    elif "TNN_R32_E45_NATIVE_QUALIFICATION_GATE=FAIL" in text:
        gate_result = "FAIL"
    manifest_bound = (
        path.name in bound_strings
        or sha256_bytes(path.read_bytes()) in bound_strings
    )
    return {
        "path": path.name,
        "manifest_bound": manifest_bound,
        "qualification_gate_result": gate_result,
        "required_values": {
            key: values[key] for key in REQUIRED_RUNTIME_ASSERTIONS if key in values
        },
        "missing_assertions": missing,
        "mismatched_assertions": mismatched,
        "pass": manifest_bound and gate_result == "PASS" and not missing and not mismatched,
    }


def native_evidence(harness_sha: str) -> tuple[dict, dict[str, bool]]:
    mac_binary = RESEARCH / "R32_E45_CORE_NATIVE_MACOS_ARM64"
    linux_binary = RESEARCH / "R32_E45_CORE_NATIVE_LINUX_X86_64"
    mac_log = RESEARCH / "R32_E45_CORE_NATIVE_MACOS_ARM64.log"
    linux_log = RESEARCH / "R32_E45_CORE_NATIVE_LINUX_X86_64.log"
    mac_text = mac_log.read_text(encoding="utf-8") if mac_log.is_file() else ""
    linux_text = linux_log.read_text(encoding="utf-8") if linux_log.is_file() else ""
    core_gate = "TNN_R32_E45_CORE_GATE=PASS"
    core_cross_arch = (
        executable_format(mac_binary) == "Mach-O"
        and executable_format(linux_binary) == "ELF"
        and mac_text == linux_text
        and core_gate in mac_text
    )

    candidates = sorted(
        path
        for path in RESEARCH.glob("R32_E45*")
        if "CORE" not in path.name
        and any(token in path.name for token in ("QUALIFICATION", "HARNESS", "NATIVE"))
    )
    binaries = [path for path in candidates if executable_format(path) is not None]
    logs = [path for path in candidates if path.suffix == ".log"]
    evidence_json_paths = [
        path
        for path in candidates
        if path.suffix == ".json" and path.name != V8_ARTIFACT_PATH.name
    ]
    evidence_json: list[tuple[Path, object]] = []
    for path in evidence_json_paths:
        try:
            evidence_json.append((path, json.loads(path.read_text(encoding="utf-8"))))
        except (OSError, json.JSONDecodeError):
            continue

    binary_hashes = {sha256_bytes(path.read_bytes()) for path in binaries}
    manifest_entries = [
        (path, value, json_strings(value)) for path, value in evidence_json
    ]
    bound_manifests = [
        (path, value, strings)
        for path, value, strings in manifest_entries
        if HARNESS_PATH.name in strings
        and harness_sha in strings
        and bool(binary_hashes & strings)
    ]
    source_bound = bool(bound_manifests)
    candidate_deterministic = any(
        json_truth_for_keys(
            value,
            {
                "double_build_byte_identical",
                "builds_byte_identical",
                "deterministic_build",
            },
        )
        for _, value in evidence_json
    )
    bound_deterministic = any(
        json_truth_for_keys(
            value,
            {
                "double_build_byte_identical",
                "builds_byte_identical",
                "deterministic_build",
            },
        )
        for _, value, _ in bound_manifests
    )
    if len(binaries) >= 2 and len(binary_hashes) < len(binaries):
        candidate_deterministic = True
        if source_bound:
            bound_deterministic = True

    bound_manifest_strings = set().union(
        *(strings for _, _, strings in bound_manifests)
    ) if bound_manifests else set()
    runtime_assertion_candidates = [
        runtime_assertion_record(path, bound_manifest_strings) for path in logs
    ]
    runtime_assertions = [
        record
        for record in runtime_assertion_candidates
        if record["manifest_bound"]
        or record["qualification_gate_result"] != "MISSING"
    ]
    passing_logs = [record["path"] for record in runtime_assertions if record["pass"]]
    source_bound_failed_logs = [
        record["path"]
        for record in runtime_assertions
        if record["manifest_bound"]
        and record["qualification_gate_result"] == "FAIL"
    ]
    source_bound_nonpassing_logs = [
        record["path"]
        for record in runtime_assertions
        if record["manifest_bound"] and not record["pass"]
    ]
    harness_compiled = bool(binaries) and source_bound
    harness_runtime = bool(passing_logs) and source_bound

    evidence = {
        "core_cross_arch_smoke": {
            "pass": core_cross_arch,
            "macos_binary": file_record(mac_binary),
            "linux_binary": file_record(linux_binary),
            "macos_log": file_record(mac_log),
            "linux_log": file_record(linux_log),
            "runtime_logs_byte_identical": bool(mac_text) and mac_text == linux_text,
            "required_gate": core_gate,
        },
        "qualification": {
            "binary_artifacts": [file_record(path) | {"format": executable_format(path)} for path in binaries],
            "runtime_logs": [file_record(path) for path in logs],
            "evidence_manifests": [file_record(path) for path, _ in evidence_json],
            "current_source_sha256": harness_sha,
            "source_and_binary_hash_bound_by_manifest": source_bound,
            "source_bound_manifests": [path.name for path, _, _ in bound_manifests],
            "candidate_deterministic_claim_present": candidate_deterministic,
            "current_harness_deterministic_build_evidence": bound_deterministic,
            "required_runtime_assertions": REQUIRED_RUNTIME_ASSERTIONS,
            "runtime_assertion_evidence": runtime_assertions,
            "passing_runtime_logs": passing_logs,
            "source_bound_failed_runtime_logs": source_bound_failed_logs,
            "source_bound_nonpassing_runtime_logs": source_bound_nonpassing_logs,
        },
        "compiler_provenance": file_record(PROVENANCE_PATH),
    }
    checks = {
        "native_core_cross_arch_smoke": core_cross_arch,
        "native_harness_compiled_source_bound": harness_compiled,
        "native_harness_deterministic_build": bound_deterministic and source_bound,
        "native_harness_runtime_gate_source_bound": harness_runtime,
        "native_harness_no_unique_and_known_truth_runtime_gates": harness_runtime,
    }
    return evidence, checks


def v7_migration_record(legacy_functions: dict[str, Function], legacy_calls: list[Call]) -> dict:
    v7_generator = V7_GENERATOR_PATH.read_text(encoding="utf-8") if V7_GENERATOR_PATH.is_file() else ""
    try:
        v7_artifact = json.loads(V7_ARTIFACT_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        v7_artifact = {}

    checks_block = re.search(r"checks\s*=\s*\{(.*?)\n\}", v7_generator, re.DOTALL)
    generator_keys = sorted(set(re.findall(r"['\"]([A-Za-z0-9_]+)['\"]\s*:", checks_block.group(1)))) if checks_block else []
    artifact_keys = sorted(v7_artifact.get("checks", {}).keys()) if isinstance(v7_artifact, dict) else []

    callee = legacy_functions.get("r32_epistemic_decide")
    wrapper = legacy_functions.get("r32_epistemic_decide_traced")
    forwarding = next(
        (
            call
            for call in legacy_calls
            if call.caller == "r32_epistemic_decide_traced" and call.callee == "r32_epistemic_decide"
        ),
        None,
    )
    expected = list(callee.parameters[-2:]) if callee else []
    forwarded = list(forwarding.arguments[-2:]) if forwarding else []
    wrapper_declared = list(wrapper.parameters) if wrapper else []
    current_mismatch = expected == ["expected_gain", "observation_cost"] and forwarded == ["probe_count", "max_probes"]

    checkpoint_source = ""
    checkpoint_member_sha = None
    if PREIMPLEMENT_CHECKPOINT_PATH.is_file():
        try:
            with tarfile.open(PREIMPLEMENT_CHECKPOINT_PATH, "r:gz") as archive:
                member = archive.extractfile("Research/tnn_r32_epistemic_chunking.zag")
                if member is not None:
                    member_bytes = member.read()
                    checkpoint_member_sha = sha256_bytes(member_bytes)
                    checkpoint_source = member_bytes.decode("utf-8")
        except (OSError, KeyError, tarfile.TarError, UnicodeDecodeError):
            checkpoint_source = ""
    stale_signature = re.search(
        r"fn\s+r32_epistemic_decide_traced\s*\([^)]*"
        r"probe_count\s*:\s*i32\s*,\s*max_probes\s*:\s*i32",
        checkpoint_source,
        re.DOTALL,
    )
    stale_forwarding = re.search(
        r"r32_epistemic_decide\s*\(\s*features\s*,\s*weights\s*,\s*bias\s*,"
        r"\s*commit_threshold\s*,\s*unknown_threshold\s*,\s*probe_count\s*,"
        r"\s*max_probes\s*\)",
        checkpoint_source,
        re.DOTALL,
    )
    stale_checkpoint_mismatch = bool(stale_signature and stale_forwarding)

    return {
        "v7_generator": file_record(V7_GENERATOR_PATH),
        "v7_artifact": file_record(V7_ARTIFACT_PATH),
        "hardcoded_mnt_data_paths": "/mnt/data/" in v7_generator,
        "generator_check_keys": generator_keys,
        "checked_in_artifact_check_keys": artifact_keys,
        "generator_schema_matches_checked_in_artifact": generator_keys == artifact_keys and bool(generator_keys),
        "stale_wrapper_argument_mismatch": {
            "present_in_v8_preimplementation_checkpoint": stale_checkpoint_mismatch,
            "present_in_current_source": current_mismatch,
            "callee": "r32_epistemic_decide",
            "callee_expected_tail_parameters": expected,
            "wrapper": "r32_epistemic_decide_traced",
            "wrapper_declared_parameters": wrapper_declared,
            "forwarded_tail_arguments": forwarded,
            "call_site": call_label(forwarding) if forwarding else None,
            "checkpoint": file_record(PREIMPLEMENT_CHECKPOINT_PATH),
            "checkpoint_legacy_source_sha256": checkpoint_member_sha,
            "meaning": (
                "The V8 preimplementation checkpoint proves that the traced wrapper labeled "
                "its decision inputs probe_count/max_probes and forwarded them positionally as "
                "expected_gain/observation_cost. The current fields separately show whether that "
                "legacy defect has since been repaired."
            ),
        },
        "v8_disposition": "Recorded as legacy debt; V8 qualification uses the E45 core/harness and does not silently claim this wrapper repaired.",
    }


def build_contract() -> dict:
    core_functions, core_calls, core_source = parse_functions(CORE_PATH)
    harness_functions, harness_calls, harness_source = parse_functions(HARNESS_PATH)
    legacy_functions, legacy_calls, _ = parse_functions(LEGACY_PATH)
    all_functions = core_functions | harness_functions
    all_calls = core_calls + harness_calls

    graph: dict[str, set[str]] = {name: set() for name in all_functions}
    for call in all_calls:
        if call.caller in graph and call.callee in all_functions:
            graph[call.caller].add(call.callee)

    inferred_policy_roots = {
        name
        for name in all_functions
        if name in DECISION_SINKS
        or name in PREDICTION_ROOTS
        or POLICY_NAME_RE.search(name)
        or FEATURE_ROOT_RE.search(name)
    }
    decision_reachable = transitive_reachable(inferred_policy_roots, graph)

    # Calls made *inside* cognition are in scope, as are calls crossing directly
    # into an inferred cognition root. A generic helper reachable from cognition
    # (for example clamp) is not thereby a policy sink everywhere else in the
    # program; this avoids misclassifying delayed evaluator-supervised training.
    decision_calls = [
        call
        for call in all_calls
        if call.caller in decision_reachable or call.callee in inferred_policy_roots
    ]
    forbidden_policy_arguments: list[dict] = []
    count_policy_arguments: list[dict] = []
    forbidden_policy_parameters: list[dict] = []
    count_policy_parameters: list[dict] = []
    for name in sorted(inferred_policy_roots):
        function = all_functions[name]
        for parameter in function.parameters:
            record = {
                "site": f"{function.file}:{function.line}:{function.name}",
                "parameter": parameter,
            }
            if EVALUATOR_LABEL_RE.search(parameter):
                forbidden_policy_parameters.append(record)
            if COUNT_STOP_RE.search(parameter):
                count_policy_parameters.append(record)
    for call in decision_calls:
        for position, argument in enumerate(call.arguments):
            # A count used only to select the already-observed evidence/state is
            # an evaluator cursor, not a learner feature or stopping input. Keep
            # evaluator-label checks strict inside indices, but remove bracket
            # expressions for the count/stage test. Direct or arithmetic count
            # arguments remain visible and fail closed.
            count_expression = re.sub(r"\[[^\]]*\]", "[]", argument)
            record = {
                "site": call_label(call),
                "argument_index": position,
                "expression": " ".join(argument.split()),
            }
            if EVALUATOR_LABEL_RE.search(argument):
                forbidden_policy_arguments.append(record)
            if COUNT_STOP_RE.search(count_expression):
                count_policy_arguments.append(record)

    feature_evaluator_violations: list[dict] = []
    feature_count_violations: list[dict] = []
    count_control_violations: list[dict] = []
    for function in all_functions.values():
        if "feature" in function.name.lower():
            evaluator_hits, count_hits = indexed_assignment_violations(function)
            feature_evaluator_violations.extend(evaluator_hits)
            feature_count_violations.extend(count_hits)
        if function.name in decision_reachable and POLICY_NAME_RE.search(function.name):
            for match in re.finditer(r"\bif\s*\(([^)]*)\)", function.body):
                condition = match.group(1)
                if COUNT_STOP_RE.search(condition):
                    line = function.line + function.body[: match.start()].count("\n")
                    count_control_violations.append(
                        {
                            "site": f"{function.file}:{line}:{function.name}",
                            "condition": " ".join(condition.split()),
                        }
                    )

    call_sites = {
        primitive: non_test_call_sites(harness_calls, primitive) for primitive in CORE_PRIMITIVES
    }

    core_compact = "\n".join(line.strip() for line in core_source.splitlines())
    combined_code = core_source + "\n" + harness_source
    forbidden_architecture_tokens = sorted(
        set(
            match.group(0).lower()
            for match in re.finditer(
                r"\b(?:transformer|tokenizer|next_token|bpe|graph_node|graph_edge|"
                r"vad_boundary|fixed_boundary|max_probes)\b",
                combined_code,
                re.IGNORECASE,
            )
        )
    )

    temporal_parameters = set(core_functions.get("r32e45_temporal_observe", Function("", "", 0, (), "", "", 0)).parameters)
    begin_parameters = set(core_functions.get("r32e45_option_begin", Function("", "", 0, (), "", "", 0)).parameters)
    record_parameters = set(core_functions.get("r32e45_option_record", Function("", "", 0, (), "", "", 0)).parameters)

    projection_function = harness_functions.get("e45_terminal_projection")
    terminal_choice_function = harness_functions.get("e45_terminal_choice_learned")
    full_feature_function = harness_functions.get("e45_fill_full_features")
    main_function = harness_functions.get("main")

    def compact(value: str) -> str:
        return re.sub(r"\s+", "", value)

    projection_compact = compact(projection_function.body) if projection_function else ""
    terminal_choice_compact = compact(terminal_choice_function.body) if terminal_choice_function else ""
    main_compact = compact(main_function.body) if main_function else ""
    terminal_projection_callers = {
        caller: compact(harness_functions[caller].body) if caller in harness_functions else ""
        for caller in ("e45_train_episode", "e45_evaluate_arm_episode")
    }
    projected_terminal_flow_re = re.compile(
        r"e45_terminal_projection\(option,terminal_option\);.*?"
        r"e45_fill_full_features\([^;]*terminal_option[^;]*\);.*?"
        r"e45_mask_features\([^;]*E45_ARM_D[^;]*\);.*?"
        r"e45_terminal_choice_learned\("
    )
    projected_terminal_flows = {
        caller: projected_terminal_flow_re.search(body) is not None
        for caller, body in terminal_projection_callers.items()
    }

    forbidden_feature_state_re = re.compile(
        r"\b(?:E45_O_OBS|E45_S_TOTAL|E45_S_FLIPS|E45_TAPE|observations|"
        r"remaining(?:_\w+)?|probe_count|max_probes|seed|evaluator_mode|"
        r"evaluator_resource)\b",
        re.IGNORECASE,
    )
    forbidden_elapsed_feature_identifiers = sorted(
        set(forbidden_feature_state_re.findall(full_feature_function.body))
        if full_feature_function
        else {"missing_e45_fill_full_features"}
    )

    no_unique_source_fragments = {
        "per_cell_modes_0_1": "if(mode==0||mode==1)" in main_compact,
        "per_cell_unknown_floor_700": "e45_rate(d_cell_unknown,d_cell_episodes)>=700" in main_compact,
        "per_cell_wrong_ceiling_300": "e45_rate(d_cell_wrong,d_cell_episodes)<=300" in main_compact,
        "all_60_cells_required": "no_unique_cells_checked!=60||no_unique_cells_passed!=no_unique_cells_checked" in main_compact,
        "aggregate_partition_required": "no_unique_unknown+no_unique_wrong==no_unique_episodes" in main_compact,
        "aggregate_unknown_floor_700": "no_unique_unknown_rate>=700" in main_compact,
        "aggregate_wrong_ceiling_300": "no_unique_wrong_rate<=300" in main_compact,
    }
    known_truth_source_fragments = {
        "known_modes_exclude_no_unique": "if(mode>=2)" in main_compact,
        "outcome_partition_all_arms": all(
            f"known_{arm}_success+known_{arm}_unknown+known_{arm}_wrong==known_{arm}_episodes"
            in main_compact
            for arm in "abcd"
        ),
        "d_wrong_not_above_a_b_c": all(
            f"known_d_wrong<=known_{arm}_wrong" in main_compact for arm in "abc"
        ),
        "d_success_not_below_c": "known_d_success>=known_c_success" in main_compact,
        "four_of_six_joint_seeds": "known_joint_seed_count>=4" in main_compact,
    }
    final_gate_names = (
        "shadow_gate",
        "baseline_parity",
        "causal_gate",
        "oracle_prevalence_gate",
        "mode_coverage_gate",
        "no_unique_prevalence_gate",
        "resource_coverage_gate",
        "no_unique_unknown_gate",
        "no_unique_wrong_commit_gate",
        "no_unique_partition_gate",
        "no_unique_cell_safety_gate",
        "known_truth_wrong_commit_gate",
    )
    final_gate_source_complete = (
        all(name in main_compact for name in final_gate_names)
        and "==12&&r32e45_core_gate()==4" in main_compact
        and "TNN_R32_E45_NATIVE_QUALIFICATION_GATE=PASS"
        in HARNESS_PATH.read_text(encoding="utf-8")
        and "TNN_R32_E45_NATIVE_QUALIFICATION_GATE=FAIL"
        in HARNESS_PATH.read_text(encoding="utf-8")
    )

    source_records = {
        "core": file_record(CORE_PATH),
        "qualification_harness": file_record(HARNESS_PATH),
        "legacy_r32": file_record(LEGACY_PATH),
    }
    harness_sha = source_records["qualification_harness"].get("sha256", "")
    native, native_checks = native_evidence(harness_sha)
    v7_migration = v7_migration_record(legacy_functions, legacy_calls)
    wrapper_record = v7_migration["stale_wrapper_argument_mismatch"]

    static_checks: dict[str, bool] = {
        "source_files_present": CORE_PATH.is_file() and HARNESS_PATH.is_file(),
        "audited_frozen_source_hashes_match": (
            source_records["core"].get("sha256") == AUDITED_CORE_SHA256
            and source_records["qualification_harness"].get("sha256")
            == AUDITED_HARNESS_SHA256
        ),
        "no_retired_or_fixed_boundary_substrate": not forbidden_architecture_tokens,
        "provenance_dependence_semantics_defined": (
            "r32e45_source_weight" in core_functions
            and "source_seen*dependence_penalty" in core_compact
            and "1000+source_seen*dependence_penalty" in core_compact
        ),
        "historical_and_current_epoch_state_separate": {
            "historical_a",
            "historical_b",
            "epoch_a",
            "epoch_b",
            "current_state",
            "prior_state",
        }.issubset(temporal_parameters),
        "transition_support_and_counterevidence_explicit": {
            "transition_support",
            "transition_counter",
            "learned_leave_weight",
            "learned_counter_weight",
            "learned_persistence_value",
        }.issubset(temporal_parameters),
        "replacement_and_reversal_semantics_explicit": (
            "R32E45_TRACE_REVERSAL" in core_source
            and "candidate==old_prior" in core_compact
            and "prior_state.*=old_current" in core_compact
        ),
        "persistent_option_state_explicit": {
            "active",
            "target_favored",
            "target_alternative",
            "cause_evidence",
            "predicted_favored",
            "predicted_alternative",
            "support_since_start",
            "contradiction_since_start",
            "accumulated_shadow_cost",
        }.issubset(begin_parameters),
        "option_consequence_credit_updates_explicit": {
            "observed_consequence",
            "expected_favored",
            "expected_alternative",
            "support_since_start",
            "contradiction_since_start",
            "accumulated_shadow_cost",
        }.issubset(record_parameters),
        "logical_unknown_is_terminal_action": (
            "r32e45_terminal_choose" in core_functions
            and "R32E45_TERM_UNKNOWN" in core_source
            and "unknown_value" in core_functions["r32e45_terminal_choose"].parameters
        ),
        "zero_utility_option_boundary": (
            "r32e45_option_continue" in core_functions
            and re.search(r"if\s*\(\s*value\s*>\s*0\s*\)", core_functions["r32e45_option_continue"].body) is not None
        ),
        "terminal_projection_clears_transient_option_state": (
            projection_function is not None
            and "e45_copy(option,terminal_option,E45_OPTION_N);" in projection_compact
            and "terminal_option[E45_O_ACTIVE]=0;" in projection_compact
            and "terminal_option[E45_O_CREDIT]=0;" in projection_compact
            and "terminal_option[E45_O_REASON]=R32E45_TRACE_TERMINATE;"
            in projection_compact
        ),
        "terminal_projection_used_before_train_and_eval_terminal_policy": all(
            projected_terminal_flows.values()
        ),
        "terminal_policy_is_shared_and_arm_invariant": (
            terminal_choice_function is not None
            and tuple(terminal_choice_function.parameters)
            == ("weights", "biases", "features")
            and "arm" not in terminal_choice_compact.lower()
        ),
        "no_elapsed_count_or_remaining_horizon_features": not forbidden_elapsed_feature_identifiers,
        "no_unique_safety_gate_source_complete": all(no_unique_source_fragments.values()),
        "known_truth_safety_gate_source_complete": all(known_truth_source_fragments.values()),
        "final_qualification_gate_includes_no_unique_and_known_truth": final_gate_source_complete,
        "legacy_traced_wrapper_argument_contract_repaired": (
            wrapper_record["present_in_v8_preimplementation_checkpoint"]
            and not wrapper_record["present_in_current_source"]
            and wrapper_record["forwarded_tail_arguments"]
            == ["expected_gain", "observation_cost"]
        ),
        "harness_complete_entrypoint": "main" in harness_functions,
        "harness_calls_provenance_from_non_test_path": bool(call_sites["r32e45_source_weight"]),
        "harness_calls_temporal_state_from_non_test_path": bool(call_sites["r32e45_temporal_observe"]),
        "harness_begins_and_records_persistent_option": bool(call_sites["r32e45_option_begin"] and call_sites["r32e45_option_record"]),
        "harness_exercises_abcd_value_ladder": all(
            call_sites[name]
            for name in (
                "r32e45_per_step_value",
                "r32e45_option_value_generic",
                "r32e45_option_value_logical",
                "r32e45_option_value_full",
            )
        ),
        "harness_uses_option_continuation_and_terminal_unknown": bool(
            call_sites["r32e45_option_continue"] and call_sites["r32e45_terminal_choose"]
        ),
        "delayed_model_update_call_sites_present": bool(
            non_test_call_sites(harness_calls, "e45_linear_update")
            and non_test_call_sites(harness_calls, "e45_shadow_update")
        ),
        "all_four_matched_arms_present": all(
            len(re.findall(rf"\bE45_ARM_{arm}\b", harness_source)) >= 2 for arm in "ABCD"
        ),
        "learner_decision_graph_present": bool(
            set(call.callee for call in harness_calls) & DECISION_SINKS
        ),
        "no_evaluator_label_in_policy_call_arguments": not forbidden_policy_arguments,
        "no_evaluator_label_in_policy_parameters": not forbidden_policy_parameters,
        "no_evaluator_label_written_to_features": not feature_evaluator_violations,
        "no_count_or_stage_in_policy_call_arguments": not count_policy_arguments,
        "no_count_or_stage_in_policy_parameters": not count_policy_parameters,
        "no_count_or_stage_written_to_features": not feature_count_violations,
        "no_count_based_policy_control_condition": not count_control_violations,
    }

    checks = static_checks | native_checks
    required_failures = [name for name, value in checks.items() if not value]
    passed = not required_failures
    if passed:
        status = "PASS"
    elif any(
        name.startswith("no_evaluator") or name.startswith("no_count")
        for name in required_failures
    ):
        status = "PENDING_SOURCE_ISOLATION_REPAIR"
    elif native["qualification"]["source_bound_failed_runtime_logs"]:
        status = "NATIVE_QUALIFICATION_FAILED"
    elif native["qualification"]["source_bound_nonpassing_runtime_logs"]:
        status = "NATIVE_QUALIFICATION_EVIDENCE_FAILED"
    elif not static_checks["harness_complete_entrypoint"]:
        status = "PENDING_HARNESS_COMPLETION"
    elif not native_checks["native_harness_compiled_source_bound"]:
        status = "PENDING_NATIVE_HARNESS_COMPILE"
    else:
        status = "PENDING_NATIVE_QUALIFICATION_EVIDENCE"

    return {
        "contract_version": 8,
        "pass": passed,
        "status": status,
        "generated_by": "Research/r32_source_contract_v8.py",
        "claim_boundary": (
            "V8 passes only with actual E45 temporal/option semantics, non-test call sites, "
            "learner/evaluator isolation, and deterministic source-bound native harness evidence. "
            "Core smoke evidence alone cannot promote R32."
        ),
        "inputs": source_records,
        "checks": checks,
        "failed_required_checks": required_failures,
        "semantic_evidence": {
            "temporal_observe_parameters": sorted(temporal_parameters),
            "option_begin_parameters": sorted(begin_parameters),
            "option_record_parameters": sorted(record_parameters),
            "forbidden_architecture_identifiers": forbidden_architecture_tokens,
            "audited_core_sha256": AUDITED_CORE_SHA256,
            "audited_harness_sha256": AUDITED_HARNESS_SHA256,
            "terminal_projection_callers": projected_terminal_flows,
            "terminal_projection_parameters": (
                list(projection_function.parameters) if projection_function else []
            ),
            "shared_terminal_policy_parameters": (
                list(terminal_choice_function.parameters) if terminal_choice_function else []
            ),
            "forbidden_elapsed_feature_identifiers": forbidden_elapsed_feature_identifiers,
            "no_unique_gate_source_fragments": no_unique_source_fragments,
            "known_truth_gate_source_fragments": known_truth_source_fragments,
            "final_gate_required_terms": list(final_gate_names),
        },
        "call_site_evidence": {
            "non_test_harness_calls": call_sites,
            "inferred_policy_roots": sorted(inferred_policy_roots),
            "decision_reachable_functions": sorted(decision_reachable),
            "forbidden_policy_argument_violations": forbidden_policy_arguments,
            "forbidden_policy_parameter_violations": forbidden_policy_parameters,
            "forbidden_feature_assignment_violations": feature_evaluator_violations,
            "count_policy_argument_violations": count_policy_arguments,
            "count_policy_parameter_violations": count_policy_parameters,
            "count_feature_assignment_violations": feature_count_violations,
            "count_policy_control_violations": count_control_violations,
            "detector_scope": (
                "Checks direct decision-graph arguments, indexed feature assignments, and "
                "policy-named control conditions. Evaluator loop caps may exist, but may not "
                "be passed into cognition or learner features."
            ),
        },
        "native_evidence": native,
        "v7_migration": v7_migration,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if checked-in R32_SOURCE_CONTRACT_V8.json differs",
    )
    arguments = parser.parse_args()
    contract = build_contract()
    rendered = json.dumps(contract, indent=2, ensure_ascii=False) + "\n"
    if arguments.check:
        if not V8_ARTIFACT_PATH.is_file():
            print(f"missing: {V8_ARTIFACT_PATH}", file=sys.stderr)
            return 1
        try:
            checked_in = json.loads(V8_ARTIFACT_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            print(f"invalid JSON: {error}", file=sys.stderr)
            return 1
        if checked_in != contract:
            print("R32_SOURCE_CONTRACT_V8.json is stale", file=sys.stderr)
            return 1
        print("R32_SOURCE_CONTRACT_V8.json matches generator")
        return 0
    sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
