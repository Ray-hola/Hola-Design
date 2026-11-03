# Publication privacy and rights review

Reviewed: 2026-11-02. Scope: the fresh source snapshot published as Hola-Design,
including all four skills, tests, maintenance files and final README assets.
The replacement repository starts with new history. Earlier commits, pull requests,
task journals, browser captures and discarded studies are not imported.

## Privacy findings and treatment

- Gitleaks 8.30.1 reported no findings in the original working tree or reachable
  local Git history. Its official release archive was checked against the published
  SHA-256 checksum before execution. The prepared snapshot is scanned separately.
- Additional text checks covered private keys, common credential formats,
  authenticated URLs, machine home paths, private addresses and personal contact
  details. No actual credential or personal contact detail was identified.
- Path and token-like matches in the upstream catalogs were inspected. They are
  fictitious bad-code examples or ordinary Task-based API documentation, not an
  author's machine path or API key. They remain under the recorded upstream hashes.
- Browser screenshots, session metadata, task-specific review journals, abandoned
  cover directions and commit maps stay in a local recovery backup. They are not
  part of the fresh publication. Ignore rules also exclude future task evidence.
- Public author attribution and upstream copyright holders are retained. Removing
  them would impair provenance rather than protect a secret.

The scene skills and generated consumer workflow now explicitly state that packaging
copies profile/evidence values, artifacts and any supplied journal without
anonymization. Local packaging or a design LOOP PASS does not clear that output
for public sharing or confer source rights.

The scanner is a bounded check, not proof that every possible secret format or
piece of personal information has been recognized. Source inputs supplied to a
future task need their own privacy review before distribution.

## Rights inventory

| Material | Basis and verification | Distribution treatment |
| --- | --- | --- |
| Project workflow, questions, helpers and starter assets | Project-authored expression; general design ideas are distinguished from copied expression | Apache-2.0, with project NOTICE; no claim that every AI-assisted element independently qualifies for copyright |
| Ten agent-skills extraction scripts | Nathan Onn, MIT; each local file matches a blob in pinned commit `37d7f0fbc9d792a8a3ab0ac2f78f318b2922375e` | Full upstream MIT license, attribution and [per-file manifest](../skills/web-design-distill/UPSTREAM.json) retained |
| UI UX Pro Max code and catalog | Next Level Builder, MIT, pinned commit `28b3b8dee8c976df4fa3e94aed4e092ad43fcb03` | Both copies retain LICENSE and 44-entry provenance manifests; one English label normalization remains explicitly documented |
| Impeccable method lessons | Paul Bakaus and contributors, Apache-2.0, pinned commit `e89e3ada3e875a89ac2c5d33d11e65ebef6fe285` | Project summaries with source locators, limitations and attribution; upstream code, assets and full documents are not bundled |
| Presentation corpus lessons and related PPT recipe cards | Project-authored generalizations from a private set of 34 presentations, some marked internal by their collector; the sources were not published or licensed for redistribution | Own-words relationships only, without source titles, names, organizations, figures, logos, page images or files; learning remains UNVERIFIED as recorded in the [corpus status](../skills/ppt-design-distill/references/lessons/presentation-corpus-status.json), separate from publication scope |
| Cover woodcut | Wellcome Collection, work `zzxxubww`, image `V0025466EL`; catalogue API identifies the full IIIF image as Public Domain Mark | Original image and credit/source record retained; cover crop and one-ink rendering are documented |
| Inter Tight and other linked font families | Inter Tight's upstream OFL checked; font software is referenced by URL rather than bundled | No font binaries distributed; the rasterized cover is separate from font software |
| General design principles and other method references | Short project review questions and conditional mechanism summaries, rather than book excerpts or chapter indexes | No reference books, chapter lists, page images, copied award entries or unlicensed interface screenshots in this snapshot |

The pinned MIT license files were read from the upstream repositories and compared
byte-for-byte with the bundled copies. Agent-skills script blobs were matched to
the pinned upstream tree. UI UX Pro Max local bytes are verified against their
manifests; those manifests preserve the recorded upstream hashes and local change.
The cover source image retains its SHA-256 in [SOURCE.md](../assets/readme/cover-source/SOURCE.md).

## Authoritative references

- [Agent-skills license at the pinned commit](https://github.com/nathanonn/agent-skills/blob/37d7f0fbc9d792a8a3ab0ac2f78f318b2922375e/LICENSE).
- [UI UX Pro Max license at the pinned commit](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/28b3b8dee8c976df4fa3e94aed4e092ad43fcb03/LICENSE).
- [Impeccable license at the pinned commit](https://github.com/pbakaus/impeccable/blob/e89e3ada3e875a89ac2c5d33d11e65ebef6fe285/LICENSE).
- [Wellcome catalogue, including image items](https://api.wellcomecollection.org/catalogue/v2/works/zzxxubww?include=items).
- [Inter Tight OFL](https://github.com/google/fonts/blob/main/ofl/intertight/OFL.txt) and
  [the OFL FAQ on using fonts in graphics](https://openfontlicense.org/ofl-faq/).
- [U.S. Copyright Office Circular 33](https://www.copyright.gov/circs/circ33.pdf)
  distinguishes ideas, methods and systems from their particular expression.

## Assessment and remaining limits

No unresolved obvious privacy exposure or missing license for bundled third-party
files was identified within this publication scope after the changes above.
Rephrasing alone is not permission to reproduce protected expression; source
selection and arrangement can also matter. New sources require a fresh assessment.

The woodcut status records the institution's Public Domain Mark assessment. Its
worldwide term, authorship and every jurisdiction's treatment were not independently
determined. Method summaries and catalog references imply neither endorsement nor
ownership of third-party brands, linked sites or fonts. This is a repository-level
engineering and provenance review, not a legal opinion or a worldwide
non-infringement guarantee.

## Repeat before publishing

Run `python3 scripts/check_repository.py` and the tests described in
[CONTRIBUTING.md](../CONTRIBUTING.md). For a release or a changed source set, also
run a maintained secret scanner on the exact source tree and Git history that will
be pushed. Recheck new licenses, any local changes and new binary assets. Keep
actual task evidence local and publish only materials with a documented basis.
