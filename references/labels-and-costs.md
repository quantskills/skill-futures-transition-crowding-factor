# Labels And Costs

The default primary label is a rule-based-roll, open-to-open five-session return: signal at `T` close, entry at `T+1` open, exit at the fifth complete session after entry. Continuous and tradable contract labels are separate.

Costs are instrument/date specific where a versioned schedule exists: commission, entry/exit slippage, roll slippage, and roll spread cost. Default slippage is two ticks per side but must be configured with a versioned tick-size schedule. Missing cost schedules leave gross research results available but make net validation unavailable.
