# Pilot report (auto-generated; private until Stage 1 submission)

Records: 2360. Models: claude-haiku-5-5, claude-opus-5, claude-sonnet-5-5. Instances: 24.


## claude-haiku-5-5

Instances: 24. A0 (task-only) solved on 4 instance(s): ['cli__cli-1cd39adbf03b', 'cli__cli-62e3e719a483', 'cli__cli-8f7afbdbdbd6', 'cli__cli-babd691446b9'] — excluded from the curve below (reported both ways).

Spend (list prices in PRICES, verify): $4.71; tokens in=1,444,491 cache_read=145,103,084 cache_write=15,272,539 out=2,407,794


### Degradation curve (excluding A0-solved; n_inst=20)

| load arm | median prompt tokens | p̂ Δ-pass [boot 95%] | p̂ Δ∧frame | paired drop vs A1 [95%] | cells |
|---|---|---|---|---|---|
| A1 | 40,840 | 0.575 [0.370, 0.780] | 0.525 | +0.000 [+0.000, +0.000] | 20 |
| P32 | 32,034 | 0.600 [0.320, 0.860] | 0.600 | +0.030 [-0.030, +0.120] | 10 |
| P64 | 64,069 | 0.493 [0.257, 0.743] | 0.493 | +0.029 [-0.014, +0.093] | 14 |
| P128 | 128,481 | 0.616 [0.426, 0.795] | 0.568 | -0.011 [-0.126, +0.105] | 19 |
| P200 | 198,593 | 0.606 [0.417, 0.778] | 0.561 | +0.033 [-0.094, +0.150] | 18 |

### Degradation curve (including A0-solved; n_inst=24)

| load arm | median prompt tokens | p̂ Δ-pass [boot 95%] | p̂ Δ∧frame | paired drop vs A1 [95%] | cells |
|---|---|---|---|---|---|
| A1 | 40,840 | 0.646 [0.467, 0.817] | 0.604 | +0.000 [+0.000, +0.000] | 24 |
| P32 | 32,019 | 0.636 [0.382, 0.873] | 0.636 | +0.027 [-0.027, +0.109] | 11 |
| P64 | 64,102 | 0.606 [0.383, 0.811] | 0.606 | +0.022 [-0.011, +0.072] | 18 |
| P128 | 128,411 | 0.652 [0.487, 0.809] | 0.613 | +0.022 [-0.091, +0.126] | 23 |
| P200 | 198,593 | 0.677 [0.505, 0.827] | 0.641 | +0.027 [-0.082, +0.123] | 22 |

Minimal sufficient load at ε=0.05: A1=22, P128=2 (k-granularity limits resolution)

Minimal sufficient load at ε=0.1: A1=22, P128=2 (k-granularity limits resolution)


Flip rate (cells with ≥3 samples, non-unanimous Δ-pass): 48/194 = 0.247; mean minority share 0.283


### Base-load arms (descriptive)

| arm | median tokens | p̂ Δ-pass [boot 95%] | pooled Wilson | p̂ Δ∧frame | n_inst |
|---|---|---|---|---|---|
| A0 | 554 | 0.096 [0.012, 0.204] | [0.065, 0.140] | 0.096 | 24 |
| W | 13,476 | 0.579 [0.404, 0.754] | [0.516, 0.640] | 0.525 | 24 |
| A1 | 40,840 | 0.646 [0.467, 0.817] | [0.583, 0.704] | 0.604 | 24 |
| A1b | 119,753 | 0.604 [0.433, 0.775] | [0.541, 0.664] | 0.550 | 24 |
| A1F | 51,783 | 0.600 [0.425, 0.771] | [0.537, 0.660] | 0.567 | 24 |

Paired A1−A1b: +0.042 [+0.012, +0.075] over 24 instances; majority-outcome disagreement π_d = 0/24

Paired A1−A1F: +0.046 [+0.012, +0.083] over 24 instances; majority-outcome disagreement π_d = 1/24

Paired A1−W: +0.067 [+0.021, +0.133] over 24 instances; majority-outcome disagreement π_d = 1/24


Ceiling rate (W alone passes every sample): 9/24


### Outcome taxonomy per arm

| arm | pass | delta_fail | frame_fail | build_error | apply_error | no_blocks | api_error | exceeds_window |
|---|---|---|---|---|---|---|---|---|
| A0 | 23 | 13 | 0 | 1 | 40 | 163 | 0 | 0 |
| W | 126 | 77 | 13 | 11 | 5 | 8 | 0 | 0 |
| A1 | 145 | 77 | 10 | 2 | 3 | 3 | 0 | 0 |
| A1b | 132 | 80 | 13 | 4 | 8 | 3 | 0 | 0 |
| A1F | 136 | 87 | 8 | 3 | 6 | 0 | 0 | 0 |
| P32 | 70 | 38 | 0 | 1 | 1 | 0 | 0 | 0 |
| P64 | 109 | 66 | 0 | 1 | 2 | 2 | 0 | 0 |
| P128 | 141 | 58 | 9 | 8 | 5 | 9 | 0 | 0 |
| P200 | 141 | 48 | 8 | 1 | 12 | 10 | 0 | 0 |

## claude-opus-5

Instances: 10. A0 (task-only) solved on 0 instance(s): [] — excluded from the curve below (reported both ways).

Spend (list prices in PRICES, verify): $27.00; tokens in=57,612 cache_read=4,340,563 cache_write=2,071,269 out=463,698


### Degradation curve (excluding A0-solved; n_inst=10)

| load arm | median prompt tokens | p̂ Δ-pass [boot 95%] | p̂ Δ∧frame | paired drop vs A1 [95%] | cells |
|---|---|---|---|---|---|
| A1 | 25,879 | 0.467 [0.167, 0.767] | 0.467 | +0.000 [+0.000, +0.000] | 10 |
| P32 | – | – | – | – | 0 |
| P64 | – | – | – | – | 0 |
| P128 | – | – | – | – | 0 |
| P200 | 198,051 | 0.481 [0.148, 0.815] | 0.481 | -0.074 [-0.185, +0.000] | 9 |

### Degradation curve (including A0-solved; n_inst=10)

| load arm | median prompt tokens | p̂ Δ-pass [boot 95%] | p̂ Δ∧frame | paired drop vs A1 [95%] | cells |
|---|---|---|---|---|---|
| A1 | 25,879 | 0.467 [0.167, 0.767] | 0.467 | +0.000 [+0.000, +0.000] | 10 |
| P32 | – | – | – | – | 0 |
| P64 | – | – | – | – | 0 |
| P128 | – | – | – | – | 0 |
| P200 | 198,051 | 0.481 [0.148, 0.815] | 0.481 | -0.074 [-0.185, +0.000] | 9 |

Minimal sufficient load at ε=0.05: A1=7, P200=2 (k-granularity limits resolution)

Minimal sufficient load at ε=0.1: A1=7, P200=2 (k-granularity limits resolution)


Flip rate (cells with ≥3 samples, non-unanimous Δ-pass): 2/29 = 0.069; mean minority share 0.333


### Base-load arms (descriptive)

| arm | median tokens | p̂ Δ-pass [boot 95%] | pooled Wilson | p̂ Δ∧frame | n_inst |
|---|---|---|---|---|---|
| A0 | 547 | 0.000 [0.000, 0.000] | [-0.000, 0.114] | 0.000 | 10 |
| A1 | 25,879 | 0.467 [0.167, 0.767] | [0.302, 0.639] | 0.467 | 10 |

Paired A1−A1b: +nan [+nan, +nan] over 0 instances; majority-outcome disagreement π_d = 0/0

Paired A1−A1F: +nan [+nan, +nan] over 0 instances; majority-outcome disagreement π_d = 0/0

Paired A1−W: +nan [+nan, +nan] over 0 instances; majority-outcome disagreement π_d = 0/0


Ceiling rate (W alone passes every sample): 0/10


### Outcome taxonomy per arm

| arm | pass | delta_fail | frame_fail | build_error | apply_error | no_blocks | api_error | exceeds_window |
|---|---|---|---|---|---|---|---|---|
| A0 | 0 | 7 | 0 | 0 | 15 | 8 | 0 | 0 |
| A1 | 14 | 16 | 0 | 0 | 0 | 0 | 0 | 0 |
| P200 | 13 | 13 | 0 | 1 | 0 | 0 | 0 | 0 |

## claude-sonnet-5-5

Instances: 24. A0 (task-only) solved on 14 instance(s): ['cli__cli-0274077b56a5', 'cli__cli-1863cb7c0f1d', 'cli__cli-1cd39adbf03b', 'cli__cli-326faaac8b5c', 'cli__cli-3f6a16a9f8c7', 'cli__cli-62e3e719a483', 'cli__cli-8f7afbdbdbd6', 'cli__cli-a8460b5af8cd', 'cli__cli-ad2a33837712', 'cli__cli-b87e58a1d390', 'cli__cli-babd691446b9', 'cli__cli-bd81afda9ab6', 'cli__cli-cba9646b8c25', 'cli__cli-ff28e72b59be'] — excluded from the curve below (reported both ways).

Spend (list prices in PRICES, verify): $29.16; tokens in=233,524 cache_read=18,947,020 cache_write=9,473,510 out=311,343


### Degradation curve (excluding A0-solved; n_inst=10)

| load arm | median prompt tokens | p̂ Δ-pass [boot 95%] | p̂ Δ∧frame | paired drop vs A1 [95%] | cells |
|---|---|---|---|---|---|
| A1 | 25,881 | 0.300 [0.000, 0.600] | 0.300 | +0.000 [+0.000, +0.000] | 10 |
| P32 | – | – | – | – | 0 |
| P64 | 63,932 | 0.333 [0.111, 0.667] | 0.333 | -0.111 [-0.333, +0.000] | 9 |
| P128 | 128,324 | 0.407 [0.111, 0.741] | 0.407 | -0.074 [-0.222, +0.000] | 9 |
| P200 | 198,053 | 0.370 [0.111, 0.704] | 0.370 | -0.037 [-0.333, +0.222] | 9 |

### Degradation curve (including A0-solved; n_inst=24)

| load arm | median prompt tokens | p̂ Δ-pass [boot 95%] | p̂ Δ∧frame | paired drop vs A1 [95%] | cells |
|---|---|---|---|---|---|
| A1 | 40,840 | 0.639 [0.458, 0.819] | 0.597 | +0.000 [+0.000, +0.000] | 24 |
| P32 | – | – | – | – | 0 |
| P64 | 64,102 | 0.611 [0.389, 0.833] | 0.611 | -0.056 [-0.167, +0.000] | 18 |
| P128 | 128,411 | 0.696 [0.507, 0.870] | 0.652 | -0.029 [-0.101, +0.029] | 23 |
| P200 | 198,593 | 0.682 [0.485, 0.864] | 0.636 | -0.015 [-0.136, +0.091] | 22 |

Minimal sufficient load at ε=0.05: A1=22, P64=1, P128=1 (k-granularity limits resolution)

Minimal sufficient load at ε=0.1: A1=22, P64=1, P128=1 (k-granularity limits resolution)


Flip rate (cells with ≥3 samples, non-unanimous Δ-pass): 12/111 = 0.108; mean minority share 0.333


### Base-load arms (descriptive)

| arm | median tokens | p̂ Δ-pass [boot 95%] | pooled Wilson | p̂ Δ∧frame | n_inst |
|---|---|---|---|---|---|
| A0 | 554 | 0.444 [0.278, 0.625] | [0.335, 0.559] | 0.417 | 24 |
| A1 | 40,840 | 0.639 [0.458, 0.819] | [0.524, 0.740] | 0.597 | 24 |

Paired A1−A1b: +nan [+nan, +nan] over 0 instances; majority-outcome disagreement π_d = 0/0

Paired A1−A1F: +nan [+nan, +nan] over 0 instances; majority-outcome disagreement π_d = 0/0

Paired A1−W: +nan [+nan, +nan] over 0 instances; majority-outcome disagreement π_d = 0/0


Ceiling rate (W alone passes every sample): 0/24


### Outcome taxonomy per arm

| arm | pass | delta_fail | frame_fail | build_error | apply_error | no_blocks | api_error | exceeds_window |
|---|---|---|---|---|---|---|---|---|
| A0 | 30 | 16 | 2 | 1 | 10 | 13 | 0 | 0 |
| A1 | 43 | 25 | 3 | 1 | 0 | 0 | 0 | 0 |
| P64 | 33 | 21 | 0 | 0 | 0 | 0 | 0 | 0 |
| P128 | 45 | 21 | 3 | 0 | 0 | 0 | 0 | 0 |
| P200 | 42 | 18 | 3 | 3 | 0 | 0 | 0 | 0 |
