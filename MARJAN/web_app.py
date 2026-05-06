import streamlit as st
import re
import math
from urllib.parse import urlparse

# --- إعدادات النظام ---
st.set_page_config(page_title="Marjan Trace v6.5", page_icon="🛡️", layout="wide")

# --- محرك التحليل الذكي ---
def analyze_threat(url):
    findings = []
    summary_for_user = "الرابط لا يظهر نشاطاً عدائياً مباشراً حتى الآن."
    danger_level = "LOW"
    
    if not url: return findings, summary_for_user, danger_level

    # منطق التحليل المطور
    if any(x in url.lower() for x in ['bank', 'secure', 'login', 'pay', 'crypto', 'wallet']):
        findings.append("محاولة هندسة اجتماعية (Phishing Attempt)")
        summary_for_user = "هذا الرابط مصمم لاصطياد الضحايا عبر محاكاة صفحات تسجيل دخول بنكية أو مالية لسرقة الأموال."
        danger_level = "HIGH"
    elif url.count('.') > 3 or len(url) > 80:
        findings.append("تمويه النطاق (URL Masking)")
        summary_for_user = "يستخدم هذا الرابط تقنيات التمويه لإخفاء وجهته الحقيقية، مما يرجح وجود برمجيات خبيثة."
        danger_level = "MEDIUM"
    
    return findings, summary_for_user, danger_level

# --- حقن الخلفية السيبرانية الشاملة (Full Page Background) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;900&display=swap');
    
    /* 1. تلوين الخلفية الكلية للمتصفح (المناطق التي كانت سوداء) */
    .stApp {
        background: radial-gradient(circle at center, #0d1117 0%, #05070a 100%) !important;
    }

    /* حاوية الخلفية المتحركة */
    #marjan-cyber-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        opacity: 0.4;
        pointer-events: none;
    }

    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #D4AF37;
        text-align: center;
        font-size: 4rem;
        letter-spacing: 8px;
        margin-top: 20px;
        text-shadow: 0 0 25px rgba(212,175,55,0.6);
    }

    /* تنسيق البطاقات لتكون شفافة (Glassmorphism) وتظهر الخلفية من ورائها */
    .report-box {
        background: rgba(13, 17, 23, 0.85) !important;
        border: 1px solid rgba(212, 175, 85, 0.3) !important;
        border-radius: 20px;
        padding: 30px;
        backdrop-filter: blur(10px);
    }

    .sandbox-preview {
        border: 2px solid #D4AF37;
        border-radius: 20px;
        height: 450px;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(15px);
        box-shadow: inset 0 0 50px rgba(212, 175, 85, 0.1);
    }

    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #b8860b 100%) !important;
        color: black !important;
        font-weight: bold;
        border-radius: 12px;
        height: 3.5em;
        border: none;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(212, 175, 85, 0.4);
    }
    </style>

    <div id="marjan-cyber-canvas"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS('marjan-cyber-canvas', {
            "particles": {
                "number": { "value": 150 },
                "color": { "value": "#D4AF37" },
                "shape": { "type": "circle" },
                "opacity": { "value": 0.5 },
                "size": { "value": 2 },
                "line_linked": { "enable": true, "distance": 150, "color": "#D4AF37", "opacity": 0.2, "width": 1 },
                "move": { "enable": true, "speed": 2 }
            },
            "interactivity": { "events": { "onhover": { "enable": true, "mode": "grab" } } }
        });
    </script>
    """, unsafe_allow_html=True)

# --- واجهة Marjan Trace ---
st.markdown("<h1 class='main-title'>MARJAN TRACE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#ffffff; font-family:Cairo; font-size:1.2em;'>النظام الذكي للتحليل الجنائي الرقمي</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
url_to_scan = st.text_input("أدخل الرابط المراد فحصه / Target URL", placeholder="https://example.com...")

if st.button("بدء الفحص الجنائي"):
    if url_to_scan:
        findings, user_info, risk = analyze_threat(url_to_scan)
        
        col_res, col_visual = st.columns([1.3, 1])
        
        with col_res:
            st.markdown(f"""
            <div class='report-box' style='direction: rtl;'>
                <h3 style='color:#D4AF37; font-family:Cairo;'>🔍 تقرير فحص النطاق</h3>
                <p><b>الرابط المكتشف:</b> <code style='color:#ff4b4b;'>{url_to_scan}</code></p>
                <hr style='opacity:0.2;'>
                <p style='font-size:1.1em;'><b>الأدلة الجرمية المكتشفة:</b></p>
                <ul style='color:#ccc;'>
                    {"<li>لم يتم رصد أنماط خبيثة معروفة.</li>" if not findings else "".join([f"<li>{f}</li>" for f in findings])}
                </ul>
                <div style='background:rgba(212,175,55,0.1); padding:20px; border-radius:15px; border-right:5px solid #D4AF37; margin-top:25px;'>
                    <h5 style='color:#D4AF37; font-family:Orbitron; margin:0;'>(Marjan Trace Advisory):</h5>
                    <p style='margin-top:10px;'>{"⚠️ تنبيه: الرابط يمثل خطورة عالية، يُنصح بحجبه فوراً." if risk != "LOW" else "✅ الرابط يبدو آمناً للاستخدام العادي."}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_visual:
            st.markdown("<h3 style='color:#D4AF37; text-align:center; font-family:Cairo;'>🛡️ محاكاة الضرر (Sandbox)</h3>", unsafe_allow_html=True)
            status_icon = "🚫" if risk == "HIGH" else "⚠️" if risk == "MEDIUM" else "🛡️"
            status_color = "#ff4b4b" if risk == "HIGH" else "#D4AF37" if risk == "MEDIUM" else "#2ea043"
            
            st.markdown(f"""
            <div class='sandbox-preview'>
                <div style='font-size: 5rem;'>{status_icon}</div>
                <h3 style='color:{status_color}; font-family:Cairo;'>تحليل المخاطر</h3>
                <div style='padding:0 20px;'>
                    <p style='color:#eee; font-family:Cairo; font-size:1.1rem;'>{user_info}</p>
                </div>
                <div style='margin-top:20px; background:rgba(255,255,255,0.05); padding:10px 20px; border-radius:30px;'>
                    <small style='color:#888;'>Isolated Environment Active</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#D4AF37; font-family:Orbitron; opacity:0.6;'>DEVELOPED BY: ENG. ZAID AL-JANABI | 2026</p>", unsafe_allow_html=True)
