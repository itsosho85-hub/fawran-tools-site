#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
فحص جودة الموقع قبل النشر — يعمل محليًا وفي GitHub Actions.
Usage: python scripts/site_audit.py
يخرج برمز 1 إذا وُجدت مشاكل حرجة (روابط مكسورة / hreflang لصفحات غير موجودة /
صفحات خارج خريطة الموقع / عناوين SEO ناقصة) حتى لا تصل الأخطاء للأبد بسهولة.
"""
import os, re, sys, glob
from collections import Counter

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)

pages = sorted(p for p in glob.glob("**/*.html", recursive=True) if ".git" not in p)
errors, warnings = [], []

# ---------- 1) ملفات موجودة ----------
all_files = set()
for root, dirs, files in os.walk("."):
    if ".git" in root or "node_modules" in root:
        continue
    for f in files:
        all_files.add(os.path.normpath(os.path.join(root, f)))

def resolve(href, page):
    """يحل رابطًا نسبيًا أو جذريًا إلى مسار ملف متوقع. يرجع None إذا غير موجود."""
    clean = href.split("?")[0]
    if clean.startswith("/"):
        clean = clean.lstrip("/")
        if not clean:                      # "/" -> index.html
            return "index.html" if os.path.exists("index.html") else None
        if clean.rstrip("/") == "en":      # "/en/" -> en/index.html
            return os.path.join("en", "index.html")
        base = "."
    else:
        base = os.path.dirname(page)
    target = os.path.normpath(os.path.join(base, clean))
    for cand in (target, target + ".html", os.path.join(target, "index.html")):
        if cand in all_files:
            return cand
    return None

# ---------- 2) فحص الروابط الداخلية (خارج السكربتات) ----------
link_re = re.compile(r'href="([^"#]+?)(?:#[^"]*)?"')
script_re = re.compile(r'<script\b.*?</script>|<script\b[^>]*/>', re.S)
for p in pages:
    html = open(p, encoding="utf-8").read()
    # استبعاد محتوى السكربتات: روابط داخل قوالب JS معروضة كأمثلة وليست روابط حقيقية
    html_no_js = script_re.sub('', html)
    for m in link_re.finditer(html_no_js):
        href = m.group(1)
        if href.startswith(("http", "//", "mailto:", "javascript:", "data:", "tel:")):
            continue
        if "${" in href or href.startswith("'"):
            continue
        if resolve(href, p) is None:
            errors.append(f"رابط مكسور: {p} -> {href}")

# ---------- 3) وسوم SEO الأساسية ----------
for p in pages:
    html = open(p, encoding="utf-8").read()
    if os.path.basename(p) == "404.html":
        continue
    if not re.search(r"<title[^>]*>[^<]+</title>", html):
        errors.append(f"بدون title: {p}")
    if not re.search(r'name="description"', html):
        errors.append(f"بدون meta description: {p}")
    if 'rel="canonical"' not in html:
        errors.append(f"بدون canonical: {p}")
    h1s = len(re.findall(r"<h1[\s>]", html))
    if h1s == 0:
        errors.append(f"بدون H1: {p}")
    elif h1s > 1:
        warnings.append(f"أكثر من H1 ({h1s}): {p}")

# ---------- 4) hreflang يجب أن يشير لصفحات موجودة ----------
existing = set(p.lstrip("./") for p in pages)
existing |= {"", "en"}   # "/" و "/en" بعد إزالة الشرطة المائلة الأخيرة
for p in pages:
    html = open(p, encoding="utf-8").read()
    for m in re.finditer(r'<link[^>]*hreflang="([^"]+)"[^>]*>', html):
        tag = m.group(0)
        href = re.search(r'href="([^"]+)"', tag)
        if not href:
            continue
        url = href.group(1)
        path = url.replace("https://fawran.tools/", "").rstrip("/")
        if path and path not in existing:
            errors.append(f"hreflang يشير لصفحة غير موجودة: {p} [{m.group(1)}] -> {url}")

# ---------- 5) خريطة الموقع ----------
sm = open("sitemap.xml", encoding="utf-8").read()
sm_urls = re.findall(r"<loc>([^<]+)</loc>", sm)
sm_paths = set(u.replace("https://fawran.tools/", "").lstrip("/") for u in sm_urls)
# "/" و "/en/" في sitemap يقابلان index.html و en/index.html
sm_paths |= {"index.html", "en/index.html"}
for u in sm_urls:
    path = u.replace("https://fawran.tools/", "").lstrip("/")
    if path and path not in existing and not path.endswith("/"):
        errors.append(f"في sitemap لكن الملف غير موجود: {u}")
dups = [u for u, c in Counter(sm_urls).items() if c > 1]
for u in dups:
    errors.append(f"تكرار في sitemap: {u}")
missing_from_sm = [
    p for p in existing
    if p not in sm_paths and os.path.basename(p) != "404.html" and not p.startswith("en/") and p not in ("", "en")
]
for p in missing_from_sm:
    warnings.append(f"صفحة عربية غير موجودة في sitemap: {p}")

# ---------- 6) فحص _headers ----------
try:
    with open("_headers", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if not s.startswith("/"):
                name = s.split(":")[0].strip()
                if s.startswith("https:") or name.startswith("https"):
                    errors.append(f"_headers سطر {i}: لا يمكن ضبط رؤوس لعناوين خارجية: {s[:60]}")
                elif ":" not in s:
                    errors.append(f"_headers سطر {i}: نص بدون # داخل البلوكات يكسر التحليل: {s[:60]}")
except FileNotFoundError:
    warnings.append("ملف _headers غير موجود")

# ---------- التقرير ----------
print(f"الصفحات المفحوصة: {len(pages)}")
print(f"روابط sitemap: {len(sm_urls)}")
print(f"\nمشاكل حرجة: {len(errors)}")
for e in errors[:30]:
    print("   ❌", e)
print(f"\nتحذيرات: {len(warnings)}")
for w in warnings[:15]:
    print("   ⚠️ ", w)

sys.exit(1 if errors else 0)
