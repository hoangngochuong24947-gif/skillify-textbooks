# Visual Infographic Spec

## Purpose

将“从书生成 skills”的主流程整理成一张可直接渲染的中文高密度信息图。

## Rendering Preset

- Layout: `dense-modules`
- Style: `pop-laboratory`
- Aspect: `portrait`
- Language: `zh`

## Visual Direction

- 背景为灰白蓝图网格感。
- 模块色以鼠尾草绿为主，荧光粉做警示，亮黄做关键词高亮。
- 每个模块都带坐标标签和细线标注。
- 所有模块都承载信息，不留装饰性空白。

## Title Block

### 主标题

从书生成 Skills

### 副标题

用 NotebookLM MCP 抽取作者思维模型，生成可调用的方法论技能包

## Module Layout

### SEC-A1 项目目标

- 把一本高质量图书转成可调用的 skills
- 不是摘要，而是方法论资产化
- 服务 Claude Code / OpenClaw 用户

### SEC-A2 NotebookLM 提问链路

- 建 notebook
- 五段式问题包
- 串行执行
- 每轮保留证据

### SEC-B1 Subagent 分工

- Book Profiler
- Author Thinking Analyst
- Methodology Miner
- Scenario Router
- Skill Packager / QA

### SEC-B2 方法论路由

- 用户问题输入
- 判断是否适合调用本书思维
- 选择 MethodCard
- 决定 subagent 组合

### SEC-C1 输出文档体系

- `00-overview.md`
- `01-author-thinking.md`
- `02-method-catalog.md`
- `03-scenario-router.md`
- `04-subagent-playbooks.md`
- `05-master-skill-spec.md`

### SEC-C2 迭代闭环

- 弱证据降级
- 缺口回补提问
- 方法去重
- 二次打包

## Suggested Prompt

```text
Create a portrait Chinese infographic using the dense-modules layout and pop-laboratory style.
Theme: turning one great book into a reusable skill bundle.
Show six modules only: project goal, NotebookLM MCP query pipeline, subagent roles, methodology routing, Markdown output bundle, iteration loop.
Use coordinate labels like SEC-A1 and SEC-B2, blueprint grid, technical annotations, minimal whitespace, and high information density.
Avoid cute/cartoon elements and avoid decorative empty space.
```
