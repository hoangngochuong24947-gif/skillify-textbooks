# 03-场景路由：《示例书名》

## 用户问题类型清单

| 问题类型 | 描述 | 典型提问方式 |
|----------|------|--------------|
| 类型A | 描述问题类型A | "如何..."、"怎么..." |
| 类型B | 描述问题类型B | "为什么..."、"什么原因..." |
| 类型C | 描述问题类型C | "什么时候..."、"是否适合..." |

## 方法匹配规则

### 规则一：问题类型A → 方法组合

**触发条件：**
- 用户问题包含关键词X、Y、Z
- 问题涉及领域A

**推荐方法组合：**
1. 首先使用 [方法A] 进行框架分析
2. 然后使用 [方法B] 进行具体评估
3. 最后用 [方法C] 验证结论

**输出文档：**
- `01-author-thinking.md`（作者视角）
- `02-method-catalog.md`（具体方法）

**示例：**
- 输入："如何用XX思维分析我的产品策略？"
- 匹配：[方法A] + [方法B]
- 置信度：高

### 规则二：问题类型B → 方法组合

**触发条件：**
- 用户问题包含关键词P、Q
- 问题寻求原因解释

**推荐方法组合：**
1. 使用 [方法D] 识别根本原因
2. 使用 [方法E] 分析影响因素

**输出文档：**
- `02-method-catalog.md`

**示例：**
- 输入："为什么会出现XX现象？"
- 匹配：[方法D]
- 置信度：中

## 组合调用规则

### 组合A：基础分析组合

**适用：** 初次接触某类问题

```yaml
sequence:
  - step: 1
    method: 方法X
    purpose: 建立问题框架
  - step: 2
    method: 方法Y
    purpose: 深入分析
  - step: 3
    method: 方法Z
    purpose: 验证结论
```

### 组合B：快速决策组合

**适用：** 时间紧迫，需要快速判断

```yaml
sequence:
  - step: 1
    method: 方法A
    purpose: 快速评估
  - step: 2
    method: 方法B
    purpose: 做出决策
```

## 不适用情况与拒绝策略

### 明确拒绝的情况

| 情况 | 拒绝理由 | 建议替代 |
|------|----------|----------|
| 问题完全无关 | 本书方法论不适用于此领域 | 推荐其他资源 |
| 需要实时数据 | 本书只提供思维框架，不包含实时信息 | 结合最新数据源 |
| 违反伦理 | 本书方法论不支持此类应用 | 明确拒绝 |

### 降级处理的情况

| 情况 | 处理方式 | 置信度 |
|------|----------|--------|
| 部分相关 | 使用相关子集，说明局限性 | 中 |
| 需要推断 | 基于书中原则推断，标记待验证 | 低 |
| 信息不足 | 要求用户提供更多上下文 | 待定 |

## RoutingDecision 示例

### 示例一：产品策略分析

```yaml
user_problem: "如何用书中的思维分析我的产品策略？"
matched_methods:
  - "框架A：整体分析框架"
  - "方法A1：具体评估方法"
  - "方法A2：验证方法"
assigned_subagents:
  - "Author Thinking Analyst"
  - "Methodology Miner"
  - "Scenario Router"
output_docs:
  - "01-author-thinking.md"
  - "02-method-catalog.md"
  - "03-scenario-router.md"
confidence: high
reasoning: "用户问题明确涉及产品策略分析，与书中框架A直接对应"
```

### 示例二：学习方法咨询

```yaml
user_problem: "这本书的学习方法是什么？"
matched_methods:
  - "方法B：学习方法"
assigned_subagents:
  - "Methodology Miner"
output_docs:
  - "02-method-catalog.md"
confidence: medium
reasoning: "问题与书中方法B相关，但需要更多上下文确认具体应用场景"
```
