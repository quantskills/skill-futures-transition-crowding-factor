---
name: futures-transition-crowding-factor
description: "Build an auditable cross-sectional futures factor from contract-level open-interest concentration, volume concentration, and confirmed dominant-contract migration. Use when an agent needs to compute point-in-time transition and crowding features from direct PandaData futures data, produce factor values and roll-ledger evidence, or prepare a handoff to an existing factor-evaluation or backtest workflow. Do not use this skill for broker DeepView reports, generic carry or term-structure research, continuous-contract auditing, portfolio optimization, or trading instructions."
quantSkills:
  organization: https://github.com/quantskills
  repository: quantskills/skill-futures-transition-crowding-factor
  repository_url: https://github.com/quantskills/skill-futures-transition-crowding-factor
  project_type: skill
  collection: futures-factor-research
  license: GPL-3.0
  category: factor
  tags: [futures-factor, crowding, contract-transition, open-interest, roll-ledger]
  platforms: [claude-code, codex, openclaw, cursor, hermes]
  language: zh-en
  status: draft
  validation_level: listed
  maintainer_type: community
  requires: []
  summary_zh: 从期货合约迁移与拥挤转移构造可审计横截面因子
  summary_en: Build an auditable futures factor from contract transitions and crowding shifts
---

```json qsh-form
{
  "version": 1,
  "task": {
    "placeholder": "构造期货合约迁移与拥挤反转因子",
    "required": true
  },
  "fields": [
    {"key": "start_date", "type": "date", "label": "开始日期"},
    {"key": "end_date", "type": "date", "label": "结束日期"},
    {"key": "confirmation_days", "type": "number", "label": "迁移确认天数"},
    {"key": "run_primary_test", "type": "select", "label": "执行主检验", "options": [
      {"value": "false", "label": "仅生成因子"},
      {"value": "true", "label": "确认后执行"}
    ]}
  ],
  "prompt_template": "{{task}}；区间：{{start_date}} 至 {{end_date}}；确认天数：{{confirmation_days}}；执行主检验：{{run_primary_test}}；附件：{{#attachments}}"
}
```

# Futures Transition Crowding Factor

## Scope

This skill uses the direct `panda_data` runtime to transform contract-level futures observations into a point-in-time instrument-level factor. The core factor measures concentration and confirmed migration pressure; it does not assert that crowding must reverse.

## Use When

Use this skill when the user asks to:

- construct a cross-sectional futures crowding or transition factor;
- calculate contract OI/volume HHI and dominant-contract migration features;
- produce a reproducible roll ledger and factor handoff panel;
- evaluate a pre-declared primary test with Rank IC, Pearson IC, grouped returns, and HAC inference.

## Do Not Use When

Do not use this skill to:

- produce a general futures DeepView or broker report;
- reproduce an existing member-position concentration, family-reversal, carry, or term-structure factor;
- replace continuous-contract or roll auditing specialists;
- run a general backtest engine or optimize factor variants;
- issue buy, sell, position, or guaranteed-return instructions.

## Direct PandaData Runtime

The production entrypoint uses the user's configured `panda_data` package directly. MCP is not a runtime dependency. The API reference may be consulted during development, but this repository does not call an MCP server, install credentials, log in, or store tokens.

Core methods and contracts:

- `get_future_daily`: contract date, symbol, underlying symbol, prices, volume, open interest, settlement, and provider dominant id;
- `get_future_detail`: lifecycle, multiplier, exchange, product, industry name, and trading status;
- `get_future_dominant`: daily provider mapping, used for comparison and diagnostics, not as the internal roll rule.

Optional layers:

- `get_future_symbol_posi` for separately queried long/short broker subsets;
- `get_future_basis` for `basis = spot_price - futures_price` and `basis_ratio`;
- `get_future_term_structure` only after its returned schema is explicitly confirmed.

## Core Workflow

1. Check the direct PandaData runtime without handling credentials.
2. Read the frozen, layered query configuration and required-field contracts.
3. Partition long date ranges according to the interface contract and retain partition hashes.
4. Normalize contract lifecycle and point-in-time eligibility.
5. Build the active Top-K candidate pool using within-instrument volume/OI percentile ranks.
6. Confirm migrations with joint OI and volume leadership for the configured consecutive days (default two); if identity or evidence is unresolved, pause the instrument.
7. Compute active/all-eligible HHI, bilateral migration pressure, and quality states.
8. Apply rolling median/MAD then daily cross-sectional robust standardization.
9. Emit the fixed core factor, optional broker-direction variants, diagnostics, and roll ledger.
10. Build labels and costs only from declared execution rules; hand off to evaluation/backtest tools without silently selecting variants.

## Core Factor Contract

The core score has exactly three required components:

```text
contract_oi_concentration
contract_volume_concentration
migration_pressure_magnitude
```

Each is fully defined before standardization. Core components are never dynamically reweighted when optional layers are missing. The output includes both `crowding_factor_long_core` and `crowding_reversal_core`; sign selection is left to declared evaluation, not learned from the test set.

## Primary Test

The default primary test is frozen before execution:

```text
factor: crowding_reversal_core
label: rule_based_roll_return_open_to_open_5d
statistic: daily Rank IC
inference: Newey-West HAC, lags=4
portfolio: five equal-weight groups, Q5 long / Q1 short
costs: instrument schedule + two ticks per side + explicit roll cost
```

Primary acceptance requires positive Rank IC, HAC p-value below 0.05, positive IC ratio, positive gross and cost-adjusted Q5-Q1, allowed group monotonicity, adequate coverage, and no declared dominance failure. Exploratory variants use predeclared Benjamini-Hochberg FDR groups.

## Safety and Evidence

Direct PandaData data, query parameters, fields, returned schema, availability policy, partitions, storage mode, and fingerprints are evidence. Missing optional data disables only dependent variants. Missing core fields block the core factor. No credentials or private data enter reports. This is research and education only, not investment advice.
