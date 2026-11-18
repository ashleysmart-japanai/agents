# claim-brief

A **claim-brief** describes one review claim to the user in chat. Use it when the user asks about a single claim ("hit me with M5", "explain B11") or when a claim is presented on its own.

- A claim list or a multi-claim report uses its own format; a claim-brief is for one claim.
- Write it in ASD-STE100 Simplified Technical English (§ Writing rules).
- The brief is short paragraphs under fixed labels, not dot points; this is the chat exception to `style/DOT_POINT_SRP.md`.

## Template

```md
**<full tracking ID> [<SEVERITY>]**

**Problem:** <short summary>.

<Details: where the issue occurs, what happens, and its effect.>

**Proposed fix:** <the concrete change and how it resolves the issue>.

**Prior evidence:** <earlier findings, applied fixes, proposals, and user decisions, with full tracking IDs>.
```

- **Heading:** the full tracking ID and severity; nothing else.
- **Problem:** one short sentence: the defect only, with no cause and no fix.
- **Details:** one to three short paragraphs.
  - Where: the file and the real symbol names (`style/QUICK_REF.md`), and what each symbol does.
  - What happens: the change, call order, or data flow that causes the defect.
  - Effect: the impact, and the limits of the impact (for example, "It does not change permission checks").
- **Proposed fix:** the concrete change, and how it resolves the issue; what to keep unchanged.
- **Prior evidence:** earlier findings, applied fixes, proposals, and user decisions.
  - Cite claims by full tracking ID and commits by SHA.
  - Say which claim or commit caused this one.
  - Say whether the fix is applied, proposed, or not started.
- Leave out a section that has no content; do not write "N/A".

## Writing rules (ASD-STE100)

- Write short sentences: 20 words or fewer for an instruction, 25 words or fewer for a description.
- Write one topic in each paragraph; use six sentences or fewer in a paragraph.
- Use the active voice.
- Use the simple tenses: present, past, and future.
- Write one instruction in each sentence; use the imperative for an instruction.
- Use each word with one meaning only; use the same word for the same thing each time.
- Use technical names (code symbols, file names, product names) as they are written.
- Use the articles "the", "a", and "an"; do not omit them to save words.
- Do not use a noun cluster of more than three words; split it with a preposition.
- Do not use phrasal verbs ("set up", "carry out"); use one verb ("configure", "do").
- Do not use the "-ing" form of a verb, except in a technical name.
- Write positive statements where possible; state what is true.
- Do not use slang, jargon that is not a technical name, or invented terms.

## Example

```md
**M5.0aBcDeFgHiJkLmNoPqRsTu [LOW]**

**Problem:** The access-warning comment is attached to the wrong method.

In `orders.service.ts`, `getOwnerByIdUnsafe()` reads only the account and project IDs that the permission check needs. `getByIdUnsafe()` reads the full order record, with its payment settings.

The ownership-only method was added between the existing warning comment and the full-record method. The warning now describes the ownership-only method. The full-record method has no warning that authorization must succeed before a call.

This is a documentation error. It does not change permission checks or data access.

**Proposed fix:** Move the warning comment to `getByIdUnsafe()` and add a comment to `getOwnerByIdUnsafe()`. Each comment then describes the method it is attached to. The full-record method again warns that authorization must succeed first.

**Prior evidence:** Commit `1a2b3c4d5e6` added the ownership-only method to fix I5.1aBcDeFgHiJkLmNoPqRsTu, which concerned detail reads before permission checks. That fix caused this comment-placement error. A fix is proposed; it is not applied.
```
