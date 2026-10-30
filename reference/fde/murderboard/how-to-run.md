# How to run a murderboard / 進め方

- **Use:** facilitate a board after its purpose, materials, and perspectives are prepared.
- **Adaptation:** the turn-by-turn assistant protocol below makes the method method usable in chat.

## Before the board / 開始前

- State the actual decision, audience, and material version.
- Choose presentation rehearsal or engineering review.
- Ask for the three questions the presenter least wants to hear.
- Identify available evidence and which topics are outside this board’s scope.
- Read [preparation](preparing-a-design-note.md) and assign [reviewer perspectives](reviewer-roles.md).

## In the board / 実施

- Let the presenter state the problem, proposal, and decision requested briefly.
- Start from the [premortem](premortem.md) to identify consequential failure hypotheses.
- Select the most decision-relevant hypothesis and ask a specific question.
- Give the presenter space to answer before introducing another concern.
- Record the answer separately from the evidence supplied for it.
- Use [questioning techniques](questioning-techniques.md) to test scope, assumptions, and failure handling.
- Use the [engineering checklist](engineering-review-checklist.md) for a technical board.
- Keep presentation delivery feedback separate from defects in the proposed design.
- Mark a question open when the presenter cannot answer it.
- Continue with another material claim rather than repeatedly demanding unavailable evidence.

## Close / 終了

- Present the strongest supported claims alongside the most consequential open issues.
- Distinguish a demonstrated defect, an untested assumption, and a question outside scope.
- Give a recommendation with its conditions and uncertainty.
- Record a go/fix/stop decision when the accountable human actually supplies one.
- Create the [follow-up record](recording-decisions-and-follow-ups.md).
- Use a focused recheck of new evidence to close findings.

## Assistant behavior / エージェント

- Support a live question-at-a-time rehearsal or an explicitly requested written first-pass review.
- Do not turn a chat rehearsal into an invented meeting transcript.
- Do not claim multiple people reviewed the work when the assistant simulated their perspectives.
- Do not send invitations, messages, or decisions merely because the guide suggests a human board.

## Continue / 続き

- [Tool guide](index.md).
- [Output worksheet](worksheet.md).
- [Source record](../methods/delivery-and-review.md).
