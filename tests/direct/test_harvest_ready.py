from pathlib import Path
import json

CONTRACT = Path(__file__).resolve().parents[2] / "contracts" / "harvest_ready.py"
SDK = "v0.2.16"
PROMPT = "Compare one declared crop observation"
STANDARD = "Use only the grower's visible and measured observations. Missing or ambiguous signs remain unsupported, and the signal is advisory rather than a safety or agronomy instruction."


def monitored(vm, direct_deploy, grower):
    vm.sender = grower
    contract = direct_deploy(str(CONTRACT), "North bed tomato lot", "A small garden tomato lot tracked for a community cooking event.", STANDARD, sdk_version=SDK)
    contract.add_readiness_sign("COLOR", "Most listed fruit has the target cultivar's even mature-red surface color.")
    contract.add_readiness_sign("FIRMNESS", "The observation describes firm fruit with a slight give and no split skin.")
    contract.begin_monitoring()
    return contract


def observe(contract, label="Morning round one"):
    contract.record_observation(label, "The grower counted twelve evenly red tomatoes; each remained firm with a slight give, and no split skins were observed.")


def test_advisory_assessment_then_grower_harvest(direct_vm, direct_deploy, direct_alice):
    contract = monitored(direct_vm, direct_deploy, direct_alice)
    observe(contract)
    direct_vm.mock_llm(PROMPT, json.dumps({"readiness_mask": "11", "signal": "READY"}))
    contract.assess_current_observation()
    leader = direct_vm._captured_validators[-1][0]
    assert direct_vm.run_validator(leader_result=leader) is True
    contract.record_grower_decision("HARVEST", "The grower reviewed the field record and independently chose to harvest this lot today.")
    assert contract.get_state()["final_decision"] == "HARVEST"
    assert contract.get_round(1)["signal"] == "READY"


def test_wait_opens_a_new_bounded_observation_round(direct_vm, direct_deploy, direct_alice):
    contract = monitored(direct_vm, direct_deploy, direct_alice)
    observe(contract)
    direct_vm.mock_llm(PROMPT, json.dumps({"readiness_mask": "10", "signal": "WATCH"}))
    contract.assess_current_observation()
    contract.record_grower_decision("WAIT", "The grower chose to wait and record a new field observation after the firmness sign becomes clearer.")
    assert contract.get_state()["status"] == "AWAITING_OBSERVATION"
    contract.record_observation("Morning round two", "The lot now has fifteen evenly red fruits; all listed fruit is firm with slight give and has no split skin.")
    assert contract.get_state()["current_round"] == 2


def test_only_grower_records_and_bad_signal_fails_closed(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = monitored(direct_vm, direct_deploy, direct_alice)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only_grower"):
        observe(contract)
    direct_vm.sender = direct_alice
    observe(contract)
    direct_vm.mock_llm(PROMPT, json.dumps({"readiness_mask": "11", "signal": "CERTAIN"}))
    with direct_vm.expect_revert("invalid_signal"):
        contract.assess_current_observation()
    assert contract.get_state()["status"] == "ASSESSING_OBSERVATION"
