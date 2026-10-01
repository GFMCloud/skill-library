#!/usr/bin/env node
// Full-resolution, full-page screenshots of one page at several widths, light and dark,
// using installed Chrome over the DevTools protocol and nothing else (no Playwright,
// no npm packages, no image tools; Node 22+ for the built-in WebSocket). The browser
// pane scales its screenshots down; these files are the page's real pixels.
//
// Usage: node screenshot.mjs <url-or-file> <out-dir> [widths]
//   widths  comma-separated CSS pixel widths, default 375,1440
//
// Writes <out-dir>/<width>-<light|dark>.png for every width and both color schemes,
// plus <out-dir>/index.html, a contact sheet of all of them (open it in the browser
// pane). Prints one line per file; exits 1 if any capture failed, 2 on bad input.
//
// Dark is emulated as prefers-color-scheme: dark (Emulation.setEmulatedMedia). A page
// that themes by a class or a stored toggle instead will look the same in both. The
// command-line --screenshot and --force-dark-mode flags are not used: on Chrome 153
// they captured black frames, ignored the dark flag and never exited (2026-10-01).
// Captures stop at 16000 px tall. Widths under 768 are emulated as mobile.

import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const [target, outDir, widthsArg = "375,1440"] = process.argv.slice(2);
if (!target || !outDir) {
  console.error("usage: node screenshot.mjs <url-or-file> <out-dir> [widths]");
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
const widths = widthsArg.split(",").map(Number);
if (widths.some((w) => !Number.isInteger(w) || w < 100)) {
  console.error(`STOP: widths must be integers of at least 100, got ${widthsArg}`);
  process.exit(2);
}

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
const profile = fs.mkdtempSync(path.join(os.tmpdir(), "shot-"));
const chrome = spawn(chromePath, [
  "--headless=new", "--remote-debugging-port=0", `--user-data-dir=${profile}`,
  "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "about:blank",
], { stdio: ["ignore", "ignore", "pipe"] });

function cleanup() {
  try { chrome.kill("SIGKILL"); } catch {}
  try { fs.rmSync(profile, { recursive: true, force: true }); } catch {}
}
const deadline = setTimeout(() => {
  console.error("FAIL: timed out after 120 s");
  cleanup();
  process.exit(1);
}, 120_000);

// Chrome prints "DevTools listening on ws://127.0.0.1:<port>/devtools/browser/<id>".
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
ws.addEventListener("message", (ev) => {
  const msg = JSON.parse(ev.data);
  if (msg.id && pending.has(msg.id)) {
    const { resolve, reject } = pending.get(msg.id);
    pending.delete(msg.id);
    msg.error ? reject(new Error(msg.error.message)) : resolve(msg.result);
  } else if (msg.method) {
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

await send("Page.enable");
let failed = 0;
const figures = [];
for (const width of widths) {
  for (const scheme of ["light", "dark"]) {
    const file = path.join(outDir, `${width}-${scheme}.png`);
    try {
      await send("Emulation.setDeviceMetricsOverride",
        { width, height: 900, deviceScaleFactor: 1, mobile: width < 768 });
      await send("Emulation.setEmulatedMedia",
        { features: [{ name: "prefers-color-scheme", value: scheme }] });
      const loaded = once("Page.loadEventFired");
      const nav = await send("Page.navigate", { url });
      if (nav.errorText) throw new Error(`navigation failed: ${nav.errorText}`);
      await loaded;
      await new Promise((r) => setTimeout(r, 750)); // late fonts and scripts
      const { result } = await send("Runtime.evaluate", {
        expression: "Math.max(document.documentElement.scrollHeight, document.body ? document.body.scrollHeight : 0)",
        returnByValue: true,
      });
      const height = Math.min(Math.max(result.value, 1), 16000);
      const shot = await send("Page.captureScreenshot", {
        format: "png", captureBeyondViewport: true,
        clip: { x: 0, y: 0, width, height, scale: 1 },
      });
      fs.writeFileSync(file, Buffer.from(shot.data, "base64"));
      console.log(`wrote ${file} (${width}x${height}, ${scheme})`);
      figures.push(`<figure><img src="${width}-${scheme}.png" width="${Math.round(width / 2)}"><figcaption>${width} px, ${scheme}</figcaption></figure>`);
    } catch (err) {
      console.error(`MISSING ${file}: ${err.message}`);
      failed++;
    }
  }
}

fs.writeFileSync(path.join(outDir, "index.html"), `<!doctype html><meta charset="utf-8"><title>Screenshots</title>
<style>body{font:14px system-ui;margin:16px;background:#888}figure{display:inline-block;vertical-align:top;margin:8px}figcaption{color:#fff}img{border:1px solid #000;display:block}</style>
<p>${url}, full page, shown at half size</p>
${figures.join("\n")}
`);
console.log(`wrote ${path.join(outDir, "index.html")} (contact sheet)`);

try { await send("Browser.close"); } catch {}
ws.close();
clearTimeout(deadline);
cleanup();
if (failed) {
  console.error(`FAIL: ${failed} capture(s) missing`);
  process.exit(1);
}
