#!/usr/bin/env python3
"""Scrollback palette check.

Parses the tokens out of references/scrollback.css and recomputes every
contrast ratio, so the numbers in rulings.md are proved against the live
stylesheet rather than restated from memory. Exits 1 on any failure.

    python3 templates/verify.py            # from the skill directory
    python3 <path>/templates/verify.py     # from anywhere

The stylesheet path is resolved from this file's own location, never from the
cwd: a cwd-derived root silently checks nothing and exits 0.
"""
import pathlib
import re
import sys

CSS = pathlib.Path(__file__).resolve().parent.parent / "references" / "scrollback.css"

CORE = ["--canvas", "--surface", "--rule", "--muted", "--text", "--bright", "--accent"]
EXTENSIONS = ["--rule-dim", "--signal-warn", "--signal-fail"]

# (foreground, background, floor, label) -- the floors the system promises
SCREEN_FLOORS = [
    ("--muted", "--surface", 4.5, "smallest text on a raised panel"),
    ("--muted", "--canvas", 4.5, "smallest text on the page"),
    ("--text", "--canvas", 4.5, "body text"),
    ("--bright", "--canvas", 4.5, "emphasis"),
    ("--accent", "--canvas", 4.5, "frame title as text"),
    ("--accent", "--canvas", 3.0, "focus indicator, WCAG 1.4.11 non-text"),
    ("--signal-warn", "--canvas", 4.5, "warn severity"),
    ("--signal-fail", "--canvas", 4.5, "fail severity"),
]
PAPER_FLOORS = [
    ("--muted", "--canvas", 4.5, "smallest text on paper"),
    ("--text", "--canvas", 4.5, "body text on paper"),
    ("--accent", "--canvas", 4.5, "accent on paper"),
]


def luminance(hex_colour):
    h = hex_colour.lstrip("#")
    channels = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        channels.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    if lb > la:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)


def tokens_in(block):
    return dict(re.findall(r"(--[\w-]+)\s*:\s*(#[0-9A-Fa-f]{6})", block))


def main():
    if not CSS.is_file():
        print(f"FAIL: stylesheet not found at {CSS}")
        return 1
    css = CSS.read_text(encoding="utf-8")

    print_split = css.split("@media print{", 1)
    screen = tokens_in(print_split[0])
    paper = dict(screen)
    if len(print_split) == 2:
        paper.update(tokens_in(print_split[1]))
    else:
        print("WARN: no @media print block found; paper palette unchecked")

    fails = []

    missing = [t for t in CORE + EXTENSIONS if t not in screen]
    if missing:
        fails.append(f"missing tokens: {', '.join(missing)}")

    declared = set(CORE) | set(EXTENSIONS)
    extra = sorted(set(screen) - declared)
    if extra:
        fails.append(f"undeclared colour tokens (core stays at seven): {', '.join(extra)}")

    for palette_name, palette, floors in (
        ("SCREEN", screen, SCREEN_FLOORS),
        ("PAPER", paper, PAPER_FLOORS),
    ):
        print(f"\n== {palette_name} ==")
        for fg, bg, floor, label in floors:
            if fg not in palette or bg not in palette:
                continue
            r = ratio(palette[fg], palette[bg])
            ok = r >= floor
            print(f"  {fg:<14} on {bg:<10} {r:6.2f}:1  floor {floor:.1f}  "
                  f"{'ok' if ok else 'FAIL'}   {label}")
            if not ok:
                fails.append(f"{palette_name} {fg} on {bg}: {r:.2f}:1 < {floor}")

    print("\n== decorative, must NOT be used as text ==")
    for tok in ("--rule", "--rule-dim"):
        if tok in screen:
            print(f"  {tok:<14} on --canvas   {ratio(screen[tok], screen['--canvas']):6.2f}:1")

    print()
    if fails:
        for f in fails:
            print(f"FAIL {f}")
        print(f"\n{len(fails)} failures")
        return 1
    print(f"{len(screen)} tokens checked: 0 failures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
