# Ablation report (auto-generated)

Records: 4587. Models: claude-haiku-5-5. Instances: 10. eps=0.05.


## claude-haiku-5-5

Spend at list prices: $37.96. Samples: 4587.

A1 now (k=20) minus A1 pilot (k=10), 6 instances: -0.003 [-0.015, +0.005]


### H5: predicted-minimal contexts vs A1 (paired, instance-level bootstrap)

Decision rule (preregistration §6, one-sided α=0.05): one-sided 95% lower bound > −eps. The two-sided interval, sign counts and the estimate without the most influential instance are shown alongside (added 2026-10-12 after the exploratory run; descriptive).

| contrast | n | mean diff | 95% CI (two-sided) | one-sided 95% LB | non-inferior at eps | sign +/−/0 | without most influential | median tokens | tokens A1 |
|---|---|---|---|---|---|---|---|---|---|
| A1g − A1 | 10 | +0.004 | [-0.042, +0.061] | -0.035 | yes | 2/4/4 | -0.020 [-0.050, +0.003] (drop 6727b2f3a92b) | 49,822 | 84,817 |
| A1t − A1 | 6 | +0.003 | [-0.067, +0.098] | -0.063 | no | 1/3/2 | -0.040 [-0.090, -0.002] (drop 6727b2f3a92b) | 55,317 | 84,817 |
| W − A1 | 10 | +0.000 | [-0.076, +0.071] | -0.060 | no | 3/3/4 | +0.030 [-0.014, +0.087] (drop 2bcdfbb1ac02) | 21,946 | 84,817 |

Instances where the predictor keeps no dependency (arm equals W): A1g 4/10, A1t 4/10. Instances with W and A1 both at ceiling (1.0): 0; both at floor (0.0): 3; W inexpressible (gold identifiers missing from W): 10. Only instances outside ceiling and floor can separate the arms.


### Necessity of dependency interfaces (removal lowers instance pass by > eps)

Instances with A1 pass > 0 (informative): 6/10. Dependency groups on informative instances: 21.

- Necessary: 0/21 = 0.000 [0.000, 0.000] (bootstrap over groups; instance clustering ignored here).
- Removal raises pass by > eps (non-monotone cells): 0/21.
- Null reference (all cells of an instance share one rate, k=20, 2,000 simulations): necessary 0.4 [0, 4], helps 0.4 [0, 2]. Observed counts inside this range are not evidence of necessity.
- Per instance (necessary/helps/groups): 4f45ded75556 0/0/5, 20147bf81fed 0/0/16.
- Predictor gold-referenced: predicted 4, precision 0.00, recall nan (tp=0, fp=4, fn=0).
- Predictor task-referenced: predicted 2, precision 0.00, recall nan (tp=0, fp=2, fn=0).
- Slack tokens(A1)/tokens(W ∪ necessary): mean 1.24 [1.00, 1.68], median 1.00.

| instance | A1 pass | group removed | pass after | drop | pred gold | pred task |
|---|---|---|---|---|---|---|
| 4f45ded75556 | 0.03 | v2 | 0.01 | +0.02 | 1 | 0 |
| 20147bf81fed | 0.01 | ghtelemetry, prompter, run | 0.00 | +0.01 | 1 | 0 |
| 20147bf81fed | 0.01 | actions, agent-task, alias | 0.00 | +0.01 | 0 | 0 |
| 20147bf81fed | 0.01 | shared, api, attestation | 0.02 | -0.01 | 0 | 0 |
| 20147bf81fed | 0.01 | auth, browse, cache | 0.00 | +0.01 | 0 | 0 |
| 20147bf81fed | 0.01 | codespace, completion, config | 0.00 | +0.01 | 0 | 0 |
| 20147bf81fed | 0.01 | gist, gpg-key, issue, label | 0.00 | +0.01 | 0 | 0 |
| 20147bf81fed | 0.01 | run, search, secret | 0.02 | -0.01 | 0 | 0 |
| 20147bf81fed | 0.01 | send-telemetry, skills, ssh-key | 0.00 | +0.01 | 0 | 0 |
| 20147bf81fed | 0.01 | status, variable, version | 0.00 | +0.01 | 0 | 1 |
| 20147bf81fed | 0.01 | workflow, cmdutil, extensions | 0.00 | +0.01 | 1 | 0 |
| 4f45ded75556 | 0.03 | caddyconfig | 0.02 | +0.01 | 0 | 0 |
| 4f45ded75556 | 0.03 | caddyfile | 0.02 | +0.01 | 0 | 0 |
| 20147bf81fed | 0.01 | findsh, iostreams, markdown, utils | 0.02 | -0.01 | 1 | 0 |
| 4f45ded75556 | 0.03 | internal | 0.03 | +0.00 | 0 | 0 |
| 4f45ded75556 | 0.03 | cmd | 0.03 | +0.00 | 0 | 0 |
| 20147bf81fed | 0.01 | text, update, accessibility | 0.01 | +0.00 | 0 | 0 |
| 20147bf81fed | 0.01 | copilot, extension, factory | 0.01 | +0.00 | 0 | 1 |
| 20147bf81fed | 0.01 | licenses, org, pr | 0.01 | +0.00 | 0 | 0 |
| 20147bf81fed | 0.01 | preview, project, release | 0.01 | +0.00 | 0 | 0 |
| 20147bf81fed | 0.01 | repo, credits, ruleset | 0.01 | +0.00 | 0 | 0 |
