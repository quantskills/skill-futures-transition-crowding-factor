# Validation Protocol

The frozen primary test is `crowding_reversal_core` against five-session rule-based-roll open-to-open returns. Rank IC is primary, Pearson IC is auxiliary, Newey-West lags default to four, and five equal-weight groups use Q5 long/Q1 short.

Acceptance is multidimensional: positive Rank IC, HAC p-value below 0.05, positive IC ratio, positive gross and net Q5-Q1, allowed monotonicity, adequate coverage, and no dominance failure. Exploratory variants use predeclared BH-FDR groups. A small smoke test never upgrades `validation_level`.
