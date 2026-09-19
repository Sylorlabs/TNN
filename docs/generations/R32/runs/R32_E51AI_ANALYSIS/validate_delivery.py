"""Read-only consistency checks for the E51AI result and current authority.

Run from any directory: python3 -B Research/R32_E51AI_ANALYSIS/validate_delivery.py
Requires the preserved archive directory recorded in R32_E51AI_EVIDENCE.json.
No experimental source or result is modified and no learner is executed.
"""
import ast
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "Research"
ANALYSIS = RESEARCH / "R32_E51AI_ANALYSIS"
SOURCE = "c46fbbf67e1b7d5a19dee7ca1164fc4c5b0eec22"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def tables(text):
    result, current = [], []
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            current.append([cell.strip() for cell in line.strip().strip("|").split("|")])
        elif current:
            require(len(current) >= 2, "malformed Markdown table")
            require(all(len(row) == len(current[0]) for row in current), "unequal Markdown table widths")
            result.append(current)
            current = []
    return result


def numbers(row):
    return [int(cell.replace(",", "")) for cell in row[1:]]


def main():
    evidence = load(RESEARCH / "R32_E51AI_EVIDENCE.json")
    archive = ROOT / evidence["local_archive_directory"]
    summary = load(ANALYSIS / "SUMMARY.json")
    scientific = evidence["frozen_scientific_verification"]
    state = load(RESEARCH / "R32_E51AI_EXECUTION_STATUS.json")
    authority = load(RESEARCH / "R32_NATIVE_AUTHORITY_CURRENT.json")
    detail = load(RESEARCH / "R32_NATIVE_AUTHORITY_DETAIL.json")
    ledger = load(RESEARCH / "R32_E51_MASTER_LEDGER.json")
    entry = next(row for row in ledger["experiments"] if row["id"] == "E51AI")
    report = (RESEARCH / "R32_E51AI_RESULT.md").read_text()
    require(evidence == runpy.run_path(str(ANALYSIS / "package.py"))["package"](archive, ROOT),
            "evidence package differs from independently regenerated package")
    require(evidence["state"] == state["state"] == "COMPLETED_VERIFIED_EXPLORATORY_DIAGNOSTIC", "incorrect completed state")
    require(state["scientific_outcome"] == scientific["outcome"] == entry["outcome"]
            == "LONGITUDINAL_CONTEXT_DIAGNOSTIC_COMPLETE", "outcome mismatch")
    require(state["artifact_verified"] is True and state["history_preserving_signal"] is False
            and entry["history_preserving_signal"] is False and summary["history_preserving_signal"] is False,
            "incorrect verification or signal state")
    require(authority["active_experiment"] is None and detail["active_experiment"] is None
            and ledger["current_frontier"]["active_experiment"] is None, "stale active experiment")
    require(authority["latest_authoritative_result"] == "R32_E51AI_RESULT.md"
            and detail["latest_authoritative_result"]["experiment"] == "R32_E51AI"
            and ledger["current_frontier"]["latest_authoritative_result"] == "E51AI", "wrong latest result")
    for obj in (evidence, state, authority, detail, ledger):
        require(obj["promotion_allowed"] is False, "promotion must remain prohibited")
        require(obj.get("canonical_system", obj.get("canonical_model")) == "R27", "canonical system changed")
    require(state["actual_blocks_completed"] == 32 and state["checkpoint_coefficients_verified"] == 17160,
            "wrong actual block/parameter count")
    require(state["actual_training_record_presentations_per_arm"] == 34560
            and scientific["probe_episode_rows_verified"] == 293760, "wrong exposure count")
    require(state["validation_executed"] == state["confirmation_executed"] == 0, "qualification exposure")
    for field, metric in (("final_reachability_by_arm", "reachable"), ("final_no_unique_by_arm", "no_unique"),
                          ("final_union_losses_by_arm", "union_lost"), ("final_anchor_losses_by_arm", "anchor_lost")):
        require(entry["observations"][field] == [summary["arms"][str(arm)]["final"][metric] for arm in range(4)],
                f"ledger observations mismatch: {field}")

    parsed = tables(report)
    final_table = next(table for table in parsed if table[0][:2] == ["Arm", "Total"])
    final_fields = ("reachable", "known", "no_unique", "union_lost", "union_rescued", "hybrid_lost", "hybrid_rescued")
    for arm, row in enumerate(final_table[2:]):
        require(numbers(row) == [summary["arms"][str(arm)]["final"][field] for field in final_fields], "final result table mismatch")
    cycle_table = next(table for table in parsed if table[0][0] == "Checkpoint")
    require(len(cycle_table[2:]) == 9, "missing cycle endpoint")
    for cycle, row in enumerate(cycle_table[2:]):
        require(numbers(row) == [summary["arms"][str(arm)]["cycle_end_reachability"][cycle] for arm in range(4)], "cycle table mismatch")
    anchor_table = next(table for table in parsed if table[0][:2] == ["Arm", "Anchor successes"])
    retention_fields = ("anchor_successes", "ever_lost", "regained_at_final", "missing_at_final", "never_lost", "worst_simultaneous_loss_after_cycle_one")
    for arm, row in enumerate(anchor_table[2:]):
        require(numbers(row) == [summary["arms"][str(arm)]["first_encounter_retention"][field] for field in retention_fields], "anchor table mismatch")
    cohort_table = next(table for table in parsed if table[0][0] == "Cohort")
    for cohort, row in enumerate(cohort_table[2:]):
        require(numbers(row) == [summary["arms"][str(arm)]["cohort_retention"][cohort]["missing_at_final"] for arm in range(4)], "cohort table mismatch")
    decision_table = next(table for table in parsed if table[0][0] == "Policy")
    decisions = [summary["arms"]["0"]["baseline"]] + [summary["arms"][str(arm)]["final"] for arm in range(4)]
    for row, expected in zip(decision_table[2:], decisions):
        require(numbers(row) == [expected[field] for field in ("t0success", "t0unknown", "t0wrong")], "initial-decision table mismatch")
        require(sum(numbers(row)) == 2160, "initial-decision denominator mismatch")

    manifest = load(archive / "extracted/SOURCE_MANIFEST.json")
    protected = [row["path"] for row in manifest["files"]] + [
        "Research/R32_E51_BASELINE_V1.json", "Research/R32_E51AH_IMPLEMENTATION_CONTRACT.md",
        "Research/R32_E51AH_HARDCODING_LEDGER.json", "Research/toolchain/znc_linux_x86_64_abed8aa1"]
    for path in protected:
        expected = subprocess.check_output(["git", "show", f"{SOURCE}:{path}"], cwd=ROOT, timeout=20)
        require((ROOT / path).read_bytes() == expected, f"frozen working source changed: {path}")
    baseline = subprocess.check_output(["git", "show", "09c5fcf63f295b52b6c82299d01ac340d554dd4e:Research/R32_E51_BASELINE_V1.json"], cwd=ROOT, timeout=20)
    require((RESEARCH / "R32_E51_BASELINE_V1.json").read_bytes() == baseline, "immutable baseline changed")
    for name, expected in evidence["analysis_file_sha256"].items():
        require(hashlib.sha256((ANALYSIS / name).read_bytes()).hexdigest() == expected, f"analysis digest mismatch: {name}")
    for path in ANALYSIS.glob("*.py"):
        ast.parse(path.read_text(), filename=str(path))
    link_count = 0
    for path in [RESEARCH / "R32_E51AI_RESULT.md", ANALYSIS / "README.md", ANALYSIS / "VALIDATION.md"]:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            require((path.parent / target).exists(), f"broken local link: {path.name} -> {target}")
            link_count += 1
    for name in ("R32_HANDOFF.md", "R32_COMPACT_HANDOFF_CURRENT.md"):
        top = (RESEARCH / name).read_text().split("## Historical E51AH", 1)[0]
        require("Completed E51AI" in top and "9964554609" in top and "R32_E51AI_RESULT.md" in top,
                f"stale handoff: {name}")
    print(json.dumps({"verified": True, "duplicate_free_json_documents": 6,
                      "frozen_files_unchanged": len(protected), "native_probe_rows_verified": 293760,
                      "report_tables_checked": 5, "local_links_checked": link_count,
                      "evidence_and_all_analysis_tables_reproduced": True,
                      "canonical_system": "R27", "history_preserving_signal": False}, indent=2))


if __name__ == "__main__":
    main()
