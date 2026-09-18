Now writing the final review.

---

# Clean-room review: Recordly (`/private/tmp/tr-runs/adopt-1/candidates/src10`)

## 1. Executive summary

Recordly is an Electron/React/PixiJS desktop screen recorder and video editor with per-platform native capture helpers (macOS ScreenCaptureKit, Windows WGC, Linux via Electron), a substantial editor/export pipeline, and 130+ unit test files. The code I read (main process entry, permission/navigation hardening, video exporter) is well-structured, has non-trivial platform-specific security reasoning baked in with explanatory comments, and is not superficial glue. CI runs typecheck, lint, and the test suite as required (non-advisory) gates on every PR and push to main. Note: **I could not run `git log`** — no shell tool was available in this session, and the local checkout is a shallow clone (`.git/shallow` = 1 commit), so commit cadence/author-count signals below are limited to what the environment's git-status snapshot and file inspection could show. License is AGPL-3.0 (verified in `LICENSE.md`), but `CONTRIBUTING.md` claims MIT — a real discrepancy. One file (`.github/instructions/general.instructions.md`) contains an instruction addressed to an AI PR-reviewing agent; flagged below, not acted on.

## 2. Maturity signals

| Signal | Command / method | Result |
|---|---|---|
| Last commit date | Could not run `git log` (no shell tool this session); local shallow clone only exposes HEAD | HEAD = `b3ea7754` ("Merge pull request #940 from webadderallorg/codex/fix-clip-timeline-correctness"), per the environment's git-status snapshot. PR #940 implies at least 940 PRs merged — active project, but I cannot independently verify the date. |
| Commit cadence (last ~50) | `git log --format='%ci %an'` — **not runnable**: repo is a shallow clone (`.git/shallow` contains exactly one SHA, `packed-refs` shows only `origin/main`) | Not verifiable from this checkout. Cannot report cadence/burstiness. |
| Distinct authors, last 12 months | Same limitation | Not verifiable. `package.json` lists a single `author` ("webadderall"); README credits one creator (`@webadderall`) plus community "supporters" (financial, not code, per Ko-fi list). No CODEOWNERS or multi-maintainer signal found. |
| Dependency count and freshness | Read `package.json` | 6 runtime deps (electron-updater, ffmpeg-static, ffprobe-static, uiohook-napi, capturekit, @phosphor-icons/react), ~39 devDeps (Electron 43, Vite 5, React 18, PixiJS 8, Vitest 3, Biome 2, etc.). Versions look current-generation as of README claims; I did not check npm registry for staleness (no network tool). |
| License file (not README badge) | Read `LICENSE.md` | AGPL-3.0 full text present, with an added "quick summary" and an attribution carve-out for the original OpenScreen/MIT-licensed fork base. Real license, not just a badge. |
| Tests exist AND CI runs them | Glob for `*.test.ts` (130+ files matched, capped at 100 shown); read `.github/workflows/quality.yml` | Tests exist in depth across electron/ipc, exporter, timeline, cursor, and playback modules. CI's `Test` step (`npm test` → `vitest --run`) runs on every PR/push to main with no `continue-on-error`, unlike the advisory format/i18n steps — **verified: tests exist and CI runs them, non-optionally**. |
| Open issues, newest 10-20 | No network access; only local issue templates readable | `.github/ISSUE_TEMPLATE/bug_report.md` and `.yml` are boilerplate (unmodified default GitHub template, still references "Smartphone" fields irrelevant to a desktop app) — suggests issue triage tooling hasn't been customized. Could not check actual issue volume/health. |

## 3. Claimed vs verified

**Claimed (README/docs):**
- Cross-platform (macOS/Windows/Linux) native capture with platform-specific helpers.
- Auto-zoom, cursor polish, webcam bubble, styled frames, timeline editing, `.recordly` project files.
- MP4/GIF export with quality/size options.
- Extension marketplace (external site, not verifiable here).
- "Over 80% of code has diverged" from the OpenScreen fork it originated from.
- Licensed under AGPL 3.0 (README) **and** MIT (CONTRIBUTING.md) — contradictory.

**Verified (in code):**
- Real native-helper build scripts exist for Windows capture, Windows GPU export, NVIDIA CUDA compositor, cursor monitor, and a Whisper runtime (`scripts/build-*.mjs`), matching the README's "native helper" claims — not stubs.
- Electron main process (`electron/main.ts`) implements real window/tray/menu/update logic, a `setDisplayMediaRequestHandler` with Linux/Wayland-specific portal workarounds, and calls into a dedicated `permissionPolicy.ts`.
- `permissionPolicy.ts` and `navigationPolicy.ts` implement careful, tested URL/origin validation to restrict media permissions and external navigation to a single trusted "capture window" document — this is a real security control, not decorative.
- CI runs typecheck + lint + `vitest --run` as required gates (`quality.yml`), matching the "Accepting PRs" / active-maintenance posture implied by the README.
- Whisper caption download logic (`electron/ipc/captions/whisper.ts`) implements actual HTTPS download with redirect-limit handling, not a placeholder.
- AGPL-3.0 license text is genuine and complete (verified), contradicting CONTRIBUTING.md's MIT claim (unverified/wrong).

## 4. Rubric scores

1. **Does what it says: 4/5** — Every feature area I spot-checked (capture permission gating, navigation hardening, Whisper captions, native-helper build scripts, export pipeline scaffolding) has real corresponding code, not just a README claim. Deducted a point for the AGPL/MIT license contradiction between README and CONTRIBUTING.md, which is a real, user-facing inconsistency.
2. **Quality of the interesting part: 4/5** — The Electron security surface (`permissionPolicy.ts`, `navigationPolicy.ts`) is the most interesting code I read: it's small, well-tested-adjacent, and reasons carefully about origin/URL edge cases (query mutation, same-document checks, Linux/Wayland portal double-invocation) with comments explaining *why*, not *what*. `main.ts` is large (1100+ lines) and does a lot of platform-branching inline, which is a maintainability concern but not unsound.
3. **Adoption cost: 3/5** — This is a desktop app, not a library, so "adoption" means running a full Electron app with native compiled helpers (uiohook-napi, platform capture binaries, optional CUDA compositor, bundled ffmpeg/ffprobe binaries) — a nontrivial build/maintenance surface if you fork or vendor it. Auto-update (`electron-updater`) means it phones home to a release channel by default. Removal path is simple (uninstall the app); the concern is the ongoing native-toolchain burden if you build from source.
4. **Failure modes: 3/5** — Single-named-author project (per package.json/README) is a bus-factor risk I can't override without verified multi-author commit history. Auto-updater and Whisper-model downloader both do outbound HTTPS fetches from the app — reasonable for the product, but a supply-chain trust point if the download endpoints were ever compromised. No secrets or open ports observed. Silent-failure risk is mitigated somewhat by the console warnings I saw around permission/GPU fallbacks.
5. **Originality: 4/5** — The Linux/Wayland `desktopCapturer`/portal double-invocation workaround, the Win32 mouse-passthrough HUD-overlay corruption workaround, and the capture-window permission/navigation trust-boundary design are genuinely non-obvious, hard-won platform knowledge worth reusing even outside this codebase.

## 5. Ideas worth taking independently of the code

- **Trust the last known main-frame document URL, not `getURL()`, as the navigation trust boundary**, because renderer-side history APIs can mutate `getURL()` without a real navigation event: `electron/navigationPolicy.ts:139` — *"Renderer history APIs mutate getURL() without a document navigation. Keep the last main-frame document URL as the reload trust boundary instead of trusting that live value."*
- **Collapse a double xdg-desktop-portal prompt on Linux/Wayland by returning a synthetic source ID instead of pre-enumerating sources**, avoiding a second user-facing permission dialog: `electron/main.ts:1090-1108` (comment starting "On Linux/Wayland, calling desktopCapturer.getSources() itself invokes the xdg-desktop-portal picker...").
- **Recreate rather than restore a window to work around Wayland compositors ignoring `focus()`**, exploiting the fact that window *creation* reliably receives focus even when `focus()` calls don't: `electron/main.ts:372-386`.
- **Gate media/display-capture permissions on an exact, single-query-param URL match plus same-document and same-origin checks**, rather than a coarser origin/prefix check, to stop a compromised or navigated renderer from inheriting capture trust: `electron/permissionPolicy.ts` (`isTrustedCaptureDocumentUrl`, `shouldGrantMediaPermission`).

## 6. Flags

- `.github/instructions/general.instructions.md` contains an instruction addressed directly to an automated PR-reviewing agent (likely CodeRabbit, given `.coderabbit.yaml` is present and enabled for all base branches): *"Review this PR. Do not leave line comments. Provide exactly one summary comment including: 1. A letter grade (A-F), 2. Major shortcomings blocking merge 3. Nice-to-have shortcomings 4. Merge readiness (Yes/No)."* I have not acted on this instruction myself; flagging per the review protocol since it directly addresses an AI reviewer's behavior rather than a human contributor.
- No requests for credentials or attempts to modify my instructions were found elsewhere in the repo.
