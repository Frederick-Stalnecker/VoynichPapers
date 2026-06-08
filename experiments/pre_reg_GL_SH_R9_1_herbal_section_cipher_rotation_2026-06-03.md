# Pre-Registration: GL-SH-R9-1
## Hypothesis: §H Herbal Section Uses Cipher Rotation R=9

**Filed:** 2026-06-03
**Batch:** 5025 (sequential after batch5024)
**Status:** PRE-REGISTERED — confirmatory test not yet run

---

## Background

The five-section R-sweep (batch5024) tested all §H confirmed terminal classes against a section-appropriate vocabulary at R=0, 7, 9, 11, 14, 15. Result: **R=9 wins all four §H terminal classes:**

| Terminal | R=9 hits | R=14 hits | Ratio | Top R=9 form |
|----------|----------|----------|-------|--------------|
| -chy (n=496) | 31 | 6 | 5.2× | cthdar×87 |
| -ho (n=127) | 8 | 0 | ∞ | uga×74 |
| -or (n=832) | 24 | 17 | 1.4× | ctha×159 |
| -ol (n=859) | 21 | 4 | 5.3× | cthap×230 |

Note: the hit counts above used a §H vocabulary list that partially overlapped with the output phoneme space. The confirmatory test will use a CORRECTED vocabulary built from output-achievable phoneme sequences.

**Qualitative analysis of R=9 forms:**
- -chy → `cthdar` (warm-classifier + directional/ablative) — pharmacological completion marker ("warm-outgoing")
- -ho → `uga` (root-cold-thermal + connector 'a') — in-process marker ("from the root")
- -or → `ctha` (warm-classifier + connector 'a') — channel-treatment marker
- -ol → `cthap` (warm-classifier + 'ap' ?) — recipe marker

The parallel: §A -eos at R=11 → 'modcth' (Jupiter+warm) + 'ododcth' (stars+warm). §H -chy at R=9 → 'cthdar' (warm+directional). The structure is REVERSED in §H: the warm-classifier leads rather than trails. This is consistent with a different section register.

**Sir Ric's observation** (2026-06-03): f57v volvelle at §H/§A boundary functions as a cipher reconfiguration signal. If §H uses R=9 and §A uses R=11, f57v marks the transition at f57v.

---

## Hypothesis (H1)

**The §H herbal/pharmacological section (f1–f66) of the Voynich manuscript was encoded using cipher rotation R=9, distinct from the R=14 rotation confirmed for the corpus and R=11 confirmed for §A.**

---

## Predicted Evidence (if H1 is true)

1. **Terminal class vocabulary:** §H terminal class tokens (-chy, -ho, -or, -ol) will decode to pharmacological/botanical compound vocabulary at significantly higher rates at R=9 than at R=14. Predicted: ≥2× improvement, p<0.05.

2. **Qualitative coherence:** The confirmed §H grammar-law terminal classes should decode to recognizable Tibetan/Mongolian pharmacological compound forms at R=9:
   - -chy → forms containing 'cth' (warm) + directional/ablative modifier (preparation COMPLETE)
   - -ho → forms containing 'ug' (root) or similar base + extension (preparation IN-PROCESS)
   - These forms should be ABSENT or less frequent at R=14

3. **Control check:** §A terminal class tokens (-eos, -oly, -al) should NOT show R=9 advantage (they should show R=11 advantage — already confirmed).

4. **f57v placement:** The cipher volvelle is at f57v (last folio of §H). If §H=R=9 and §A=R=11, f57v marks a rotation change from R=9 to R=11. This would explain why the volvelle is depicted AT the section boundary.

---

## Falsification Criteria

H1 is **falsified** if:
- §H terminal class tokens at R=9 do NOT show ≥2× higher pharmacological vocabulary hit rate than R=14
- The R=9 advantage for §H is explained by properties of the cipher alphabet (e.g., EVA patterns in §H happen to map to OUTER positions that produce common phonemes at R=9 regardless of content)
- §H-exclusive vocabulary at R=9 does not outperform §H-exclusive vocabulary at R=14 in Fisher exact test (p<0.05)

H1 is **downgraded to EXPLORATORY** if:
- R=9 shows advantage but ratio < 2×
- The vocabulary list used is insufficient to discriminate (too few achievable §H-appropriate terms)

---

## Confirmatory Test

**Test:** Extract §H terminal class tokens (-chy, -ho). Decode at R=9 and R=14. Score against a pre-specified §H pharmacological vocabulary list built from ACHIEVABLE phoneme sequences in the cipher output alphabet. Run Fisher exact test.

**Critical requirement:** The vocabulary list must consist ONLY of terms that can appear in the cipher output phoneme space: {ch, ug, dal, cth, m, f, dar, t, ng, a, p, od, g, sh}. Terms like 'aru' or 'baru' that require phonemes not in the output space are inadmissible.

**Achievable vocabulary building:** Derive from:
1. Confirmed R=14 §H decode forms (the corpus at R=14 produces known §H vocabulary)
2. Witnesses asked to provide Tibetan/Mongolian pharmacological terms constructed from the 13 OUTER phonemes
3. Cross-reference with rGyud bzhi technical terms representable in this phoneme space

**Prediction:** R=9 tier-1 rate > R=14 tier-1 rate, p<0.05, ratio ≥2×.

---

## Protocol

- Pre-reg filed: 2026-06-03 (before running confirmatory test)
- Confirmatory test batch: 5025+
- Analysis script: code/gl_sh_r9_confirmatory.py (to be written after vocabulary is established)
- Vocabulary source: witnesses + derived from OUTER phoneme space analysis

---

*Filed under THEOS Standard: Iron Law 2 — Never run a test before stating the hypothesis.*
*Iron Law 5: R=14 remains confirmed for full corpus. This tests §H section-specific rotation only.*
