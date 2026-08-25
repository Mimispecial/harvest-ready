# Architecture

## Deployment boundary

Deploy once per crop lot or growing batch. A fresh deployment reuses the same reviewed logic with different lot facts, signs, and observations.

Constructor data establishes the deployment subject and fixed role boundary. Later writes add only the bounded records permitted by the lifecycle; a completed instance cannot be reopened.

## Participants

The deployer is the grower and controls sign setup, observation rounds, and the final HARVEST or WAIT decision.

Addresses are normalized before authorization comparisons. Role checks and lifecycle gates execute before semantic assessment.

## State machine

`SETTING_SIGNS → AWAITING_OBSERVATION → ASSESSING_OBSERVATION → GROWER_DECISION → AWAITING_OBSERVATION or COMPLETE`

The phase-like field is the primary lifecycle lock. Each write advances that path, performs a documented bounded loop, or fails with an `[EXPECTED]` user error.

## Evidence assembly

The stored lot label and context, advisory boundary, ordered readiness signs, round label, and grower's declared observation. No sensor, weather service, or farm record is fetched.

Before consensus, the contract normalizes bounded text, copies required storage into plain local values, serializes a sorted JSON packet, and places it between explicit START/END delimiters. Nondeterministic callbacks do not read contract storage.

## Consensus boundary

Produce a readiness mask and READY, WATCH, or NOT_READY advisory for one declared observation round.

The leader callback validates exact JSON shape, field types, closed labels, masks or codes, and length bounds. A validator reruns the same semantic operation and rejects disagreement before state is committed.

## Deterministic boundary

Sign freezing, the three-round cap, round history, grower authorization, and the grower's HARVEST or WAIT decision are deterministic.

Important invariants:

- At least two grower-defined signs freeze before monitoring begins.
- Only the grower can record an observation or make the harvest decision.
- Every round retains its mask, signal, decision, and note.
- The AI signal cannot harvest a crop or override the grower.

No method sends value, pays rewards, escrows assets, deletes external data, calls another contract, or invokes a webhook.

## Failure model

- Invalid caller input or lifecycle use raises `[EXPECTED]` and leaves state unchanged.
- Malformed or out-of-policy model output raises `[LLM_ERROR]` and cannot be stored.
- Validator disagreement cannot commit the semantic result.
- StudioNet proof reads explicitly target `LATEST_FINAL`, avoiding stale pre-final state.
