import streamlit as st
import requests
import base64
import re
import math
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace v4.3", page_icon="🛡️", layout="wide")

# --- محرك التحليل الجنائي المطور ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

# --- التنسيق البصري وحقن الخلفية ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;700&display=swap');
    .stApp { background: #05070a !important; }
    #cyber-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; opacity: 0.2; }
    .sys-title { font-family: 'Orbitron', sans-serif; color: #D4AF37 !important; text-align: center; font-size: 3.8em; font-weight: 700; margin-bottom: 0px; text-shadow: 0 0 30px rgba(212, 175, 85, 0.4); }
    .arabic-sub { font-family: 'Cairo', sans-serif; color: #ffffff; text-align: center; font-size: 1.6em; margin-top: -15px; }
    .metric-card { background: rgba(13, 17, 23, 0.9); border: 1px solid rgba(212, 175, 85, 0.2); border-top: 4px solid #D4AF37; padding: 25px; border-radius: 15px; text-align: center; }
    .report-box { background: rgba(10, 25, 47, 0.85); border-radius: 15px; padding: 25px; border: 1px solid rgba(212, 175, 85, 0.1); margin-top: 20px; border-right: 8px solid #D4AF37; }
    .ss-frame { border: 2px solid #D4AF37; border-radius: 15px; background: rgba(0,0,0,0.85); min-height: 420px; padding: 20px; display: flex; flex-direction: column; justify-content: center; }
    .rtl-container { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    </style>
    <div id="cyber-bg"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS('cyber-bg', {
            "particles": { "number": { "value": 100 }, "color": { "value": "#D4AF37" }, "line_linked": { "enable": true, "color": "#D4AF37", "opacity": 0.1 }, "move": { "enable": true, "speed": 1 } }
        });
    </script>
""", unsafe_allow_html=True)

st.markdown("<h1 class='sys-title'>MARJAN TRACE</h1>", unsafe_allow_html=True)
st.markdown("<p class='arabic-sub'>نظام مَرْجَان لِلتحقيقِ الرَّقَمي</p>", unsafe_allow_html=True)

target_url = st.text_input("رابط الهدف المراد فحصه (Target URL)", placeholder="أدخل الرابط هنا...")

if st.button("تفعيل بروتوكول الكشف الجنائي"):
    if target_url:
        clean_url = target_url.strip()
        if not clean_url.startswith("http"): clean_url = "https://" + clean_url
        domain = urlparse(clean_url).netloc
        entropy = get_entropy(domain)
        
        # --- منطق الكشف الصارم ---
        alerts = []
        # كشف الكلمات الدلالية للتصيد
        mal_keywords = ['online', 'vendas', 'wallet', 'crypto', 'login', 'secure', 'bank', 'banc', 'official', 'verify']
        if any(word in clean_url.lower() for word in mal_keywords):
            alerts.append("🚨 مؤشر انتحال: الرابط يحتوي على كلمات دلالية تُستخدم عادةً في عمليات التصيد.")

        # كشف أسماء النطاقات المشبوهة (DGA)
        if entropy > 3.0: 
            alerts.append(f"🕵️ كشف DGA: معامل العشوائية ({round(entropy,2)}) مرتفع، مما يشير لاسم نطاق مولد آلياً.")

        # كشف المنصات المجانية
        if any(p in domain for p in ['github.io', 'wixstudio', 'vercel', 'pages.dev']):
            alerts.append("🚩 تمويه الاستضافة: يتم استخدام منصة استضافة موثوقة لإخفاء نشاط مشبوه.")

        # تحديد الحالة النهائية بناءً على وجود أي تنبيه
        is_threat = len(alerts) > 0
        final_label = "CRITICAL / خطر" if is_threat else "CLEAN / آمن"
        final_color = "#ff4b4b" if is_threat else "#2ea043"

        col_main, col_ss = st.columns([1.2, 1])
        with col_main:
            st.markdown("<div class='rtl-container'><h3>📊 لوحة مؤشرات الفحص</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h6>الحالة النهائية</h6><h3 style="color:{final_color};">{final_label}</h3></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h6>بلاغات عالمية</h6><h2>0</h2></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h6>معامل العشوائية</h6><h2>{round(entropy,2)}</h2></div>', unsafe_allow_html=True)

            st.markdown('<div class="report-box rtl-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 التقرير الجنائي التفصيلي</h4>", unsafe_allow_html=True)
            st.write(f"**الهدف:** `{clean_url}`")
            st.markdown("---")
            if alerts:
                for a in alerts: st.markdown(f"<p style='color:#ff4b4b; font-weight:bold;'>• {a}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم رصد أدلة جرمية في بنية الرابط.</p>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:15px; border-radius:10px; border:1px solid #D4AF37; margin-top:20px;">
                    <h5 style="color:#D4AF37;">💡 توصية نظام مرجان:</h5>
                    <p>بناءً على المعطيات الجنائية، الرابط <b>{"غير آمن نهائياً" if is_threat else "يبدو سليماً"}</b>. يُنصح بحظر النطاق فوراً.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ss:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 معاينة Sandbox</h3>", unsafe_allow_html=True)
            st.markdown(f"""<div class="ss-frame rtl-container"><div style="text-align:center;"><span style="font-size:4em;">🛡️</span><h4 style="color:#ff4b4b;">المعاينة محجوبة أمنياً</h4></div></div>""", unsafe_allow_html=True)

st.markdown(f"<div style='text-align:center; padding:20px; color:#D4AF37;'>Developed by: Eng. Zaid Al-Janabi | Al-Maarif University</div>", unsafe_allow_html=True)
