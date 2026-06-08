#!/usr/bin/env python3
"""
Batch 630b — Within-line position shuffle test for positional grammar laws.

Tests Laws 9 and 11, which make claims about WHERE in a line a token appears —
not which section it appears in. These cannot be tested by folio-section
permutation (batch629/630) because shuffling folios between sections preserves
within-folio line order.

Method: for each folio independently, randomly permute the tokens within each
line 10,000 times. Compute the position-based test statistic after each shuffle.
Permutation p-value = fraction of position-shuffled corpora >= observed statistic.

This is a WITHIN-LINE position shuffle: it tests whether the observed positional
patterns are more extreme than expected if each token's position within its line
were random, holding constant the set of tokens on each line.

Law 9 test: Does ot-class mean position differ between text (expected: late) and
  pharma/bio (expected: early)?
  Statistic: (mean ot-pos in text) − (mean ot-pos in pharma+bio).
  Observed should be positive (late in text, early in pharma/bio).

Law 11 test: Is cheol bimodal (early OR late) more extreme than chance?
  Statistic: proportion of cheol occurrences at position ≤0.20 OR ≥0.80.
  Observed should exceed a random-position baseline.
"""

import re
import random
from collections import defaultdict

# ── Section assignments ─────────────────────────────────────────────────────────
SECTION_RANGES = {
    'herbal': list(range(1, 58)),
    'astro':  list(range(67, 75)),
    'bio':    list(range(75, 85)),
    'pharma': list(range(87, 103)),
    'text':   list(range(103, 117)),
}

def folio_to_section(fn):
    for sec, fr in SECTION_RANGES.items():
        if fn in fr:
            return sec
    return None

def folio_num_from_tag(tag):
    m = re.match(r'<f(\d+)', tag)
    return int(m.group(1)) if m else None

def tokenise_line(raw):
    tokens = re.split(r'[., ]', raw)
    return [t.strip().lower() for t in tokens
            if t.strip() and re.match(r'^[a-z]+$', t.strip())]

# ── Load corpus at LINE level ────────────────────────────────────────────────────
print("Loading corpus (line level)...")
corpus_file = '/Users/mbp/THEOS2/data/ZL3b-n.txt'

# folio_lines[fn] = list of lines; each line is a list of tokens
folio_lines = defaultdict(list)
current_folio = None

with open(corpus_file, 'r', encoding='utf-8') as f:
    for raw_line in f:
        raw_line = raw_line.rstrip('\n')
        m = re.match(r'^(<f\d+[rv]?\d*>)', raw_line)
        if m:
            fn = folio_num_from_tag(m.group(1))
            if fn is not None:
                current_folio = fn
            continue
        if raw_line.startswith('#') or raw_line.startswith('<%'):
            continue
        if current_folio is None:
            continue
        clean = re.sub(r'<[^>]+>', ' ', raw_line)
        toks = tokenise_line(clean)
        if len(toks) >= 2:   # only multi-token lines (position is meaningful)
            folio_lines[current_folio].append(toks)

# Filter to sections
folio_sec = {}
for fn in folio_lines:
    sec = folio_to_section(fn)
    if sec:
        folio_sec[fn] = sec

# Section → list of (token, position) pairs
def build_sec_pos(folio_lines_dict, folio_sec_dict):
    sec_pos = defaultdict(list)   # section → [(token, pos)]
    for fn, lines in folio_lines_dict.items():
        sec = folio_sec_dict.get(fn)
        if not sec:
            continue
        for line in lines:
            n = len(line)
            for i, tok in enumerate(line):
                p = i / (n - 1)
                sec_pos[sec].append((tok, p))
    return sec_pos

sec_pos_obs = build_sec_pos(folio_lines, folio_sec)

total = sum(len(v) for v in sec_pos_obs.values())
print(f"Loaded {total} positioned tokens from {len(folio_sec)} folios")
for s, tp in sorted(sec_pos_obs.items()):
    print(f"  {s:8s}: {len(tp):6d} positioned tokens")

# ── Token testers ───────────────────────────────────────────────────────────────
def is_ot(tok):    return tok.startswith('ot') or tok in ('otcham', 'otaiin', 'otol', 'otchy')
def is_cheol(tok): return tok == 'cheol'

# ── Law 9 statistic ─────────────────────────────────────────────────────────────
def law9_stat(sec_pos):
    """
    Difference: mean ot-class position in TEXT minus mean ot-class position in PHARMA+BIO.
    Positive = ot is later in text than in pharma/bio.
    """
    text_ot = [p for tok, p in sec_pos.get('text', []) if is_ot(tok)]
    bio_ot   = [p for tok, p in sec_pos.get('bio',   []) if is_ot(tok)]
    pha_ot   = [p for tok, p in sec_pos.get('pharma',[]) if is_ot(tok)]
    pharma_bio_ot = bio_ot + pha_ot
    if not text_ot or not pharma_bio_ot:
        return 0.0
    return sum(text_ot)/len(text_ot) - sum(pharma_bio_ot)/len(pharma_bio_ot)

# ── Law 11 statistic ────────────────────────────────────────────────────────────
def law11_stat(sec_pos):
    """
    Proportion of cheol occurrences at position <= 0.20 or >= 0.80 (bimodal extremes).
    Counts across ALL sections (cheol's bimodality is corpus-wide, not section-specific).
    """
    all_cheol_pos = [p for sec in sec_pos for tok, p in sec_pos[sec] if is_cheol(tok)]
    if not all_cheol_pos:
        return 0.0
    extreme = sum(1 for p in all_cheol_pos if p <= 0.20 or p >= 0.80)
    return extreme / len(all_cheol_pos)

# ── Observed ─────────────────────────────────────────────────────────────────────
obs_l9  = law9_stat(sec_pos_obs)
obs_l11 = law11_stat(sec_pos_obs)
print(f"\n=== Observed statistics ===")
print(f"  Law 9  (ot text-late minus pharma/bio-early): {obs_l9:.4f}")
print(f"  Law 11 (cheol extremal proportion ≤.20 or ≥.80): {obs_l11:.4f}")

# ── Permutation: shuffle token positions within each line ─────────────────────
N_PERM = 10000
random.seed(42)
print(f"\nRunning {N_PERM} within-line position shuffles (seed=42)...")

count_l9  = 0
count_l11 = 0

# Pre-build shufflable structure: folio → list of lines (each line = list of tokens)
# After shuffling each line, recompute positions
folios = list(folio_sec.keys())

for perm_idx in range(N_PERM):
    # Shuffle token order within each line of each folio
    shuffled_sec_pos = defaultdict(list)
    for fn in folios:
        sec = folio_sec[fn]
        for line in folio_lines[fn]:
            perm_line = line.copy()
            random.shuffle(perm_line)
            n = len(perm_line)
            for i, tok in enumerate(perm_line):
                p = i / (n - 1)
                shuffled_sec_pos[sec].append((tok, p))

    p_l9  = law9_stat(shuffled_sec_pos)
    p_l11 = law11_stat(shuffled_sec_pos)

    if p_l9  >= obs_l9:  count_l9  += 1
    if p_l11 >= obs_l11: count_l11 += 1

    if (perm_idx + 1) % 1000 == 0:
        print(f"  {perm_idx+1}/{N_PERM} done")

# ── Results ──────────────────────────────────────────────────────────────────────
p_l9_perm  = count_l9  / N_PERM
p_l11_perm = count_l11 / N_PERM

print(f"\n=== Permutation p-values (within-line shuffle, N=10,000, seed=42) ===")
print(f"{'Law':<50s}  {'p_perm':>8s}  {'obs':>8s}  {'verdict':>8s}")
print("-" * 78)
def verdict(p): return "STRONG" if p < 0.001 else ("MODERATE" if p < 0.05 else "n.s.")
print(f"  {'Law 9 (ot text-late diff)':<50s}  {p_l9_perm:>8.4f}  {obs_l9:>8.4f}  {verdict(p_l9_perm):>8s}")
print(f"  {'Law 11 (cheol extremal proportion)':<50s}  {p_l11_perm:>8.4f}  {obs_l11:>8.4f}  {verdict(p_l11_perm):>8s}")

print("""
Notes:
  Law 9:  A positive statistic confirms that ot-class tokens appear later in text
    lines than in pharma/bio lines, consistent with the 'stellar-timing in text =
    explanatory context' interpretation. The within-line shuffle destroys positional
    structure while preserving which tokens appear on each line.
  Law 11: The cheol bimodal statistic measures the fraction of cheol occurrences
    at extreme line positions (first 20% or last 20%). Under random position
    assignment, the expected fraction at these extremes is exactly 0.40 for a
    uniform distribution. The observed fraction > 0.40 confirms bimodal positional
    preference.
  Law 9 is classified MODERATE (p=0.039 by token-level KS test) in Table 3.1.
  Law 11 is classified STRONG (binomial p≈10⁻⁵). Results here should match these
  classifications; if they differ, the more conservative p-value governs.
""")
