# 状态敏感度测试结果

模型：Qwen3.8-27B；场景 12 个；状态变体 7 种（含无状态对照）。

## nothink@T0.0  (n=84, parse failures=0)

动作分布（行=状态变体，列=模型选的动作，单位 %）

| variant       |   PROBE |   HINT |   EXPLAIN |   CORRECT |   AFFIRM |   MANAGE |
|:--------------|--------:|-------:|----------:|----------:|---------:|---------:|
| ctrl          |      67 |      0 |         0 |        25 |        8 |        0 |
| unknown       |     100 |      0 |         0 |         0 |        0 |        0 |
| careless      |      33 |     17 |         0 |        50 |        0 |        0 |
| misconception |      83 |     17 |         0 |         0 |        0 |        0 |
| escalate      |       0 |      0 |        17 |        83 |        0 |        0 |
| frustrated    |       0 |      0 |         0 |         0 |        0 |      100 |
| timeout       |       0 |      0 |         0 |       100 |        0 |        0 |

按状态变体：符合启发式期望的比例 / 讲解或告知的比例 / 回复中出现最终答案的比例（%）

| variant       | expect          |   follow |   tell |   leak |
|:--------------|:----------------|---------:|-------:|-------:|
| ctrl          | -               | nan      |     25 |      8 |
| unknown       | PROBE           | 100      |      0 |      0 |
| careless      | HINT            |  16.6667 |     50 |     50 |
| misconception | EXPLAIN         |   0      |      0 |      0 |
| escalate      | EXPLAIN|EXAMPLE |  16.6667 |    100 |     83 |
| frustrated    | MANAGE          | 100      |      0 |      0 |
| timeout       | CORRECT         | 100      |    100 |    100 |

每个场景在 6 种状态下的多数动作互不相同的个数（最大 6）：均值 3.42，分布 {4: 3, 3: 8, 5: 1}

各场景多数动作：

| scenario                | unknown   | careless   | misconception   | escalate   | frustrated   | timeout   |
|:------------------------|:----------|:-----------|:----------------|:-----------|:-------------|:----------|
| S01_rational_sub        | PROBE     | CORRECT    | PROBE           | EXPLAIN    | MANAGE       | CORRECT   |
| S02_power_neg           | PROBE     | CORRECT    | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S03_expand_bracket      | PROBE     | PROBE      | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S04_solve_linear        | PROBE     | PROBE      | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S05_like_terms          | PROBE     | CORRECT    | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S06_clear_denominator   | PROBE     | PROBE      | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S07_abs_value           | PROBE     | HINT       | PROBE           | EXPLAIN    | MANAGE       | CORRECT   |
| S08_supplementary_angle | PROBE     | PROBE      | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S09_scientific_notation | PROBE     | HINT       | HINT            | CORRECT    | MANAGE       | CORRECT   |
| S10_discount_word       | PROBE     | CORRECT    | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S11_reciprocal          | PROBE     | CORRECT    | HINT            | CORRECT    | MANAGE       | CORRECT   |
| S12_monomial_degree     | PROBE     | CORRECT    | PROBE           | CORRECT    | MANAGE       | CORRECT   |

总体：状态符合率 56%，讲解/告知率 42%，泄答案率 39%；无状态对照组讲解/告知率 25%，泄答案率 8%

## nothink@T0.7  (n=420, parse failures=0)

动作分布（行=状态变体，列=模型选的动作，单位 %）

| variant       |   PROBE |   HINT |   EXPLAIN |   CORRECT |   AFFIRM |   MANAGE |
|:--------------|--------:|-------:|----------:|----------:|---------:|---------:|
| ctrl          |      55 |      5 |         0 |        30 |       10 |        0 |
| unknown       |      98 |      2 |         0 |         0 |        0 |        0 |
| careless      |      38 |     15 |         0 |        47 |        0 |        0 |
| misconception |      57 |     28 |         0 |        15 |        0 |        0 |
| escalate      |      18 |      8 |        20 |        53 |        0 |        0 |
| frustrated    |       0 |      0 |         0 |         0 |        2 |       98 |
| timeout       |       0 |      0 |         0 |       100 |        0 |        0 |

按状态变体：符合启发式期望的比例 / 讲解或告知的比例 / 回复中出现最终答案的比例（%）

| variant       | expect          |   follow |   tell |   leak |
|:--------------|:----------------|---------:|-------:|-------:|
| ctrl          | -               | nan      |     30 |     18 |
| unknown       | PROBE           |  98.3333 |      0 |      0 |
| careless      | HINT            |  15      |     47 |     37 |
| misconception | EXPLAIN         |   0      |     15 |     12 |
| escalate      | EXPLAIN|EXAMPLE |  20      |     73 |     60 |
| frustrated    | MANAGE          |  98.3333 |      0 |      2 |
| timeout       | CORRECT         | 100      |    100 |     88 |

每个场景在 6 种状态下的多数动作互不相同的个数（最大 6）：均值 3.50，分布 {4: 4, 3: 7, 5: 1}

各场景多数动作：

| scenario                | unknown   | careless   | misconception   | escalate   | frustrated   | timeout   |
|:------------------------|:----------|:-----------|:----------------|:-----------|:-------------|:----------|
| S01_rational_sub        | PROBE     | CORRECT    | PROBE           | HINT       | MANAGE       | CORRECT   |
| S02_power_neg           | PROBE     | CORRECT    | HINT            | CORRECT    | MANAGE       | CORRECT   |
| S03_expand_bracket      | PROBE     | PROBE      | PROBE           | PROBE      | MANAGE       | CORRECT   |
| S04_solve_linear        | PROBE     | PROBE      | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S05_like_terms          | PROBE     | PROBE      | CORRECT         | CORRECT    | MANAGE       | CORRECT   |
| S06_clear_denominator   | PROBE     | PROBE      | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S07_abs_value           | PROBE     | HINT       | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S08_supplementary_angle | PROBE     | PROBE      | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S09_scientific_notation | PROBE     | HINT       | HINT            | EXPLAIN    | MANAGE       | CORRECT   |
| S10_discount_word       | PROBE     | CORRECT    | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S11_reciprocal          | PROBE     | CORRECT    | HINT            | CORRECT    | MANAGE       | CORRECT   |
| S12_monomial_degree     | PROBE     | CORRECT    | PROBE           | CORRECT    | MANAGE       | CORRECT   |

总体：状态符合率 55%，讲解/告知率 39%，泄答案率 33%；无状态对照组讲解/告知率 30%，泄答案率 18%

## think@T0.6  (n=252, parse failures=8)

动作分布（行=状态变体，列=模型选的动作，单位 %）

| variant       |   PROBE |   HINT |   EXPLAIN |   PRACTICE |   CORRECT |   MANAGE |   PARSE_FAIL |
|:--------------|--------:|-------:|----------:|-----------:|----------:|---------:|-------------:|
| ctrl          |      42 |      6 |         0 |          3 |        31 |        0 |           19 |
| unknown       |     100 |      0 |         0 |          0 |         0 |        0 |            0 |
| careless      |      31 |     47 |         0 |          0 |        19 |        0 |            3 |
| misconception |      50 |     28 |         3 |          0 |        19 |        0 |            0 |
| escalate      |       0 |      0 |         0 |          0 |       100 |        0 |            0 |
| frustrated    |       3 |     42 |         3 |          0 |        11 |       42 |            0 |
| timeout       |       0 |      0 |         0 |          0 |       100 |        0 |            0 |

按状态变体：符合启发式期望的比例 / 讲解或告知的比例 / 回复中出现最终答案的比例（%）

| variant       | expect          |    follow |   tell |   leak |
|:--------------|:----------------|----------:|-------:|-------:|
| ctrl          | -               | nan       |     31 |     31 |
| unknown       | PROBE           | 100       |      0 |      0 |
| careless      | HINT            |  48.5714  |     19 |     19 |
| misconception | EXPLAIN         |   2.77778 |     22 |     17 |
| escalate      | EXPLAIN|EXAMPLE |   0       |    100 |     97 |
| frustrated    | MANAGE          |  41.6667  |     14 |     11 |
| timeout       | CORRECT         | 100       |    100 |     97 |

每个场景在 6 种状态下的多数动作互不相同的个数（最大 6）：均值 3.33，分布 {3: 8, 4: 4}

各场景多数动作：

| scenario                | unknown   | careless   | misconception   | escalate   | frustrated   | timeout   |
|:------------------------|:----------|:-----------|:----------------|:-----------|:-------------|:----------|
| S01_rational_sub        | PROBE     | PROBE      | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S02_power_neg           | PROBE     | HINT       | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S03_expand_bracket      | PROBE     | HINT       | PROBE           | CORRECT    | HINT         | CORRECT   |
| S04_solve_linear        | PROBE     | PROBE      | PROBE           | CORRECT    | HINT         | CORRECT   |
| S05_like_terms          | PROBE     | HINT       | CORRECT         | CORRECT    | CORRECT      | CORRECT   |
| S06_clear_denominator   | PROBE     | PROBE      | PROBE           | CORRECT    | MANAGE       | CORRECT   |
| S07_abs_value           | PROBE     | HINT       | HINT            | CORRECT    | MANAGE       | CORRECT   |
| S08_supplementary_angle | PROBE     | PROBE      | PROBE           | CORRECT    | HINT         | CORRECT   |
| S09_scientific_notation | PROBE     | HINT       | CORRECT         | CORRECT    | CORRECT      | CORRECT   |
| S10_discount_word       | PROBE     | PROBE      | HINT            | CORRECT    | MANAGE       | CORRECT   |
| S11_reciprocal          | PROBE     | HINT       | HINT            | CORRECT    | CORRECT      | CORRECT   |
| S12_monomial_degree     | PROBE     | HINT       | CORRECT         | CORRECT    | MANAGE       | CORRECT   |

总体：状态符合率 49%，讲解/告知率 43%，泄答案率 40%；无状态对照组讲解/告知率 31%，泄答案率 31%
