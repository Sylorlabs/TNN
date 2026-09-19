"""Assemble E51AJ from immutable E51AI inputs without executing cognition."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

PARENT = "c46fbbf67e1b7d5a19dee7ca1164fc4c5b0eec22"
PARENT_SHA = "20916b1836b15fa591d204766f3eadf8f62a2e23ab4203e717ff279fb078bb61"
OUT = Path(".scratch/e51aj")


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f"non-unique assembly marker: {old[:90]}")
    return text.replace(old, new, 1)


def function(text, name):
    marker = f"fn {name}("
    if text.count(marker) != 1:
        raise ValueError(f"non-unique function: {name}")
    return marker + text.split(marker, 1)[1].split("\nfn ", 1)[0]


def assemble():
    OUT.mkdir(parents=True, exist_ok=True)
    inherited_assembler = Path(".github/scripts/e51ai_assemble.py")
    if inherited_assembler.read_bytes() != subprocess.check_output(["git", "show", f"{PARENT}:{inherited_assembler}"]):
        raise ValueError("parent assembler changed")
    subprocess.run([sys.executable, "-B", str(inherited_assembler)], check=True, timeout=240)
    parent = Path(".scratch/e51ai/SOURCE.zag").read_text()
    if hashlib.sha256(parent.encode()).hexdigest() != PARENT_SHA:
        raise ValueError("parent assembly identity changed")
    manifest = json.loads(Path(".scratch/e51ai/SOURCE_MANIFEST.json").read_text())
    if len(manifest["files"]) != 53:
        raise ValueError("parent manifest width changed")
    paths = set()
    for entry in manifest["files"]:
        path = entry["path"]
        if Path(path).read_bytes() != subprocess.check_output(["git", "show", f"{PARENT}:{path}"]):
            raise ValueError(f"frozen parent input changed: {path}")
        paths.add(path)
    original = Path("Research/R32_E51AI_NATIVE/01_helpers.zagfrag").read_text()
    reused = "\n".join(function(original, name) for name in (
        "e51ai_feature_pair", "e51ai_raw", "e51ai_hash", "e51ai_fit", "e51ai_choice", "e51ai_success"
    )).replace("e51ai", "e51aj").replace("E51AI", "E51AJ")
    fit = function(reused, "e51aj_fit")
    for forbidden in ("probe_", "e51aj_evaluate", "truth", "meta[", "mode", "checkpoint"):
        if forbidden in fit:
            raise ValueError(f"learner channel violation: {forbidden}")
    prefix = Path("Research/R32_E51AE_NATIVE/02a_run_direct.zagfrag").read_text()
    prefix = prefix.replace("e51ae", "e51aj").replace("E51AE", "E51AJ")
    prefix = prefix.replace("trajectory_critical_candidate_residual_v1", "shared_start_replay_order_dose_v1")
    prefix = prefix.replace("native_candidate_value_capacity_discriminator_not_promotion", "exploratory_replay_order_dose_not_qualification")
    prefix = prefix.replace("residual_features,32_evaluator_blind_terminal_features", "residual_features,32_current_plus_32_same_episode_lag")
    data = Path("Research/R32_E51AI_NATIVE/02_run.zagfrag").read_text()
    data = "    let train_x" + data.split("    let train_x", 1)[1].split("    let weights", 1)[0]
    data = data.replace("e51ai", "e51aj").replace("E51AI", "E51AJ")
    data = replace_once(data, "let stage:i32=111+dataset;", "let stage:i32=119+replica*8+dataset;")
    for key in ("training_record", "dataset"):
        data = replace_once(data, f'_zag_print("e51aj_{key},");',
                            f'_zag_print("e51aj_{key},"); e45_print_i32(replica); _zag_print(",");')
    beginning = """
    let integrity:i32=1;
    let schedule_gate:i32=e51aj_schedule_gate(); e45_print_pair("e51aj_schedule_gate",schedule_gate);
    if(world_gate!=1 || schedule_gate!=1 || terminal_reproduction_gate!=1 || direct_integrity!=1 || terminal_hash_before!=238967492 || direct_hash_before!=1790306570){ integrity=0; }
    if(integrity!=1){ _zag_println("e51aj_integrity_gate,0"); return 0; }
    let replica:i32=0;
    while(replica<3){
"""
    native = Path("Research/R32_E51AJ_NATIVE")
    fragment = ((native / "01_schedule.zagfrag").read_text() + "\n" + reused + "\n" +
                (native / "02_measure.zagfrag").read_text() + "\n" + prefix + beginning + data +
                (native / "03_continue.zagfrag").read_text())
    old_entry = Path("Research/R32_E51AH_NATIVE/03_main_injection.zagfrag").read_text().replace("e51ah", "e51ai")
    new_entry = old_entry.replace("e51ai", "e51aj")
    source = replace_once(parent, "fn e51y_run(\n", fragment + "\nfn e51y_run(\n")
    source = replace_once(source, old_entry, new_entry)
    if source.count("let e51ai_completion:i32=e51ai_run(") or source.count("let e51aj_completion:i32=e51aj_run(") != 1:
        raise ValueError("wrong active scientific entry point")
    digest = hashlib.sha256(source.encode()).hexdigest()
    pin = Path("Research/R32_E51AJ_SOURCE_PIN.json")
    if pin.exists() and json.loads(pin.read_text())["source_sha256"] != digest:
        raise ValueError("E51AJ source pin mismatch")
    (OUT / "SOURCE.zag").write_text(source)
    (OUT / "E51AJ_FRAGMENT.zag").write_text(fragment)
    core = "tnn_r32_e45_investigation_core.zag"
    (OUT / core).write_bytes((Path(".scratch/e51ai") / core).read_bytes())
    paths.update(str(p) for p in native.glob("*.zagfrag"))
    paths.update(str(p) for p in Path(".github/scripts").glob("e51aj_*.py"))
    paths.update(("Research/R32_E51AJ_REPLAY_ORDER_DOSE_PREREG.md", "Research/R32_E51AJ_HARDCODING_LEDGER.json",
                  ".github/workflows/r32-e51aj-native.yml"))
    if pin.exists():
        paths.add(str(pin))
    entries = []
    for path in sorted(paths):
        content = Path(path).read_bytes()
        dest = OUT / "inputs" / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)
        entries.append({"path": path, "sha256": hashlib.sha256(content).hexdigest(),
                        "git_blob": hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()})
    result = {"parent_scientific_commit": PARENT, "parent_source_sha256": PARENT_SHA,
              "source_sha256": digest, "files": entries}
    (OUT / "SOURCE_MANIFEST.json").write_text(json.dumps(result, indent=2) + "\n")
    (OUT / "SOURCE_PIN_GATE.txt").write_text("1\n" if pin.exists() else "0\n")
    print(json.dumps({"source_sha256": digest, "input_files": len(entries), "pinned": pin.exists()}))


if __name__ == "__main__":
    assemble()
