import streamlit as st
import requests
import base64
import re
import math
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace v2.2", page_icon="🛡️", layout="wide")

# --- محرك التحليل المتقدم ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

def marjan_logic_engine(url, vt_malicious, local_alerts):
    risk = 0
    if vt_malicious > 0: risk += 50 + (vt_malicious * 5)
    risk += len(local_alerts) * 20
    if url.startswith("http://"): risk += 15
    return min(risk, 100)

# --- التنسيق البصري (عودة الهوية الإنجليزية مع نتائج عربية) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500&display=swap');
    
    .main { background-color: #05070a; color: #e2e8f0; }
    h1 { font-family: 'Orbitron', sans-serif; color: #D4AF37 !important; text-align: center; }
    .eng-sub { font-family: 'Orbitron', sans-serif; color: #888; text-align: center; font-size: 0.9em; }
    
    .metric-card {
        background: #0d1117;
        border: 1px solid #30363d;
        border-top: 3px solid #D4AF37;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    
    .report-box {
        background: #0d1117;
        border-radius: 15px;
        padding: 25px;
        border: 1px solid #30363d;
        margin-top: 20px;
        direction: rtl; /* النتائج بالعربي */
    }
    
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background: #0d1117; color: #D4AF37;
        text-align: center; padding: 10px;
        border-top: 1px solid #D4AF37; font-family: 'Orbitron', sans-serif;
    }
    
    .stButton>button {
        background: #D4AF37 !important; color: black !important;
        font-family: 'Orbitron', sans-serif; font-weight: bold; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- الهيدر (إنجليزي) ---
st.markdown("<h1>🛡️ MARJAN TRACE</h1>", unsafe_allow_html=True)
st.markdown("<p class='eng-sub'>Advanced Digital Forensic Intelligence</p>", unsafe_allow_html=True)

# --- منطقة الإدخال ---
target_url = st.text_input("Target URL / رابط الهدف", placeholder="example.com")
if st.button("EXECUTE ANALYSIS"):
    if target_url:
        if not target_url.startswith("http"): target_url = "https://" + target_url
        domain = urlparse(target_url).netloc
        
        with st.spinner("Processing Intelligence Data..."):
            # 1. التحليل المحلي (قوي جداً)
            alerts = []
            entropy = get_entropy(domain)
            
            # كشف الكلمات المفتاحية للاحتيال (حتى لو لم يكتشفه PhishTank)
            phish_keywords = ['login', 'verify', 'bank', 'secure', 'update', 'account', 'office365', 'wp', 'vendas']
            if any(key in target_url.lower() for key in phish_keywords):
                alerts.append(f"🚨 انتحال هوية: الرابط يحتوي على كلمات دلالية ({', '.join([k for k in phish_keywords if k in target_url.lower()])}) تستخدم عادة في التصيد.")
            
            if entropy > 3.7:
                alerts.append("🕵️ تحليل DGA: اسم النطاق عشوائي جداً، وهذا أسلوب متبع في البرمجيات الخبيثة.")
            
            if ".online" in domain or ".top" in domain or ".vendas" in domain:
                alerts.append(f"🚩 نطاق عالي المخاطر: الامتداد .{domain.split('.')[-1]} يسجل نشاطات احتيالية مكثفة.")

            # 2. فحص VirusTotal (API)
            vt_hits = 0
            API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
            u_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
            try:
                res = requests.get(f"https://www.virustotal.com/api/v3/urls/{u_id}", headers={"x-apikey": API_KEY}, timeout=10)
                if res.status_code == 200:
                    vt_hits = res.json()['data']['attributes']['last_analysis_stats']['malicious']
            except: pass

            # 3. حساب النتيجة
            final_risk = marjan_logic_engine(target_url, vt_hits, alerts)

            # --- عرض النتائج (عربي) ---
            st.markdown("### 📊 لوحة مؤشرات الفحص")
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h5>مستوى الخطر</h5><h2 style="color:{"#ff4b4b" if final_risk > 40 else "#2ea043"}">{final_risk}%</h2></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h5>بلاغات عالمية</h5><h2>{vt_hits}</h2></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h5>معامل العشوائية</h5><h2>{round(entropy, 2)}</h2></div>', unsafe_allow_html=True)

            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.markdown("<h3 style='color:#D4AF37;'>🔍 تقرير التحليل الجنائي</h3>", unsafe_allow_html=True)
            st.write(f"**الرابط المطلوب:** `{target_url}`")
            st.markdown("---")
            
            if alerts or vt_hits > 0:
                for a in alerts: st.markdown(f"<p style='color:#ff4b4b; font-weight:bold;'>• {a}</p>", unsafe_allow_html=True)
                if vt_hits > 0: st.markdown(f"<p style='color:#ff4b4b; font-weight:bold;'>🚨 تم تأكيد الخطورة من قبل {vt_hits} محرك أمني عالمي.</p>", unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background:rgba(212,175,55,0.05); border:1px solid #D4AF37; padding:15px; border-radius:10px; margin-top:20px;">
                    <h4 style="color:#D4AF37; margin-top:0;">💡 توصية المهندس زيد (Zaid's Advisory):</h4>
                    <p>بناءً على المعطيات الجنائية، هذا الرابط <b>غير آمن</b>. يُنصح بحظر النطاق فوراً على مستوى الشبكة.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043; font-weight:bold;'>✅ محرك مَرجان: الرابط يبدو آمناً للاستخدام حالياً.</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- التذييل (إنجليزي) ---
st.markdown(f"""
    <div class="footer">
        Developed by: Eng. Zaid Al-Janabi | Marjan Trace v2.2 | Al-Maarif University
    </div>
""", unsafe_allow_html=True)
