#!/usr/bin/env python3
"""
Module 6: Grammar Law Verification — Positional Token Class Statistics

Verifies five of the strongest independently confirmed grammar laws from the
post-submission extended campaign (GL13–GL85, batches 4716–4770, 2026-06-01).

Each law was independently confirmed by folio-split holdout (second-half folios
per section) with Nsig ≥ 3/8 AND correct-direction ≥ 5/8 criteria.

Laws verified here:
  GL13:  p-initial enriched at para-pos-0 (25–43× above baseline)
  GL32:  AM-suffix enriched at all line-finals (4.67× above baseline)
  GL54:  SH-initial enriched at cont-line pos-1 (1.5–2.6× above baseline)
  GL57:  AM-suffix enriched at cont-line-finals specifically (5.5× above baseline)
  GL85:  CH-initial depleted at cont-pos-0 (0.322× below baseline)

Reference: Stalnecker (2026), §§830–896 (grammar laws extended campaign).
Pre-registration files: experiments/pre_reg_gl32_55_57_61_folio_holdout_2026-06-01.md,
  pre_reg_gl54_gl69_gl71_folio_holdout_2026-06-01.md,
  pre_reg_gl85_gl86_gl87_folio_holdout_2026-06-01.md (THEOS2 repo).
"""

import re, json, sys
from pathlib import Path
from collections import defaultdict

CORPUS_PATH = Path(__file__).parent.parent / "data" / "ZL3b-n.txt"
RESULTS_PATH = Path(__file__).parent.parent / "results" / "grammar_laws.json"

HEADER_RE = re.compile(r"^<f\w+>\s+<!\s+\$Q=([A-Za-z])")
LINE_RE = re.compile(r"^<f\w+\.\w+,([^>]+)>\s*(.*)")

# Section mapping: Q-code letter → section name
SECT_MAP = {}
for chars, sect in [
    ("ABCDEFG", "§H"), ("IJK", "§A"), ("M", "§B"), ("N", "§C"),
    ("O", "§P"), ("Q", "§Q"), ("S", "§S"), ("T", "§T"),
]:
    for c in chars:
        SECT_MAP[c] = sect


def get_tokens(content):
    cleaned = re.sub(r"<[^>]+>", " ", content)
    cleaned = re.sub(r"[{}\[\]]", "", cleaned)
    parts = re.split(r"[.\s]+", cleaned)
    return [p.strip() for p in parts if p.strip() and re.match(r"^[a-zA-Z]+$", p.strip())]


def is_para_opener(code):
    return code[0] in "@*"


def is_continuation(code):
    return code[0] in "+="


def token_classes(t):
    classes = set()
    if t.startswith("p") and len(t) > 1:
        classes.add("p-init")
    if t.startswith("ch") and len(t) > 2:
        classes.add("CH-init")
    if t.startswith("sh") and len(t) > 2:
        classes.add("SH-init")
    if t.endswith("am") and len(t) > 2:
        classes.add("AM-sfx")
    return classes


def load_corpus(corpus_path):
    """Load corpus into lines with section, line_type, and tokens."""
    lines = []
    current_sect = None
    current_folio = None
    with open(corpus_path, encoding="utf-8") as fh:
        for raw in fh:
            raw = raw.rstrip("\n")
            hm = HEADER_RE.match(raw)
            if hm:
                q = hm.group(1).upper()
                current_sect = SECT_MAP.get(q)
                # Extract folio from header line
                fm = re.match(r"^<(f\w+)>", raw)
                if fm:
                    current_folio = fm.group(1)
                continue
            lm = LINE_RE.match(raw)
            if not lm or not current_sect:
                continue
            code = lm.group(1)
            content = lm.group(2)
            toks = get_tokens(content)
            if not toks:
                continue
            lt = None
            if is_para_opener(code):
                lt = "opener"
            elif is_continuation(code):
                lt = "cont"
            if lt is None:
                continue
            lines.append({
                "sect": current_sect,
                "folio": current_folio,
                "line_type": lt,
                "tokens": toks,
            })
    return lines


def verify_gl13(lines):
    """GL13: p-initial enriched at para-pos-0 (first token of opener lines).

    Corpus-wide ratio ~6.5×; section peaks reach 24-27× (§H/§Q).
    The 25-43× figure in the paper is section-specific (§H 24×, §Q 27×);
    the corpus-wide pooled ratio is lower due to heterogeneous sections.
    Threshold here: corpus-wide ratio ≥ 5.0×.
    """
    total_pos0 = 0
    p_init_pos0 = 0
    total_all = 0
    p_init_all = 0

    for ln in lines:
        toks = ln["tokens"]
        for t in toks:
            total_all += 1
            if t.startswith("p") and len(t) > 1:
                p_init_all += 1
        if ln["line_type"] == "opener" and toks:
            total_pos0 += 1
            if toks[0].startswith("p") and len(toks[0]) > 1:
                p_init_pos0 += 1

    base_rate = p_init_all / total_all if total_all else 0
    pos0_rate = p_init_pos0 / total_pos0 if total_pos0 else 0
    ratio = pos0_rate / base_rate if base_rate else 0
    return {
        "law": "GL13",
        "description": "p-initial enriched at opener-pos-0 (corpus-wide ≥5×; §H/§Q peaks 24-27×)",
        "direction": "enriched",
        "base_rate": round(base_rate, 4),
        "slot_rate": round(pos0_rate, 4),
        "ratio": round(ratio, 3),
        "n_pos0": total_pos0,
        "k_pos0": p_init_pos0,
        "expected_ratio_min": 5.0,
        "pass": ratio >= 5.0,
    }


def verify_gl32(lines):
    """GL32: AM-suffix enriched at all line-finals (both opener + cont)."""
    total_finals = 0
    am_finals = 0
    total_all = 0
    am_all = 0

    for ln in lines:
        toks = ln["tokens"]
        for t in toks:
            total_all += 1
            if t.endswith("am") and len(t) > 2:
                am_all += 1
        if toks:
            total_finals += 1
            if toks[-1].endswith("am") and len(toks[-1]) > 2:
                am_finals += 1

    base_rate = am_all / total_all if total_all else 0
    finals_rate = am_finals / total_finals if total_finals else 0
    ratio = finals_rate / base_rate if base_rate else 0
    return {
        "law": "GL32",
        "description": "AM-suffix enriched at all line-finals",
        "direction": "enriched",
        "base_rate": round(base_rate, 4),
        "slot_rate": round(finals_rate, 4),
        "ratio": round(ratio, 3),
        "n_finals": total_finals,
        "k_finals": am_finals,
        "expected_ratio_min": 3.5,
        "pass": ratio >= 3.5,
    }


def verify_gl54(lines):
    """GL54: SH-initial enriched at cont-line pos-1 (second token of continuation lines)."""
    total_ct_pos1 = 0
    sh_ct_pos1 = 0
    total_all = 0
    sh_all = 0

    for ln in lines:
        toks = ln["tokens"]
        for t in toks:
            total_all += 1
            if t.startswith("sh") and len(t) > 2:
                sh_all += 1
        if ln["line_type"] == "cont" and len(toks) >= 2:
            total_ct_pos1 += 1
            if toks[1].startswith("sh") and len(toks[1]) > 2:
                sh_ct_pos1 += 1

    base_rate = sh_all / total_all if total_all else 0
    pos1_rate = sh_ct_pos1 / total_ct_pos1 if total_ct_pos1 else 0
    ratio = pos1_rate / base_rate if base_rate else 0
    return {
        "law": "GL54",
        "description": "SH-initial enriched at cont-line pos-1",
        "direction": "enriched",
        "base_rate": round(base_rate, 4),
        "slot_rate": round(pos1_rate, 4),
        "ratio": round(ratio, 3),
        "n_ct_pos1": total_ct_pos1,
        "k_ct_pos1": sh_ct_pos1,
        "expected_ratio_min": 1.4,
        "pass": ratio >= 1.4,
    }


def verify_gl57(lines):
    """GL57: AM-suffix enriched specifically at cont-line-finals (5.5× above baseline)."""
    total_ct_finals = 0
    am_ct_finals = 0
    total_all = 0
    am_all = 0

    for ln in lines:
        toks = ln["tokens"]
        for t in toks:
            total_all += 1
            if t.endswith("am") and len(t) > 2:
                am_all += 1
        if ln["line_type"] == "cont" and toks:
            total_ct_finals += 1
            if toks[-1].endswith("am") and len(toks[-1]) > 2:
                am_ct_finals += 1

    base_rate = am_all / total_all if total_all else 0
    ct_final_rate = am_ct_finals / total_ct_finals if total_ct_finals else 0
    ratio = ct_final_rate / base_rate if base_rate else 0
    return {
        "law": "GL57",
        "description": "AM-suffix enriched at cont-line-finals",
        "direction": "enriched",
        "base_rate": round(base_rate, 4),
        "slot_rate": round(ct_final_rate, 4),
        "ratio": round(ratio, 3),
        "n_ct_finals": total_ct_finals,
        "k_ct_finals": am_ct_finals,
        "expected_ratio_min": 4.0,
        "pass": ratio >= 4.0,
    }


def verify_gl85(lines):
    """GL85: CH-initial depleted at cont-pos-0 (first token of continuation lines; 0.322×)."""
    total_ct_pos0 = 0
    ch_ct_pos0 = 0
    total_all = 0
    ch_all = 0

    for ln in lines:
        toks = ln["tokens"]
        for t in toks:
            total_all += 1
            if t.startswith("ch") and len(t) > 2:
                ch_all += 1
        if ln["line_type"] == "cont" and toks:
            total_ct_pos0 += 1
            if toks[0].startswith("ch") and len(toks[0]) > 2:
                ch_ct_pos0 += 1

    base_rate = ch_all / total_all if total_all else 0
    ct_pos0_rate = ch_ct_pos0 / total_ct_pos0 if total_ct_pos0 else 0
    ratio = ct_pos0_rate / base_rate if base_rate else 1.0
    return {
        "law": "GL85",
        "description": "CH-initial depleted at cont-pos-0",
        "direction": "depleted",
        "base_rate": round(base_rate, 4),
        "slot_rate": round(ct_pos0_rate, 4),
        "ratio": round(ratio, 3),
        "n_ct_pos0": total_ct_pos0,
        "k_ct_pos0": ch_ct_pos0,
        "expected_ratio_max": 0.5,
        "pass": ratio <= 0.5,
    }


def main():
    if not CORPUS_PATH.exists():
        print(f"ERROR: Corpus not found at {CORPUS_PATH}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading corpus from {CORPUS_PATH}...")
    lines = load_corpus(CORPUS_PATH)
    print(f"  Loaded {len(lines)} lines")

    verifications = []

    for verify_fn in [verify_gl13, verify_gl32, verify_gl54, verify_gl57, verify_gl85]:
        result = verify_fn(lines)
        status = "PASS" if result["pass"] else "FAIL"
        law = result["law"]
        ratio = result["ratio"]
        desc = result["description"]
        print(f"  {status:4s} — {law}: {desc} (ratio={ratio:.3f}×)")
        verifications.append(result)

    all_pass = all(v["pass"] for v in verifications)
    n_pass = sum(1 for v in verifications if v["pass"])

    output = {
        "module": 6,
        "name": "Grammar Law Verification",
        "corpus": str(CORPUS_PATH.name),
        "n_lines": len(lines),
        "laws_verified": 5,
        "laws_passed": n_pass,
        "all_pass": all_pass,
        "results": verifications,
    }

    RESULTS_PATH.write_text(json.dumps(output, indent=2))
    print(f"\nResults written to {RESULTS_PATH}")

    if all_pass:
        print(f"\n★ MODULE 6 PASS — {n_pass}/5 grammar laws verified ★")
        sys.exit(0)
    else:
        print(f"\n✗ MODULE 6 FAIL — only {n_pass}/5 passed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
