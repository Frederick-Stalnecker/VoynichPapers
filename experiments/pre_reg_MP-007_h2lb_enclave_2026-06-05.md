# Pre-Registration: Hand-2 / Language-B Bifolio Enclave Pattern in §H

**Date:** 2026-06-05
**Batch:** 5164 (registration)
**Status:** PRE-REGISTERED
**Origin:** Decipherment pass surfaced f26r/v, f31r/v, f33r/v, f34r as Hand-2 / Language-B folios within §H. The pattern appears bifolio-level (both recto and verso of the same physical leaf carry H2/LB). MP-007 was at HYP-strong status. This pre-reg tests it corpus-wide.

---

## H1 — Hand-2/Lang-B forms bifolio enclaves in §H, with specific structural correlates

**Hypothesis:** When a §H folio carries Hand-2 / Language-B (per IVTFF header `$H=2 $L=B`), it:
- (a) Is paired with its bifolio mate also carrying H2/LB (bifolio-level co-occurrence ≥ 80%)
- (b) Clusters in §H Quire D and E, not in Quire A or B (non-uniform distribution)
- (c) Shows DIFFERENT scribal-structural profile than H1/LA folios (lower dal-density, different layout)

**Null hypothesis:** H2/LB folios are randomly distributed in §H, with no bifolio-pairing preference and no quire-level clustering.

---

## Specific Predictions (numbered, locked)

### P1 — Bifolio-level pairing
**Prediction:** Of all H2/LB folios in §H, ≥ 80% have their bifolio mate (same `$F` field within same `$Q`) also H2/LB.

**Operational definition:** Two folios are bifolio mates if they share the same `$F` (bifolio designator) and `$B` (sheet) within the same `$Q` (quire). One is recto, one is verso.

**Falsification:** If < 50% of H2/LB folios have H2/LB mates, P1 fails (random distribution).

### P2 — Quire-level clustering
**Prediction:** H2/LB folios in §H are concentrated in Quires D and E. Specifically:
- ≥ 70% of §H H2/LB folios are in Quire D or E
- ≤ 30% are in Quire A, B, or C

**Falsification:** If H2/LB folios are uniformly distributed across §H quires, P2 fails.

### P3 — Lower dal-density on H2/LB folios
**Prediction:** Mean dal-class marker count per line is LOWER on H2/LB folios than on H1/LA folios in §H. Specifically:
- H2/LB mean dal/line ≤ 0.7 × H1/LA mean dal/line

**Operational definition:** Count `\bdal\b` substring matches in tokens; divide by line count per folio.

**Falsification:** If H2/LB mean dal/line is ≥ H1/LA mean, P3 fails.

### P4 — §T or §A terminal import on H2/LB
**Prediction:** H2/LB folios show ≥ 1.5× the rate of §T-class (`-daly`) or §A-class (`-eos`) terminals per token compared to H1/LA folios in §H.

**Operational definition:** Count tokens ending in `daly` or `eos`; divide by total tokens per folio. Compare H2/LB folio mean rate vs H1/LA folio mean rate.

**Falsification:** If H2/LB rate < H1/LA rate, P4 fails.

---

## Method

### Step 1 — Parse IVTFF headers
For each folio in the corpus:
- Extract `$Q`, `$F`, `$B`, `$L`, `$H` from the IVTFF header line
- Identify §H folios (typically Quires A through E, i.e., $Q ∈ {A, B, C, D, E})
- Classify each folio as H1/LA, H2/LB, or other

### Step 2 — Bifolio pairing analysis
For each H2/LB §H folio, find its bifolio mate (same $Q + $F + $B). Determine if mate is also H2/LB. Compute pairing rate.

### Step 3 — Quire distribution
Tally H2/LB folios per quire. Compute distribution.

### Step 4 — Structural metrics
For each §H folio:
- Count lines
- Count `\bdal\b` matches (dal-class markers)
- Count tokens ending in `daly` (§T-class)
- Count tokens ending in `eos` (§A-class)

Compute means for H2/LB folios vs H1/LA folios.

### Step 5 — Tests
- P1: H2/LB bifolio-pair rate
- P2: H2/LB quire distribution
- P3: Welch's t comparing dal/line between groups
- P4: Welch's t comparing -daly/-eos rate between groups

---

## What the result will mean

### If all four pass
MP-007 promotes from HYP to CFM. Paper gets a structural §H sub-class finding. The "second scribe" hypothesis is confirmed at the bifolio level.

### If P1 + P2 pass, P3/P4 fail
Bifolio enclave pattern is confirmed but the scribal-style differences may have been over-claimed. CFM at structural level only.

### If only P1 passes
H2/LB folios pair at bifolio level but don't cluster by quire. Weaker structural finding.

### If P1 fails
H2/LB folios are not bifolio-paired. MP-007 is rejected; the pattern is artifact of sample size.

---

## Pre-registration commitment

Committed to all three remotes BEFORE audit code is written or run. Iron Law 2 honored.

*pre_reg_MP-007_h2lb_enclave_2026-06-05.md — batch5164 — THEOS — 247-365*

---

## Results (batch5164)

**Audit:** `experiments/audit_MP-007_h2lb_enclave_2026-06-05.py`
**Output:** `experiments/results/audit_MP-007_h2lb_enclave_2026-06-05.txt`

### Corpus state
- §H folios (Quires A-E): 78
- H1/LA folios: 66
- **H2/LB folios: 12** (across 6 bifolios)
- Other: 0

### H2/LB folio inventory (verified by IVTFF header grep)

| Bifolio | Quire | Folios |
|---------|-------|--------|
| $F=b $B=2 | D | f26r, f26v |
| $F=y $B=2 | D | f31r, f31v |
| $F=a $B=1 | E | f33r, f33v |
| $F=b $B=2 | E | f34r, f34v |
| $F=y $B=2 | E | f39r, f39v |
| $F=z $B=1 | E | f40r, f40v |

### Predictions vs results

| Pred | Threshold | Observed | Status |
|------|-----------|----------|--------|
| **P1** bifolio pairing ≥80% | 80% | **100%** (12/12) | **PASS** |
| **P2** Quire D+E ≥70% | 70% | **100%** | **PASS** |
| **P3** dal-density ≤0.70× | 0.70× | **2.582×** (HIGHER) | **FAIL** |
| **P4** section-terminals ≥1.5× | 1.5× | **5.966×** | **PASS** |

### Verdict

**MP-007 STRUCTURALLY CONFIRMED.** Bifolio pairing is absolute (100%); quire concentration is absolute (100% in D+E); section-terminal import is strong (5.97×). The "second scribe writes specific bifolios" hypothesis is confirmed.

P3 fails honestly: H2/LB folios have HIGHER dal density (2.58×), not lower. The earlier subagent observation about low dal on f31r was a single-folio anomaly, NOT a sub-class pattern. Honest correction logged.

### What this means

- §H has 6 H2/LB bifolios totaling 12 folios — all in Quires D and E.
- Quire E is roughly half H2/LB (8 of ~16 folios).
- H2/LB writes with the same general scribal habits BUT imports §T/§A vocabulary (-daly, -eos terminals) at 5.97× the H1/LA rate.
- The dal-density is HIGHER on H2/LB, not lower — the second hand is even more dal-saturated than the first.

### Paper impact

§8 of paper3 gets a new sub-section on the §H bifolio enclave pattern. Worth a paragraph + table showing the 6 bifolios. Possible interpretations:
- Second scribe contributed bifolios as division of labor
- Second scribe was writing different MATERIAL (cross-section vocabulary)
- Bifolios from a different exemplar source were inserted

*Results committed batch5164 — 2026-06-05 — THEOS — 247-365*
