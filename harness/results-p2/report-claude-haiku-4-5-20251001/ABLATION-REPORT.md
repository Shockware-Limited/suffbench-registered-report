# Ablation report (auto-generated)

Records: 520. Models: claude-haiku-4-5-20251001. Instances: 10. eps=0.05.


## claude-haiku-4-5-20251001

Spend at list prices: $7.32. Samples: 520.


### H5: predicted-minimal contexts vs A1 (paired, instance-level bootstrap)

Decision rule (preregistration §6, one-sided α=0.05): one-sided 95% lower bound > −eps. The two-sided interval, sign counts and the estimate without the most influential instance are shown alongside (added 2026-10-12 after the exploratory run; descriptive).

| contrast | n | mean diff | 95% CI (two-sided) | one-sided 95% LB | non-inferior at eps | sign +/−/0 | without most influential | median tokens | tokens A1 |
|---|---|---|---|---|---|---|---|---|---|
| A1g − A1 | 8 | -0.006 | [-0.019, +0.000] | -0.019 | yes | 0/1/7 | +0.000 [+0.000, +0.000] (drop ff28e72b59be) | 49,822 | 84,817 |
| A1t − A1 | 4 | -0.025 | [-0.075, +0.000] | -0.050 | yes | 0/1/3 | +0.000 [+0.000, +0.000] (drop c8591a1e46e4) | 55,317 | 84,817 |
| W − A1 | 8 | +0.025 | [-0.019, +0.094] | -0.013 | yes | 1/1/6 | -0.007 [-0.021, +0.000] (drop c8591a1e46e4) | 21,946 | 84,817 |

Instances where the predictor keeps no dependency (arm equals W): A1g 4/10, A1t 4/10. Instances with W and A1 both at ceiling (1.0): 0; both at floor (0.0): 6; W inexpressible (gold identifiers missing from W): 10. Only instances outside ceiling and floor can separate the arms.


### Necessity of dependency interfaces (removal lowers instance pass by > eps)

Instances with A1 pass > 0 (informative): 2/10. Dependency groups on informative instances: 0.

