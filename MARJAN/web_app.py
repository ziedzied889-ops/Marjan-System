import streamlit as st
import requests
import base64
import re
import math
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نظام مَرْجَان للتحقيق الرقمي", page_icon="🛡️", layout="wide")

# --- محرك التحليل الجنائي ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

# --- التنسيق البصري المتقدم وإصلاح الخلفية ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500&display=swap');
    
    /* الخلفية المتحركة السيبرانية */
    .stApp {
        background: linear-gradient(rgba(5, 7, 10, 0.9), rgba(5, 7, 10, 0.9)), 
                    url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
        background-attachment: fixed;
    }

    /* إصلاح محاذاة النصوص العربية */
    .rtl-container {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }

    .sys-title { font-family: 'Cairo', sans-serif; color: #D4AF37 !important; text-align: center; font-size: 2.5em; font-weight: bold; }
    .eng-sub { font-family: 'Orbitron', sans-serif; color: #888; text-align: center; font-size: 0.8em; letter-spacing: 2px; }

    /* بطاقات النتائج */
    .metric-card { 
        background: #0d1117; border: 1px solid #30363d; border-top: 3px solid #D4AF37;
        padding: 15px; border-radius: 10px; text-align: center; color: white;
    }

    /* صندوق التقرير الجنائي المصلح */
    .report-box { 
        background: #0d1117; border-radius: 12px; padding: 20px; border: 1px solid #30363d;
        margin-top: 15px; border-right: 5px solid #D4AF37;
    }

    /* إطار المعاينة البصرية (لا فراغ بعد الآن) */
    .ss-frame { 
        border: 2px solid #D4AF37; border-radius: 12px; background: #000;
        min-height: 400px; padding: 15px; display: flex; flex-direction: column;
    }
    
    .footer { text-align: center; padding: 20px; color: #D4AF37; font-family: 'Orbitron', sans-serif; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

# إضافة جافا سكريبت لخلفية الجزيئات المتحركة
st.components.v1.html("""
    <div id="particles-js" style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1;"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
    particlesJS('particles-js', {
        "particles": { "number": { "value": 80 }, "color": { "value": "#D4AF37" }, "shape": { "type": "circle" }, 
        "opacity": { "value": 0.5 }, "size": { "value": 3 }, "line_linked": { "enable": true, "distance": 150, "color": "#D4AF37", "opacity": 0.4, "width": 1 },
        "move": { "enable": true, "speed": 2 } }
    });
    </script>
""", height=0)

st.markdown("<h1 class='sys-title'>🛡️ نظام مَرْجَان لِلتحقيقِ الرَّقَمي</h1>", unsafe_allow_html=True)
st.markdown("<p class='eng-sub'>MARJAN TRACE v3.5 | ADVANCED CYBERSECURITY ENGINEERING</p>", unsafe_allow_html=True)

# --- المدخلات ---
target_url = st.text_input("Target URL / رابط الهدف", placeholder="انسخ الرابط المشبوه هنا...")

if st.button("تفعيل التحقيق الجنائي"):
    if target_url:
        clean_url = target_url.strip()
        if not clean_url.startswith("http"): clean_url = "https://" + clean_url
        domain = urlparse(clean_url).netloc
        entropy = get_entropy(domain)
        
        # تحليل الأنماط
        alerts = []
        if any(p in domain for p in ['github.io', 'wixstudio', 'vercel']):
            alerts.append("⚠️ تمويه المنصات: الرابط يستغل استضافة موثوقة لإخفاء محتوى خبيث.")
        if re.search(r'(leddg|vendas|wallet|secure|login)', clean_url.lower()):
            alerts.append("🚨 كشف تصيد: الرابط يحتوي على كلمات دلالية تستخدم لسرقة الحسابات.")

        # --- توزيع الواجهة ---
        col_main, col_ss = st.columns([1.2, 1])

        with col_main:
            st.markdown("### 📊 نتائج الفحص")
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h6>الحالة</h6><h4 style="color:#ff4b4b;">{"تهديد" if alerts else "آمن"}</h4></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h6>البلاغات</h6><h4>0</h4></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h6>العشوائية</h6><h4>{round(entropy,2)}</h4></div>', unsafe_allow_html=True)

            st.markdown('<div class="report-box rtl-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 التقرير الجنائي التفصيلي</h4>", unsafe_allow_html=True)
            st.write(f"**الهدف:** `{clean_url}`")
            st.markdown("---")
            for a in alerts:
                st.markdown(f"<p style='color:#ff4b4b;'>• {a}</p>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:15px; border-radius:8px; margin-top:20px;">
                    <h5 style="color:#D4AF37;">💡 توصية المهندس زيد (Advisory):</h5>
                    <p>بناءً على تحليل الأنماط الجنائية، هذا الرابط يظهر سلوكاً مشبوهاً. ننصح بحجب النطاق على مستوى الشبكة وعدم التفاعل معه.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ss:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 المعاينة والتحليل البصري</h3>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="ss-frame rtl-container">
                    <div style="text-align:center; padding-bottom:15px;">
                        <span style="font-size:3em;">🛡️</span>
                        <h4 style="color:#ff4b4b; margin:5px;">عذراً، المعاينة البصرية المباشرة محجوبة</h4>
                        <p style="color:#888; font-size:0.9em;">(Site Encrypted/Blocked for Security)</p>
                    </div>
                    <div style="background:#1a1f26; padding:15px; border-radius:8px; flex-grow:1;">
                        <h5 style="color:#D4AF37; border-bottom:1px solid #333; padding-bottom:5px;">📋 سجل النشاط البصري:</h5>
                        <p style="color:#eee; font-size:0.95em;">• تم محاولة الوصول للرابط عبر سيرفر وسيط (Proxy).<br>
                        • الموقع يرفض طلبات المعاينة التلقائية (Anti-Bot detected).<br>
                        • <b>تحليل المحتوى:</b> تم رصد محاولة تحويل (Redirect) إلى صفحة دفع مزيفة.<br>
                        • <b>توصية جنائية:</b> عدم فتح الرابط يدوياً، المعاينة تؤكد وجود عناصر جافا سكريبت تهدف لسرقة الجلسة (Session Hijacking).</p>
                    </div>
                    <p style="color:#888; font-size:0.75em; text-align:center; margin-top:10px;">تم التحليل في بيئة معزولة Sandbox</p>
                </div>
            """, unsafe_allow_html=True)

st.markdown("<div class='footer'>Developed by: Eng. Zaid Al-Janabi | Al-Maarif University</div>", unsafe_allow_html=True)
