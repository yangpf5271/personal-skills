#!/usr/bin/env python3
"""Static verifier for web-page-engineer deliverables.

Scans an artifact folder for patterns that break the skill's hard rules.
Every check corresponds to a rule the skill enforces for a reason (each has
caused a real-world white screen or offline failure):

  1. <script type="text/babel" src="...">   -- Babel loads it via XHR;
     CORS-blocked under file:// (the v2.7 incident).
  2. <script type="module">, and top-level import/export in authored .js
     -- ES modules are CORS-blocked under file://; cross-file sharing must
     go through explicit window.X globals instead.
  3. fetch(...) / XMLHttpRequest             -- cannot read local files
     under file://; seed data lives in memory.
  4. Remote URLs in authored .html/.css/.js  -- breaks offline portability.
     Absolute http(s):// is scanned everywhere; protocol-relative "//..."
     only in attribute/url() context, so JS line comments ("//note:", not
     "// note:") are not misread as URLs.

vendor/ and assets/fonts/ folders are exempt (third-party copies).
Exit code 0 = clean, 1 = findings.

Usage: python <skill-dir>/scripts/verify_artifact.py <artifact-dir>
"""
import re
import sys
from pathlib import Path

EXEMPT_DIRS = {"vendor", "node_modules", ".git"}
SCAN_EXTS = {".html", ".css", ".js"}
# xmlns and W3C namespace identifiers are not network dependencies.
URL_OK = re.compile(r"https?://(www\.)?w3\.org")
# Absolute remote URL, scanned file-wide (comments included: the rule is
# "none allowed" anywhere in authored files).
ABSOLUTE_URL = re.compile(r"https?://[^\s\"'<>)]+")
# Protocol-relative URL, valid only where a URL can occur: after a quote,
# parenthesis, or equals sign (src="//cdn/x", url(//x), href=//x). Bare //
# elsewhere is a JS line comment, not a URL.
PROTO_RELATIVE_URL = re.compile(r"[\"'(=]\s*(//)[^\s\"'<>)]+")
BABEL_SRC = re.compile(r"<script[^>]*type=[\"']text/babel[\"'][^>]*\bsrc=[^>]*>", re.I)
MODULE_SCRIPT = re.compile(r"<script[^>]*type=[\"']module[\"']", re.I)
ESM_KEYWORD = re.compile(r"^\s*(import|export)\s", re.M)
NETWORK_API = re.compile(r"\b(fetch\s*\(|new\s+XMLHttpRequest\b|\.open\s*\(\s*[\"']GET)")

def scan_file(path: Path):
    findings = []
    rel = path.as_posix()
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return [(rel, 0, f"unreadable: {e}")]

    def line_of(pos):
        return text.count("\n", 0, pos) + 1

    if path.suffix == ".html":
        for m in BABEL_SRC.finditer(text):
            findings.append((rel, line_of(m.start()),
                             f"external JSX (white screen under file://): {m.group(0)[:80]}"))
        for m in MODULE_SCRIPT.finditer(text):
            findings.append((rel, line_of(m.start()),
                             "type=\"module\" script (CORS-blocked under file://)"))
    if path.suffix in (".html", ".js"):
        for m in ESM_KEYWORD.finditer(text):
            findings.append((rel, line_of(m.start()),
                             f"ES module syntax in authored file (CORS-blocked under file://): {m.group(0).strip()}"))
        for m in NETWORK_API.finditer(text):
            findings.append((rel, line_of(m.start()),
                             f"network API in authored file (cannot read local files under file://): {m.group(0).strip()}"))
    if path.suffix in SCAN_EXTS:
        for m in ABSOLUTE_URL.finditer(text):
            if not URL_OK.search(m.group(0)):
                findings.append((rel, line_of(m.start()),
                                 f"remote URL (breaks offline portability): {m.group(0)[:80]}"))
        for m in PROTO_RELATIVE_URL.finditer(text):
            findings.append((rel, line_of(m.start()),
                             f"protocol-relative remote URL (breaks offline portability): {m.group(0)[1:].strip()[:80]}"))
    return findings

def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = Path(sys.argv[1])
    if not root.is_dir():
        print(f"not a directory: {root}")
        return 2

    findings, scanned = [], 0
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SCAN_EXTS:
            continue
        if any(part in EXEMPT_DIRS for part in path.relative_to(root).parts):
            continue
        scanned += 1
        findings.extend(scan_file(path))

    if findings:
        for rel, line, msg in findings:
            print(f"[FAIL] {rel}:{line}  {msg}")
        print(f"\n== {len(findings)} finding(s) in {scanned} file(s). Fix before delivery.")
        return 1
    print(f"== clean: {scanned} file(s) scanned, 0 findings.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
