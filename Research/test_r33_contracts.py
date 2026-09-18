"""Synthetic, in-memory authoring tests. Not TNN learning or sensor evidence."""
from __future__ import annotations

import copy
import unittest

from r33_validate import (
    ContractError, RESEARCH, check_finite, digest, load_json, parse_b000_output,
    schema_check, validate_b000_source, validate_batch, validate_record,
    validate_registries, validate_reviews, validate_schema_definition, validate_pins,
)


class R33Contracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(RESEARCH / "R33_TELEMETRY_SCHEMA.json")
        cls.state = load_json(RESEARCH / "R33_CURRENT_STATE.json")
        cls.registry = load_json(RESEARCH / "R33_EXPERIMENT_REGISTRY.json")
        cls.consumed = load_json(RESEARCH / "R33_CONSUMED_EVIDENCE_REGISTRY.json")
        cls.reviews = load_json(RESEARCH / "R33_INDEPENDENT_REVIEWS.json")
        cls.audit_config = load_json(RESEARCH / "R33_B000_CONFIG.json")
        cls.audit_source = (RESEARCH / "R33_B000_SOURCE.zag").read_text()
        cls.original_source = (RESEARCH / "tnn_r32_epistemic_chunking.zag").read_text()

    def blank_snapshot(self) -> dict:
        missing = {"status": "NOT_MEASURED", "value": None, "reason": "synthetic authoring fixture"}
        return {
            "record_type": "COMPETENCY_SNAPSHOT", "schema_version": 1,
            "snapshot_id": "fixture:snapshot", "experiment_id": "fixture:only",
            "brain_id": "fixture:not-a-brain", "branch_id": "fixture:branch",
            "competency_id": "fixture:competency", "checkpoint_sha256": "0" * 64,
            "aggregation_version": "fixture:v1", "visibility": "EVALUATOR_ONLY",
            "metrics": {key: copy.deepcopy(missing) for key in self.schema["$defs"]["competency_metrics"]["required"]},
            "resources": {key: copy.deepcopy(missing) for key in self.schema["$defs"]["resources"]["required"]},
            "source_event_ids": [], "qualification_status": "NOT_ASSESSED",
        }

    def blank_event(self) -> dict:
        snapshot = self.blank_snapshot()
        return {
            "record_type": "CAUSAL_EVENT", "schema_version": 1,
            "event_id": "fixture:event", "ordinal": 0, "clock_domain": "fixture:clock", "timestamp_ns": 0,
            "experiment_id": "fixture:only", "brain_id": "fixture:not-a-brain", "branch_id": "fixture:branch",
            "competency_ids": [], "event_kind": "ERROR", "visibility": "SUPERVISOR_ONLY",
            "actor": {"actor_id": "fixture:supervisor", "kind": "PROTECTED_SUPERVISOR"},
            "authority": {"policy_sha256": "0" * 64, "grant_id": None, "grant_status": "NOT_APPLICABLE_AUDIT", "effective_milestone": None, "supervisor_epoch": 0},
            "parent_event_ids": [], "experience_id": None, "payload_sha256": None,
            "checkpoint_before_sha256": "0" * 64, "checkpoint_after_sha256": "0" * 64,
            "causal_refs": {key: [] for key in self.schema["$defs"]["event"]["properties"]["causal_refs"]["required"]},
            "mutations": [],
            "assistance": {"stage": "NOT_APPLICABLE", "assisted": False, "requested_by_learner": False, "input_event_ids": [], "human_interventions": 0, "software_aid_interventions": 0},
            "resources": snapshot["resources"],
            "coverage": {"status": "INCOMPLETE", "missing_fields": ["fixture:unmeasured"], "dropped_events": 0, "claim_scope": "authoring test only"},
        }

    def test_valid_unmeasured_snapshot(self) -> None:
        validate_record(self.blank_snapshot(), self.schema)

    def test_valid_scoped_event(self) -> None:
        validate_record(self.blank_event(), self.schema)

    def test_missing_metric_rejected(self) -> None:
        record = self.blank_snapshot()
        del record["metrics"]["delayed_retention"]
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_unmeasured_zero_rejected(self) -> None:
        record = self.blank_snapshot()
        record["metrics"]["fresh_performance"]["value"] = 0
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_unmeasured_without_reason_rejected(self) -> None:
        record = self.blank_snapshot()
        del record["metrics"]["fresh_performance"]["reason"]
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_measured_without_evidence_rejected(self) -> None:
        record = self.blank_snapshot()
        record["metrics"]["fresh_performance"] = {"status": "MEASURED", "value": 1, "unit": "fraction", "method": "fixture", "evidence_event_ids": []}
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_real_zero_measurement_allowed(self) -> None:
        record = self.blank_snapshot()
        record["metrics"]["fresh_performance"] = {"status": "MEASURED", "value": 0, "unit": "fraction", "method": "fixture", "evidence_event_ids": ["fixture:e"], "numerator": 0, "denominator": 5, "sample_unit": "independent_fixture"}
        validate_record(record, self.schema)

    def test_zero_denominator_rejected(self) -> None:
        record = self.blank_snapshot()
        record["metrics"]["fresh_performance"] = {"status": "MEASURED", "value": 0, "unit": "fraction", "method": "fixture", "evidence_event_ids": ["fixture:e"], "denominator": 0}
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_unmeasured_qualification_rejected(self) -> None:
        record = self.blank_snapshot()
        record["qualification_status"] = "PASSED_BOUNDED_CONTRACT"
        record["source_event_ids"] = ["fixture:e"]
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_snapshot_cannot_enter_learner_stream(self) -> None:
        record = self.blank_snapshot()
        record["visibility"] = "LEARNER_ADMITTED"
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_learner_self_grant_rejected(self) -> None:
        record = self.blank_event()
        record["event_kind"] = "GRANT"
        record["actor"]["kind"] = "LEARNER"
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_ungranted_milestone_rejected(self) -> None:
        record = self.blank_event()
        record["authority"]["effective_milestone"] = "M3"
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_teacher_requires_human_delegation(self) -> None:
        record = self.blank_event()
        record["actor"]["kind"] = "SOFTWARE_TEACHING_AID"
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_silent_trace_gap_rejected(self) -> None:
        record = self.blank_event()
        record["coverage"].update(status="COMPLETE_WITHIN_DECLARED_SCOPE", missing_fields=[], dropped_events=1)
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_hidden_help_rejected(self) -> None:
        record = self.blank_event()
        record["assistance"]["human_interventions"] = 1
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_unattributed_update_rejected(self) -> None:
        record = self.blank_event()
        record["event_kind"] = "UPDATE"
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_self_parent_rejected(self) -> None:
        record = self.blank_event()
        record["parent_event_ids"] = [record["event_id"]]
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_assessment_visibility_rejected(self) -> None:
        record = self.blank_event()
        record.update(event_kind="ASSESSMENT", visibility="LEARNER_ADMITTED")
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_boolean_is_not_integer_counter(self) -> None:
        record = self.blank_event()
        record["ordinal"] = True
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_extra_rationale_field_rejected(self) -> None:
        record = self.blank_event()
        record["invented_reason"] = "I felt certain"
        with self.assertRaises(ContractError): validate_record(record, self.schema)

    def test_unknown_schema_keyword_rejected(self) -> None:
        with self.assertRaises(ContractError): schema_check(3, {"type": "number", "unsupportedRule": True}, {})

    def test_current_registries(self) -> None:
        validate_registries(self.state, self.registry, self.consumed)

    def test_false_promotion_rejected(self) -> None:
        state = copy.deepcopy(self.state)
        state["promotion_allowed"] = True
        with self.assertRaises(ContractError): validate_registries(state, self.registry, self.consumed)

    def test_duplicate_experiment_rejected(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["proposed_batches"].append(copy.deepcopy(registry["proposed_batches"][0]))
        with self.assertRaises(ContractError): validate_registries(self.state, registry, self.consumed)

    def test_old_stage_reuse_rejected(self) -> None:
        consumed = copy.deepcopy(self.consumed)
        consumed["new_scientific_allocations"] = [{"stages": [119]}]
        with self.assertRaises(ContractError): validate_registries(self.state, self.registry, consumed)

    def test_nominal_new_stage_insufficient(self) -> None:
        consumed = copy.deepcopy(self.consumed)
        consumed["new_scientific_allocations"] = [{"stages": [143]}]
        with self.assertRaises(ContractError): validate_registries(self.state, self.registry, consumed)

    def test_capacity_design_arithmetic(self) -> None:
        expected = [(8, 538, 2152), (32, 2146, 8584), (128, 8578, 34312), (512, 34306, 137224), (2048, 137218, 548872)]
        for cells, parameters, byte_count in expected:
            self.assertEqual(67 * cells + 2, parameters)
            self.assertEqual(4 * parameters, byte_count)

    def synthetic_audit_output(self) -> str:
        # Parser fixtures only: never represent this generated text as native output.
        rows = [f"M,{key},{value}" for key, value in self.audit_config["expected_metrics"].items()]
        for key, values in self.audit_config["expected_vectors"].items():
            rows.extend(f"V,{key},{i},{value}" for i, value in enumerate(values))
        return "\n".join(rows) + "\n"

    def test_review_inventory(self) -> None:
        validate_reviews(self.reviews)

    def test_missing_safety_review_rejected(self) -> None:
        reviews = copy.deepcopy(self.reviews)
        reviews["reviews"] = [r for r in reviews["reviews"] if r["role"] != "safety"]
        with self.assertRaises(ContractError): validate_reviews(reviews)

    def test_unintegrated_reviews_rejected(self) -> None:
        reviews = copy.deepcopy(self.reviews)
        reviews["status"] = "IN_PROGRESS"
        with self.assertRaises(ContractError): validate_reviews(reviews)

    def test_same_reviewer_twice_rejected(self) -> None:
        reviews = copy.deepcopy(self.reviews)
        reviews["reviews"][1]["agent_id"] = reviews["reviews"][0]["agent_id"]
        with self.assertRaises(ContractError): validate_reviews(reviews)

    def test_missing_review_disposition_rejected(self) -> None:
        reviews = copy.deepcopy(self.reviews)
        reviews["reviews"][0]["disposition"] = ""
        with self.assertRaises(ContractError): validate_reviews(reviews)

    def test_exact_helper_copy(self) -> None:
        validate_b000_source(self.audit_source, self.original_source)

    def test_stray_reconstruction_assignment_rejected(self) -> None:
        changed = self.audit_source.replace("out_seq[n]=c_data[", "out_seq[n]=-1;out_seq[n]=c_data[", 1)
        self.assertNotEqual(changed, self.audit_source)
        with self.assertRaises(ContractError): validate_b000_source(changed, self.original_source)

    def test_unexpected_source_import_rejected(self) -> None:
        changed = '@import("prior_scientific_main.zag")\n' + self.audit_source
        with self.assertRaises(ContractError): validate_b000_source(changed, self.original_source)

    def test_unexpected_native_function_rejected(self) -> None:
        changed = self.audit_source + "\nfn unknown_learning() i32 {return 0;}\n"
        with self.assertRaises(ContractError): validate_b000_source(changed, self.original_source)

    def test_trace_constant_change_rejected(self) -> None:
        changed = self.audit_source.replace("const TRACE_CAP:i32=8192;", "const TRACE_CAP:i32=8193;")
        with self.assertRaises(ContractError): validate_b000_source(changed, self.original_source)

    def test_synthetic_parser_fixture(self) -> None:
        result = parse_b000_output(self.synthetic_audit_output(), self.audit_config)
        self.assertEqual(result["status"], "EXPECTED_WITNESSES_MATCHED")
        self.assertIs(result["sensory_or_authority_contract_satisfied"], False)

    def test_duplicate_audit_metric_rejected(self) -> None:
        text = self.synthetic_audit_output() + "M,audit.completed,1\n"
        with self.assertRaises(ContractError): parse_b000_output(text, self.audit_config)

    def test_missing_audit_vector_element_rejected(self) -> None:
        text = self.synthetic_audit_output().replace("V,visual.raw_a,0,0\n", "")
        with self.assertRaises(ContractError): parse_b000_output(text, self.audit_config)

    def test_duplicate_audit_vector_element_rejected(self) -> None:
        text = self.synthetic_audit_output() + "V,visual.raw_a,0,0\n"
        with self.assertRaises(ContractError): parse_b000_output(text, self.audit_config)

    def test_unknown_audit_metric_rejected(self) -> None:
        text = self.synthetic_audit_output() + "M,unexpected,1\n"
        with self.assertRaises(ContractError): parse_b000_output(text, self.audit_config)

    def test_audit_mismatch_not_hidden(self) -> None:
        text = self.synthetic_audit_output().replace("M,audio.unsampled_distance,0\n", "M,audio.unsampled_distance,99\n")
        result = parse_b000_output(text, self.audit_config)
        self.assertEqual(result["status"], "OBSERVATION_MISMATCH_REQUIRES_ANALYSIS")
        self.assertEqual(result["mismatched_keys"], ["audio.unsampled_distance"])

    def test_audit_incomplete_marker_rejected(self) -> None:
        text = self.synthetic_audit_output().replace("M,audit.completed,1\n", "M,audit.completed,0\n")
        with self.assertRaises(ContractError): parse_b000_output(text, self.audit_config)

    def test_noninteger_audit_field_rejected(self) -> None:
        text = self.synthetic_audit_output().replace("M,audio.zero_distance,0\n", "M,audio.zero_distance,NaN\n")
        with self.assertRaises(ContractError): parse_b000_output(text, self.audit_config)

    def test_unvisited_schema_keyword_rejected(self) -> None:
        schema = copy.deepcopy(self.schema)
        schema["$defs"]["unused"] = {"type": "number", "unsupportedRule": 1}
        with self.assertRaises(ContractError): validate_schema_definition(schema, schema)

    def test_nonlocal_schema_reference_rejected(self) -> None:
        schema = {"$ref": "https://invalid.example/schema"}
        with self.assertRaises(ContractError): validate_schema_definition(schema, schema)

    def test_opaque_payload_nan_rejected(self) -> None:
        with self.assertRaises(ContractError): check_finite({"payload": [float("nan")]})

    def test_missing_preregistration_pins_rejected(self) -> None:
        batch = {"id": "R33-B000", "kind": "ISOLATED_NATIVE_BOUNDARY_AUDIT",
                 "status": "PREREGISTERED_NOT_EXECUTED", "training": False,
                 "canonical_mutation": False, "scientific_world_allocation": False,
                 "learner_authority_granted": False, "source_pins": []}
        with self.assertRaises(ContractError): validate_batch(batch, self.reviews)

    def test_audit_cannot_grant_learner_authority(self) -> None:
        batch = {"id": "R33-B000", "kind": "ISOLATED_NATIVE_BOUNDARY_AUDIT",
                 "status": "PREREGISTERED_NOT_EXECUTED", "training": False,
                 "canonical_mutation": False, "scientific_world_allocation": False,
                 "learner_authority_granted": True, "source_pins": []}
        with self.assertRaises(ContractError): validate_batch(batch, self.reviews)

    def test_matching_source_pin(self) -> None:
        validate_pins([{"path": "Research/R33_B000_SOURCE.zag", "sha256": digest(RESEARCH / "R33_B000_SOURCE.zag")}])

    def test_drifted_source_pin_rejected(self) -> None:
        with self.assertRaises(ContractError):
            validate_pins([{"path": "Research/R33_B000_SOURCE.zag", "sha256": "0" * 64}])

    def test_duplicate_source_pin_rejected(self) -> None:
        pin = {"path": "Research/R33_B000_SOURCE.zag", "sha256": digest(RESEARCH / "R33_B000_SOURCE.zag")}
        with self.assertRaises(ContractError): validate_pins([pin, pin])

    def test_escaping_source_pin_rejected(self) -> None:
        with self.assertRaises(ContractError): validate_pins([{"path": "../out-of-scope", "sha256": "0" * 64}])

    def test_invalid_hash_format_rejected(self) -> None:
        with self.assertRaises(ContractError): validate_pins([{"path": "Research/R33_B000_SOURCE.zag", "sha256": "not-a-hash"}])


if __name__ == "__main__":
    unittest.main(verbosity=2)
