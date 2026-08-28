# Full deployment guide — CalcPro

## Overview

| What | Where | Cost |
|------|-------|------|
| Code | GitHub | Free |
| Public website | Netlify | Free |
| Android APK | GitHub Actions builds it | Free |
| Custom domain | Netlify or your registrar | Optional |

---

## STEP 1 — Push to GitHub

```powershell
cd "D:\Users\anthony.rahul_navi\Desktop\draft projects\calculator"
git init
git add .
git commit -m "CalcPro calculator with offline APK"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/calcpro.git
git push -u origin main
```

Create repo on GitHub first (github.com → New repository → name: `calcpro`)

---

## STEP 2 — Deploy public website on Netlify

1. [netlify.com](https://netlify.com) → Sign up → **Sign up with GitHub**
2. **Add new site → Import an existing project → GitHub**
3. Select **calcpro** repo
4. Settings should show:
   - Build: `python build_web.py`
   - Publish: `dist`
5. **Deploy site**
6. Your public URL: `https://something.netlify.app`

### Rename your URL
**Domain management → Options → Edit site name** → e.g. `calcpro-calc`

Final URLs:
- Calculator: `https://calcpro-calc.netlify.app`
- Install APK: `https://calcpro-calc.netlify.app/install.html`

---

## STEP 3 — Build Android APK

1. GitHub repo → **Actions** tab
2. **Build Android APK** → **Run workflow**
3. Wait for green ✓ (~5–10 minutes)
4. GitHub automatically adds `release-assets/calculator.apk`
5. Netlify redeploys automatically

### If APK not appearing — manual upload
1. Actions → completed run → **Artifacts** → download `calculator-apk` ZIP
2. Unzip → get `calculator.apk`
3. GitHub repo → **release-assets/** → Upload files → upload `calculator.apk`
4. Commit → Netlify redeploys

---

## STEP 4 — Install on Android phone

1. Open `https://YOUR-SITE.netlify.app/install.html`
2. Should show **Ready — X.X MB**
3. Tap **Download APK**
4. **Files → Downloads → calculator.apk → Install**
5. If blocked: **Settings → Apps → Chrome → Install unknown apps → Allow**

Works **offline** after install.

---

## STEP 5 — Install on iPhone

1. Open site in **Safari**
2. Tap **Share** → **Add to Home Screen**
3. Works offline as PWA

---

## STEP 6 — Custom domain (optional)

1. Buy domain (Namecheap, GoDaddy, etc.)
2. Netlify → **Domain settings → Add custom domain**
3. Follow DNS instructions
4. HTTPS is automatic

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| APK not on server | Run GitHub Action Build Android APK |
| Problem parsing package | File is not real APK — re-download from Artifacts |
| Netlify build fails | Check build log; ensure Python 3.12 |
| Site not updating | Netlify → Deploys → Trigger deploy |

---

## Share your app

Send friends:
- **Web:** `https://YOUR-SITE.netlify.app`
- **Android install:** `https://YOUR-SITE.netlify.app/install.html`
