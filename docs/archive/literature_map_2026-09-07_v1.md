# 文献对照表（骨架，待逐篇核）

建于 2026-09-06。用途：形成你自己能辩护的心智框架；填完即 related work 的骨架。

## 阅读顺序（2026-09-07 从被删会话恢复；先按这个读，读完再动下面的表）

原则：带着杀死空位的目的读，不是确认。第一层每篇读完写一句"这篇是否已做我们打算做的事"，写不出"否"的理由就说明空位不成立。预算两天，这两天不阻塞任何事。

**先读：教育第一层 6 篇，逐段读，按此顺序**
1. 2507.16252 Efficient RL for conversation-level outcomes（L1-1）：结构上最接近的对手，潜在状态 → 高层动作 → 条件生成。第一个要回答的问题：它和我们的差别够不够撑一篇论文。
2. 2605.27088 LLMs Are Already Good Tutors（L1-2）：门槛二的对手。看清提示词优化怎么做、评什么、承认了什么代价。
3. 2507.06910 BEA 2025 预测专家策略（L1-3）：和 T2 最像。它失败是模型问题还是目标多解？报没报标注者一致率？
4. 2607.19371 脚手架坍缩（L1-4）：已定义了我们的发现 3。我们相对它多了什么？
5. TutorMoments（L1-5）：真实日志上的决策点，第二代理评测集候选。
6. Bridge 重读（L1-6）：有没有报老师一致率；微调模型为什么"差到没法报数"；GPT-4 的 32% 等于多数类基线意味着什么。

**再读：通用 G1 4 篇，获奖或 oral 且结构对应**
7. CollabLLM（ICML 2025 Outstanding）：会话级奖励 + 模拟用户。
8. LLMs Get Lost in Multi-Turn Conversation（ICLR 2026 Outstanding）：多轮退化的评测协议，实验 C 要对齐它。
9. SOTOPIA（ICLR 2024 Spotlight）：轨迹级目标达成评测的模板。
10. Debating with More Persuasive LLMs（ICML 2024 Best Paper）：弱对手 + 会话级结果；对应最弱，最后读。

**然后：第二层，只读方法和主表**
教育 L2 9 篇（PEARL、2505.15607、2606.21502、GuideEval、2606.15766、2601.04025、ES-LLMs、EduClaw-Bench、Tutor CoPilot）；通用 G2 14 篇，其中 PPDPP、ArCHer、ACT、TRIP、Abdulhai 人设一致性、Sycophancy 六篇优先。

**最后：第三层只读摘要。**

读完要交的三样东西见文末：对照表、"空位在哪"一段、基线清单。

---

## 使用规则

1. 每篇一个块，字段固定。你读一篇填一块，填完把块首的 `[ ] 待核` 改成 `[x] 已核 <日期>`。
2. 标着"另一会话摘要（未核）"的句子是另一个 Claude 会话从网页搜索得来的主张。它已经把 Bridge 说错过一处。**读的目的是证伪这些句子，不是确认。**
3. 每篇最后一个字段"是否已做我们打算做的事"必须写出"否"的理由。写不出来，就说明空位不成立，直接告诉我。
4. 会议、获奖、开源信息由子任务核实后填入，标"已核"。没标的一律当未核。
5. 第一层逐段读，第二层读方法与主表，第三层只读摘要。

我们打算做的事，一句话，作为每篇对照的基准：
> 从真实专家日志学一个策略，输入结构化学生状态（错因、掌握度等），输出显式教学动作，并证明它比强提示的前沿模型更接近专家、且带来更高的多轮学习增益。

## 固定字段

```
标题 / ID / 会议（核实状态）
任务定义：
数据：真实 or 模拟；学段；语言；规模
动作标签：有/无；标签集是什么
状态条件：有/无；状态怎么表示、从哪来
方法：训练 or 提示；具体
评测指标：
自认局限：
可用产物：代码 / checkpoint / 数据（能否直接跑在我们的评测集上）
另一会话摘要（未核）：
是否已做我们打算做的事：否/是/部分 + 理由
对我们的作用：门槛二对手 / 代理评测集 / T3 参考 / related work / 无
我的感悟：（事实之外的判断：这篇的失败原因是什么、哪个指标我们不能用、它改变了我对空位的看法吗）
```

---


### 会议核实后的质量分层（2026-09-07 核）

同行评审的顶会正文只有 4 篇：Bridge（NAACL 2024）、2505.15607（EMNLP 2025 oral）、MathTutorBench（EMNLP 2025 oral）、2601.04025（ACL 2026）。次一级：MathDial（EMNLP 2023 Findings）、ES-LLMs（AIED 2026）、2606.20138（EMNLP 2026 Industry）、两篇 workshop。
其余 13 篇全部是 arXiv 预印本，其中 GuideEval 被 ICLR 2026 拒稿，4 篇是单作者且无代码。

含义：另一会话用来论证"空位"和"对手"的几篇（2605.27088 提示词优化、2607.19371 脚手架坍缩、PEARL、两篇规则阶梯）都还没过同行评审。它们的结论要打折，但 2605.27088 作为门槛二的对手不能因此免掉，因为审稿人会问同样的问题。

## 第一层：逐段读（决定门槛与定位）

### [ ] 待核  L1-1  Efficient RL for optimizing conversation level outcomes with an LLM-based tutor — 2507.16252（Nam et al.）
- 会议（已核）：arXiv only；同作者另一标题版本进了 NeurIPS 2025 Multi-Turn Interactions workshop。无代码
- 任务定义：
- 数据：
- 动作标签：本会话从摘要页核到：4 个高层动作 instruct / encourage / refocus / ask a question
- 状态条件：本会话核到：25 维潜在状态向量，由 LLM 从对话历史抽取（参与度、进度、情绪、交互模式、教学历史、轮次）
- 方法：本会话核到：在潜在状态上训长期策略选高层动作，奖励 +1/−1（是否在 20 轮内解出）
- 评测指标：
- 自认局限：
- 可用产物：
- 另一会话摘要（未核）：另一会话的"空位"论证**没有提到这篇**。
- 是否已做我们打算做的事：**这是最接近的一篇**：潜在状态 → 高层动作 → 条件生成，RL 训练。差别候选：动作只有 4 个且粗；状态是 LLM 抽的向量不是错因/掌握度；奖励来自模拟结果不是专家决策；数据非真实日志。你要判断这些差别够不够撑起一篇论文。
- 对我们的作用：直接对手 + T2/T3 架构模板
- 我的感悟：

### [ ] 待核  L1-2  LLMs Are Already Good Tutors: Training-Free Prompt Optimization for Pedagogical Math Tutoring — 2605.27088（Unggi Lee et al.）
- 会议（已核）：arXiv only（2026-05）。代码只有匿名 4open.science 链接。与 EduClaw-Bench 同一组
- 任务定义：
- 数据：
- 动作标签：
- 状态条件：
- 方法：
- 评测指标：
- 自认局限：
- 可用产物：（关键：提示词优化代码是否开源，能否直接跑在我们的探针集上）
- 另一会话摘要（未核）：提示词优化在后测通过率、泄答案控制、有帮助性三项上超过 RL 训练的基线；代价是意图层面的脚手架行为低约 10 个百分点。
- 是否已做我们打算做的事：
- 对我们的作用：**门槛二的对手**。它的优化方法就是我们必须补的强基线。
- 我的感悟：

### [ ] 待核  L1-3  Exploring LLMs for Predicting Tutor Strategy and Student Outcomes in Dialogues — 2507.06910（Ikram et al.）
- 会议（已核）：BEA 2025 workshop。无代码
- 任务定义：
- 数据：
- 动作标签：
- 状态条件：
- 方法：
- 评测指标：
- 自认局限：
- 可用产物：
- 另一会话摘要（未核）：GPT-4o 和 Llama 3 都预测不好专家下一步策略，作者明说需要更强的方法。
- 是否已做我们打算做的事：（重点：它失败是模型问题，还是目标多解？它报没报标注者一致率？）
- 对我们的作用：T2 作为"动作预测"的最近工作；它的失败要能解释
- 我的感悟：

### [ ] 待核  L1-4  Mitigating Scaffolding Collapse in Socratic Tutors via Representation Alignment — 2607.19371（Jing Shao et al.）
- 会议（已核）：arXiv only，自述 under review（2026-06 提交）。无代码。注意：方法主体是表示对齐损失，DPO 只是其中一部分，另一会话的概括不准
- 任务定义：
- 数据：
- 动作标签：
- 状态条件：
- 方法：
- 评测指标：
- 自认局限：
- 可用产物：
- 另一会话摘要（未核）：定义"脚手架坍缩"（多轮后从引导退化成报答案），Qwen3-8B 上 68% 对话坍缩，带轨迹权重的 DPO 降到 32%。
- 是否已做我们打算做的事：（我们的发现 3 是它已定义的现象；我们相对它多了什么？）
- 对我们的作用：related work 必引；T3 泄答案指标可对齐
- 我的感悟：

### [ ] 待核  L1-5  TutorMoments / "When Help is Unhelpful: Evaluating AI Tutors for Productive Struggle"（Ai2，Albert Zhang 等 13 人，含 Jacob Andreas、Susanna Loeb）
- 会议（已核）：**没有 arXiv 号**，working paper，HF 数据卡写"paper in preparation"。数据已放出：huggingface.co/datasets/allenai/tutormoments-preview（CC BY 4.0，462 段、520 个决策点、7280 次 replay），代码 github.com/allenai/tutormoments。引用按 Zhang et al. 2026 working paper
- 任务定义：
- 数据：另一会话称 462 段真实辅导记录
- 动作标签：另一会话称标了"该帮还是该放手"的决策点
- 状态条件：
- 方法：
- 评测指标：
- 自认局限：
- 可用产物：（数据能否下载，是第二代理评测集的前提）
- 另一会话摘要（未核）：模型默认过度帮助，把权衡写进提示词能改善但追不上人。
- 是否已做我们打算做的事：
- 对我们的作用：第二个代理评测集候选；"真实日志 ≠ 基准"论点的证据
- 我的感悟：

### [ ] 待核  L1-6  Bridge — 2310.10648，NAACL 2024（已核，代码与数据已放出）
- 任务定义：本会话已核：错因 → 策略 → 意图三层专家决策，700 段真实辅导对话
- 数据：真实；美国小学到初一；英文；train 419 / val 71 / test 210
- 动作标签：10 个策略（形式分类，ask_question 占 30%）
- 状态条件：错因 6 类，由专家事后标注
- 方法：GPT-4 提示 + 专家决策；也微调了 Flan-T5 和 GODEL 预测决策，论文称"效果差到没法报数"
- 评测指标：人评偏好；决策路径熵
- 本会话核到的关键事实：**没有报告标注者一致率**；GPT-4 预测专家策略准确率 32% = 多数类基线，200 次里 170 次猜 ask_question
- 可用产物：数据、GPT-4 输出、微调模型输出，已在 data/raw/bridge
- 另一会话摘要（未核）：**"只是 GPT-4 提示，没训"，此句错误**，见上。
- 是否已做我们打算做的事：
- 对我们的作用：T2 模板；代理评测集；32% 这个数是"专家动作可预测性"的基准
- 我的感悟：

---

## 第二层：读方法与主表（T3 地形、评测有效性）

### [ ] 待核  L2-1  PEARL: Training Socratic Tutors with Pedagogically Aligned RL — 2605.29582（Qikai Chang，USTC/讯飞）
- 会议（已核）：arXiv only（v2 2026-09-01）。无 checkpoint（HF 链接只有基线模型）
- 另一会话摘要（未核）：Qwen3-30B 底座；模拟器带知识图上的掌握状态和五维认知画像；八维奖励；MathDial 和 MathTutorBench 上大幅超基线；自认局限是模拟器没有长期学习动态；策略只看对话历史，不输出动作标签。
- 其余字段：
- 是否已做我们打算做的事：
- 对我们的作用：T3 现成模拟器与奖励的候选；不复现，有 checkpoint 就跑
- 我的感悟：

### [ ] 待核  L2-2  From Problem-Solving to Teaching Problem-Solving: Aligning LLMs with Pedagogy using RL — 2505.15607（Dinucu-Jianu & Macina，ETH）
- 会议（已核）：**EMNLP 2025 Main, oral**。代码 github.com/eth-lre/PedagogicalRL
- 本会话从摘要核到：7B 在线 RL，模拟学生，可控奖励权重平衡教学支持与解题准确率，接近 LearnLM
- 其余字段：
- 是否已做我们打算做的事：
- 对我们的作用：T3 参考；"小模型追平大模型"叙事的先例
- 我的感悟：

### [ ] 待核  L2-3  Towards Pedagogically Aligned LLM Tutors for Math Mistake Remediation — 2606.21502（Petukhova）
- 会议（已核）：arXiv only。代码在正文里：github.com/Kpetyxova/towards-aligned-math-tutor（Qwen3-4B/8B，SFT+DPO）
- 另一会话摘要（未核）：Qwen3-8B 做错误补救，DPO；不预测动作。
- 其余字段：
- 是否已做我们打算做的事：
- 对我们的作用：有 checkpoint 则作基线
- 我的感悟：

### [ ] 待核  L2-4  Discerning minds or generic tutors? (GuideEval) — 2508.06583（Ying Liu）
- 会议（已核）：arXiv only。**ICLR 2026 被拒**，现在 ARR 2026-05 轮。无代码。它微调了 Qwen3-8B（SFT/DPO/KTO）
- 交接文档已列。设计：固定历史、变学生状态。实验 A 的方法来源。
- 其余字段：
- 是否已做我们打算做的事：
- 对我们的作用：敏感度评测协议来源
- 我的感悟：

### [ ] 待核  L2-5  Rethinking Scaffolding in LLM Tutors: The Interactional Mismatch Between Benchmarks and Real-World Deployments — 2606.15766（Neagu）
- 会议（已核）：ICML 2026 Pluralistic Alignment workshop。无代码。**另一会话的"九千多段真实对话"不准**：9,490 段来自 9 个数据集，混合基准和真实部署
- 另一会话摘要（未核）：分析九千多段真实对话；基准假设学生会跟着脚手架走，真实学生经常绕过。
- 其余字段：
- 是否已做我们打算做的事：
- 对我们的作用：内部日志价值的论据
- 我的感悟：

### [ ] 待核  L2-6  Simulated Students in Tutoring Dialogues: Substance or Illusion? — 2601.04025（Scarlatos，UMass）
- 会议（已核）：**ACL 2026**。代码 github.com/umass-ml4ed/sim-student-eval
- 其余字段：
- 对我们的作用：T3 模拟器有效性的质疑，模拟器必须回应
- 我的感悟：

### [ ] 待核  L2-7  ES-LLMs：From Untamed Black Box to Interpretable Pedagogical Orchestration — 2603.23990（Nizam Kadir，单作者）
- 会议（已核）：AIED 2026 full paper，Springer LNCS 已出。无代码
- 交接文档已列：决策与生成解耦；"掌握度增益悖论"（过度帮助虚增分数）。
- 其余字段：
- 对我们的作用：解耦架构先例；评测里必须防的悖论
- 我的感悟：

### [ ] 待核  L2-8  EduClaw-Bench: A Long-Horizon Benchmark for Pedagogical LLM Agents with Simulated Learners — 2608.03206（Unggi Lee）
- 会议（已核）：arXiv only。代码只有匿名链接
- 交接文档已列：KT 驱动 30 天模拟学生，长程评测。
- 其余字段：
- 对我们的作用：T3 模拟器升级路线
- 我的感悟：

### [ ] 待核  L2-9  Tutor CoPilot: A Human-AI Approach for Scaling Real-Time Expertise — 2410.03017（Rose Wang）
- 会议（已核）：截至今日仍是 working paper（Annenberg EdWorkingPaper、Research Square 预印本），**未见同行评审发表**。代码 github.com/rosewang2008/tutor-copilot，OSF 预注册 osf.io/8d6ha
- 本会话所知：真实随机对照实验，给导师提供专家式决策提示，看学生掌握度。
- 其余字段：
- 对我们的作用：**"专家决策提示能提高真实学习结果"的因果证据**，是整个 T2 主张的现实依据
- 我的感悟：

---

## 第三层：只读摘要

| # | 论文 | ID | 另一会话摘要（未核） | 对我们的作用 |
|---|---|---|---|---|
| L3-1 | StudentSim（Microsoft） | 2609.01591 | arXiv only，2026-09-01；代码 github.com/microsoft/StudentSim。训模拟学生当奖励模型 | T3 参考 |
| L3-2 | Pedagogical Safety in Educational RL: reward hacking | 2604.04237 | 投 IJAIED 未录；纯仿真无 LLM；无代码。教育 RL 里的奖励作弊 | T3 奖励设计时参考，权重低 |
| L3-3 | Supervisor architecture, withhold the answer | 2608.12292 | arXiv only，单作者，无代码。规则架构，用状态控制帮助程度（"披露合同"或"帮助阶梯"，两篇对应关系未核） | related work，权重低 |
| L3-4 | Auditable Release Control for Pedagogical Leakage | 2608.00515 | arXiv only，单作者（与 ES-LLMs 同人），无代码 | related work，权重低 |
| L3-5 | Learning to Prompt: Adaptive High-School Tutoring | 2606.20138 | EMNLP 2026 Industry Track；无代码 | 门槛二可能的第二个对手 |
| L3-6 | MathTutorBench（Macina，ETH） | 2502.18940 | **EMNLP 2025 Main, oral**；基准、代码、榜单已放出 | 评测对齐，必用 |
| L3-7 | MathDial | 2305.14536 | EMNLP 2023 Findings。本会话已用：2861 段，人类老师 + LLM 模拟七年级学生，4 类 move | 代理数据 |

---

## 通用领域：问题结构相同的顶会论文

候选 16 篇加新找 6 篇，会议与荣誉已由子任务核实（2026-09-07，来源：会议官网 oral/poster 页、ACL Anthology、PMLR、dblp）。"未核"表示 dblp 只收录 CoRR、找不到会议页。

我们的问题拆成四个结构子问题，通用论文按它们归类：
(a) 按对方潜在状态选对话动作而不是直接回答；(b) 优化会话级/长程结果而非单轮质量；(c) 多轮不退化；(d) 模拟用户可信。

### G1 必读：获奖或 oral，结构直接对应

| 论文 | 会议 / 荣誉（已核） | 结构对应 | 拿来用什么 | 代码 |
|---|---|---|---|---|
| CollabLLM: From Passive Responders to Active Collaborators（Wu，2502.00640） | **ICML 2025 Outstanding Paper + oral** | (b)(d)：用模拟用户前向采样算多轮感知奖励 | T3 目标函数（交接文档已列）；verl 有 recipe | github.com/Wuyxin/collabllm |
| LLMs Get Lost in Multi-Turn Conversation（Laban，2505.06120） | **ICLR 2026 Outstanding Paper + oral** | (c)：通用领域的多轮退化现象与测量协议 | "多轮后退化"的评测协议直接借；我们的实验 C 应对齐它的口径 | github.com/microsoft/lost_in_conversation |
| SOTOPIA: Interactive Evaluation for Social Intelligence（Zhou，2310.11667） | ICLR 2024 **Spotlight** | (b)(d)：与带隐藏目标的模拟对手交互，按整段目标达成打分 | T3 轨迹级评测框架的模板 | github.com/sotopia-lab/sotopia |
| Debating with More Persuasive LLMs Leads to More Truthful Answers（Khan，2402.06782） | **ICML 2024 Best Paper** | (b)：面向弱裁判优化会话级结果 | 弱对手 + 会话级结果的实验设计范式；注意它是辩论不是辅导，结构对应最弱 | github.com/ucl-dark/llm_debate |

### G2 读方法：顶会正文，方法可直接借

| 论文 | 会议（已核） | 结构对应 | 拿来用什么 | 代码 |
|---|---|---|---|---|
| Plug-and-Play Policy Planner (PPDPP)（Deng，2311.00262） | ICLR 2024 | (a)(b)：小策略模型选对话策略标签，大模型只按策略生成，RL 用模拟用户训 | **这就是记忆里"大模型不可微调时的解耦架构"，2024 年已有。架构不能作为我们的新意** | github.com/dengyang17/PPDPP |
| ArCHer（Zhou，2402.19446） | ICML 2024 | (b)：话语级 critic + token 级策略的层级多轮 RL | T3 信用分配；与 SWEET-RL 的非对称 critic 对照 | github.com/YifeiZhou02/ArCHer |
| Learning to Clarify (ACT)（Chen，2406.00222） | ICLR 2025 | (a)：动作对比自训练 | T2 训练方法（交接文档已列） | google-research/learning_to_clarify |
| Modeling Future Conversation Turns to Teach LLMs to Ask Clarifying Questions（Zhang，2410.13788） | ICLR 2025 | (a)(b)：模拟未来轮次决定"问还是答" | PROBE vs 直接讲的决策原理 | github.com/mikejqzhang/clarifying_questions |
| Enhancing Personalized Multi-Turn Dialogue with Curiosity Reward（Wan，2504.03206） | NeurIPS 2025 | (a)(b)(d)：奖励模型推断用户潜在特质 | "推断学生状态"的内在奖励设计 | 无公开仓库 |
| Uncertainty of Thoughts（Hu，2402.03271） | NeurIPS 2024 | (a)(b)：按对隐藏状态的信息增益选问题 | 诊断性追问的选择准则 | github.com/zhiyuanhubj/UoT |
| Multi-turn RL from Preference Human Feedback（Shani，2405.14655） | NeurIPS 2024 | (b)：会话级偏好优化 | T3 算法候选 | 无 |
| REFUEL（Gao，2410.04612） | ICLR 2025 | (b)：多轮 RLHF 的高效策略优化 | T3 算法候选 | github.com/ZhaolinGao/REFUEL |
| SOTOPIA-π（Wang，2403.08715） | ACL 2024 | (b)(d)：与模拟对手交互式自我提升 | T3 训练循环模板 | github.com/sotopia-lab/sotopia-pi |
| Strength Lies in Differences (TRIP)（Zhang，2403.06769） | EMNLP 2024 | (a)(d)：策略规划器在单一模拟器上过拟合，用多样化用户模拟解决 | **模拟学生人设必须多样，否则策略过拟合模拟器**；直接指导阶段 3 | 无 |
| Consistently Simulating Human Personas with Multi-Turn RL（Abdulhai，2511.00222） | NeurIPS 2025 | (d)：模拟用户多轮人设漂移，含学生角色 | 模拟器"错误稳定、不被说服"的验证方法 | github.com/abdulhaim/consistent-LLMs |
| Towards Understanding Sycophancy（Sharma，2310.13548） | ICLR 2024 | (c)(d)：模型在用户反驳下让步 | 两用：辅导模型被学生错误主张带偏；模拟学生被辅导模型轻易说服 | github.com/meg-tong/sycophancy-eval |
| Eliciting Human Preferences with LMs (GATE)（Li，2310.11589） | ICLR 2025 | (a)：主动提问获取潜在偏好 | related work | github.com/alextamkin/generative-elicitation |
| Rethinking the Evaluation for Conversational Recommendation (iEvaLM)（Wang，2305.13112）+ How Reliable is Your Simulator?（Zhu，2403.16416） | EMNLP 2023 main + WWW 2024 Companion | (d)：LLM 模拟用户泄目标、过度顺从 | 模拟学生"泄答案/被说服"问题在推荐领域的先例与检测法 | github.com/RUCAIBox/iEvaLM-CRS |

### G3 只读摘要或会议未核

| 论文 | 状态（已核） | 备注 |
|---|---|---|
| SWEET-RL（Zhou，2503.15478） | **会议未核**，dblp 只有 CoRR；代码 github.com/facebookresearch/sweet_rl | 交接文档列为 T3 算法，引用时按预印本 |
| Dialogue Action Tokens（Li，2406.11978） | 未核，预印本；代码有 | 先在动作空间规划再生成，解耦架构的另一先例 |
| Zero-Shot Goal-Directed Dialogue via RL on Imagined Conversations（Hong，2311.05584） | 未核，预印本 | 用想象对话训目标导向策略 |
| Grounded in Reality: Learning and Deploying Proactive LLM from Offline Logs（Wei，2510.25441） | 未核，ICLR 2026 投稿 | **从离线真实日志学主动对话策略，和我们"从真实日志学"的路径同构，必须看** |
| Interactive Dialogue Agents via RL on Hindsight Regenerations（Hong，2411.05194） | 未核，预印本 | 事后重生成做多轮 RL |
| STaR-GATE（Andukuri，2403.19154） | COLM 2024 | 自训练学提澄清问题 |
| MediQ（Li，2406.00922） | NeurIPS 2024 | 医疗场景"问还是答"，不确定性驱动 |
| Tell Me More!（Qian，2402.09205） | ACL 2024 | 行动前澄清 |
| Yoon et al.（2403.09738） | NAACL 2024 | 用户模拟器保真度协议 |

### 通用文献对我们的三条含义

1. **方法层面的新意空间很小。** "状态 → 动作策略 + 大模型生成"的解耦是 PPDPP（ICLR 2024）；话语级决策 + token 级生成的层级 RL 是 ArCHer（ICML 2024）；多轮感知奖励是 CollabLLM。我们的方法论文不可能靠架构或目标函数取胜，只能靠"策略从真实专家日志学出"和"教育结果"两点。这和教育文献对照的结论一致。
2. **评测协议不要自创。** 多轮退化用 Laban 2025 的协议，轨迹级评测用 SOTOPIA 的方式，模拟器可信度用 TRIP + 人设一致性 + 谄媚性三套现成检验。自创口径会被审稿人拿这些来比。
3. **模拟学生是 T3 最大的方法论风险，通用领域已经给出了失败模式和检验法**：单一模拟器过拟合（TRIP）、人设漂移（Abdulhai）、被说服（Sharma）、泄目标（iEvaLM）。阶段 3 的"必须验证错误稳定、不会被随便说服"要按这四篇的方法做，不能只靠人工抽查。


---

## 汇总（全部读完后填）

| 论文 | 是否已做我们打算做的事 | 最接近的差别 | 对我们的作用 |
|---|---|---|---|
| | | | |

## 读完后要写的三样东西

1. 用自己的话写一段"空位在哪"，点名最接近的两三篇（L1-1 大概率在内），说清它们为什么没填上。
2. 基线清单：哪篇有 checkpoint 或代码可以直接跑在我们的探针集上，哪篇只能引数字。
3. 从文献里借的指标清单，避免评测口径自创。
