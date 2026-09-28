"""External lifecycle tests plus the frozen authoring suite on original inputs."""
import copy
import unittest

import test_r33_contracts as historical
from r33_validate import RESEARCH, ContractError, load_json
from r33_execution_validate import RUN, lifecycle


class FrozenAuthoringContracts(historical.R33Contracts):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if (RUN / "REGISTRATION_SNAPSHOT.json").exists():
            old = load_json(RUN / "REGISTRATION_SNAPSHOT.json")
            cls.state = old["R33_CURRENT_STATE.json"]
            cls.registry = old["R33_EXPERIMENT_REGISTRY.json"]
            cls.consumed = old["R33_CONSUMED_EVIDENCE_REGISTRY.json"]


class ExecutionContracts(unittest.TestCase):
    def fixture(self):
        if (RUN / "REGISTRATION_SNAPSHOT.json").exists():
            old = load_json(RUN / "REGISTRATION_SNAPSHOT.json")
            state, registry, consumed = (old[k] for k in ("R33_CURRENT_STATE.json", "R33_EXPERIMENT_REGISTRY.json",
                                                        "R33_CONSUMED_EVIDENCE_REGISTRY.json"))
        else:
            state, registry, consumed = (load_json(RESEARCH / k) for k in (
                "R33_CURRENT_STATE.json", "R33_EXPERIMENT_REGISTRY.json", "R33_CONSUMED_EVIDENCE_REGISTRY.json"))
        execution = load_json(RESEARCH / "R33_B000_EXECUTION_STATUS.json")
        execution.update(status="PREREGISTERED_NOT_EXECUTED", primary_execution_attempts=0,
                         native_fixture_exposures=0, observed_witness_results=None)
        return [copy.deepcopy(state), copy.deepcopy(registry), copy.deepcopy(consumed), execution, None]

    def completed(self):
        values = self.fixture()
        state, registry, consumed, execution, _ = values
        state["r33_native_experiments_executed"] = 1
        registry["experiments"][0].update(status="COMPLETED", primary_attempts=1)
        consumed["diagnostic_fixtures"][0]["primary_executions"] = 1
        parsed = {"status": "EXPECTED_WITNESSES_MATCHED", "mismatched_keys": []}
        execution.update(status="COMPLETED", primary_execution_attempts=1, native_fixture_exposures=1,
                         observed_witness_results=parsed)
        values[4] = {"fixture_exposures": 1, "status": "EXPECTED_WITNESSES_MATCHED", "errors": [],
                     "canonical_mutated": False, "learner_authority_granted": False,
                     "sensory_qualification": False, "promotion": False, "parsed_output": parsed,
                     "runtime": {"native_process_started": True, "exit_code": 0, "termination_reason": None,
                                 "wall_seconds": 0.01, "cpu_seconds": 0.01, "peak_rss_bytes": 1024,
                                 "stdout_bytes": 100, "stderr_bytes": 0}}
        return values

    def test_pre_execution_valid(self): lifecycle(*self.fixture())
    def test_completed_valid(self): lifecycle(*self.completed())

    def test_invented_result_rejected(self):
        v = self.fixture(); v[4] = {}
        with self.assertRaises(ContractError): lifecycle(*v)

    def test_master_plan_false_completion_rejected(self):
        v = self.completed(); v[0]["all_r33_research_complete"] = True
        with self.assertRaises(ContractError): lifecycle(*v)

    def test_repeated_primary_rejected(self):
        v = self.completed(); v[1]["experiments"][0]["primary_attempts"] = 2
        v[3]["primary_execution_attempts"] = 2
        with self.assertRaises(ContractError): lifecycle(*v)

    def test_unrecorded_exposure_rejected(self):
        v = self.completed(); v[2]["diagnostic_fixtures"][0]["primary_executions"] = 0
        with self.assertRaises(ContractError): lifecycle(*v)

    def test_sensor_claim_rejected(self):
        v = self.completed(); v[4]["sensory_qualification"] = True
        with self.assertRaises(ContractError): lifecycle(*v)

    def test_authority_claim_rejected(self):
        v = self.completed(); v[0]["scientifically_qualified_r33_milestone"] = "M0"
        with self.assertRaises(ContractError): lifecycle(*v)

    def test_runtime_failure_rejected(self):
        v = self.completed(); v[4]["runtime"]["exit_code"] = 1
        with self.assertRaises(ContractError): lifecycle(*v)

    def test_missing_result_rejected(self):
        v = self.completed(); v[4] = None
        with self.assertRaises(ContractError): lifecycle(*v)

    def test_memory_overrun_rejected(self):
        v = self.completed(); v[4]["runtime"]["peak_rss_bytes"] = 268435457
        with self.assertRaises(ContractError): lifecycle(*v)

    def test_missing_memory_measure_rejected(self):
        v = self.completed(); v[4]["runtime"]["peak_rss_bytes"] = None
        with self.assertRaises(ContractError): lifecycle(*v)

    def test_wall_overrun_rejected(self):
        v = self.completed(); v[4]["runtime"]["wall_seconds"] = 31
        with self.assertRaises(ContractError): lifecycle(*v)

    def test_freshness_inflation_rejected(self):
        v = self.completed(); v[2]["diagnostic_fixtures"][0]["fresh_generalization_evidence"] = True
        with self.assertRaises(ContractError): lifecycle(*v)

    def test_historical_guard_changed_rejected(self):
        v = self.completed(); v[2]["legacy_guard"]["guarded_stage_range"] = [1, 118]
        with self.assertRaises(ContractError): lifecycle(*v)

    def test_scope_expansion_rejected(self):
        v = self.completed(); v[1]["experiments"][0]["training"] = True
        with self.assertRaises(ContractError): lifecycle(*v)


if __name__ == "__main__":
    unittest.main(verbosity=2)
