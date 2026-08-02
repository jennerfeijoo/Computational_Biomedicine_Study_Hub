# BMB830 source-grounded audit

## Boundary

The active public SDU description defines the curricular scope. It requires R scripting, basic probability, statistical modelling, visualisation, interpretation, introductory multivariate analysis, biological-data analysis, critical discussion of published methods, tutorial/exercise completion, and an individual oral examination.

The public description does not expose the complete Itslearning reading list, exercise specification, grading criteria, or examination prompts. Those elements remain outside the repository evidence model and are not reconstructed.

## Reference families

The audit uses:

- the active SDU BMB830 description;
- *Introduction to Modern Statistics*, second edition, for data, exploratory analysis, probability, inference, randomization tests, group comparison, regression, and model interpretation;
- *An Introduction to Statistical Learning with Applications in R*, second edition, for statistical learning, resampling, model assessment, and validation;
- the uploaded Yachay Tech probability/statistics notes;
- the uploaded Yachay Tech biostatistics and linear-model notes.

Visible teaching material remains original trilingual paraphrase and adaptation. Textbook prose, figures, tables, and proprietary exercises are not reproduced.

## Current focused review

Reviewed and marked `consistent`:

- M01 — R foundations and reproducible workflow;
- M02 — data quality, descriptive summaries, and visualisation;
- M03 — probability, sampling, and distributions;
- M04 — estimation and confidence intervals;
- M05 — hypothesis testing, errors, power, and randomization tests;
- M06 — group comparison, ANOVA, and planned contrasts.

Pending focused review:

- M07 — correlation and simple regression;
- M08 — multiple regression;
- M09 — interactions and nonlinearity;
- M10 — diagnostics and validation;
- M11 — introductory multivariate analysis;
- M12 — high-dimensional biological case.

Source mapping alone is not treated as completed verification.

## Findings and additions

### M01

Existing coverage of R objects, factors, indexing, identifiers, missingness, assertions, clean-session execution, and traceable output is consistent. No duplicate teaching block was added. Source-basis metadata is explicit.

### M02

Existing coverage of centre, dispersion, robust summaries, outlier investigation, quality rules, visual encoding, denominators, uncertainty, and causal boundaries is consistent. No duplicate teaching block was added. Source-basis metadata is explicit.

### M03 — Bayesian updating and base rates

The module already distinguished `P(disease | positive)` from `P(positive | disease)`, but lacked a complete numerical update. The extension covers:

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

### M05 — randomization tests and exchangeability

The module already covered null and alternative hypotheses, one- and two-sided tests, p-values, type I and type II errors, power, minimum relevant effects, and effect-size reporting. The extension adds:

- construction of a null distribution through permitted reassignments;
- exchangeability as a design-dependent condition;
- preservation of group sizes for independent comparisons;
- within-pair swaps or sign flips for paired designs;
- cluster-level reassignment for clustered designs;
- consistent calculation of observed and null statistics;
- exhaustive enumeration versus Monte Carlo correction.

The deterministic example enumerates all twenty assignments of six observations to two groups of three and returns:

```text
observed=4.33
assignments=20
p=0.100
```

### M06 — ANOVA decomposition and planned contrasts

The module already covered independent and paired comparisons, Welch procedures, ANOVA, rank-based alternatives, assumptions, and multiplicity boundaries. The extension adds:

- the between-group and within-group decomposition;
- the F ratio as signal relative to residual variation;
- the global null that all population means are equal;
- the limited conclusion that at least one mean differs;
- planned contrasts as prespecified scientific comparisons;
- multiplicity control for exploratory pairwise families;
- the boundary between classical and Welch ANOVA under heteroscedasticity.

The deterministic example calculates the ANOVA decomposition for three balanced groups and returns:

```text
F=13.00
p=0.0066
C_minus_A=4.00
```

## Version state

- M01: `1.0.0` — reviewed, no visible extension;
- M02: `1.0.0` — reviewed, no visible extension;
- M03: `1.1.0` — Bayesian extension;
- M04: `1.1.0` — bootstrap extension;
- M05: `1.1.0` — randomization-test extension;
- M06: `1.1.0` — ANOVA and contrast extension;
- M07–M12: `1.0.0` — focused review pending.

Experimental-data acquisition remains deferred. Synthea and bounded synthetic matrices are not treated as substitutes for external biological evidence.
