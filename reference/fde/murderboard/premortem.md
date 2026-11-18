# Premortem / プレモーテム

- **Use:** uncover failure hypotheses that success-oriented planning may overlook.

## Procedure / 手順

- Set a future frame: the proposal or deployment failed after launch.
- Ask participants to write plausible reasons independently before discussing them.
- Group reasons by the claim or dependency they challenge.
- Separate causes from symptoms and consequences.
- For each serious hypothesis, ask what could be checked before the decision.
- Turn the most consequential hypotheses into board questions.
- Preserve an unusual but plausible hypothesis rather than discarding it because most people did not mention it.

## Hypothesis record / 仮説の記録

- **Failure:** what went wrong for the customer.
- **Cause:** the assumption, missing control, or dependency that might produce it.
- **Evidence status:** observed / reported / assumed.
- **Disconfirming check:** observation or test that could reduce the concern.
- **Owner:** role able to run the check or supply the answer.

## Example / 例

- **Synthetic failure:** operators stopped using a recommendation screen.
- **Possible cause:** recommendations used stale source data.
- **Check:** inspect update behavior and test a source-version change.
- **Limit:** this is an illustrative hypothesis, not an incident report.

## Continue / 続き

- [Tool guide](index.md).
- [Output worksheet](worksheet.md).
- [Source record](../methods/delivery-and-review.md).
