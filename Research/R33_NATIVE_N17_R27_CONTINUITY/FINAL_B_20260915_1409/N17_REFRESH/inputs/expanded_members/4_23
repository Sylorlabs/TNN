from pathlib import Path
import ast
import hashlib
import json
import subprocess


PARENT_SOURCE_REV = "80069f979084f0dcc6341fffe59b8e1a7ad2e7f1"
PARENT_ASSEMBLERS = (
    ".github/scripts/e51x_assemble.py",
    ".github/scripts/e51y_assemble.py",
    ".github/scripts/e51ad_assemble.py",
)
PARENT_ASSEMBLED_SHA256 = "67ac4a8412e4098a9572a248bee2be1c9b6ea9699fd52cc568e5e25e1c132314"
CORE_SHA256 = "6812efb4c2cb990a59bd0f33f0a44469950201cac6633099fa4f4b2c7ae276e0"

PINNED_BLOBS = {
    "Research/R32_E51AH_GROUNDED_PRESERVATION_REPLAY_PREREG.md": "bd6f34e689b73004b7d3605fb37e63bba7a532c9",
    "Research/R32_E51AE_NATIVE/01a_contract_selection.zagfrag": "7881bf966d0a41dbb01abca61be438446b58ea77",
    "Research/R32_E51AE_NATIVE/01b_objective_fit.zagfrag": "dcf6a244c1589b56065d2ce3349827de55777ac7",
    "Research/R32_E51AE_NATIVE/02a_run_direct.zagfrag": "d056a87e525699d1f7532bdc4a01b22af386a7ea",
    "Research/R32_E51AD_NATIVE/03_main_injection.zagfrag": "3c616cecb3c75258b7aa4aab85cb198295d9a381",
}


def frozen_parent_entry(path: str) -> dict:
    expected = subprocess.check_output(
        ["git", "rev-parse", f"{PARENT_SOURCE_REV}:{path}"], text=True
    ).strip()
    actual = subprocess.check_output(["git", "hash-object", path], text=True).strip()
    if actual != expected:
        raise SystemExit(f"E51AH transitive parent pin failure: {path}")
    data = Path(path).read_bytes()
    return {"path": path, "git_blob": actual, "sha256": hashlib.sha256(data).hexdigest()}


# These three frozen assemblers use literal Research paths for all source reads.
# Verify the scripts before inspecting their literals; the assembled-source and
# imported-core pins below independently cover the complete cognitive bytes.
parent_manifest = [frozen_parent_entry(path) for path in PARENT_ASSEMBLERS]
parent_paths = {path for path in PINNED_BLOBS if "R32_E51AH" not in path}
parent_paths.add("Research/tnn_r32_e45_investigation_core.zag")
for script in PARENT_ASSEMBLERS:
    for node in ast.walk(ast.parse(Path(script).read_text())):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value
            if value.startswith("Research/") and value.endswith((".zagfrag", ".zag")):
                parent_paths.add(value)
parent_manifest.extend(frozen_parent_entry(path) for path in sorted(parent_paths))


for path, expected in PINNED_BLOBS.items():
    actual = subprocess.check_output(["git", "hash-object", path], text=True).strip()
    if actual != expected:
        raise SystemExit(
            f"E51AH source pin failure: {path}: expected {expected}, got {actual}"
        )


def transform_namespace(text: str) -> str:
    return text.replace("E51AE", "E51AH").replace("e51ae", "e51ah")


def transform_support(text: str) -> str:
    text = transform_namespace(text)
    replacements = {
        "const E51AH_STAGE_DEV:i32=97;": "const E51AH_STAGE_DEV:i32=108;",
        "const E51AH_STAGE_VALIDATION:i32=98;": "const E51AH_STAGE_VALIDATION:i32=109;",
        "const E51AH_STAGE_CONFIRM:i32=99;": "const E51AH_STAGE_CONFIRM:i32=110;",
        "const E51AH_PREVIOUS_STAGE:i32=96;": "const E51AH_PREVIOUS_STAGE:i32=107;",
        "const E51AH_ARMS:i32=5;": "const E51AH_ARMS:i32=6;",
    }
    for old, new in replacements.items():
        if text.count(old) != 1:
            raise SystemExit(f"E51AH support anchor count for {old!r}: {text.count(old)}")
        text = text.replace(old, new, 1)

    # E51AE's arm labels and dose helper describe its superseded 5-arm layout.
    # E51AH supplies its own explicit 6-arm map below, so retaining these dead
    # declarations would make the assembled audit surface internally ambiguous.
    legacy_arm_lines = (
        "const E51AH_ARM_GLOBAL:i32=1;\n"
        "const E51AH_ARM_LOCAL_96:i32=2;\n"
        "const E51AH_ARM_LOCAL_384:i32=3;\n"
        "const E51AH_ARM_DIRECT_ORACLE:i32=4;\n"
    )
    if text.count(legacy_arm_lines) != 1:
        raise SystemExit(
            f"E51AH legacy arm block count: {text.count(legacy_arm_lines)}"
        )
    text = text.replace(legacy_arm_lines, "", 1)

    legacy_dose = (
        "fn e51ah_dose(arm:i32)i32 {\n"
        "    if(arm==E51AH_ARM_LOCAL_96){ return 96; }\n"
        "    return 384;\n"
        "}\n\n"
    )
    if text.count(legacy_dose) != 1:
        raise SystemExit(f"E51AH legacy dose helper count: {text.count(legacy_dose)}")
    text = text.replace(legacy_dose, "", 1)

    # E51AH classifies development support from frozen mechanism success and
    # grounded candidate utility. Remove E51AE's now-unused evaluator-mode
    # classifier entirely so prohibited identifiers are absent from the learner
    # support implementation, not merely unreachable at runtime.
    legacy_classifier = (
        "fn e51ah_classify_kinds(base_kinds:[]i32,episodes:i32,per_cell:i32,kinds:[]i32,slot_count:*i32,direct_count:*i32,neither_known:*i32,neither_nu:*i32)void {\n"
        "    slot_count.*=0; direct_count.*=0; neither_known.*=0; neither_nu.*=0;\n"
        "    let episode:i32=0;\n"
        "    while(episode<episodes){\n"
        "        if(base_kinds[episode]==E51AD_KIND_PRESERVE){ kinds[episode]=E51AH_KIND_SLOT_COVERED; slot_count.*=slot_count.*+1;\n"
        "        }else{ if(base_kinds[episode]==E51AD_KIND_DIRECT_ONLY){ kinds[episode]=E51AH_KIND_DIRECT_REQUIRED; direct_count.*=direct_count.*+1;\n"
        "            }else{\n"
        "                let mode:i32=e45_mod(episode/(E45_RESOURCES*per_cell),E45_MODES);\n"
        "                if(mode==0 || mode==1){ kinds[episode]=E51AH_KIND_NEITHER_NU; neither_nu.*=neither_nu.*+1;\n"
        "                }else{ kinds[episode]=E51AH_KIND_NEITHER_KNOWN; neither_known.*=neither_known.*+1; }\n"
        "            }\n"
        "        }\n"
        "        episode=episode+1;\n"
        "    }\n"
        "}\n\n"
    )
    if text.count(legacy_classifier) != 1:
        raise SystemExit(
            f"E51AH legacy evaluator classifier count: {text.count(legacy_classifier)}"
        )
    text = text.replace(legacy_classifier, "", 1)
    return text


def transform_run_prefix(text: str) -> str:
    text = transform_namespace(text)
    replacements = {
        "experiment_schema,tnn_r32_e51ah_trajectory_critical_candidate_residual_v1":
            "experiment_schema,tnn_r32_e51ah_grounded_preservation_replay_v1",
        "claim_boundary,native_candidate_value_capacity_discriminator_not_promotion":
            "claim_boundary,grounded_preservation_replay_discriminator_not_promotion",
        "residual_features,32_evaluator_blind_terminal_features":
            "residual_features,32_evaluator_blind_terminal_features_with_grounded_replay_support",
        "deployment_policy,frozen_e51ac_score_max_with_residual_corrected_candidate_values":
            "deployment_policy,frozen_union_control_and_preregistered_replay_residual_arms",
    }
    for old, new in replacements.items():
        if text.count(old) != 1:
            raise SystemExit(f"E51AH run anchor count for {old!r}: {text.count(old)}")
        text = text.replace(old, new, 1)
    return text


base_path = Path(".scratch/e51ad/tnn_r32_e51ad_trajectory_critical_router.zag")
if not base_path.exists():
    raise SystemExit(f"missing frozen E51AD base: {base_path}")
if hashlib.sha256(base_path.read_bytes()).hexdigest() != PARENT_ASSEMBLED_SHA256:
    raise SystemExit("E51AH complete assembled E51AD parent identity failure")
src = base_path.read_text()

support = transform_support(
    "".join(
        Path(path).read_text()
        for path in (
            "Research/R32_E51AE_NATIVE/01a_contract_selection.zagfrag",
            "Research/R32_E51AE_NATIVE/01b_objective_fit.zagfrag",
        )
    )
)
replay_helpers = Path(
    "Research/R32_E51AH_NATIVE/01d_preservation_replay.zagfrag"
).read_text()
run_prefix = transform_run_prefix(
    Path("Research/R32_E51AE_NATIVE/02a_run_direct.zagfrag").read_text()
)
run_tail = Path(
    "Research/R32_E51AH_NATIVE/02b_run_preservation_replay.zagfrag"
).read_text()
frag = support + replay_helpers + run_prefix + run_tail

required_once = (
    "const E51AH_STAGE_DEV:i32=108;",
    "const E51AH_STAGE_VALIDATION:i32=109;",
    "const E51AH_STAGE_CONFIRM:i32=110;",
    "const E51AH_PREVIOUS_STAGE:i32=107;",
    "const E51AH_ARMS:i32=6;",
    "fn e51ah_select_preservation_replay(\n",
    "fn e51ah_repeat_critical(\n",
    "fn e51ah_eval_partition(\n",
    "fn e51ah_run(\n",
    "fn e51ah_select_replay_arm(",
    "fn e51ah_validation_class(",
    "PRESERVATION_REPLAY_DEVELOPMENT_FAILURE",
    "TNN_R32_E51AH_EXECUTION_COMPLETE=1",
)
for marker in required_once:
    if frag.count(marker) != 1:
        raise SystemExit(f"E51AH marker count for {marker!r}: {frag.count(marker)}")

for forbidden in (
    "E51AE_",
    "e51ae_",
    "const E51AH_STAGE_DEV:i32=97;",
    "const E51AH_STAGE_VALIDATION:i32=98;",
    "const E51AH_STAGE_CONFIRM:i32=99;",
    "const E51AH_PREVIOUS_STAGE:i32=96;",
    "const E51AH_ARM_GLOBAL:i32=1;",
    "const E51AH_ARM_LOCAL_96:i32=2;",
    "const E51AH_ARM_LOCAL_384:i32=3;",
    "const E51AH_ARM_DIRECT_ORACLE:i32=4;",
    "fn e51ah_dose(",
    "fn e51ah_classify_kinds(",
):
    if forbidden in frag:
        raise SystemExit(f"E51AH forbidden stale marker present: {forbidden}")

if frag.count("fn e51ah_eval_partition(\n") != 1:
    raise SystemExit("E51AH evaluation helper duplication")
if replay_helpers.count("fn e51ah_classify_grounded_kinds(\n") != 1:
    raise SystemExit("E51AH grounded classifier definition missing or duplicated")
if run_tail.count("e51ah_classify_grounded_kinds(\n") != 1:
    raise SystemExit("E51AH grounded classifier call missing or duplicated")
if "e51ah_development_open_gate" not in run_tail:
    raise SystemExit("E51AH development opening gate missing")
if "e51ah_classify_kinds(base_kinds" in run_tail:
    raise SystemExit("E51AH run tail uses evaluator-mode kind classification")
if "mode==0 || mode==1" in run_tail:
    raise SystemExit("E51AH development tail contains evaluator mode classification")
if run_tail.count("if(arm==selected_replay_arm)") != 3:
    raise SystemExit("E51AH outcome branches must use the pre-validation selected arm")
oracle_block = replay_helpers.split("if(arm==E51AH_ARM_ORACLE){", 1)[1].split("}else{", 1)[0]
if "success=1;" in oracle_block or "success=e51ac_choice_success(" not in oracle_block:
    raise SystemExit("E51AH oracle must score its action through the grounded evaluator")
if run_tail.find("e51ah_development_open_gate") > run_tail.find(
    "E51AH_STAGE_VALIDATION"
):
    raise SystemExit("E51AH validation appears before development opening gate")

old_injection = Path("Research/R32_E51AD_NATIVE/03_main_injection.zagfrag").read_text()
new_injection = Path("Research/R32_E51AH_NATIVE/03_main_injection.zagfrag").read_text()
function_marker = "fn e51y_run(\n"
if src.count(function_marker) != 1:
    raise SystemExit(f"E51AH function insertion marker count {src.count(function_marker)}")
if src.count(old_injection) != 1:
    raise SystemExit(f"E51AH main injection anchor count {src.count(old_injection)}")
src = src.replace(function_marker, frag + "\n\n" + function_marker, 1)
src = src.replace(old_injection, new_injection, 1)

scratch = Path(".scratch/e51ah")
scratch.mkdir(parents=True, exist_ok=True)
(scratch / "E51AH_FRAGMENT.zag").write_text(frag)
(scratch / "tnn_r32_e51ah_grounded_preservation_replay.zag").write_text(src)
core = Path("Research/tnn_r32_e45_investigation_core.zag")
if hashlib.sha256(core.read_bytes()).hexdigest() != CORE_SHA256:
    raise SystemExit("E51AH imported core identity failure")
(scratch / "tnn_r32_e45_investigation_core.zag").write_bytes(core.read_bytes())
(scratch / "TRANSITIVE_SOURCE_MANIFEST.json").write_text(json.dumps({
    "parent_source_revision": PARENT_SOURCE_REV,
    "assembled_parent_sha256": PARENT_ASSEMBLED_SHA256,
    "core_sha256": CORE_SHA256,
    "files": parent_manifest,
}, indent=2) + "\n")
for entry in parent_manifest:
    dest = scratch / "transitive_source" / entry["path"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(Path(entry["path"]).read_bytes())
(scratch / "SOURCE_PIN_GATE.txt").write_text("1\n")
