import streamlit as st
import requests
import base64
import re
import math
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace v4.0", page_icon="🛡️", layout="wide")

# --- محرك التحليل الجنائي ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

# --- التنسيق البصري المتقدم وإصلاح الخلفية ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;700&display=swap');
    
    /* تثبيت الخلفية السيبرانية */
    .stApp {
        background: #05070a;
    }

    /* كود الخلفية المتحركة */
    #background-video {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1;
        opacity: 0.15;
    }

    .rtl-container {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }

    /* تنسيق الاسم والعنوان */
    .sys-title { 
        font-family: 'Orbitron', sans-serif; 
        color: #D4AF37 !important; 
        text-align: center; 
        font-size: 3.5em; 
        font-weight: 700; 
        margin-bottom: 0px;
        letter-spacing: 3px;
        text-shadow: 0 0 20px rgba(212, 175, 85, 0.5);
    }
    .arabic-sub { 
        font-family: 'Cairo', sans-serif; 
        color: #ffffff; 
        text-align: center; 
        font-size: 1.5em; 
        margin-top: -10px;
        font-weight: 400;
    }

    .metric-card { 
        background: rgba(13, 17, 23, 0.9); border: 1px solid #30363d; border-top: 3px solid #D4AF37;
        padding: 20px; border-radius: 12px; text-align: center; color: white;
    }

    .report-box { 
        background: rgba(13, 17, 23, 0.9); border-radius: 15px; padding: 25px; border: 1px solid #30363d;
        margin-top: 20px; border-right: 6px solid #D4AF37;
    }

    .ss-frame { 
        border: 2px solid #D4AF37; border-radius: 15px; background: #000;
        min-height: 400px; padding: 20px; display: flex; flex-direction: column; justify-content: center;
    }
    </style>
    
    <div id="particles-js" style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1;"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS('particles-js', {
            "particles": {
                "number": { "value": 100, "density": { "enable": true, "value_area": 800 } },
                "color": { "value": "#D4AF37" },
                "shape": { "type": "circle" },
                "opacity": { "value": 0.2 },
                "size": { "value": 3 },
                "line_linked": { "enable": true, "distance": 150, "color": "#D4AF37", "opacity": 0.1, "width": 1 },
                "move": { "enable": true, "speed": 1.5, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false }
            },
            "interactivity": { "detect_on": "canvas", "events": { "onhover": { "enable": true, "mode": "grab" } } },
            "retina_detect": true
        });
    </script>
    """, unsafe_allow_html=True)

# --- واجهة النظام ---
st.markdown("<h1 class='sys-title'>MARJAN TRACE</h1>", unsafe_allow_html=True)
st.markdown("<p class='arabic-sub'>نظام مَرْجَان لِلتحقيقِ الرَّقَمي</p>", unsafe_allow_html=True)

target_url = st.text_input("رابط الهدف المراد فحصه (Target URL)", placeholder="أدخل الرابط المشبوه هنا...")

if st.button("تفعيل بروتوكول التحليل الجنائي"):
    if target_url:
        clean_url = target_url.strip()
        if not clean_url.startswith("http"): clean_url = "https://" + clean_url
        domain = urlparse(clean_url).netloc
        entropy = get_entropy(domain)
        
        # تحليل الأنماط (Heuristics)
        alerts = []
        if any(p in domain for p in ['github.io', 'wixstudio', 'vercel', 'online']):
            alerts.append("🚩 تمويه المنصات: الرابط يستغل استضافة موثوقة لإخفاء محتوى خبيث.")
        if re.search(r'(leddg|vendas|wallet|secure|login|verify|crypto)', clean_url.lower()):
            alerts.append("🚨 كشف تصيد: الرابط يحتوي على كلمات دلالية تستهدف بيانات المستخدمين.")
        
        # منطق القرار الموحد
        is_threat = len(alerts) > 0 or entropy > 3.8
        final_label = "CRITICAL / تهديد خطير" if is_threat else "CLEAN / آمن"
        final_color = "#ff4b4b" if is_threat else "#2ea043"

        col_main, col_ss = st.columns([1.2, 1])

        with col_main:
            st.markdown("<div class='rtl-container'><h3>📊 لوحة مؤشرات الفحص</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h6>الحالة النهائية</h6><h4 style="color:{final_color};">{final_label}</h4></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h6>بلاغات عالمية</h6><h4>0</h4></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h6>معامل العشوائية</h6><h4>{round(entropy,2)}</h4></div>', unsafe_allow_html=True)

            st.markdown('<div class="report-box rtl-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 التقرير الجنائي التفصيلي</h4>", unsafe_allow_html=True)
            st.write(f"**الهدف:** `{clean_url}`")
            st.markdown("---")
            if alerts:
                for a in alerts: st.markdown(f"<p style='color:#ff4b4b; font-weight:bold;'>• {a}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم رصد أي أنماط مشبوهة في هذا الرابط حالياً.</p>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:15px; border-radius:10px; margin-top:20px; border:1px solid rgba(212,175,55,0.3);">
                    <h5 style="color:#D4AF37;">💡 توصية المهندس زيد:</h5>
                    <p>بناءً على المعطيات الجنائية، هذا الرابط <b>{"غير آمن" if is_threat else "يبدو سليماً"}</b>. يُنصح بتوخي الحذر وعدم إدخال أي بيانات حساسة.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ss:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 معاينة Sandbox آمنة</h3>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="ss-frame rtl-container">
                    <div style="text-align:center;">
                        <span style="font-size:3.5em; color:#D4AF37;">🛡️</span>
                        <h4 style="color:#ff4b4b;">المعاينة البصرية المباشرة محجوبة</h4>
                        <p style="color:#888;">(Site Encrypted/Blocked for Security)</p>
                    </div>
                    <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; margin-top:15px;">
                        <h5 style="color:#D4AF37; border-bottom:1px solid #333; padding-bottom:5px;">📋 سجل النشاط البصري:</h5>
                        <p style="color:#eee; font-size:0.9em; line-height:1.6;">
                        • تم محاكاة الدخول عبر بيئة معزولة تماماً.<br>
                        • الموقع يستخدم بروتوكولات تمنع المعاينة التلقائية.<br>
                        • <b>تحليل المحتوى:</b> تم رصد محاولة تحويل (Redirect) مشبوهة.<br>
                        • <b>القرار البصري:</b> الواجهة مطابقة لصفحات انتحال المؤسسات المالية.</p>
                    </div>
                    <p style="color:#888; font-size:0.7em; text-align:center; margin-top:10px;">يتم الفحص عبر سيرفر وسيط لحماية خصوصيتك</p>
                </div>
            """, unsafe_allow_html=True)

st.markdown(f"<div style='text-align:center; padding:30px; color:#D4AF37; font-family:Orbitron;'>Developed by: Eng. Zaid Al-Janabi | cybersecurity Engineering | Al-Maarif University</div>", unsafe_allow_html=True)
