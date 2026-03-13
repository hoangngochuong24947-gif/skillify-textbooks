# Subagent Playbooks

## Shared Rules

- 每个 subagent 只能处理自己的职责范围。
- 所有输出必须回填到统一 schema。
- 如果输入证据不足，优先返回问题和缺口，不要直接脑补。
- 第一版按串行流程执行，但交接格式要为未来并行保留接口。

## 1. Book Profiler

### Mission

建立全书地图，说明这本书究竟在解决什么问题，以及整本书如何展开。

### Inputs

- `BookBrief`
- Pack 1 的 NotebookLM 输出

### Outputs

- 章节结构
- 核心命题
- 关键词表
- `00-overview.md` 草稿

## 2. Author Thinking Analyst

### Mission

把“作者如何思考”从内容里剥离出来，形成稳定的思维方式描述。

### Inputs

- `BookBrief`
- Pack 2 的 NotebookLM 输出
- `00-overview.md`

### Outputs

- 作者常用观察维度
- 判断原则
- 分析顺序
- `01-author-thinking.md` 草稿

## 3. Methodology Miner

### Mission

将显性方法和隐性方法合并为统一 `MethodCard`。

### Inputs

- Pack 3 的 NotebookLM 输出
- `00-overview.md`
- `01-author-thinking.md`

### Outputs

- `MethodCard[]`
- 去重说明
- `02-method-catalog.md` 草稿

## 4. Scenario Router

### Mission

把方法和用户问题连接起来，明确什么时候调用哪种方法。

### Inputs

- `MethodCard[]`
- Pack 4 的 NotebookLM 输出

### Outputs

- `RoutingDecision` 模式
- 方法触发条件和禁用条件
- `03-scenario-router.md` 草稿

## 5. Skill Packager / QA

### Mission

把前面的结果包装为 skill 规范，并检查证据完整性、重复项和宿主兼容性。

### Inputs

- `MethodCard[]`
- `RoutingDecision`
- Pack 5 的 NotebookLM 输出

### Outputs

- `04-subagent-playbooks.md`
- `05-master-skill-spec.md`
- `SkillBundleManifest`
- 待确认问题清单
