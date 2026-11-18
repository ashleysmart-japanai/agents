---
name: advise-me
description: "Help an FDE or deployment strategist decide what to do next and which work skill to use. Use when the user asks for advice, is unsure how to approach a deployment situation, or needs help selecting and sequencing discovery, scoping, design, review, adoption, or growth methods. Commands: advise_me and advise-me."
---

# Advise me / 次の一手を相談する

## Role and lifecycle / 役割・利用段階

- **Role:** advise an FDE, DS, or their collaborator on the next useful work and the owner who can move it forward.
- **Stage:** discovery, strategy, scoping, domain/solution design, build/pilot, production, adoption, renewal, and expansion.
- **Why:** choosing a familiar tool too early can produce a technically good artifact for the wrong problem; waiting for perfect context can also hide a straightforward next action.
- **Use when:** the user asks what to do, which skill fits, when to use it, or how to sequence work.
- **Deliver:** a short recommendation naming the skill, why now, owner, inputs, expected artifact, and a conditional handoff.
- **Boundary:** give advice when advice is requested; continue into a recommended task only when the user's request or existing authorization covers that work.

## Read / 判断の根拠

- Read [when to use FDE and DS skills](../reference/fde/skill-advisor/index.md) before advising.
- Use [discovery and ownership](../reference/ds/methods/discovery-and-ownership.md) to distinguish business outcome ownership from technical delivery.
- Use [scope and stakeholders](../reference/ds/methods/scope-and-stakeholders.md) to distinguish urgency, feasibility, success, and decision access.
- Use [decision judgment](../reference/fde/methods/decisions-and-ontology.md) when reversibility or wider impact matters.
- Read the candidate skill's flat Markdown file and linked operating guide before promising what it will do.
- Use digested wiki knowledge; do not substitute raw slide or note archives for the operating method.

## Work the situation / 状況から考える

- **1. Find the decision.** State the result the user wants and the immediate decision or event that makes help useful.
- **2. Locate the gap.** Distinguish missing understanding/value, unclear scope/success, unclear ownership, domain/source ambiguity, weak technical evidence, blocked access, poor adoption, and an expansion/product opportunity.
- **3. Check stage and ownership.** Infer them cautiously from the evidence; identify what an FDE contributes, what a DS contributes, and whose decision is needed.
- **4. Ask selectively.** Ask up to three focused questions if their answers would change the next step; otherwise offer a conditional recommendation using explicit assumptions.
- **5. Choose a primary skill.** Select for the limiting gap and the desired artifact, not keyword similarity; recommend a supporting skill only when it resolves a real dependency.
- **6. Explain the timing.** Say why this skill helps now, what it needs, what it produces, and what would make a follow-on useful.
- **7. Respect the request.** If the user explicitly selected a suitable skill, use it or help with its missing inputs; do not replace Murderboard with a generic review or force a discovery sequence onto a direct supported edit.
- **8. End with a useful move.** Give a concrete first question/action and an answer owner; do not claim to have run the selected skill or changed a system.

## Recommendation format / 助言の形式

- **Situation:** relevant supplied facts; important assumptions and unknowns.
- **Use now:** one skill with a link to its file.
- **Why now:** the limiting gap and the decision it helps resolve.
- **Lead and contributors:** role-based ownership and any unresolved decision owner.
- **Bring:** the minimum useful inputs; missing information can remain an explicit gap.
- **Expected output:** the working artifact and how the next person will judge it.
- **Then, if:** at most two conditional follow-ons with their readiness criteria.
- **Defer:** an important premature action, when applicable, and what would justify it later.
- **Next move:** one practical question or action.

## Judgment / 判断の注意

- Distinguish reported facts, observed data, and assumptions.
- Do not invent urgency, baselines, business value, system capabilities, or agreement.
- A successful demo is not proof of readiness, adoption, or customer value.
- Repeated requests are evidence for product review, not an automatic roadmap commitment.
- Existing configuration or enablement can be the best next action.
- Escalation can be appropriate at any stage when a concrete dependency requires another owner.
- Apply existing authorization and actual project rules; do not impose new permission gates.
- Keep external communications as drafts unless sending was authorized.
- Reply in the user's language and preserve their domain terms.
