# Harvest Ready

Compares bounded crop observations with grower-defined readiness signs and records an advisory signal while leaving every harvest decision to the grower.

## Why it is an Intelligent Contract

Produce a readiness mask and READY, WATCH, or NOT_READY advisory for one declared observation round. GenLayer validators independently replay that semantic judgment before it becomes shared state. Sign freezing, the three-round cap, round history, grower authorization, and the grower's HARVEST or WAIT decision are deterministic.

## Reusable deployment model

Deploy once per crop lot or growing batch. A fresh deployment reuses the same reviewed logic with different lot facts, signs, and observations.

A completed deployment is an auditable record and is not reset or silently repurposed. Reuse means deploying the same reviewed source with new constructor data.

## Roles and workflow

The deployer is the grower and controls sign setup, observation rounds, and the final HARVEST or WAIT decision.

State path: `SETTING_SIGNS → AWAITING_OBSERVATION → ASSESSING_OBSERVATION → GROWER_DECISION → AWAITING_OBSERVATION or COMPLETE`

## Evidence boundary

The stored lot label and context, advisory boundary, ordered readiness signs, round label, and grower's declared observation. No sensor, weather service, or farm record is fetched.

## Core invariants

- At least two grower-defined signs freeze before monitoring begins.
- Only the grower can record an observation or make the harvest decision.
- Every round retains its mask, signal, decision, and note.
- The AI signal cannot harvest a crop or override the grower.

## Public interface

Write methods: `add_readiness_sign, assess_current_observation, begin_monitoring, record_grower_decision, record_observation`

View methods: `get_policy, get_round, get_state`

`get_policy` exposes the machine-readable operating boundary and confirms that this contract never custodies funds.

## Verification

Pinned GenVM runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

```powershell
python -m pip install -r requirements.txt
genvm-lint check contracts/harvest_ready.py
genvm-lint typecheck contracts/harvest_ready.py
pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
gltest tests/integration/test_glsim_consensus.py --network localnet -q
```

The StudioNet smoke test is opt-in and uses three disposable Mimi-only accounts protected outside the workspace. It asserts finalized successful execution and reads committed state with `LATEST_FINAL`.

## Final StudioNet proof

- Contract: https://explorer-studio.genlayer.com/address/0x8573E3C71298945868cEcfb784E3F9dC38AB082C
- Studio import: https://studio.genlayer.com/?import-contract=0x8573E3C71298945868cEcfb784E3F9dC38AB082C
- Deployment transaction: https://explorer-studio.genlayer.com/tx/0xde1188b322ca64547a55bb41058275ee84018f53b25e487e2284b67b998a393b
- Intelligent transaction: https://explorer-studio.genlayer.com/tx/0xc0cbd937fa44006de511dd0cd0c13a820b9574d9993ba2e0585e61277b7e59bf
- Observed committed state: `{"readiness_mask":"11","signal":"READY"}`
- Audited source SHA-256: `3d8837f0a159fc9872713ff5141157627b3ff6a50245b29c80f20eca5fcbef49`

## Limitations

- Observations are self-declared and are not verified against sensors or images.
- The result is not agronomy, food-safety, weather, or regulatory advice.
- A READY signal only means the stored observation supports the frozen signs.

## Repository map

- `contracts/harvest_ready.py` — Intelligent Contract source
- `tests/direct` — hardened leader/validator and lifecycle tests
- `tests/integration/test_glsim_consensus.py` — five-validator simulator flow
- `tests/integration/test_studionet_smoke.py` — live opt-in proof
- `deployments/studionet.json` — source-bound public deployment evidence
- `ARCHITECTURE.md`, `SOURCE_POLICY.md`, `SECURITY.md`, `AUDIT.md` — reviewer material

License: MIT.
