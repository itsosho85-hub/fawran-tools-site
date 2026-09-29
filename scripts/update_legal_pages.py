#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refresh the four legal documents with source-accurate, non-duplicated copy."""
from pathlib import Path
import re, json

ROOT = Path(__file__).resolve().parents[1]
DATE_AR = "29 سبتمبر 2026"
DATE_EN = "29 September 2026"

LEGAL_CSS = r'''
/* legal-page-refresh */
.legal-summary{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:start;margin:0 0 24px;padding:18px 20px;border:1px solid rgba(79,63,240,.22);border-radius:14px;background:linear-gradient(135deg,rgba(79,63,240,.10),rgba(240,169,59,.10));}
.legal-summary .legal-icon{display:grid;place-items:center;width:42px;height:42px;border-radius:12px;background:var(--indigo-deep,#4F3FF0);color:#fff;font-size:21px;font-weight:900;}
.legal-summary h2{margin:0 0 4px!important;font-size:17px!important;}.legal-summary p{margin:0!important;color:var(--ink-soft);line-height:1.85;}
.legal-section{padding-top:4px;}.legal-section h2{padding-bottom:9px;border-bottom:1px solid var(--line);}.legal-section h3{font-size:15px;margin:18px 0 7px;}
.legal-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:14px 0;}.legal-grid>div{padding:14px;border:1px solid var(--line);border-radius:11px;background:var(--surface-sunk,#f8f7ff);}.legal-grid strong{display:block;margin-bottom:4px;color:var(--ink);}.legal-grid p{margin:0!important;font-size:13.5px!important;}
.legal-note{margin:14px 0;padding:13px 15px;border-inline-start:3px solid var(--gold,#F0A93B);border-radius:0 9px 9px 0;background:rgba(240,169,59,.10);font-size:14px;line-height:1.9;}.legal-note strong{color:var(--ink);}.legal-status{display:inline-flex;align-items:center;gap:6px;margin:0 0 13px;padding:4px 9px;border-radius:999px;background:rgba(11,136,81,.10);color:#087044;font-size:12px;font-weight:800;}
.data-table caption{padding:0 0 8px;text-align:start;font-weight:800;color:var(--ink);}.data-table code{font-family:var(--mono,monospace);font-size:12px;word-break:break-word;}[data-theme="dark"] .legal-grid>div{background:rgba(255,255,255,.035);}[data-theme="dark"] .legal-summary{background:linear-gradient(135deg,rgba(111,94,255,.16),rgba(240,169,59,.10));}
@media(max-width:640px){.legal-summary{grid-template-columns:1fr;padding:16px;}.legal-grid{grid-template-columns:1fr;}.legal-summary .legal-icon{width:36px;height:36px;}.legal-note{font-size:13px;}}
/* end legal-page-refresh */
'''

PRIVACY_AR = f'''<main id="main-content">
<div class="wrap">
  <div class="page-head"><h1>سياسة الخصوصية</h1><p>آخر تحديث: {DATE_AR}</p></div>
  <div class="legal-summary"><div class="legal-icon" aria-hidden="true">⌁</div><div><h2>ملخص واضح قبل البدء</h2><p>تشرح هذه السياسة البيانات التي يتعامل معها موقع فورا.tools، ومتى تبقى في متصفحك ومتى يتصل الموقع بخدمة خارجية. معظم عمليات الملفات والنصوص تتم محليًا، لكن ذلك لا ينطبق تلقائيًا على كل أداة أو كل خدمة خارجية.</p></div></div>
  <div class="toc"><h2>محتوى الصفحة</h2><ul>
    <li><a href="#scope">١. نطاق السياسة</a></li><li><a href="#local-processing">٢. الملفات والمحتوى داخل المتصفح</a></li>
    <li><a href="#browser-storage">٣. التخزين على جهازك</a></li><li><a href="#analytics">٤. التحليلات وسجلات الخدمة</a></li>
    <li><a href="#ratings">٥. التقييمات</a></li><li><a href="#external">٦. الطلبات والخدمات الخارجية</a></li>
    <li><a href="#ads">٧. الإعلانات وملفات تعريف الارتباط</a></li><li><a href="#contact-data">٨. التواصل ومشاركة البيانات</a></li>
    <li><a href="#retention">٩. الاحتفاظ والأمان</a></li><li><a href="#choices">١٠. خياراتك وحقوقك</a></li>
    <li><a href="#children">١١. الأطفال والتعديلات</a></li><li><a href="#privacy-contact">١٢. التواصل بشأن الخصوصية</a></li>
  </ul></div>
  <article class="content-card">
    <section class="legal-section" id="scope"><h2>١. نطاق هذه السياسة</h2><p>تسري هذه السياسة على موقع <strong>فورا.tools</strong> وصفحاته وأدواته المجانية. لا ينشئ الموقع حساب مستخدم للوصول إلى الأدوات، ولا نطلب منك اسمًا أو رقم هاتف أو كلمة مرور لاستخدام وظائفه الأساسية. قد تختلف معالجة البيانات عندما تختار استخدام خدمة تابعة لطرف ثالث أو تراسلنا بنفسك.</p><div class="legal-note"><strong>القاعدة العملية:</strong> اقرأ وصف الأداة قبل إدخال رابط أو مفتاح API أو ملف حساس. إذا كانت الأداة تحتاج اتصالًا بخدمة خارجية، نوضح ذلك في هذه الصفحة وفي سياق الأداة قدر الإمكان.</div></section>
    <section class="legal-section" id="local-processing"><h2>٢. الملفات والنصوص داخل المتصفح</h2><p>تصمم غالبية أدوات الصور وPDF والنصوص والمطورين لمعالجة مدخلاتك محليًا داخل متصفحك باستخدام تقنيات المتصفح. في هذه الحالات لا يرسل الموقع ملفك إلى خادم فورا.tools لمجرد اختيارك له أو معالجته داخل الأداة.</p><p>قد يحتفظ المتصفح بالملف أو المعاينة في الذاكرة المؤقتة طوال الجلسة. يزول ذلك عادة عند إغلاق الصفحة أو تحديثها، لكن سلوك الذاكرة والتحميلات يخضع لإعدادات المتصفح وجهازك. احتفظ دائمًا بالنسخة الأصلية، ولا ترفع محتوى لا تملك حق معالجته.</p></section>
    <section class="legal-section" id="browser-storage"><h2>٣. التخزين على جهازك</h2><p>نستخدم التخزين المحلي أو تخزين الجلسة في متصفحك لتحسين تجربة الزيارة. هذه القيم لا تنتقل إلينا تلقائيًا مع كل زيارة، ويمكنك حذفها من إعدادات المتصفح.</p>
      <table class="data-table"><caption>أمثلة على القيم المخزنة محليًا</caption><thead><tr><th>القيمة أو الفئة</th><th>الغرض</th><th>المكان</th></tr></thead><tbody>
      <tr><td><code>fawran-theme</code></td><td>تذكر الوضع الداكن أو الفاتح</td><td>Local Storage</td></tr>
      <tr><td><code>fawran-favorites</code> و<code>fawran-recent</code></td><td>عرض الأدوات المفضلة والمستخدمة مؤخرًا</td><td>Local Storage</td></tr>
      <tr><td><code>fawran-rated-*</code></td><td>تذكر أن هذا المتصفح أرسل تقييمًا لأداة</td><td>Local Storage</td></tr>
      <tr><td>تفضيلات بعض الأدوات</td><td>مثل آخر زوج عملات أو مفتاح PageSpeed الذي تختار حفظه أو سجل أداة مخصص</td><td>Local Storage</td></tr>
      <tr><td><code>fawran-adblock-dismissed</code></td><td>عدم إظهار تنبيه مانع الإعلانات مرة أخرى في الجلسة نفسها</td><td>Session Storage</td></tr>
      </tbody></table>
      <p>حذف بيانات الموقع من إعدادات المتصفح يزيل هذه القيم من جهازك. لا نخزن كلمات مرورك أو ملفاتك الشخصية ضمن هذه المفاتيح العامة.</p></section>
    <section class="legal-section" id="analytics"><h2>٤. التحليلات وسجلات الخدمة</h2><p>قد نستخدم Google Analytics لفهم استخدام الصفحات بصورة مجمعة، مثل الصفحات المفتوحة، نوع المتصفح، الجهاز، مصدر الزيارة، والتفاعل العام. توفر المتصفحات ومزودو البنية التحتية أيضًا سجلات تقنية معتادة، مثل عنوان IP والتوقيت وبيانات الطلب، لأغراض التشغيل والأمان ومنع الإساءة.</p><p>لا نستخدم هذه البيانات لبناء حساب شخصي لك داخل الموقع. تعامل Google وNetlify أو مزود الاستضافة مع البيانات يخضع كذلك لسياساتهم المستقلة.</p></section>
    <section class="legal-section" id="ratings"><h2>٥. نظام التقييمات</h2><p>عند تقييم أداة، يرسل الموقع إلى وظيفة التقييم الخاصة به <strong>معرّف الأداة</strong> و<strong>عدد النجوم من 1 إلى 5</strong>. تحفظ الخدمة إجمالي عدد التقييمات ومجموعها لإظهار متوسط عام؛ لا نطلب اسمًا أو تعليقًا أو حسابًا لهذا الغرض. ويحتفظ متصفحك بمؤشر محلي لتقليل التقييم المتكرر من الجهاز نفسه.</p></section>
    <section class="legal-section" id="external"><h2>٦. الطلبات والخدمات الخارجية</h2><p>بعض الميزات تعتمد على مورد خارجي لأن وظيفتها لا يمكن تنفيذها من الموقع وحده. عند استخدامك لها، يتلقى ذلك الطرف طلبًا تقنيًا من متصفحك وقد يرى عنوان IP وبيانات المتصفح المعتادة، إضافة إلى المدخل المرتبط بالميزة.</p>
      <div class="legal-grid"><div><strong>الخطوط والمكتبات</strong><p>قد تُحمّل Google Fonts ومكتبات من jsDelivr أو cdnjs لتشغيل واجهة أو معالجة محلية؛ وهي طلبات تحميل عادية من المتصفح.</p></div><div><strong>أسعار العملات</strong><p>تطلب أداة العملات وودجت العملات بيانات أسعار عامة من مزود عملات خارجي لعرض التحويلات.</p></div><div><strong>فحص الموقع</strong><p>عند فحص رابط أو حالة HTTP أو سرعة موقع، قد يُطلب الرابط من متصفحك أو من واجهة Google PageSpeed بحسب الأداة. لا تدخل روابط خاصة أو تحتوي بيانات سرية.</p></div><div><strong>مفتاح PageSpeed</strong><p>إذا أدخلت مفتاح Google PageSpeed API واخترت حفظه، يبقى في Local Storage على جهازك؛ لا نرسله إلى خادم فورا.tools.</p></div></div>
      <p>روابط المشاركة تفتح المنصة التي تختارها، وعندها تسري سياسة تلك المنصة. لا نتحكم في مدى دقة أو إتاحة أو ممارسات الأطراف الخارجية.</p></section>
    <section class="legal-section" id="ads"><h2>٧. الإعلانات وملفات تعريف الارتباط</h2><p>قد يعرض الموقع إعلانات من Google AdSense أو شبكات إعلانية أخرى لتمويل تشغيل الخدمة. عند تفعيل الإعلانات، قد تستخدم Google وشركاؤها ملفات تعريف ارتباط أو معرّفات مشابهة وفق سياساتهم والقواعد المطبقة على منطقتك. يمكنك إدارة الإعلانات المخصصة من <a href="https://adssettings.google.com/" rel="noopener noreferrer" target="_blank">إعدادات إعلانات Google</a> وضبط ملفات الارتباط من متصفحك.</p><p>إذا كانت القواعد في بلدك تفرض موافقة مسبقة على تقنيات إعلانية غير ضرورية، فقد تظهر لك واجهة موافقة عند تفعيلها. تعطيل ملفات الارتباط أو مانع الإعلانات قد يغير بعض وظائف العرض أو التمويل، لكنه لا يمنعك من استخدام الأدوات الأساسية.</p></section>
    <section class="legal-section" id="contact-data"><h2>٨. التواصل ومشاركة البيانات</h2><p>صفحة الاتصال تفتح برنامج البريد على جهازك ولا ترسل النموذج إلى قاعدة بيانات الموقع. إذا أرسلت لنا بريدًا، نستلم الاسم أو عنوان البريد والمحتوى الذي تختار إرساله لنتمكن من الرد أو متابعة الطلب. لا نبيع بياناتك الشخصية، ولا نشاركها لغرض إعلاني مستقل عن تشغيل الموقع، إلا إذا كان ذلك مطلوبًا قانونًا أو ضروريًا لحماية الخدمة وحقوق مستخدميها.</p></section>
    <section class="legal-section" id="retention"><h2>٩. الاحتفاظ والأمان</h2><p>تبقى تفضيلات المتصفح على جهازك حتى تحذفها. تحفظ بيانات التقييمات بصيغة إجمالية ما دامت لازمة لعرض المتوسطات ومنع العبث، وقد تحتفظ جهات الاستضافة أو الأطراف الخارجية بسجلاتها طبقًا لسياساتها. نستخدم إجراءات تقنية معقولة لحماية الموقع، لكن لا توجد خدمة إنترنت خالية من المخاطر؛ لا ترسل معلومات لا ينبغي كشفها عبر روابط أو رسائل عامة.</p></section>
    <section class="legal-section" id="choices"><h2>١٠. خياراتك وحقوقك</h2><ul><li>احذف Local Storage وSession Storage وملفات الارتباط من إعدادات المتصفح.</li><li>لا تحفظ مفتاح API في أداة إن كنت تستخدم جهازًا مشتركًا.</li><li>استخدم إعدادات Google لإدارة الإعلانات والقياس وفق الخيارات المتاحة لك.</li><li>راسلنا لطلب توضيح أو طلب متعلق ببيانات رسالة أرسلتها إلينا؛ قد نحتاج معلومات كافية للتحقق من الطلب.</li></ul></section>
    <section class="legal-section" id="children"><h2>١١. الأطفال والتعديلات</h2><p>الموقع ليس موجّهًا عمدًا إلى جمع بيانات من الأطفال. إذا كنت دون السن الذي يسمح لك بالموافقة الرقمية في بلدك، استخدم الموقع بإشراف ولي الأمر. قد نعدّل هذه السياسة عند تغير وظائف الموقع أو المتطلبات القانونية، وسيظهر تاريخ التحديث أعلى الصفحة.</p></section>
    <section class="legal-section" id="privacy-contact"><h2>١٢. التواصل بشأن الخصوصية</h2><p>للاستفسار عن هذه السياسة أو عن رسالة أرسلتها إلينا، استخدم <a href="contact.html">صفحة التواصل</a> أو راسلنا على <a href="mailto:hello@fawran.tools">hello@fawran.tools</a>. هذه السياسة عامة وليست استشارة قانونية فردية.</p></section>
  </article>
</div>
</main>'''

TERMS_AR = f'''<main id="main-content">
<div class="wrap">
  <div class="page-head"><h1>شروط الاستخدام</h1><p>آخر تحديث: {DATE_AR}</p></div>
  <div class="legal-summary"><div class="legal-icon" aria-hidden="true">§</div><div><h2>فهم سريع للخدمة</h2><p>فورا.tools منصة أدوات مجانية تساعدك على معالجة ملفات ونصوص وإنشاء نتائج عملية داخل المتصفح. هذه الشروط تنظّم طريقة الاستخدام؛ أما تفاصيل البيانات والملفات وملفات الارتباط فتجدها في <a href="privacy.html">سياسة الخصوصية</a> بدل تكرارها هنا.</p></div></div>
  <div class="toc"><h2>محتوى الصفحة</h2><ul>
    <li><a href="#acceptance">١. قبول الشروط</a></li><li><a href="#service">٢. نطاق الخدمة</a></li>
    <li><a href="#use">٣. الاستخدام المسموح</a></li><li><a href="#content">٤. ملفاتك ونتائج الأدوات</a></li>
    <li><a href="#external-terms">٥. خدمات الأطراف الخارجية</a></li><li><a href="#availability">٦. الإتاحة والتحديثات</a></li>
    <li><a href="#ip">٧. الملكية الفكرية</a></li><li><a href="#ads-terms">٨. الإعلانات</a></li>
    <li><a href="#disclaimer">٩. إخلاء المسؤولية</a></li><li><a href="#liability">١٠. حدود المسؤولية</a></li>
    <li><a href="#general">١١. أحكام عامة وتواصل</a></li>
  </ul></div>
  <article class="content-card">
    <section class="legal-section" id="acceptance"><h2>١. قبول الشروط</h2><p>باستخدامك فورا.tools أو أي أداة فيه، تقر بأنك قرأت هذه الشروط وتوافق على الالتزام بها. إذا لم توافق عليها، توقف عن استخدام الموقع. استمرار الاستخدام بعد نشر نسخة محدثة يعني قبولك للنسخة الجديدة في حدود ما يسمح به القانون.</p></section>
    <section class="legal-section" id="service"><h2>٢. نطاق الخدمة</h2><p>يوفر الموقع أدوات مساعدة للصور وPDF والنصوص والتطوير وSEO والمواقع ويوتيوب. تقدم الأدوات لأغراض عامة ومعلوماتية وإنتاجية، ولا تمثل مشورة قانونية أو مالية أو طبية أو مهنية متخصصة. لا يتطلب الموقع حسابًا للوصول إلى وظائفه الأساسية، وقد تتغير الأدوات أو خصائصها أو تتوقف دون أن يشكل ذلك التزامًا باستمرار خدمة بعينها.</p><div class="legal-note"><strong>النتائج تحتاج مراجعة:</strong> راجع المخرجات قبل استخدامها في عقد، قرار مالي، ملف رسمي، نشر عام، أو أي موقف تكون فيه الدقة ذات أثر مهم.</div></section>
    <section class="legal-section" id="use"><h2>٣. الاستخدام المسموح</h2><p>يمكنك استخدام الأدوات بصورة شخصية أو مهنية مشروعة، بشرط ألا:</p><ul><li>تدخل أو تعالج محتوى لا تملك حق استخدامه أو ينتهك خصوصية أو حقوق الآخرين.</li><li>تحاول تعطيل الموقع أو تجاوز الحماية أو إجراء طلبات آلية مفرطة تضر بالخدمة.</li><li>تستخدم الأدوات لإنشاء أو نشر محتوى غير قانوني أو احتيالي أو ضار أو يحض على العنف والكراهية.</li><li>تعيد بيع الموقع أو تمثل الأدوات على أنها خدمتك أو تضمنها في منتج تجاري دون موافقة كتابية.</li><li>تنسب إلى الموقع نتيجة أو موافقة أو شراكة غير موجودة.</li></ul><p>إذا كنت قاصرًا وفق قوانين بلدك، استخدم الموقع بإشراف ولي الأمر عند الحاجة.</p></section>
    <section class="legal-section" id="content"><h2>٤. ملفاتك ونتائج الأدوات</h2><p>تبقى حقوقك في الملفات والنصوص التي تختار معالجتها لك أو لمالكها. أنت مسؤول عن وجود الحق أو الإذن اللازم لاستخدام ما تدخله. لا ننقل إليك حقوقًا في محتوى طرف ثالث، ولا تمنحنا ملكية ملفاتك لمجرد استخدامك للأداة.</p><p>قد تؤدي التحويلات أو الضغط أو التوليد إلى نتيجة غير مناسبة لحالتك أو إلى فقدان جودة أو بيانات. احفظ النسخة الأصلية واختبر الناتج قبل الاعتماد عليه. لا تعتمد على نتيجة أداة لاتخاذ قرار قانوني أو طبي أو استثماري دون مراجعة مختص مؤهل.</p></section>
    <section class="legal-section" id="external-terms"><h2>٥. خدمات الأطراف الخارجية</h2><p>تتطلب بعض الأدوات خدمة خارجية، مثل بيانات أسعار العملات أو Google PageSpeed أو خطوط ومكتبات تشغيل. استخدامك لهذه الميزات قد يخضع لشروط وسياسات ذلك الطرف، وقد ترسل الأداة مدخلًا ضروريًا — مثل رابط عام أو مفتاح API تختاره — مباشرة من متصفحك. أنت مسؤول عن حماية مفاتيحك والالتزام بشروط مزود الخدمة.</p><p>لا نضمن استمرار أو دقة بيانات أي طرف ثالث، ولا نتحمل مسؤولية تغيير واجهاته أو سياساته أو توقفه.</p></section>
    <section class="legal-section" id="availability"><h2>٦. الإتاحة والتحديثات والتقييمات</h2><p>نسعى لتشغيل الموقع بصورة مستقرة، لكن لا نضمن أن تكون الخدمة متاحة دائمًا أو خالية من الأخطاء أو مناسبة لكل جهاز ومتصفح. يجوز لنا إصلاح أداة أو تعديلها أو تقييدها أو إيقافها لأسباب تشغيلية أو أمنية أو قانونية.</p><p>تقييمات الأدوات تعكس متوسط النجوم المرسل من الزوار ولا تمثل توصية مهنية أو وعدًا بجودة ثابتة. يجوز معالجة التقييمات الإجمالية عند وجود نشاط آلي أو تلاعب ظاهر لحماية نزاهة النظام.</p></section>
    <section class="legal-section" id="ip"><h2>٧. الملكية الفكرية</h2><p>اسم فورا.tools وشعاره وهوية الموقع وتصميمه ومحتوى الأدلة والشفرة الخاصة به محمية بالحقوق المعمول بها، باستثناء الحقوق الخاصة بالمكتبات مفتوحة المصدر وأصحابها. يمكنك استخدام الموقع كما تتيحه واجهته، لكن لا يجوز نسخ أجزاء جوهرية منه أو إعادة نشرها أو إنشاء خدمة منافسة منه دون إذن كتابي.</p></section>
    <section class="legal-section" id="ads-terms"><h2>٨. الإعلانات</h2><p>قد يعرض الموقع إعلانات لتمويل تشغيل الأدوات. قد تكون هذه الإعلانات مقدمة من شبكات خارجية وتخضع لشروطها وسياساتها. لا تعني الإعلانات تأييدًا منا للمنتج أو الخدمة المعلن عنها. راجع <a href="privacy.html#ads">قسم الإعلانات وملفات الارتباط</a> لمعرفة كيفية التعامل مع التقنيات الإعلانية.</p></section>
    <section class="legal-section" id="disclaimer"><h2>٩. إخلاء المسؤولية</h2><p>تقدم الأدوات والمحتوى «كما هي» و«بحسب التوافر». لا نضمن صحة أو اكتمال أو ملاءمة كل نتيجة لغرض محدد، ولا نضمن عدم انقطاع الخدمة أو توافقها مع جميع البيئات. تقع عليك مسؤولية فحص المدخلات والمخرجات وتحديد مدى ملاءمتها لاستخدامك.</p></section>
    <section class="legal-section" id="liability"><h2>١٠. حدود المسؤولية</h2><p>إلى الحد الذي يسمح به القانون، لا يكون فورا.tools أو القائمون عليه مسؤولين عن خسارة بيانات أو أرباح أو أعمال أو أضرار غير مباشرة أو تبعية تنشأ عن استخدام الموقع أو تعذر استخدامه أو الاعتماد على مخرجاته. لا يحد هذا النص من أي حق لا يمكن استبعاده بموجب قانون واجب التطبيق.</p></section>
    <section class="legal-section" id="general"><h2>١١. أحكام عامة وتواصل</h2><p>قد نحدّث هذه الشروط عند تغير الخدمة أو المتطلبات القانونية، ويظهر تاريخ المراجعة في أعلى الصفحة. تخضع العلاقة بينك وبين الموقع للقانون الواجب التطبيق مع الحفاظ على الحقوق الإلزامية للمستهلك في محل إقامته. للاستفسار عن الشروط، استخدم <a href="contact.html">صفحة التواصل</a> أو راسل <a href="mailto:hello@fawran.tools">hello@fawran.tools</a>.</p></section>
  </article>
</div>
</main>'''

PRIVACY_EN = f'''<main id="main-content">
<div class="wrap">
  <div class="page-head"><h1>Privacy Policy</h1><p>Last updated: {DATE_EN}</p></div>
  <div class="legal-summary"><div class="legal-icon" aria-hidden="true">⌁</div><div><h2>A clear summary first</h2><p>This policy explains what Fawran Tools handles, what stays in your browser, and when a feature makes a request to another service. Most file and text work is local, but that is not an automatic promise for every tool or external feature.</p></div></div>
  <div class="toc"><h2>On this page</h2><ul>
    <li><a href="#scope">1. Scope</a></li><li><a href="#local-processing">2. Files and browser processing</a></li>
    <li><a href="#browser-storage">3. Storage on your device</a></li><li><a href="#analytics">4. Analytics and service logs</a></li>
    <li><a href="#ratings">5. Ratings</a></li><li><a href="#external">6. External requests and services</a></li>
    <li><a href="#ads">7. Advertising and cookies</a></li><li><a href="#contact-data">8. Contact and sharing</a></li>
    <li><a href="#retention">9. Retention and security</a></li><li><a href="#choices">10. Your choices and rights</a></li>
    <li><a href="#children">11. Children and changes</a></li><li><a href="#privacy-contact">12. Privacy contact</a></li>
  </ul></div>
  <article class="content-card">
    <section class="legal-section" id="scope"><h2>1. Scope of this policy</h2><p>This policy applies to the Fawran Tools website, its pages and its free utilities. The core tools do not require an account, name, phone number or password. Processing can differ when you choose a third-party feature or contact us directly.</p><div class="legal-note"><strong>A practical rule:</strong> read a tool's description before entering a URL, API key or sensitive file. Where a feature needs an external service, this page and the tool context identify that as clearly as possible.</div></section>
    <section class="legal-section" id="local-processing"><h2>2. Files and text in your browser</h2><p>Most image, PDF, text and developer tools are designed to process the material you provide locally in your browser using browser technologies. Selecting or processing a file in those tools does not by itself upload that file to a Fawran Tools server.</p><p>Your browser may hold a file or preview in temporary memory while the page is open. It normally disappears when you refresh or close the page, subject to your device and browser settings. Keep an original copy and do not process material you do not have a right to use.</p></section>
    <section class="legal-section" id="browser-storage"><h2>3. Storage on your device</h2><p>We use browser local storage and session storage to make a visit more useful. Those values are not automatically sent to us on every visit, and you can remove them in your browser settings.</p>
      <table class="data-table"><caption>Examples of browser-stored values</caption><thead><tr><th>Value or group</th><th>Purpose</th><th>Location</th></tr></thead><tbody>
      <tr><td><code>fawran-theme</code></td><td>Remember a light or dark appearance</td><td>Local Storage</td></tr>
      <tr><td><code>fawran-favorites</code> and <code>fawran-recent</code></td><td>Show favorite and recently used tools</td><td>Local Storage</td></tr>
      <tr><td><code>fawran-rated-*</code></td><td>Remember that this browser rated a tool</td><td>Local Storage</td></tr>
      <tr><td>Selected tool preferences</td><td>For example, a currency pair, a saved PageSpeed key, or a tool-specific browser history</td><td>Local Storage</td></tr>
      <tr><td><code>fawran-adblock-dismissed</code></td><td>Avoid repeating an ad-block notice in the same session</td><td>Session Storage</td></tr>
      </tbody></table><p>Clearing site data removes these values from your device. We do not use these general keys to store your passwords or personal files.</p></section>
    <section class="legal-section" id="analytics"><h2>4. Analytics and service logs</h2><p>We may use Google Analytics to understand aggregated use of pages, including pages viewed, browser and device type, traffic source and general interaction. Browsers and infrastructure providers also create ordinary technical logs such as IP address, request time and request data for operation, security and abuse prevention.</p><p>We do not create a Fawran Tools user account profile from this information. Google, Netlify and other infrastructure providers handle data under their own policies as well.</p></section>
    <section class="legal-section" id="ratings"><h2>5. Tool ratings</h2><p>When you rate a tool, the site sends the <strong>tool identifier</strong> and a <strong>one-to-five-star value</strong> to its rating function. The service keeps an aggregate count and total to display an average; it does not request a name, comment or account for that purpose. Your browser stores a local marker to reduce repeat ratings from the same device.</p></section>
    <section class="legal-section" id="external"><h2>6. External requests and services</h2><p>Some features rely on an external resource because the job cannot be performed by the site alone. When you use one, that provider receives a technical request from your browser and may receive standard connection data such as IP address and browser information, plus the input relevant to the feature.</p>
      <div class="legal-grid"><div><strong>Fonts and libraries</strong><p>Google Fonts and libraries from jsDelivr or cdnjs may load to render the interface or enable local processing; these are normal browser asset requests.</p></div><div><strong>Currency rates</strong><p>The currency converter and currency widget request public exchange-rate data from an external currency-data provider.</p></div><div><strong>Site checks</strong><p>When you check a URL, HTTP status or site speed, the URL can be requested by your browser or by the Google PageSpeed interface, depending on the tool. Do not enter private or secret URLs.</p></div><div><strong>PageSpeed API key</strong><p>If you enter a Google PageSpeed API key and choose to save it, it remains in local storage on your device; Fawran Tools does not receive it on its server.</p></div></div>
      <p>Sharing links open the platform you select, where that platform's policy applies. We do not control external providers' availability, accuracy or privacy practices.</p></section>
    <section class="legal-section" id="ads"><h2>7. Advertising and cookies</h2><p>The site may display Google AdSense or other advertising-network ads to help fund the free service. When advertising is enabled, Google and its partners may use cookies or similar identifiers under their policies and rules that apply in your region. You can manage personalized ads through <a href="https://adssettings.google.com/" rel="noopener noreferrer" target="_blank">Google Ad Settings</a> and manage cookies in your browser.</p><p>If rules in your country require consent before non-essential advertising technology is used, a consent interface may be shown when it is enabled. Blocking cookies or ads can change some display or funding behavior but does not prevent access to the core tools.</p></section>
    <section class="legal-section" id="contact-data"><h2>8. Contact and data sharing</h2><p>The contact page opens your device's email app; it does not submit the form to a Fawran Tools database. If you email us, we receive the address, name and message you choose to send so we can reply or handle the request. We do not sell personal information or share it for an independent advertising purpose, except where disclosure is legally required or necessary to protect the service and its users.</p></section>
    <section class="legal-section" id="retention"><h2>9. Retention and security</h2><p>Browser preferences remain on your device until you remove them. Rating data is kept as aggregate information while needed to show averages and address manipulation. Hosts and external providers may retain their own logs under their policies. We use reasonable technical measures to protect the site, but no internet service is risk-free; do not place information in public URLs or messages that should remain secret.</p></section>
    <section class="legal-section" id="choices"><h2>10. Your choices and rights</h2><ul><li>Clear local storage, session storage and cookies in your browser settings.</li><li>Do not save an API key in a tool when using a shared device.</li><li>Use Google settings to manage advertising and measurement where options are available.</li><li>Contact us to request clarification or make a request about information in a message you sent us; we may need enough detail to verify the request.</li></ul></section>
    <section class="legal-section" id="children"><h2>11. Children and changes</h2><p>The site is not designed to knowingly collect children's data. If you are below the age at which you can provide digital consent where you live, use the site with a parent or guardian where required. We may revise this policy when the service or legal requirements change; the revision date appears at the top of this page.</p></section>
    <section class="legal-section" id="privacy-contact"><h2>12. Privacy contact</h2><p>For questions about this policy or a message you sent us, use the <a href="contact.html">contact page</a> or email <a href="mailto:hello@fawran.tools">hello@fawran.tools</a>. This policy is general information, not individual legal advice.</p></section>
  </article>
</div>
</main>'''

TERMS_EN = f'''<main id="main-content">
<div class="wrap">
  <div class="page-head"><h1>Terms of Use</h1><p>Last updated: {DATE_EN}</p></div>
  <div class="legal-summary"><div class="legal-icon" aria-hidden="true">§</div><div><h2>How the service is offered</h2><p>Fawran Tools is a free collection of browser utilities for files, text and everyday web tasks. These terms govern use of the tools. Details about files, browser storage and cookies are in the <a href="privacy.html">Privacy Policy</a> rather than repeated here.</p></div></div>
  <div class="toc"><h2>On this page</h2><ul>
    <li><a href="#acceptance">1. Acceptance</a></li><li><a href="#service">2. Service scope</a></li>
    <li><a href="#use">3. Acceptable use</a></li><li><a href="#content">4. Your files and results</a></li>
    <li><a href="#external-terms">5. Third-party services</a></li><li><a href="#availability">6. Availability and updates</a></li>
    <li><a href="#ip">7. Intellectual property</a></li><li><a href="#ads-terms">8. Advertising</a></li>
    <li><a href="#disclaimer">9. Disclaimer</a></li><li><a href="#liability">10. Liability</a></li>
    <li><a href="#general">11. General terms and contact</a></li>
  </ul></div>
  <article class="content-card">
    <section class="legal-section" id="acceptance"><h2>1. Acceptance of these terms</h2><p>By using Fawran Tools or any tool on it, you confirm that you have read and agree to these terms. If you do not agree, do not use the site. Continued use after an updated version is posted means acceptance of that version to the extent permitted by law.</p></section>
    <section class="legal-section" id="service"><h2>2. Service scope</h2><p>The site offers utilities for images, PDFs, text, development, SEO, websites and YouTube. The tools are provided for general productivity and informational purposes. They are not legal, financial, medical or other specialist advice. Core features do not require an account, and a tool or feature may change, be restricted or stop without creating a promise of continuing availability.</p><div class="legal-note"><strong>Review matters:</strong> check every output before using it in a contract, financial decision, official document, public publication, or any setting where accuracy has a material effect.</div></section>
    <section class="legal-section" id="use"><h2>3. Acceptable use</h2><p>You may use the tools for lawful personal or professional work. You must not:</p><ul><li>Submit or process material you have no right to use or that violates another person's privacy or rights.</li><li>Disrupt the site, bypass security, or make excessive automated requests that harm the service.</li><li>Use the tools to create or distribute illegal, fraudulent, harmful, violent or hateful material.</li><li>Resell the site, represent the tools as your service, or embed them in a commercial offering without written permission.</li><li>State or imply a Fawran Tools approval, partnership or result that does not exist.</li></ul><p>If local rules treat you as unable to consent to these terms on your own, obtain permission from the responsible adult in your household before using the site.</p></section>
    <section class="legal-section" id="content"><h2>4. Your files and tool results</h2><p>You retain rights in files and text you choose to process, or those rights remain with their owner. You are responsible for having the necessary right or permission to use the material. Using a tool does not transfer third-party rights to you, and it does not give us ownership of your files.</p><p>Conversion, compression or generation can produce a result that does not fit your case or can reduce quality or remove data. Keep the original and test the result before relying on it. Do not use a tool result as the sole basis for a legal, medical or investment decision without qualified review.</p></section>
    <section class="legal-section" id="external-terms"><h2>5. Third-party services</h2><p>Some tools use external services, including currency-rate data, Google PageSpeed, fonts and operational libraries. Use of those features may be subject to the provider's terms and policies. A feature can send a necessary input — such as a public URL or an API key you choose — directly from your browser. You are responsible for protecting your credentials and following the provider's rules.</p><p>We do not guarantee the availability or accuracy of third-party data and are not responsible for a provider changing its API, policies or service.</p></section>
    <section class="legal-section" id="availability"><h2>6. Availability, updates and ratings</h2><p>We aim to keep the site operating reliably, but do not promise uninterrupted, error-free service or compatibility with every device and browser. We may repair, modify, limit or discontinue a tool for operational, security or legal reasons.</p><p>Tool ratings are visitor-submitted star averages. They are not professional recommendations or a promise of a fixed level of quality. Aggregate ratings may be addressed where there is apparent automated activity or manipulation.</p></section>
    <section class="legal-section" id="ip"><h2>7. Intellectual property</h2><p>The Fawran Tools name, logo, site identity, design, guide content and proprietary code are protected by applicable rights, apart from open-source libraries and their owners' rights. You may use the site through its provided interface, but may not copy substantial parts, republish them, or build a competing service from them without written permission.</p></section>
    <section class="legal-section" id="ads-terms"><h2>8. Advertising</h2><p>The site may display advertising to fund the free tools. Ads can be served by outside networks and are subject to those networks' policies. An advertisement is not our endorsement of the advertised product or service. See the <a href="privacy.html#ads">advertising and cookies section</a> for information about advertising technologies.</p></section>
    <section class="legal-section" id="disclaimer"><h2>9. Disclaimer</h2><p>The tools and content are provided “as is” and “as available.” We do not warrant that every result is accurate, complete or suitable for a particular purpose, or that the service will be uninterrupted or compatible with every environment. You are responsible for checking input, output and suitability for your use.</p></section>
    <section class="legal-section" id="liability"><h2>10. Limitation of liability</h2><p>To the extent permitted by law, Fawran Tools and those operating it are not liable for lost data, profits or business, or indirect or consequential loss arising from use of, inability to use, or reliance on the site or its outputs. This does not limit any right that cannot lawfully be excluded.</p></section>
    <section class="legal-section" id="general"><h2>11. General terms and contact</h2><p>We may revise these terms for operational or regulatory reasons and will publish the current version at this address with its effective date. The relationship between you and the site is subject to applicable law while preserving mandatory consumer rights where you live. For a terms question, send it to <a href="mailto:hello@fawran.tools">hello@fawran.tools</a> with “Terms” in the subject line.</p></section>
  </article>
</div>
</main>'''

PAGES = {
    "privacy.html": {
        "main": PRIVACY_AR, "title": "سياسة الخصوصية وملفات الارتباط | فورا.tools", "description": "سياسة خصوصية فورا.tools: معالجة الملفات داخل المتصفح، التخزين المحلي، التحليلات، الإعلانات والخدمات الخارجية.", "og": "سياسة الخصوصية | فورا.tools", "lang": "ar", "url": "https://fawran.tools/privacy.html"},
    "terms.html": {
        "main": TERMS_AR, "title": "شروط الاستخدام وإخلاء المسؤولية | فورا.tools", "description": "شروط استخدام فورا.tools: نطاق الخدمة، الاستخدام المسموح، مخرجات الأدوات، والخدمات الخارجية.", "og": "شروط الاستخدام | فورا.tools", "lang": "ar", "url": "https://fawran.tools/terms.html"},
    "en/privacy.html": {
        "main": PRIVACY_EN, "title": "Privacy Policy & Cookies | Fawran Tools", "description": "Fawran Tools privacy policy: browser processing, local storage, analytics, advertising and external services.", "og": "Privacy Policy | Fawran Tools", "lang": "en", "url": "https://fawran.tools/en/privacy.html"},
    "en/terms.html": {
        "main": TERMS_EN, "title": "Terms of Use & Disclaimer | Fawran Tools", "description": "Fawran Tools terms: service scope, acceptable use, tool outputs and third-party services.", "og": "Terms of Use | Fawran Tools", "lang": "en", "url": "https://fawran.tools/en/terms.html"},
}


def tag_meta(attr, value, content):
    return f'<meta {attr}="{value}" content="{content}"/>'


def set_meta(page, attr, value, content):
    pattern = rf'<meta\b(?=[^>]*\b{attr}="{re.escape(value)}")[^>]*?/?>'
    repl = tag_meta(attr, value, content)
    if re.search(pattern, page):
        return re.sub(pattern, repl, page, count=1)
    return page.replace('</head>', repl + '\n</head>', 1)


def update(path, conf):
    page = (ROOT / path).read_text(encoding="utf-8")
    page = re.sub(r'<main id="main-content"[^>]*>.*?</main>', conf["main"], page, count=1, flags=re.S)
    page = re.sub(r'<title>.*?</title>', f'<title>{conf["title"]}</title>', page, count=1, flags=re.S)
    page = set_meta(page, "name", "description", conf["description"])
    page = set_meta(page, "property", "og:title", conf["og"])
    page = set_meta(page, "property", "og:description", conf["description"])
    page = set_meta(page, "name", "twitter:title", conf["og"])
    page = set_meta(page, "name", "twitter:description", conf["description"])
    # Replace only the style fragment managed by this script, then append it to
    # the existing legal page styles so these styles never leak to tool pages.
    page = re.sub(r'/\* legal-page-refresh \*/.*?/\* end legal-page-refresh \*/\n?', '', page, flags=re.S)
    page = page.replace('</style>', LEGAL_CSS + '</style>', 1)
    schema = '<script id="legal-webpage-schema" type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "WebPage", "name": conf["og"], "url": conf["url"],
        "inLanguage": conf["lang"], "dateModified": "2026-09-29", "isPartOf": {"@type": "WebSite", "name": "Fawran Tools", "url": "https://fawran.tools/"}
    }, ensure_ascii=False, separators=(",", ":")) + '</script>'
    page = re.sub(r'<script id="legal-webpage-schema" type="application/ld\+json">.*?</script>', '', page, flags=re.S)
    page = page.replace('</head>', schema + '\n</head>', 1)
    (ROOT / path).write_text(page, encoding="utf-8")


if __name__ == "__main__":
    for file, config in PAGES.items():
        update(file, config)
        print(f"updated {file}")
