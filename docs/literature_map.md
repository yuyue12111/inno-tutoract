# 文献地图 v2

2026-09-07 重写。v1 存 `docs/archive/literature_map_2026-09-07_v1.md`。全文在 `data/papers/`（按 arXiv 号），Bridge 在 `data/raw/bridge`。

**对照基准（每篇都拿这句话去比）：**
> 从真实专家日志学一个策略：输入结构化学生状态（错因、掌握度等），输出显式教学动作；证明它比强提示的前沿模型更接近专家，且带来更高的多轮学习增益。

**四个结构子问题（通用论文按此归类）：** (a) 按对方潜在状态选动作而不是直接回答；(b) 优化会话级结果而非单轮质量；(c) 多轮不退化；(d) 模拟用户可信。

## 读法

1. 带着杀死空位的目的读。每篇最后一个字段必填，写不出"否"的理由就告诉我。
2. 读完把块首 `[ ]` 改成 `[x] 日期`。
3. 标"未核"的句子是网页搜索来的，已核出 5 处错，读的目的是证伪它。
4. `我的感悟` 写事实之外的判断：它为什么失败、哪个指标不能用、它有没有改变你对空位的看法。

## 阅读顺序

1. 2507.16252 会话级结果 RL（L1-1）
2. ScaffoldLM，ACL 2026（L1-7，新加，已发表的最近对手）
3. 2605.27088 提示词优化（L1-2）
4. 2507.06910 预测专家策略（L1-3）
5. 2607.19371 脚手架坍缩（L1-4）
6. TutorMoments（L1-5）
7. Bridge 重读（L1-6）
8. CollabLLM（G1-1）
9. LLMs Get Lost in Multi-Turn（G1-2）
10. SOTOPIA（G1-3）
11. LLM Debate（G1-4）
12. 然后 L2 与 G2 只读方法和主表；G2 里 PPDPP、ArCHer、ACT、TRIP、Abdulhai、Sycophancy 优先。L3、G3 只读摘要。

## 已核的硬事实（读之前先知道）

- 同行评审顶会正文（教育侧）只有 6 篇：Bridge、SocraticLM、2505.15607、MathTutorBench、2601.04025、ScaffoldLM。其余多为预印本，GuideEval 被 ICLR 2026 拒。
- "小策略选动作、大模型按动作生成"的解耦架构是 PPDPP（ICLR 2024）；层级多轮 RL 是 ArCHer（ICML 2024）；多轮感知奖励是 CollabLLM。架构和目标函数不是新意。
- Bridge 里 GPT-4 预测专家策略准确率 32%，等于全猜多数类；Bridge 未报标注者一致率。专家动作可预测性的天花板未知。

## 字段模板

```
### [ ] 编号 标题 — ID · 会议（核实状态）· 代码
- 事实：任务 / 数据（真实或模拟；学段；语言；规模）/ 动作标签 / 状态条件 / 方法 / 指标 / 自认局限 / 可用产物
- 未核：（网页搜索来的主张，读时证伪）
- 是否已做我们打算做的事：否 / 是 / 部分 + 理由
- 作用：门槛二对手 / 代理评测集 / 基线 / T3 参考 / 指标来源 / related work
- 我的感悟：
```

---

# 一、通用领域

## G1 必读：获奖或 oral，结构直接对应

### [ ] G1-1 CollabLLM: From Passive Responders to Active Collaborators — 2502.00640 · ICML 2025 Outstanding Paper, oral · github.com/Wuyxin/collabllm
- 对应：(b)(d) 用模拟用户前向采样算多轮感知奖励
- 借：T3 目标函数；verl 有 recipe
- 是否已做我们打算做的事：
- 我的感悟：

### [ ] G1-2 LLMs Get Lost in Multi-Turn Conversation — 2505.06120 · ICLR 2026 Outstanding Paper, oral · github.com/microsoft/lost_in_conversation
- 对应：(c) 多轮退化的现象与测量协议
- 借：实验 C 的评测口径直接对齐它
- 是否已做我们打算做的事：
- 我的感悟：

### [ ] G1-3 SOTOPIA — 2310.11667 · ICLR 2024 Spotlight · github.com/sotopia-lab/sotopia
- 对应：(b)(d) 与带隐藏目标的模拟对手交互，按整段目标达成打分
- 借：T3 轨迹级评测框架
- 是否已做我们打算做的事：
- 我的感悟：

### [ ] G1-4 Debating with More Persuasive LLMs Leads to More Truthful Answers — 2402.06782 · ICML 2024 Best Paper · github.com/ucl-dark/llm_debate
- 对应：(b) 面向弱裁判优化会话级结果；是辩论不是辅导，对应最弱
- 借：弱对手 + 会话级结果的实验设计
- 是否已做我们打算做的事：
- 我的感悟：

## G2 读方法：顶会正文，方法可直接借

### [ ] G2-1 PPDPP: Plug-and-Play Policy Planner — 2311.00262 · ICLR 2024 · github.com/dengyang17/PPDPP
- 对应：(a)(b) 小策略模型选对话策略标签，大模型按标签生成，RL 用模拟用户训
- 借：这就是解耦架构，2024 年已发表；我们不能拿架构当新意
- 我的感悟：

### [ ] G2-2 ArCHer — 2402.19446 · ICML 2024 · github.com/YifeiZhou02/ArCHer
- 对应：(b) 话语级 critic + token 级策略的层级多轮 RL
- 借：T3 信用分配，与 SWEET-RL 对照
- 我的感悟：

### [ ] G2-3 ACT: Learning to Clarify — 2406.00222 · ICLR 2025 · google-research/learning_to_clarify
- 对应：(a) 动作对比自训练
- 借：T2 训练方法（交接文档已列）
- 我的感悟：

### [ ] G2-4 Modeling Future Conversation Turns to Teach LLMs to Ask Clarifying Questions — 2410.13788 · ICLR 2025 · github.com/mikejqzhang/clarifying_questions
- 对应：(a)(b) 模拟未来轮次决定"问还是答"
- 借：PROBE 与直接讲的决策原理
- 我的感悟：

### [ ] G2-5 Enhancing Personalized Multi-Turn Dialogue with Curiosity Reward — 2504.03206 · NeurIPS 2025 · 无代码
- 对应：(a)(b)(d) 奖励模型推断用户潜在特质
- 借："推断学生状态"的内在奖励
- 我的感悟：

### [ ] G2-6 Uncertainty of Thoughts — 2402.03271 · NeurIPS 2024 · github.com/zhiyuanhubj/UoT
- 对应：(a)(b) 按对隐藏状态的信息增益选问题
- 借：诊断性追问的选择准则
- 我的感悟：

### [ ] G2-7 Multi-turn RL from Preference Human Feedback — 2405.14655 · NeurIPS 2024 · 无代码
- 对应：(b) 会话级偏好优化
- 借：T3 算法候选
- 我的感悟：

### [ ] G2-8 REFUEL — 2410.04612 · ICLR 2025 · github.com/ZhaolinGao/REFUEL
- 对应：(b) 多轮 RLHF 高效策略优化
- 借：T3 算法候选
- 我的感悟：

### [ ] G2-9 SOTOPIA-π — 2403.08715 · ACL 2024 · github.com/sotopia-lab/sotopia-pi
- 对应：(b)(d) 与模拟对手交互式自我提升
- 借：T3 训练循环模板
- 我的感悟：

### [ ] G2-10 TRIP: Strength Lies in Differences — 2403.06769 · EMNLP 2024 · 无代码
- 对应：(a)(d) 策略规划器在单一模拟器上过拟合，用多样化用户模拟解决
- 借：模拟学生人设必须多样；直接指导阶段 3
- 我的感悟：

### [ ] G2-11 Consistently Simulating Human Personas with Multi-Turn RL — 2511.00222 · NeurIPS 2025 · github.com/abdulhaim/consistent-LLMs
- 对应：(d) 模拟用户多轮人设漂移，含学生角色
- 借：模拟器"错误稳定、不被说服"的验证方法
- 我的感悟：

### [ ] G2-12 Towards Understanding Sycophancy — 2310.13548 · ICLR 2024 · github.com/meg-tong/sycophancy-eval
- 对应：(c)(d) 模型在用户反驳下让步
- 借：辅导模型被学生带偏；模拟学生被轻易说服，两用
- 我的感悟：

### [ ] G2-13 GATE: Eliciting Human Preferences with LMs — 2310.11589 · ICLR 2025 · github.com/alextamkin/generative-elicitation
- 对应：(a) 主动提问获取潜在偏好
- 借：related work
- 我的感悟：

### [ ] G2-14 iEvaLM — 2305.13112 · EMNLP 2023 main · github.com/RUCAIBox/iEvaLM-CRS；配 How Reliable is Your Simulator — 2403.16416 · WWW 2024 Companion
- 对应：(d) LLM 模拟用户泄目标、过度顺从
- 借：模拟学生泄答案 / 被说服的检测法
- 我的感悟：

## G3 只读摘要

### [ ] G3-1 CoSToM: Causal-oriented Steering for Intrinsic Theory-of-Mind Alignment — ACL 2026 Best Paper（新加）
- 对应：(a) 推断他人心理状态；对辅导对应弱，看它怎么定义"推断状态"的评测
- 我的感悟：

### [ ] G3-2 DialToM: Forecasting State-Driven Dialogue Trajectories — 2604.20443 · 会议未核（新加）
- 对应：(a) 从心理状态画像预测对话走向；发现 LLM 会抽状态但不会用状态做预测，与实验 A 现象同构
- 我的感悟：

### [ ] G3-3 AgentGym-RL — ICLR 2026 oral（新加）
- 对应：(b) 多轮 RL 训练框架，基础设施而非方法
- 我的感悟：

### [ ] G3-4 SWEET-RL — 2503.15478 · 会议未核 · github.com/facebookresearch/sweet_rl
- 交接文档列为 T3 算法；引用按预印本
- 我的感悟：

### [ ] G3-5 Dialogue Action Tokens — 2406.11978 · 未核 · 有代码
- 先在动作空间规划再生成，解耦架构另一先例
- 我的感悟：

### [ ] G3-6 Grounded in Reality: Learning and Deploying Proactive LLM from Offline Logs — 2510.25441 · 未核，ICLR 2026 投稿
- 从离线真实日志学主动对话策略，和我们"从真实日志学"同构，必看
- 我的感悟：

### [ ] G3-7 Zero-Shot Goal-Directed Dialogue via RL on Imagined Conversations — 2311.05584 · 未核
- 我的感悟：

### [ ] G3-8 Interactive Dialogue Agents via RL on Hindsight Regenerations — 2411.05194 · 未核
- 我的感悟：

### [ ] G3-9 STaR-GATE — 2403.19154 · COLM 2024
- 我的感悟：

### [ ] G3-10 MediQ — 2406.00922 · NeurIPS 2024
- 医疗场景"问还是答"，不确定性驱动
- 我的感悟：

### [ ] G3-11 Tell Me More! — 2402.09205 · ACL 2024
- 我的感悟：

### [ ] G3-12 Yoon et al. 用户模拟器保真度协议 — 2403.09738 · NAACL 2024
- 我的感悟：

---

# 二、教育垂直领域

## L1 逐段读：决定门槛与定位

### [ ] L1-1 Efficient RL for optimizing conversation-level outcomes with an LLM-based tutor — 2507.16252 · arXiv only（同作者另一版进 NeurIPS 2025 MTI workshop）· 无代码
- 事实：4 个高层动作 instruct / encourage / refocus / ask a question；25 维潜在状态由 LLM 从历史抽取；在潜在状态上训策略选动作，奖励 ±1（20 轮内是否解出）
- 待填：任务 / 数据 / 指标 / 局限
- 是否已做我们打算做的事：结构最接近。差别候选：动作粗；状态是向量不是错因 / 掌握度；奖励来自模拟结果不是专家决策；非真实日志。够不够撑一篇论文，由你判断
- 作用：直接对手；T2/T3 架构模板
- 我的感悟：

### [ ] L1-2 LLMs Are Already Good Tutors: Training-Free Prompt Optimization — 2605.27088 · arXiv only · 代码仅匿名链接
- 待填：全部
- 未核：提示词优化在后测、泄答案、有帮助性上超过 RL 基线；代价是意图层脚手架低约 10 点
- 是否已做我们打算做的事：
- 作用：门槛二对手；它的方法就是我们必须补的强基线
- 我的感悟：

### [ ] L1-3 Exploring LLMs for Predicting Tutor Strategy and Student Outcomes — 2507.06910 · BEA 2025 workshop · 无代码
- 待填：全部
- 未核：GPT-4o 和 Llama 3 预测不好专家下一步策略
- 是否已做我们打算做的事：重点看它失败是模型问题还是目标多解；报没报标注者一致率
- 作用：T2 最近的"动作预测"工作
- 我的感悟：

### [ ] L1-4 Mitigating Scaffolding Collapse via Representation Alignment — 2607.19371 · arXiv only, under review · 无代码
- 事实：方法主体是表示对齐损失，DPO 只是一部分
- 未核：Qwen3-8B 上 68% 对话坍缩，方法降到 32%
- 是否已做我们打算做的事：我们的发现 3 是它已定义的现象，我们多了什么？
- 作用：related work 必引；T3 泄答案指标可对齐
- 我的感悟：

### [ ] L1-5 TutorMoments / When Help is Unhelpful — Ai2 working paper，无 arXiv 号 · 数据 huggingface.co/datasets/allenai/tutormoments-preview（462 段、520 决策点）· 代码 github.com/allenai/tutormoments
- 未核：模型默认过度帮助，把权衡写进提示词能改善但追不上人
- 是否已做我们打算做的事：
- 作用：第二代理评测集；"真实日志 ≠ 基准"的证据
- 我的感悟：

### [ ] L1-6 Bridge — 2310.10648 · NAACL 2024 · 数据与代码已在 data/raw/bridge
- 事实：错因 → 策略 → 意图三层；700 段真实、美国小学到初一、英文；10 个策略按形式分，ask_question 占 30%；GPT-4 预测策略 32% = 多数类；微调 Flan-T5 / GODEL "差到没法报数"；**未报标注者一致率**
- 是否已做我们打算做的事：
- 作用：T2 模板；代理评测集；可预测性基准
- 我的感悟：

### [ ] L1-7 ScaffoldLM: Planning-Guided Tutoring with Assessment-Driven Memory — ACL 2026 main（北师大）· github.com/BNU-ERC-ITEA/ScaffoldLM（新加）
- 事实：学生状态 7 类（correct / incorrect / question / comprehension / confusion / irrelevant / end），每类映射到一个固定操作（推进 / 引导自纠 / 提示或简化 / 回答并拉回 / 重聚焦 / 收尾），见其 Table 1；Qwen2.5-7B-Instruct 在合成数据上 SFT（5,844 段、8.5 轮/段）；评测 ScaffoldEval，GPT-4o-mini 打分 6 个教学维度；基线含 SocraticLM、TutorRL-7B、**InnoSpark-turbo**、EduChat；自认局限：合成数据
- 是否已做我们打算做的事：部分。有显式"状态 → 动作"，但状态是回答类型不是错因 / 掌握度，映射是手写规则不是从专家日志学的，数据全合成。这三条差别正是我们的位置，要写清
- 作用：已发表的最近对手；基线（有代码）；它拿我们实验室的模型当基线，要知道它怎么评的
- 我的感悟：

## L2 读方法与主表：T3 地形、评测有效性

### [ ] L2-1 PEARL — 2605.29582 · arXiv only（v2 2026-09-01）· 无 checkpoint
- 未核：Qwen3-30B；模拟器带知识图掌握状态 + 五维认知画像；八维奖励；策略只看对话不出动作标签；自认局限是无长期学习动态
- 作用：T3 模拟器与奖励候选；不复现
- 我的感悟：

### [ ] L2-2 From Problem-Solving to Teaching Problem-Solving (TutorRL) — 2505.15607 · EMNLP 2025 main, oral · github.com/eth-lre/PedagogicalRL
- 事实：7B 在线 RL + 模拟学生，可控奖励权重，接近 LearnLM
- 作用：T3 参考；"小模型追平大模型"先例
- 我的感悟：

### [ ] L2-3 Towards Pedagogically Aligned LLM Tutors for Math Mistake Remediation — 2606.21502 · arXiv only · github.com/Kpetyxova/towards-aligned-math-tutor
- 未核：Qwen3-4B/8B，SFT + DPO；五维教学分类做数据目标，不预测动作
- 作用：有 checkpoint 则作基线
- 我的感悟：

### [ ] L2-4 GuideEval: Discerning minds or generic tutors — 2508.06583 · arXiv only，ICLR 2026 被拒 · 无代码
- 事实：固定历史、变学生状态的评测设计；微调了 Qwen3-8B
- 作用：实验 A 协议来源
- 我的感悟：

### [ ] L2-5 Rethinking Scaffolding: Benchmarks vs Real-World Deployments — 2606.15766 · ICML 2026 Pluralistic Alignment workshop · 无代码
- 事实：9,490 段来自 9 个数据集，混合基准与真实部署（不是"九千段真实对话"）
- 作用：内部日志价值的论据
- 我的感悟：

### [ ] L2-6 Simulated Students in Tutoring Dialogues: Substance or Illusion? — 2601.04025 · ACL 2026 main · github.com/umass-ml4ed/sim-student-eval
- 作用：T3 模拟器必须回应的质疑
- 我的感悟：

### [ ] L2-7 ES-LLMs: Interpretable Pedagogical Orchestration — 2603.23990 · AIED 2026 · 无代码，单作者
- 事实：决策与生成解耦；"掌握度增益悖论"
- 作用：解耦先例；评测必防的悖论
- 我的感悟：

### [ ] L2-8 EduClaw-Bench — 2608.03206 · arXiv only · 代码仅匿名链接
- 事实：KT 驱动 30 天模拟学生，长程评测
- 作用：T3 模拟器升级路线
- 我的感悟：

### [ ] L2-9 Tutor CoPilot — 2410.03017 · working paper，未见同行评审 · github.com/rosewang2008/tutor-copilot · 预注册 osf.io/8d6ha
- 事实：真实 RCT，给导师专家式决策提示，看学生掌握度
- 作用："专家决策提示提高真实学习结果"的因果证据，T2 主张的现实依据
- 我的感悟：

### [ ] L2-10 Training LLM-based Tutors to Improve Student Learning Outcomes in Dialogues — 2503.06424 · AIED 2025（Scarlatos & Lan）· 代码待核（新加）
- 事实：候选回复用 LLM 学生模型预测答对概率 + GPT-4o 教学量表打分，DPO 训 Llama 3.1 8B
- 作用：T3 "按学生结果训"的直接先例；比 PEARL 早且过了评审
- 我的感悟：

### [ ] L2-11 SocraticLM — NeurIPS 2024 Spotlight · github.com/Ljyustc/SocraticLM · checkpoint huggingface.co/CogBase-USTC/SocraticLM（新加）
- 事实：Dean–Teacher–Student 三智能体合成 SocraTeach 35K 段；SFT；交接文档列为开源教育模型基线
- 作用：基线，有 checkpoint 可直接跑
- 我的感悟：

### [ ] L2-12 LearnerCoMPASS — ACL 2026 main · 代码待核（新加）
- 事实：编码器-解码器做动态认知诊断得多维状态向量，动态知识图 + Graph-RAG 做路径规划；是 ITS 路径规划不是对话动作
- 作用：学生状态表示的一种做法，看它的状态向量怎么定义和验证
- 我的感悟：

## L3 只读摘要

### [ ] L3-1 StudentSim — 2609.01591 · arXiv only · github.com/microsoft/StudentSim
- 训模拟学生当奖励模型
- 我的感悟：

### [ ] L3-2 Pedagogical Safety in Educational RL: Reward Hacking — 2604.04237 · 未录用 · 无代码
- 我的感悟：

### [ ] L3-3 Supervisor Architecture: Withhold the Answer — 2608.12292 · arXiv only，单作者
- 规则架构，用学生状态控制帮助阶梯
- 我的感悟：

### [ ] L3-4 Auditable Release Control for Pedagogical Leakage — 2608.00515 · arXiv only，单作者
- 我的感悟：

### [ ] L3-5 Learning to Prompt: Adaptive High-School Tutoring — 2606.20138 · EMNLP 2026 Industry · 无代码
- 上下文赌博机做提示路由，真实高中生 A/B；门槛二可能的第二对手
- 我的感悟：

### [ ] L3-6 MathTutorBench — 2502.18940 · EMNLP 2025 main, oral · github.com/eth-lre/mathtutorbench
- 评测对齐必用
- 我的感悟：

### [ ] L3-7 MathDial — 2305.14536 · EMNLP 2023 Findings · 已在 data/raw/mathdial
- 2,861 段，人类老师 + LLM 模拟七年级学生，4 类 move
- 我的感悟：

### [ ] L3-8 Unifying AI Tutor Evaluation / MRBench — 2412.09416 · NAACL 2025，SAC Award（新加）
- 8 个教学维度，192 段对话 1,596 条回复带金标注；指标来源
- 我的感悟：

### [ ] L3-9 TutorBench — 2510.02663 · arXiv only（新加）
- 1,490 条专家编写样本，高中与 AP；前沿模型最高 56%
- 我的感悟：

### [ ] L3-10 Stepwise Verification and Remediation of Student Reasoning Errors — 2407.09136 · 会议未核（ETH）· github.com/eth-lre/verify-then-generate（新加）
- 先验证学生哪一步错再生成补救；1K 段带教师标注首错步
- 我的感悟：

### [ ] L3-11 Hey Chat, Can You Teach Me? — 2606.11744 · arXiv only（新加）
- 课程排序、苏格拉底对话、知识状态推断三者解耦，PPO 定教学进度
- 我的感悟：

---

## 读完交三样东西

1. 一段"空位在哪"：点名最接近的两三篇（L1-1、L1-7 大概率在内），说清它们为什么没填上。
2. 基线清单：有 checkpoint 或代码可直接跑的（SocraticLM、ScaffoldLM、TutorRL、2606.21502 待核），只能引数字的。
3. 借用的指标清单：多轮退化按 G1-2，轨迹级按 G1-3，模拟器可信度按 G2-10 / G2-11 / G2-12，教学维度按 L3-8 / L3-6。
