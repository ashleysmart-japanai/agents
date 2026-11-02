# Segmentation and Clustering

- **Basis:** authored method guidance; validate suitability against the task evidence.
- **Shared method:** [Analytical evidence and handoff](../methods/evidence-and-handoff.md).

## Inputs

- Entity grain, purpose of segmentation, features, distance meaning, population, and intended use of groups.

## Method

- Choose features that describe the intended grouping rather than convenient identifiers.
- Handle missing values, mixed types, scaling, and redundant features before choosing distance measures.
- Compare clustering choices with a simple interpretable segmentation baseline.
- Assess stability under resampling, seed changes, and plausible preprocessing choices.
- Use internal separation metrics as diagnostics rather than proof of business usefulness.
- Describe group sizes, feature distributions, overlap, and assignment uncertainty.
- Check whether segments remain useful on held-out or later data.
- Avoid presenting unstable clusters as inherent labels for people.
- Document how new observations receive a group and how groups can change.

## Deliverable

- Segment profiles, assignment procedure, stability evidence, actionable distinctions, and limits on interpretation.

## Validation probe

- Rescaling a measurement from metres to centimetres should not silently redefine a standardized distance-based segmentation.
