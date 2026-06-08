# Pre-Registration: §H Clock-Absent Sub-Class — Rate and Structural Correlates

**Date:** 2026-06-05
**Batch:** 5165 (registration)
**Status:** PRE-REGISTERED
**Origin:** During the decipherment pass (batches 5138–5162), clock-absent §H folios consistently appeared at ~50% rate over 7 consecutive batches (47%/47%/47%/50%/52.4%/50%/52.2%). MP-001 was at HYP-CFM-ready status. This pre-reg tests the rate corpus-wide and characterizes the sub-class.

---

## H1 — §H has a stable clock-absent sub-class of ~50% of folios, with structural correlates

**Hypothesis:** The §H corpus is approximately equally split between clock-bearing folios and clock-absent folios. The clock-absent sub-class is non-random — it correlates with comma-fragmentation (SS-001) and possibly with Hand/Language.

**Null hypothesis:** Clocks are randomly distributed across §H folios; there is no stable clock-absent sub-class.

---

## Specific Predictions (numbered, locked)

### P1 — Corpus-wide §H clock-absent rate
**Prediction:** Of the 78 §H folios (Quires A through E), the clock-absent rate is in **40%–60%**.

**Operational definition:** A folio is "clock-absent" if `grep "^<folio\." data/ZL3b-n.txt` returns zero `@\d+;` matches across all its content lines.

**Falsification:** If rate is outside the 40-60% band, P1 fails.

### P2 — Subset relationship to SS-001 (comma-frag cluster)
**Prediction:** Of clock-absent §H folios, ≥ 60% are comma-fragmentation carriers (have at least one comma-fragmented token, `xxx,yyy` pattern).

**Operational definition:** A folio is a "comma-frag carrier" if it contains at least one token matching the pattern of an EVA word containing an internal `,` (`\w+,\w+`).

**Falsification:** If overlap < 40%, P2 fails — clock-absent and comma-frag are unrelated.

### P3 — Hand/Language stratification
**Prediction:** The clock-absent rate differs between H1/LA and H2/LB folios. Specifically:
- H1/LA clock-absent rate: predict in 45%–65% range (continuing the observed pattern)
- H2/LB clock-absent rate: distinct from H1/LA (either significantly higher or lower)

**Operational definition:** Same as P1 but stratified by `$H` and `$L` fields.

**Falsification:** If H1/LA and H2/LB clock-absent rates are within 5 percentage points of each other, P3 fails — Hand/Language doesn't differentiate.

### P4 — Quire-level distribution
**Prediction:** Clock-absent rate is non-uniform across §H quires. Specifically, at least one quire has rate ≥ 60% and at least one has rate ≤ 40%.

**Operational definition:** Stratify by `$Q`. Compute clock-absent rate per quire.

**Falsification:** If all quires have rates within the 40-60% band (i.e., uniformity), P4 fails — there's no quire-level structure to the clock distribution.

---

## Method

### Step 1 — Parse IVTFF headers
Extract `$Q`, `$F`, `$B`, `$L`, `$H` for each folio (already done in MP-007 audit; reuse).

### Step 2 — Per-folio clock check
For each §H folio:
- Grep content lines for `@\d+;` pattern
- Record clock-present (≥1 clock) or clock-absent (0 clocks)

### Step 3 — Per-folio comma-frag check
For each §H folio:
- Grep content lines for `\w+,\w+` patterns (excluding scribal corrections; specifically tokens with internal comma)
- Record as comma-frag-carrier or not

### Step 4 — Compute rates
- §H overall clock-absent rate
- §H clock-absent ∩ comma-frag overlap
- H1/LA vs H2/LB clock-absent rates
- Per-quire clock-absent rates

### Step 5 — Compare to predictions
P1-P4 against thresholds.

---

## What the result will mean

### All 4 pass
MP-001 promotes to CFM. The clock-absent sub-class is real, correlates with SS-001, varies by Hand/Language, and shows quire-level structure. Paper-grade.

### 3 of 4
Sub-class is real and has at least one strong correlate; paper sub-section warranted.

### 2 or fewer
Sub-class may exist but lacks meaningful correlates. Demote to OBS.

### P1 fails
The 50% observation was sampling artifact. Sub-class hypothesis rejected.

---

## Pre-registration commitment

Committed to all three remotes BEFORE audit code runs. Iron Law 2 honored.

*pre_reg_MP-001_clock_absent_2026-06-05.md — batch5165 — THEOS — 247-365*

---

## Results (batch5165)

**Audit:** `experiments/audit_MP-001_clock_absent_2026-06-05.py`
**Output:** `experiments/results/audit_MP-001_clock_absent_2026-06-05.txt`

### Headline numbers
- §H folios: 78
- Clock-absent: 45 (57.7%)
- Clock-absent ∩ comma-frag: 45/45 = 100%

### Predictions vs results

| Pred | Threshold | Observed | Status |
|------|-----------|----------|--------|
| P1 §H rate 40-60% | 40-60% | **57.7%** | **PASS** |
| P2 overlap ≥60% | 60% | **100%** | **PASS** |
| P3 H1/H2 diff ≥5pp | 5pp | **10.6pp** | **PASS** |
| P4 at least one quire ≥60% AND ≤40% | bounds | max 75%, min 43.8% | **FAIL** |

### Quire stratification
- Quire A: 56.2% clock-absent
- Quire B: 57.1%
- Quire C: 43.8% (lowest)
- Quire D: 56.2%
- Quire E: 75.0% (highest — Quire E is the most clock-absent, partially driven by H2/LB enclaves)

### Verdict

**MP-001 STRONG (3/4 PASS).** The clock-absent sub-class is real. Key findings:
- **100% subset relationship** to comma-frag (SS-001) — every clock-absent §H folio is also a comma-frag carrier. This is the strongest finding.
- H2/LB folios are MORE clock-absent than H1/LA (66.7% vs 56.1%).
- Quire E is the most clock-absent (75%), driven partly by H2/LB enclaves.

P4 fails honestly: no quire goes below 40% (Quire C at 43.8% is closest). The pattern is real but not as strictly quire-stratified as I predicted. The 100% comma-frag subset is the more important finding.

### Paper impact
§8 gets a sub-section on §H clock-absent sub-class. The 100% subset relationship to comma-frag is paper-grade evidence for a coherent scribal/textual sub-class.

*Results committed batch5165 — 2026-06-05 — THEOS — 247-365*
