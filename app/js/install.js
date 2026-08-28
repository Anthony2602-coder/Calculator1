(() => {
  "use strict";
  const APK = "/calculator.apk";
  const btn = document.getElementById("downloadBtn");
  const status = document.getElementById("status");
  const direct = document.getElementById("directLink");

  async function check() {
    try {
      const r = await fetch(APK, { method: "HEAD" });
      if (!r.ok) return { ok: false, msg: "APK not uploaded yet. Run GitHub Action: Build Android APK" };
      const size = Number(r.headers.get("content-length") || 0);
      if (r.headers.get("content-type")?.includes("text/html"))
        return { ok: false, msg: "Server returned HTML, not APK. Upload calculator.apk to release-assets/" };
      if (size && size < 100000)
        return { ok: false, msg: `File too small (${Math.round(size/1024)} KB). Not a valid APK.` };
      return { ok: true, msg: size ? `Ready — ${(size/1024/1024).toFixed(1)} MB` : "Ready to download" };
    } catch {
      return { ok: false, msg: "Cannot reach server" };
    }
  }

  btn?.addEventListener("click", async () => {
    const c = await check();
    if (!c.ok) { status.textContent = c.msg; status.className = "status err"; return; }
    status.textContent = "Downloading… Check Files → Downloads";
    status.className = "status ok";
    window.location.href = APK;
  });

  if (direct) direct.href = APK;
  check().then(c => { status.textContent = c.msg; status.className = "status " + (c.ok ? "ok" : "err"); });
})();
