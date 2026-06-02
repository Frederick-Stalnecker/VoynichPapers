# THEOS Research Institute — Voynich Atlas

**Author:** Frederick Davis Stalnecker  
**Institution:** THEOS Research Institute  
**Contact:** frederick.stalnecker@theosresearch.org  
**Status:** Active — chapters in development (2026)

---

## What This Atlas Is

This directory contains the working manuscript for the *Voynich Atlas* — a comprehensive scholarly work documenting the decipherment of the Voynich Manuscript (Beinecke MS 408, Yale University) as a hybrid Classical Mongolian / Tibetan Sowa Rigpa pharmaceutical text, encrypted by a rotational substitution cipher calibrated at R=14.

The Atlas is the long-form companion to the statistical evidence repository in the parent directory. Where the evidence repository provides reproducible quantitative proof, the Atlas provides historical context, instrument comparisons, manuscript analysis, and the full scholarly argument.

---

## Canonical Anchor Document

> **All chapter authors and AI collaborators MUST read the following document before beginning any chapter or section:**
>
> [`07_briefing_cards/chatgpt_atlas_briefing_cards_2026-06-02.md`](07_briefing_cards/chatgpt_atlas_briefing_cards_2026-06-02.md)

This briefing cards document is the **single authoritative source of record** for:

- The confirmed decipherment findings as of June 2, 2026
- The pre-registered hypotheses and their current status
- The historical and linguistic framework (Timurid, Mongolian, Tibetan Sowa Rigpa)
- The instrument tradition context (volvelle, equatorium, astrolabe)
- The terminology and nomenclature conventions used throughout the Atlas
- The boundaries of confirmed vs. working vs. falsified hypotheses

**Do not begin writing any chapter without anchoring it to this document.** This prevents drift into unrelated Voynich folklore, speculative theories, or claims that contradict the pre-registered evidence base.

---

## Directory Structure

| Folder | Contents |
|---|---|
| `00_master_outline/` | Master outline, table of contents, editorial rules |
| `01_historical_foundation/` | Timurid scientific world, Iskandar horoscope, al-Kashi, Plate of Heavens, Plate of Conjunctions |
| `02_instrument_tradition/` | Equatorium, astrolabe, volvelle, saphea, armillary sphere, celestial globe, quadrant |
| `03_vms_comparisons/` | f57v timing volvelle, f67r1 solar wheel, f67r2 lunar wheel, nine-rosette foldout, comparison tables |
| `04_medical_sections/` | Herbal section, bath section, prescription codex, closing inscription |
| `05_figures/` | Source images, AI reconstructions, book spreads, print-ready assets |
| `06_citations/` | Primary sources, secondary sources, manuscript catalog, bibliography |
| `07_briefing_cards/` | **Canonical anchor document** — read before all chapter work |
| `08_theos_findings/` | Confirmed findings, working hypotheses, falsified hypotheses |
| `09_publication/` | Submission packages for Cryptologia, arXiv, and the book manuscript |

---

## Editorial Rules

1. **Anchor first.** Every chapter begins by citing the relevant briefing card section.
2. **No folklore.** Claims not grounded in the pre-registered evidence base or primary source documents do not belong in this Atlas.
3. **Distinguish status.** Always mark whether a claim is CONFIRMED, WORKING HYPOTHESIS, or FALSIFIED. See `08_theos_findings/` for the master status list.
4. **Cite everything.** All historical claims require a primary or secondary source citation from `06_citations/`.
5. **Figures go in `05_figures/`.** Do not embed images inline in chapter files; reference them by path.

---

*This Atlas is part of the THEOS Research Institute's open-science commitment. The statistical evidence underlying all claims is independently reproducible via `../reproduce.sh`.*
