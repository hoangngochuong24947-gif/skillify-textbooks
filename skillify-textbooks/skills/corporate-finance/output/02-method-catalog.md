# 《公司理财》方法论目录 (Method Cards)

---

## 一、估值方法论 (Valuation Methods)

### MethodCard 1: NPV分析法 (Net Present Value)

**名称**: NPV分析法

**核心论点**: 净现值是评估投资项目的最佳准则，因为它直接衡量项目为股东创造的价值。

**触发条件**:

- 评估资本投资项目
- 比较不同投资方案
- 确定项目是否值得执行

**执行步骤**:

1. **识别现金流**: 确定项目各期的增量现金流（包括初始投资、运营现金流、终结现金流）
2. **确定折现率**: 使用反映项目风险的资本成本(WACC)或要求回报率
3. **计算现值**: 将各期现金流按折现率折现到当前
4. **计算NPV**: NPV = ∑[CFt / (1+r)^t] - 初始投资
5. **决策规则**: NPV > 0 接受；NPV < 0 拒绝

**应用场景**:

- 企业资本预算决策
- 新产品开发评估
- 设备更新决策
- 并购估值

**使用限制**:

- 需要准确预测未来现金流
- 折现率选择存在主观性
- 忽略实物期权价值
- 无法比较不同规模项目（需结合PI）

**证据引用**:

> "NPV is the most important capital budgeting metric in practice...The survey numbers show importance of capital budgeting metrics in practice."
> — Chapter 9, Net Present Value and Other Investment Criteria

**分配Agent**:

- `NPV-Calculator`: 执行NPV计算
- `Cashflow-Analyzer`: 识别相关现金流
- `Risk-Assessor`: 确定合适折现率

---

### MethodCard 2: IRR分析法 (Internal Rate of Return)

**名称**: IRR分析法

**核心论点**: IRR是使项目NPV为零的折现率，代表项目的预期回报率。

**触发条件**:

- 需要以百分比形式表达投资回报
- 与要求回报率直接比较
- 初步筛选大量项目

**执行步骤**:

1. **建立方程**: 0 = ∑[CFt / (1+IRR)^t] - 初始投资
2. **求解IRR**: 使用试错法、财务计算器或Excel求解
3. **与 hurdle rate 比较**: IRR > 要求回报率则接受
4. **检查多重IRR**: 当现金流符号多次变化时，可能存在多个IRR
5. **必要时使用MIRR**: 当再投资假设不合理时，使用修正IRR

**应用场景**:

- 向非财务背景利益相关者汇报
- 快速筛选投资项目
- 与历史投资回报率比较

**使用限制**:

- 非常规现金流可能导致多重IRR或无解
- 隐含再投资假设（以IRR再投资）可能不现实
- 与NPV冲突时，NPV优先
- 无法处理融资型项目（现金流符号相反）

**证据引用**:

> "NPV, IRR, payback, discounted payback, MIRR, and accounting rate of return...Consistent, balanced examination of advantages and disadvantages of various criteria."
> — Chapter 9

**分配Agent**:

- `IRR-Calculator`: 执行IRR计算
- `Conflict-Resolver`: 处理NPV与IRR冲突

---

### MethodCard 3: DCF估值模型 (Discounted Cash Flow Valuation)

**名称**: DCF估值模型

**核心论点**: 任何资产的价值等于其未来产生的现金流的现值之和。

**触发条件**:

- 股票/债券估值
- 企业整体估值
- 项目估值
- 任何产生现金流的资产

**执行步骤**:

1. **预测现金流**: 预测未来各期自由现金流(FCFF)或股利
2. **确定预测期**: 通常5-10年详细预测+永续价值
3. **计算WACC**: 确定适当的折现率
4. **计算现值**: 折现详细预测期现金流
5. **计算终值**: 使用永续增长模型或退出倍数
6. **加总得估值**: PV(详细期) + PV(终值)

**应用场景**:

- 上市公司股票估值
- 私募股权/风险投资估值
- 并购目标估值
- 内部项目估值

**使用限制**:

- 对预测假设高度敏感
- 永续增长率假设影响巨大
- 不适用于无现金流资产
- 资本成本估算存在误差

**证据引用**:

> "Firm valuation. Develops the free cash flow approach to firm valuation."
> — Chapter 14, Cost of Capital

**分配Agent**:

- `DCF-Modeler`: 构建DCF模型
- `Forecast-Generator`: 生成财务预测
- `Terminal-Value-Calculator`: 计算终值

---

## 二、资本预算方法论 (Capital Budgeting Methods)

### MethodCard 4: 情景分析法 (Scenario Analysis)

**名称**: 情景分析法

**核心论点**: 通过构建不同情景（乐观、基本、悲观）来评估项目风险和价值范围。

**触发条件**:

- 关键变量存在高度不确定性
- 需要了解项目的风险暴露
- 向管理层展示价值区间

**执行步骤**:

1. **识别关键变量**: 确定对NPV影响最大的变量（销量、价格、成本等）
2. **定义情景**: 设定乐观、基本、悲观三种情景的参数值
3. **计算各情景NPV**: 分别计算三种情景下的NPV
4. **分析范围**: 确定NPV的范围和概率分布
5. **决策**: 评估最坏情况是否可接受

**应用场景**:

- 新产品上市评估
- 进入新市场决策
- 大宗商品价格敏感项目

**使用限制**:

- 情景定义主观
- 只考虑离散情景，忽略连续分布
- 不考虑变量间相关性

**证据引用**:

> "Scenario and sensitivity 'what-if' analyses...Illustrates how to actually apply and interpret these tools in a project analysis."
> — Chapter 11, Project Analysis and Evaluation

**分配Agent**:

- `Scenario-Builder`: 构建情景假设
- `Risk-Analyzer`: 分析风险分布

---

### MethodCard 5: 敏感性分析法 (Sensitivity Analysis)

**名称**: 敏感性分析法

**核心论点**: 通过一次改变一个变量，观察NPV的变化程度，识别关键风险因素。

**触发条件**:

- 需要了解哪些变量对项目价值影响最大
- 识别需要更多研究的变量
- 制定风险对冲策略

**执行步骤**:

1. **建立基础案例**: 计算基本假设下的NPV
2. **识别变量**: 列出所有关键输入变量
3. **逐一测试**: 每次只改变一个变量（±10%或±20%），保持其他不变
4. **计算弹性**: 记录NPV对各变量的敏感度
5. **排序**: 按敏感度排序，识别关键变量
6. **龙卷风图**: 可视化各变量的影响程度

**应用场景**:

- 优先级排序：哪些变量需要更精确预测
- 谈判准备：了解价格/成本变动的底线
- 风险管理：识别需要对冲的风险

**使用限制**:

- 假设变量独立（忽略相关性）
- 线性假设可能不准确
- 不提供概率信息

**证据引用**:

> "Scenario and sensitivity 'what-if' analyses...Break-even analysis."
> — Chapter 11

**分配Agent**:

- `Sensitivity-Analyzer`: 执行敏感性分析
- `Tornado-Chart-Generator`: 生成龙卷风图

---

### MethodCard 6: 盈亏平衡分析法 (Break-even Analysis)

**名称**: 盈亏平衡分析法

**核心论点**: 确定使NPV=0（或EAT=0）的销售量，评估项目的安全边际。

**触发条件**:

- 评估项目的最低可行销售量
- 比较不同成本结构的项目
- 设定销售目标

**执行步骤**:

1. **确定类型**: 选择会计盈亏平衡、现金盈亏平衡或财务盈亏平衡
2. **计算固定成本**: 识别不随销量变化的成本
3. **计算单位贡献**: 单价 - 单位变动成本
4. **计算盈亏平衡点**:
   - 会计盈亏平衡 = (固定成本 + 折旧) / 单位贡献
   - 现金盈亏平衡 = 固定成本 / 单位贡献
   - 财务盈亏平衡 = 使NPV=0的销量（需迭代计算）
5. **比较预期销量**: 评估安全边际

**应用场景**:

- 确定最低销售目标
- 定价策略制定
- 成本结构优化

**使用限制**:

- 假设线性成本结构
- 忽略时间价值（会计/现金盈亏平衡）
- 单一产品假设

**证据引用**:

> "Break-even analysis. Covers cash, accounting, and financial break-even levels."
> — Chapter 11

**分配Agent**:

- `BreakEven-Calculator`: 计算各类盈亏平衡点

---

## 三、风险与收益方法论 (Risk & Return Methods)

### MethodCard 7: CAPM模型 (Capital Asset Pricing Model)

**名称**: CAPM模型

**核心论点**: 资产的预期收益等于无风险利率加上风险溢价，风险溢价由Beta和市场风险溢价决定。

**触发条件**:

- 估算权益资本成本
- 确定项目要求回报率
- 评估投资组合绩效

**执行步骤**:

1. **确定无风险利率(Rf)**: 通常使用长期国债收益率
2. **估算市场风险溢价(Rm-Rf)**: 历史数据或前瞻性估计
3. **计算Beta(β)**:
   - 回归分析：股票收益 vs 市场收益
   - 或使用行业平均Beta
   - 杠杆调整：将可比公司Beta去杠杆再加杠杆
4. **应用CAPM公式**: E(R) = Rf + β(Rm - Rf)
5. **验证合理性**: 与市场数据和专业判断对比

**应用场景**:

- 权益成本估算（WACC计算）
- 投资组合预期收益预测
- 项目风险调整折现率

**使用限制**:

- 假设投资者均值-方差优化
- 单期模型，忽略多期动态
- Beta估计不稳定
- 市场组合难以观测

**证据引用**:> "Beta and the security market line. Develops the security market line with an intuitive approach...CAPM: RA = Rf + βA(RM – Rf)"

> — Chapter 13, Return, Risk, and the Security Market Line

**分配Agent**:

- `Beta-Estimator`: 计算股票Beta
- `CAPM-Calculator`: 应用CAPM公式
- `Risk-Premium-Assessor`: 估算市场风险溢价

---

### MethodCard 8: 投资组合多元化法 (Portfolio Diversification)

**名称**: 投资组合多元化法

**核心论点**: 通过持有多样化资产组合，可以消除非系统性风险，只承担市场系统性风险。

**触发条件**:

- 构建投资组合
- 评估投资策略风险
- 理解风险来源

**执行步骤**:

1. **识别风险类型**:
   - 系统性风险（市场风险）：影响所有资产
   - 非系统性风险（特有风险）：特定于公司/行业
2. **计算组合风险**:
   - 组合方差 = ∑∑wi wj σi σj ρij
   - 考虑资产间相关性
3. **观察多元化效应**: 随着资产数量增加，非系统风险下降
4. **确定最优组合**: 在给定风险下最大化收益（或反之）
5. **监控相关性**: 危机时相关性可能上升，削弱多元化效果

**应用场景**:

- 401(k)投资组合构建
- 基金经理资产配置
- 企业跨行业多元化评估

**使用限制**:

- 相关性在危机时趋同
- 存在残余非系统风险（约15-20个资产后边际效益递减）
- 无法消除系统性风险

**证据引用**:> "Diversification and systematic and unsystematic risk...Illustrates basics of risk and return in a straightforward fashion."

> — Chapter 13

**分配Agent**:

- `Portfolio-Optimizer`: 优化投资组合权重
- `Diversification-Analyzer`: 分析多元化效果

---

## 四、财务分析方法论 (Financial Analysis Methods)

### MethodCard 9: 杜邦分析法 (DuPont Analysis)

**名称**: 杜邦分析法

**核心论点**: ROE可以分解为三个组成部分（利润率×资产周转率×权益乘数），帮助识别业绩驱动因素。

**触发条件**:

- 分析ROE变化原因
- 比较不同公司盈利能力
- 识别改进机会

**执行步骤**:

1. **计算基础ROE**: 净利润 / 股东权益
2. **三因素分解**:
   - 净利润率 = 净利润 / 销售收入
   - 总资产周转率 = 销售收入 / 总资产
   - 权益乘数 = 总资产 / 股东权益
3. **五因素扩展**（可选）:
   - 税收负担 = 净利润/EBT
   - 利息负担 = EBT/EBIT
   - EBIT利润率 = EBIT/销售收入
4. **趋势分析**: 比较历史变化
5. **同业对比**: 与行业平均比较
6. **识别驱动因素**: 确定ROE变化的主要来源

**应用场景**:

- 业绩归因分析
- 战略评估（高利润vs高周转模式）
- 财务健康诊断

**使用限制**:

- 会计政策差异影响可比性
- 不适用于亏损公司
- 行业差异（资本密集型vs轻资产）

**证据引用**:> "Expanded DuPont analysis...Expands the basic DuPont equation to better explore the interrelationships between operating and financial performance."

> — Chapter 3, Working with Financial Statements

**分配Agent**:

- `DuPont-Analyzer`: 执行杜邦分析
- `ROE-Decomposer`: 分解ROE驱动因素

---

### MethodCard 10: 财务比率分析法 (Financial Ratio Analysis)

**名称**: 财务比率分析法

**核心论点**: 通过标准化财务数据，可以跨公司、跨时间比较财务表现和健康状况。

**触发条件**:

- 评估公司财务健康
- 信用分析
- 投资研究
- 预算与实际对比

**执行步骤**:

1. **选择比率类别**:
   - 流动性比率（短期偿债能力）
   - 杠杆比率（长期偿债能力）
   - 营运能力比率（资产使用效率）
   - 盈利能力比率（收益生成能力）
   - 市场价值比率（市场估值）
2. **计算比率**: 使用财务报表数据
3. **建立基准**: 与行业平均、历史数据、竞争对手比较
4. **趋势分析**: 观察时间序列变化
5. **综合评估**: 结合多个比率形成整体判断
6. **识别红旗**: 异常值或恶化趋势

**关键比率清单**:

| 类别   | 关键比率                           |
| ------ | ---------------------------------- |
| 流动性 | 流动比率、速动比率、现金比率       |
| 杠杆   | 负债率、权益乘数、利息保障倍数     |
| 营运   | 存货周转、应收账款周转、总资产周转 |
| 盈利   | ROA、ROE、毛利率、净利率           |
| 市场   | PE、PB、EV/EBITDA                  |

**使用限制**:

- 会计政策差异
- 行业特征差异
- 季节性影响
- 比率之间可能矛盾

**证据引用**:> "Understanding financial statements. Thorough coverage of standardized financial statements and key ratios."

> — Chapter 3

**分配Agent**:

- `Ratio-Calculator`: 计算财务比率
- `Benchmark-Analyzer`: 与基准比较

---

## 五、资本结构方法论 (Capital Structure Methods)

### MethodCard 11: 权衡理论模型 (Trade-off Theory)

**名称**: 权衡理论模型

**核心论点**: 最优资本结构在债务税盾收益与财务困境成本之间权衡确定。

**触发条件**:

- 确定目标资本结构
- 评估债务容量
- 资本结构优化决策

**执行步骤**:

1. **计算债务税盾价值**: 每年利息支出 × 税率
2. **估算财务困境成本**:
   - 直接成本：法律、会计费用
   - 间接成本：客户流失、供应商收紧信用、员工离职
3. **考虑代理成本**:
   - 资产替代问题（股东-债权人冲突）
   - 投资不足问题
4. **构建权衡曲线**:
   - 横轴：债务水平
   - 纵轴：企业价值
   - 税盾价值递增，但边际效益递减
   - 困境成本递增且加速
5. **确定最优点**: 企业价值最大化处的债务水平
6. **制定调整路径**: 如何从现在状态移动到最优

**应用场景**:

- 再融资决策
- 资本结构重组
- 收购融资设计

**使用限制**:

- 财务困境成本难以量化
- 假设静态环境
- 忽略信息不对称（Pecking Order Theory）

**证据引用**:> "Optimal capital structure is part debt and part equity...Occurs where the benefit from an additional dollar of debt is just offset by the increase in expected bankruptcy costs."

> — Chapter 16, Financial Leverage and Capital Structure Policy

**分配Agent**:

- `TradeOff-Modeler`: 构建权衡模型
- `Distress-Cost-Estimator`: 估算财务困境成本

---

### MethodCard 12: MM定理应用法 (Modigliani-Miller Propositions)

**名称**: MM定理应用法

**核心论点**: 在无税、无摩擦的完美市场中，资本结构不影响企业价值；有税时，债务增加价值。

**触发条件**:

- 理解资本结构的基础理论
- 评估税收对资本结构的影响
- 教学/理论分析

**执行步骤**:

1. **明确假设**:
   - MM无税：无税、无破产成本、信息对称
   - MM有税：引入公司所得税
2. **命题I（价值）**:
   - 无税：VL = VU（杠杆企业价值=无杠杆企业价值）
   - 有税：VL = VU + Tc×D（税盾价值）
3. **命题II（权益成本）**:
   - RE = RA + (RA - RD)×(D/E)
   - 权益成本随杠杆增加而线性增加
4. **WACC分析**:
   - 无税：WACC恒定，与资本结构无关
   - 有税：WACC随债务增加而下降
5. **扩展到不完美市场**: 加入破产成本、代理成本

**应用场景**:

- 理论教学
- 分析税收对融资决策的影响
- 理解资本结构的基础逻辑

**使用限制**:

- 假设过于理想化
- 实际市场中其他因素（信号、代理成本）更重要
- 主要用于理解，而非直接应用

**证据引用**:> "Modigliani and Miller Theory of Capital Structure...RE = Rf + βA(1+D/E)(RM – Rf)"

> — Chapter 16

**分配Agent**:

- `MM-Calculator`: 应用MM定理计算

---

## 六、营运资本方法论 (Working Capital Methods)

### MethodCard 13: 现金周期管理法 (Cash Conversion Cycle)

**名称**: 现金周期管理法

**核心论点**: 通过管理经营周期和现金周期，优化营运资本投入，释放现金流。

**触发条件**:

- 营运资本优化
- 现金流改善
- 营运效率评估

**执行步骤**:

1. **计算经营周期**:
   - 经营周期 = 存货周转天数 + 应收账款周转天数
2. **计算应付账款周转天数**:
   - 应付账款周转天数 = 平均应付账款 / (销售成本/365)
3. **计算现金周期**:
   - 现金周期 = 经营周期 - 应付账款周转天数
4. **分析组成**:
   - 存货周转天数 = 平均存货 / (销售成本/365)
   - 应收账款周转天数 = 平均应收账款 / (销售收入/365)
5. **识别改进机会**:
   - 减少存货（JIT系统）
   - 加速收款（折扣、保理）
   - 延迟付款（不损害供应商关系）
6. **量化影响**: 每减少1天现金周期释放的现金

**应用场景**:

- 营运资本效率改进
- 供应链金融设计
- 季节性现金流管理

**使用限制**:

- 行业差异（零售vs制造vs服务）
- 过度优化可能损害供应商/客户关系
- 需要考虑竞争环境

**证据引用**:> "Operating and cash cycles...Stresses the importance of cash flow timing."

> — Chapter 18, Short-Term Finance and Planning

**分配Agent**:

- `CashCycle-Calculator`: 计算现金周期
- `WCOptimizer`: 优化营运资本

---

### MethodCard 14: 信用政策分析法 (Credit Policy Analysis)

**名称**: 信用政策分析法

**核心论点**: 最优信用政策在增加销售收益与应收账款持有成本、坏账成本之间权衡。

**触发条件**:

- 设计或修订信用政策
- 评估现有信用政策效果
- 客户信用评估

**执行步骤**:

1. **分析当前政策**:
   - 信用标准、信用期间、现金折扣
   - 应收账款周转、坏账率、DSO
2. **识别成本组成**:
   - 应收账款机会成本（资金占用）
   - 坏账成本
   - 信用分析和管理成本
   - 现金折扣成本
3. **估算收益**: 增加销售带来的边际贡献
4. **计算NPV**: 政策变化的增量收益 - 增量成本
5. **敏感性测试**: 不同坏账率、销售增长率下的结果
6. **实施与监控**: 建立信用评分系统，持续跟踪

**关键决策变量**:

- **信用标准**: 多严格的客户筛选
- **信用期间**: 30天、60天还是90天
- **现金折扣**: 2/10 net 30等
- **收款政策**: 逾期处理方式

**使用限制**:

- 客户行为难以预测
- 竞争压力可能迫使放宽标准
- 需要准确的成本数据

**证据引用**:> "Credit management...Analysis of credit policy and implementation."

> — Chapter 20, Credit and Inventory Management

**分配Agent**:

- `CreditPolicy-Analyzer`: 分析信用政策
- `Credit-Scorer`: 客户信用评分

---

## 七、实物期权方法论 (Real Options Methods)

### MethodCard 15: 实物期权估值法 (Real Options Valuation)

**名称**: 实物期权估值法

**核心论点**: 管理灵活性（扩张、放弃、延迟的选择权）具有价值，应纳入项目评估。

**触发条件**:

- 高度不确定性项目
- 分阶段投资决策
- 战略价值评估

**执行步骤**:

1. **识别期权类型**:
   - **扩张期权**: 成功后扩大规模的权利
   - **放弃期权**: 情况恶化时退出的权利
   - **延迟期权**: 等待更多信息再投资的权利
   - **转换期权**: 改变运营方式的权利
2. **计算传统NPV**: 作为基准
3. **识别期权参数**:
   - 标的资产现值(S)
   - 执行价格(K)
   - 波动率(σ)
   - 到期时间(T)
   - 无风险利率(r)
4. **应用期权定价模型**:
   - Black-Scholes（欧式期权）
   - 二叉树模型（美式期权）
   - 蒙特卡洛模拟（复杂路径依赖）
5. **计算战略NPV**: 传统NPV + 期权价值
6. **决策**: 即使传统NPV为负，战略NPV可能为正

**应用场景**:

- 研发项目投资决策
- 自然资源开采项目
- 新药开发
- 房地产投资

**使用限制**:

- 参数估计困难（特别是波动率）
- 模型假设（市场完备性）现实中难满足
- 可能高估项目价值

**证据引用**:> "Stock options, employee stock options, and real options...real options (like expansion or abandonment options)."

> — Chapter 24, Options and Corporate Finance

**分配Agent**:

- `RealOptions-Valuator`: 估值实物期权
- `BlackScholes-Calculator`: 应用BS模型

---

## 方法论分组索引

### 按应用领域

| 应用领域           | 相关MethodCards                                                 |
| ------------------ | --------------------------------------------------------------- |
| **估值**     | 1-NPV, 2-IRR, 3-DCF                                             |
| **资本预算** | 1-NPV, 2-IRR, 4-情景分析, 5-敏感性分析, 6-盈亏平衡, 15-实物期权 |
| **风险分析** | 4-情景分析, 5-敏感性分析, 7-CAPM, 8-多元化, 15-实物期权         |
| **财务分析** | 9-杜邦, 10-财务比率                                             |
| **资本结构** | 11-权衡理论, 12-MM定理                                          |
| **营运资本** | 13-现金周期, 14-信用政策                                        |

### 按决策层级

| 层级               | MethodCards                                               |
| ------------------ | --------------------------------------------------------- |
| **战略层**   | 11-权衡理论, 12-MM定理, 15-实物期权                       |
| **投资层**   | 1-NPV, 2-IRR, 3-DCF, 4-情景分析, 5-敏感性分析, 6-盈亏平衡 |
| **运营层**   | 9-杜邦, 10-财务比率, 13-现金周期, 14-信用政策             |
| **风险管理** | 7-CAPM, 8-多元化                                          |

---

## 证据来源汇总

- [1] McGraw-Hill Fundamentals of Corporate Finance 2024 Release - Core methodology documentation
- [2] Corporate Finance 11e Solutions Manual - Method application examples
- [3] Brandeis University Study Notes - Method framework summaries
- [4] Chapter-specific method descriptions and formulas

---

## 待补充项

- [ ] 各MethodCard的具体计算公式和Excel模板
- [ ] 更多实际案例（S&S Air, Conch Republic等）
- [ ] 与其他教材方法的对比（如APV方法、FTE方法）
- [ ] 各方法的常见错误和注意事项

---

*文档生成时间: 2026-03-15*
*NotebookLM Notebook ID: b2566da4-0597-44df-87ff-fe76c81d428e*
