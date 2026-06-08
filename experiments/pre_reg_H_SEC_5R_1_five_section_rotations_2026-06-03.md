# Pre-Registration: H-SEC-5R-1
## Hypothesis: Five Manuscript Sections Each Use a Distinct Cipher Rotation

**Filed:** 2026-06-03
**Batch:** 5024 (sequential after batch5023)
**Status:** PRE-REGISTERED — section sweeps not yet run

---

## Background

The Voynich manuscript has five structurally distinct text sections confirmed by terminal class grammar analysis:
- **§H** (f1–f66): herbal/pharmacological — GL-CHY-1 (-chy 3.85×), GL-HO-1 (-ho 9.21×)
- **§A** (f67–f74): astrological/timing — GL-EOS-1 (-eos 8.23×), GL-OLY-1 (-oly 5.66×), GL-AKAL-1 (-al 4.92×)
- **§B** (f75–f84): biological/anatomical — GL-BCHAN-1 (rtsa anatomical), GL-EDY-1 (-edy §B enriched)
- **§S** (f87–f102): pharmaceutical recipes — H-SCHAN-1 (channel recipes)
- **§T** (f103–f116): prescription codex — GL-TCOLD-1 (-lk 15.4× §T enriched)

The Alberti cipher was confirmed at R=14 for the full corpus (p=8.43×10⁻¹², 9/9 crib tests). The §A astrological section is now EXPLORATORY-STRONG for R=11: terminal class -eos → 'modcth' (Jupiter+warm) ×9 and 'ododcth' (stars-plural+warm) ×4 at R=11; absent at R=14.

Sir Ric's observation (2026-06-03 session): exactly 5 R values (R=0, R=7, R=9, R=11, R=14) show significantly elevated vocabulary matches in R-sweeps across the corpus. There are exactly 5 manuscript sections. The conjunction is not coincidental — it suggests one rotation per section.

This is consistent with standard Alberti cipher design: the outer ring rotates, and the rotation position can be changed by agreement between encipherer and decipherer. Using distinct rotations for distinct content domains adds a second layer of protection beyond the cipher itself.

---

## Hypothesis (H1)

**Each of the five Voynich manuscript sections uses a distinct Alberti cipher rotation:**

- §H (herbal/pharmacological): R = one of {0, 7, 9, 14}
- §A (astrological): R = 11 (EXPLORATORY-STRONG, established in pre_reg_GL_SA_R11_1)
- §B (biological/anatomical): R = one of {0, 7, 9, 14}
- §S (pharmaceutical recipes): R = one of {0, 7, 9, 14}
- §T (prescription codex): R = one of {0, 7, 9, 14}

The specific R values for §H, §B, §S, §T are not yet predicted (exploratory sweep required first). Once each section's candidate R is identified, a pre-registered confirmatory test will follow for each.

---

## Predicted Evidence (if H1 is true)

1. **Terminal class vocabulary:** For each section's confirmed grammar-law terminal classes, decoding at the correct section R will produce semantically coherent vocabulary (botanical for §H, anatomical for §B, recipe terms for §S, prescription terms for §T) at a significantly higher rate than R=14.

2. **Section exclusivity:** §A-exclusive vocabulary decoded at R=11 should outperform all other R values (established as EXPLORATORY-STRONG). Similarly, §H-exclusive vocabulary should decode better at its specific R than at R=14 or R=11.

3. **Mutual independence:** The optimal R for §H should NOT produce meaningful §A vocabulary, and vice versa. Each section's R should be selective.

4. **The five R values {0, 7, 9, 11, 14} should cover all five sections with minimal overlap.** No two sections should share an optimal R.

---

## Falsification Criteria

H1 is **falsified** if:
- No section (other than §A) shows a significantly different R from R=14 by its section-appropriate vocabulary scoring
- The five R values observed in R-sweeps are explained by properties of the cipher alphabet and vocabulary structure independent of section boundaries
- A section-exclusive vocabulary test shows R=14 > R=X for all sections other than §A

H1 is **downgraded to COINCIDENCE** if:
- R=11 is the global winner across all sections (indicating scoring bias rather than section-specific rotation)
- The "five R values" reduce to R=11 winning everywhere due to phonological properties

---

## Confirmatory Test Plan

For each section: extract section-exclusive terminal class tokens → decode at R=0, 7, 9, 11, 14 → score against section-appropriate vocabulary → Fisher exact test comparing candidate R vs R=14.

Section-appropriate vocabularies to be built from:
- §H: Tibetan/Mongolian plant names, preparation terms, pharmacological vocabulary (rGyud bzhi materia medica)
- §B: Anatomical channel terms (rtsa, lus, snying, mkhal), humoral vocabulary
- §S: Recipe/preparation terms, ingredient classes, measurement vocabulary
- §T: Prescription format terms, disease categories, treatment types

Current progress:
- §A: EXPLORATORY-STRONG (R=11, terminal class analysis complete)
- §H: Exploratory sweep in progress (batch5024)
- §B, §S, §T: Not yet started

---

## Protocol

Pre-registered: 2026-06-03, before running §H sweep.
Analysis script: `code/section_r_sweep.py` (to be written)
Output: `experiments/results/section_r_sweep_2026-06-03.md`

---

*Filed under THEOS Standard: Iron Law 2 — Never run a test before stating the hypothesis.*
*Iron Law 5: R=14 remains the confirmed corpus rotation. This hypothesis tests SECTION-SPECIFIC variants only.*
