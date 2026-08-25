import json
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address


def ok(receipt):
    assert tx_execution_succeeded(receipt)
    assert receipt.get("status_name") == TransactionStatus.FINALIZED.value
    assert receipt.get("result_name") in (None, "AGREE", "MAJORITY_AGREE")
    assert receipt.get("tx_execution_result_name") in (None, "FINISHED_WITH_RETURN")
    return receipt


@pytest.mark.integration
def test_studionet_harvest_observation(default_account):
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "harvest_ready.py")
    deployed = ok(factory.deploy_contract_tx(args=["North bed tomato lot", "A small garden tomato lot tracked for a community cooking event.", "Use only visible and measured observations; missing signs remain unsupported and the signal is advisory, not food-safety or agronomy advice."], account=default_account, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    contract = factory.build_contract(address, account=default_account)
    ok(contract.add_readiness_sign(args=["COLOR", "Most listed fruit has the target cultivar's even mature-red surface color."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(contract.add_readiness_sign(args=["FIRMNESS", "The observation describes firm fruit with slight give and no split skin."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(contract.begin_monitoring(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(contract.record_observation(args=["Morning round one", "The grower counted twelve evenly red tomatoes; each remained firm with slight give, and no split skins were observed."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = ok(contract.assess_current_observation(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    round_state = contract.get_round(args=[1]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert round_state["signal"] in ("READY", "WATCH", "NOT_READY")
    observed = {"readiness_mask": round_state["readiness_mask"], "signal": round_state["signal"]}
    print("STUDIONET_RECORD=" + json.dumps({"address": address, "deploy_tx": deployed["hash"], "intelligent_tx": intelligent["hash"], "observed": observed}, sort_keys=True))
