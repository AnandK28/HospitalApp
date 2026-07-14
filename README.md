# Hospital Records App

A KivyMD (Python) app: search patients/diagnoses, view full stay details,
add new records, export to Excel. Data is stored locally on-device in
SQLite (`db.py`), seeded with 3 demo patients on first launch.

## Files
- `main.py` — UI and app logic (search, detail view, add-record form)
- `db.py` — SQLite schema (mirrors your Postgres tables) + Excel export
- `buildozer.spec` — Android build configuration
- `requirements.txt` — for running on desktop first

## 1. Try it on your laptop first (fastest way to see it working)
```bash
pip install -r requirements.txt
python main.py
```
This opens the same UI you'll get on Android — good for checking the
design/logic before spending time on an APK build.

## 2. Building the actual APK — don't use Colab
Colab can run `buildozer`, but its sessions time out (compiling the
Android SDK/NDK toolchain the first time takes 30–60+ min) and it's not
built for interactive Android builds. Use one of these instead:

**Option A — GitHub Actions (recommended, free, no local setup):**
1. Push this folder to a GitHub repo.
2. Add a workflow using the community action
   [`ArtemSBulgakov/buildozer-action`](https://github.com/ArtemSBulgakov/buildozer-action).
   It runs `buildozer -v android debug` on GitHub's Linux runners and
   uploads the resulting `.apk` as a build artifact you download.

**Option B — A real Linux machine (or WSL2 on Windows):**
```bash
pip install buildozer cython
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf \
    libtool pkg-config zlib1g-dev libncurses-dev libffi-dev libssl-dev
buildozer android debug
```
First build takes a while (downloads SDK/NDK); the APK lands in `bin/`.

macOS won't build Android APKs directly with Buildozer — use Option A or a Linux VM.

## Notes / next steps
- This is a **standalone** app — no server needed, data lives in the
  app's private storage on the phone.
- Exported Excel files are saved to the app's private `exports/` folder.
  If you want them to land in the phone's normal Downloads folder (so
  they show up in a file manager / can be shared via WhatsApp etc.),
  add the `plyer` package and Android's storage-access-framework share
  intent — happy to add that next if useful.
- Since this holds real patient data, consider adding an app-open PIN/
  biometric lock before using it with real records.
