#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replace repeated tool copy with a task-specific editorial guide per tool.

The script is deliberately data-driven: every tool keeps its original UI/logic while
receiving a unique introduction, walkthrough, use cases, practitioner notes, FAQs,
related internal links, and matching FAQPage + HowTo JSON-LD.
"""
from __future__ import annotations

import hashlib
import html as html_lib
import importlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "assets/tools-index.js").read_text(encoding="utf-8")


def tools_for(lang: str):
    match = re.search(rf"window\.TOOLS_INDEX_{lang}\s*=\s*(\[.*?\]);", INDEX, re.S)
    if not match:
        raise RuntimeError(f"TOOLS_INDEX_{lang} was not found")
    return json.loads(match.group(1))


AR_TOOLS = tools_for("AR")
EN_TOOLS = tools_for("EN")
AR_BY_SLUG = {x["slug"]: x for x in AR_TOOLS}
EN_BY_SLUG = {x["slug"]: x for x in EN_TOOLS}

# The image pages received hand-written, long-form Arabic copy.  Other records are
# generated from an explicit, tool-specific focus statement plus category workflows.
import sys
sys.path.insert(0, str(ROOT / "scripts"))
try:
    from content_images_ar_1 import CONTENT as IMAGE_COPY_1
    from content_images_ar_2 import CONTENT as IMAGE_COPY_2
except ImportError as exc:
    raise RuntimeError("Arabic image editorial source files are required") from exc
IMAGE_COPY_AR = {**IMAGE_COPY_1, **IMAGE_COPY_2}

# One clear job statement for every non-image utility.  It is used in the opening
# explanation, steps, use cases, hints and FAQ answers so pages are not variants of
# a single boilerplate paragraph.
FOCUS_AR = {
    # SEO
    "article-schema-generator": "إنشاء ترميز Article JSON-LD دقيق يعرّف جوجل بعنوان المقال وكاتبه وتواريخه وصورته",
    "canonical-checker": "فحص وسم canonical والتأكد من أن الصفحة تشير إلى النسخة الأساسية المقصودة",
    "faq-schema-generator": "تحويل أسئلة وأجوبة الصفحة إلى FAQPage JSON-LD صالح للنسخ",
    "heading-analyzer": "قراءة تسلسل H1 إلى H6 وكشف القفزات والعناوين الفارغة في صفحة",
    "http-status-checker": "التحقق من رمز استجابة HTTP وسلسلة التحويلات التي يمر بها عنوان الويب",
    "image-alt-checker": "حصر صور الصفحة التي تفتقد نص alt أو تحمل وصفًا غير مفيد",
    "internal-link-checker": "استخراج الروابط الداخلية من HTML لمراجعة بنية الربط والتنقل",
    "keyword-clustering": "تجميع قائمة الكلمات المفتاحية في مجموعات نية بحث متقاربة",
    "keyword-density": "قياس تكرار الكلمات والعبارات داخل النص من دون تخمين أو حشو",
    "local-business-schema": "إنشاء LocalBusiness Schema لنشاط محلي يشمل الاسم والعنوان وساعات العمل",
    "meta-tags-analyzer": "تحليل title وmeta description وrobots وcanonical في كود الصفحة",
    "open-graph-checker": "مراجعة وسوم Open Graph التي تتحكم في شكل الرابط عند مشاركته",
    "page-word-counter": "حساب كلمات الصفحة ومقاطعها ونصها المرئي لتقدير عمق المحتوى",
    "readability-analyzer": "تقدير وضوح النص وطول جمله وكلماته لاتخاذ قرار تحريري مدروس",
    "robots-txt-tester": "اختبار قاعدة robots.txt لمعرفة ما إذا كان مسار محدد مسموحًا للزحف",
    "schema-validator": "فحص JSON-LD مكتوب يدويًا قبل إضافته إلى الصفحة",
    "security-headers-checker": "قراءة ترويسات الأمان في استجابة موقع والتنبيه إلى السياسات الغائبة",
    "seo-audit": "تحويل HTML أو بيانات الصفحة إلى قائمة ملاحظات SEO قابلة للتنفيذ",
    "serp-snippet-preview": "معاينة العنوان والوصف كما قد يبدوان في نتائج البحث قبل النشر",
    "sitemap-validator": "فحص بنية Sitemap XML واكتشاف روابط أو وسوم غير متوقعة",
    "twitter-card-generator": "توليد وسوم Twitter Card لصورة وعنوان ووصف الرابط",
    "url-slug-generator": "تحويل العناوين إلى Slug نظيف ومقروء ومناسب للرابط",
    "utm-link-builder": "بناء رابط UTM منظم لحملات التسويق والقياس في التحليلات",
    "website-seo-checklist": "إنتاج قائمة تدقيق SEO عملية للموقع قبل الإطلاق أو بعد تعديل كبير",
    # Developer
    "base64-encoder-decoder": "ترميز النص إلى Base64 أو فك سلسلة Base64 بسرعة مع الحفاظ على النص الأصلي",
    "color-converter": "التنقل بدقة بين قيم HEX وRGB وHSL عند بناء واجهة أو نظام ألوان",
    "hash-generator": "إنشاء بصمات Hash والتحقق من أن النص نفسه ينتج البصمة المتوقعة",
    "html-formatter": "تنسيق HTML غير المقروء إلى بنية متداخلة يسهل فحصها وتعديلها",
    "json-formatter": "ترتيب JSON وعرضه بمسافات وطبقات واضحة من دون تغيير بياناته",
    "json-minifier": "حذف المسافات والأسطر غير الضرورية من JSON لتقليل حجمه في النقل",
    "json-validator": "كشف خطأ الصياغة في JSON وتحديد موضعه قبل إدخاله إلى التطبيق",
    "jwt-decoder": "قراءة ترويسة وحمولة JWT محليًا لفهم المطالبات دون محاولة كسر التوقيع",
    "regex-tester": "تجربة تعبير نمطي على نص حقيقي ومعاينة التطابقات قبل وضعه في الكود",
    "unix-timestamp-converter": "التحويل المتبادل بين Unix timestamp والتاريخ والوقت المقروءين",
    "url-encoder-decoder": "ترميز أحرف الرابط الخاصة أو فكها مع منع كسر المعلمات",
    "uuid-generator": "إنشاء معرفات UUID فريدة للاختبارات والسجلات ومعرفات الكيانات",
    # PDF
    "images-to-pdf": "جمع صور متفرقة في مستند PDF واحد مرتب وقابل للمشاركة",
    "pdf-compress": "تقليل حجم PDF حتى يصبح مناسبًا للبريد والرفع مع مراجعة نتيجة الضغط",
    "pdf-delete-pages": "حذف صفحات زائدة أو حساسة من ملف PDF مع الإبقاء على البقية",
    "pdf-duplicate-pages": "تكرار صفحات مختارة داخل PDF عند الحاجة إلى نسخ إضافية للطباعة",
    "pdf-extract-pages": "استخراج صفحات محددة من PDF في ملف مستقل أخف وأسهل مشاركة",
    "pdf-info": "عرض خصائص PDF الأساسية مثل عدد الصفحات والحجم وبيانات المستند",
    "pdf-merge": "دمج أكثر من PDF في ملف واحد بترتيب تحدده أنت",
    "pdf-metadata-remover": "إنشاء نسخة PDF نظيفة بلا عنوان أو مؤلف أو بيانات تعريفية متروكة",
    "pdf-page-numbers": "إضافة أرقام صفحات واضحة إلى مستند PDF قبل مشاركته أو طباعته",
    "pdf-reorder-pages": "إعادة ترتيب صفحات PDF بالسحب قبل إخراج النسخة النهائية",
    "pdf-rotate": "تصحيح اتجاه صفحات PDF المائلة أو المقلوبة",
    "pdf-split": "تقسيم PDF طويل إلى ملفات أصغر وفق النطاقات التي تحتاجها",
    # Websites
    "currency-converter": "تحويل مبلغ بين عملات عالمية مع قراءة النتيجة كتقدير لا كسعر تنفيذ مصرفي",
    "currency-widget-generator": "بناء ودجت أسعار صرف قابل للتضمين في موقعك من دون كتابة الهيكل يدويًا",
    "favicon-generator": "إنتاج حزمة أيقونات موقع بالمقاسات اللازمة للمتصفح والتبويبات",
    "meta-tags-generator": "توليد title ووصف ووسوم مشاركة واضحة لصفحة أو منتج",
    "og-image-maker": "تصميم صورة Open Graph بأبعاد مناسبة لظهور الرابط في الشبكات الاجتماعية",
    "redirect-generator": "كتابة قاعدة تحويل 301 صحيحة لخادم Apache أو Nginx أو Netlify",
    "robots-generator": "إنشاء ملف robots.txt يوازن بين إتاحة الزحف وحماية المسارات غير العامة",
    "schema-generator": "توليد JSON-LD أساسي للصفحات والمنتجات والجهات بطريقة منظمة",
    "sitemap-generator": "إنشاء Sitemap XML من قائمة الصفحات لتسهيل اكتشافها من محركات البحث",
    "website-speed-checker": "قراءة عوامل الويب الأساسية التي تؤثر في زمن تحميل الصفحة وتجربة الزائر",
    # Email
    "disposable-email-checker": "معرفة ما إذا كان نطاق البريد مؤقتًا أو مخصصًا لبريد قصير العمر",
    "email-extractor": "التقاط عناوين البريد الموجودة في نص طويل وفرزها في قائمة قابلة للاستخدام",
    "email-list-cleaner": "تنظيف قائمة بريد من التكرار والفراغات والصيغ غير السليمة قبل الاستيراد",
    "email-signature-generator": "تكوين توقيع بريد منظم يعرض الاسم والدور وطرق التواصل بهوية احترافية",
    "email-validator": "فحص شكل البريد والنطاق قبل إدخاله إلى نموذج أو قائمة تواصل",
    "fake-email-generator": "إنشاء عناوين اختبار وهمية آمنة لاستخدامها في بيئات التطوير والعروض",
    "gmail-dot-trick-generator": "توليد صيغ Gmail بالنقاط لاختبار التسجيلات وتصفية الرسائل",
    "gmail-plus-alias-generator": "إنتاج aliases من نمط +tag لتنظيم الرسائل الواردة إلى Gmail",
    "mailto-link-generator": "إنشاء رابط mailto يملأ العنوان والموضوع ونص الرسالة مسبقًا",
    # AI
    "image-prompt-builder": "صياغة برومبت صورة منظم يصف الموضوع والأسلوب والإضاءة والنسبة",
    "ocr-text-extractor": "استخراج النص العربي أو الإنجليزي القابل للنسخ من صورة أو لقطة شاشة",
    "prompt-enhancer": "توسيع فكرة قصيرة إلى برومبت محدد بسياق وقيود ومخرج مطلوب",
    "prompt-library": "استكشاف قوالب برومبتات عملية ثم تخصيصها قبل إرسالها للنموذج",
    "social-metadata-generator": "صياغة عنوان ووصف SEO ونص منشور اجتماعي انطلاقًا من موضوع واحد",
    "speech-to-text": "تحويل الكلام المباشر من الميكروفون إلى نص قابل للتحرير والمراجعة",
    "text-analyzer": "تحليل النص من حيث طول القراءة والكلمات البارزة وبنية المحتوى",
    # Text
    "remove-duplicate-lines": "إزالة الأسطر المتكررة من قائمة أو سجل نصي مع الإبقاء على النسخة الأولى",
    "text-compare": "إبراز الفروق بين نسختين من نص أو كود بدل المقارنة اليدوية سطرًا بسطر",
    "word-counter": "حساب الكلمات والحروف والفقرات ووقت القراءة في نص قبل نشره",
    # Video
    "quick-video-editor": "دمج مقاطع وصور قصيرة في تسلسل فيديو بسيط قبل التصدير",
    "whiteboard-video-maker": "تحويل صور ومشاهد مختارة إلى فيديو بأسلوب السبورة البيضاء",
    # YouTube
    "youtube-banner-maker": "تصميم غلاف قناة يوتيوب يحترم منطقة الأمان المرئية على كل الأجهزة",
    "youtube-channel-description-generator": "كتابة وصف قناة يعرّف المجال والجمهور والقيمة بوضوح",
    "youtube-channel-name-generator": "توليد أسماء قناة قابلة للتذكر وقابلة للتطوير داخل مجال محدد",
    "youtube-chapters-generator": "ترتيب فصول زمنية تساعد المشاهد على التنقل في فيديو طويل",
    "youtube-description-generator": "صياغة وصف فيديو يقدم السياق والكلمات المهمة والدعوة المناسبة للمشاهدة",
    "youtube-earnings-calculator": "تقدير نطاق أرباح محتمل من المشاهدات مع فهم حدود هذا التقدير",
    "youtube-engagement-calculator": "حساب معدل التفاعل من المشاهدات والإعجابات والتعليقات بمؤشر واضح",
    "youtube-hashtag-generator": "اقتراح هاشتاجات محددة ومرتبطة بالموضوع بدلاً من قوائم عامة",
    "youtube-hook-generator": "ابتكار افتتاحيات أولى تحافظ على انتباه المشاهد في ثواني الفيديو الأولى",
    "youtube-keyword-tool": "تنظيم عبارات بحث يوتيوب حول موضوع ونية مشاهدة محددة",
    "youtube-logo-maker": "بناء فكرة شعار قناة بسيطة قابلة للتمييز في المقاس الصغير",
    "youtube-seo-checklist": "مراجعة عناصر تحسين فيديو يوتيوب قبل الضغط على نشر",
    "youtube-tag-generator": "اقتراح وسوم فيديو مرتبطة بدقة بموضوعه وجمهوره",
    "youtube-thumbnail-analyzer": "تقييم عناصر الصورة المصغرة من وضوح النص والتباين والتركيز البصري",
    "youtube-thumbnail-downloader": "الحصول على نسخة الصورة المصغرة العامة من رابط فيديو يوتيوب",
    "youtube-thumbnail-maker": "تصميم تخطيط صورة مصغرة يعطي الموضوع وعدًا بصريًا واضحًا",
    "youtube-timestamp-link": "إنشاء رابط يفتح فيديو يوتيوب في ثانية أو دقيقة محددة",
    "youtube-title-analyzer": "فحص عنوان الفيديو من حيث الطول والوضوح وقابلية النقر بلا تضليل",
    "youtube-title-generator": "توليد عناوين فيديو قابلة للاختبار حول موضوع وجمهور محددين",
    "youtube-upload-checklist": "تنظيم خطوات رفع الفيديو من العنوان حتى شاشات النهاية والتعليقات",
    "youtube-video-ideas": "تحويل مجال قناة إلى قائمة أفكار قابلة للإنتاج بدل انتظار الإلهام",
}

FOCUS_EN = {
    "article-schema-generator": "building Article JSON-LD that identifies an article's headline, author, dates and image",
    "canonical-checker": "checking a canonical tag and confirming which version of a URL should be primary",
    "faq-schema-generator": "turning page questions and answers into copy-ready FAQPage JSON-LD",
    "heading-analyzer": "reviewing the H1-to-H6 hierarchy and spotting skipped or empty headings",
    "http-status-checker": "checking an HTTP response code and the redirect chain behind a URL",
    "image-alt-checker": "finding images in a page that are missing useful alt text",
    "internal-link-checker": "extracting internal links from HTML to review site navigation and linking",
    "keyword-clustering": "grouping a keyword list by closely related search intent",
    "keyword-density": "measuring repeated words and phrases in a text without guessing",
    "local-business-schema": "creating LocalBusiness Schema with a name, address and opening hours",
    "meta-tags-analyzer": "reviewing title, meta description, robots and canonical markup in page code",
    "open-graph-checker": "checking the Open Graph tags that control a shared-link preview",
    "page-word-counter": "counting visible page text to assess the depth of a page",
    "readability-analyzer": "reviewing sentence and word complexity to make writing easier to scan",
    "robots-txt-tester": "testing whether a robots.txt rule allows a given crawler path",
    "schema-validator": "checking manually written JSON-LD before it goes live",
    "security-headers-checker": "reading security headers in a site response and flagging missing policies",
    "seo-audit": "turning page HTML into an actionable SEO review",
    "serp-snippet-preview": "previewing how a title and description can appear in search results",
    "sitemap-validator": "checking an XML sitemap for malformed or unexpected entries",
    "twitter-card-generator": "creating Twitter Card metadata for a link, title, description and image",
    "url-slug-generator": "turning a title into a clean, readable URL slug",
    "utm-link-builder": "building a consistent UTM campaign URL for analytics",
    "website-seo-checklist": "creating a practical SEO launch or post-change checklist",
    "base64-encoder-decoder": "encoding text as Base64 or decoding an existing Base64 value",
    "color-converter": "moving precisely between HEX, RGB and HSL color values",
    "hash-generator": "creating hash fingerprints for test data and integrity checks",
    "html-formatter": "turning hard-to-read HTML into an indented structure",
    "json-formatter": "formatting JSON into a readable indented document without changing its data",
    "json-minifier": "removing unnecessary spaces and line breaks from JSON",
    "json-validator": "finding a JSON syntax issue before it reaches an application",
    "jwt-decoder": "reading a JWT header and payload locally without attempting to break a signature",
    "regex-tester": "testing a regular expression against real sample text",
    "unix-timestamp-converter": "converting between Unix timestamps and human-readable dates",
    "url-encoder-decoder": "encoding special URL characters or decoding an encoded value",
    "uuid-generator": "creating unique UUID values for test data, records and identifiers",
    "images-to-pdf": "combining separate images into one ordered PDF document",
    "pdf-compress": "reducing a PDF file size before email or upload",
    "pdf-delete-pages": "removing unwanted or sensitive pages from a PDF",
    "pdf-duplicate-pages": "duplicating selected PDF pages for printing or repeated inserts",
    "pdf-extract-pages": "extracting selected PDF pages into a separate file",
    "pdf-info": "reading basic PDF file properties and document metadata",
    "pdf-merge": "merging several PDF files into one ordered document",
    "pdf-metadata-remover": "making a PDF copy without leftover author or document metadata",
    "pdf-page-numbers": "adding visible page numbers before sharing or printing a PDF",
    "pdf-reorder-pages": "reordering PDF pages before exporting the final copy",
    "pdf-rotate": "correcting sideways or upside-down PDF pages",
    "pdf-split": "splitting a long PDF into smaller, purpose-specific files",
    "currency-converter": "converting an amount between world currencies as a planning estimate",
    "currency-widget-generator": "building an embeddable currency-rate widget without hand-writing its structure",
    "favicon-generator": "creating a set of site icons for browser tabs and shortcuts",
    "meta-tags-generator": "generating a clear title, description and share metadata for a page",
    "og-image-maker": "designing an Open Graph image at a share-friendly size",
    "redirect-generator": "writing a correct 301 redirect rule for Apache, Nginx or Netlify",
    "robots-generator": "creating a robots.txt file that balances crawl access and private paths",
    "schema-generator": "generating structured JSON-LD for pages, products or organizations",
    "sitemap-generator": "building an XML sitemap from a list of important pages",
    "website-speed-checker": "reviewing web factors that affect loading time and visitor experience",
    "disposable-email-checker": "checking whether an email domain is disposable or short-lived",
    "email-extractor": "collecting email addresses present in a long text into a usable list",
    "email-list-cleaner": "cleaning a mailing list of duplicates, whitespace and malformed values",
    "email-signature-generator": "assembling a professional email signature with identity and contact details",
    "email-validator": "checking an email's format and domain before using it in a form or list",
    "fake-email-generator": "creating safe fake email addresses for testing and demonstrations",
    "gmail-dot-trick-generator": "creating Gmail dot variations for sign-up tests and inbox filtering",
    "gmail-plus-alias-generator": "creating Gmail plus aliases to organize incoming messages",
    "mailto-link-generator": "creating a mailto link that pre-fills a recipient, subject and message",
    "image-prompt-builder": "building a structured image prompt with subject, style, lighting and aspect ratio",
    "ocr-text-extractor": "extracting copyable Arabic or English text from an image or screenshot",
    "prompt-enhancer": "expanding a short idea into a focused prompt with context and constraints",
    "prompt-library": "exploring practical prompt patterns and tailoring one before sending it to a model",
    "social-metadata-generator": "writing an SEO title, meta description and social post from one topic",
    "speech-to-text": "turning live microphone speech into editable text",
    "text-analyzer": "reviewing reading length, prominent terms and content structure in a text",
    "remove-duplicate-lines": "removing repeated lines from a list or log while preserving the first occurrence",
    "text-compare": "highlighting differences between two text or code versions",
    "word-counter": "counting words, characters, paragraphs and reading time before publishing",
    "quick-video-editor": "combining short clips and images into a simple video sequence",
    "whiteboard-video-maker": "turning selected images and scenes into a whiteboard-style video",
    "youtube-banner-maker": "designing a channel banner that respects YouTube safe areas on every device",
    "youtube-channel-description-generator": "writing a channel description that makes its audience and value clear",
    "youtube-channel-name-generator": "generating memorable channel names that can grow with a niche",
    "youtube-chapters-generator": "organizing timestamps into chapters that make a long video easier to navigate",
    "youtube-description-generator": "writing a video description with context, useful terms and a clear next step",
    "youtube-earnings-calculator": "estimating a possible revenue range from views while respecting its limits",
    "youtube-engagement-calculator": "calculating an engagement rate from views, likes and comments",
    "youtube-hashtag-generator": "suggesting focused, topic-relevant hashtags instead of generic lists",
    "youtube-hook-generator": "brainstorming openings that retain attention in the first seconds of a video",
    "youtube-keyword-tool": "organizing YouTube search phrases around a topic and viewing intent",
    "youtube-logo-maker": "building a simple channel-logo concept that remains recognizable at small sizes",
    "youtube-seo-checklist": "reviewing YouTube search and publishing elements before a video goes live",
    "youtube-tag-generator": "suggesting video tags that closely fit a topic and audience",
    "youtube-thumbnail-analyzer": "reviewing thumbnail text, contrast and visual focus",
    "youtube-thumbnail-downloader": "retrieving the public thumbnail image for a YouTube video URL",
    "youtube-thumbnail-maker": "designing a thumbnail layout with a clear visual promise",
    "youtube-timestamp-link": "creating a URL that opens a YouTube video at an exact moment",
    "youtube-title-analyzer": "checking a video title for length, clarity and click appeal without misleading viewers",
    "youtube-title-generator": "brainstorming testable video titles for a topic and audience",
    "youtube-upload-checklist": "organizing the steps from a video's title through end screens and comments",
    "youtube-video-ideas": "turning a channel niche into a usable list of production ideas",
}

# These category guides tell the walkthrough what sort of input, configuration and
# deliverable a real visitor should expect.  A tool's individual focus always names
# the actual task; the category guide makes the instructions operational.
CAT_AR = {
    "images": ("الصورة أو الملف المرئي الذي تريد معالجته", "خيارات الصورة الظاهرة في الواجهة", "ملف الصورة الناتج أو معاينته", "افحص المعاينة والحجم قبل حفظ النسخة النهائية"),
    "pdf": ("ملف PDF أو الصور التي تريد تنظيمها", "الصفحات أو الترتيب أو نطاق العمل", "ملف PDF الناتج", "افتح الملف الناتج وراجع الصفحات قبل إرساله"),
    "seo": ("رابط الصفحة أو HTML أو البيانات المطلوبة للفحص", "الإعدادات أو الحقول المطابقة لصفحتك", "تقريرًا أو كودًا قابلًا للنسخ", "نفّذ التوصيات في صفحة تجريبية ثم راقب أثرها"),
    "developer": ("النص البرمجي أو القيمة المراد معالجتها", "الصيغة والخيار المناسبين للمهمة", "ناتجًا منسقًا وقابلًا للنسخ", "اختبر الناتج في بيئة آمنة قبل وضعه في الإنتاج"),
    "websites": ("بيانات الصفحة أو الموقع التي ستبني عليها النتيجة", "الحقول والخيارات الخاصة بمنصتك", "كودًا أو ملفًا أو نتيجة قابلة للاستخدام", "الصق الناتج في بيئة اختبار وتحقق منه قبل النشر"),
    "email": ("النص أو عنوان البريد أو بيانات التوقيع المطلوبة", "الخيار أو الحقل الذي يطابق حالة الاستخدام", "قائمة أو رابطًا أو قالبًا جاهزًا", "راجع العناوين والروابط يدويًا قبل إرسال أي رسالة"),
    "ai": ("الفكرة أو النص أو المصدر الذي ستعمل عليه", "اللغة والنبرة والقيود التي تهمك", "نصًا أو اقتراحًا أو تحليلاً قابلًا للتحرير", "عامل النتيجة كمسودة ثم راجع الحقائق والصياغة"),
    "text": ("النص أو النسختين المطلوب فحصهما", "طريقة المقارنة أو خيارات التنظيف", "نصًا أو إحصاءات قابلة للنسخ", "راجع النتيجة ضمن سياقها قبل اعتمادها"),
    "video": ("المقاطع أو الصور التي ستدخل في الفيديو", "الترتيب والمدة وخيارات التصدير", "معاينة أو ملف فيديو ناتج", "شاهد الناتج كاملًا وتأكد من الصوت والترتيب قبل نشره"),
    "youtube": ("موضوع الفيديو والجمهور والكلمات أو الأرقام ذات الصلة", "النبرة واللغة والقيود التي تعكس قناتك", "اقتراحات أو نصًا أو حسابًا قابلاً للتعديل", "راجع الاقتراحات لتبقى دقيقة وملائمة لجمهور القناة"),
}

CAT_EN = {
    "images": ("the image or visual file you want to process", "the image options shown in the interface", "an image file or preview", "inspect the preview and file size before saving the final version"),
    "pdf": ("the PDF or image files you want to organize", "the pages, order or range that applies", "a PDF output file", "open the result and review every page before you send it"),
    "seo": ("the page URL, HTML or audit data", "the settings and fields that match your page", "a report or copy-ready code", "apply recommendations to a test page and monitor the result"),
    "developer": ("the code, text or value to process", "the format and option that fit the task", "a formatted value that can be copied", "test the result in a safe environment before production"),
    "websites": ("the site or page data that drives the result", "the fields and options for your platform", "code, a file or a usable result", "test the output before you publish it"),
    "email": ("the text, email address or signature details", "the option that matches your use case", "a list, link or ready-to-use template", "review addresses and links manually before you send a message"),
    "ai": ("the idea, text or source material", "language, tone and constraints", "editable text, suggestions or an analysis", "treat the output as a draft and review facts and wording"),
    "text": ("the text or two versions to inspect", "the comparison or cleaning options", "text or statistics you can copy", "review the outcome in its original context"),
    "video": ("the clips or images for the video", "order, duration and export choices", "a preview or video file", "watch the entire result and check sequence and audio before publishing"),
    "youtube": ("the video topic, audience and relevant keywords or figures", "tone, language and channel constraints", "editable suggestions, text or a calculation", "review suggestions so they remain accurate and suitable for your audience"),
}

CATEGORY_KEYWORDS_AR = {
    "images": "معالجة الصور، أداة صور أونلاين، تعديل الصور محليًا",
    "pdf": "أدوات PDF، معالجة PDF أونلاين، تنظيم المستندات",
    "seo": "أدوات SEO، تحسين محركات البحث، تدقيق المواقع",
    "developer": "أدوات المطورين، برمجة ويب، معالجة البيانات",
    "websites": "أدوات المواقع، تطوير الويب، إعدادات الموقع",
    "email": "أدوات البريد الإلكتروني، تنظيم الإيميلات، إنتاجية العمل",
    "ai": "أدوات الذكاء الاصطناعي، كتابة ذكية، إنتاجية المحتوى",
    "text": "أدوات النصوص، تحرير النص، تحليل المحتوى",
    "video": "أدوات الفيديو، تعديل الفيديو أونلاين، صناعة المحتوى",
    "youtube": "أدوات يوتيوب، نمو القناة، تحسين الفيديو",
}
CATEGORY_KEYWORDS_EN = {
    "images": "image tools, online image editing, local image processing",
    "pdf": "PDF tools, online PDF processing, document organization",
    "seo": "SEO tools, search optimization, website auditing",
    "developer": "developer tools, web development, data processing",
    "websites": "website tools, web development, site configuration",
    "email": "email tools, inbox organization, work productivity",
    "ai": "AI tools, smarter writing, content productivity",
    "text": "text tools, text editing, content analysis",
    "video": "video tools, online video editing, content creation",
    "youtube": "YouTube tools, channel growth, video optimization",
}


def esc(s: str) -> str:
    return html_lib.escape(str(s), quote=True)


def variant(slug: str) -> int:
    return int(hashlib.sha1(slug.encode()).hexdigest()[:4], 16) % 4


def local_href(slug: str) -> str:
    return f"{slug}.html"


def related(tool: dict, all_tools: list[dict], lang: str) -> list[dict]:
    same = [x for x in all_tools if x["cat"] == tool["cat"] and x["slug"] != tool["slug"]]
    # A deterministic rotation makes related links distinct and distributes internal links.
    shift = int(hashlib.md5(tool["slug"].encode()).hexdigest()[:2], 16) % max(1, len(same))
    return (same[shift:] + same[:shift])[:3]


def generic_record_ar(tool: dict) -> dict:
    title, cat, slug = tool["title"], tool["cat"], tool["slug"]
    focus = FOCUS_AR.get(slug, tool["desc"].rstrip("."))
    input_, config, output, check = CAT_AR[cat]
    v = variant(slug)
    intros = [
        [f"{title} هو مسار عملي لـ{focus}. يعرض المهمة في خطوات قابلة للتدقيق بدل تركك مع نتيجة مجردة لا تعرف كيف وصلت إليها.", f"ينطلق {title} من {input_}. عند {focus} اضبط {config}، ثم افحص {output} قبل أن تنتقل إلى الخطوة التالية في مشروعك."],
        [f"الغرض المحدد من {title} هو {focus}. الفائدة ليست في الضغط على زر فقط، بل في معرفة المدخلات والقرارات التي تؤثر في النتيجة النهائية.", f"أدخل {input_} في {title}، واربط {config} بهدف {focus}. بعد ذلك ستظهر {output} لتراجعها في سياق العمل الحقيقي."],
        [f"عند الحاجة إلى {focus}، يجعل {title} المسار أقصر وأوضح. ستظل المراجعة المهنية ضرورية، لكنك تبدأ من نتيجة منظمة بدل خطوات يدوية متفرقة.", f"في {title} تستخدم {input_} وتحدد {config}. هذا يولّد {output}؛ ومن الأفضل اختبارها قبل أن تؤثر في نشر أو تسليم."],
        [f"{title} يخدم قرارًا واحدًا بوضوح: {focus}. كل جزء من الدليل التالي يربط ما تدخله بالنتيجة التي يمكنك استخدامها أو تعديلها.", f"ابدأ بـ{input_} في {title}. اختر {config} بما يلائم {focus}، ثم راجع {output} مراجعة واعية لا شكلية."],
    ][v]
    steps = [
        (f"جهّز {input_}", f"ابدأ {title} بمصدر موثوق. في {focus} عبر {title}، اجعل المدخلات مكتملة ومحدّثة لا نسخة مبتورة."),
        (f"عرّف هدف {focus}", f"أدخل القيم داخل حقول {title}. اربط كل قيمة بـ{focus} في {title} كي لا تنتج عن المهمة قراءة في سياق غير مقصود."),
        (f"اضبط {config}", f"اضبط {title} لحالة الاستخدام الفعلية. عند {focus}، غيّر خيار {title} واحدًا في كل مرة ثم راقب الأثر."),
        (f"اقرأ {output}", f"بعد تشغيل {title}، قارن {output} بهدف {focus}. أي تنبيه في {title} الآن أسهل من خطأ متأخر بعد النشر."),
        ("اعتمد النسخة التي تحققت منها", f"بعد {focus} عبر {title}، أتم مراجعة مشروعك. احفظ نسخة {title} التي تمثل {focus} المعتمدة."),
    ]
    cases = [
        f"قبل أن يسلّم {title} عملاً يحتاج إلى {focus} وفق مواصفات واضحة.",
        f"عندما يحتاج {focus} إلى مراجعة فريق، يحفظ {title} القرارات ظاهرة لا مبهمة.",
        f"حين تصبح نتيجة {focus} من {title} جزءًا من صفحة أو رسالة أو ملف يحتاج فحصًا أخيرًا.",
        f"لإنشاء نسخة {title} أولية من {focus} ثم صقلها داخل {title} للسياق المستهدف.",
    ]
    tips = [
        f"في {title}، احتفظ بالأصل كي تظل تجربة {focus} قابلة للعكس والمقارنة عبر {title}.",
        f"إذا كان {focus} سيتكرر في فريق، دوّن داخل {title} سبب كل إعداد من إعدادات {title}.",
        f"قبل اعتماد {focus}، راجعه في البيئة التي سيظهر فيها ناتج {title} لا في نافذة {title} وحدها.",
        f"كلما كان هدف {focus} محددًا، قلّ الضجيج داخل {title} وصار ناتج {title} أسهل للتحقق.",
    ]
    faq = [
        (f"ما المدخلات المناسبة لـ{title}؟", f"يعتمد {title} على {input_}. عند {focus} في {title} اختر مصدرًا حديثًا؛ نقص المصدر يغيّر ناتج {title}."),
        (f"كيف أتأكد أن {title} حقق هدفي؟", f"قارن {output} بهدف {focus}، ثم راجعه داخل وجهته النهائية بعد {title}."),
        (f"هل أستطيع تعديل العملية في {title}؟", f"نعم. أعد {focus} في {title} بعد تغيير إعداد واحد؛ هكذا يوضح {title} ما الذي أثّر في الناتج."),
        (f"متى أحتاج مراجعة إضافية لنتيجة {title}؟", f"عندما يمس {focus} عبر {title} نشرًا عامًا أو عميلًا أو بيانات حساسة. اختبر نسخة {title} قبل الاعتماد."),
    ]
    return {"h2": f"دليل {title} العملي", "intro": intros, "steps": steps, "cases": cases, "tips": tips, "faq": faq, "keywords": f"{title}، {CATEGORY_KEYWORDS_AR[cat]}"}


def generic_record_en(tool: dict) -> dict:
    title, cat, slug = tool["title"], tool["cat"], tool["slug"]
    focus = FOCUS_EN.get(slug, tool["desc"].rstrip("."))
    input_, config, output, check = CAT_EN[cat]
    v = variant(slug)
    intros = [
        [f"{title} provides a practical route for {focus}. It makes the {title} decision reviewable instead of leaving you with unexplained output.", f"{title} starts with {input_}. While you are {focus}, set {config}, then inspect {output} before using it in the next part of your project."],
        [f"The specific job of {title} is {focus}. In {title}, the useful part is seeing which input and choices change that specific outcome.", f"Add {input_} to {title}, then connect {config} to the goal of {focus}. You will receive {output} to review in the context of real work."],
        [f"When you need {focus}, {title} makes the path shorter and more explicit. {title} still benefits from professional review, but {focus} starts from an organized result.", f"With {title}, you work from {input_} and choose {config}. That creates {output}; test it before it affects a publication or delivery."],
        [f"{title} supports one clear decision: {focus}. This {title} guide connects each input with the version of {focus} you can use or improve.", f"Begin with {input_} in {title}. Choose {config} for {focus}, then review {output} deliberately rather than cosmetically."],
    ][v]
    steps = [
        (f"Prepare {input_}", f"Start {title} from a reliable source. For {focus} in {title}, prefer current input; a partial {title} source weakens {focus}."),
        (f"Define the goal of {focus}", f"Add values in the correct {title} fields. Link each value to {focus} inside {title}; this prevents a mismatched context."),
        (f"Set {config}", f"Set the real case in {title}. For {focus}, change one {title} option at a time and observe its effect."),
        (f"Read {output}", f"After {title} runs, compare {output} with {focus}. A {title} warning now is safer than a late public error."),
        ("Approve the version you checked", f"After {focus} with {title}, complete your project review. Save the {title} version that represents approved {focus}."),
    ]
    cases = [
        f"Before {title} delivers work that needs {focus} against clear requirements.",
        f"When {focus} needs a team review, {title} keeps the choices visible instead of opaque.",
        f"When {focus} from {title} becomes part of a page, message or file needing a final check.",
        f"To create an initial {title} version of {focus}, then adapt it within {title} for the target context.",
    ]
    tips = [
        f"In {title}, preserve the original so {focus} remains reversible and comparable in {title}.",
        f"When {focus} enters team work, record inside {title} why each {title} setting was chosen.",
        f"Before approving {focus}, check where the {title} output will appear, not only the {title} window.",
        f"A tighter target for {focus} gives {title} less noise and makes its {title} result easier to validate.",
    ]
    faq = [
        (f"What input fits {title}?", f"{title} uses {input_}. For {focus} in {title}, choose a current source; missing material changes the {title} result."),
        (f"How do I know {title} reached my goal?", f"Compare {output} with the target for {focus}, then complete the {title} review in its final destination."),
        (f"Can I adjust a {title} process?", f"Yes. Run {focus} in {title} after one setting change; {title} will show what affected the output."),
        (f"When does a {title} result need extra review?", f"When {focus} through {title} affects public work, a client or sensitive data. Test the {title} copy before approval."),
    ]
    return {"h2": f"Practical guide to {title}", "intro": intros, "steps": steps, "cases": cases, "tips": tips, "faq": faq, "keywords": f"{title}, {CATEGORY_KEYWORDS_EN[cat]}"}


def normalize_content(content: dict) -> dict:
    """The hand-written image source may contain string tuples after editing; normalize it."""
    out = dict(content)
    out["cases"] = [x[0] if isinstance(x, tuple) else x for x in content["cases"]]
    out["tips"] = [x[0] if isinstance(x, tuple) else x for x in content["tips"]]
    return out


def record_for(tool: dict, lang: str) -> dict:
    if lang == "AR" and tool["slug"] in IMAGE_COPY_AR:
        record = normalize_content(IMAGE_COPY_AR[tool["slug"]])
        record["keywords"] = f"{tool['title']}، {CATEGORY_KEYWORDS_AR[tool['cat']]}"
        return record
    return generic_record_ar(tool) if lang == "AR" else generic_record_en(tool)


def render_section(tool: dict, record: dict, all_tools: list[dict], lang: str) -> str:
    title = tool["title"]
    if lang == "AR":
        sections = [("overview", "نظرة سريعة"), ("steps", "خطوات الاستخدام"), ("cases", "متى تفيدك الأداة؟"), ("tips", "نصائح للحصول على نتيجة دقيقة"), ("faq", "أسئلة شائعة"), ("related", "أدوات مرتبطة")]
        kicker = "دليل عملي ومحتوى مراجع"
        step_intro = f"اتبع هذه الخطوات لاستخدام {title} بدقة:"
        cases_intro = f"هذه أمثلة عملية تُظهر متى يكون {title} الاختيار المناسب:"
        tips_intro = f"هذه ملاحظات تخص {title} قبل اعتماد النتيجة النهائية:"
        keyword_label = "مصطلحات بحث ذات صلة"
        related_intro = f"هذه الأدوات قد تكمل الخطوة التالية بعد {title}:"
    else:
        sections = [("overview", "Overview"), ("steps", "How to use it"), ("cases", "When it helps"), ("tips", "Professional notes"), ("faq", "Frequently asked questions"), ("related", "Related tools")]
        kicker = "Practical guide and reviewed content"
        step_intro = f"Follow these steps to use {title} carefully:"
        cases_intro = f"Here are practical moments when {title} is the right choice:"
        tips_intro = f"Use these {title}-specific notes before you rely on the final result:"
        keyword_label = "Related search terms"
        related_intro = f"These tools can help with the next {title} step:"
    nav = "".join(f'<a href="#{sid}">{esc(label)}</a>' for sid, label in sections)
    steps = "".join(f"<li><strong>{esc(name)}</strong><span>{esc(text)}</span></li>" for name, text in record["steps"])
    cases = "".join(f"<li>{esc(item)}</li>" for item in record["cases"])
    tips = "".join(f"<li>{esc(item)}</li>" for item in record["tips"])
    faqs = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in record["faq"])
    rel = related(tool, all_tools, lang)
    related_html = "".join(f'<a class="guide-related-link" href="{local_href(x["slug"])}">{esc(x["title"])}</a>' for x in rel)
    return f'''<section class="tool-guide" aria-labelledby="guide-{esc(tool["slug"])}" data-content-version="2026-09">
  <p class="guide-kicker">{esc(kicker)}</p>
  <h2 id="guide-{esc(tool["slug"])}">{esc(record["h2"])}</h2>
  <nav class="guide-nav" aria-label="{'أقسام الدليل' if lang == 'AR' else 'Guide sections'}">{nav}</nav>
  <div class="guide-section" id="overview"><h3>{esc(sections[0][1])}</h3><p>{esc(record["intro"][0])}</p><p>{esc(record["intro"][1])}</p><p class="tool-keywords"><strong>{esc(keyword_label)}:</strong> {esc(record["keywords"])}</p></div>
  <div class="guide-section" id="steps"><h3>{esc(sections[1][1])}</h3><p>{esc(step_intro)}</p><ol class="guide-steps">{steps}</ol></div>
  <div class="guide-section" id="cases"><h3>{esc(sections[2][1])}</h3><p>{esc(cases_intro)}</p><ul>{cases}</ul></div>
  <div class="guide-section" id="tips"><h3>{esc(sections[3][1])}</h3><p>{esc(tips_intro)}</p><ul>{tips}</ul></div>
  <div class="guide-section guide-faq" id="faq"><h3>{esc(sections[4][1])}</h3>{faqs}</div>
  <div class="guide-section" id="related"><h3>{esc(sections[5][1])}</h3><p>{esc(related_intro)}</p><div class="guide-related">{related_html}</div></div>
</section>'''


def jsonld(tool: dict, record: dict, lang: str) -> str:
    base_url = "https://fawran.tools/" if lang == "AR" else "https://fawran.tools/en/"
    if lang == "AR":
        howto_name = f"طريقة استخدام {tool['title']}"
        qs = ["الأسئلة الشائعة عن", tool["title"]]
    else:
        howto_name = f"How to use {tool['title']}"
        qs = ["Frequently asked questions about", tool["title"]]
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in record["faq"]],
    }
    howto = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": howto_name,
        "description": record["intro"][0],
        "url": f"{base_url}tools/{tool['slug']}.html",
        "step": [{"@type": "HowToStep", "position": i, "name": name, "text": text} for i, (name, text) in enumerate(record["steps"], 1)],
    }
    return '<script type="application/ld+json">' + json.dumps(faq, ensure_ascii=False, separators=(",", ":")) + '</script>\n' + '<script type="application/ld+json">' + json.dumps(howto, ensure_ascii=False, separators=(",", ":")) + '</script>'


def remove_generated_schemas(page: str) -> str:
    """Keep SoftwareApplication/Organization JSON-LD; replace only FAQ and HowTo."""
    def keep_or_remove(match: re.Match) -> str:
        raw = match.group(1).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return match.group(0)
        typ = data.get("@type")
        return "" if typ in {"FAQPage", "HowTo"} else match.group(0)
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', keep_or_remove, page, flags=re.S)


def replace_section(page: str, section: str, lang: str) -> str:
    # Remove every former editorial block. Some older Arabic pages contain both
    # `.enrich` and the later duplicated `.enrich-extra`; a rerun also replaces
    # an existing `.tool-guide` rather than layering a second guide on the page.
    old = re.compile(r'<section class="(?:tool-guide|enrich(?:-[^"]+)?)"[^>]*>.*?</section>', re.S)
    seen = False
    def replace(match: re.Match) -> str:
        nonlocal seen
        if seen:
            return ""
        seen = True
        return section
    page = old.sub(replace, page)
    if seen:
        return page
    # EN pages have the actual tool UI followed by </main> but no editorial section.
    # Two Arabic pages use that structure too after their older extra section is gone.
    if "</main>" not in page:
        raise RuntimeError("No editorial marker or </main> found")
    return page.replace("</main>", section + "\n</main>", 1)


def inject_schemas(page: str, schemas: str) -> str:
    # Keep semantic guide and structured data close to each other, before scripts/body.
    anchor = "</main>"
    if anchor in page:
        return page.replace(anchor, schemas + "\n" + anchor, 1)
    return page.replace("</body>", schemas + "\n</body>", 1)


def process_tool(tool: dict, lang: str, all_tools: list[dict], write: bool) -> tuple[Path, int]:
    path = ROOT / ("tools" if lang == "AR" else "en/tools") / f"{tool['slug']}.html"
    original = path.read_text(encoding="utf-8")
    record = record_for(tool, lang)
    section = render_section(tool, record, all_tools, lang)
    page = remove_generated_schemas(original)
    page = replace_section(page, section, lang)
    page = inject_schemas(page, jsonld(tool, record, lang))
    # A guard makes reruns safe: a source page should have exactly one guide and
    # exactly one FAQ + one HowTo after processing.
    if page.count('class="tool-guide"') != 1:
        raise RuntimeError(f"{path}: expected one tool guide")
    # Count schema script blocks, not strings inside a tool's own JavaScript.
    schema_types = []
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        try:
            schema_types.append(json.loads(block.strip()).get("@type"))
        except json.JSONDecodeError:
            pass
    if schema_types.count("FAQPage") != 1 or schema_types.count("HowTo") != 1:
        raise RuntimeError(f"{path}: structured data injection failed ({schema_types})")
    if write and page != original:
        path.write_text(page, encoding="utf-8")
    return path, len(page.split())


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Render validation only; do not write files")
    args = parser.parse_args()
    totals = {}
    for lang, items in (("AR", AR_TOOLS), ("EN", EN_TOOLS)):
        words = []
        for tool in items:
            _, wc = process_tool(tool, lang, items, write=not args.check)
            words.append(wc)
        totals[lang] = (len(words), min(words), round(sum(words) / len(words)))
    for lang, (count, minimum, average) in totals.items():
        print(f"{lang}: {count} tools | minimum rendered words: {minimum} | average: {average}")


if __name__ == "__main__":
    main()
