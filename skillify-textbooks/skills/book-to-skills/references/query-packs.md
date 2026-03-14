# Query Packs

All prompts should be explicit, narrow, and tied to a specific stage. Avoid open-ended prompts like “summarize the whole book”.

## Resource Acquisition Guide

Before running query packs, you need to get the book content into NotebookLM.

### Option 1: Direct PDF Upload (Preferred)
- If you have the book PDF, use `source_add` with `source_type=”file”`
- Wait for processing to complete before querying

### Option 2: Web Research (Fallback)
- If no PDF available, use `research_start` with `source=”web”` and query the book title
- Import relevant sources found during research
- **Note:** Web sources may be secondary; mark evidence accordingly

### Option 3: Google Drive (If available)
- If book is in Google Drive, use `source_add` with `source_type=”drive”`
- Requires document_id and proper doc_type

### Language Handling
- If original book is in English but output should be Chinese:
  - Extract content in English via NotebookLM
  - Translate key concepts while keeping original terms in parentheses
  - Example: “系统1思维 (System 1 Thinking)”
- Always preserve original terminology for accuracy

### Processing Check
Before starting Pack 1, verify:
- [ ] Notebook has at least one source
- [ ] Source status is “processed” or “completed”
- [ ] You can successfully query the source

## Pack 1: 全书结构图

### Objective

建立全书地图，明确章节递进、核心命题、关键概念和逻辑骨架。

### Questions

1. 这本书的核心命题是什么？请按章节或主题分层列出。
2. 作者是如何一步步展开论证的？请说明章节之间的递进关系。
3. 书中反复出现的关键概念有哪些？每个概念服务于什么判断任务？
4. 如果把全书压缩成一张结构图，应有哪些一级模块？

### Expected Output

- 章节地图
- 核心命题列表
- 关键概念列表
- 结构骨架说明

## Pack 2: 作者思维方式

### Objective

提炼作者如何观察问题、如何判断、如何组织分析顺序。

### Questions

1. 作者看问题时最常使用哪些分析维度？
2. 作者如何区分表象、结构、因果、约束和优先级？
3. 作者做判断时有哪些默认前提或价值排序？
4. 作者常用什么顺序展开分析：先定义问题、先找变量、先找案例，还是先给原则？

### Expected Output

- 观察框架
- 判断原则
- 分析顺序
- 作者的默认视角

## Pack 3: 方法论抽取

### Objective

把显性和隐性方法都抽出来，并合并成可重复调用的方法卡候选项。

### Questions

1. 书中直接给出的模型、步骤、框架和准则有哪些？
2. 书中没有命名但反复出现的分析套路有哪些？
3. 哪些零散观点可以组合成一个更完整的方法？
4. 如果把这些方法交给另一个人复用，最少需要保留哪些步骤与前提？

### Expected Output

- 方法候选列表
- 每项方法的步骤草稿
- 方法之间的依赖关系
- 证据出处

## Pack 4: 适用场景与边界

### Objective

建立方法和任务场景之间的路由关系。

### Questions

1. 每个方法最适合解决哪类问题？
2. 每个方法不适合处理哪些问题？
3. 哪些方法适合作为起手框架，哪些适合作为复核或补充？
4. 当用户问题模糊时，应该优先调用哪一类方法？

### Expected Output

- 方法到问题类型的映射
- 触发条件
- 禁用条件
- 组合调用建议

## Pack 5: 冲突校验与综合

### Objective

去重、降级、归并，并生成适合封装 skill 的最终骨架。

### Questions

1. 哪些方法实际上是同一种方法的不同表述？
2. 哪些方法之间存在前置依赖或互斥关系？
3. 哪些结论证据不足，需要标记为待确认？
4. 如果要把结果封装为一个 master skill，应如何组织主流程和分工？

### Expected Output

- 去重后的方法总表
- 依赖与冲突说明
- 待确认清单
- skill 封装建议
