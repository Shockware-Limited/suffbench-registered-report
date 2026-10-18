# Ablation report (auto-generated)

Records: 260. Models: claude-sonnet-5-5. Instances: 10. eps=0.05.


## claude-sonnet-5-5

Spend at list prices: $12.39. Samples: 260.

A1 now (k=20) minus A1 pilot (k=10), 6 instances: +0.039 [+0.000, +0.083]


### H5: predicted-minimal contexts vs A1 (paired, instance-level bootstrap)

Decision rule (preregistration §6, one-sided α=0.05): one-sided 95% lower bound > −eps. The two-sided interval, sign counts and the estimate without the most influential instance are shown alongside (added 2026-10-12 after the exploratory run; descriptive).

| contrast | n | mean diff | 95% CI (two-sided) | one-sided 95% LB | non-inferior at eps | sign +/−/0 | without most influential | median tokens | tokens A1 |
|---|---|---|---|---|---|---|---|---|---|
| A1g − A1 | 10 | -0.030 | [-0.180, +0.060] | -0.150 | no | 2/1/7 | +0.033 [+0.000, +0.078] (drop c8591a1e46e4) | 49,822 | 84,817 |
| A1t − A1 | 6 | -0.083 | [-0.300, +0.050] | -0.283 | no | 1/1/4 | +0.020 [+0.000, +0.060] (drop c8591a1e46e4) | 55,317 | 84,817 |
| W − A1 | 10 | -0.010 | [-0.120, +0.070] | -0.100 | no | 3/2/5 | +0.033 [-0.011, +0.089] (drop c8591a1e46e4) | 21,946 | 84,817 |

Instances where the predictor keeps no dependency (arm equals W): A1g 4/10, A1t 4/10. Instances with W and A1 both at ceiling (1.0): 0; both at floor (0.0): 5; W inexpressible (gold identifiers missing from W): 10. Only instances outside ceiling and floor can separate the arms.


### Necessity of dependency interfaces (removal lowers instance pass by > eps)

Instances with A1 pass > 0 (informative): 4/10. Dependency groups on informative instances: 0.

