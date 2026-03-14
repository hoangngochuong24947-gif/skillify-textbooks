# 04-Subagent 手册：《示例书名》

## 角色总览

```
Book Profiler
    ↓ (输出 00-overview.md)
Author Thinking Analyst
    ↓ (输出 01-author-thinking.md)
Methodology Miner
    ↓ (输出 02-method-catalog.md)
Scenario Router
    ↓ (输出 03-scenario-router.md)
Skill Packager / QA
    ↓ (输出 04/05-spec.md)
```

## 1. Book Profiler

### 职责

建立全书地图，说明这本书究竟在解决什么问题，以及整本书如何展开。

### 输入

- `BookBrief`（用户提供的书籍基本信息）
- Pack 1 的 NotebookLM 输出（全书结构查询结果）

### 处理流程

1. 解析 BookBrief，确认缺失信息
2. 分析 NotebookLM 的 Pack 1 输出
3. 提取章节结构、核心命题、关键词
4. 组织成标准化的 00-overview.md

### 输出

- **文档：** `00-overview.md`
- **包含内容：**
  - BookBrief 完整信息
  - 章节结构图
  - 核心命题列表
  - 关键词表
  - 阅读对象与适用任务

### 交接给下一角色

将以下传递给 Author Thinking Analyst：
- BookBrief
- 00-overview.md 草稿
- Pack 2 的 NotebookLM 输出

### 质量检查点

- [ ] BookBrief 所有字段已填写（或标记为推断）
- [ ] 章节结构清晰可读
- [ ] 核心命题有证据支持

## 2. Author Thinking Analyst

### 职责

把"作者如何思考"从内容里剥离出来，形成稳定的思维方式描述。

### 输入

- BookBrief
- 00-overview.md
- Pack 2 的 NotebookLM 输出（作者思维方式查询结果）

### 处理流程

1. 阅读 00-overview.md 了解全书结构
2. 分析 Pack 2 输出，识别作者的：
   - 观察维度
   - 判断原则
   - 分析顺序
   - 默认前提
3. 提取易误读点
4. 组织成 01-author-thinking.md

### 输出

- **文档：** `01-author-thinking.md`
- **包含内容：**
  - 作者的默认视角
  - 常用分析维度
  - 判断原则（带证据）
  - 分析顺序
  - 易误读点

### 交接给下一角色

将以下传递给 Methodology Miner：
- 01-author-thinking.md 草稿
- 00-overview.md
- Pack 3 的 NotebookLM 输出

### 质量检查点

- [ ] 每条判断原则都有证据引用
- [ ] 易误读点明确具体
- [ ] 分析顺序可操作

## 3. Methodology Miner

### 职责

将显性方法和隐性方法合并为统一的 MethodCards。

### 输入

- 00-overview.md
- 01-author-thinking.md
- Pack 3 的 NotebookLM 输出（方法论查询结果）

### 处理流程

1. 识别显性方法（书中明确命名的）
2. 识别隐性方法（反复出现但未命名的）
3. 合并重复的方法
4. 按粒度分级：宏观框架 → 中层方法 → 微观技巧
5. 为每个方法创建 MethodCard
6. 标记证据不足的方法

### 输出

- **文档：** `02-method-catalog.md`
- **包含内容：**
  - 宏观框架（3-5个）
  - 中层方法（每个框架下2-4个）
  - 微观技巧（补充）
  - 方法关系图
  - 待确认方法清单

### MethodCard 模板

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
  - "Chapter X, Section Y: quote"
assigned_agents:
  - string
```

### 交接给下一角色

将以下传递给 Scenario Router：
- MethodCards 列表
- 02-method-catalog.md 草稿
- Pack 4 的 NotebookLM 输出

### 质量检查点

- [ ] 每个 MethodCard 都有证据
- [ ] 粒度分级清晰
- [ ] 待确认方法已标记

## 4. Scenario Router

### 职责

把方法和用户问题连接起来，明确什么时候调用哪种方法。

### 输入

- MethodCards 列表
- 02-method-catalog.md
- Pack 4 的 NotebookLM 输出（适用场景查询结果）

### 处理流程

1. 定义用户问题类型
2. 为每个问题类型匹配方法组合
3. 定义组合调用顺序
4. 定义不适用情况和拒绝策略
5. 创建 RoutingDecision 示例
6. 组织成 03-scenario-router.md

### 输出

- **文档：** `03-scenario-router.md`
- **包含内容：**
  - 用户问题类型清单
  - 方法匹配规则
  - 组合调用规则
  - 不适用情况与拒绝策略
  - RoutingDecision 示例

### 交接给下一角色

将以下传递给 Skill Packager / QA：
- 03-scenario-router.md 草稿
- 所有之前的文档
- Pack 5 的 NotebookLM 输出

### 质量检查点

- [ ] 匹配规则明确可执行
- [ ] 拒绝策略完整
- [ ] RoutingDecision 示例覆盖主要场景

## 5. Skill Packager / QA

### 职责

把前面的结果包装为 skill 规范，并检查证据完整性、重复项和宿主兼容性。

### 输入

- 所有 MethodCards
- 所有 RoutingDecisions
- 00/01/02/03 文档草稿
- Pack 5 的 NotebookLM 输出（冲突校验与综合）

### 处理流程

1. 验证所有 MethodCards 的证据完整性
2. 检查方法去重情况
3. 验证冲突解决方法
4. 创建 subagent playbook 文档
5. 创建 master skill spec 文档
6. 生成 SkillBundleManifest
7. 列出待确认问题清单

### 输出

- **文档：**
  - `04-subagent-playbooks.md`（本文档）
  - `05-master-skill-spec.md`
- **元数据：**
  - `SkillBundleManifest`
  - 待确认问题清单

### 质量检查点

- [ ] 所有 MethodCards 有证据
- [ ] 无重复方法
- [ ] 冲突已解决或标记
- [ ] 文档格式一致

## 交接规范

### 文档格式

所有交接文档使用 Markdown，包含：
- YAML frontmatter（如适用）
- 清晰的章节标题
- 表格和列表优先于长段落

### 状态标记

每个文档应包含状态：
- `draft` - 草稿，待审核
- `reviewed` - 已审核，可能需修改
- `final` - 最终版本

### 证据引用格式

统一使用：`Chapter X, Section Y: "具体引用或描述"`

## 错误处理

### 证据不足

如果发现某个关键方法证据不足：
1. 标记为 `pending_confirmation`
2. 记录在待确认问题清单
3. 不影响其他方法的打包

### 冲突无法解决

如果两个方法存在无法调和的冲突：
1. 列出冲突点
2. 提供两种解释
3. 建议用户根据上下文选择

### 文档缺失

如果前序文档未完成：
1. 暂停当前角色
2. 要求完成前序文档
3. 不推测或脑补缺失内容
