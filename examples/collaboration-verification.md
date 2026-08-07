# Synthetic Collaboration Verification

This fixture verifies the local factor mechanics only:

- HHI uses active-contract subsets and retains all-eligible diagnostics;
- activity candidates use deterministic within-instrument percentile ranks;
- the direct runtime boundary is `panda_data`, but no live credentials or external service is used here;
- no broker, basis, or term-structure variant is fabricated when its layer is absent;
- synthetic output is not a live PandaData result and does not justify `validation_level: verified`.
