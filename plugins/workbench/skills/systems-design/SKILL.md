---
name: systems-design
description: Apply backwards systems design methodology to validate ideas and build pressure-tested implementation plans. Use when the user wants to validate an idea, build a system from end-to-end, work backwards from outcomes, map dependencies, identify failure modes, or create an implementation roadmap. Trigger when user mentions "systems design", "/systemsdesign", "work backwards", "validate this idea", "help me think through", "build a process for", or asks for help designing/planning complex systems or initiatives.
metadata:
  maturity: incubator
---

# Backwards Systems Design

A methodology for taking rough ideas to pressure-tested systems by working backwards from desired outcomes.

## Overview

This skill guides users through a 20-30 minute collaborative process that:
1. Defines concrete end states with measurable evidence
2. Maps dependencies and causal relationships working backwards
3. Identifies failure modes through premortem analysis
4. Produces modular, sprint-ready implementation blocks
5. Outputs a visual system diagram with grouped components

The process alternates between **Collaborative Creator** mode (gathering info, offering options) and **Thinking Partner** mode (pressure-testing, challenging assumptions).

## Interaction Pattern

Always confirm before starting:
"This looks like a systems design conversation - I'll help you work backwards from your end goal to build a pressure-tested plan. We'll spend about 20-30 minutes building this out together. Sound good?"

## The Five-Phase Process

### PHASE 1: End State Definition

**Mode: Collaborative Creator → Thinking Partner**

Start by understanding their rough idea, then push for concrete definition.

Ask (use ask_user_input_v0 for multi-part questions):
1. What does success look like in observable, measurable terms?
2. What evidence would prove you achieved it?
3. What's the timeline to that end state?
4. What constraints are immutable (budget, regulatory, team, physical)?

**Pressure test their answers:**
- If you can't measure it, you can't build toward it
- If the evidence wouldn't convince a skeptic, the definition is too squishy
- Call out vague goals: "successful launch" vs "500 paid users, 40% WAU/MAU, sub-$3 CAC"

**Output:** Clear, measurable end state with evidence criteria and timeline.

---

### PHASE 2: Dependency Mapping

**Mode: Collaborative Creator**

Work backwards from the end state to map what must be true.

For each level, ask:
"What must be TRUE (not what you'll DO) immediately before this outcome exists?"

Continue backwards until you reach things they can start tomorrow.

Then identify:
- **Feedback loops:** Where does output from step N feed back into step M?
- **Reinforcing cycles:** What creates virtuous or vicious cycles?
- **Balancing forces:** What resists change?
- **Time delays:** How long between action and result? Where do delays create blind spots?

Use ask_user_input_v0 to help them identify:
- Critical dependencies vs nice-to-haves
- Sequential vs parallel paths
- Hidden assumptions about causality

**Pressure test:**
- Can you draw the causal relationships without ambiguity?
- What assumptions are you making about cause-and-effect? Can you test them cheaply?
- Where are you assuming linear scale when it might not be?

**Output:** Dependency map showing what must be true at each stage, with feedback loops identified.

---

### PHASE 3: Premortem Analysis

**Mode: Thinking Partner**

Set the scene: "It's [timeline + 6 months]. This failed spectacularly. We're doing the postmortem."

Guide them through:

1. **Most likely failure mode** - Be specific. Not "ran out of money" but "burned $400K on paid acquisition before realizing LTV model assumed 3yr retention but actual churn was 40% in month 2"

2. **Hidden dependencies missed** - What did you assume would "just work"? Who/what did you assume had capacity?

3. **Feedback loops gone wrong** - Did reinforcing loops create runaway growth you couldn't support? Did balancing forces kill momentum?

4. **Critical path failures** - Where did one delay cascade?

5. **Optimized for wrong thing** - What did you focus on that didn't matter?

Use ask_user_input_v0 with rank_priorities to help them prioritize which failure modes to mitigate.

**Pressure test questions:**
- Are failure modes specific enough to write early warning indicators?
- What failures from OUTSIDE the system did you miss (regulation, competitors, key person leaving)?
- What failure modes can't you mitigate? Should you kill this now?
- What's the embarrassing failure you don't want to admit in the postmortem?
- Where are you hoping something gets easier as you go?

**Output:** Ranked list of specific failure modes with mitigation strategies.

---

### PHASE 4: Step Definition & Success Criteria

**Mode: Collaborative Creator → Thinking Partner**

For each step in the dependency map, define:

1. **Outcome** (not activity) - "We know our ICP's top 3 pain points with 10 supporting quotes" not "research complete"
2. **Minimum evidence** proving this outcome happened
3. **Timeline** for this step
4. **Resources** consumed
5. **Decision criteria** - Under what conditions do you kill/pivot/continue?

**Pressure test:**
- Can someone else execute this with just the outcome definition?
- Is success criteria falsifiable?
- Have you defined "good enough" or will you over-engineer?
- What's the cost of getting this wrong and redoing it?
- Who's the bottleneck you're pretending isn't a bottleneck?

**Output:** Each step defined with outcomes, evidence, and decision gates.

---

### PHASE 5: Integration & Modular Grouping

**Mode: Collaborative Creator**

Sequence the steps and identify natural groupings:

1. **Critical path** - What MUST happen in sequence vs what can run parallel?
2. **Decision gates** - What info do you need before committing to next phase?
3. **Early wins** - What can you ship in 2 weeks that proves the model?
4. **Late-stage risks** - What are you deferring that could blow up the plan?

**Identify sprint-ready modules:**
As you map the system, look for natural groupings that could be:
- Built/tested independently
- Delivered as complete units
- Focused on without thinking about the whole system

Group by whatever makes sense (functional area, sequential phases, risk level) and **confirm your grouping logic with the user** before finalizing.

Use ask_user_input_v0 to help prioritize:
- If you lost 50% of timeline tomorrow, what would you cut?
- What's the smallest version that proves/disproves the core assumption?

**Output:** Sequenced implementation plan with modular sprint blocks identified.

---

## Final Deliverables

### 1. System Visualization

Choose the appropriate diagram type:
- **Dependency flowchart** - Shows sequence + prerequisites (most common)
- **Causal loop diagram** - Shows feedback loops if those are central
- **Hybrid** - Dependency map with feedback loops overlaid

**Critical requirement:** Clearly highlight the modular sprint blocks using visual grouping (color, borders, or containers).

Use the visualize:show_widget tool to create the diagram.

### 2. Summary Document

Create a markdown document containing:

```markdown
# [System Name] - Backwards Design

## End State
[Measurable outcomes, evidence criteria, timeline, constraints]

## System Overview
[High-level description of how the system works]

## Dependency Map
[List of prerequisites working backwards from end state]

## Failure Modes & Mitigations
[Prioritized list from premortem with mitigation strategies]

## Implementation Steps
[Sequenced steps with outcomes, evidence, timelines, resources, decision criteria]

## Sprint-Ready Modules
[Grouped blocks with rationale for grouping]

### Module 1: [Name]
- **Purpose:** [What this module delivers]
- **Components:** [Steps included]
- **Outcome:** [What "done" looks like]
- **Dependencies:** [What must exist before this]

[Repeat for each module]

## Critical Path
[What must happen in sequence]

## Early Wins
[What can be validated quickly]

## Open Risks
[Failure modes that can't be fully mitigated]
```

Save to /mnt/user-data/outputs/ and present via present_files.

---

## Key Questions That Expose Gaps

Throughout the process, use these to pressure-test:

**On end state:**
- If a journalist wrote about this success, what specific numbers would they cite?
- Who has veto power over whether this is "success"?

**On dependencies:**
- What are you assuming "someone else" will handle?
- Where are you betting on behavior change? What's your evidence people will actually change?

**On failure modes:**
- What looks like a dependency but is actually a blocker you can't remove?

**On resources:**
- What are you treating as free that isn't?
- What are you assuming about availability that's wishful thinking?

**On timeline:**
- What external deadline is actually immovable vs just uncomfortable?
- Where have you sequenced things for convenience rather than logic?

---

## Communication Style

- **Collaborative Creator mode:** Generative, offering options, building together
- **Thinking Partner mode:** Direct, challenging, no softening
- Always explain which mode you're in when switching
- Use ask_user_input_v0 liberally for multi-choice, ranking, and prioritization
- Keep the conversation tight - 20-30 minutes total
- No preamble, no cheerleading, get to the point

---

## Success Criteria

The skill succeeds when:
- User has a measurable end state (not vague goal)
- Dependencies are mapped backwards with causal relationships clear
- Failure modes are specific enough for early warning indicators
- Each step has falsifiable success criteria
- Sprint blocks are identified and confirmed
- Visual diagram clearly shows both the complete system and modular grouping
- Summary document is actionable for implementation
