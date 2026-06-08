#!/usr/bin/env python3
"""
Batch 629 — Folio-level permutation test for Grammar Laws 2, 3, 4, 5, 6, 10
Addresses the non-independence caveat in §2.4.

For each grammar law, we:
1. Compute the observed test statistic using the canonical section assignments
2. Run 10,000 permutations: randomly reassign FOLIOS to sections,
   keeping each folio's token sequence intact (preserves within-folio correlation)
3. Compute the permutation p-value = fraction of permutations >= observed statistic

Folio-level permutation: folios are the unit of randomisation, not tokens.
This makes the test explicitly conservative w.r.t. within-folio token correlation.
"""

import re
import random
import math
from collections import defaultdict

# ── Section assignments (folio ranges) ─────────────────────────────────────────
SECTION_RANGES = {
    'herbal': list(range(1, 58)),           # f1–f57
    'astro':  list(range(67, 75)),           # f67–f74
    'bio':    list(range(75, 85)),           # f75–f84
    'pharma': list(range(87, 103)),          # f87–f102
    'text':   list(range(103, 117)),         # f103–f116
}

def folio_to_section(folio_num):
    for sec, frange in SECTION_RANGES.items():
        if folio_num in frange:
            return sec
    return None

def folio_num_from_tag(tag):
    """Extract integer folio number from tag like <f1r>, <f103v>, <f69v1>"""
    m = re.match(r'<f(\d+)', tag)
    if m:
        return int(m.group(1))
    return None

def tokenise(raw):
    """Canonical tokeniser: split on ., space, comma; keep alphabetic tokens."""
    tokens = re.split(r'[., ]', raw)
    return [t.strip().lower() for t in tokens
            if t.strip() and re.match(r'^[a-z]+$', t.strip())]

# ── Load corpus ─────────────────────────────────────────────────────────────────
print("Loading corpus...")
corpus_file = '/Users/mbp/THEOS2/data/ZL3b-n.txt'
folio_tokens = defaultdict(list)   # folio_num -> [tokens]
current_folio = None

with open(corpus_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\n')
        # Folio tag
        m = re.match(r'^(<f\d+[rv]?\d*>)', line)
        if m:
            fn = folio_num_from_tag(m.group(1))
            if fn is not None:
                current_folio = fn
            continue
        # Skip comments and metadata
        if line.startswith('#') or line.startswith('<%'):
            continue
        if current_folio is None:
            continue
        # Strip inline annotations <...>
        clean = re.sub(r'<[^>]+>', ' ', line)
        tokens = tokenise(clean)
        if tokens:
            folio_tokens[current_folio].extend(tokens)

# Assign each folio to its section
folio_section = {}
for fn, toks in folio_tokens.items():
    sec = folio_to_section(fn)
    if sec:
        folio_section[fn] = sec

# Build per-section token lists (observed)
section_tokens_obs = defaultdict(list)
for fn, toks in folio_tokens.items():
    sec = folio_section.get(fn)
    if sec:
        section_tokens_obs[sec].extend(toks)

total_tokens = sum(len(v) for v in section_tokens_obs.values())
print(f"Loaded {total_tokens} tokens across {len(folio_section)} folios in 5 sections")
for sec, toks in section_tokens_obs.items():
    print(f"  {sec:8s}: {len(toks):6d} tokens, "
          f"{sum(1 for fn,s in folio_section.items() if s==sec)} folios")

# ── Token testers ────────────────────────────────────────────────────────────────
def ends_edy(t):  return t.endswith('edy')
def is_chor(t):   return t == 'chor'
def ends_eol(t):  return t.endswith('eol')
def ends_eok(t):  return t.startswith('ok') and 'eo' in t  # ok-eo completive
def ends_am(t):   return t.endswith('am')
def is_qol(t):    return t == 'qol'

# ── Observed statistics ──────────────────────────────────────────────────────────
print("\n=== Observed statistics ===")

def edy_chi2(sec_toks):
    """Law 2: -edy enrichment in bio. Chi-squared bio vs all other."""
    bio_n = len(sec_toks.get('bio', []))
    bio_edy = sum(1 for t in sec_toks.get('bio', []) if ends_edy(t))
    other_n = sum(len(sec_toks[s]) for s in sec_toks if s != 'bio')
    other_edy = sum(1 for s in sec_toks if s != 'bio'
                    for t in sec_toks[s] if ends_edy(t))
    # 2x2 chi-squared
    a, b = bio_edy, bio_n - bio_edy
    c, d = other_edy, other_n - other_edy
    n = a + b + c + d
    if 0 in [a+b, c+d, a+c, b+d]:
        return 0
    E_a = (a+b)*(a+c)/n
    E_b = (a+b)*(b+d)/n
    E_c = (c+d)*(a+c)/n
    E_d = (c+d)*(b+d)/n
    chi2 = (a-E_a)**2/E_a + (b-E_b)**2/E_b + (c-E_c)**2/E_c + (d-E_d)**2/E_d
    return chi2

def chor_bio_zero(sec_toks):
    """Law 3: chor count in bio. Observed should be 0; statistic = count (lower is more 'null-like')."""
    # We test: given we expect ~100 (herbal rate * bio size), how unusual is 0?
    herbal_rate = sum(1 for t in sec_toks.get('herbal', []) if is_chor(t)) / max(1, len(sec_toks.get('herbal', [])))
    bio_expected = herbal_rate * len(sec_toks.get('bio', []))
    bio_observed = sum(1 for t in sec_toks.get('bio', []) if is_chor(t))
    # Statistic: bio_observed - bio_expected (more negative = more extreme)
    # For permutation: we use the observed count in bio (want to show 0 is extreme)
    return bio_observed  # permutation p = fraction of perms where bio_chor <= observed

def eol_chi2(sec_toks):
    """Law 4: -eol enrichment in pharma."""
    ph_n = len(sec_toks.get('pharma', []))
    ph_eol = sum(1 for t in sec_toks.get('pharma', []) if ends_eol(t))
    ot_n = sum(len(sec_toks[s]) for s in sec_toks if s != 'pharma')
    ot_eol = sum(1 for s in sec_toks if s != 'pharma'
                 for t in sec_toks[s] if ends_eol(t))
    a, b = ph_eol, ph_n - ph_eol
    c, d = ot_eol, ot_n - ot_eol
    n = a + b + c + d
    if 0 in [a+b, c+d, a+c, b+d]:
        return 0
    E_a = (a+b)*(a+c)/n
    E_b = (a+b)*(b+d)/n
    E_c = (c+d)*(a+c)/n
    E_d = (c+d)*(b+d)/n
    chi2 = (a-E_a)**2/E_a + (b-E_b)**2/E_b + (c-E_c)**2/E_c + (d-E_d)**2/E_d
    return chi2

def okeo_chi2(sec_toks):
    """Law 5: ok-eo completive in astro."""
    ast_n = len(sec_toks.get('astro', []))
    ast_okeo = sum(1 for t in sec_toks.get('astro', []) if ends_eok(t))
    ot_n = sum(len(sec_toks[s]) for s in sec_toks if s != 'astro')
    ot_okeo = sum(1 for s in sec_toks if s != 'astro'
                  for t in sec_toks[s] if ends_eok(t))
    a, b = ast_okeo, ast_n - ast_okeo
    c, d = ot_okeo, ot_n - ot_okeo
    n = a + b + c + d
    if 0 in [a+b, c+d, a+c, b+d]:
        return 0
    E_a = (a+b)*(a+c)/n
    E_b = (a+b)*(b+d)/n
    E_c = (c+d)*(a+c)/n
    E_d = (c+d)*(b+d)/n
    chi2 = (a-E_a)**2/E_a + (b-E_b)**2/E_b + (c-E_c)**2/E_c + (d-E_d)**2/E_d
    return chi2

def qol_fisher_stat(sec_toks):
    """Law 10: qol enrichment in bio. Return bio qol count / bio total (rate)."""
    bio_n = len(sec_toks.get('bio', []))
    bio_qol = sum(1 for t in sec_toks.get('bio', []) if is_qol(t))
    if bio_n == 0:
        return 0
    return bio_qol / bio_n  # rate; permutation p = fraction exceeding observed rate

# Compute observed
obs_edy = edy_chi2(section_tokens_obs)
obs_chor = chor_bio_zero(section_tokens_obs)
obs_eol = eol_chi2(section_tokens_obs)
obs_okeo = okeo_chi2(section_tokens_obs)
obs_qol = qol_fisher_stat(section_tokens_obs)

print(f"Law 2 (-edy bio chi2):     {obs_edy:.1f}")
print(f"Law 3 (chor bio count):    {obs_chor} (observed; permutation tests if this is low)")
print(f"Law 4 (-eol pharma chi2):  {obs_eol:.1f}")
print(f"Law 5 (ok-eo astro chi2):  {obs_okeo:.1f}")
print(f"Law 10 (qol bio rate):     {obs_qol:.5f}")

# ── Permutation test ──────────────────────────────────────────────────────────────
N_PERM = 10000
random.seed(42)

print(f"\nRunning {N_PERM} folio-level permutations...")

# Get the list of (folio, section) pairs and list of folio token lists
folios = list(folio_section.keys())
folio_sections_list = [folio_section[fn] for fn in folios]

# Section folio counts
sec_counts = defaultdict(int)
for s in folio_sections_list:
    sec_counts[s] += 1

count_edy_exceeds  = 0
count_chor_lte     = 0   # chor: count permutations where bio_chor <= observed
count_eol_exceeds  = 0
count_okeo_exceeds = 0
count_qol_exceeds  = 0

for perm_idx in range(N_PERM):
    # Shuffle section assignments at the folio level
    # Keep section sizes EXACTLY the same (stratified shuffle)
    shuffled_sections = folio_sections_list.copy()
    random.shuffle(shuffled_sections)

    # Build permuted section token lists
    perm_sec_toks = defaultdict(list)
    for fn, sec in zip(folios, shuffled_sections):
        perm_sec_toks[sec].extend(folio_tokens[fn])

    # Compute statistics
    p_edy  = edy_chi2(perm_sec_toks)
    p_chor = chor_bio_zero(perm_sec_toks)
    p_eol  = eol_chi2(perm_sec_toks)
    p_okeo = okeo_chi2(perm_sec_toks)
    p_qol  = qol_fisher_stat(perm_sec_toks)

    if p_edy  >= obs_edy:   count_edy_exceeds  += 1
    if p_chor <= obs_chor:  count_chor_lte     += 1
    if p_eol  >= obs_eol:   count_eol_exceeds  += 1
    if p_okeo >= obs_okeo:  count_okeo_exceeds += 1
    if p_qol  >= obs_qol:   count_qol_exceeds  += 1

    if (perm_idx + 1) % 1000 == 0:
        print(f"  {perm_idx+1}/{N_PERM} done")

print("\n=== Permutation p-values (folio-level, N=10,000) ===")
p_edy_perm  = count_edy_exceeds  / N_PERM
p_chor_perm = count_chor_lte     / N_PERM
p_eol_perm  = count_eol_exceeds  / N_PERM
p_okeo_perm = count_okeo_exceeds / N_PERM
p_qol_perm  = count_qol_exceeds  / N_PERM

print(f"Law 2 (-edy bio enrichment):  p_perm = {p_edy_perm:.4f}  [obs chi2={obs_edy:.1f}]")
print(f"Law 3 (chor bio-zero):        p_perm = {p_chor_perm:.4f}  [obs chor_bio={obs_chor}]")
print(f"Law 4 (-eol pharma):          p_perm = {p_eol_perm:.4f}  [obs chi2={obs_eol:.1f}]")
print(f"Law 5 (ok-eo astro):          p_perm = {p_okeo_perm:.4f}  [obs chi2={obs_okeo:.1f}]")
print(f"Law 10 (qol bio rate):        p_perm = {p_qol_perm:.4f}  [obs rate={obs_qol:.5f}]")
print()
print("All p_perm < 0.001 → STRONG under folio-level permutation? ",
      all(p < 0.001 for p in [p_edy_perm, p_chor_perm, p_eol_perm, p_okeo_perm, p_qol_perm]))
