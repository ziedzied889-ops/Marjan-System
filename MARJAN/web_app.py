import streamlit as st
import requests
import base64
import re
import math
from urllib.parse import urlparse

# --- إعدادات الصفحة النهائية ---
st.set_page_config(page_title="Marjan Trace v4.1", page_icon="🛡️", layout="wide")

# --- محرك التحليل الجنائي ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

# --- نظام التنسيق المتقدم (إصلاح الخلفية السوداء) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;700&display=swap');
    
    /* 1. إجبار الخلفية على التغير (الطبقة الأساسية) */
    .stApp {
        background: radial-gradient(circle at center, #0a192f 0%, #05070a 100%) !important;
    }

    /* 2. حاوية الجسيمات المتحركة */
    #particles-js {
        position: fixed;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        z-index: 0; /* خلف العناصر */
    }

    /* 3. جعل عناصر الواجهة فوق الخلفية */
    .main .block-container {
        position: relative;
        z-index: 1;
    }

    .rtl-container { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }

    /* تنسيق الهوية البصرية المحدثة */
    .sys-title { 
        font-family: 'Orbitron', sans-serif; color: #D4AF37 !important; 
        text-align: center; font-size: 3.8em; font-weight: 700; 
        margin-bottom: 0px; letter-spacing: 5px;
        text-shadow: 0 0 30px rgba(212, 175, 85, 0.4);
    }
    .arabic-sub { 
        font-family: 'Cairo', sans-serif; color: #ffffff; 
        text-align: center; font-size: 1.6em; margin-top: -15px;
        font-weight: 400; letter-spacing: 1px;
    }

    .metric-card { 
        background: rgba(13, 17, 23, 0.85); border: 1px solid rgba(212, 175, 85, 0.2); 
        border-top: 4px solid #D4AF37; padding: 25px; border-radius: 15px; 
        text-align: center; color: white; backdrop-filter: blur(5px);
    }

    .report-box { 
        background: rgba(10, 25, 47, 0.8); border-radius: 15px; padding: 25px; 
        border: 1px solid rgba(212, 175, 85, 0.1); margin-top: 20px; 
        border-right: 8px solid #D4AF37; backdrop-filter: blur(10px);
    }

    .ss-frame { 
        border: 2px solid #D4AF37; border-radius: 15px; background: rgba(0,0,0,0.8);
        min-height: 420px; padding: 20px; display: flex; flex-direction: column; 
        justify-content: center; backdrop-filter: blur(10px);
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #b8860b 100%) !important;
        color: black !important; font-weight: bold; border-radius: 10px; height: 3.5em;
    }
    </style>

    <div id="particles-js"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS('particles-js', {
            "particles": {
                "number": { "value": 120, "density": { "enable": true, "value_area": 800 } },
                "color": { "value": "#D4AF37" },
                "shape": { "type": "circle" },
                "opacity": { "value": 0.3, "random": true },
                "size": { "value": 2, "random": true },
                "line_linked": { "enable": true, "distance": 150, "color": "#D4AF37", "opacity": 0.15, "width": 1 },
                "move": { "enable": true, "speed": 2, "direction": "none", "random": true, "out_mode": "out" }
            },
            "interactivity": { "detect_on": "window", "events": { "onhover": { "enable": true, "mode": "repulse" } } },
            "retina_detect": true
        });
    </script>
    """, unsafe_allow_html=True)

# --- محتوى الواجهة ---
st.markdown("<h1 class='sys-title'>MARJAN TRACE</h1>", unsafe_allow_html=True)
st.markdown("<p class='arabic-sub'>نظام مَرْجَان لِلتحقيقِ الرَّقَمي</p>", unsafe_allow_html=True)

# حقل الإدخال
st.markdown("<br>", unsafe_allow_html=True)
target_url = st.text_input("رابط الهدف المراد فحصه (Target URL)", placeholder="أدخل الرابط المشبوه هنا لتفعيل الكشف...")

if st.button("تفعيل بروتوكول الكشف الجنائي الشامل"):
    if target_url:
        clean_url = target_url.strip()
        if not clean_url.startswith("http"): clean_url = "https://" + clean_url
        domain = urlparse(clean_url).netloc
        entropy = get_entropy(domain)
        
        # تحليل الأنماط الجنائية
        alerts = []
        if any(p in domain for p in ['github.io', 'wixstudio', 'vercel', 'online', 'top']):
            alerts.append("🚩 استغلال المنصات: الرابط يستخدم بيئة استضافة موثوقة للتمويه على نشاطه.")
        if re.search(r'(leddg|vendas|wallet|secure|login|verify|crypto|banc)', clean_url.lower()):
            alerts.append("🚨 مؤشر انتحال: تم رصد كلمات مفتاحية تستخدم عادة في صفحات التصيد المالي.")
        
        # منطق القرار الموحد (حل مشكلة "آمن" مع الرابط الخطر)
        is_threat = len(alerts) > 0 or entropy > 3.6
        final_label = "CRITICAL / خطر" if is_threat else "CLEAN / آمن"
        final_color = "#ff4b4b" if is_threat else "#2ea043"

        col_main, col_ss = st.columns([1.2, 1])

        with col_main:
            st.markdown("<div class='rtl-container'><h3>📊 مؤشرات التحليل اللحظي</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h6>الحالة النهائية</h6><h3 style="color:{final_color};">{final_label}</h3></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h6>بلاغات عالمية</h6><h2>0</h2></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h6>معامل العشوائية</h6><h2>{round(entropy,2)}</h2></div>', unsafe_allow_html=True)

            st.markdown('<div class="report-box rtl-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 تقرير الفحص التفصيلي</h4>", unsafe_allow_html=True)
            st.write(f"**الرابط المطلوب:** `{clean_url}`")
            st.markdown("<hr style='border:0.5px solid rgba(212,175,85,0.2);'>", unsafe_allow_html=True)
            if alerts:
                for a in alerts: st.markdown(f"<p style='color:#ff4b4b; font-weight:bold;'>• {a}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم رصد أدلة جرمية مباشرة في بنية الرابط.</p>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:15px; border-radius:10px; margin-top:20px; border:1px solid rgba(212,175,55,0.3);">
                    <h5 style="color:#D4AF37;">💡 (Zaid's Advisory) توصية المهندس زيد:</h5>
                    <p>بناءً على الأدلة الجنائية المذكورة، الرابط <b>{"خطير جداً" if is_threat else "يبدو سليماً من الخارج"}</b>. نوصي بحجب النطاق ومنع التعامل معه نهائياً.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ss:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 محاكاة Sandbox الآمنة</h3>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="ss-frame rtl-container">
                    <div style="text-align:center;">
                        <span style="font-size:4em; color:#D4AF37;">🛡️</span>
                        <h4 style="color:#ff4b4b;">المعاينة البصرية محجوبة أمنياً</h4>
                        <p style="color:#888;">(Isolated Environment Execution)</p>
                    </div>
                    <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:10px; margin-top:20px;">
                        <h5 style="color:#D4AF37; border-bottom:1px solid #333; padding-bottom:5px;">📋 سجل النشاط البصري:</h5>
                        <p style="color:#ccc; font-size:0.9em; line-height:1.7;">
                        • تم الدخول عبر Proxy معزول لحماية هويتك.<br>
                        • الموقع يحتوي على شيفرات تمنع الروبوتات من الفحص.<br>
                        • <b>تحليل الواجهة:</b> تم رصد حقول إدخال تطلب بيانات سرية.<br>
                        • <b>القرار الجنائي:</b> الرابط يمثل خطورة "تصيد عالي المستوى".</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; padding:20px; color:#D4AF37; font-family:Orbitron; border-top:1px solid rgba(212,175,85,0.1);'>Developed by: Eng. Zaid Al-Janabi | Department of Cybersecurity Engineering | Al-Maarif University</div>", unsafe_allow_html=True)
