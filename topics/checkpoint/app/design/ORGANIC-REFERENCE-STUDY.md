# Organic emotion family — reference study and current direction

## What the user asked to change

The emotion library should feel natural, wholesome and cohesive, with considered composition. The previous library was visibly inconsistent: it mixed a line, an angular scribble, a punctuation symbol and geometric faces. This iteration uses a common organic character language while keeping differences in posture and expression.

## References actually inspected

1. [Arash — Character Development / Ding Blobs](https://dribbble.com/shots/25206701-Character-Development-Ding-Blobs). The creator's displayed illustration uses soft, asymmetric forms and consistent facial line weight. Transferable principle: a small, shared expression vocabulary can unite varied silhouettes. We did not reuse its characters, sparkles, layout or artwork as app assets.
2. [Headspace — Nexus Studios case study](https://nexusstudios.com/work/headspace-case-study/). The primary studio describes characterful animation and simple visual analogies. Transferable principle: expression and posture should carry meaning within a consistent visual world. This is design reference material, not recognition-validation evidence.
3. [Headspace — BUCK](https://buck.co/work/headspace). The full page timed out; the publicly indexed still was downloaded and visually inspected. Its forms share a grounded composition and common facial treatment. Transferable principle: common baselines, proportions and material treatment help a set feel collected.
4. [Pinterest discovery preview](https://www.pinterest.com/pin/24840235438401762/). Pinterest search/pin pages were inaccessible to the browsing tool. A publicly available image preview was inspected through its indexed image URL. The exact author of that pinned image was not verified; it is not attributed to a particular studio or included as product artwork.

Downloaded reference images are local study material in `design/references/`. They are not loaded by the app or included in the review bundle. The reference URLs and observations are supplied so the source work can be assessed directly.

## Direction selected

Organic flat characters fit the native app: they remain editable, draw with bounded vector geometry, and support restrained motion. A dimensional clay direction would need a different rendering pipeline; an ink-only direction would retain the sparse icon feeling the user wants to change. This iteration develops the organic flat direction without redesigning unrelated product functions.

The original character family uses:

- Rounded, slightly uneven silhouettes with optical weight kept similar across the set.
- One dark green face ink and a related palette of muted sage, clay, ochre, lilac and blue.
- Shared face proportions and line treatment. Negative feelings retain tense or downturned expressions.
- A common contact shadow and baseline, with variation in height, lean and compression.
- Smooth breathing with a longer exhale, quiet weight shifts and a brief anticipation before excitement lifts. No decorative rays, particle spray or flashing.
- A static, empty organic outline for an unreported/mixed state, with no assumed emotion or neutral coordinates.

## Meaning and trade-offs

The palette is art direction, not a valence/activation scale. The player's word selects the character; pleasantness and activation remain separate user-reported CMA values below it. CMA does not prescribe these silhouettes. Existing slider suggestions are adjustable design defaults, not measured norms.

A stronger family resemblance can make nearby meanings harder to separate. Frustrated/angry and confused/bewildered remain priority pairs for an unlabelled recognition study. Greater perceived warmth, naturalness, recognisability and frustration reduction have not been established with players. Keep labels and reduced-motion versions, and revise or merge a distinction if players cannot read it.

The eight-word vocabulary, cancellation, privacy, manual mode, explicit source selection and classifier isolation remain in the native app. No new facial-model training or production-readiness claim is part of this visual revision.

## Current review assets

- `artifacts/organic-emotion-library.png`
- `artifacts/organic-emotion-ui.png`
- `artifacts/organic-emotion-ui-dark.png`
- `artifacts/organic-emotion-dialog.png`
- `artifacts/organic-emotion-checkin.png`
- `artifacts/organic-emotion-unreported.png`
- `artifacts/organic-emotion-motion.mp4`
- Figma page **10 Organic emotion family**: https://www.figma.com/design/Rj3WAO6IpUb48OFUerY7aW?node-id=98-87

Regenerate the current native assets with `python -m scripts.render_organic --video` (ffmpeg is required for the MP4). Prior review assets and Figma pages are preserved for comparison.
