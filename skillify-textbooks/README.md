# Skillify Textbooks

将书籍转化为可复用的 Claude Code 技能体系。

## 项目概述

本项目提供一套系统化方法，将高质量图书中的思考方式、分析框架和方法论，整理成可被 Claude Code、OpenClaw 等 agent 环境直接调用的技能（skills）。

**核心价值：**
- 不是做摘要，而是做"可调用的方法论资产"
- 不是单次问答，而是"分阶段、多角色、可复用"的抽取流水线
- 所有结论都有证据支撑，可追溯、可验证

## 快速开始

### 前置要求

- Claude Code 或兼容的 agent 环境
- NotebookLM MCP 连接（用于书籍内容处理）

### 使用方法

1. **激活 Skill**
   ```
   在 Claude Code 中，skill 会自动触发于以下场景：
   - "帮我从《书名》生成 skill"
   - "把这本书转换成方法论技能"
   - "提取这本书的思维模型"
   ```

2. **准备 BookBrief**
   ```yaml
   title: 书名
   author: 作者
   domain: 领域（如：决策心理学）
   audience: 目标读者
   goal: 提取目标
   language: zh | en
   ```

3. **执行 Workflow**
   - 创建 NotebookLM notebook
   - 执行五段式问题包
   - 生成 MethodCards
   - 输出 Markdown 文档包

## 项目结构

```
skillify-textbooks/
├── README.md                          # 项目说明
├── docs/                              # 设计文档
│   ├── book-to-skill-brainstorm.md   # 头脑风暴文档
│   └── book-to-skill-plan.md         # 项目规划文档
├── skills/                            # 技能定义
│   └── book-to-skills/
│       ├── SKILL.md                   # 主技能定义
│       └── references/                # 参考文档
│           ├── notebooklm-mcp-workflow.md
│           ├── query-packs.md
│           ├── subagent-playbooks.md
│           ├── output-schemas.md
│           └── visual-infographic-spec.md
├── tests/                             # 压力测试场景
│   └── baseline-scenarios.md
└── examples/                          # 示例输出
    └── example-book/
        ├── 00-overview.md
        ├── 01-author-thinking.md
        ├── 02-method-catalog.md
        ├── 03-scenario-router.md
        ├── 04-subagent-playbooks.md
        └── 05-master-skill-spec.md
```

## 核心概念

### MethodCard

标准化方法卡片，包含：
- `name`: 方法名称
- `thesis`: 核心论点
- `triggers`: 触发条件
- `steps`: 执行步骤
- `scenarios`: 应用场景
- `limits`: 使用边界
- `evidence`: 证据引用
- `assigned_agents`: 负责角色

### 五段式问题包

1. **全书结构图** - 建立章节地图与核心命题
2. **作者思维方式** - 提炼作者的分析维度和判断习惯
3. **方法论抽取** - 收集显性和隐性方法
4. **适用场景与边界** - 建立触发条件和禁用条件
5. **冲突校验与综合** - 去重、归并、降级弱证据

### Subagent 角色

| 角色 | 职责 | 输出 |
|------|------|------|
| Book Profiler | 建立全书地图 | 00-overview.md |
| Author Thinking Analyst | 抽取作者思维方式 | 01-author-thinking.md |
| Methodology Miner | 标准化 MethodCards | 02-method-catalog.md |
| Scenario Router | 方法路由逻辑 | 03-scenario-router.md |
| Skill Packager / QA | 打包与质量检查 | 04/05-spec.md |

## 开发方法

本项目使用 **Superpowers TDD 方法** 进行迭代：

1. **RED**: 运行基线测试，观察无 skill 时的自然行为
2. **GREEN**: 改进 SKILL.md 解决基线问题
3. **REFACTOR**: 关闭漏洞，完善 reference 文件

### 运行基线测试

```bash
# 查看测试场景
cat tests/baseline-scenarios.md

# 使用子代理运行压力测试
# (通过 Claude Code Agent 工具)
```

## 质量保证

### 证据规则

- 每个 MethodCard 必须有证据引用
- 证据格式：`Chapter X, Section Y: specific quote`
- 弱证据结论标记为 `pending_confirmation`

### 迭代闭环

```
识别缺口 → 设计回补提问 → NotebookLM 查询 →
更新 MethodCard → 重新评估 → 输出/再迭代
```

## 路线图

- [x] 第一版：单书处理、串行执行
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
