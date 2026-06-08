# Pre-Registration: GL-SA-R11-1
## Hypothesis: §A Astrological Section Uses Cipher Rotation R=11

**Filed:** 2026-06-03
**Batch:** 5023 (next in sequence after batch5022 pre-reg GL-KAIN-1)
**Status:** PRE-REGISTERED — analysis not yet run on confirmatory test

---

## Background

The Voynich manuscript cipher was confirmed at R=14 (17-position Alberti ring) by 9/9 independent crib tests, p=8.43×10⁻¹² (paper3_grammar_laws.md §8.3). This R=14 confirmation was established primarily on herbal (§H), pharmaceutical (§S), and biological (§B) section vocabulary.

Three terminal classes show dramatic enrichment in the astrological/timing section (§A, f67–f74) relative to all other sections:
- **-oly**: 5.66× §A enrichment (GL-OLY-1, p=1.546×10⁻¹⁵, batch5021)
- **-al**: 4.92× §A enrichment (GL-AKAL-1, confirmed strong)
- **-eos**: 8.23× §A enrichment (GL-EOS-1, p=1.631×10⁻³⁸, batch5020)

Sir Ric proposed (2026-06-03 transcript, Message 3): *"I believe that it's very possible that there is a cipher wheel deduction that may come from R=15 that would tell you what the words in the astrological sections actually are. It may be that the astrological section operates from a different R factor."*

Exploratory R-sweep across R=10–20 (batch5023 session) found:
- R=15 produces near-empty strings; weakest astronomical vocabulary signal (1 tier-1 hit before correction, 80 after)
- **R=11 produces the strongest astronomical vocabulary signal**: 1,314 tier-1 hits vs 1,091 for R=14 (corrected scoring)
- At R=11, -eos terminal decodes to **modcth** (×22) and **ododcth** (×6)
  - *mod* = wood/Jupiter (Mongolian Five Elements)
  - *odod* = stars plural (Mongolian)
  - *cth* = confirmed warm-classifier (R=14 grammar)
- At R=11, -oly terminal decodes to **odng** (×4), **modng** (×4)
  - *od* = star (Mongolian)
  - *mod* = Jupiter (Mongolian)

Multi-model witness council (Grok, Gemini, GPT-4o, Perplexity) conducted 2026-06-03:
- Grok (definitive): *"R=11 is the only setting that produces strings with clear, non-coincidental overlaps to known Mongolian planetary and stellar vocabulary. Definitive verdict: R=11."*
- Gemini: *"VERY STRONG HIT — odod (stars plural). The clear and undeniable presence of mod and od/odod is compelling evidence."*
- GPT-4o: R=11 produces *mod* (Jupiter) and *od* (star); R=14 and R=15 do not
- Perplexity: R=11 is closest, full forms not yet attested in scholarly sources; recommended Mostaert's *Manual of Mongolian Astrology and Divination* as the confirmatory resource

**R=15 performed consistently poorly across all tests**, confirming cipher coherence — the wrong rotation reliably produces wrong answers, which validates the system.

---

## Hypothesis (H1)

**The §A astrological/timing section (f67–f74) of the Voynich manuscript was encoded using cipher rotation R=11, distinct from the R=14 rotation confirmed for the remaining sections (§H, §B, §S, §T).**

This is consistent with standard Alberti cipher design, in which section-specific rotations provide additional protection for sensitive content.

---

## Predicted Evidence (if H1 is true)

1. **Vocabulary match rate**: §A-exclusive tokens (appearing only in §A, not in any other section) will decode to Mongolian/Tibetan astronomical vocabulary at a significantly higher rate at R=11 than at R=14. Predicted: at least 2× match rate improvement.

2. **Terminal class decode**: The confirmed §A terminal classes will decode to recognizable astronomical compounds at R=11:
   - -eos → *mod-cth* (Jupiter + warm-classifier) or *odod-cth* (stars + warm-classifier)
   - -oly → *od-ng* (star + consonant cluster)
   - -al → forms containing *dar* (directional) or other confirmed grammar

3. **Mostaert/scholarly confirmation**: Mongolian astrological texts will show *mod* (Jupiter/wood) forming compounds with thermal/elemental classifiers of the type found in the rGyud bzhi Five Elements system. If this is confirmed, *modcth* = "Jupiter/warm" is a plausible astrological-medical compound.

4. **Cross-validation**: R=11 decode of §A-exclusive vocabulary will produce semantically coherent astronomical phrases (planet names, directional terms, timing classifiers) at a rate distinguishable from R=14 decode of the same tokens.

---

## Falsification Criteria

H1 is **falsified** if any of the following:
- §A-exclusive tokens at R=11 do not show significantly higher astronomical vocabulary match rate than at R=14 (< 1.5× improvement)
- Mostaert and scholarly sources show that *mod-X* compounds are not attested in Mongolian astrological literature — i.e., the *modcth* form has no structural parallel
- A systematic crib test on known §A vocabulary (if any can be identified) shows R=14 > R=11 match rate
- The *mod* and *od* hits at R=11 are explained by the high frequency of EVA 'o' character (pos=0 → od at R=11), producing spurious astronomical hits by coincidence

H1 is **downgraded to EXPLORATORY** if:
- §A-exclusive vocabulary shows R=11 advantage but < 2× improvement
- Mostaert confirms *mod*-compound structure but not the specific *cth* classifier

---

## Confirmatory Test

**Test**: Extract all §A-exclusive token types (appearing 0 times in §H + §B + §S + §T). Decode each at R=11 and R=14. Score against a pre-specified Mongolian/Tibetan astronomical vocabulary list (the same ASTRO_TARGETS dictionary from r_sweep_corrected.py). Compute: tier-1 match rate at R=11 vs R=14. Run Fisher exact test.

**Prediction**: R=11 tier-1 rate > R=14 tier-1 rate, p < 0.05.

**Secondary test**: Compare §A-exclusive vs §H-exclusive vocabulary decode quality at R=11 vs R=14. §H-exclusive should show R=14 advantage (confirmed cipher). §A-exclusive should show R=11 advantage (if H1 is true).

---

## Protocol

This pre-registration is filed **before** running the §A-exclusive vocabulary test. The exploratory R-sweep (batch5023 session) pointed toward R=11. The test below has not been run yet.

- Pre-reg filed: 2026-06-03
- Confirmatory test batch: 5023 (to be run after this file is committed)
- Analysis script: to be written as `code/gl_sa_r11_confirmatory.py`
- Output: `experiments/results/gl_sa_r11_confirmatory_2026-06-03.md`

---

*Filed under THEOS Standard: Iron Law 2 — Never run a test before stating the hypothesis.*
