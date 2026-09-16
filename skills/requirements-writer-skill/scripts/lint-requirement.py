#!/usr/bin/env python3
"""Linter for REQ-NNN.md files produced by requirements-writer-skill.

Exit 0 = compliant. Exit 1 = violations printed to stderr.

Usage: python scripts/lint-requirement.py <path-to-REQ-NNN.md>

Hard Check 0 enforces:
  - Exactly ONE SHALL (case-sensitive) in the `## Rule` section.
  - `project_slug` and `language` present in front-matter.
  - All [bracketed] terms in the rule exist in /req/GLOSSARY.md.
  - score in [50, 100].
"""
import re
import sys
from pathlib import Path

SHALL_RE = re.compile(r"\bSHALL\b")
TERM_LINK_RE = re.compile(r"\[([^\]]+)\]")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
RULE_SECTION_RE = re.compile(
    r"^## Rule\s*\n(.+?)(?=\n## |\Z)", re.DOTALL | re.MULTILINE
)


def lint(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    fm_match = FRONTMATTER_RE.search(text)
    if not fm_match:
        errors.append("Missing front-matter (--- block).")
        return errors
    fm = fm_match.group(1)
    for key in ("project_slug", "language"):
        if not re.search(rf"^{key}:\s*\S+", fm, re.MULTILINE):
            errors.append(f"Front-matter missing `{key}`.")

    rule_match = RULE_SECTION_RE.search(text)
    if not rule_match:
        errors.append("Missing `## Rule` section.")
        return errors
    rule_body = rule_match.group(1).strip()
    shall_count = len(SHALL_RE.findall(rule_body))
    if shall_count != 1:
        errors.append(
            f"Rule section contains {shall_count} SHALL(s); "
            "exactly 1 required (R18)."
        )

    score_match = re.search(r"^\s*score:\s*(\d+)", fm, re.MULTILINE)
    if score_match:
        score = int(score_match.group(1))
        if not (50 <= score <= 100):
            errors.append(f"score={score} out of range [50,100].")

    terms_in_rule = set(TERM_LINK_RE.findall(rule_body))
    glossary_path = path.parent.parent.parent / "GLOSSARY.md"
    if glossary_path.exists():
        glossary_terms = set(
            TERM_LINK_RE.findall(glossary_path.read_text(encoding="utf-8"))
        )
        missing = terms_in_rule - glossary_terms
        if missing:
            errors.append(
                f"Rule references undefined glossary terms: {sorted(missing)}"
            )

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: lint-requirement.py <REQ-NNN.md>", file=sys.stderr)
        return 1
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Not found: {path}", file=sys.stderr)
        return 1
    errors = lint(path)
    if errors:
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print(f"\nFAILED: {len(errors)} violation(s).", file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())