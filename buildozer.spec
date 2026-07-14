[app]
title = Hospital Records
package.name = hospitalrecords
package.domain = org.dayani
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.2.1,kivymd==1.2.0,openpyxl,sqlite3
orientation = portrait
fullscreen = 0

# Permissions: only needed if you later want to export/share files
# outside the app's private storage (e.g. to Downloads).
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
