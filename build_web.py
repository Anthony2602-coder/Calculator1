"""Build static site for Netlify + Capacitor."""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
APP = ROOT / "app"
VERIFY = ROOT / "scripts" / "verify_apk.py"

INDEX = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="theme-color" content="#6366f1">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-title" content="CalcPro">
  <title>CalcPro</title>
  <link rel="manifest" href="/manifest.json">
  <link rel="icon" href="/icons/icon-192.png">
  <link rel="apple-touch-icon" href="/icons/icon-192.png">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <div class="bg-glow"></div>
  <main class="shell">
    <header class="top">
      <div class="brand"><span class="brand-dot"></span><h1>CalcPro</h1></div>
      <button type="button" id="modeBtn" class="chip">Standard</button>
    </header>
    <section class="calc-card" aria-label="Calculator">
      <div class="display"><p id="expr" class="expr"></p><p id="result" class="result">0</p></div>
      <div id="sciPad" class="grid sci hidden">
        <button type="button" data-fn="sin">sin</button><button type="button" data-fn="cos">cos</button>
        <button type="button" data-fn="tan">tan</button><button type="button" data-fn="log">log</button>
        <button type="button" data-fn="sqrt">√</button><button type="button" data-const="pi">π</button>
        <button type="button" data-const="e">e</button><button type="button" data-op="^">xʸ</button>
      </div>
      <div class="grid keys">
        <button type="button" class="key fn" data-action="clear">AC</button>
        <button type="button" class="key fn" data-action="sign">±</button>
        <button type="button" class="key fn" data-action="percent">%</button>
        <button type="button" class="key op" data-op="/">÷</button>
        <button type="button" class="key" data-num="7">7</button><button type="button" class="key" data-num="8">8</button>
        <button type="button" class="key" data-num="9">9</button><button type="button" class="key op" data-op="*">×</button>
        <button type="button" class="key" data-num="4">4</button><button type="button" class="key" data-num="5">5</button>
        <button type="button" class="key" data-num="6">6</button><button type="button" class="key op" data-op="-">−</button>
        <button type="button" class="key" data-num="1">1</button><button type="button" class="key" data-num="2">2</button>
        <button type="button" class="key" data-num="3">3</button><button type="button" class="key op" data-op="+">+</button>
        <button type="button" class="key wide" data-num="0">0</button><button type="button" class="key" data-action="dot">.</button>
        <button type="button" class="key eq" data-action="equals">=</button>
      </div>
      <button type="button" id="backBtn" class="back" aria-label="Backspace">⌫</button>
    </section>
    <footer class="bottom"><span>Works offline</span><a href="/install.html">Install Android APK</a></footer>
  </main>
  <script src="/js/calculator.js" defer></script><script src="/js/app.js" defer></script>
</body></html>"""

INSTALL = """<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <meta name="theme-color" content="#6366f1"><title>Install CalcPro</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css"><link rel="stylesheet" href="/css/install.css">
</head><body class="install-body"><div class="install-card">
  <img src="/icons/icon-192.png" alt="" class="install-icon">
  <span class="pill">Free · Offline · No Play Store</span>
  <h1>Install CalcPro</h1>
  <p>Download APK and install via Android package installer.</p>
  <button type="button" id="downloadBtn" class="btn-download">Download APK</button>
  <p id="status" class="status">Checking…</p>
  <a id="directLink" class="direct" href="/calculator.apk">Direct: /calculator.apk</a>
  <a class="back-link" href="/">← Back to calculator</a>
  <div class="help"><h2>How to install</h2><ol>
    <li>Tap Download APK</li><li>Files → Downloads → calculator.apk</li>
    <li>Tap Install</li><li>Allow Chrome unknown apps if asked</li>
  </ol></div>
</div><script src="/js/install.js" defer></script></body></html>"""


def verify_apk(path):
    if not path.exists():
        return False
    r = subprocess.run([sys.executable, str(VERIFY), str(path)], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    return r.returncode == 0


def build_dir(target: Path, relative=False):
    subprocess.run([sys.executable, str(ROOT / "generate_icons.py")], check=True)
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    static = ROOT / "static"
    for folder in ("css", "icons", "js"):
        shutil.copytree(static / folder, target / folder)

    manifest = json.loads((static / "manifest.json").read_text())
    prefix = "./" if relative else "/"
    manifest["start_url"] = prefix
    manifest["icons"] = [
        {"src": f"{prefix}icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
        {"src": f"{prefix}icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
    ]
    (target / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    (target / "index.html").write_text(INDEX, encoding="utf-8")
    (target / "install.html").write_text(INSTALL, encoding="utf-8")

    sw = (static / "js" / "sw.js").read_text(encoding="utf-8")
    if relative:
        sw = sw.replace('"/', '"./')
    (target / "js" / "sw.js").write_text(sw, encoding="utf-8")

    apk = ROOT / "release-assets" / "calculator.apk"
    if verify_apk(apk):
        shutil.copy2(apk, target / "calculator.apk")
    else:
        print("WARNING: No valid calculator.apk in release-assets/")


def main():
    build_dir(DIST, relative=False)
    build_dir(APP, relative=True)
    print(f"Built {DIST} and {APP}")


if __name__ == "__main__":
    main()
