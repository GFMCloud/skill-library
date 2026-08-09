#!/usr/bin/env python3
"""
chart_selector.py - recommend a chart type from the question being asked.

Given the SHAPE of the data and the QUESTION the slide is meant to answer,
return a chart-type recommendation with a one-line rationale and an
anti-pattern warning. Pure logic - no dependencies, no rendering, no network.

The defaults encoded here:
  - Line for time-series. Anything else needs a reason.
  - Small multiples when more than ~5 series share a time axis.
  - Never pie. Use bar or stacked-bar instead.
  - Ranked lists: horizontal bar, sorted by value.
  - Correlation: scatter with named outliers, not a naked cloud.
  - Diverging color only with a meaningful zero.

Usage:
    from chart_selector import select_chart
    select_chart("change_over_time", {"n_series": 3, "x_type": "time"})

CLI:
    python3 chart_selector.py change_over_time '{"n_series": 3}'
"""

PATTERNS = {
    "change_over_time": {
        "single_series": {
            "recommended": "line chart",
            "why": "One line, one accent color, direct end-of-line label.",
            "avoid": "Area chart, unless the filled magnitude is the point - areas exaggerate.",
        },
        "few_series": {
            "recommended": "line chart, one hero series in accent, the rest grey",
            "why": "Color the line the story is about; demote the rest to context.",
            "avoid": "Coloring every line - viewers can only track one or two at once.",
        },
        "many_series": {
            "recommended": "small multiples (one panel per series, shared axes)",
            "why": "Past ~5 lines a single chart becomes spaghetti.",
            "avoid": "Piling 12 lines on one axis with a 12-color legend.",
        },
    },
    "compare_categories": {
        "few": {
            "recommended": "horizontal bar chart, sorted by value",
            "why": "Labels fit horizontally; viewers compare bar lengths effortlessly.",
            "avoid": "Vertical bars that force rotated labels.",
        },
        "many": {
            "recommended": "dot plot or small bar chart with named head and tail",
            "why": "Annotate the extremes; leave the middle as context.",
            "avoid": "50 tiny bars when only 6 matter.",
        },
    },
    "show_distribution": {
        "default": {
            "recommended": "histogram or strip plot (jittered dots)",
            "why": "A density curve hides the actual observations; dots show them.",
            "avoid": "Box plots - general audiences don't read them.",
        },
    },
    "show_correlation": {
        "default": {
            "recommended": "scatter plot with 3-5 named outliers and a reference line",
            "why": "A naked cloud of dots says nothing; annotate the named points.",
            "avoid": "A regression line with no R-squared or no plain-English meaning.",
        },
    },
    "show_composition": {
        "default": {
            "recommended": "stacked bar (one bar per period or category)",
            "why": "Stacks read fast. Pies fail completely past four slices.",
            "avoid": "Pie. 3D pie. Donut, unless the hole shows a total.",
        },
        "over_time": {
            "recommended": "stacked area, most-volatile component on top",
            "why": "Put the volatile band where the eye lands - the upper baseline.",
            "avoid": "Streamgraphs - pretty but unreadable for actual numbers.",
        },
    },
    "rank_items": {
        "default": {
            "recommended": "ranked horizontal bar chart, sorted descending",
            "why": "Sort by the variable being compared, not alphabetical. Length = value.",
            "avoid": "Alphabetical sort; lollipops where the dot carries no value.",
        },
    },
    "where_is_it": {
        "single_point": {
            "recommended": "locator map (zoom in, label known landmarks)",
            "why": "The question is where it sits relative to things people know.",
            "avoid": "A single point dropped on a world map with no reference.",
        },
        "many_values": {
            "recommended": "choropleth (sequential ramp) or sized-circle map",
            "why": "Choropleth when geography matters and values vary; circles for raw counts.",
            "avoid": "Choropleth when the story is absolute counts in dense areas.",
        },
    },
}

CANONICAL_QUESTIONS = list(PATTERNS.keys())


def select_chart(question_type, data_shape=None):
    """Return the recommendation for this data + question."""
    data_shape = data_shape or {}
    rules = PATTERNS.get(question_type)
    if not rules:
        return {
            "recommended": "line chart (default)",
            "why": "When unsure, start with a line on a time axis - the safe default.",
            "avoid": "Reaching for novelty (sankey, chord, radial) before line/bar fail.",
        }

    n_series = data_shape.get("n_series", 1)
    has_time = data_shape.get("x_type") == "time"

    if question_type == "change_over_time":
        if n_series == 1:
            return rules["single_series"]
        if n_series <= 5:
            return rules["few_series"]
        return rules["many_series"]

    if question_type == "compare_categories":
        return rules["few"] if data_shape.get("n_rows", 0) < 15 else rules["many"]

    if question_type == "where_is_it":
        return rules["many_values"] if n_series > 1 else rules["single_point"]

    if question_type == "show_composition":
        return rules["over_time"] if has_time else rules["default"]

    return rules.get("default", list(rules.values())[0])


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 2:
        print("Usage: chart_selector.py <question_type> [json_data_shape]")
        print(f"  question_types: {CANONICAL_QUESTIONS}")
        sys.exit(1)
    q = sys.argv[1]
    shape = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    print(json.dumps(select_chart(q, shape), indent=2))
