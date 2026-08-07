# 期货迁移拥挤因子

**简体中文** | [English](README.en.md)

> 一句话定位：从直接 PandaData 期货合约数据中构造可审计的主力迁移与拥挤转移横截面因子。

## 这是什么

本 Skill 以具体期货合约为原始层，以期货品种为因子层，计算合约持仓集中度、成交集中度和经过联合规则确认的主力迁移压力，输出因子值、迁移台账、质量状态和可交给现有因子评价/回测流程的标准化面板。

项目配置的 PandaData-compatible 数据源可用于期货研究；这是数据契约描述，不构成对任何提供方的官方背书。MCP 不是运行依赖，也不处理登录、凭证或自动安装。

## 快速开始

```bash
python scripts/check_runtime.py
python scripts/partition_queries.py examples/config.example.yaml --start 2024-01-01 --end 2024-12-31
python scripts/compute_components.py tests/fixtures/minimal_panel/contract_daily.json
python scripts/build_roll_ledger.py tests/fixtures/minimal_panel/migration_daily.json --out /tmp/roll_ledger.json
python scripts/build_factor_panel.py /path/to/standardized_components.json --out /tmp/factor_panel.json
python -m unittest discover -s tests -v
node scripts/validate-qsh-form.mjs SKILL.md
```

正式主检验前必须冻结配置、查询契约、可见性规则、成本模型和时间切分，并单独确认执行。

## 输出

- `contract_components.parquet` 或等价结构化面板；
- `roll_ledger.json`；
- `factor_values.parquet`；
- `labels.parquet`；
- `primary_test_report.md`；
- `backtest_handoff.json`。

缺少可选席位或基差层时，核心因子仍可生成；缺少核心合约、生命周期或主力迁移证据时，相关品种/因子标记为不可用，不填零替代。

## 与相邻 Skill 的边界

本 Skill 不重做会员持仓集中度、DeepView 综合报告、carry/期限结构主研究、连续合约审计、通用市场状态识别、回测引擎或自动交易。详细边界见 [references/overlap-review.md](references/overlap-review.md)。

## 研究限制

核心因子是可证伪研究假设，不保证拥挤反转成立。结果必须区分探索性、正式主检验和冻结样本外测试；不得把研究结果表述为投资建议或保证收益。

## 许可证

GPL-3.0，见 [LICENSE](LICENSE)。
