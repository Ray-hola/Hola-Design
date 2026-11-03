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

## Reading rendered results and parser counts

- Check a render before judging it. Without the deck's fonts, a renderer can show
  missing glyphs or a wider substitute, which creates false overflow and collisions.
  Map fonts to a suitable installed family and record that substitution as a limit.
- Compare rendered and declared page counts. LibreOffice's PDF export omitted slides
  marked hidden in the inspected decks. Hidden slides and notes may still hold content.
- Blank-looking pages may be a renderer failure on pasted metafiles or embedded objects.
  Inspect the slide's parts before calling the page unfinished in the source.
- Many real decks draw titles as ordinary text boxes, so a missing title placeholder
  does not mean a missing title. Parsed text counts also omit table cells and charts
  held in graphic frames, so such counts understate density on table-heavy pages.
- For a large set, use numbered contact sheets for sequence and enlarge pages for
  detail. Contact sheets do not establish small-text legibility or exact alignment.
