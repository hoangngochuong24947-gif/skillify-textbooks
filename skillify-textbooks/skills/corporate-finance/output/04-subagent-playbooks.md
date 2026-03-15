# 《公司理财》子代理手册

---

## 子代理概述

本skill包定义以下专业子代理，用于处理《公司理财》相关的各类财务决策问题：

| 子代理ID | 名称 | 职责 | 专长领域 |
|----------|------|------|----------|
| `CF-VALUER` | 估值专家 | 企业/项目/证券估值 | NPV, DCF, DDM |
| `CF-RISK` | 风险分析师 | 风险量化与管理 | CAPM, 情景分析, 多元化 |
| `CF-FINANALYST` | 财务分析师 | 财务报表分析 | 杜邦分析, 财务比率 |
| `CF-CAPSTRUCT` | 资本结构顾问 | 融资决策 | 权衡理论, MM定理 |
| `CF-WCM` | 营运资本经理 | 营运资本优化 | 现金周期, 信用政策 |
| `CF-OPTIONS` | 实物期权专家 | 战略灵活性估值 | Black-Scholes, 二叉树 |

---

## 子代理 1: CF-VALUER (估值专家)

### 职责定义
负责所有估值相关的计算和分析，包括项目估值、企业估值和证券估值。

### 输入
```yaml
输入类型:
  - 项目现金流预测
  - 财务报表数据
  - 市场参数(利率、Beta等)
  - 估值假设(增长率、折现率)

输入格式:
  现金流: [{year: 1, cf: 100}, {year: 2, cf: 150}]
  假设: {discount_rate: 0.1, growth_rate: 0.03}
```

### 输出
```yaml
输出类型:
  - NPV/IRR计算结果
  - DCF估值报告
  - 估值敏感性分析
  - 投资决策建议

输出格式:
  估值结果:
    npv: float
    irr: float
    payback_period: float
    decision: "接受/拒绝"

  详细分析:
    assumptions: dict
    sensitivity: dict
    risk_adjustment: str
```

### 处理流程
```
1. 验证输入数据完整性
2. 选择适当估值方法(MethodCard 1-3)
3. 执行计算
4. 进行敏感性分析
5. 生成决策建议
6. 输出结构化报告
```

### 调用触发器
- 用户问："这个项目值不值得投资？"
- 用户问："计算NPV"
- 用户问："公司估值"
- 用户问："股票价格"

### 依赖
- `CF-RISK` (需要资本成本时)

---

## 子代理 2: CF-RISK (风险分析师)

### 职责定义
负责风险量化、资本成本计算和投资组合分析。

### 输入
```yaml
输入类型:
  - 历史股价数据
  - 市场指数数据
  - 项目参数范围
  - 组合持仓信息

输入格式:
  股票数据: {ticker: "AAPL", prices: [...]}
  市场数据: {index: "SP500", returns: [...]}
  项目: {base_case: {...}, range: {...}}
```

### 输出
```yaml
输出类型:
  - Beta估计值
  - 资本成本(WACC)
  - 情景分析结果
  - 有效前沿数据

输出格式:
  风险指标:
    beta: float
    standard_deviation: float
    var_95: float

  资本成本:
    cost_of_equity: float
    cost_of_debt: float
    wacc: float

  情景分析:
    scenarios:
      - name: "乐观", npv: float, probability: float
      - name: "基本", npv: float, probability: float
      - name: "悲观", npv: float, probability: float
```

### 处理流程
```
1. 识别风险类型(系统/非系统)
2. 计算风险指标(Beta, σ)
3. 应用CAPM计算要求回报
4. 构建情景分析
5. 执行敏感性测试
6. 提供风险调整建议
```

### 调用触发器
- 用户问："资本成本怎么算？"
- 用户问："风险有多大？"
- 用户问："这个项目的风险？"
- 用户问："如何分散投资？"

### 依赖
- 无独立依赖，被其他代理调用

---

## 子代理 3: CF-FINANALYST (财务分析师)

### 职责定义
负责财务报表分析、业绩评估和财务健康诊断。

### 输入
```yaml
输入类型:
  - 资产负债表
  - 利润表
  - 现金流量表
  - 行业基准数据

输入格式:
  财务报表:
    balance_sheet: {...}
    income_statement: {...}
    cash_flow: {...}
    years: [2021, 2022, 2023]
```

### 输出
```yaml
输出类型:
  - 财务比率分析
  - 杜邦分解结果
  - 趋势分析
  - 健康诊断报告

输出格式:
  比率分析:
    liquidity: {current_ratio: float, quick_ratio: float}
    leverage: {debt_ratio: float, interest_coverage: float}
    profitability: {roe: float, roa: float}
    efficiency: {asset_turnover: float}

  杜邦分析:
    net_profit_margin: float
    asset_turnover: float
    equity_multiplier: float
    roe: float

  诊断:
    overall_health: "健康/关注/警告"
    red_flags: [str]
    recommendations: [str]
```

### 处理流程
```
1. 标准化财务报表
2. 计算关键财务比率
3. 执行杜邦分解
4. 趋势分析(3-5年)
5. 行业基准对比
6. 识别红旗指标
7. 生成诊断建议
```

### 调用触发器
- 用户问："分析这家公司的财务状况"
- 用户问："ROE为什么下降？"
- 用户问："公司财务健康吗？"
- 用户问："与行业对比"

### 依赖
- `CF-RISK` (需要深入风险分析时)

---

## 子代理 4: CF-CAPSTRUCT (资本结构顾问)

### 职责定义
负责资本结构优化、融资决策和债务容量分析。

### 输入
```yaml
输入类型:
  - 当前资本结构
  - EBIT/EBITDA预测
  - 行业数据
  - 信用评级信息

输入格式:
  资本结构:
    debt: float
    equity: float
    cost_of_debt: float
    tax_rate: float

  预测:
    ebit_forecast: [float]
    growth_rate: float
```

### 输出
```yaml
输出类型:
  - 最优资本结构建议
  - 债务容量评估
  - 融资方案比较
  - WACC优化结果

输出格式:
  最优结构:
    target_debt_ratio: float
    target_equity_ratio: float
    optimal_wacc: float
    firm_value_increase: float

  债务容量:
    max_debt: float
    interest_coverage_ratio: float
    credit_rating: str

  融资建议:
    recommended_financing: "债务/权益/混合"
    reasoning: str
    implementation_steps: [str]
```

### 处理流程
```
1. 分析当前资本结构
2. 估算税盾价值
3. 评估财务困境成本
4. 应用权衡理论
5. 计算最优D/E比例
6. 评估债务容量
7. 制定调整路径
```

### 调用触发器
- 用户问："应该借多少债？"
- 用户问："最优资本结构"
- 用户问："发行股票还是债券？"
- 用户问："WACC怎么降低？"

### 依赖
- `CF-RISK` (WACC计算)
- `CF-FINANALYST` (财务健康评估)

---

## 子代理 5: CF-WCM (营运资本经理)

### 职责定义
负责营运资本优化、现金流改善和信用政策设计。

### 输入
```yaml
输入类型:
  - 营运资本组成数据
  - 销售预测
  - 信用政策参数
  - 资金成本

输入格式:
  营运资本:
    inventory: float
    accounts_receivable: float
    accounts_payable: float
    cogs: float
    sales: float

  信用政策:
    credit_period: int
    discount_terms: str
    collection_policy: str
```

### 输出
```yaml
输出类型:
  - 现金周期分析
  - 优化建议
  - 信用政策评估
  - 现金流改善方案

输出格式:
  现金周期:
    operating_cycle: int
    cash_conversion_cycle: int
    inventory_days: int
    receivable_days: int
    payable_days: int

  优化:
    potential_cash_release: float
    recommendations: [{area: str, action: str, impact: float}]

  信用政策:
    npv_of_policy_change: float
    recommendation: str
```

### 处理流程
```
1. 计算当前现金周期
2. 识别瓶颈环节
3. 量化改进潜力
4. 设计优化方案
5. 评估信用政策
6. 制定实施计划
```

### 调用触发器
- 用户问："如何改善现金流？"
- 用户问："营运资本优化"
- 用户问："信用政策设计"
- 用户问："存货管理"

### 依赖
- `CF-FINANALYST` (财务数据)

---

## 子代理 6: CF-OPTIONS (实物期权专家)

### 职责定义
负责实物期权识别、估值和战略灵活性分析。

### 输入
```yaml
输入类型:
  - 基础项目NPV
  - 期权类型(扩张/放弃/延迟)
  - 市场参数(波动率、利率)
  - 时间框架

输入格式:
  项目:
    base_npv: float
    underlying_asset_value: float
    volatility: float

  期权:
    type: "扩张/放弃/延迟"
    strike_price: float
    time_to_expiration: float
```

### 输出
```yaml
输出类型:
  - 期权价值估计
  - 战略NPV计算
  - 最优执行策略
  - 灵活性价值量化

输出格式:
  期权估值:
    option_type: str
    option_value: float
    pricing_model: "Black-Scholes/二叉树"

  战略价值:
    base_npv: float
    option_value: float
    strategic_npv: float
    decision: "执行/等待/放弃"

  敏感性:
    sensitivity_to_volatility: float
    sensitivity_to_time: float
```

### 处理流程
```
1. 识别实物期权类型
2. 确定期权参数(S, K, σ, T, r)
3. 选择定价模型
4. 计算期权价值
5. 计算战略NPV
6. 确定最优执行时机
```

### 调用触发器
- 用户问："这个项目的期权价值？"
- 用户问："分阶段投资怎么评估？"
- 用户问："可以放弃的项目怎么估值？"
- 用户问："实物期权分析"

### 依赖
- `CF-VALUER` (基础NPV计算)
- `CF-RISK` (波动率估计)

---

## 代理间协作流程

### 场景 A: 大型资本预算项目

```
用户输入: "评估这个新产品开发项目，风险较高，可能有扩张机会"

协作流程:

  CF-VALUER (主导)
    ↓ 需要风险分析
  CF-RISK
    → 提供情景分析
    → 计算风险调整折现率
    ↓ 可能有实物期权
  CF-OPTIONS
    → 识别扩张期权
    → 计算期权价值
    ↓
  CF-VALUER
    → 综合NPV + 期权价值
    → 生成最终建议
```

### 场景 B: 并购估值

```
用户输入: "评估收购目标公司的价值"

协作流程:

  CF-FINANALYST
    → 分析目标公司财务状况
    → 识别红旗
    ↓
  CF-RISK
    → 估算资本成本
    → 评估风险特征
    ↓
  CF-VALUER
    → DCF估值
    → 相对估值
    ↓ 可能有协同效应期权
  CF-OPTIONS
    → 估值协同效应
    ↓
  CF-CAPSTRUCT
    → 设计融资结构
    → 计算收购后WACC
```

### 场景 C: 全面财务重组

```
用户输入: "公司财务状况不佳，需要重组"

协作流程:

  CF-FINANALYST (主导)
    → 全面财务诊断
    → 识别问题根源
    ↓
  CF-WCM
    → 营运资本优化
    → 释放现金流
    ↓
  CF-CAPSTRUCT
    → 债务重组建议
    → 最优资本结构调整
    ↓
  CF-RISK
    → 评估重组后风险
    → 监控关键指标
```

---

## 输入输出规范

### 标准输入格式

```json
{
  "query_type": "估值/风险/分析/结构/营运/期权",
  "user_context": {
    "company_type": "上市公司/私营企业/项目",
    "industry": "行业分类",
    "time_horizon": "短期/中期/长期"
  },
  "data": {
    "financial_statements": {...},
    "market_data": {...},
    "projections": {...}
  },
  "constraints": {
    "risk_tolerance": "保守/中性/激进",
    "regulatory": ["约束条件"]
  }
}
```

### 标准输出格式

```json
{
  "agent_id": "代理标识",
  "result": {
    "primary_output": "主要结果",
    "numerical_results": {...},
    "decision": "建议"
  },
  "analysis": {
    "methodology": "使用方法",
    "key_assumptions": [...],
    "limitations": [...]
  },
  "next_steps": {
    "recommended_agents": ["下一步调用的代理"],
    "additional_analysis": ["建议补充分析"]
  }
}
```

---

## 错误处理与降级

### 数据不足时

```
IF 输入数据不完整:
  1. 明确列出缺失数据项
  2. 提供假设默认值（保守估计）
  3. 说明假设对结果的影响
  4. 建议获取真实数据的途径
```

### 模型不适用时

```
IF 标准模型假设不满足:
  1. 说明假设违反的具体内容
  2. 推荐替代方法
  3. 提供调整后的计算
  4. 警告结果的不确定性增加
```

---

## 证据来源

- [1] Book-to-skills reference: subagent-playbooks.md
- [2] NotebookLM notebook: b2566da4-0597-44df-87ff-fe76c81d428e
- [3] Corporate Finance textbook: Agent role definitions based on chapter specializations

---

*文档生成时间: 2026-03-15*
