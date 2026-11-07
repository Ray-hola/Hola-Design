# Motion sampling, reconstruction and comparison

Use for temporal references: entrances, hover/scroll transitions, loaders,
recorded product sequences and animated slide/web/UI studies. Static work does
not need a motion pipeline. Reanimate is an optional, pinned measurement backend;
the existing profile, journal and `loop_tools.py finish` remain authoritative.

## Tools and fidelity contract

`vendor/reanimate/` carries unmodified MIT source at the commit in `UPSTREAM.json`,
including capture, frame extraction, easing, comparison, contact sheets and GPU
analysis. Its license covers its software, not captured assets, fonts or code.
Dependencies and browser/ffmpeg binaries are installed locally, never packaged.

Read the bundled [analysis guide](../../vendor/reanimate/references/analysis.md) for the per-element/property motion
spec and [capture guide](../../vendor/reanimate/references/capture.md) for the selected source type. State the user's
target, destination and fidelity before sampling:

- `motion-faithful`: preserve trigger, sequence, easing, stagger, relative travel
  and layout relationships; evaluate every relevant spec row.
- `pixel-faithful`: also preserve the requested type, styling and assets. The
  strict adapter checks 2% mean, 5% worst-frame and 0.5% resting-frame mismatch.
- Mixed requests: identify the exact cloned region and separate creative additions.
  Extract a declared region before strict comparison; inspect the whole as well.

Use real media times and sampling fps. Start with overview frames to locate the
sequence, then sample fast changes densely enough to inspect their intermediate
states. Mark occlusion, dropped/duplicated frames, compression and source changes.
Do not infer a product trigger or backend from a presentation recording.

## Connect the two inner loops and the outer loop

| Existing loop | Motion work | Decision and return path |
| --- | --- | --- |
| DISTILL inner loop | Capture the actual reference; inspect filmstrips, object identity and intermediate states; write per-element timing/easing/relationships in the existing profile evidence and conditional rules | Wrong or missing observation returns to source sampling; inferred intent stays inferred |
| DESIGN inner loop | Reconstruct the requested fidelity, and apply the learned mechanism to genuinely new content; capture both at comparable settings; inspect sheets and task behavior | An implementation difference returns to the artifact; an intentional creative departure needs a baseline and a reason |
| FEEDBACK outer loop | A distinct task/evaluator tests the consumer skill, using declared source access and actual outcomes | Attribute the defect to extraction tool, learned rule, design output or scope; reopen the responsible journal, repair and check the failure plus relevant neighbors |

A faithful clone is a fidelity test, not the new-content DESIGN task. A comparison
report is measurement evidence, not independent FEEDBACK. The upstream five-round
stopping advice is a bounded backend run: report residuals and continue the
existing adaptive LOOP or record a real blocker; never silently change user limits
or declare the parent loop complete because the backend stopped.

## Commands

Resolve `SKILL_ROOT` to the active scene or generated consumer skill. Optional
runtime: Python 3.9+ launches a pinned Bun 1.4.4 environment. `doctor` verifies a bundled or
installed engine against the pinned source; `--engine` selects an exact match.

```sh
# One-time setup, including Bun when missing, frozen dependencies and Chromium.
# Uses a user cache; does not write inside the installed skill or alter PATH.
python3 "$SKILL_ROOT/scripts/motion_tools.py" setup --allow-browser
python3 "$SKILL_ROOT/scripts/motion_tools.py" doctor --allow-browser

# Local original video: probe, extract a selected interval, then inspect every sheet.
python3 "$SKILL_ROOT/scripts/motion_tools.py" frames -- \
  --in reference.mp4 --probe
python3 "$SKILL_ROOT/scripts/motion_tools.py" frames -- \
  --in reference.mp4 --out motion/ref/frames --fps 25 --start 0:03 --end 0:05
python3 "$SKILL_ROOT/scripts/motion_tools.py" sheet --allow-browser -- \
  filmstrip --frames motion/ref/frames --out motion/ref/sheets

# Reconstruct in the user's existing stack. Capture the clone at the same size,
# fps, duration and trigger; use a fresh directory for every round.
python3 "$SKILL_ROOT/scripts/motion_tools.py" compare --fidelity pixel-faithful -- \
  --ref motion/ref/frames --clone motion/clone-1/frames --out motion/compare-1
python3 "$SKILL_ROOT/scripts/motion_tools.py" sheet --allow-browser -- \
  compare --ref motion/ref/frames --clone motion/clone-1/frames \
  --diff motion/compare-1/diff --out motion/compare-1/sheets --offset 0
```

For permitted browser capture, `capture --allow-browser -- <upstream options>`
uses the pinned capturer. Sheet rendering also requires `--allow-browser` because
the upstream sheet script renders local HTML with Chromium. Otherwise export from the host's permitted browser
tool and use the local-media path. Installation is not permission to import
cookies, attach another debugger, or revisit an origin whose access was denied.
The upstream setup launches its own Chromium; run it only where that backend is
permitted. Neither source scripts nor this guide override host permissions.

The strict adapter refuses existing output directories, missing/nonconsecutive
frames, different counts/fps/dimensions, shifted coverage and mismatched recorded
browser settings. It fixes offset at zero and does not resize frames or blur
differences. Upstream raw comparison exits 0 even for failed metrics; the adapter
reads the report and returns 2 for failed measurement limits. Exit 0 means only
that these measurements fit their limits, never a design or LOOP PASS.

Use identical explicit capture options, including selector/target/track names in
the reference and clone test harness. Capture timestamps and source/output paths
may differ. The strict adapter rejects duplicate options and checks its own
recorded options as well as upstream metadata when both receipts exist. For raw
upstream captures or media exports, settings absent from the metadata still need
manual verification. A selector rename needs a reviewed semantic mapping in a
separate scoped analysis; do not edit metadata merely to make comparison pass.
The adapter rehashes the complete input frame sets after comparison and rejects
inputs that changed during the run. Preserve failed rounds rather than reuse them.

For GPU/particle work read the bundled WebGL reference and inspect trace coverage,
constants, clocks, draw structure and omitted channels. A zero-channel GL comparison
is not proof. Establish a repeat-reference noise floor; a virtual clock/seed does
not prove that workers, network state or server variants are deterministic.

## Bind evidence without inventing acceptance

Keep recordings, frames, per-round outputs and any sensitive URLs outside public
packages. Each `motion-receipt.json` binds the script, source media/frame hashes,
settings and comparison report. After inspecting the actual outputs, register
them through the existing evidence contract:

- Bind an actual plan ID, context, loop and current delivery revision. A source
  frame belongs to its source ID; a clone frame belongs to the rendered artifact.
- Reference the receipt/report and sheets with real file hashes. For visual plan
  items use `method=visual`, `inspection=inspected` only after viewing the sheets;
  for executed interaction/measurement items use their actual method and result.
- Set `coverage_ids`, per-question `observations` and `rendered_from` to the
  tested files. Do not promote `captured_only` or a subprocess success to inspection.
- Evaluate each spec row's identity, trigger, timing, easing, travel and stagger;
  global activity curves cannot prove all of them. Inspect entry, intermediate,
  settled, exit and relevant error/recovery states in the complete composition.
- Use the existing `reopen` and repair attribution before a fix; retain earlier
  failures, current artifact snapshots and relevant regression observations.

Finish with the existing intent, quality, challenge, integrity and convergence
gates and the actual `loop_tools.py finish` result. Motion metrics neither replace
the weakest-subject judgment nor establish usability, source rights or transfer.

## Portable environment contract

Native targets: macOS arm64/x64, Linux glibc arm64/x64 and Windows x64.
Python 3.9+, internet access, a writable user cache and roughly 1 GB free space
are prerequisites. Use `python` on Windows if `python3` is unavailable. Follow
Playwright's current OS requirements; an unsupported OS/CPU is a real blocker,
not an installation success. Windows ARM64 and Linux musl are not claimed.

`setup --allow-browser` downloads missing Bun from fixed official release URLs,
checks the pinned archive SHA-256 and executable version, copies verified source
into the user cache, installs frozen dependencies, explicitly installs ffmpeg,
and installs Chromium. Runtime-only, hash-checked adaptations select `ffmpeg.exe` and valid file URLs
on Windows, and use full Chromium consistently in capture, sheets and the probe;
bundled upstream source is unchanged. It then actually
launches Chromium, decodes an owned screenshot and executes a pixel comparison.
Only a fully successful probe sets `ready=true` and exits 0. `doctor` without
`--allow-browser` leaves browser readiness unprobed and exits 2.

Use `--cache-dir <writable-directory>` to isolate/recover an installation, and
`--download-bun` for a genuine binary download test despite preinstalled Bun.
On supported Linux, add `--with-system-deps` only when apt/root installation is
permitted; otherwise install the named Playwright system libraries through the
host administrator. No setup script bypasses host permissions.

Browser downloads can fail due to network/DNS/proxy restrictions. Preserve the
failed cache and error, configure permitted `HTTPS_PROXY`,
`PLAYWRIGHT_DOWNLOAD_HOST` or `PLAYWRIGHT_DOWNLOAD_CONNECTION_TIMEOUT` per the
platform, then rerun the same command. Do not report a partially installed runtime
as ready or claim that every computer is supported.

Before running helpers, detect Python 3.9+. If it is missing, install it through
the host's permitted native package manager (for example Homebrew, apt or winget),
then run setup; do not treat a missing interpreter as a successful installation.
A read-only/offline host or unavailable OS privileges remains a disclosed blocker.
Git checkout must preserve LF source bytes; this repository's `.gitattributes`
prevents Windows autocrlf from invalidating the pinned provenance hashes.
