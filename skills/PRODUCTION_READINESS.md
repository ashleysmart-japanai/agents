---
name: production-readiness
description: "Review production readiness, handover conditions, operational gaps, or an unsupported capability claim. Supports prototype → pilot → production; revisit when usage, data, or operating conditions change."
---

# Production Readiness Review / 本番準備レビュー

## Role and lifecycle / 役割・利用段階

- **Role:** FDE assesses delivery evidence; DS resolves scope and operating agreements with the customer.
- **Stage:** Prototype → pilot → production; revisit when usage, data, or operating conditions change.
- **Why:** Separate a successful demonstration from the conditions required for reliable everyday work.
- **Use when:** Review production readiness, handover conditions, operational gaps, or an unsupported capability claim.
- **Deliver:** An evidence-backed gap backlog and scoped readiness recommendation for the actual project decision process.

## Inputs / 入力

- Prototype behavior and the actual intended production workflow.
- Known data, runtime, permissions, evaluation evidence, and user interfaces.
- Expected usage, operational ownership, and current capability documentation.
- Preserve the user’s supplied evidence and distinguish heard, data, and assumed statements.
- Ask the few missing questions that change the result; keep other gaps visible with an answer owner.

## Method / 進め方

- **1.** State fairly what the prototype already demonstrates; avoid dismissing the customer’s work.
- **2.** Review runtime access/audit/data location; source freshness and shared meaning; agent/workflow behavior and evaluations; the user’s working interface; maintenance and ownership.
- **3.** For each gap, distinguish verified platform capability, customer-specific build work, and an agreement needed before launch.
- **4.** Attach evidence or an explicit verification task to every platform capability claim; training slides are not a current capability guarantee.
- **5.** Prioritize gaps by the failure consequence for the intended workflow; identify the next log, test, or end-to-end demonstration.
- **6.** Create a readiness backlog with owners and closure criteria; leave launch authorization to the actual project process.

## Knowledge to use / 判断の根拠

- [Distilled method and decision criteria](../reference/fde/methods/readiness-and-positioning.md).
- [Operating guide](../reference/fde/production-readiness/index.md).
- [Detection questions and failure patterns](../reference/fde/production-readiness/failure-patterns.md).
- [Output worksheet](../reference/fde/production-readiness/worksheet.md).
- Use these digested references for operational guidance.
- Converted slide and note archives are background material, not the task instructions or default retrieval context.

## Check before handoff / 引き継ぎ確認

- Each readiness claim has evidence or an explicit unknown.
- Customer-specific work is distinguished from platform behavior.
- Operational ownership extends beyond go-live.
- Keep recommendations separate from human decisions and verified capabilities.
- Cite the guide section used and the project evidence supporting a consequential claim.
- Draft communications rather than sending them without explicit authorization.
- Reply in the user’s language; preserve domain terms.
