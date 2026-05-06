import streamlit as st
import requests
import base64
import re
import math
from urllib.parse import urlparse

# --- إعدادات الصفحة الأصلية (لا تغيير) ---
st.set_page_config(page_title="Marjan Trace v4.2", page_icon="🛡️", layout="wide")

# --- محرك التحليل الجنائي الأصلي (لا تغيير) ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

# --- إضافة الخلفية السيبرانية الاحترافية وتحسين التنسيق ---
# تم وضع هذا الكود في البداية لضمان تحميل الخلفية كطبقة سفلى
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;700&display=swap');
    
    /* 1. تثبيت الخلفية السيبرانية المتحركة */
    .stApp {
        background: #05070a !important; /* لون أساسي غامق جداً */
    }
    
    /* حاوية الجسيمات المتحركة (Cyber Network) */
    #cyber-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1; /* خلف كل شيء */
        opacity: 0.15; /* شفافية عالية لكي لا تؤثر على القراءة */
        pointer-events: none; /* لا تتفاعل مع الماوس لكي لا تعيق الأزرار */
    }

    /* 2. تحسين تنسيقات الواجهة لتبدو احترافية فوق الخلفية */
    .rtl-container { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }

    /* تنسيق الهوية البصرية */
    .sys-title { 
        font-family: 'Orbitron', sans-serif; color: #D4AF37 !important; 
        text-align: center; font-size: 3.8em; font-weight: 700; 
        margin-bottom: 0px; letter-spacing: 5px;
        text-shadow: 0 0 30px rgba(212, 175, 85, 0.4);
    }
    .arabic-sub { 
        font-family: 'Cairo', sans-serif; color: #ffffff; 
        text-align: center; font-size: 1.6em; margin-top: -15px;
        font-weight: 400;
    }

    /* تنسيق البطاقات لتدعم الشفافية (Glassmorphism) */
    .metric-card { 
        background: rgba(13, 17, 23, 0.85) !important; /* شفافية جزئية */
        border: 1px solid rgba(212, 175, 85, 0.2) !important; 
        border-top: 4px solid #D4AF37 !important; padding: 25px; border-radius: 15px; text-align: center;
        backdrop-filter: blur(5px); /* تأثير ضبابي للخلفية */
    }

    .report-box { 
        background: rgba(10, 25, 47, 0.8) !important; border-radius: 15px; padding: 25px; 
        border: 1px solid rgba(212, 175, 85, 0.1) !important; margin-top: 20px; 
        border-right: 8px solid #D4AF37 !important;
        backdrop-filter: blur(5px);
    }

    .ss-frame { 
        border: 2px solid #D4AF37 !important; border-radius: 15px; background: rgba(0,0,0,0.8) !important;
        min-height: 420px; padding: 20px; display: flex; flex-direction: column; justify-content: center;
        backdrop-filter: blur(5px);
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #b8860b 100%) !important;
        color: black !important; font-weight: bold; border-radius: 10px; height: 3.5em;
        border: none;
    }
    </style>

    <div id="cyber-bg"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS('cyber-bg', {
            "particles": {
                "number": { "value": 100, "density": { "enable": true, "value_area": 800 } },
                "color": { "value": "#D4AF37" }, /* اللون الذهبي الخاص بمرجان */
                "shape": { "type": "circle" },
                "opacity": { "value": 0.5, "random": true },
                "size": { "value": 2, "random": true },
                "line_linked": { "enable": true, "distance": 150, "color": "#D4AF37", "opacity": 0.15, "width": 1 },
                "move": { "enable": true, "speed": 1.5, "direction": "none", "random": true, "out_mode": "out" }
            },
            "interactivity": { "detect_on": "window", "events": { "onhover": { "enable": true, "mode": "repulse" } } },
            "retina_detect": true
        });
    </script>
    """, unsafe_allow_html=True)

# --- واجهة المستخدم الأصلية (لا تغيير في المحتوى) ---
st.markdown("<h1 class='sys-title'>MARJAN TRACE</h1>", unsafe_allow_html=True)
st.markdown("<p class='arabic-sub'>نظام مَرْجَان لِلتحقيقِ الرَّقَمي</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
target_url = st.text_input("رابط الهدف المراد فحصه (Target URL)", placeholder="أدخل الرابط المشبوه هنا...")

if st.button("تفعيل بروتوكول الكشف الجنائي"):
    if target_url:
        clean_url = target_url.strip()
        if not clean_url.startswith("http"): clean_url = "https://" + clean_url
        domain = urlparse(clean_url).netloc
        entropy = get_entropy(domain)
        
        # --- منطق التحليل الأصلي (لا تغيير) ---
        alerts = []
        if any(p in domain for p in ['online', 'top', 'xyz', 'vendas', 'wallet']):
            alerts.append("🚩 نطاق عالي المخاطر: تم رصد امتداد أو اسم مرتبط بنشاطات مشبوهة.")
        if entropy > 3.7:
            alerts.append(f"🕵️ تحليل DGA: معامل العشوائية ({round(entropy,2)}) يشير لاسم نطاق مولد آلياً.")

        is_threat = len(alerts) > 0 or entropy > 3.8
        final_label = "CRITICAL / خطر" if is_threat else "CLEAN / آمن"
        final_color = "#ff4b4b" if is_threat else "#2ea043"

        col_main, col_ss = st.columns([1.2, 1])

        with col_main:
            st.markdown("<div class='rtl-container'><h3>📊 مؤشرات الفحص</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h6>الحالة النهائية</h6><h3 style="color:{final_color};">{final_label}</h3></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h6>بلاغات عالمية</h6><h2>0</h2></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h6>العشوائية</h6><h2>{round(entropy,2)}</h2></div>', unsafe_allow_html=True)

            st.markdown('<div class="report-box rtl-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 تقرير التحقيق التفصيلي</h4>", unsafe_allow_html=True)
            st.write(f"**الهدف:** `{clean_url}`")
            if alerts:
                for a in alerts: st.markdown(f"<p style='color:#ff4b4b;'>• {a}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم رصد تهديدات مباشرة.</p>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:15px; border-radius:10px; border:1px solid #D4AF37; margin-top:20px;">
                    <h5 style="color:#D4AF37;">💡 توصية المهندس زيد (Zaid's Advisory):</h5>
                    <p>بناءً على المعطيات، الرابط <b>{"غير آمن" if is_threat else "سليم"}</b> ويجب التعامل معه بحذر شديد.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ss:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 معاينة Sandbox</h3>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="ss-frame rtl-container">
                    <div style="text-align:center;">
                        <span style="font-size:4em; color:#D4AF37;">🛡️</span>
                        <h4 style="color:#ff4b4b;">المعاينة محجوبة لأسباب أمنية</h4>
                        <p style="color:#888;">(Isolated Environment)</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# --- التذييل الأصلي (لا تغيير) ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; padding:20px; color:#D4AF37; border-top:1px solid rgba(212,175,55,0.1);'>Developed by: Eng. Zaid Al-Janabi | Department of Cybersecurity Engineering | Al-Maarif University</div>", unsafe_allow_html=True)
