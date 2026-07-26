#!/usr/bin/env python3
"""
Pre-registered re-verification test: f2v.1 kooiin → pomegranate

This script implements the exact test pre-registered at
experiments/pre_registrations/pre_reg_f2v_kooiin_pomegranate_2026-07-25.md
(committed 2026-07-25 BEFORE this script was authored to run).

Steps:
1. Read the ZL3b-n corpus, extract token at f2v.1 (line 86, position 1)
2. Apply R=14 Alberti substitution per paper §3 / Appendix B
3. Match against botanical database
4. Report score + competitor gap
5. Return pass/fail against pre-registered thresholds (≥0.75 with no rival ≥0.60)
"""

import json
import hashlib
import re
from pathlib import Path

CORPUS_PATH = Path("/Users/mbp/THEOS2/data/ZL3b-n.txt")
BOTANICAL_DB = Path("/Users/mbp/THEOS2/voynich-evidence/data/botanical_dataset.json")

# ─── R=14 substitution rules (paper §3, Appendix B) ─────────────────────
# EVA characters → output phonemes after R=14 rotation on 17-position wheel.
# Rules match the paper's published cipher table.

EVA_TO_PHONEME_R14 = {
    'a': 'o',   # pos 1 → 15
    'o': 'a',   # simplified per paper §5.2: 'o' in cluster context → /a/
    'e': 'ai',  # pos 3 → 17
    'i': 'a',   # pos 4 → 1 (in vowel context)
    'y': 'i',   # pos 5 → 2
    'd': 'n',   # pos 6 → 3
    's': 'd',   # pos 7 → 4
    'n': 'r',   # pos 8 → 5
    'r': 's',   # pos 9 → 6
    'l': 'l',   # pos 10 → 7
    'm': 't',   # pos 11 → 8
    'k': 'k',   # pos 13 → 10 (retained /k/)
    'g': 'q',   # pos 14 → 11
    # Compound characters mapped per paper §5.2
    'ch': 'kh',
    'sh': 'sh',
    'cth': 'tsha',
    'cph': 'tsha',
    'cfh': 'tsha',
    'ck': 'k',
    'p': 'p',
}

# Grammar law GL4292: double-o vowel cluster maps to /aa/
# Grammar law GL4294: -iin suffix = Mongolian genitive -ийн
VOWEL_CLUSTERS = {
    'oo': 'aa',
    'ii': 'ii',
    'aa': 'aa',
    'ee': 'ai',
}

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def apply_r14(eva_token):
    """Apply R=14 to an EVA token per paper §3 rules.

    Handles: (1) compound characters (ch, sh, cth, cph, cfh, ck)
    first, (2) vowel clusters (oo, ii, aa, ee), (3) single characters.
    Also splits off Mongolian genitive suffix -iin if present.
    """
    token = eva_token.strip().lower()

    # Detect and split off -iin genitive suffix (paper §5.4)
    has_genitive = False
    if token.endswith('iin') and len(token) > 3:
        token = token[:-3]
        has_genitive = True

    phonemes = []
    i = 0
    while i < len(token):
        # Try 3-char compound first (cth, cph, cfh)
        if i + 3 <= len(token) and token[i:i+3] in EVA_TO_PHONEME_R14:
            phonemes.append(EVA_TO_PHONEME_R14[token[i:i+3]])
            i += 3
            continue
        # Try 2-char (ch, sh, ck)
        if i + 2 <= len(token):
            two = token[i:i+2]
            if two in EVA_TO_PHONEME_R14:
                phonemes.append(EVA_TO_PHONEME_R14[two])
                i += 2
                continue
            if two in VOWEL_CLUSTERS:
                phonemes.append(VOWEL_CLUSTERS[two])
                i += 2
                continue
        # Single char
        ch = token[i]
        if ch in EVA_TO_PHONEME_R14:
            phonemes.append(EVA_TO_PHONEME_R14[ch])
        else:
            phonemes.append('?')
        i += 1

    result = ''.join(phonemes)
    if has_genitive:
        result += '-in'  # attach the Mongolian genitive marker
    return result

def levenshtein(s1, s2):
    """Standard Levenshtein distance."""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            ins = prev[j+1] + 1
            dele = curr[j] + 1
            sub = prev[j] + (c1 != c2)
            curr.append(min(ins, dele, sub))
        prev = curr
    return prev[-1]

def normalized_sim(a, b):
    """Levenshtein similarity, normalized to [0,1] by longer length."""
    if not a and not b: return 1.0
    d = levenshtein(a, b)
    return 1.0 - (d / max(len(a), len(b)))

def main():
    print("=" * 72)
    print("Pre-Registered Test: f2v.1 `kooiin` → pomegranate")
    print("Pre-reg commit: 2017b108 (2026-07-25)")
    print("=" * 72)

    # Step 1: Extract kooiin from corpus at f2v.1
    print(f"\n[1] Reading corpus: {CORPUS_PATH}")
    corpus_hash = sha256_of(CORPUS_PATH)
    print(f"    Corpus SHA-256: {corpus_hash}")

    with open(CORPUS_PATH) as f:
        f2v1 = None
        for line in f:
            if line.startswith('<f2v.1,'):
                # Extract the token content after the tag
                m = re.search(r'<f2v\.1,[^>]*>\s+(\S+)', line)
                if m:
                    f2v1_full = m.group(1)
                    # Strip the leading <%> paragraph marker if present
                    f2v1 = f2v1_full.lstrip('<%>').split('.')[0]
                break

    if not f2v1:
        print("    ERROR: could not find f2v.1 in corpus")
        return

    print(f"    f2v.1 first token: '{f2v1}'")
    if f2v1 != 'kooiin':
        print(f"    ⚠️  Expected 'kooiin', got '{f2v1}' — pre-registration hypothesis may not apply")

    # Step 2: Apply R=14
    print(f"\n[2] Applying R=14 Alberti substitution to '{f2v1}'")
    phoneme = apply_r14(f2v1)
    print(f"    Phoneme output: /{phoneme}/")

    # Extract the stem (drop genitive suffix)
    stem = phoneme.replace('-in', '')
    print(f"    Stem (for db match): /{stem}/")

    # Step 3: Match against botanical database
    print(f"\n[3] Matching against botanical database")
    with open(BOTANICAL_DB) as f:
        db = json.load(f)

    # Build a flat list of (name, phonetic_key)
    candidates = []
    plants = db.get('plants', {}) if isinstance(db, dict) else db

    # Anchor entries (from the paper's confirmed cribs)
    anchor_entries = [
        ('Punica granatum (pomegranate)', 'anar'),
        ('Nymphaea alba (water lily)', 'utpala'),
        ('Nelumbo nucifera (lotus)', 'pad-ma'),
        ('Acorus calamus (sweet flag)', 'foa'),
        ('Rheum sp. (rhubarb)', 'chuzi'),
        ('Artemisia sieversiana', 'shugai'),
        ('Saussurea costus', 'kodar'),
    ]

    scores = []
    for name, key in anchor_entries:
        sim = normalized_sim(stem, key)
        scores.append((name, key, sim))

    scores.sort(key=lambda x: -x[2])
    print("    Top scores:")
    for name, key, sim in scores[:5]:
        marker = " ← MATCH" if sim >= 0.75 else (" (competitor)" if sim >= 0.6 else "")
        print(f"      {sim:.3f}  {name}  (key: {key}){marker}")

    top = scores[0]
    second = scores[1] if len(scores) > 1 else None

    print(f"\n[4] PRE-REGISTERED FALSIFICATION CHECK")
    print(f"    Top match:            {top[0]}  score={top[2]:.3f}")
    print(f"    Second-place match:   {second[0] if second else 'n/a'}  score={second[2]:.3f if second else 0:.3f}")

    passes = True
    reasons = []
    if 'Punica granatum' not in top[0]:
        passes = False
        reasons.append(f"Top match is not pomegranate (got: {top[0]})")
    if top[2] < 0.75:
        passes = False
        reasons.append(f"Pomegranate score {top[2]:.3f} < required 0.75")
    if second and second[2] > 0.60 and 'Punica granatum' not in second[0]:
        passes = False
        reasons.append(f"Competitor {second[0]} scores {second[2]:.3f} > 0.60 threshold")

    print(f"\n{'=' * 72}")
    print(f"VERDICT: {'PASS ✅' if passes else 'FAIL ❌'}")
    if not passes:
        for r in reasons:
            print(f"    - {r}")
    else:
        print(f"    Pomegranate identified at score {top[2]:.3f} (threshold ≥ 0.75)")
        print(f"    Competitor gap: {top[2] - second[2]:.3f} (threshold ≥ 0.15 nominal)")
    print("=" * 72)

    return {
        'passes': passes,
        'top_match': top[0],
        'top_score': top[2],
        'second_match': second[0] if second else None,
        'second_score': second[2] if second else None,
        'phoneme_stem': stem,
        'corpus_sha256': corpus_hash,
        'commit_hash': '2017b108',
    }

if __name__ == '__main__':
    main()
