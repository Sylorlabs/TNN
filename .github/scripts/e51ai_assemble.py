"""Assemble E51AI without running scientific entry points or altering frozen AH."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

SOURCE = "c8f62bac285e72653bd6e9412498575ea8036b77"
AH_SHA = "8ee32cdb8b51b4e996c8a42968227eae8c29879c62d5df3f4bd749263658cc23"
root = Path(".scratch/e51ai")
root.mkdir(parents=True, exist_ok=True)
for name in ("e51x", "e51y", "e51ad", "e51ah"):
    path = f".github/scripts/{name}_assemble.py"
    if Path(path).read_bytes() != subprocess.check_output(["git", "show", f"{SOURCE}:{path}"]):
        raise SystemExit(f"Inherited assembler modified: {path}")
    subprocess.run([sys.executable, path], check=True, timeout=60)
parent = Path(".scratch/e51ah/tnn_r32_e51ah_grounded_preservation_replay.zag").read_bytes()
if hashlib.sha256(parent).hexdigest() != AH_SHA:
    raise SystemExit("Frozen complete E51AH assembly mismatch")
prefix_path = "Research/R32_E51AE_NATIVE/02a_run_direct.zagfrag"
prefix = subprocess.check_output(["git", "show", f"{SOURCE}:{prefix_path}"]).decode()
prefix = prefix.replace("E51AE", "E51AI").replace("e51ae", "e51ai")
prefix = prefix.replace("trajectory_critical_candidate_residual_v1", "longitudinal_context_diagnostic_v1")
prefix = prefix.replace("native_candidate_value_capacity_discriminator_not_promotion", "exploratory_persistent_learning_diagnostic_not_qualification")
prefix = prefix.replace("residual_features,32_evaluator_blind_terminal_features", "residual_features,current_quadratic_real_lag_destroyed_lag_matched_controls")
helper = Path("Research/R32_E51AI_NATIVE/01_helpers.zagfrag").read_text()
tail = Path("Research/R32_E51AI_NATIVE/02_run.zagfrag").read_text()
fragment = helper + "\n" + prefix + "\n" + tail
src = parent.decode()
old = Path("Research/R32_E51AH_NATIVE/03_main_injection.zagfrag").read_text()
new = old.replace("e51ah", "e51ai")
marker = "fn e51y_run(\n"
if src.count(marker) != 1 or src.count(old) != 1:
    raise SystemExit("Non-unique experiment insertion anchor")
src = src.replace(marker, fragment + "\n" + marker, 1).replace(old, new, 1)
if src.count("let e51ah_completion:i32=e51ah_run(") or src.count("let e51ai_completion:i32=e51ai_run(") != 1:
    raise SystemExit("Wrong active entry point")
if "e51ai_world_gate()" not in prefix or "e51ai_run(" not in prefix:
    raise SystemExit("Wrong reconstruction prefix")
# Learner routines are limited to sanitized x, training targets and weights.
fit_body = helper.split("fn e51ai_fit(", 1)[1].split("fn e51ai_choice(", 1)[0]
for forbidden in ("probe_", "e51ai_evaluate(", "mode", "truth", "meta["):
    if forbidden in fit_body:
        raise SystemExit(f"Unexpected learner channel: {forbidden}")
pair_body = helper.split("fn e51ai_feature_pair(", 1)[1].split("fn e51ai_column(", 1)[0]
if "e50_batch_column" not in pair_body or "index+1" in pair_body or "+34" in pair_body:
    raise SystemExit("Feature boundary violation")
(root / "SOURCE.zag").write_text(src)
(root / "E51AI_FRAGMENT.zag").write_text(fragment)
core = Path(".scratch/e51ah/tnn_r32_e45_investigation_core.zag")
(root / core.name).write_bytes(core.read_bytes())

inherited = json.loads(Path(".scratch/e51ah/TRANSITIVE_SOURCE_MANIFEST.json").read_text())
paths = {x["path"] for x in inherited["files"]}
paths.update((".github/scripts/e51ah_assemble.py", "Research/R32_E51AH_GROUNDED_PRESERVATION_REPLAY_PREREG.md"))
paths.update(str(p) for p in Path("Research/R32_E51AH_NATIVE").glob("*.zagfrag"))
paths.update(("Research/R32_E51AI_LONGITUDINAL_CONTEXT_PREREG.md", "Research/R32_E51AI_HARDCODING_LEDGER.json"))
paths.update(str(p) for p in Path("Research/R32_E51AI_NATIVE").glob("*.zagfrag"))
paths.update(str(p) for p in Path(".github/scripts").glob("e51ai_*.py"))
paths.add(".github/workflows/r32-e51ai-native.yml")
entries = []
for path in sorted(paths):
    data = Path(path).read_bytes()
    dest = root / "inputs" / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    entries.append({"path": path, "sha256": hashlib.sha256(data).hexdigest(),
                    "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()})
manifest = {"parent_scientific_commit": SOURCE, "assembled_parent_sha256": AH_SHA,
            "source_sha256": hashlib.sha256(src.encode()).hexdigest(), "files": entries}
(root / "SOURCE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
(root / "SOURCE_PIN_GATE.txt").write_text("1\n")
print(json.dumps({"source_sha256": manifest["source_sha256"], "input_files": len(entries)}))
