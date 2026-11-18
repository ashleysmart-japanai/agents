# When to use FDE and DS skills / FDE・DSスキルの使い分け

- **Purpose:** choose a useful next action from the customer situation, the decision needed, and the evidence available.
- **Audience:** FDEs, deployment strategists, and assistants supporting their work.
- **Entry:** [advise_me skill](../../../skills/ADVISE_ME.md).
- **Principle:** choose the skill for the next unresolved decision, not simply for the current project phase or a familiar tool name.
- **Proportionality:** a small configuration task can need a short capability check rather than a full discovery workshop.
- **Authority:** this guide helps select work; it does not create new organizational approval rules.

## Start with the situation / 状況を確かめる

- Identify the outcome the user wants and the decision or work that should change.
- Identify who owns that outcome and who can supply the technical or business evidence.
- Find the current stage from what is happening, rather than treating a project label as proof of readiness.
- Identify the next consequential event: a customer meeting, build commitment, pilot result, launch, renewal, or product decision.
- Find the limiting gap: understanding, value, scope, ownership, model, technical evidence, access, adoption, or a decision.
- Ask a few targeted questions only when different answers would change the recommended next step.
- Keep a stage or owner inferred from sparse context labeled assumed.

## Role and lifecycle / 役割と段階

- **Discovery:** DS leads problem/value discovery; FDE contributes technical understanding; work toward an evidenced customer problem.
- **Strategy and scope:** DS and FDE shape the first useful step together; work toward bounded scope, measurable success, and known dependencies.
- **Domain and solution design:** FDE leads technical design with domain input from DS and customer roles; work toward a model and delivery approach that serve the decisions.
- **Build and pilot:** FDE leads implementation and technical verification; DS keeps scope and customer outcomes visible; surface dependencies before they silently delay work.
- **Production and handover:** FDE provides operational evidence; DS resolves use, success, and ownership agreements with the customer.
- **Adoption and renewal:** DS leads customer value and relationships; FDE investigates technical causes and supplies operating evidence.
- **Expansion and product feedback:** DS tests the next customer need; FDE identifies reusable foundations and repeated effort; the relevant product owner decides shared investment.
- **Boundary:** these are working patterns; confirm actual decision and delivery ownership rather than imposing an organization chart.

## Pick the skill / スキルを選ぶ

- **Unknown work or vague request → [Discovery Interviewer](../../../skills/DISCOVERY_INTERVIEWER.md).** Reconstruct a real day or incident; finish with events, decisions, information inputs, handoffs, and open questions.
- **Known symptom, unclear cause or value → [Problem & Value Explorer](../../../skills/PROBLEM_VALUE.md).** Test cause branches and connect operational change to activity, outcome, and impact measures with owners.
- **A first step or stalled pilot needs shaping → [Scope & Success Designer](../../../skills/SCOPE_SUCCESS.md).** Produce In / Out / Not now, feasibility dependencies, and measurable done; use [DS Scope Checker](../../../skills/DS_SCOPE_CHECKER.md) for a detailed check or FDE handoff review.
- **Nobody knows who decides or takes over → [Ownership & Handoff Designer](../../../skills/OWNERSHIP_HANDOFF.md).** Separate decision ownership from delivery and test the boundary against a real scenario.
- **The model cannot explain business terms, sources, or decisions → [Ontology Designer](../../../skills/ONTOLOGY_SKETCHER.md).** Design and test competency questions, events, objects, source mappings, links, and actions; use [Builder Wizard](../../../skills/BUILDER_WIZARD.md) to facilitate that work over several turns.
- **The outcome is understood but the delivery approach is open → [Deployment Planner](../../../skills/DEPLOYMENT_PLANNER.md).** Check existing functionality, then choose Configure / Extend / Invent with evidence and ongoing owners.
- **A proposal or design is ready for consequential challenge → [Murderboard](../../../skills/MURDERBOARD.md).** Test the decision case or engineering assumptions before the meeting, major commitment, or handover; retain the question log and owned follow-ups.
- **The next action has unclear reversibility or wider impact → [Decision Advisor](../../../skills/DECISION_ADVISOR.md).** Assess the undo path, blast radius, and actual decision authority; keep the reasoning in a decision/check-in record.
- **A blocker, business decision, or opportunity needs another owner → [Steering & Escalation Planner](../../../skills/STEERING_ESCALATION.md).** Prepare an actionable help request or value-focused steering brief; routine steering and urgent escalation are different work modes.
- **A working prototype may be mistaken for production readiness → [Production Readiness Review](../../../skills/PRODUCTION_READINESS.md).** Check intended use, data, access, behavior, interfaces, and maintenance; produce an evidence-backed gap backlog.
- **An alternative or objection needs a credible response → [Customer Conversation Rehearsal](../../../skills/CUSTOMER_CONVERSATION.md).** Understand what the customer means, acknowledge what works, and rehearse a response tied to evidence and a next step.
- **A customer decision is stuck in relationships or concerns → [Stakeholder & Conversation Planner](../../../skills/STAKEHOLDER_CONVERSATION.md).** Map roles and observed influence; test champion access and rehearse listening, the relevant number, and a specific request.
- **A useful deployment should enable the next useful result → [Account Growth Planner](../../../skills/ACCOUNT_GROWTH.md).** Show now/next/later, the requesting customer role, concrete reuse, and the next validation action.
- **Repeated needs may justify shared capability → [Product Opportunity Scout](../../../skills/PRODUCT_OPPORTUNITY.md).** Distinguish standard, bespoke, and reusable needs; deduplicate accounts and produce a product-candidate note for the decision owner.

## Sequence by the limiting gap / 足りないものから順番を決める

- **Request → discovery → value → scope:** establish the problem and its consequence before committing a solution.
- **Scope → model and delivery approach → review:** clarify the domain where needed, choose an implementation approach, and challenge the consequential assumptions.
- **Pilot → evidence → readiness → adoption:** technical success does not prove that the work changes, people use it, or operations have owners.
- **Adoption → next useful layer → product feedback:** distinguish account expansion from cross-account product investment.
- **Feedback loops:** return to discovery when actual work differs from assumptions; return to scope when the success condition is wrong; return to source/model work when evidence exposes an identity or meaning gap.
- **Exception handling:** a real dependency or consequential risk can need escalation during any stage.
- **Existing authorization:** do not introduce a consultation gate for routine work that is already authorized.

## Advice and handoff / 助言と引き継ぎ

- **Situation:** state the supplied facts and the assumptions that matter.
- **Recommend now:** identify one primary skill and the immediate decision it helps resolve.
- **Why now:** explain the gap and consequence that make the skill useful.
- **Owner:** identify the business lead, technical contributor, and human decision owner where known.
- **Bring:** name the smallest set of inputs needed to start.
- **Produce:** describe the artifact and the evidence that makes it useful to the next person.
- **Then:** name a follow-on only with its readiness condition; avoid an automatic full-course checklist.
- **Defer:** explain an attractive premature action and the evidence needed before reconsidering it.
- **Next move:** propose a concrete first question or action; do not claim the recommended work has already happened.

## Worked choices / 判断例

- [Examples and nearby choices](decision-examples.md) illustrate how to select a next step without turning the lifecycle into a mandatory checklist.

## Distilled foundations / 判断の根拠

- [Delivery ownership and critical review](../methods/delivery-and-review.md) explains decomposing before building and reviewing consequential proposals.
- [Diagnosis and value](../methods/diagnosis-and-value.md) explains cause/value chains, measurement, steering, and escalation.
- [Decision judgment and ontology](../methods/decisions-and-ontology.md) explains proportional action and testing a shared model.
- [Readiness and positioning](../methods/readiness-and-positioning.md) explains prototype gaps and evidence-led conversations.
- [Discovery and responsibility](../../ds/methods/discovery-and-ownership.md) explains interviews, outcome ownership, and lifecycle handoffs.
- [Reuse and growth](../../ds/methods/product-reuse-and-growth.md) explains account versus shared-product opportunities.
- [Scope and stakeholders](../../ds/methods/scope-and-stakeholders.md) explains urgency, useful first steps, success, feasibility, and decision access.
- **Synthesis:** the routing order and advice format organize these methods; they are not a universal process or a fixed organizational policy.
