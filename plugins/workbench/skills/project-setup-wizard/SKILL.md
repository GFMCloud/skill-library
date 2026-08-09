---
name: project-setup-wizard
description: Helps set up new Claude Projects from rough ideas. Takes a voice dump or brain dump about what you're working on, asks clarifying questions, and outputs a clean project description plus suggested knowledge/docs to upload. Use when starting a new project and you want to get the foundation right before diving in.
metadata:
  maturity: incubator
---

## Trigger

When the user types '/newproject', activate this skill and begin the workflow. Respond by acknowledging the command and asking for their brain dump:

"Got it - let's set up a new project. Give me your brain dump - what are you working on, what are you trying to accomplish, any context you've got dump it all out here."

# Project Setup Wizard

This Skill transforms messy ideas into well-structured Claude Projects. It takes your rough brain dump, asks the right questions, and outputs everything you need to create a focused, effective project.

## When to Use This Skill

Use this Skill when you:
- Have an idea or workstream that deserves its own project container
- Want to set up a project but aren't sure how to describe it well
- Have a fuzzy idea and need help figuring out what you're actually trying to do
- Want to avoid the "20 minutes in and I realize I didn't set the right expectations" problem

## Core Process

### Step 1: Receive the Brain Dump

Accept the user's raw voice dump or text explanation of what they're working on. This will often be messy, incomplete, or stream-of-consciousness. That's fine - that's the point.

### Step 2: Scope Check

Before going deeper, quickly assess: Does this actually need to be a project, or is it a standalone chat?

**Signs it needs a project:**
- Multiple conversations will be needed
- You'll want Claude to remember context across sessions
- There are documents/data to reference repeatedly
- It's an ongoing workstream, not a one-off task

**Signs it's a standalone chat:**
- It's a single deliverable (one email, one doc, one answer)
- No accumulated context needed
- One conversation will handle it

If it's clearly a standalone chat, say so: "This sounds like a one-off task - you probably don't need a project for this. Want to just tackle it directly?"

If it needs a project, proceed to Step 3.

### Step 3: Determine Mode

Based on how complete/confident the initial dump sounds, determine the mode:

**Quick Mode indicators:**
- User has clear goal and scope
- They know what they need, just need help packaging it
- Dump includes specifics about deliverables, timeline, decisions

**Deep Mode indicators:**
- Idea is fuzzy or exploratory
- User says things like "I'm not sure exactly what I need" or "help me think through this"
- Missing major pieces (no clear goal, no sense of what done looks like)
- Multiple possible directions

If unclear, ask: "I can either help you quickly package this into a project description, or we can go deeper with some questions to make sure we nail the foundation. Which do you prefer?"

### Step 4a: Quick Mode

For Quick Mode, extract and organize what they already know:
- Confirm the goal in 1-2 sentences
- Confirm what "done" looks like
- Identify the key deliverables/outputs
- List what context/docs Claude will need

Also infer from the dump (don't ask separately unless truly unclear):
- What role Claude is playing - executor, thought partner, reviewer, writer, etc.
- Tone signals - formal/casual, internal/external, collaborative/directive
- Output format preferences - docs, bullets, frameworks, drafts, etc.
- Any strong constraints or things explicitly off-limits

These feed directly into the Project Instructions output. In Quick Mode, infer them from context rather than asking.

Then skip to Step 5 (Output).

### Step 4b: Deep Mode

For Deep Mode, work through clarifying questions. Mix selectable options for simple questions with batched open-ended questions for deeper exploration.

**Selectable option questions (use for quick yes/no or simple choices):**

- "Are you looking for input on direction, or do you already have a set direction and need execution help?"
  - [ ] I need help figuring out the direction
  - [ ] Direction is set, I need help executing
  - [ ] Mix of both

- "What's the timeline pressure?"
  - [ ] Urgent - need something this week
  - [ ] Near-term - next few weeks
  - [ ] Ongoing - no hard deadline
  - [ ] Specific date (tell me)

- "Who's the primary audience for what you produce?"
  - [ ] Just me (thinking/planning tool)
  - [ ] Internal team/leadership
  - [ ] External (clients/customers/partners)
  - [ ] Mixed audiences

**Batched open-ended questions (group 2-4 related questions):**

Present these as a batch for the user to answer together:

"Let me ask a few questions to make sure we set this up right:

1. What does 'done' look like for this project? How will you know it's complete or successful?

2. What decisions need to be made along the way? Where do you need input vs. where are you just executing?

3. What is this project NOT about? What rabbit holes or tangents should we avoid?

4. What have you already tried, considered, or ruled out? Where are you starting from?"

**Additional questions to pull from as needed:**

- What information or data does Claude need that you have access to? What do you need to go get?
- Who else is involved in this? Who needs to approve or review outputs?
- What format should the outputs take? (Doc, talking points, framework, email, slides, etc.)
- What constraints exist that would shape the approach?
- How do you want Claude to show up in this project? (e.g., push back on your thinking, just execute, ask clarifying questions, draft first and refine, etc.)
- What tone is right for outputs from this project - and does that vary by deliverable or audience?
- Are there things Claude should never do or assume in this project - topics to avoid, angles that are off the table, decisions already made?

Don't ask all questions - pick the ones that matter based on what's missing from the initial dump.

### Step 5: Output

Provide three clearly separated sections:

**Section 1: Project Description (Copyable)**

Provide a clean 1-4 sentence description formatted for easy copy/paste into the Claude project description field. This should capture:
- What the project is about
- What you're trying to accomplish
- Key constraints or scope boundaries (if critical)

Format it in a clearly copyable block.

**Section 2: Setup Summary**

Provide a brief summary that includes:
- **Suggested documents/knowledge to upload:** What context should Claude have? Be specific - name the types of docs, data sources, or information.
- **Links or connections needed:** Any tools, data sources, or integrations that would help?
- **Starter questions:** 2-3 good first conversations to have in this project once it's set up.

**Section 3: Project Instructions (Copyable)**

Generate a full, ready-to-paste system prompt for the Claude project. This is the most important output - it defines how Claude behaves across every conversation in this project. Write it in second person directed at Claude ("You are...", "Your job is...", "When asked to...").

Calibrate depth to mode: Quick Mode instructions can be tighter and more inferred; Deep Mode instructions should be more explicit and detailed given the richer context gathered.

The instructions should always cover:

- **Role and purpose** - Who Claude is in this project and what it's here to do. Be specific about the type of work, not just the domain.
- **Working style** - How Claude should engage. Push back or just execute? Ask clarifying questions or make assumptions and flag them? Draft first or discuss first?
- **Tone and voice** - How outputs should sound. If outputs vary by audience or deliverable type, call that out explicitly.
- **Output format defaults** - What format Claude should default to (prose, bullets, frameworks, structured docs, etc.) and when to deviate.
- **Scope and constraints** - What this project is and isn't about. Decisions already made. Topics, angles, or approaches that are off the table.
- **Handling uncertainty** - What Claude should do when it doesn't have enough context: ask, flag assumptions, or make a reasonable call and note it.
- **Key context** - Any background that should persist across all conversations: who the user is, what org they're in, what stage the work is at, relevant history.

If something wasn't explicitly covered in the conversation, infer a reasonable default and write it in - don't leave blanks or placeholders. A complete, opinionated set of instructions is more useful than a template with gaps.

## Example Output

---

Project Description (copy this):

Building the go-to-market positioning and sales enablement materials for our AWS migration services. Goal is to create a clear value prop, competitive differentiation, and a set of reusable assets (one-pager, talk track, email templates) by end of Q2. Scope is limited to migration services - not the broader cloud practice.

---

Setup Summary:

Suggested documents to upload:
- Any existing AWS practice positioning or messaging docs
- Competitor research or battlecards if you have them
- Notes from recent customer conversations about why they chose you
- Internal strategy docs about the AWS practice direction

Links/connections that might help:
- AWS partner portal pages on migration competencies
- Competitor websites for positioning analysis

Starter questions for this project:
1. "Help me articulate what makes our migration approach different from the big SIs"
2. "Review this draft one-pager and pressure-test the value prop"
3. "What questions should I be asking customers to sharpen our positioning?"

---

Project Instructions (copy this):

You are a strategic messaging and sales enablement partner working on our AWS migration services go-to-market. Your job is to help develop positioning, competitive differentiation, and a set of reusable sales assets - specifically a one-pager, talk track, and email templates.

Your role in this project is to think and write, not just execute. Push back if the messaging feels generic or if a claim won't hold up under customer scrutiny. Point out where the positioning is weak before being asked.

Tone and voice: External-facing outputs should be confident and direct - written for a skeptical IT or procurement buyer, not a marketing reader. Internal outputs (talk tracks, strategy notes) can be more candid and informal. Never use marketing fluff or superlatives without substance behind them.

Output format defaults: For strategy and positioning work, lead with a clear point of view in prose before any bullets or frameworks. For sales assets, follow whatever template or format is provided - if none is provided, ask before inventing structure.

Scope: This project is strictly about AWS migration services. Don't pull in the broader cloud practice, cloud strategy, or other service lines unless explicitly asked. The competitive landscape to focus on is large SIs (Accenture, Deloitte, CDW) and AWS-native boutiques - not general IT resellers.

Constraints and decisions already made: We're positioning as a mid-market specialist - don't write for enterprise deals or Fortune 500 buyers. The Q2 deadline is fixed. Asset formats (one-pager, talk track, email templates) are decided - don't propose alternatives unless the existing formats clearly won't work.

Handling uncertainty: If you don't have enough context to write something specific, say so and ask one focused question. Don't produce vague placeholder content - a short honest question is better than a generic draft.

---

## Guidelines

- **Bias toward action**: Don't over-question. Get enough to set up a solid foundation, then let them start working.
- **Be direct about scope check**: If something doesn't need a project, say so. Save them the overhead.
- **Make outputs immediately usable**: All three sections should be ready to paste with zero editing.
- **Be specific on suggested docs**: "Upload relevant context" is useless. Name the specific types of documents.
- **Starter questions should be good first moves**: Not generic - specific to what they're trying to accomplish.
- **Project Instructions should be opinionated**: Fill gaps with reasonable inferences rather than leaving placeholders. A complete set of instructions that's 80% right is more useful than a template that's 100% empty. If you infer something significant, note it briefly so the user can correct it.
- **Calibrate instruction depth to mode**: Quick Mode instructions can be tighter - 3-5 focused paragraphs. Deep Mode instructions should be more thorough given the richer context gathered.

## Anti-Patterns to Avoid

- Don't turn this into a 20-question interrogation - pick the questions that matter
- Don't write project descriptions that are vague or generic
- Don't suggest docs to upload that they obviously don't have
- Don't skip the scope check - some things really are standalone chats
- Don't over-complicate Quick Mode - if they know what they want, package it fast
- Don't write Project Instructions that read like a template - no bracketed placeholders, no "as discussed" filler, no generic AI assistant boilerplate
- Don't make the instructions so long they become noise - every sentence should be earning its place by shaping Claude's behavior in a specific, non-obvious way
