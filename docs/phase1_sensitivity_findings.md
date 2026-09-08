# 阶段 1 实验 A：Qwen3.8-27B 状态敏感度测试

日期：2026-09-06。原始输出 `results/sensitivity/*.jsonl`，汇总 `results/sensitivity/report.md`，图 `results/sensitivity/action_by_state.png`。复现：

```bash
.venv/bin/python scripts/run_sensitivity.py --thinking off --temperature 0 --n 1 --tag nothink_t0
.venv/bin/python scripts/run_sensitivity.py --thinking off --temperature 0.7 --n 5 --tag nothink_t07
.venv/bin/python scripts/run_sensitivity.py --thinking on --temperature 0.6 --n 3 --tag think_t06
.venv/bin/python scripts/analyze_sensitivity.py results/sensitivity/nothink_t0.jsonl results/sensitivity/nothink_t07.jsonl results/sensitivity/think_t06.jsonl
```

## 1. 问题

文献说通用模型"不随学生状态变化"（2508.06583 的设计：固定历史、只变学生状态）。这里验证 Qwen3.8-27B 在我们的动作集上是否如此，以及它在哪些维度上敏感、哪些维度上不敏感。

## 2. 设计

- **场景**：12 道七年级数学题（有理数、整式、一元一次方程、几何初步、科学记数法、应用题），每个场景的对话历史固定为"老师出题，学生给一个错误的裸答案"。见 `data/sensitivity/scenarios.json`。
- **状态变体**：同一历史配 7 种学生状态块，其中一种是无状态对照。状态用动作集 v0 的结构化字段表示，外加一句自然语言说明。

| 变体 | 关键字段 | 启发式期望动作 |
|---|---|---|
| ctrl | 不给状态 | 无 |
| unknown | error_type=unknown，只给了裸答案 | PROBE |
| careless | error_type=careless，mastery=mid，近期正确率 85% | HINT |
| misconception | error_type=misconception，mastery=low，近期正确率 20% | EXPLAIN |
| escalate | error_type=procedure，已提示 2 次仍错 | EXPLAIN 或 EXAMPLE |
| frustrated | affect=frustrated，连续错 3 次，说"不想做了" | MANAGE |
| timeout | 已提示 3 次，剩余时间不足 1 分钟 | CORRECT |

- **输出格式**：两段式，先动作 ID 再回复。系统提示里给出 8 个动作的定义。
- **配置**：不思考贪心（n=1）、不思考采样 T=0.7（n=5）、思考 T=0.6（n=3）。共 756 次生成。
- **指标**：动作分布；状态符合率（选中期望动作的比例）；讲解/告知率（EXPLAIN + CORRECT）；泄答案率（回复文本里出现本题最终答案）。

## 3. 结果

### 3.1 动作分布（不思考、采样 T=0.7，n=420，单位 %）

| 状态 | PROBE | HINT | EXPLAIN | CORRECT | AFFIRM | MANAGE |
|---|---|---|---|---|---|---|
| ctrl | 55 | 5 | 0 | 30 | 10 | 0 |
| unknown | 98 | 2 | 0 | 0 | 0 | 0 |
| careless | 38 | 15 | 0 | 47 | 0 | 0 |
| misconception | 57 | 28 | 0 | 15 | 0 | 0 |
| escalate | 18 | 8 | 20 | 53 | 0 | 0 |
| frustrated | 0 | 0 | 0 | 0 | 2 | 98 |
| timeout | 0 | 0 | 0 | 100 | 0 | 0 |

### 3.2 三种配置的符合率 / 泄答案率（单位 %）

| 状态 | 期望 | 不思考贪心 符合/泄 | 不思考采样 符合/泄 | 思考 符合/泄 |
|---|---|---|---|---|
| unknown | PROBE | 100 / 0 | 98 / 0 | 100 / 0 |
| careless | HINT | 17 / 50 | 15 / 37 | 49 / 19 |
| misconception | EXPLAIN | 0 / 0 | 0 / 12 | 3 / 17 |
| escalate | EXPLAIN 或 EXAMPLE | 17 / 83 | 20 / 60 | 0 / 97 |
| frustrated | MANAGE | 100 / 0 | 98 / 2 | 42 / 11 |
| timeout | CORRECT | 100 / 100 | 100 / 88 | 100 / 97 |
| ctrl | 无 | – / 8 | – / 18 | – / 31 |

思考模式有 8 次输出为空（多在 ctrl 组），已计入 PARSE_FAIL，不影响结论。

## 4. 发现

**发现 1：模型对"表面信号"敏感，对"教学信号"不敏感。**
情绪（frustrated）、时间（timeout）、无过程（unknown）这三种状态，模型几乎 100% 按预期切换动作。但错因和掌握度这两个字段基本不起作用：`careless` 和 `misconception` 两种状态在模型眼里差别很小，都是"先追问，或者直接报答案"。而错因和掌握度恰恰是 T2 个性化的核心维度。

**发现 2：EXPLAIN、EXAMPLE、PRACTICE 三个动作几乎不用。**
756 次生成里 EXAMPLE 和 PRACTICE 合计出现 3 次，EXPLAIN 在三种配置里占比都低于 10%。模型的动作空间实际只有 PROBE、CORRECT、MANAGE 三个。系统提示里明明给了 8 个动作的定义，模型也不用。

**发现 3：升级路径是"追问 → 报答案"，跳过了讲解和示例。**
`escalate` 状态（已提示两次仍错）下，模型 53% 到 100% 选 CORRECT，泄答案率 60% 到 97%。教学上此时应该讲解或换一个简化实例，模型直接放弃引导。这是文献里"会讲不会选"和"过度帮助"的直接证据。

**发现 4：`careless` 状态下的过度帮助。**
状态明确告诉模型"近期正确率 85%，本次是粗心"，模型仍有 47% 直接报答案。对一个只是粗心的学生，一句提示就够，报答案是最差的动作，因为剥夺了自纠机会（ES-LLMs 的"掌握度增益悖论"）。

**发现 5：思考模式没有帮助，部分维度更差。**
思考模式把 careless 的符合率从 15% 提到 49%，但 escalate 的泄答案率升到 97%，frustrated 的符合率从 98% 降到 42%（模型在思考里自己说服自己"学生烦躁但还是应该继续教"）。无状态对照组的泄答案率也从 18% 升到 31%。思考让模型更倾向于"把题讲完"。

## 5. 与文献三个现状的对应

| 文献说法 | 本实验证据 | 强度 |
|---|---|---|
| 会讲不会选，直接给答案 | escalate 下泄答案 60% 到 97%；careless 下 37% 到 50%；无状态时 8% 到 31% | 强 |
| 不随学生状态变化 | 情绪和时间维度敏感；错因和掌握度维度不敏感。需要改说法为"只对表面信号敏感" | 中，比文献说法更细 |
| 多轮后退化 | 本实验是单轮，未测 | 未测 |

## 6. 局限

- 期望动作来自 v0 的启发式表，不是人工标注的金标准。`misconception → EXPLAIN` 有争议，先 PROBE 一次也说得通。但 `escalate → CORRECT` 和 `careless → CORRECT` 的问题不依赖这个争议。
- 12 个场景是自己写的，学生错误都是"裸答案"，没有过程。有过程的错误可能让模型更容易判断错因，敏感度可能更高。
- 状态以文本形式喂给模型，模型是否信任这段文本本身是个变量。真实部署时状态由系统推断，这一点会保持一致。
- 只测了一个模型。需要补一个前沿 API 和一个小模型（Qwen3-8B 级）做对照，否则不知道这是 27B 的问题还是所有模型的问题。
- 泄答案检测是正则匹配最终答案，对"x + 6"这类会漏掉写法变体，实际泄答案率只会更高。

## 7. 候选含义（未经验证，不得作为结论引用）

本节在 2026-09-06 修订。原稿把下面几条写成了确认的贡献点，这是过度声明：期望动作来自作者自写的启发式表，模型不符合这张表不等于不符合专家；只测了一个模型、一版手写提示词，不能得出"prompt 做不到、要靠训练"。

**不依赖启发式表的观察（描述性事实）：**
- 动作空间坍缩：EXPLAIN、EXAMPLE、PRACTICE 三个动作合计占比不到 10%。
- 状态不敏感：`careless` 与 `misconception` 两种状态下模型的动作分布几乎相同。

**要把观察变成短板，必须先过两个门槛：**
1. **专家标注门槛**：两位七年级数学老师在同一批场景和状态上标注应选动作，证明专家动作确实随错因和掌握度变化，且两人之间一致。若动作标签不变但提示内容变化，说明 v0 动作集太粗，应修动作集。Bridge 700 段里专家策略随错因变化（guess→explain_concept、careless→provide_correction、imprecise→affirm 最多）是支持性证据，但学段、语言、分类体系不同，只能算迁移线索。
2. **强基线门槛**：前沿模型（最好是项目最终的目标模型）加优化过的提示词，在专家标注上仍明显落后于老师。过不了这一关，T2 的训练故事不成立。

**两个门槛都过之后才成立的候选贡献：**
- 让错因和掌握度进入决策；让升级路径从"追问、报答案"变成"追问、提示、讲解、示例、报答案"。这两件事已有工作用规则阶梯和 DPO 碰过，作为目标不新；可能新的是"从真实专家日志学出的策略"，需要内部日志。
- SFT 与 DPO 数据的重点状态是 careless / misconception / escalate。
- "状态符合率"与"泄答案率"作为 T2 评测列，前提是符合率的参照换成专家标注而非启发式表。

在两个门槛有答案之前，不写训练代码。

## 8. 下一步

- 补对照模型：一个前沿 API、一个 Qwen3-8B 级小模型，同一脚本跑，出三模型对比图。
- 实验 B：Bridge 代理评测。把 Bridge 700 段映射到 v0 标签，测三个模型的动作一致率和混淆矩阵，验证发现 2（动作空间坍缩到三个）在真实对话上是否成立。
- 实验 C：多轮泄答案测试。prompt 扮演模拟学生，在 12 个场景上跑 5 到 8 轮，测泄答案轮次和多轮退化。
- 把 12 个场景扩到 30 个，加入带过程的错误作答，重跑一次看敏感度是否变化。
