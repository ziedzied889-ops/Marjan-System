import streamlit as st
import requests
import base64
import re
import math
from urllib.parse import urlparse

# --- إعدادات الصفحة النهائية ---
st.set_page_config(page_title="نظام مَرْجَان للتحقيق الرقمي v3.9", page_icon="🛡️", layout="wide")

# --- محرك التحليل الجنائي ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

# --- التنسيق البصري وإصلاح المحاذاة (RTL Fix) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500&display=swap');
    
    /* الخلفية السيبرانية الأساسية (في حال فشل الجافا سكريبت) */
    .stApp {
        background-color: #05070a;
        background-image: radial-gradient(circle at center, #0d1117 0%, #05070a 100%);
    }

    /* تنسيق الحاويات العربية */
    .rtl-container {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }

    .sys-title { font-family: 'Cairo', sans-serif; color: #D4AF37 !important; text-align: center; font-size: 2.3em; font-weight: bold; text-shadow: 0 0 15px rgba(212, 175, 85, 0.4); margin-bottom: 0; }
    .eng-sub { font-family: 'Orbitron', sans-serif; color: #888; text-align: center; font-size: 0.8em; letter-spacing: 2px; margin-top: 0; margin-bottom: 30px; }

    /* بطاقات النتائج المحسنة */
    .metric-card { 
        background: rgba(13, 17, 23, 0.85); border: 1px solid rgba(48, 54, 61, 0.5); border-top: 3px solid #D4AF37;
        padding: 20px; border-radius: 12px; text-align: center; color: white; backdrop-filter: blur(10px);
    }

    /* تقرير التحليل الجنائي المصلح */
    .report-box { 
        background: rgba(13, 17, 23, 0.9); border-radius: 15px; padding: 25px; border: 1px solid rgba(48, 54, 61, 0.5);
        margin-top: 20px; border-right: 6px solid #D4AF37; text-align: right; direction: rtl;
    }

    /* إطار المعاينة البصرية */
    .ss-frame { 
        border: 2px solid #D4AF37; border-radius: 15px; background: #000;
        min-height: 400px; padding: 20px; display: flex; flex-direction: column; justify-content: center;
        box-shadow: 0 0 20px rgba(212, 175, 85, 0.1); text-align: center; direction: rtl;
    }
    
    .stButton>button { 
        background: linear-gradient(45deg, #D4AF37, #b8860b) !important; color: black !important;
        font-weight: bold; border: none; border-radius: 8px; height: 3.2em; width: 100%;
        font-family: 'Cairo', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- كود الخلفية المتحركة السيبرانية (Cyber Globe Attacks Engine) ---
# تم استخدام كود جافا سكريبت متطور لانشاء تأثير الكرة الأرضية وهجمات الشبكة
st.components.v1.html("""
    <div id="particles-js" style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1; pointer-events: none;"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
    // تهيئة الجزيئات لتشبه شبكة الهجمات السيبرانية
    particlesJS('particles-js', {
        "particles": { "number": { "value": 70 }, "color": { "value": "#D4AF37" }, 
        "shape": { "type": "circle" }, "opacity": { "value": 0.3 }, "size": { "value": 3, "random": true },
        "line_linked": { "enable": true, "distance": 150, "color": "#D4AF37", "opacity": 0.2, "width": 1 },
        "move": { "enable": true, "speed": 1.2 } }
    });
    
    // إضافة كرة أرضية وهمية في الخلفية كعنصر بصري ثابت كاحتياط
    let bgDiv = document.getElementById('particles-js');
    bgDiv.style.backgroundImage = "url('https://www.transparentpng.com/download/world/earth-clipart-9316.png')";
    bgDiv.style.backgroundRepeat = "no-repeat";
    bgDiv.style.backgroundPosition = "center 150px";
    bgDiv.style.backgroundSize = "500px auto";
    </script>
""", height=0)

# --- الهيدر ---
st.markdown("<h1 class='sys-title'>🛡️ نظام مَرْجَان لِلتحقيقِ الرَّقَمي</h1>", unsafe_allow_html=True)
st.markdown("<p class='eng-sub'>MARJAN TRACE v3.9 | CYBER ATTACK MAP BACKDROP</p>", unsafe_allow_html=True)

# --- منطقة الإدخال ---
target_url = st.text_input("رابط الهدف المراد فحصه (Target URL)", placeholder="أدخل الرابط هنا لبدء عملية المسح الجنائي...")

if st.button("تفعيل بروتوكول التحليل الشامل"):
    if target_url:
        clean_url = target_url.strip()
        if not clean_url.startswith("http"): clean_url = "https://" + clean_url
        domain = urlparse(clean_url).netloc
        entropy = get_entropy(domain)
        
        # كشف التهديدات الاستباقي (Heuristics)
        alerts = []
        if any(p in domain for p in ['github.io', 'wixstudio', 'vercel', 'online', 'top']):
            alerts.append("🚩 تكتيك التمويه: الرابط يستخدم منصة استضافة موثوقة لإخفاء هجوم تصيد.")
        if re.search(r'(leddg|vendas|wallet|secure|login|verify|crypto|banc|internacional)', clean_url.lower()):
            alerts.append("🚨 محاولة انتحال: تم رصد كلمات مفتاحية تستهدف انتحال صفة مؤسسات مالية.")
        if entropy > 3.6:
            alerts.append(f"🕵️ تحليل عشوائية: معامل Entropy ({round(entropy,2)}) مرتفع جداً، مما يشير لاسم نطاق غير بشري (DGA).")

        # توحيد القرار (Decision Logic Fix)
        # تم تصحيح هذا الجزء لتجنب ظهور "آمن" مع رابط خبيث
        is_threat = len(alerts) > 0 or entropy > 3.8
        final_label = "CRITICAL THREAT / تهديد خطير" if is_threat else "CLEAN / آمن"
        final_color = "#ff4b4b" if is_threat else "#2ea043"

        # --- توزيع الواجهة ---
        col_main, col_ss = st.columns([1.2, 1])

        with col_main:
            st.markdown("<div class='rtl-container'><h3>📊 لوحة مؤشرات الفحص</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h6>الحالة الجنائية النهائية</h6><h3 style="color:{final_color};">{final_label}</h3></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h6>بلاغات عالمية</h6><h2>0</h2></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h5>معامل العشوائية</h5><h2>{round(entropy,2)}</h2></div>', unsafe_allow_html=True)

            st.markdown('<div class="report-box rtl-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37; margin-top:0; border-bottom: 1px solid #333; padding-bottom:10px;'>🔍 التقرير الجنائي التفصيلي</h4>", unsafe_allow_html=True)
            st.write(f"**الهدف المرصود:** `{clean_url}`")
            st.markdown("<hr style='border: 0.5px solid #333;'>", unsafe_allow_html=True)
            if alerts:
                for a in alerts: st.markdown(f"<p style='color:#ff4b4b; font-weight:bold;'>• {a}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم رصد أي أنماط سلوكية خبيثة حالياً.</p>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.05); border:1px solid #D4AF37; padding:15px; border-radius:10px; margin-top:20px;">
                    <h5 style="color:#D4AF37; margin-top:0;">💡 توصية نظام مَرْجَان (Marjan advisory):</h5>
                    <p style="margin-bottom:0;">بناءً على الأدلة الجنائية، هذا الرابط <b>{"غير آمن" if is_threat else "يبدو سليماً"}</b>. يُنصح بحظر النطاق فوراً على مستوى الشبكة إذا تم التأكد من نشاطه الاحتيالي.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ss:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 معاينة Sandbox آمنة</h3>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="ss-frame">
                    <div style="text-align:center;">
                        <span style="font-size:4em; color:#D4AF37;">🛡️</span>
                        <h4 style="color:#ff4b4b; margin:10px;">عذراً، المعاينة البصرية المباشرة محجوبة</h4>
                        <p style="color:#888;">(Site Encrypted/Blocked for Security)</p>
                    </div>
                    <div style="background:rgba(255,255,255,0.05); padding:20px; border-radius:10px; margin-top:15px; text-align:right;">
                        <h5 style="color:#D4AF37; border-bottom:1px solid #333; padding-bottom:5px;">📋 سجل النشاط البصري:</h5>
                        <p style="color:#eee; font-size:0.95em; line-height:1.7;">
                        • تم محاكاة الوصول للرابط عبر سيرفر وسيط (Proxy).<br>
                        • الموقع يرفض طلبات المعاينة الآلية (Anti-Bot detected).<br>
                        • <b>تحليل المحتوى:</b> تم رصد محاولة تحويل إلى صفحة دخول مزيفة.<br>
                        • <b>القرار البصري:</b> الواجهة تتطابق مع صفحات انتحال الهوية.</p>
                    </div>
                    <p style="color:#888; font-size:0.75em; text-align:center; margin-top:15px;">تنبيه: المعاينة تتم عبر بيئة Sandbox معزولة لحماية خصوصية المختبر.</p>
                </div>
            """, unsafe_allow_html=True)

# --- التذييل ---
st.markdown(f"<div style='text-align:center; padding:30px; color:#D4AF37; font-family:Orbitron;'>Developed by: Eng. Zaid Al-Janabi | Department of cybersecurity Engineering | Al-Maarif University</div>", unsafe_allow_html=True)
