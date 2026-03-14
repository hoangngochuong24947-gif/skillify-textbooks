# Output Schemas

## Markdown Bundle

### `00-overview.md`

- 书名、作者、领域、目标
- 全书结构图
- 核心命题
- 关键词表
- 阅读对象与适用任务

### `01-author-thinking.md`

- 作者的默认视角
- 常用分析维度
- 判断原则
- 分析顺序
- 易误读点

### `02-method-catalog.md`

每个方法都用统一 `MethodCard` 表示：

```yaml
name: string              # 方法名称，动词+名词形式，如"锚定调整法"
thesis: string            # 核心论点，一句话概括这个方法解决什么问题
triggers:                 # 触发条件：什么情况下应该调用此方法
  - string
steps:                    # 执行步骤：可操作的指令序列
  - string
scenarios:                # 应用场景：具体例子说明何时使用
  - string
limits:                   # 使用边界：何时不应该使用此方法
evidence:                 # 证据引用：书中文献，支持多种格式
  - "Chapter X, Section Y: specific quote"
  - "Page N: key concept reference"
  - "Part Z: methodology description"
assigned_agents:          # 负责执行的subagent角色
  - string
```

**MethodCard 粒度指南：**

| 粒度级别 | 例子 | 适用情况 |
|---------|------|----------|
| **宏观框架** | "双系统思维模型" | 全书核心思想，适用于高层决策 |
| **中层方法** | "可得性启发判断法" | 特定问题类型的分析套路 |
| **微观技巧** | "锚定值调整三步法" | 具体可执行的操作步骤 |

**规则：**
- 一本书通常产出 3-5 个宏观框架
- 每个框架下可拆解 2-4 个中层方法
- 每个方法可包含 1-3 个微观技巧
- 优先输出中层方法，微观技巧作为补充

### `03-scenario-router.md`

- 用户问题类型清单
- 每类问题推荐的方法组合
- 不同方法之间的先后顺序
- 不适用情况和拒绝策略

### `04-subagent-playbooks.md`

- 每个 subagent 的任务
- 每个 subagent 的输入
- 每个 subagent 的输出
- 上下游交接关系

### `05-master-skill-spec.md`

- 顶层调用目标
- 进入条件
- 方法筛选规则
- subagent 委派规则
- 输出文档规则
- 证据与降级规则

## Core Interfaces

### `BookBrief`

```yaml
title: string
author: string
domain: string
audience: string
goal: string
language: zh | en
```

### `QueryPack`

```yaml
stage: string
objective: string
questions:
  - string
evidence_rule: string
expected_output: string
```

### `RoutingDecision`

```yaml
user_problem: string
matched_methods:
  - string
assigned_subagents:
  - string
output_docs:
  - string
confidence: low | medium | high
```

### `SkillBundleManifest`

```yaml
source_book: string
master_skill_name: string
included_methods:
  - string
generated_docs:
  - string
platform_notes:
  - string
```

## Quality Gates

| 检查项 | 通过标准 | 失败处理 |
|--------|----------|----------|
| 证据完整性 | 每个 `MethodCard` 至少有1条证据引用 | 标记为 `pending_confirmation`，不入主skill |
| 匹配可解释性 | 每个 `RoutingDecision` 能解释匹配理由 | 添加 `reasoning` 字段说明逻辑 |
| 边界明确性 | 所有”适用范围”都有明确的禁用条件 | 补充 `limits` 字段 |
| 证据强度 | 高强度结论（如”总是”、”最佳”）需要多来源证据 | 降级为”通常”、”可能”，或标记待确认 |
| 多语言一致性 | 中文skill引用英文书时，关键术语保留双语 | 在括号中添加原文术语 |

## 迭代闭环流程

当发现证据不足或结论存疑时：

```
1. 识别缺口
   ↓ 记录缺失的证据类型
2. 设计回补提问
   ↓ 创建针对性QueryPack
3. NotebookLM二次查询
   ↓ 获取补充证据
4. 更新MethodCard
   ↓ 添加新证据或调整结论
5. 重新评估
   ↓ 确认是否满足Quality Gates
6. 输出或再次迭代
```

**何时需要回补提问：**
- MethodCard的 `evidence` 字段为空或薄弱
- 不同Pack的结论相互矛盾
- 用户问题需要书中未覆盖的方法
- 验证测试发现理解偏差

**回补提问格式：**
```yaml
stage: “supplemental_query”
objective: “获取关于[具体方法]的更多证据”
target_method: “方法名称”
evidence_gap: “缺少[类型]的证据”
questions:
  - “书中第X章如何描述这个方法的具体步骤？”
  - “作者提供了哪些案例来说明这个方法？”
expected_evidence: “章节引用、具体案例、操作步骤”
```
