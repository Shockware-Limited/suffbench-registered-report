# Ablation report (auto-generated)

Records: 5020. Models: claude-haiku-5-5. Instances: 23. eps=0.05.


## claude-haiku-5-5

Spend at list prices: $12.87. Samples: 5020.

A1 now (k=20) minus A1 pilot (k=10), 23 instances: -0.041 [-0.074, -0.013]


### H5: predicted-minimal contexts vs A1 (paired, instance-level bootstrap)

Decision rule (preregistration §6, one-sided α=0.05): one-sided 95% lower bound > −eps. The two-sided interval, sign counts and the estimate without the most influential instance are shown alongside (added 2026-10-12 after the exploratory run; descriptive).

| contrast | n | mean diff | 95% CI (two-sided) | one-sided 95% LB | non-inferior at eps | sign +/−/0 | without most influential | median tokens | tokens A1 |
|---|---|---|---|---|---|---|---|---|---|
| A1g − A1 | 23 | +0.017 | [-0.002, +0.041] | +0.000 | yes | 5/2/16 | +0.011 [-0.005, +0.032] (drop 2bcdfbb1ac02) | 13,513 | 39,586 |
| A1t − A1 | 23 | +0.007 | [-0.020, +0.030] | -0.015 | yes | 5/3/15 | +0.000 [-0.023, +0.023] (drop 2bcdfbb1ac02) | 15,335 | 39,586 |
| W − A1 | 23 | -0.028 | [-0.096, +0.017] | -0.083 | no | 4/4/15 | +0.000 [-0.025, +0.023] (drop babd691446b9) | 13,476 | 39,586 |

Instances where the predictor keeps no dependency (arm equals W): A1g 14/23, A1t 11/23. Instances with W and A1 both at ceiling (1.0): 8; both at floor (0.0): 5; W inexpressible (gold identifiers missing from W): 10. Only instances outside ceiling and floor can separate the arms.


### Necessity of dependency interfaces (removal lowers instance pass by > eps)

Instances with A1 pass > 0 (informative): 17/23. Dependency groups on informative instances: 135.

- Necessary: 33/135 = 0.244 [0.178, 0.319] (bootstrap over groups; instance clustering ignored here).
- Removal raises pass by > eps (non-monotone cells): 33/135.
- Null reference (all cells of an instance share one rate, k=20, 2,000 simulations): necessary 30.8 [13, 49], helps 30.4 [12, 53]. Observed counts inside this range are not evidence of necessity.
- Per instance (necessary/helps/groups): 326faaac8b5c 0/14/16, b87e58a1d390 11/2/15, 8f7afbdbdbd6 9/2/11, 3f6a16a9f8c7 3/3/10, 01bcd474447b 5/0/15, ad2a33837712 0/5/7, cba9646b8c25 4/1/9, 2bcdfbb1ac02 0/3/4.
- Predictor gold-referenced: predicted 10, precision 0.20, recall 0.06 (tp=2, fp=8, fn=31).
- Predictor task-referenced: predicted 18, precision 0.33, recall 0.18 (tp=6, fp=12, fn=27).
- Slack tokens(A1)/tokens(W ∪ necessary): mean 2.71 [1.66, 4.06], median 1.56.

| instance | A1 pass | group removed | pass after | drop | pred gold | pred task |
|---|---|---|---|---|---|---|
| 8f7afbdbdbd6 | 0.95 | iostreams | 0.50 | +0.45 | 0 | 0 |
| ad2a33837712 | 0.60 | gh | 0.90 | -0.30 | 0 | 0 |
| 8f7afbdbdbd6 | 0.95 | api | 0.65 | +0.30 | 0 | 1 |
| 2bcdfbb1ac02 | 0.05 | cmdutil | 0.30 | -0.25 | 0 | 0 |
| 3f6a16a9f8c7 | 0.85 | io | 0.60 | +0.25 | 0 | 0 |
| babd691446b9 | 1.00 | gh | 0.75 | +0.25 | 1 | 1 |
| cba9646b8c25 | 0.85 | gh | 0.60 | +0.25 | 0 | 0 |
| ad2a33837712 | 0.60 | set | 0.80 | -0.20 | 0 | 0 |
| b87e58a1d390 | 0.50 | ghinstance | 0.30 | +0.20 | 0 | 0 |
| b87e58a1d390 | 0.50 | text | 0.30 | +0.20 | 0 | 0 |
| b87e58a1d390 | 0.50 | cmdutil | 0.30 | +0.20 | 0 | 0 |
| b87e58a1d390 | 0.50 | iostreams | 0.30 | +0.20 | 0 | 0 |
| 3f6a16a9f8c7 | 0.85 | verification | 0.65 | +0.20 | 0 | 1 |
| 8f7afbdbdbd6 | 0.95 | shared | 0.75 | +0.20 | 0 | 0 |
| cba9646b8c25 | 0.85 | safeurl | 0.65 | +0.20 | 0 | 0 |
| 2bcdfbb1ac02 | 0.05 | iostreams | 0.20 | -0.15 | 1 | 1 |
| 326faaac8b5c | 0.85 | context | 1.00 | -0.15 | 0 | 0 |
| 326faaac8b5c | 0.85 | git | 1.00 | -0.15 | 0 | 0 |
| 326faaac8b5c | 0.85 | prompter | 1.00 | -0.15 | 0 | 1 |
| 326faaac8b5c | 0.85 | source | 1.00 | -0.15 | 0 | 1 |
| 326faaac8b5c | 0.85 | tableprinter | 1.00 | -0.15 | 0 | 0 |
| 326faaac8b5c | 0.85 | text | 1.00 | -0.15 | 0 | 1 |
| 326faaac8b5c | 0.85 | iostreams | 1.00 | -0.15 | 0 | 0 |
| ad2a33837712 | 0.60 | ghtelemetry | 0.75 | -0.15 | 0 | 0 |
| ad2a33837712 | 0.60 | ghrepo | 0.75 | -0.15 | 0 | 0 |
| b87e58a1d390 | 0.50 | prompter | 0.35 | +0.15 | 0 | 0 |
| 8f7afbdbdbd6 | 0.95 | git | 0.80 | +0.15 | 0 | 0 |
| 8f7afbdbdbd6 | 0.95 | text | 0.80 | +0.15 | 0 | 0 |
| 8f7afbdbdbd6 | 0.95 | surveyext | 0.80 | +0.15 | 0 | 0 |
| 2bcdfbb1ac02 | 0.05 | client | 0.15 | -0.10 | 0 | 0 |
| 326faaac8b5c | 0.85 | api | 0.95 | -0.10 | 0 | 0 |
| 326faaac8b5c | 0.85 | ghrepo | 0.95 | -0.10 | 0 | 0 |
| 326faaac8b5c | 0.85 | frontmatter | 0.95 | -0.10 | 0 | 0 |
| 326faaac8b5c | 0.85 | installer | 0.95 | -0.10 | 1 | 1 |
| 3f6a16a9f8c7 | 0.85 | gh | 0.95 | -0.10 | 0 | 0 |
| 3f6a16a9f8c7 | 0.85 | ghinstance | 0.75 | +0.10 | 0 | 0 |
| 3f6a16a9f8c7 | 0.85 | artifact | 0.95 | -0.10 | 0 | 1 |
| 3f6a16a9f8c7 | 0.85 | cmdutil | 0.95 | -0.10 | 0 | 0 |
| 8f7afbdbdbd6 | 0.95 | ghinstance | 0.85 | +0.10 | 0 | 0 |
| 8f7afbdbdbd6 | 0.95 | ghrepo | 0.85 | +0.10 | 0 | 0 |
