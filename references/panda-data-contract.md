# PandaData Contract

Direct runtime: `import panda_data`.

Core method contracts are based on the installed PandaData API reference and must be checked against returned schemas before formal validation.

- `get_future_daily`: `date`, `symbol`, `dominant_id`, `underlying_symbol`, `open`, `close`, `volume`, `open_interest`, `settlement`.
- `get_future_detail`: `symbol`, lifecycle dates, `contract_multiplier`, `exchange`, `industry_name`, `product`, `is_trading`.
- `get_future_dominant`: `date`, `underlying_symbol`, `symbol`.
- `get_future_basis`: `basis = spot_price - futures_price`, `basis_ratio = basis / spot_price`.

The skill does not assume an API method's presence proves its field semantics. Missing required fields block only dependent layers. Credentials are configured by the user and are never handled by this skill.
