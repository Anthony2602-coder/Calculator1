# CalcPro Calculator

Beautiful offline calculator — **Django**, **Python**, **HTML**, **CSS**, **JavaScript**.  
Works on **iOS**, **Android**, and as an **offline installable APK**.

## Features

- Modern glassmorphism UI with gradient accents
- Standard + scientific modes
- Fully offline (PWA + APK)
- Free Android APK install (no Play Store fee)
- Public deploy via GitHub + Netlify

## Run locally

```powershell
cd calculator
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python generate_icons.py
python manage.py runserver
```

Open: http://127.0.0.1:8000

---

## Deploy to GitHub

```powershell
git init
git add .
git commit -m "CalcPro calculator app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/calcpro.git
git push -u origin main
```

---

## Deploy to public domain (Netlify — FREE)

### 1. Push code to GitHub (above)

### 2. Create Netlify site
1. Go to [netlify.com](https://netlify.com) → Sign up with GitHub
2. **Add new site → Import an existing project**
3. Select your repo
4. Build settings (auto from `netlify.toml`):
   - **Build command:** `python build_web.py`
   - **Publish directory:** `dist`
5. Click **Deploy**

### 3. Get your public URL
Netlify gives you: `https://random-name.netlify.app`

Rename it: **Site settings → Domain management → Edit site name**  
Example: `https://calcpro-app.netlify.app`

### 4. Build & publish APK
1. GitHub → **Actions** → **Build Android APK** → **Run workflow**
2. Wait for green checkmark (~5–10 min)
3. Netlify auto-redeploys with APK included

### 5. Install on Android
Open: `https://YOUR-SITE.netlify.app/install.html`  
Tap **Download APK** → Install

### 6. Install on iPhone
Safari → open your site → Share → **Add to Home Screen**

---

## Project structure

```
calculator/
├── calc/              # Django app
├── config/            # Django settings
├── static/            # CSS, JS, icons
├── app/               # Capacitor web bundle
├── dist/              # Netlify publish folder
├── release-assets/    # calculator.apk (from GitHub Actions)
├── build_web.py       # Builds dist + app
└── netlify.toml       # Netlify config
```

## Custom domain (optional)

Netlify → **Domain settings → Add custom domain**  
Example: `calcpro.yourdomain.com`

---

See **[DEPLOY.md](DEPLOY.md)** for detailed step-by-step guide.
