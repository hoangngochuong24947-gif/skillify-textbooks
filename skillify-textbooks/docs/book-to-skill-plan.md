# 从书生成 Skills 项目规划文档

## 1. 项目定位

这个项目的目标不是“总结一本书”，而是把一本高价值图书里的思考方式、分析框架、零散方法论和适用边界，整理成一套可以被 Claude Code、OpenClaw 一类 agent 软件直接调用的 skills 体系。

第一版只处理一本书，重点验证以下闭环是否成立：

1. 把书导入 NotebookLM。
2. 通过固定问题包多轮提问抽出结构化知识。
3. 把知识整理成方法卡和路由规则。
4. 生成一个总控 skill 和多个子方法论文档。
5. 让宿主在接到用户问题时，能判断是否适合调用这本书的思维方式。

## 2. 核心原则

- 不是做摘要，而是做“可调用的方法论资产”。
- 不是单次问答，而是做“分阶段、多角色、可复用”的抽取流水线。
- 不是自由发挥，而是所有中间产物都遵守统一输入输出。
- 不是只服务某个单一宿主，而是优先兼容 Claude Code / OpenClaw 的技能调用习惯。
- 不是一次性内容生成，而是可反复用于不同书籍的 meta-skill。

## 3. 标准主流程

```text
选书/定义目标
-> 建立 NotebookLM notebook
-> 执行五段式问题包
-> 形成全书结构图与作者思维模型
-> 抽取零散方法论并标准化为 MethodCard
-> 建立场景路由与 subagent 分工
-> 生成 Markdown 文档包
-> 封装为 master skill + references
```

## 4. 系统结构

### 4.1 Master Skill

顶层 `book-to-skills` skill 负责四件事：

1. 理解用户当前问题。
2. 判断是否适合调用这本书的思维方式。
3. 选择最合适的方法论模块。
4. 委派哪些 subagents 参与，并声明将产出哪些 Markdown 文档。

### 4.2 五类 Subagents

| 角色 | 主要职责 | 关键输出 |
| --- | --- | --- |
| Book Profiler | 建立全书地图、章节结构、核心议题 | `00-overview.md` |
| Author Thinking Analyst | 抽出作者的判断方式、分析视角、推理顺序 | `01-author-thinking.md` |
| Methodology Miner | 把分散方法归并为可复用方法卡 | `02-method-catalog.md` |
| Scenario Router | 判断方法在什么问题下触发、如何组合 | `03-scenario-router.md` |
| Skill Packager / QA | 把前述结果整理成 skill 规范并做证据校验 | `04-subagent-playbooks.md`、`05-master-skill-spec.md` |

## 5. NotebookLM MCP 设计

NotebookLM 使用 MCP 作为第一版主接口，执行方式采用“逻辑并行、实际串行”。

### 5.1 五段式问题包

| 阶段 | 目标 | 典型问题 |
| --- | --- | --- |
| 全书结构图 | 建立章节地图与核心命题 | 这本书的核心结构是什么？章节之间如何递进？ |
| 作者思维方式 | 提炼作者如何观察、如何判断、如何拆解问题 | 作者看问题时最常用的分析维度是什么？ |
| 方法论抽取 | 收集显性和隐性方法 | 书中有哪些可重复使用的方法、步骤或判断准则？ |
| 适用场景与边界 | 建立触发条件和禁用条件 | 这些方法适合什么问题，不适合什么问题？ |
| 冲突校验与综合 | 去重、归并、降级弱证据 | 哪些方法互相补充、冲突或依赖前提？ |

### 5.2 执行规则

- 每轮问题都要带目标，不允许“开放聊天式”提问。
- 每个结论都要求证据出处，至少指向章节、段落或明显内容片段。
- 证据不足的结论只能标为“待确认”，不能直接进入 skill 主体。
- 每一阶段都产出结构化草稿，再交给下一阶段处理。

## 6. 公共接口

### 6.1 `BookBrief`

```yaml
title: string
author: string
domain: string
audience: string
goal: string
language: zh | en
```

### 6.2 `QueryPack`

```yaml
stage: string
objective: string
questions:
  - string
evidence_rule: string
expected_output: string
```

### 6.3 `MethodCard`

```yaml
name: string
thesis: string
triggers:
  - string
steps:
  - string
scenarios:
  - string
limits:
  - string
evidence:
  - string
assigned_agents:
  - string
```

### 6.4 `RoutingDecision`

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

### 6.5 `SkillBundleManifest`

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

## 7. 默认输出包

每次完成一次“书 -> skills”处理，默认输出以下 Markdown 包：

- `00-overview.md`：全书目标、结构、概念地图、关键词。
- `01-author-thinking.md`：作者的观察方式、判断框架、分析顺序。
- `02-method-catalog.md`：所有方法卡，按主题分组。
- `03-scenario-router.md`：什么问题对应什么方法，如何组合。
- `04-subagent-playbooks.md`：每个 subagent 的职责、输入、输出、交接关系。
- `05-master-skill-spec.md`：顶层 skill 的调用逻辑、委派逻辑、产出逻辑。

## 8. 标准化信息图结构

这一轮不直接生成图片，但要准备好可直接喂给信息图工具的结构稿。推荐使用 `dense-modules + pop-laboratory + portrait`。

### 8.1 六大模块

1. `MOD-1 项目目标`：什么是“从书生成 skills”，解决什么问题。
2. `MOD-2 NotebookLM 提问链路`：五段式问题包与串行执行。
3. `MOD-3 Subagent 分工`：五个角色各做什么。
4. `MOD-4 方法论路由`：用户问题如何匹配 MethodCard。
5. `MOD-5 输出文档体系`：六份 Markdown 的关系。
6. `MOD-6 迭代闭环`：证据校验、回补提问、二次收敛。

### 8.2 视觉语法

- 每个模块都带坐标标签，如 `SEC-A1`、`SEC-B2`。
- 主色调用灰白底、鼠尾草绿模块、荧光粉警示、亮黄高亮。
- 使用网格、细线、标尺、箭头和参数标注强化“系统化”质感。
- 尽量减少装饰元素，所有角落都承载信息，不保留空白装饰区。

## 9. 第一版验收标准

- 能针对一本方法论强的书产出至少 5 张高质量 `MethodCard`。
- 能针对一本方法论分散的书做归并，不只给摘要。
- 当用户说“用这本书的思维分析我的产品策略”时，系统能输出方法匹配、subagent 分派和文档计划。
- 证据不足时会明确降级，而不是编造成熟结论。
- 顶层 skill 的描述不依赖 Claude Code 私有上下文，OpenClaw 也能理解同一结构。

## 10. 当前不做的事

- 不做多书融合。
- 不做真实并发执行。
- 不做自动发布、自动同步、自动索引。
- 不做图片最终生成，只交付图片结构稿和渲染说明。
