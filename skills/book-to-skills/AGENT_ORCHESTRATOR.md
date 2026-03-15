# Agent Orchestrator Specification

Agent 编排器规范 - 定义如何在并行和串行模式之间调度 subagents。

## 核心职责

编排器负责：
1. **解析依赖图** - 根据 `parallel-manifest.yaml` 构建执行计划
2. **并行启动** - 同时触发无依赖的 agents
3. **结果合并** - 在同步点收集和合并各 agent 输出
4. **错误处理** - 处理部分失败和重试逻辑

## 执行模式

### 模式 A: 全自动并行（推荐）

由主 Claude Code 实例直接并行调用多个 subagents：

```yaml
execution_mode: "auto_parallel"
steps:
  1. 读取 parallel-manifest.yaml
  2. 识别 group_a_discovery (无依赖)
  3. 同时创建 2 个 subagents:
     - Book Profiler
     - Author Thinking Analyst
  4. 等待两者完成
  5. 合并输出，启动 group_b_extraction
  6. 继续直到完成
```

### 模式 B: 手动分批

用户控制每批执行：

```yaml
execution_mode: "manual_batch"
steps:
  1. 提示用户: "准备启动 Group A (2 个并行 agents)"
  2. 等待用户确认
  3. 执行并行 batch
  4. 展示结果，询问是否继续
```

### 模式 C: 纯串行（Fallback）

当并行执行失败时使用：

```yaml
execution_mode: "sequential_fallback"
steps:
  1. 按顺序执行每个 agent
  2. 每个 agent 等待前一个完成
  3. 总耗时较长但稳定性最高
```

## 并行执行协议

### 启动阶段

```python
# 伪代码示意
def launch_parallel_group(group):
    agents = group.agents
    results = {}

    # 同时提交所有 agents
    for agent in agents:
        results[agent.name] = submit_subagent(
            prompt=agent_prompts[agent.name],
            context=build_context(agent.inputs)
        )

    # 等待所有完成
    wait_for_all(results.values())

    return merge_results(results, group.merge_strategy)
```

### 合并策略

#### Strategy 1: Concatenate（直接拼接）

用于 Group A - Discovery 阶段：

```
Input:  00-overview.md + 01-author-thinking.md
Output: combined_discovery_context.md
Action: 简单拼接，添加分隔符
```

#### Strategy 2: Combine Methods（方法合并）

用于 Group B - Extraction 阶段：

```
Input:  explicit_methods.json + implicit_methods.json
Process:
  1. 去重（名称相似度 > 0.8 视为重复）
  2. 分类（宏观/中层/微观）
  3. 排序（按书中出现顺序）
Output: 02-method-catalog.md
```

#### Strategy 3: Validation Pass（验证合并）

用于 Group D - QA 阶段：

```
Input: 所有文档
Process:
  1. 检查交叉引用一致性
  2. 验证证据完整性
  3. 标记待确认项
Output: validation_report + final_bundle
```

## Subagent Prompt 模板

### Book Profiler Prompt

```markdown
你是 Book Profiler subagent。

任务：建立《{{book_title}}》的全书结构图。

输入：
- BookBrief: {{book_brief}}
- NotebookLM Notebook ID: {{notebook_id}}

执行步骤：
1. 使用 NotebookLM MCP 执行 Pack 1 问题包
2. 提取：章节结构、核心命题、关键词表
3. 生成：00-overview.md

输出格式：
严格按照 references/output-schemas.md 中的 00-overview.md 格式。

时间限制：5 分钟内完成。
```

### Methodology Miner (Explicit) Prompt

```markdown
你是 Methodology Miner - Explicit subagent。

任务：提取《{{book_title}}》中直接命名的方法。

输入：
- 00-overview.md
- 01-author-thinking.md
- NotebookLM Notebook ID: {{notebook_id}}

执行步骤：
1. 查询 NotebookLM: "书中直接命名的框架、模型、方法有哪些？"
2. 每个方法创建 MethodCard
3. 必须包含：证据引用（章节/页码）

输出格式：
JSON 数组，每个元素符合 MethodCard schema。

时间限制：7 分钟内完成。
```

### Methodology Miner (Implicit) Prompt

```markdown
你是 Methodology Miner - Implicit subagent。

任务：提取《{{book_title}}》中反复出现但未命名的分析套路。

输入：
- 00-overview.md
- 01-author-thinking.md
- NotebookLM Notebook ID: {{notebook_id}}

执行步骤：
1. 查询 NotebookLM: "作者反复使用但未明确命名的分析模式有哪些？"
2. 识别隐性套路（如"先否定再肯定"、"极端案例分析"）
3. 为每个套路创建 MethodCard

输出格式：
JSON 数组，每个元素符合 MethodCard schema。

注意：
- 只提取书中实际使用的套路，不要发明
- 证据必须指向具体段落
```

## 错误处理

### Agent 失败时的策略

| 失败类型 | 处理策略 |
|---------|---------|
| 单个 agent 超时 | 重试 1 次，仍失败则标记为阻塞 |
| 单个 agent 输出无效 | 请求修正，提供 schema 验证错误 |
| 合并时冲突 | 创建冲突报告，请求人工裁决 |
| 全部 agent 失败 | 降级为串行模式 |

### 恢复机制

```yaml
recovery:
  checkpoint_interval: "per_group"
  saved_state:
    - last_completed_group
    - all_outputs_so_far
    - pending_agents

  resume_procedure:
    1. 加载最后保存的状态
    2. 重新启动失败的 agents
    3. 继续正常流程
```

## 性能监控

### 指标收集

```yaml
metrics:
  - agent_start_time
  - agent_end_time
  - agent_output_size
  - notebooklm_query_count
  - merge_time
  - total_execution_time
```

### 预期性能

| 阶段 | 串行时间 | 并行时间 | 加速比 |
|-----|---------|---------|-------|
| Group A | 8-10 min | 5 min | 1.6-2x |
| Group B | 10-14 min | 7 min | 1.4-2x |
| 总计 | 25-35 min | 15-20 min | ~1.7x |

## 与 SKILL.md 的关系

```
SKILL.md
  └── 定义了 What（做什么）
      └── 引用 AGENT_ORCHESTRATOR.md
          └── 定义了 How（怎么做 - 并行策略）
              └── 引用 parallel-manifest.yaml
                  └── 定义了 When（执行顺序和依赖）
```
