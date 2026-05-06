import streamlit as st
import requests
import base64
import re
import math
from urllib.parse import urlparse
from datetime import datetime

# --- إعدادات الصفحة الاحترافية ---
st.set_page_config(page_title="Marjan Trace v2.0", page_icon="🛡️", layout="wide")

# --- محرك حساب درجة الخطورة (The Engineering Heart) ---
def calculate_marjan_score(url, vt_malicious, phishtank_status, local_alerts):
    score = 0
    # 1. نقاط بناءً على التحليل المحلي (40%)
    score += len(local_alerts) * 10
    
    # 2. نقاط بناءً على التقارير العالمية (40%)
    score += (vt_malicious * 5)
    if phishtank_status:
        score += 30
        
    # 3. نقاط بناءً على التشفير (20%)
    if url.startswith("http://"):
        score += 20
        
    return min(score, 100) # الحد الأقصى 100%

# حساب العشوائية (Entropy) لكشف الروابط المشبوهة برمجياً
def calculate_entropy(domain):
    prob = [float(domain.count(c)) / len(domain) for c in dict.fromkeys(list(domain))]
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy

# --- التنسيق البصري المتطور (Cyber-Security Theme) ---
st.markdown("""
    <style>
    .main { background-color: #0a0e14; }
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top right, #1a202c, #0a0e14);
        color: #e2e8f0;
    }
    .stMetric { background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; border: 1px solid rgba(212, 175, 55, 0.2); }
    h1 { color: #D4AF37 !important; font-family: 'Orbitron', sans-serif; letter-spacing: 2px; }
    .report-card { 
        background: rgba(15, 23, 42, 0.8); 
        padding: 25px; 
        border-radius: 20px; 
        border-left: 5px solid #D4AF37;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }
    .footer { 
        position: fixed; left: 0; bottom: 0; width: 100%; 
        background: rgba(10, 14, 20, 0.95); 
        color: #D4AF37; text-align: center; padding: 15px;
        border-top: 1px solid #D4AF37; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- واجهة المستخدم (Layout) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align:center;'>🛡️ MARJAN TRACE v2.0</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>Advanced Cyber Intelligence & Forensic Analysis</p>", unsafe_allow_html=True)

# مدخل الرابط
target_url = st.text_input("إدخال الهدف (Target URL):", placeholder="https://example.com")

if st.button("RUN FORENSIC ANALYSIS"):
    if target_url:
        # تصحيح البروتوكول
        if not target_url.startswith(("http://", "https://")):
            target_url = "https://" + target_url

        with st.spinner("Executing Forensic Protocols..."):
            # --- 1. التحليل المحلي الهيكلي ---
            local_reasons = []
            parsed = urlparse(target_url)
            domain = parsed.netloc.lower()
            
            # فحص الـ Entropy
            if calculate_entropy(domain) > 3.8:
                local_reasons.append("⚠️ عشوائية عالية: اسم النطاق يبدو وكأنه مولد آلياً (DGA Detection).")
            
            # فحص الـ TLDs
            if any(domain.endswith(tld) for tld in ['.xyz', '.top', '.zip', '.monster', '.bid']):
                local_reasons.append("🚩 نطاق عالي الخطورة: استخدام TLD مرتبط تاريخياً بهجمات سيبرانية.")

            # --- 2. جلب الاستخبارات الخارجية ---
            vt_malicious = 0
            phishtank_hit = False
            
            # VirusTotal
            API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
            url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
            try:
                vt_res = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers={"x-apikey": API_KEY}, timeout=10)
                if vt_res.status_code == 200:
                    vt_malicious = vt_res.json()['data']['attributes']['last_analysis_stats']['malicious']
            except: pass

            # --- 3. حساب النتيجة النهائية ---
            final_score = calculate_marjan_score(target_url, vt_malicious, phishtank_hit, local_reasons)

            # --- عرض النتائج (Dashboard Style) ---
            st.markdown("---")
            m1, m2, m3 = st.columns(3)
            m1.metric("Marjan Risk Level", f"{final_score}%", delta="- High Risk" if final_score > 50 else "Safe", delta_color="inverse")
            m2.metric("VT Detections", vt_malicious)
            m3.metric("Entropy Score", round(calculate_entropy(domain), 2))

            st.markdown(f"""
            <div class="report-card">
                <h3 style="color:#D4AF37;">📋 Forensic Report Summary</h3>
                <p><b>Target:</b> {target_url}</p>
                <hr style="border-color:rgba(212,175,55,0.1);">
                {"".join([f"<p style='color:#ff4b4b;'>• {r}</p>" for r in local_reasons])}
                {f"<p style='color:#ff4b4b;'>• تم رصد تهديد في {vt_malicious} محركات بحث عالمية.</p>" if vt_malicious > 0 else ""}
                <br>
                <h4 style="color:#D4AF37;">💡 Eng. Zaid's Recommendation:</h4>
                <p style="background:rgba(212,175,55,0.1); padding:10px; border-radius:10px;">
                    {'الرابط شديد الخطورة، يمنع فتحه نهائياً.' if final_score > 50 else 'الرابط يبدو سليماً، لكن توخى الحذر دائماً.'}
                </p>
            </div>
            """, unsafe_allow_html=True)

# --- تذييل الصفحة (حقوق المطور) ---
st.markdown(f"""
    <div class="footer">
        Developed by: Eng. Zaid Al-Janabi | Department of Cybersecurity Engineering | Al-Maarif University
    </div>
""", unsafe_allow_html=True)
