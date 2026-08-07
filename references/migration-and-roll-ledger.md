# Migration And Roll Ledger

Default migration configuration:

```yaml
confirmation_days: 2
candidate_pool:
  k: 3
  volume_weight: 0.5
  open_interest_weight: 0.5
roll_execution:
  price_field: open
  execution_lag: next_tradeable_session
  fallback_fields: []
```

A candidate must lead the current contract in both open interest and volume for the configured consecutive days. The next tradeable session is the execution date. If identity or required observations are unresolved, the instrument is paused; it is not silently switched to provider dominant.

The ledger records current/candidate contracts, confirmation dates, execution date, prices, source fields, and quality states.
