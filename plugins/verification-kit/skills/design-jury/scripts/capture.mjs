#!/usr/bin/env node
// Render contract producer for the web medium: what a design-jury judge is allowed to see.
// Drives installed Chrome over the DevTools protocol (Node 22+, no npm packages), the same
// way site-review's screenshot.mjs does. That script takes one tall full-page PNG; award
// sites reveal content on scroll and run their own smooth-scroll, so a tall capture shows
// dimmed or unrevealed sections. This one scrolls with real wheel events and captures one
// viewport-sized frame per step, at desktop and mobile widths.
//
// Usage: node capture.mjs <url-or-file> <out-dir> [max-frames]
//   max-frames  per viewport, default 8
//
// Writes:
//   <out-dir>/desktop/frame-NN.png, <out-dir>/mobile/frame-NN.png   viewport frames, top down
//   <out-dir>/text.md                                               extracted page text
//   <out-dir>/manifest.json                                         frames, probe, failures, not-observed list
// Exits 1 when a viewport produced no frames or navigation failed, 2 on bad input. At the
// 480 s deadline it writes what it has; manifest.json `failures` then says the capture is
// partial, and the exit is 0 only if both viewports have frames.

import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const [target, outDir, maxArg = "8"] = process.argv.slice(2);
if (!target || !outDir) {
  console.error("usage: node capture.mjs <url-or-file> <out-dir> [max-frames]");
  process.exit(2);
}
let url = target;
if (!/^(https?|file):\/\//.test(target)) {
  if (!fs.existsSync(target)) {
    console.error(`STOP: ${target} is neither a URL nor a file`);
    process.exit(2);
  }
  url = "file://" + path.resolve(target);
}
const maxFrames = Number(maxArg);
if (!Number.isInteger(maxFrames) || maxFrames < 1 || maxFrames > 30) {
  console.error(`STOP: max-frames must be an integer from 1 to 30, got ${maxArg}`);
  process.exit(2);
}

const VIEWPORTS = [
  { name: "desktop", width: 1440, height: 900, mobile: false },
  { name: "mobile", width: 390, height: 844, mobile: true },
];
const SETTLE_MS = 3500; // intro loaders on award sites commonly run 2 to 3 s
const STEP_MS = 1400;   // smooth-scroll easing plus reveal transitions
// A frame whose PNG is under this many bytes per 1000 pixels is almost one flat colour:
// a blank or black capture, or a deliberate solid section. Heuristic, flagged not failed.
const BLANK_BYTES_PER_KPX = 12;

const chromePath = [
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome",
  "/usr/bin/chromium",
].find((p) => fs.existsSync(p));
if (!chromePath) {
  console.error("STOP: no Chrome or Chromium found");
  process.exit(2);
}

fs.mkdirSync(outDir, { recursive: true });
const profile = fs.mkdtempSync(path.join(os.tmpdir(), "jury-"));
const chrome = spawn(chromePath, [
  "--headless=new", "--remote-debugging-port=0", `--user-data-dir=${profile}`,
  "--no-first-run", "--no-default-browser-check", "--hide-scrollbars",
  "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "about:blank",
], { stdio: ["ignore", "ignore", "pipe"] });

function cleanup() {
  try { chrome.kill("SIGKILL"); } catch {}
  try { fs.rmSync(profile, { recursive: true, force: true }); } catch {}
}
// Heavy WebGL under software GL can take minutes per viewport. At the deadline, keep what
// was captured: write a partial manifest (its failures say so) and exit 0 when both
// viewports have at least one frame, 1 otherwise.
let manifest = null;
const deadline = setTimeout(() => {
  console.error("FAIL: deadline of 480 s reached; writing a partial capture");
  let usable = false;
  if (manifest) {
    manifest.failures.push("deadline of 480 s reached: capture is partial");
    writeOutputs();
    usable = VIEWPORTS.every((vp) => manifest.viewports[vp.name]?.frames.length > 0);
  }
  cleanup();
  process.exit(usable ? 0 : 1);
}, 480_000);

function writeOutputs() {
  if (manifest.probe?.body_text !== undefined) {
    const p = manifest.probe;
    fs.writeFileSync(path.join(outDir, "text.md"),
      `# Extracted text: ${p.title}\n\nSource: ${url}\n\n## Outline\n\n${p.outline.map((o) => "- " + o).join("\n")}\n\n` +
      `## Navigation\n\n${p.nav_links.join(" | ")}\n\n## Body text (first 6000 characters)\n\n${p.body_text}\n`);
    delete manifest.probe.body_text;
  }
  fs.writeFileSync(path.join(outDir, "manifest.json"), JSON.stringify(manifest, null, 2));
  console.log(`wrote ${path.join(outDir, "manifest.json")}`);
}

const browserWs = await new Promise((resolve, reject) => {
  let buf = "";
  chrome.stderr.on("data", (d) => {
    buf += d;
    const m = buf.match(/DevTools listening on (ws:\/\/\S+)/);
    if (m) resolve(m[1]);
  });
  chrome.on("exit", () => reject(new Error("Chrome exited before DevTools came up")));
});
const port = new URL(browserWs).port;
const pages = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
const page = pages.find((p) => p.type === "page");

const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let nextId = 0;
const pending = new Map();
const waiters = [];
const pageErrors = [];
ws.addEventListener("message", (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.id && pending.has(msg.id)) {
    const { resolve, reject } = pending.get(msg.id);
    pending.delete(msg.id);
    msg.error ? reject(new Error(msg.error.message)) : resolve(msg.result);
  } else if (msg.method) {
    if (msg.method === "Runtime.exceptionThrown") {
      pageErrors.push(msg.params.exceptionDetails?.exception?.description?.split("\n")[0]
        ?? msg.params.exceptionDetails?.text ?? "exception");
    }
    for (const w of waiters.filter((w) => w.method === msg.method)) {
      waiters.splice(waiters.indexOf(w), 1);
      w.resolve(msg.params);
    }
  }
});
const send = (method, params = {}) => new Promise((resolve, reject) => {
  const id = ++nextId;
  pending.set(id, { resolve, reject });
  ws.send(JSON.stringify({ id, method, params }));
});
const once = (method) => new Promise((resolve) => waiters.push({ method, resolve }));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const evaluate = async (expression) =>
  (await send("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true })).result.value;

const PROBE = `(() => {
  const q = (s) => Array.from(document.querySelectorAll(s));
  const txt = (e) => (e.innerText || e.textContent || "").replace(/\\s+/g, " ").trim();
  const ff = (e) => e ? getComputedStyle(e).fontFamily : null;
  const libs = {
    gsap: !!window.gsap, three: !!window.THREE, lenis: !!(window.lenis || window.Lenis) ||
      document.documentElement.className.includes("lenis"),
    locomotive: !!window.LocomotiveScroll || !!document.querySelector("[data-scroll-container]"),
    barba: !!window.barba, swup: !!window.swup, framer: !!document.querySelector("[data-framer-name]"),
    webflow: !!window.Webflow,
  };
  const body = document.body ? txt(document.body) : "";
  const res = performance.getEntriesByType("resource");
  const nav = performance.getEntriesByType("navigation")[0];
  return {
    title: document.title,
    description: document.querySelector('meta[name="description"]')?.content ?? null,
    lang: document.documentElement.lang || null,
    outline: q("h1,h2,h3").slice(0, 40).map((h) => h.tagName + ": " + txt(h).slice(0, 120)),
    nav_links: q("nav a, header a").slice(0, 25).map((a) => txt(a).slice(0, 60)).filter(Boolean),
    word_count: body ? body.split(" ").length : 0,
    images: q("img").length,
    images_missing_alt: q("img:not([alt])").length,
    fonts: { h1: ff(document.querySelector("h1")), body: ff(document.body),
             p: ff(document.querySelector("p")),
             loaded: Array.from(new Set(Array.from(document.fonts).filter((f) => f.status === "loaded").map((f) => f.family))) },
    motion: {
      running_animations: document.getAnimations().length,
      canvases: q("canvas").length, videos: q("video").length,
      custom_cursor: getComputedStyle(document.body).cursor === "none" ||
        !!document.querySelector('[class*="cursor" i]'),
      libraries: Object.keys(libs).filter((k) => libs[k]),
    },
    weight: { requests: res.length,
      transfer_kb: Math.round(res.reduce((s, r) => s + (r.transferSize || 0), 0) / 1024),
      load_ms: nav ? Math.round(nav.loadEventEnd) : null },
    body_text: body.slice(0, 6000),
  };
})()`;

// The single visible control whose whole label is an entry word. More than one
// candidate means it is ordinary navigation, not a gate, so nothing is pressed.
const ENTRY_GATE = `(() => {
  const words = /^(start|enter|enter site|explore|begin|let's go|discover|sound on|sound off|with sound|without sound|skip intro|continue)$/i;
  const hits = Array.from(document.querySelectorAll("button, a, [role=button], div, span"))
    .filter((e) => words.test((e.innerText || "").trim()) && e.children.length <= 2)
    .map((e) => ({ e, r: e.getBoundingClientRect() }))
    .filter(({ r }) => r.width > 0 && r.height > 0 && r.top >= 0 && r.bottom <= innerHeight);
  const labels = new Set(hits.map(({ e }) => e.innerText.trim().toLowerCase()));
  if (hits.length === 0 || labels.size > 1) return null;
  const { e, r } = hits[hits.length - 1];
  return { text: e.innerText.trim(), x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2) };
})()`;

// No clip: a clip is in page coordinates, so a fixed { y: 0 } clip after scrolling
// captures the unpainted region above the viewport and comes back blank (2026-10-03).
async function captureFrame(file, width, height) {
  const shot = await send("Page.captureScreenshot", { format: "png" });
  const buf = Buffer.from(shot.data, "base64");
  fs.writeFileSync(file, buf);
  const suspectBlank = buf.length < BLANK_BYTES_PER_KPX * (width * height) / 1000;
  return { data: shot.data, bytes: buf.length, suspectBlank };
}

await send("Page.enable");
await send("Runtime.enable");
manifest = {
  manifest: "design-jury-capture/v1",
  target: url,
  captured_at: new Date().toISOString(),
  viewports: {},
  ambient_motion: null,
  probe: null,
  page_errors: pageErrors,
  failures: [],
  not_observed: [
    "hover and cursor-follow effects",
    "click interactions and page transitions between routes",
    "sound",
    "real-device performance and scroll smoothness (headless, software GL)",
    "prefers-reduced-motion behaviour",
  ],
};
let failed = false;

for (const vp of VIEWPORTS) {
  const dir = path.join(outDir, vp.name);
  fs.mkdirSync(dir, { recursive: true });
  const record = { width: vp.width, height: vp.height, frames: [], stopped: null };
  manifest.viewports[vp.name] = record;
  try {
    await send("Emulation.setDeviceMetricsOverride",
      { width: vp.width, height: vp.height, deviceScaleFactor: 1, mobile: vp.mobile });
    const loaded = once("Page.loadEventFired");
    const nav = await send("Page.navigate", { url });
    if (nav.errorText) throw new Error(`navigation failed: ${nav.errorText}`);
    await Promise.race([loaded, sleep(30_000)]);
    await sleep(SETTLE_MS);

    // Entry gate: a lone "Start" / "Enter" control a visitor must press before the site
    // shows anything. Press it once, as a visitor would, and record that it was there.
    const gate = await evaluate(ENTRY_GATE);
    if (gate) {
      await send("Input.dispatchMouseEvent", { type: "mousePressed", x: gate.x, y: gate.y, button: "left", clickCount: 1 });
      await send("Input.dispatchMouseEvent", { type: "mouseReleased", x: gate.x, y: gate.y, button: "left", clickCount: 1 });
      record.entry_gate = gate.text;
      await sleep(SETTLE_MS);
    }

    // Layout tiles: the full-page render cut into viewport-height tiles at full
    // resolution, before any scrolling. Robust where scroll-driven rendering is not
    // (a headless page can leave scrolled sections blank), but shows content in its
    // pre-reveal state.
    const pageH = Math.min(await evaluate(
      "Math.max(document.documentElement.scrollHeight, document.body ? document.body.scrollHeight : 0)"), 16000);
    record.page_height = pageH;
    record.tiles = [];
    const tileDir = path.join(outDir, `${vp.name}-tiles`);
    fs.mkdirSync(tileDir, { recursive: true });
    for (let k = 0; k * vp.height < pageH && k < maxFrames; k++) {
      const file = path.join(tileDir, `tile-${String(k).padStart(2, "0")}.png`);
      const shot = await send("Page.captureScreenshot", {
        format: "png", captureBeyondViewport: true,
        clip: { x: 0, y: k * vp.height, width: vp.width, height: Math.min(vp.height, pageH - k * vp.height), scale: 1 },
      });
      const buf = Buffer.from(shot.data, "base64");
      fs.writeFileSync(file, buf);
      record.tiles.push({ file: path.relative(outDir, file), y: k * vp.height,
        suspect_blank: buf.length < BLANK_BYTES_PER_KPX * (vp.width * vp.height) / 1000 });
      console.log(`wrote ${file}`);
    }
    await send("Emulation.setDeviceMetricsOverride",
      { width: vp.width, height: vp.height, deviceScaleFactor: 1, mobile: vp.mobile });
    if (vp.name === "desktop") manifest.probe = await evaluate(PROBE);

    let prev = null;
    for (let i = 0; i < maxFrames; i++) {
      const file = path.join(dir, `frame-${String(i).padStart(2, "0")}.png`);
      if (i === 0 && vp.name === "desktop") {
        // Ambient motion: does the first viewport change with no input at all?
        const a = await captureFrame(file, vp.width, vp.height);
        await sleep(800);
        const b = await captureFrame(file, vp.width, vp.height);
        manifest.ambient_motion = a.data !== b.data;
      }
      let f = await captureFrame(file, vp.width, vp.height);
      // The first frame can land mid-transition (after an entry gate or a loader).
      for (let w = 0; i === 0 && f.suspectBlank && w < 6; w++) {
        await sleep(1000);
        f = await captureFrame(file, vp.width, vp.height);
      }
      const y = await evaluate("Math.round(window.scrollY)");
      // A dark spacer section repeats an identical frame mid-page, so identity only ends
      // the run when the scroll position also stayed put.
      if (prev !== null && f.data === prev && y === record.frames.at(-1).scrollY) {
        fs.rmSync(file);
        record.stopped = "frame identical to previous: end of page, or scrolling is blocked";
        break;
      }
      const scrollY = y;
      // Page pixels between the bottom of the previous frame and the top of this one that
      // no frame shows. 0 when frames overlap or touch; recorded so a gap is never silent.
      const last = record.frames.at(-1);
      const gap = last ? Math.max(0, scrollY - last.scrollY - vp.height) : 0;
      record.frames.push({ file: path.relative(outDir, file), scrollY, gap_before_px: gap,
        bytes: f.bytes, suspect_blank: f.suspectBlank });
      console.log(`wrote ${file}${f.suspectBlank ? " (suspect blank)" : ""}`);
      prev = f.data;
      // Smooth-scroll libraries (Lenis and kin) damp one large wheel event to a few
      // dozen pixels, so scroll the way a trackpad does: small ticks, checking after each
      // one, until the page has moved about 80% of a viewport. Checking only every fifth
      // 120 px tick overshot to 1,200 px and left 300 to 356 px of every step unseen
      // (found by an independent review, 2026-10-04).
      // On a virtual-scroll scene scrollY never moves; stop after twenty ticks, which has
      // advanced the scene, instead of spending all eighty.
      const step = Math.round(vp.height * 0.8);
      const goal = scrollY + step;
      for (let t = 0; t < 80; t++) {
        await send("Input.dispatchMouseEvent", {
          type: "mouseWheel", x: vp.width / 2, y: vp.height / 2, deltaX: 0, deltaY: 60,
        });
        await sleep(30);
        const now = await evaluate("Math.round(window.scrollY)");
        if (now >= goal || (t >= 19 && now === scrollY)) break;
      }
      await sleep(STEP_MS);
      // Smooth scrolling keeps coasting after the last tick. If it carried the page past
      // a full viewport, pull it back to the step so the next frame overlaps this one.
      if (await evaluate("Math.round(window.scrollY)") > scrollY + vp.height - 40) {
        await evaluate(`window.scrollTo(0, ${goal})`);
        await sleep(800);
      }
      // If the wheel did not move the document, try scrollBy too. Never stop on scroll
      // position alone: WebGL and virtual-scroll sites move a scene on wheel input while
      // scrollY stays 0 (two Sites of the Day were cut to their intro that way,
      // 2026-10-03). The identical-frame check above ends truly static pages.
      if (await evaluate("Math.round(window.scrollY)") === scrollY) {
        await evaluate(`window.scrollBy(0, ${Math.round(vp.height * 0.85)})`);
        await sleep(800);
      }
    }
    if (!record.stopped) record.stopped = `max-frames (${maxFrames}) reached`;
  } catch (err) {
    manifest.failures.push(`${vp.name}: ${err.message}`);
    console.error(`FAIL ${vp.name}: ${err.message}`);
  }
  if (record.frames.length === 0) failed = true;
}

writeOutputs();

// Chrome can drop the socket before answering Browser.close; never wait on it for long.
try { await Promise.race([send("Browser.close"), sleep(2000)]); } catch {}
ws.close();
clearTimeout(deadline);
cleanup();
if (failed) console.error("FAIL: a viewport produced no frames; see manifest.json failures");
// Exit explicitly: Chrome's helper processes can hold the stderr pipe open after the main
// process is killed, which keeps Node alive indefinitely (seen 2026-10-03 and 10-04).
process.exit(failed ? 1 : 0);
