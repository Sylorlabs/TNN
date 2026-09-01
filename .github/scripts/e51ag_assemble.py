from pathlib import Path
import subprocess

PINNED_BLOBS = {
    "Research/R32_E51AG_CURRENT_RESIDUAL_REPLICATION_PREREG.md": "212821c903ae05ddb3446b77c7a6fb4f421f05ad",
    "Research/R32_E51AE_NATIVE/01a_contract_selection.zagfrag": "7881bf966d0a41dbb01abca61be438446b58ea77",
    "Research/R32_E51AE_NATIVE/01b_objective_fit.zagfrag": "dcf6a244c1589b56065d2ce3349827de55777ac7",
    "Research/R32_E51AE_NATIVE/01c_evaluation.zagfrag": "e739fb1c5f3529ceda2f8edd7a66d96891c9b71e",
    "Research/R32_E51AE_NATIVE/02a_run_direct.zagfrag": "d056a87e525699d1f7532bdc4a01b22af386a7ea",
    "Research/R32_E51AE_NATIVE/02b_run_development.zagfrag": "f2bc7df4e5211962ccf7d6159eb4f6ecb7ae5652",
    "Research/R32_E51AE_NATIVE/02c_run_local.zagfrag": "2157436269c77126a3a1a606b3bdd9c8be837f34",
}

for path, expected in PINNED_BLOBS.items():
    actual = subprocess.check_output(["git", "hash-object", path], text=True).strip()
    if actual != expected:
        raise SystemExit(f"E51AG source pin failure: {path}: expected {expected}, got {actual}")

def transform_parent(text: str) -> str:
    text = text.replace("E51AE", "E51AG").replace("e51ae", "e51ag")
    old_val = "const E51AG_STAGE_VALIDATION:i32=98;"
    old_conf = "const E51AG_STAGE_CONFIRM:i32=99;"
    if text.count(old_val) != 1 or text.count(old_conf) != 1:
        raise SystemExit("E51AG stage substitution anchor failure")
    text = text.replace(old_val, "const E51AG_STAGE_VALIDATION:i32=104;", 1)
    text = text.replace(old_conf, "const E51AG_STAGE_CONFIRM:i32=107;", 1)
    text = text.replace(
        "experiment_schema,tnn_r32_e51ag_trajectory_critical_candidate_residual_v1",
        "experiment_schema,tnn_r32_e51ag_current_residual_replication_v1",
    )
    text = text.replace(
        "claim_boundary,native_candidate_value_capacity_discriminator_not_promotion",
        "claim_boundary,frozen_current_residual_replication_not_promotion",
    )
    return text

base_path = Path(".scratch/e51ad/tnn_r32_e51ad_trajectory_critical_router.zag")
if not base_path.exists():
    raise SystemExit(f"missing frozen E51AD base: {base_path}")
src = base_path.read_text()

parent_paths = (
    "Research/R32_E51AE_NATIVE/01a_contract_selection.zagfrag",
    "Research/R32_E51AE_NATIVE/01b_objective_fit.zagfrag",
    "Research/R32_E51AE_NATIVE/01c_evaluation.zagfrag",
    "Research/R32_E51AE_NATIVE/02a_run_direct.zagfrag",
    "Research/R32_E51AE_NATIVE/02b_run_development.zagfrag",
    "Research/R32_E51AE_NATIVE/02c_run_local.zagfrag",
)
parent = "".join(Path(p).read_text() for p in parent_paths)
parent = transform_parent(parent)
contract = Path("Research/R32_E51AG_NATIVE/01d_replication_contract.zagfrag").read_text()
tail = Path("Research/R32_E51AG_NATIVE/02d_run_replication.zagfrag").read_text()
frag = parent + contract + tail

if "E51AE_STAGE_VALIDATION" in frag or "e51ae_" in frag:
    raise SystemExit("E51AG namespace transformation incomplete")
if "const E51AG_STAGE_VALIDATION:i32=98;" in frag:
    raise SystemExit("E51AG stage-98 validation path present")
if frag.count("const E51AG_STAGE_VALIDATION:i32=104;") != 1:
    raise SystemExit("E51AG stage-104 anchor failure")
if frag.count("const E51AG_STAGE_CONFIRM:i32=107;") != 1:
    raise SystemExit("E51AG stage-107 anchor failure")

old_injection = Path("Research/R32_E51AD_NATIVE/03_main_injection.zagfrag").read_text()
new_injection = Path("Research/R32_E51AG_NATIVE/03_main_injection.zagfrag").read_text()
marker = "fn e51y_run(\n"
if src.count(marker) != 1:
    raise SystemExit(f"E51AG function insertion marker count {src.count(marker)}")
if src.count(old_injection) != 1:
    raise SystemExit(f"E51AG main injection anchor count {src.count(old_injection)}")
src = src.replace(marker, frag + "\n\n" + marker, 1)
src = src.replace(old_injection, new_injection, 1)

scratch = Path(".scratch/e51ag")
scratch.mkdir(parents=True, exist_ok=True)
(scratch / "E51AG_FRAGMENT.zag").write_text(frag)
(scratch / "tnn_r32_e51ag_current_residual_replication.zag").write_text(src)
core = Path("Research/tnn_r32_e45_investigation_core.zag")
(scratch / "tnn_r32_e45_investigation_core.zag").write_bytes(core.read_bytes())
(scratch / "SOURCE_PIN_GATE.txt").write_text("1\n")
