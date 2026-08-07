# Futures Transition Crowding Factor

> One-line positioning: Build an auditable cross-sectional factor from contract-level futures concentration and confirmed dominant-contract transitions using the direct `panda_data` runtime.

## What this is

This skill keeps concrete contracts as the raw layer and futures instruments as the factor layer. It computes contract open-interest concentration, volume concentration, and jointly confirmed migration pressure, then emits factor values, a roll ledger, quality states, and a structured handoff for existing factor evaluation or backtest workflows.

Project-configured PandaData-compatible data sources are supported for futures research; this describes a data contract and is not an official endorsement of any provider. MCP is not a runtime dependency; this skill does not install packages, handle login, or store credentials.

## Quick start

```bash
python scripts/check_runtime.py
python scripts/partition_queries.py examples/config.example.yaml --start 2024-01-01 --end 2024-12-31
python scripts/compute_components.py tests/fixtures/minimal_panel/contract_daily.json
python scripts/build_roll_ledger.py tests/fixtures/minimal_panel/migration_daily.json --out /tmp/roll_ledger.json
python scripts/build_factor_panel.py /path/to/standardized_components.json --out /tmp/factor_panel.json
python -m unittest discover -s tests -v
node scripts/validate-qsh-form.mjs SKILL.md
```

Before a formal primary test, freeze the configuration, query contracts, availability rules, cost model, and time split, then confirm execution separately.

## Outputs

- `contract_components.parquet` or an equivalent structured panel;
- `roll_ledger.json`;
- `factor_values.parquet`;
- `labels.parquet`;
- `primary_test_report.md`;
- `backtest_handoff.json`.

Missing optional broker or basis layers disable only their variants. Missing core contract, lifecycle, or migration evidence makes the affected instrument/factor unavailable; it is never silently filled with zero.

## Boundary with neighboring skills

This skill does not reimplement member-position concentration, DeepView reports, carry/term-structure research, continuous-contract auditing, generic market-regime detection, a backtest engine, or automated trading. See [references/overlap-review.md](references/overlap-review.md).

## Research limits

The core factor is a falsifiable research hypothesis; crowding reversal is not assumed to work. Results must distinguish exploratory work, the formal primary test, and a frozen out-of-sample test. Research output is not investment advice or a guarantee of returns.

## License

GPL-3.0. See [LICENSE](LICENSE).
