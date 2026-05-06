import streamlit as st
import requests
import base64
import re
import math
import socket
from urllib.parse import urlparse
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نظام مرجان للتحقيق الرقمي", page_icon="🛡️", layout="wide")

# --- خوارزمية مرجان للتقييم الذكي (Logic) ---
def marjan_logic_engine(url, vt_malicious, local_alerts):
    risk_score = 0
    # التحليل المحلي (قوة المهندس) - 50% من الوزن
    risk_score += len(local_alerts) * 15
    
    # النتائج العالمية - 50% من الوزن
    risk_score += (vt_malicious * 10)
    
    # فحص أمن الاتصال
    if url.startswith("http://"):
        risk_score += 20
        
    return min(risk_score, 100)

def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

# --- التصميم الجديد (Modern Dark Cyber) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .main { background-color: #05070a; }
    
    /* بطاقات النتائج */
    .metric-card {
        background: #0d1117;
        border: 1px solid #1f2937;
        border-right: 4px solid #D4AF37;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    
    /* حاوية التقرير */
    .report-box {
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #30363d;
        padding: 30px;
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0 8px 32px 0 rgba(0,0,0,0.8);
    }
    
    .danger-text { color: #ff4b4b; font-weight: bold; margin-bottom: 10px; }
    .safe-text { color: #2ea043; font-weight: bold; }
    
    /* التذييل */
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background: #0d1117; color: #D4AF37;
        text-align: center; padding: 10px;
        border-top: 2px solid #D4AF37; z-index: 1000;
    }
    
    /* تحسين شكل الأزرار */
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37, #b8860b) !important;
        color: black !important; font-weight: bold !important;
        border: none !important; border-radius: 8px !important;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px rgba(212,175,55,0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- الواجهة ---
st.markdown("<h1 style='text-align:center; color:#D4AF37;'>🛡️ نظام مَرْجَان لِلتحقيقِ الرَّقَمي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8b949e; margin-bottom:40px;'>الإصدار 2.1 - تحت إشراف هندسة تقنيات الأمن السيبراني</p>", unsafe_allow_html=True)

# حقل الإدخال
col_a, col_b, col_c = st.columns([1, 4, 1])
with col_b:
    target_url = st.text_input("", placeholder="ضع الرابط هنا لبدء التحليل الجنائي...")
    search_btn = st.button("تفعيل بروتوكول الفحص")

if search_btn and target_url:
    with st.spinner("جاري تحليل التهديدات واستخلاص البيانات..."):
        # 1. معالجة الرابط
        if not target_url.startswith("http"): target_url = "https://" + target_url
        parsed_url = urlparse(target_url)
        domain = parsed_url.netloc
        
        # 2. التحليل المحلي (Heuristics)
        alerts = []
        entropy = get_entropy(domain)
        
        if entropy > 3.8:
            alerts.append("🕵️ كشف DGA: اسم النطاق يحتوي على عشوائية عالية، مما يشير لروابط مولدة برمجياً.")
        if any(domain.endswith(t) for t in ['.xyz', '.zip', '.top', '.monster', '.support']):
            alerts.append("🚩 نطاق مشبوه: الامتداد المستخدم مرتبط بنشاطات احتيالية عالمية.")
        if target_url.startswith("http://"):
            alerts.append("🔓 بروتوكول غير آمن: الرابط يفتقر لتشفير SSL/TLS.")

        # 3. التحليل العالمي (VirusTotal)
        vt_hits = 0
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        u_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        try:
            res = requests.get(f"https://www.virustotal.com/api/v3/urls/{u_id}", headers={"x-apikey": API_KEY}, timeout=8)
            if res.status_code == 200:
                vt_hits = res.json()['data']['attributes']['last_analysis_stats']['malicious']
        except: pass

        # 4. حساب النتيجة النهائية
        final_risk = marjan_logic_engine(target_url, vt_hits, alerts)

        # --- عرض النتائج ---
        st.markdown("### 📊 لوحة مؤشرات الفحص")
        m_col1, m_col2, m_col3 = st.columns(3)
        
        with m_col1:
            st.markdown(f'<div class="metric-card"><h4>مستوى الخطر</h4><h2 style="color:{"#ff4b4b" if final_risk > 40 else "#2ea043"}">{final_risk}%</h2></div>', unsafe_allow_html=True)
        with m_col2:
            st.markdown(f'<div class="metric-card"><h4>بلاغات عالمية</h4><h2>{vt_hits}</h2></div>', unsafe_allow_html=True)
        with m_col3:
            st.markdown(f'<div class="metric-card"><h4>معامل العشوائية</h4><h2>{round(entropy, 2)}</h2></div>', unsafe_allow_html=True)

        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#D4AF37;'>🔍 تقرير التحليل الجنائي (Forensic Report)</h3>", unsafe_allow_html=True)
        st.write(f"**الهدف المستهدف:** `{target_url}`")
        st.markdown("---")
        
        if alerts or vt_hits > 0:
            for a in alerts: st.markdown(f"<p class='danger-text'>{a}</p>", unsafe_allow_html=True)
            if vt_hits > 0: st.markdown(f"<p class='danger-text'>🚨 تم تصنيف الرابط كخبيث من قبل {vt_hits} مصدر أمني عالمي.</p>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background:rgba(255,75,75,0.1); padding:15px; border-radius:10px; border:1px solid #ff4b4b; margin-top:20px;">
                    <h4 style="color:#ff4b4b; margin:0;">💡 توصية المهندس زيد (Zaid's Advisory):</h4>
                    <p style="margin:5px 0 0 0;">الرابط يشكل خطراً أمنياً. يوصى بحظر الدخول وتنبيه فريق الاستجابة للحوادث.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<p class='safe-text'>✅ لم يتم رصد أي أنماط مشبوهة في هذا الرابط حالياً.</p>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# --- تذييل الصفحة الثابت ---
st.markdown(f"""
    <div class="footer">
        بواسطة: المهندس زيد الجنابي | كلية هندسة تقنيات الأمن السيبراني - جامعة المعارف
    </div>
""", unsafe_allow_html=True)
