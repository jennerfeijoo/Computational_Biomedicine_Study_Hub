# BMB830 source-grounded audit

## Boundary

The active public SDU description defines the curricular scope. It requires R scripting, basic probability, statistical modelling, visualisation, interpretation, introductory multivariate analysis, biological-data analysis, critical discussion of published methods, tutorial/exercise completion, and an individual oral examination.

The public description does not expose the complete Itslearning reading list, exercise specification, grading criteria, or examination prompts. Those elements remain outside the repository evidence model and are not reconstructed.

## Reference families

The audit uses:

- the active SDU BMB830 description;
- *Introduction to Modern Statistics*, second edition, for data, exploratory analysis, probability, inference, regression, and model interpretation;
- *An Introduction to Statistical Learning with Applications in R*, second edition, for statistical learning, resampling, model assessment, and validation;
- the uploaded Yachay Tech probability/statistics notes;
- the uploaded Yachay Tech biostatistics and linear-model notes.

Visible teaching material remains original trilingual paraphrase and adaptation. Textbook prose, figures, tables, and proprietary exercises are not reproduced.

## Current focused review

Reviewed and marked `consistent`:

- M01 — R foundations and reproducible workflow;
- M02 — data quality, descriptive summaries, and visualisation;
- M03 — probability, sampling, and distributions;
- M04 — estimation and confidence intervals.

Pending focused review:

- M05 — hypothesis testing;
- M06 — group comparison;
- M07 — correlation and simple regression;
- M08 — multiple regression;
- M09 — interactions and nonlinearity;
- M10 — diagnostics and validation;
- M11 — introductory multivariate analysis;
- M12 — high-dimensional biological case.

Source mapping alone is not treated as completed verification.

## Findings and additions

### M01

Existing coverage of R objects, factors, indexing, identifiers, missingness, assertions, clean-session execution, and traceable output is consistent. No duplicate teaching block was added. Source-basis metadata is now explicit.

### M02

Existing coverage of centre, dispersion, robust summaries, outlier investigation, quality rules, visual encoding, denominators, uncertainty, and causal boundaries is consistent. No duplicate teaching block was added. Source-basis metadata is now explicit.

### M03 — Bayesian updating and base rates

The module already distinguished `P(disease | positive)` from `P(positive | disease)`, but lacked a complete numerical update. The extension now covers:

- sensitivity and specificity as oppositely conditioned probabilities;
- prevalence as the prior probability;
- true-positive and false-positive routes;
- the total-positive denominator;
- positive predictive value;
- dependence of predictive value on the target population;
- transportability limits.

The deterministic example uses prevalence 0.02, sensitivity 0.90, and specificity 0.95 and returns:

```text
P(D|+)=0.269
```

### M04 — bootstrap and design-preserving resampling

The module already covered estimands, standard errors, t intervals, Wilson intervals, repeated-sampling coverage, effective sample size, and precision. The extension adds:

- resampling with replacement at the original sample size;
- recalculation of the complete estimator in each replicate;
- percentile intervals;
- Monte Carlo reproducibility versus design validity;
- resampling of complete patients, pairs, clusters, or blocks when dependence is present;
- the limits of bootstrap under bias, poor representativeness, or measurement error.

The deterministic example exhaustively enumerates all `4^4 = 256` bootstrap samples for four observations and returns:

```text
observed=5.00
resamples=256
ci=[2.75, 7.75]
```

## Version state

- M01: `1.0.0` — reviewed, no visible extension;
- M02: `1.0.0` — reviewed, no visible extension;
- M03: `1.1.0` — Bayesian extension;
- M04: `1.1.0` — bootstrap extension;
- M05–M12: `1.0.0` — focused review pending.

Experimental-data acquisition remains deferred. Synthea and bounded synthetic matrices are not treated as substitutes for external biological evidence.
