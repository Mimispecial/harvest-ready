from pathlib import Path
import json

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address

PROMPT = "Compare one declared crop observation"


def context():
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {PROMPT: json.dumps({"readiness_mask": "11", "signal": "READY"})}})
    return {"validators": [validator.to_dict() for validator in validators]}


def ok(receipt):
    assert tx_execution_succeeded(receipt)


def test_five_validator_advisory_harvest_round():
    grower_account = create_accounts(1)[0]
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "harvest_ready.py")
    deployed = factory.deploy_contract_tx(args=["North bed tomato lot", "A small garden tomato lot tracked for a community cooking event.", "Use only visible and measured observations; missing signs remain unsupported and the signal is advisory, not food-safety or agronomy advice."], account=grower_account, wait_transaction_status=TransactionStatus.FINALIZED)
    ok(deployed)
    contract = factory.build_contract(extract_contract_address(deployed), account=grower_account)
    ok(contract.add_readiness_sign(args=["COLOR", "Most listed fruit has the target cultivar's even mature-red surface color."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(contract.add_readiness_sign(args=["FIRMNESS", "The observation describes firm fruit with slight give and no split skin."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(contract.begin_monitoring(args=[]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(contract.record_observation(args=["Morning round one", "The grower counted twelve evenly red tomatoes; each remained firm with slight give, and no split skins were observed."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    ok(contract.assess_current_observation(args=[]).transact(transaction_context=context(), wait_transaction_status=TransactionStatus.FINALIZED))
    ok(contract.record_grower_decision(args=["HARVEST", "The grower independently reviewed the field record and chose to harvest this lot today."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert contract.get_state(args=[]).call()["final_decision"] == "HARVEST"
