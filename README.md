# Interfaces or Bodies? A Preregistered Test of ε-Sufficient Context for Language-Model Code Editing in Go

Jude Castiel Johansen, Shockware Limited, independent researcher. ORCID 0009-0002-5644-3073.

Stage 1 protocol of a Registered Report prepared for the MSR 2027 Registered Reports track, archived as DOI 10.5281/zenodo.23307547. No confirmatory data have been collected. The study operationalises ε-sufficient context (definitions note, DOI 10.5281/zenodo.23282195) as a paired non-inferiority test of a compiler-computed interface context against dependency bodies and the transitive slice, with a degradation curve at fixed coverage and an ablation of dependency interfaces.

| Item | Where |
|---|---|
| Stage 1 report (LaTeX, IEEEtran) | `main.tex`, `refs.bib`; build with `tectonic main.tex` |
| Preregistration text, with dated amendments | `preregistration.md` |
| Power and sample size | `analysis/power.py` |
| Pilot analysis | `analysis/pilot.py` |
| Ablation analysis (H5) | `analysis/ablation.py` |
| Harness: mining, context building, running, ablation arms | `harness/` |
| Pilot paper and release packaging | `pilot-paper/` |
| Pilot release as archived on Zenodo (DOI 10.5281/zenodo.23307204) | `pilot-release/` |

Pilot verdict records are in `harness/results/`. Instance files under `harness/instances/` carry the author's local checkout paths; `pilot-paper/make_release.py` rewrites them for release.

## Licence

Text and data: CC-BY-4.0. Code: Apache-2.0.
