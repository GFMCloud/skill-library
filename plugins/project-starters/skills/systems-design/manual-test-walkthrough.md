# Manual Test: Customer Referral Program

## Test Prompt
"I want to launch a customer referral program for our B2B SaaS product. Help me design the system."

## Expected Skill Behavior

### 1. Initial Confirmation
✓ Should trigger systems-design skill
✓ Should ask: "This looks like a systems design conversation - I'll help you work backwards from your end goal to build a pressure-tested plan. We'll spend about 20-30 minutes building this out together. Sound good?"

### 2. Phase 1: End State Definition (Collaborative → Thinking Partner)

Should ask using ask_user_input_v0:
- What does success look like in measurable terms?
  * Options might be: # of referrals, conversion rate, revenue from referrals, customer LTV
- What evidence proves you achieved it?
- Timeline?
- Constraints?

Should pressure test vague answers:
- If user says "more referrals" → push for specific number
- If user says "successful program" → demand measurable evidence
- Should call out gap between fuzzy goal and concrete outcome

Expected output: "50 new customers from referrals in 6 months, 15% referral-to-paid conversion, $500K ARR from referred customers"

### 3. Phase 2: Dependency Mapping (Collaborative)

Should work backwards:
- For 50 new customers → need ~333 referrals at 15% conversion
- For 333 referrals → need existing customers to refer
- For customers to refer → need incentive structure + easy referral mechanism
- For incentive structure → need to understand customer motivation

Should identify feedback loops:
- Positive: Good referred customers → happier referrer → more referrals
- Negative: Poor referral experience → damaged trust → fewer referrals
- Balancing: Referral fatigue - customers won't refer infinitely

Should ask about time delays:
- How long from referral to signup?
- How long to see if referred customer is quality?

Expected output: Dependency map showing prerequisites at each level + feedback loops

### 4. Phase 3: Premortem (Thinking Partner)

Should set the scene: "It's 12 months from now. The referral program failed. Why?"

Should guide through failure modes:
- "We gave $500 credits but referred customers churned in month 2 because they weren't qualified"
- "Existing customers didn't refer because the process required 8 clicks and a form"
- "We hit our referral numbers but cannibalized direct sales - same customers were going to buy anyway"
- "Referral incentive was too high and attracted referral fraud/gaming"

Should use rank_priorities to help user prioritize which to mitigate

Should pressure test:
- Are failure modes specific enough for early warning indicators?
- What about external failures? (Competitor launches better program, regulation changes on incentives)
- What can't you mitigate? Should you kill this?

Expected output: Ranked failure modes with mitigation strategies

### 5. Phase 4: Step Definition (Collaborative → Thinking Partner)

For each step, should define:
- Outcome: "Referral mechanism live with <3 clicks to refer"
- Evidence: "10 beta customers successfully referred at least 1 person"
- Timeline: "2 weeks"
- Resources: "Frontend dev 40hrs, backend dev 20hrs"
- Decision criteria: "If beta referral rate <5%, pivot incentive structure"

Should pressure test:
- Is "good enough" defined or will you over-engineer?
- Who's the bottleneck? (Design? Legal approval? Integration with payment system?)

Expected output: Each step with outcomes, evidence, decision gates

### 6. Phase 5: Integration & Modular Grouping (Collaborative)

Should identify critical path:
- Must design incentive structure BEFORE building referral UX
- Can run legal review parallel with technical build

Should identify sprint modules and CONFIRM grouping logic:
- Module 1: Incentive Design (research motivation, design structure, legal review)
- Module 2: Referral Mechanism (UX design, technical build, integration)
- Module 3: Tracking & Attribution (analytics, reporting, dashboards)
- Module 4: Launch & Optimization (beta test, rollout, iteration)

Should ask: "I'm grouping these by functional area - incentive design, technical build, measurement, and launch. Does that make sense for how you'd want to tackle this?"

Should use ask_user_input_v0:
- If you lost 50% of timeline, what would you cut?
- What's smallest version to prove model?

Expected output: Sequenced plan with confirmed sprint modules

### 7. Final Deliverables

Should create:
1. Visual diagram using visualize:show_widget
   - Shows complete referral system flow
   - Clearly highlights the 4 modules (color/borders/grouping)
   - Shows dependencies between modules
   - Shows feedback loops

2. Markdown summary document
   - End state with metrics
   - Dependency map
   - Failure modes & mitigations
   - Implementation steps
   - Sprint modules with rationale
   - Critical path
   - Early wins

Should save to /mnt/user-data/outputs/ and present via present_files

## Pass/Fail Criteria

PASS if:
✓ Skill triggers automatically
✓ Pushes for measurable outcomes (not "successful program")
✓ Maps dependencies backwards
✓ Runs premortem with specific failure modes
✓ Identifies and CONFIRMS modular grouping
✓ Creates visual with highlighted modules
✓ Produces actionable summary doc
✓ Uses ask_user_input_v0 for multi-choice questions
✓ Switches between Collaborative and Thinking Partner modes appropriately
✓ Completes in reasonable conversation length (not 50 back-and-forths)

FAIL if:
✗ Doesn't trigger skill
✗ Accepts vague goals without pushing
✗ Skips premortem
✗ Doesn't identify sprint modules
✗ Doesn't confirm grouping logic with user
✗ No visual diagram or diagram doesn't highlight modules
✗ Summary doc is generic/not actionable
