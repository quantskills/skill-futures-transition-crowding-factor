# Crowding Components

Core components are fixed:

```text
contract_oi_concentration = active-contract OI HHI
contract_volume_concentration = active-contract volume HHI
migration_pressure_magnitude = bilateral old/new OI-share and volume-share transfer strength
```

All-eligible and active HHI diagnostics are retained. The core requires at least three active contracts by default. Standardization is rolling median/MAD with a 252-session window and 80% minimum history, followed by daily cross-sectional robust standardization. MAD below tolerance makes the component unavailable.

Optional broker and basis components never dynamically replace a missing core component.
