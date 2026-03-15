# Skillify Textbooks
将书籍转化为可复用的 Claude Code 技能体系。
## 项目概述
你是否总是感觉读完一本书，虽然书里很多思考方式都非常有用，可是自己读完一本书既忘记了知识点也想不起来该怎么学着像作者一样思考了？
你是否也希望自己能在找到一本好书后真正把作者的思考方式内化于自身？
你是否觉得直接与GPT、Gemini这样的聊天机器人学习时，尽管要求了对方的思考方式，但在一段时间的上下文后依然回归默认、幻觉丛生？
本项目提供一套系统化方法，将高质量图书中的思考方式、分析框架和方法论，整理成可被 Claude Code、OpenClaw 等 agent 环境直接调用的技能（skills）。
**核心价值：**
- 不是做摘要，而是做"可调用的方法论资产"
- 不是单次问答，而是"分阶段、多角色、可复用"的抽取流水线
- 不是串行执行，而是"智能并行"的 agent 编排（节省 ~40% 时间）
- 所有结论都有证据支撑，可追溯、可验证
## 快速开始
### 安装
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/skillify-textbooks.git

# Copy skill to your Claude Code skills directory
cp -r skillify-textbooks/skills/book-to-skills ~/.claude/skills/
```
详见 [INSTALL.md](INSTALL.md)。
### 使用方法
在 Claude Code 中，skill 会自动触发于以下场景：
```
"帮我从《思考，快与慢》生成一套技能"
"把这本书转换成方法论技能"
"提取这本书的思维模型"
```
系统会自动：
1. 解析 BookBrief（书名、作者等）
2. 创建 NotebookLM workspace
3. **并行启动**多个 subagents 进行抽取
4. 生成完整的 skill 文档包
## 项目结构
```
skillify-textbooks/
├── README.md                          # 项目说明
├── VERSION                            # 版本号
├── CHANGELOG.md                       # 变更日志
├── INSTALL.md                         # 安装指南
├── docs/                              # 设计文档
│   ├── book-to-skill-brainstorm.md
│   └── book-to-skill-plan.md
├── skills/                            # 技能定义
│   └── book-to-skills/
│       ├── SKILL.md                   # 主技能定义
│       ├── parallel-manifest.yaml     # 并行执行配置 ⭐ NEW
│       ├── AGENT_ORCHESTRATOR.md      # Agent 编排规范 ⭐ NEW
│       └── references/                # 参考文档
│           ├── notebooklm-mcp-workflow.md
│           ├── query-packs.md
│           ├── subagent-playbooks.md
│           ├── output-schemas.md
│           └── visual-infographic-spec.md
├── tests/                             # 压力测试场景
│   └── baseline-scenarios.md
├── examples/                          # 示例输出
│   └── example-book/
│       ├── 00-overview.md
│       ├── 01-author-thinking.md
│       ├── 02-method-catalog.md
│       ├── 03-scenario-router.md
│       ├── 04-subagent-playbooks.md
│       └── 05-master-skill-spec.md
└── .github/workflows/                 # CI/CD
    └── validate-skill.yml
```

## 核心特性

### 1. 并行 Agent 执行

通过 `parallel-manifest.yaml` 定义 agent 依赖图，实现智能并行：

```
Phase 1 (并行): Book Profiler + Author Thinking Analyst
                      ↓
Phase 2 (并行): Methodology Miner (Explicit) + Methodology Miner (Implicit)
                      ↓
Phase 3: Scenario Router
                      ↓
Phase 4: Skill Packager / QA
```

**性能对比：**
| 模式 | 预计耗时 | 加速比 |
|-----|---------|-------|
| 串行执行 | 25-35 分钟 | 1.0x |
| 并行执行 | 15-20 分钟 | **~1.7x** |

### 2. MethodCard 标准

每个提取的方法都遵循统一格式：

```yaml
name: 方法名称
thesis: 核心论点
triggers: [触发条件]
steps: [执行步骤]
scenarios: [应用场景]
limits: [使用边界]
evidence: ["Chapter X: 引用"]
assigned_agents: [负责角色]
```

### 3. 五段式问题包

1. **全书结构图** - 建立章节地图与核心命题
2. **作者思维方式** - 提炼作者的分析维度
3. **方法论抽取** - 收集显性和隐性方法（并行执行）
4. **适用场景与边界** - 建立触发条件和禁用条件
5. **冲突校验与综合** - 去重、归并、降级弱证据

### 4. Subagent 分工

| 角色 | 职责 | 输出 | 执行组 |
|------|------|------|-------|
| Book Profiler | 建立全书地图 | 00-overview.md | Group A |
| Author Thinking Analyst | 抽取思维方式 | 01-author-thinking.md | Group A |
| Methodology Miner | 标准化 MethodCards | 02-method-catalog.md | Group B |
| Scenario Router | 方法路由逻辑 | 03-scenario-router.md | Group C |
| Skill Packager / QA | 打包与质量检查 | 04/05-spec.md | Group D |

## 执行模式

支持三种执行模式，通过 `AGENT_ORCHESTRATOR.md` 配置：

### 模式 A: 全自动并行（默认）
```yaml
execution_mode: "auto_parallel"
# 自动识别独立任务，同时启动 agents
```

### 模式 B: 手动分批
```yaml
execution_mode: "manual_batch"
# 每批执行前请求用户确认
```

### 模式 C: 纯串行（Fallback）
```yaml
execution_mode: "sequential_fallback"
# 当并行执行失败时自动降级
```

## 质量保证

### 证据规则
- 每个 MethodCard 必须有证据引用
- 证据格式：`Chapter X, Section Y: specific quote`
- 弱证据结论标记为 `pending_confirmation`

### CI/CD
GitHub Actions 自动验证：
- YAML 文件格式检查
- SKILL.md 结构完整性
- 引用文件存在性检查
- 文件命名一致性

## 路线图

- [x] 第一版：单书处理、串行执行
- [x] **第一版增强：并行 agent 执行** ⭐ NEW
- [ ] 第二版：完整试跑验证
- [ ] 第三版：Claude Code 自动调用
- [ ] 未来：多书融合、真实并发

## 贡献

按照 Superpowers TDD 流程：
1. 创建压力场景测试当前 skill
2. 观察失败模式
3. 改进 SKILL.md 或 reference 文件
4. 验证改进解决了问题
5. 提交 PR

## 许可

MIT License
