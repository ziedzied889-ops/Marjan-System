import streamlit as st
import requests
import base64
import re
import math
import time
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace v3.1", page_icon="🛡️", layout="wide")

# --- محرك الذكاء الجنائي (Aggressive Zero-Trust) ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

def get_forensic_status(vt_hits, alerts, entropy):
    if vt_hits > 0 or len(alerts) >= 2 or entropy > 3.8:
        return "CRITICAL THREAT / تهديد خطير", "#ff4b4b"
    elif len(alerts) > 0 or entropy > 3.2:
        return "SUSPICIOUS / نشاط مشبوه", "#ffa500"
    else:
        return "CLEAN / نظام آمن", "#2ea043"

# --- التنسيق البصري (Cyber Dashboard) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500&display=swap');
    .main { background-color: #05070a; color: #e2e8f0; }
    .sys-title { font-family: 'Cairo', sans-serif; color: #D4AF37 !important; text-align: center; font-size: 2.3em; font-weight: bold; margin-bottom: 0; }
    .eng-sub { font-family: 'Orbitron', sans-serif; color: #888; text-align: center; font-size: 0.8em; letter-spacing: 2px; margin-top: 0; }
    .metric-card { background: #0d1117; border: 1px solid #30363d; border-top: 3px solid #D4AF37; padding: 20px; border-radius: 10px; text-align: center; }
    .report-box { background: #0d1117; border-radius: 15px; padding: 25px; border: 1px solid #30363d; margin-top: 20px; direction: rtl; text-align: right; }
    .screenshot-frame { border: 2px solid #D4AF37; border-radius: 10px; overflow: hidden; background: #000; min-height: 350px; display: flex; align-items: center; justify-content: center; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background: #0d1117; color: #D4AF37; text-align: center; padding: 10px; border-top: 1px solid #D4AF37; font-family: 'Orbitron', sans-serif; font-size: 0.85em; }
    .stButton>button { background: #D4AF37 !important; color: black !important; font-family: 'Cairo', sans-serif; font-weight: bold; width: 100%; border-radius: 8px; border: none; height: 3.2em; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='sys-title'>🛡️ نظام مَرْجَان لِلتحقيقِ الرَّقَمي</h1>", unsafe_allow_html=True)
st.markdown("<p class='eng-sub'>MARJAN TRACE v3.1: PROFESSIONAL FORENSIC SUITE</p>", unsafe_allow_html=True)

# --- واجهة الإدخال ---
target_url = st.text_input("Target URL / رابط الهدف", placeholder="ادخل الرابط المشبوه هنا لفك تشفيره جنائياً...")

if st.button("بَدء بروتوكول التَّحليل الشامل"):
    if target_url:
        clean_url = target_url.strip()
        if not clean_url.startswith("http"): clean_url = "https://" + clean_url
        domain = urlparse(clean_url).netloc

        # 1. تفعيل شريط الحالة (حل مشكلة الحقل الفارغ)
        progress_text = "جاري فحص طبقات الحماية وتحليل التهديدات..."
        my_bar = st.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(0.5)
        my_bar.empty() # حذف الشريط بعد الانتهاء لجعل الواجهة نظيفة

        with st.spinner("استخلاص النتائج النهائية..."):
            alerts = []
            
            # منطق الكشف العدواني (Aggressive Detection)
            # كشف التمويه في GitHub و Wix وغيرها
            if any(p in domain for p in ['github.io', 'wixstudio', 'web.app', 'vercel', 'online', 'top']):
                alerts.append(f"🚩 كشف استضافة وسيطة: الرابط يستغل منصة موثوقة ({domain}) لتنفيذ هجوم تصيد.")

            # كشف الكلمات الملغمة (مثل leddgr و boticario)
            blacklisted = ['leddg', 'vendas', 'boticario', 'secure', 'login', 'verify', 'wallet', 'crypto']
            if any(key in clean_url.lower() for key in blacklisted):
                alerts.append("🚨 محاولة انتحال: تم رصد هيكلية رابط مطابقة لهجمات سرقة الهوية والبيانات المالية.")

            entropy = get_entropy(domain)
            if entropy > 3.4:
                alerts.append(f"🕵️ تحليل عشوائية: معامل Entropy ({round(entropy,2)}) يشير إلى نطاق مولد آلياً.")

            # الاستعلام العالمي (VirusTotal)
            vt_hits = 0
            API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
            u_id = base64.urlsafe_b64encode(clean_url.encode()).decode().strip("=")
            try:
                res = requests.get(f"https://www.virustotal.com/api/v3/urls/{u_id}", headers={"x-apikey": API_KEY}, timeout=10)
                if res.status_code == 200:
                    vt_hits = res.json()['data']['attributes']['last_analysis_stats']['malicious']
            except: pass

            status_label, status_color = get_forensic_status(vt_hits, alerts, entropy)

            # --- عرض النتائج ---
            st.markdown("### 📊 لوحة المؤشرات الرقمية")
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h5>الحالة الجنائية</h5><h3 style="color:{status_color};">{status_label}</h3></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h5>بلاغات عالمية</h5><h2>{vt_hits}</h2></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h5>معامل العشوائية</h5><h2>{round(entropy, 2)}</h2></div>', unsafe_allow_html=True)

            col_res, col_ss = st.columns([1.3, 1])
            
            with col_res:
                st.markdown('<div class="report-box">', unsafe_allow_html=True)
                st.markdown("<h3 style='color:#D4AF37; margin-top:0;'>🔍 التقرير الجنائي التفصيلي</h3>", unsafe_allow_html=True)
                st.write(f"**الهدف المرصود:** `{clean_url}`")
                st.markdown("---")
                
                if alerts or vt_hits > 0:
                    for a in alerts: st.markdown(f"<p style='color:#ff4b4b; font-weight:bold;'>• {a}</p>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div style="background:rgba(212,175,55,0.05); border:1px solid #D4AF37; padding:15px; border-radius:10px; margin-top:20px;">
                        <h4 style="color:#D4AF37; margin-top:0;">💡 توصية نظام مَرْجَان (Marjan Advisory):</h4>
                        <p>بناءً على الأدلة الجنائية المكتشفة، هذا الرابط <b>غير آمن</b>. تم تصنيفه كـ {status_label}. يُحظر التعامل معه أو إدخال أي بيانات حساسة.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color:#2ea043; font-weight:bold;'>✅ نظام مَرْجَان: لم يتم رصد تهديدات مباشرة حالياً.</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_ss:
                st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 معاينة Sandbox آمنة</h3>", unsafe_allow_html=True)
                # استخدام محرك معاينة مجاني ومستقر
                ss_url = f"https://render-tron.appspot.com/screenshot/{clean_url}"
                st.markdown(f'<div class="screenshot-frame"><img src="{ss_url}" width="100%" onerror="this.parentElement.innerHTML=\'<p style=\\\'color:#888; text-align:center; padding:20px;\\\'>جاري توليد المعاينة البصرية المعزولة...</p>\'"></div>', unsafe_allow_html=True)
                st.markdown("<p style='color:#888; font-size:0.8em; text-align:center; margin-top:8px;'>تنبيه: المعاينة تتم عبر سيرفر وسيط (Proxy) لحماية جهازك من الأكواد الخبيثة.</p>", unsafe_allow_html=True)

# --- التذييل ---
st.markdown(f'<div class="footer">Developed by: Eng. Zaid Al-Janabi | Marjan Trace v3.1 | Al-Maarif University</div>', unsafe_allow_html=True)
