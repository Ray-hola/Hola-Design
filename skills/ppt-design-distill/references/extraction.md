# Presentation evidence

For PPTX, run scripts/extract_pptx.py. It reads ZIP members without unpacking or
executing them. Follow presentation.xml relationships for actual order; filenames
are not presentation order. Preserve source SHA-256 and part/shape IDs.

The parser distinguishes theme declarations, master/layout declarations and local
slide geometry. Local coordinates normalized to canvas are useful relationships;
missing local coordinates may inherit from a layout. Do not replace them with 0.
Font and color declarations may be inherited or themed. A theme font is not proof
that every body run renders in it. Inspect representative rendered pages to resolve
claims about actual type and composition. Embedded media counts are not image analysis.

Choose source pages by the requested breadth: cover, different content purposes,
dense and sparse cases, data-heavy and image-heavy pages, and transitions. Review
full order before asserting deck-level narrative. Log omitted page types. This is
purpose-based sampling, not a fixed random page quota.

For PDF or slide images, inspect available pages at known resolution. Record
pixel/ratio estimates as such; distinguish screenshot raster dimensions from the
slide's logical size. Do not infer masters, fonts or animation from a still image.
For multiple decks, keep separate source sets; first find recurring rules and
then record deliberate variations. Shared colors do not prove shared narrative.

If rendering is unavailable, deliver an XML-grounded draft with explicit visual
unknowns. Do not claim a visual gate passed. Creation/editing/rendering can use
available presentation tools; the extractor itself only reads evidence.
