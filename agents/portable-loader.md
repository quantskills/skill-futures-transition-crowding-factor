# Portable Loader Prompt

Use this prompt when the host does not automatically discover `SKILL.md` files. Replace `<FUTURES_TRANSITION_CROWDING_FACTOR_SKILL_ROOT>` with the absolute repository root before loading.

Load and follow:

1. `<FUTURES_TRANSITION_CROWDING_FACTOR_SKILL_ROOT>/SKILL.md` as the authoritative contract.
2. The data and lifecycle references under `<FUTURES_TRANSITION_CROWDING_FACTOR_SKILL_ROOT>/references/`, especially `panda-data-contract.md`, `contract-lifecycle.md`, and `migration-and-roll-ledger.md`.
3. `<FUTURES_TRANSITION_CROWDING_FACTOR_SKILL_ROOT>/references/crowding-components.md`, `labels-and-costs.md`, and `validation-protocol.md` for fixed calculations and test boundaries.
4. The schemas under `<FUTURES_TRANSITION_CROWDING_FACTOR_SKILL_ROOT>/schemas/` before validating or writing outputs.
5. The relevant deterministic scripts under `<FUTURES_TRANSITION_CROWDING_FACTOR_SKILL_ROOT>/scripts/` instead of reimplementing their rules.

Use direct `panda_data` only under the declared runtime and authorization boundary. Keep the fixed core components and point-in-time rules unchanged; missing core evidence blocks the affected output rather than becoming zero. Keep synthetic fixtures separate from live evidence. Never handle credentials or private data, and do not issue trading instructions.
