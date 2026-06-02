# Atlas Editorial Standards
**THEOS Research Institute — Voynich Atlas**  
**Author:** Frederick Davis Stalnecker  
**Status:** Binding — applies to all contributors, human and AI  
**Last updated:** June 2, 2026

---

> **Before contributing to any chapter, read the canonical anchor document:**  
> [`../07_briefing_cards/chatgpt_atlas_briefing_cards_2026-06-02.md`](../07_briefing_cards/chatgpt_atlas_briefing_cards_2026-06-02.md)

---

## Purpose

This file establishes the editorial standards that govern all content in the THEOS Research Institute Voynich Atlas. These rules apply equally to human authors, AI collaborators (ChatGPT, Claude, Manus, and others), and any future contributors. Their purpose is to ensure that the Atlas remains internally consistent, academically credible, and clearly distinguished from the large body of speculative Voynich literature.

---

## 1. The Four Content Categories

Every claim, paragraph, and figure in the Atlas must belong to exactly one of the following four categories. The category must be stated explicitly at the top of each chapter section.

| Category | Definition | Label to use |
|---|---|---|
| **Historical Foundation** | Claims about the historical world (Timurid court, Islamic astronomy, Mongolian medicine, Tibetan Sowa Rigpa) that are independently documented in primary or secondary sources, without reference to the Voynich Manuscript | `[HISTORICAL]` |
| **Instrument Tradition** | Descriptions of scientific instruments (astrolabe, equatorium, volvelle, etc.) drawn from documented historical sources | `[INSTRUMENT]` |
| **Structural Comparison** | Direct comparisons between Voynich Manuscript folios and historical documents or instruments, where the comparison is visual or structural and does not assert decipherment | `[COMPARISON]` |
| **THEOS Interpretation** | Claims that represent the THEOS Research Institute's specific decipherment findings, including cipher identification, language identification, and pharmaceutical register analysis | `[THEOS]` |

**Rule:** Do not mix categories within a single paragraph. If a paragraph transitions from historical context to THEOS interpretation, split it into two paragraphs with separate labels.

---

## 2. Citation Requirements

### Historical claims
Every `[HISTORICAL]` claim must be followed by a citation in the format `[Author, Year, page]`. Citations must appear in `06_citations/primary_sources.md` or `06_citations/secondary_sources.md` before the chapter is considered complete.

### Manuscript references
Every reference to a specific Voynich folio must use the standard Beinecke folio notation (e.g., f57v, f67r1, f103r) and must be accompanied by a reference to the Yale Beinecke Digital Library record where applicable.

### THEOS findings
Every `[THEOS]` claim must reference its corresponding pre-registration entry in `PRE_REGISTRATIONS.md` in the parent repository. Claims that are not pre-registered must be explicitly labeled as `[THEOS — WORKING HYPOTHESIS]` or `[THEOS — UNREGISTERED]`.

**Rule:** Unsourced historical claims will not be accepted. If a source cannot be identified, the claim must be labeled `[UNVERIFIED — SOURCE NEEDED]` and flagged for follow-up.

---

## 3. Reconstruction Labeling

Any image, figure, diagram, or text passage that represents a reconstruction — that is, a modern interpretation or re-creation of a historical object or text — must be labeled explicitly.

### Figure type labels (required in every figure caption)

| Label | Meaning |
|---|---|
| `[HISTORICAL IMAGE]` | A reproduction of an original historical document, manuscript page, or artifact |
| `[MANUSCRIPT IMAGE]` | A reproduction of a Voynich Manuscript folio from the Beinecke Digital Library |
| `[RECONSTRUCTION]` | A modern re-creation or interpretation of a historical object, based on documented sources |
| `[THEOS INTERPRETATION]` | A visual representation of a THEOS Research Institute finding or hypothesis |

**Rule:** No figure may appear in the Atlas without one of these four labels in its caption. AI-generated images must always carry either `[RECONSTRUCTION]` or `[THEOS INTERPRETATION]` — never `[HISTORICAL IMAGE]` or `[MANUSCRIPT IMAGE]`.

---

## 4. Falsifiability Requirement

Every chapter must include a section titled **"What Would Falsify This Chapter's Central Claim."** This section must state, in plain language, the specific evidence or finding that would require the chapter's central argument to be revised or withdrawn.

**Example format:**
> *The central claim of this chapter — that the f57v volvelle is structurally homologous to the Timurid equatorium tradition — would be falsified by the discovery of a pre-Timurid European instrument with an identical wheel configuration, or by a demonstration that the folio's wheel count and rotation geometry are consistent with a non-astronomical function.*

This requirement applies to all chapters in sections `01` through `04`. It does not apply to `05_figures`, `06_citations`, or `09_publication`.

---

## 5. THEOS Findings Status Labels

All `[THEOS]` claims must carry one of the following status labels, consistent with the master status list in `08_theos_findings/confirmed_findings.md`:

| Status | Meaning |
|---|---|
| `CONFIRMED` | Pre-registered, statistically tested, p-value reported in `REPRODUCTION_REPORT.md` |
| `WORKING HYPOTHESIS` | Under active investigation; not yet pre-registered or statistically tested |
| `FALSIFIED` | Previously held hypothesis that has been formally retracted; see `08_theos_findings/falsified_hypotheses.md` |
| `UNREGISTERED` | A new claim not yet entered into the pre-registration system; must be flagged for registration |

**Rule:** Do not use the word "proven" anywhere in the Atlas. Use "confirmed," "supported by," or "consistent with" instead.

---

## 6. Prohibited Content

The following types of content will not be accepted in any chapter of this Atlas:

- Alternative decipherment theories not developed by THEOS Research Institute
- References to popular Voynich folklore (Roger Bacon authorship, alien origin, Cathar heresy, etc.) unless explicitly cited and immediately refuted with evidence
- Claims about the manuscript's authorship, date, or provenance that are not grounded in the pre-registered evidence base or primary source documentation
- Speculation presented without a `[WORKING HYPOTHESIS]` label
- Passive-voice claims that obscure the source of an assertion (e.g., "it is believed that" without identifying who believes it and on what basis)

---

## 7. Workflow for AI Contributors

AI collaborators (ChatGPT, Claude, Manus, and others) must follow this sequence before contributing to any chapter:

1. **Read the briefing cards** at `07_briefing_cards/chatgpt_atlas_briefing_cards_2026-06-02.md`
2. **Read this file** in full
3. **Read the target chapter file** to understand what content already exists
4. **Identify the content category** (`[HISTORICAL]`, `[INSTRUMENT]`, `[COMPARISON]`, or `[THEOS]`) for every paragraph to be written
5. **Draft content** with all required labels, citations, and falsifiability statements
6. **Flag any claim** that cannot be sourced or categorized with `[NEEDS REVIEW]`

AI contributors must not introduce new THEOS findings. New findings must originate with Frederick Davis Stalnecker and be entered into the pre-registration system before appearing in the Atlas.

---

## 8. Version Control

All substantive changes to chapter files must be accompanied by a Git commit message that identifies:
- Which chapter was changed
- What category of change was made (new content, correction, citation added, label updated)
- Whether the change affects any pre-registered claim

**Example commit message:**
```
atlas: add [HISTORICAL] section to chapter_01 on Timurid observatory network

- Added three paragraphs on Ulugh Beg's Samarkand observatory
- Citations added to 06_citations/primary_sources.md
- No pre-registered claims affected
```

---

*These standards were established by Frederick Davis Stalnecker, THEOS Research Institute, June 2, 2026, in consultation with ChatGPT (OpenAI) and Manus (Manus Team). They are binding on all future contributors.*
