# EduLM T2/T3 教学动作集 v0（七年级数学）

状态：初稿，2026-09-06。基于 Bridge、MathDial、2507.16252 三套体系起草，用 Bridge 20 段试标校验过一轮。待内部日志到位后用真实对话重做试标并修订为 v1。

## 1. 范围与用途

- 学科学段：数学，七年级（有理数、整式、一元一次方程、几何初步、数据初步）。动作定义本身不依赖年级，年级只影响触发条件里的错因类别和例子。
- 用途：(a) T2 评测集的标签空间；(b) T2 两段式输出的第一段（动作标签）；(c) T3 轨迹里每一步的动作记录；(d) 学生模拟器观察到的教师行为类型。
- 粒度：8 个封闭动作。这是交接文档定的 6–8 个上限，试标表明 8 个刚好覆盖，再少会把功能不同的动作揉在一起（见第 7 节）。

## 2. 设计原则

1. **按功能分，不按形式分。** Bridge 的 `ask_question` 既可能是诊断追问、也可能是带指向的提示、也可能是验证性练习，同一个形式对应三种教学意图。v0 一律按"这一步想让学生状态发生什么变化"来分类。试标里 5 个映射不一致有 3 个来自这一条。
2. **每个动作可由学生状态触发。** 触发条件必须能用第 4 节的状态字段写出来，否则模型学不到"看状态选动作"。
3. **一轮一个主动作，允许一个次动作。** 教师一句话常是"肯定 + 引导"，主动作取决定下一个学生行为的那个，次动作记录附带的。
4. **泄答案要可测。** CORRECT 动作带 `reveals_answer` 标志，T3 的奖励项直接读它。
5. **与三套公开体系可互相映射**，这样 Bridge/MathDial 能当代理评测数据。

## 3. 三套公开体系对照

| 来源 | 动作/策略集 | 特点 |
|---|---|---|
| Bridge (NAACL 2024) | 10 个策略：explain_concept, ask_question, provide_hint, provide_strategy, provide_example, provide_correction, provide_similar_problem, simplify_question, affirm_correct_answer, encourage_student；另有错因 6 类、意图 10 类 | 三层决策（错因→策略→意图），但策略层按形式分，`ask_question` 占 30%，歧义大 |
| MathDial (EMNLP 2023) | 4 大类 11 小类：Focus{seek strategy, guiding focus, recall info}, Probing{ask explanation, seek self-correction, perturb question, world knowledge}, Telling{reveal strategy, reveal answer}, Generic{greeting, general inquiry} | 七年级应用题，明确区分"引导"和"告知"，reveal answer 单列，适合测泄答案 |
| 2507.16252 | 4 个高层动作：instruct, encourage, refocus, ask a question；学生状态是 25 维向量 | 最粗，为 RL 做的；证明粗动作集也能学，但对 T2 评测太粗 |
| 交接文档 | 追问 / 提示 / 讲解 / 示例 / 练习 / 跳转 | 缺"纠错告知"和"确认推进"，试标里这两类在专家回复中占 15%，在新手导师回复中占 25% |

Bridge 全量 700 段的策略分布：ask_question 212，explain_concept 137，provide_hint 63，provide_strategy 56，provide_correction 41，provide_similar_problem 38，simplify_question 38，affirm 31，encourage 24，provide_example 20。
MathDial 2861 段教师 move 分布：focus 6808，generic 4456，probing 4252，telling 3091。

## 4. 学生状态表示 v0（结构化）

每个学生轮次之后标注一次。字段少而硬，先够用。

| 字段 | 取值 | 说明 |
|---|---|---|
| `last_response` | correct / partial / incorrect / no_answer / claims_understanding / off_task | 学生上一轮的作答性质。`claims_understanding` 单列，因为"我懂了"需要验证而不是推进 |
| `error_type` | none / careless / imprecise / misinterpret / procedure / misconception / concept_gap / fact_recall / unknown | 错因。前四类来自 Bridge；procedure（步骤错）、misconception（系统性误解）、concept_gap（没学过/不会）、fact_recall（记不住事实）是七年级数学补的；unknown 表示需要诊断 |
| `mastery` | low / mid / high / unverified | 对当前知识点的掌握估计。unverified 专门给"声称懂了"和"答对但可能是猜的" |
| `affect` | ok / frustrated / disengaged / overconfident / wants_to_quit | 情绪与投入 |
| `step_error_streak` | 整数 | 当前步骤连续错几次 |
| `hints_given` | 整数 | 当前步骤已给过几次提示 |
| `turn_index` | 整数 | 对话轮次 |

七年级错因参考（填 `error_type` 时的具体例子）：有理数运算符号错、去括号变号漏项、移项不变号、合并同类项系数加错、方程两边同除漏项、把 x 当乘号、比例关系读反、单位换算方向反。

## 5. 动作集 v0

每个动作：定义、触发条件（用第 4 节字段写）、不选它的情况、例子（Bridge 原文 + 七年级改写）、映射。

### A1 PROBE 追问诊断

- **定义**：让学生说出自己的想法、步骤或依据，或提一个诊断性子问题，目的是搞清学生状态。不给任何内容。
- **触发**：`error_type = unknown`；或 `last_response = incorrect` 且只给了裸答案没有过程；或 `last_response = correct` 但 `mastery = unverified` 怀疑是猜的。
- **不选它**：错因已经明确时不要再问，直接进 HINT / EXPLAIN。连续 PROBE 两次学生仍答不上来时停止。
- **例子**：Bridge 6166030_16，学生把体积公式答成"the volume is 5"，专家："Could you let me know how you got 5?"。七年级：解 3x − 5 = 7 学生答 x = 2/3，教师："你是怎么算出 2/3 的？把第一步写给我看。"
- **映射**：Bridge ask_question(+diagnose_mistake / elaborate_answer)；MathDial Probing{ask explanation}、Generic{general inquiry "walk me through"}；2507 ask a question。

### A2 HINT 提示引导

- **定义**：给一个带指向的线索让学生自己纠错或走出下一步：指出错误位置、提醒相关信息、把问题换个说法或降一级难度、给验算方法。不说出答案，不完整讲规则。
- **触发**：`error_type ∈ {careless, imprecise, misinterpret}` 或 `error_type = procedure` 且 `mastery ≥ mid`；`hints_given ≤ 1`。学生有正确思路、差一小步。
- **不选它**：`hints_given ≥ 2` 且 `step_error_streak ≥ 2` 时提示已无效，升级到 EXPLAIN；`error_type ∈ {concept_gap, misconception}` 时提示不解决根本问题。
- **例子**：Bridge 6348278_24，学生 57 − 5 算成 53，专家："To check your work you could add 53 to 5 and you should get 57"。七年级：学生解 2(x + 3) = 10 去括号得 2x + 3 = 10，教师："括号里有两项，2 要乘给每一项，再看看 3 前面。"
- **映射**：Bridge provide_hint、simplify_question、ask_question(+hint_mistake)、provide_strategy(+hint_mistake)；MathDial Focus 全部三类、Probing{seek self-correction}。

### A3 EXPLAIN 讲解

- **定义**：直接教概念、规则、方法或解题程序，可以附一两个小例说明规则，但不完整演示一道同类题。
- **触发**：`error_type ∈ {concept_gap, misconception}`；或 HINT 已用 2 次仍 `step_error_streak ≥ 2`；或学生明确说"不会/没学过"。
- **不选它**：学生只是粗心或差一步时讲解是过度帮助，浪费学习机会（ES-LLMs 里的"掌握度增益悖论"）。
- **例子**：Bridge 2962429_51，学生把代数式里的 x 当乘号，专家："In arithmetic, the x means multiplication, but in algebra, the x represents a variable"。七年级：学生认为 −3 − 5 = −2，教师讲"减去一个数等于加上它的相反数，−3 − 5 = −3 + (−5)，同号相加取相同符号再把绝对值相加"。
- **映射**：Bridge explain_concept、provide_strategy(通用方法)；MathDial Telling{reveal strategy}；2507 instruct。

### A4 EXAMPLE 示例类比

- **定义**：在原题**尚未解决**时，引入一个更简单或同构的实例来搭脚手架。可以是教师演示一道例题，也可以是让学生先做一个简化版实例，做完再回到原题。
- **触发**：EXPLAIN 之后学生仍不能应用；或概念抽象、直接讲解无效；或 `error_type = concept_gap` 且题目可降维。
- **不选它**：原题已经解决后再给题是 PRACTICE 不是 EXAMPLE。区分标准只有一条：原题解决前的类比是 EXAMPLE，解决后的新题是 PRACTICE。
- **例子**：Bridge 6165902_95，学生答 7 在 9 和 15 之间，专家："Let's look at a similar problem. Is 10 between 15 and 18?"。七年级：学生不会解 5x − 2 = 3x + 4，教师："先看一道简单的：x + 2 = 5，x 等于几？怎么把 2 弄到右边去的？用同样的办法处理 3x。"
- **映射**：Bridge provide_example、provide_similar_problem(原题未解决时)；MathDial 无对应（最接近 Focus{guiding focus}）。

### A5 PRACTICE 练习验证

- **定义**：当前题解决后，或学生声称已懂时，给一道新的同类或变式题让学生独立做，用于巩固、迁移或验证。
- **触发**：`last_response = claims_understanding`；或 `last_response = correct` 且 `mastery = unverified`；或当前题已解决、时间允许。
- **不选它**：原题没解决时给新题会打断，除非目的是诊断（这种情况归 PROBE 的诊断子问题或 EXAMPLE）。
- **例子**：Bridge 2979999_58，学生说"yes"懂了，专家："Ok great! Let's try to find a fraction equivalent to 4/5"。七年级：学生刚在教师帮助下解出 3x − 5 = 7，教师："自己试一道：4x + 3 = 15。"
- **映射**：Bridge provide_similar_problem(原题已解决)、ask_question(+understand_topic 且是新题)；MathDial Probing{perturb question}。

### A6 CORRECT 纠错告知

- **定义**：明确指出错在哪并直接给出正确的那一项：小修正、说法修正、事实告知，直到最后手段的报答案。带 `reveals_answer` 标志：给出的是当前题最终答案时为 true。
- **触发**：`error_type ∈ {imprecise, fact_recall}`，错误不值得绕路；或 `error_type = careless` 且学生已自查一次仍没发现；或 `hints_given ≥ 2` 且 `step_error_streak ≥ 3` 且时间用尽（此时 reveals_answer = true，是 T3 里被惩罚的动作）。
- **不选它**：学生有正确思路时告知会剥夺自纠机会，先 HINT。这是新手导师最常见的错误动作（试标里新手导师 25% 的回复是 CORRECT 且多数泄答案）。
- **例子**：Bridge 2916342_42，学生说 7 的值是 2,000，专家："It's in the thousands place. We can just say thousands, but it would be wrong to say 2,000"。七年级：学生把 (−2)² 写成 −4，已提示一次仍没改，教师："(−2)² 是 (−2) × (−2) = 4，负负得正。−2² 才是 −4。"
- **映射**：Bridge provide_correction、explain_concept(只告知事实不讲理由时)；MathDial Telling{reveal answer}。

### A7 AFFIRM 确认推进

- **定义**：确认学生答对或步骤正确，并推进到下一步、下一问或收尾。
- **触发**：`last_response = correct` 且 `mastery ≥ mid`（不需要验证）。
- **不选它**：`mastery = unverified` 时先 PRACTICE 或 PROBE；答对但过程有问题时先 HINT。
- **例子**：Bridge 2916344_54，学生答"hudrid"(hundreds)，专家："Great! The 5 is in the hundreds spot."。七年级："对，x = 4。代回去验一下左边等不等于 7，然后我们看下一题。"
- **映射**：Bridge affirm_correct_answer；MathDial Generic(肯定类)；2507 encourage(部分)。

### A8 MANAGE 反馈调控

- **定义**：不含教学内容的一切：纯评价反馈（"不对，再检查一下"）、情绪鼓励、把跑题学生拉回来、开场/结束/流程说明。
- **触发**：`affect ∈ {frustrated, disengaged, wants_to_quit}`；`last_response = off_task`；对话开始或结束。
- **不选它**：学生答错且情绪正常时，只说"不对再试试"是无效动作。试标里新手导师 60% 的回复属于此类，专家只有 0%。这个对比本身是 gap 图的素材。
- **例子**：Bridge 原导师回复大量属于此类："That was a good try. Please recheck your work"。七年级："这道题确实绕，你前两步都是对的，休息一下我们再看第三步。"
- **映射**：Bridge encourage_student、"End session"等自由文本；MathDial Generic{greeting/farewell}；2507 encourage、refocus。

## 6. 决策启发式（状态 → 动作）

标注时的判断顺序，也是后面规则基线的雏形。从上往下第一条命中的生效。

| 序 | 条件 | 动作 |
|---|---|---|
| 1 | affect ∈ {frustrated, disengaged, wants_to_quit} 或 last_response = off_task | MANAGE |
| 2 | last_response = correct 且 mastery ≥ mid | AFFIRM |
| 3 | last_response ∈ {correct, claims_understanding} 且 mastery = unverified | PRACTICE |
| 4 | error_type = unknown 或 裸答案无过程 | PROBE |
| 5 | error_type ∈ {imprecise, fact_recall} | CORRECT (reveals_answer = false) |
| 6 | error_type ∈ {careless, misinterpret, procedure} 且 hints_given ≤ 1 | HINT |
| 7 | error_type ∈ {concept_gap, misconception} 或 hints_given ≥ 2 | EXPLAIN |
| 8 | EXPLAIN 后仍错 | EXAMPLE |
| 9 | hints_given ≥ 2 且 step_error_streak ≥ 3 且时间用尽 | CORRECT (reveals_answer = true) |

## 7. 试标结果（Bridge 20 段，分层抽样，seed 7）

文件：`data/annotation/bridge_trial20.annotated.jsonl`，脚本：`scripts/trial_agreement.py`。

**覆盖**：20 段全部能标，没有落到"其他"的。专家回复动作分布：HINT 7、PROBE 3、EXPLAIN 3、PRACTICE 3、CORRECT 2、EXAMPLE 1、AFFIRM 1。新手导师原回复分布：MANAGE 12、CORRECT 5、EXPLAIN 2、HINT 1。

**与 Bridge 标签的一致率**：

| 映射方式 | 一致 |
|---|---|
| 只用 strategy 字段做朴素映射 | 12/20 = 60% |
| strategy + intent 联合映射 | 15/20 = 75% |

**5 个不一致的原因**：

| 段 | Bridge | v0 | 原因 |
|---|---|---|---|
| 4233340_58 | explain_concept | CORRECT | 专家只告知"一分钟 60 秒"，没讲道理。Bridge 不区分讲解和告知 |
| 2927541_87 | explain_concept | PROBE | 专家实际回复是"what makes you say that?"，Bridge 标签与专家回复本身不符 |
| 2979999_58 | ask_question/motivate | PRACTICE | 学生声称懂了，专家出新题验证。Bridge 把它当提问 |
| 4055603_31 | ask_question/understand_topic | PRACTICE | 同上，答对后要另一个例子 |
| 2939758_51 | encourage_student | HINT | "对，是风筝！它的对称轴在哪？"主动作是把焦点拉回问题，肯定只是次动作 |

结论：不一致全部来自 Bridge 按形式分类，没有一例是 v0 定义漏洞。75% 可以作为 Bridge 映射到 v0 的噪声上限，用 Bridge 做代理评测时要在论文里说明。

**试标后对 v0 的三处修订**（已并入上文）：

1. 增加 `last_response = claims_understanding` 状态值和 PRACTICE 的验证触发条件。20 段里 3 段是这种情况，原稿没覆盖。
2. EXAMPLE 与 PRACTICE 的边界改为"原题是否已解决"，原稿按"教师演示 vs 学生做"分，6165902_95 和 6136439_9 标不清。
3. MANAGE 明确纳入"纯评价反馈无内容"。原稿只有鼓励和流程，新手导师 60% 的回复无处可放。

## 8. 标注规则

1. 标注对象是**教师的一整轮**（连续多条消息合并），不是单条消息。
2. 主动作取"决定学生下一步做什么"的那个；附带的肯定、鼓励记为次动作。
3. 先填学生状态再选动作，状态字段不允许空。
4. CORRECT 必须填 `reveals_answer`。
5. 拿不准时记录到 notes，不要硬选；notes 是修订动作集的主要输入。

## 9. 已知问题与待拍板

- **HINT 内部粒度**。HINT 占专家回复 35%，内部至少有三种（指出位置、换说法降难度、给验算方法）。v0 不拆，T2 评测跑完看混淆矩阵，如果模型在 HINT 上一致率虚高再拆。
- **MANAGE 是否拆成 ENCOURAGE 和 TRANSITION**。对 T3 的情绪建模可能需要，对 T2 暂时不需要。
- **多标签**。v0 用主次两个槽位；如果内部日志里一轮三个动作的比例高，改为多标签。
- **状态字段的标注成本**。7 个字段逐轮标 200 段约 800 轮，估计 15 到 20 小时。可以先让 27B 预标、人工改。
- Bridge 和 MathDial 都是英文、小学到七年级难度，映射噪声上限 75%，只能做 gap 实验不能做主表。

## 10. 文件清单

| 文件 | 内容 |
|---|---|
| `docs/action_set_v0.md` | 本文档 |
| `data/action_set_v0.json` | 机器可读的动作、状态字段、映射表，评测脚本直接读 |
| `scripts/sample_bridge_trial.py` | Bridge 分层抽样并生成标注模板 |
| `data/annotation/bridge_trial20.template.jsonl` | 空模板 |
| `data/annotation/bridge_trial20.annotated.jsonl` | 20 段试标结果 |
| `scripts/trial_agreement.py` | 与 Bridge 标签的一致率与不一致清单 |
| `data/raw/bridge`, `data/raw/mathdial` | 公开数据原始仓库 |
