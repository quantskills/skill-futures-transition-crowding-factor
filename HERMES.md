# Hermes Loader

This file is the repository-local Hermes entry point. It is a compatibility instruction, not an organization-wide Hermes schema.

Load the root `SKILL.md` as the authoritative contract for `futures-transition-crowding-factor`. Read only the references and schemas needed for the request, then use the deterministic scripts under `scripts/` for runtime checks, query partitioning, factor construction, labels, and freeze validation.

Use direct `panda_data` only under the declared runtime and authorization boundary. Keep the fixed core components and point-in-time rules unchanged; missing core evidence blocks the affected output rather than becoming zero. Keep synthetic fixtures separate from live evidence. Never handle credentials or private data, and do not issue trading instructions.
