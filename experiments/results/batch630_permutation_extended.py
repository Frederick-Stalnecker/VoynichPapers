#!/usr/bin/env python3
"""
Batch 630 — Extended folio-level permutation test for ALL section-distribution
grammar laws: Laws 1, 2, 3, 4, 5, 6, 7, 10.

Laws covered here are those where the section enrichment/depletion is the
testable claim (section-distribution laws). Laws 9, 11 are positional laws
(where within a line a token appears); folio-level shuffling does not disrupt
within-folio positional structure, so those laws require a separate within-folio
position-shuffle test (see batch630b). Law 12 (ee WEAK) is retained as a
descriptive note; Fisher p=0.0008 for CTH-depletion already available.

Method: identical to batch629 — shuffle folio→section assignments, preserve
within-folio token sequences, N=10,000 permutations, seed=42.

Laws:
  Law 1:  daiin line-closer — herbal enrichment (daiin rate herbal vs others)
  Law 2:  -edy bio enrichment (chi2 bio vs others)
  Law 3:  chor bio-zero (count in bio should be 0)
  Law 4:  -eol pharma enrichment (chi2 pharma vs others)
  Law 5:  ok-eo completive astro enrichment (chi2 astro vs others)
  Law 6:  -am text enrichment (chi2 text vs others)
  Law 7:  ch-class herbal enrichment (chi2 herbal vs others)
  Law 10: qol bio-exclusive (rate in bio vs others)
"""

import re
import random
from collections import defaultdict

# ── Section assignments ─────────────────────────────────────────────────────────
SECTION_RANGES = {
    'herbal': list(range(1, 58)),           # f1–f57
    'astro':  list(range(67, 75)),          # f67–f74
    'bio':    list(range(75, 85)),          # f75–f84
    'pharma': list(range(87, 103)),         # f87–f102
    'text':   list(range(103, 117)),        # f103–f116
}

def folio_to_section(folio_num):
    for sec, frange in SECTION_RANGES.items():
        if folio_num in frange:
            return sec
    return None

def folio_num_from_tag(tag):
    m = re.match(r'<f(\d+)', tag)
    if m:
        return int(m.group(1))
    return None

def tokenise(raw):
    tokens = re.split(r'[., ]', raw)
    return [t.strip().lower() for t in tokens
            if t.strip() and re.match(r'^[a-z]+$', t.strip())]

# ── Load corpus ─────────────────────────────────────────────────────────────────
print("Loading corpus...")
corpus_file = '/Users/mbp/THEOS2/data/ZL3b-n.txt'
folio_tokens = defaultdict(list)
current_folio = None

with open(corpus_file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.rstrip('\n')
        m = re.match(r'^(<f\d+[rv]?\d*>)', line)
        if m:
            fn = folio_num_from_tag(m.group(1))
            if fn is not None:
                current_folio = fn
            continue
        if line.startswith('#') or line.startswith('<%'):
            continue
        if current_folio is None:
            continue
        clean = re.sub(r'<[^>]+>', ' ', line)
        tokens = tokenise(clean)
        if tokens:
            folio_tokens[current_folio].extend(tokens)

folio_section = {}
for fn, toks in folio_tokens.items():
    sec = folio_to_section(fn)
    if sec:
        folio_section[fn] = sec

section_tokens_obs = defaultdict(list)
for fn, toks in folio_tokens.items():
    sec = folio_section.get(fn)
    if sec:
        section_tokens_obs[sec].extend(toks)

total_tokens = sum(len(v) for v in section_tokens_obs.values())
print(f"Loaded {total_tokens} tokens across {len(folio_section)} folios in 5 sections")
for sec, toks in sorted(section_tokens_obs.items()):
    print(f"  {sec:8s}: {len(toks):6d} tokens, "
          f"{sum(1 for fn,s in folio_section.items() if s==sec):3d} folios")

# ── Token testers ───────────────────────────────────────────────────────────────
def is_daiin(t):     return t == 'daiin'
def ends_edy(t):     return t.endswith('edy')
def is_chor(t):      return t == 'chor'
def ends_eol(t):     return t.endswith('eol')
def ends_okeo(t):    return t.startswith('ok') and 'eo' in t
def ends_am(t):      return t.endswith('am') and len(t) >= 3
def is_ch_class(t):  return t.startswith('ch')   # ch-class (ch-initial)
def is_qol(t):       return t == 'qol'

# ── Chi-squared helper ──────────────────────────────────────────────────────────
def chi2_2x2(target_sec, tester_fn, sec_toks):
    """Chi-squared: target_sec enrichment vs all others for tester_fn tokens."""
    t_n   = len(sec_toks.get(target_sec, []))
    t_pos = sum(1 for tok in sec_toks.get(target_sec, []) if tester_fn(tok))
    o_n   = sum(len(sec_toks[s]) for s in sec_toks if s != target_sec)
    o_pos = sum(1 for s in sec_toks if s != target_sec
                for tok in sec_toks[s] if tester_fn(tok))
    a, b = t_pos, t_n - t_pos
    c, d = o_pos, o_n - o_pos
    n = a + b + c + d
    if n == 0 or 0 in [a+b, c+d, a+c, b+d]:
        return 0.0
    E_a = (a+b)*(a+c)/n
    E_b = (a+b)*(b+d)/n
    E_c = (c+d)*(a+c)/n
    E_d = (c+d)*(b+d)/n
    return (a-E_a)**2/E_a + (b-E_b)**2/E_b + (c-E_c)**2/E_c + (d-E_d)**2/E_d

def rate_in_section(target_sec, tester_fn, sec_toks):
    """Token rate in target section."""
    toks = sec_toks.get(target_sec, [])
    if not toks:
        return 0.0
    return sum(1 for t in toks if tester_fn(t)) / len(toks)

def count_in_section(target_sec, tester_fn, sec_toks):
    """Raw count in target section."""
    return sum(1 for t in sec_toks.get(target_sec, []) if tester_fn(t))

# ── Observed statistics ─────────────────────────────────────────────────────────
print("\n=== Observed statistics ===")

obs = {
    'L1_daiin_herbal':   chi2_2x2('herbal', is_daiin,    section_tokens_obs),
    'L2_edy_bio':        chi2_2x2('bio',    ends_edy,    section_tokens_obs),
    'L3_chor_bio_count': count_in_section('bio', is_chor, section_tokens_obs),
    'L4_eol_pharma':     chi2_2x2('pharma', ends_eol,   section_tokens_obs),
    'L5_okeo_astro':     chi2_2x2('astro',  ends_okeo,  section_tokens_obs),
    'L6_am_text':        chi2_2x2('text',   ends_am,    section_tokens_obs),
    'L7_ch_herbal':      chi2_2x2('herbal', is_ch_class, section_tokens_obs),
    'L10_qol_bio':       rate_in_section('bio', is_qol, section_tokens_obs),
}

for k, v in obs.items():
    print(f"  {k:<28s}: {v:.4f}")

# ── Permutation test ─────────────────────────────────────────────────────────────
N_PERM = 10000
random.seed(42)

print(f"\nRunning {N_PERM} folio-level permutations (seed=42)...")

folios             = list(folio_section.keys())
folio_sections_lst = [folio_section[fn] for fn in folios]

counts = {k: 0 for k in obs}

for perm_idx in range(N_PERM):
    shuffled = folio_sections_lst.copy()
    random.shuffle(shuffled)

    pst = defaultdict(list)
    for fn, sec in zip(folios, shuffled):
        pst[sec].extend(folio_tokens[fn])

    # Compute permuted statistics
    p_stat = {
        'L1_daiin_herbal':   chi2_2x2('herbal', is_daiin,    pst),
        'L2_edy_bio':        chi2_2x2('bio',    ends_edy,    pst),
        'L3_chor_bio_count': count_in_section('bio', is_chor, pst),
        'L4_eol_pharma':     chi2_2x2('pharma', ends_eol,   pst),
        'L5_okeo_astro':     chi2_2x2('astro',  ends_okeo,  pst),
        'L6_am_text':        chi2_2x2('text',   ends_am,    pst),
        'L7_ch_herbal':      chi2_2x2('herbal', is_ch_class, pst),
        'L10_qol_bio':       rate_in_section('bio', is_qol, pst),
    }

    # Count extremes
    for k in obs:
        if k == 'L3_chor_bio_count':
            # Law 3: zero is the observed; count permutations where bio_chor <= 0
            if p_stat[k] <= obs[k]:
                counts[k] += 1
        else:
            # All other laws: enrichment; count permutations >= observed
            if p_stat[k] >= obs[k]:
                counts[k] += 1

    if (perm_idx + 1) % 1000 == 0:
        print(f"  {perm_idx+1}/{N_PERM} done")

# ── Results ──────────────────────────────────────────────────────────────────────
print("\n=== Permutation p-values (folio-level, N=10,000, seed=42) ===")
print(f"{'Law':<30s}  {'p_perm':>8s}  {'obs_stat':>12s}  {'verdict':>8s}")
print("-" * 68)

results = {}
for k in obs:
    p = counts[k] / N_PERM
    results[k] = p
    obs_v = obs[k]
    verdict = "STRONG" if p < 0.001 else ("MODERATE" if p < 0.05 else "n.s.")
    print(f"  {k:<30s}  {p:>8.4f}  {obs_v:>12.2f}  {verdict:>8s}")

print()
all_pass = all(results[k] < 0.001 for k in results if k != 'L3_chor_bio_count')
chor_pass = results['L3_chor_bio_count'] < 0.001
print(f"All section-distribution laws p < 0.001:  {all_pass and chor_pass}")

print("""
Notes:
  Law 3 (L3_chor_bio_count): permutation p = fraction where shuffled bio_chor <= 0
    (i.e., random section assignment also produces a bio chor-count of zero).
    If p is small, the observed zero is NOT what you would expect by chance.

  Laws NOT included in this folio-permutation framework:
    Law 8 (-edy/-eol/-eo/-eey paradigm) — captures the same variance as Laws 2,4,5
    Law 9 (ot positional early/late) — positional within lines; folio shuffle
      does not disrupt within-folio line ordering. Separate analysis required.
    Law 11 (cheol dual positional) — same reason as Law 9.
    Law 12 (ee WEAK) — Fisher CTH-depletion p=0.0008 already available; positional
      test p=0.584 (not significant, WEAK classification retained).
""")
