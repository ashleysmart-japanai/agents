# Delivery ownership and adversarial review / 導入責任と批判的レビュー

## Outcome ownership / 成果への責任

- An FDE owns the technical delivery behind a customer outcome.
- A DS leads the business need and value hypothesis with the customer.
- Requirements need both perspectives: what should change and what can be built.
- After launch, adoption and value still need an accountable owner.
- Delegating a task does not resolve a gap in outcome ownership.

## Configure, Extend, Invent / 作業の選択

- **Configure:** use existing behavior with customer-specific settings.
- **Extend:** add a workflow, integration, or object model on a working foundation.
- **Invent:** create capability the foundation does not provide.
- Verify existing capability before selecting custom development.
- Record why an extension or invention is needed.
- Repeated custom work is evidence for product review, not an automatic commitment.

## What a board tests / レビューの目的

- A presentation board challenges the decision case and the communication.
- An engineering board challenges the proposed behavior and its evidence.
- A premortem starts from a hypothetical failure and works backward to assumptions.
- Different reviewer perspectives expose different gaps.
- A confident answer is not equivalent to a test result.
- An unanswered question becomes an owned follow-up, not a fabricated answer.

## Minimum engineering preparation / 設計準備

- State the problem, goals, non-goals, and proposed design.
- Explain the alternatives, including configuration.
- Identify evaluation cases, correct-answer ownership, and acceptable failure behavior.
- Describe data/access assumptions and human hand-back.
- State operational ownership and workload/cost assumptions.
- Keep the note short enough for reviewers to read before the board.

## Closing the board / 終了

- Distinguish an observed defect from an untested assumption.
- Explain the consequence for the intended customer decision.
- Record the human decision separately from the assistant recommendation.
- Assign each unresolved item an owner, date, and closure condition.
- Preserve the reasons and final evidence for the next team.

## Example / 例

- A support assistant produces plausible answers in a small demonstration.
- A reviewer asks which policy versions were tested and who can certify correctness.
- If that evidence is unavailable, record an evaluation gap.
- Do not conclude that the assistant is proven unsafe or ready to launch from that gap alone.

## Apply / 実務で使う

- [Deployment Planner / 導入計画](../deployment-planner/index.md).
- [Murderboard / マーダーボード](../murderboard/index.md).
