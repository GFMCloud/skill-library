#!/usr/bin/env python3
"""
annotate.py - lint a chart spec against chart discipline and score it.

Annotation is the single biggest delta between a default chart and a deliberate
one. This module audits a dict describing a chart and returns specific,
actionable fixes plus a 0-100 score. Pure standard library - runs anywhere,
no rendering, format-agnostic (PPTX or HTML).

Usage:
    from annotate import audit, score
    audit({"chart_type": "bar", "y_min": 5, ...})  # -> list of issues
    score({...})                                    # -> 0-100

CLI:
    python3 annotate.py spec.json
    python3 annotate.py            # runs a demo spec
"""

REQUIRED_FIELDS = {
    "headline": "Declarative headline stating the takeaway ('RDS spend fell 40% after rightsizing') - not a label",
    "subtitle": "Subtitle naming unit + timeframe ('Monthly spend, USD, 2025')",
    "source": "Source line ('Source: Cost Explorer')",
    "y_axis_unit": "Y-axis unit ('Spend per month, $', 'Share of total, %')",
}

DISCIPLINE_CHECKS = [
    {
        "name": "direct_labels",
        "test": lambda c: c.get("series_count", 1) > 1 and not c.get("direct_labels"),
        "severity": "high",
        "message": "Multiple series shown via legend instead of direct labels.",
        "fix": "Label each series at its endpoint. Legends force the eye back and forth; direct labels keep it on the data.",
    },
    {
        "name": "hero_color",
        "test": lambda c: c.get("series_count", 1) > 2 and c.get("colored_series", 0) == c.get("series_count"),
        "severity": "high",
        "message": "Every series is colored - no hero.",
        "fix": "Color ONE series in the brand accent; demote the rest to grey. The viewer should know in one second which matters.",
    },
    {
        "name": "annotation_for_inflection",
        "test": lambda c: c.get("has_known_inflection") and not c.get("inflection_annotated"),
        "severity": "high",
        "message": "A known inflection point in the data is not annotated.",
        "fix": "Add an inline label at the inflection ('migration cutover', 'RI purchase'). Context lives on the chart.",
    },
    {
        "name": "axis_label_humanized",
        "test": lambda c: c.get("y_axis_label", "").islower() or "_" in c.get("y_axis_label", ""),
        "severity": "medium",
        "message": "Y-axis label reads like a column name, not English.",
        "fix": "Replace 'monthly_spend' with 'Monthly spend ($)'. Write like a person, not a database.",
    },
    {
        "name": "zero_baseline",
        "test": lambda c: c.get("chart_type") == "bar" and c.get("y_min", 0) != 0,
        "severity": "high",
        "message": "Bar chart doesn't start at zero.",
        "fix": "A bar chart's y-axis MUST start at 0. Cropping it lies about magnitude. Use a dot plot if you need to crop.",
    },
    {
        "name": "gridline_chartjunk",
        "test": lambda c: c.get("gridlines_dark") or c.get("axis_spine"),
        "severity": "medium",
        "message": "Heavy gridlines or visible axis spines compete with the data.",
        "fix": "Keep gridlines pale and remove the axis spine. Only the data should carry weight.",
    },
    {
        "name": "color_ramp_choice",
        "test": lambda c: c.get("uses_rainbow") or c.get("uses_jet"),
        "severity": "critical",
        "message": "Rainbow / jet color ramp detected.",
        "fix": "Replace with a monotonic-luminance ramp. Rainbow lies about order to colorblind viewers and to anyone printing greyscale.",
    },
    {
        "name": "readable_at_a_glance",
        "test": lambda c: c.get("requires_interaction_for_takeaway"),
        "severity": "critical",
        "message": "The takeaway is only legible on hover/click or at full screen.",
        "fix": "The key point must land at a glance - on a Zoom share and in a printed leave-behind. Rewrite labels shorter if they only work full screen.",
    },
]


def audit(chart_spec):
    """Return a severity-sorted list of issues."""
    issues = []
    for field, description in REQUIRED_FIELDS.items():
        if not chart_spec.get(field):
            issues.append({
                "severity": "high",
                "name": f"missing_{field}",
                "message": f"Missing {field}.",
                "fix": description,
            })
    for check in DISCIPLINE_CHECKS:
        try:
            if check["test"](chart_spec):
                issues.append({k: v for k, v in check.items() if k != "test"})
        except Exception:
            pass
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    issues.sort(key=lambda i: order.get(i["severity"], 4))
    return issues


def score(chart_spec):
    """0-100 discipline score for the chart spec."""
    issues = audit(chart_spec)
    penalties = {"critical": 25, "high": 10, "medium": 4, "low": 1}
    deduction = sum(penalties.get(i["severity"], 0) for i in issues)
    return max(0, 100 - deduction)


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 2:
        demo = {
            "chart_type": "line",
            "series_count": 4,
            "colored_series": 4,
            "has_known_inflection": True,
            "inflection_annotated": False,
            "y_axis_label": "monthly_spend",
        }
        print(json.dumps({"score": score(demo), "issues": audit(demo)}, indent=2))
    else:
        with open(sys.argv[1]) as f:
            spec = json.load(f)
        print(json.dumps({"score": score(spec), "issues": audit(spec)}, indent=2))
