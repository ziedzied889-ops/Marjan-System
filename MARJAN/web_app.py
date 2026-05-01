import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري المتطور مع درع الأمن والشبكة الرقمية ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #05070a !important;
        background-image: 
            url("https://www.transparentpng.com/download/security/shield-security-icon-9.png"),
            linear-gradient(rgba(212, 175, 55, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(212, 175, 55, 0.03) 1px, transparent 1px),
            radial-gradient(circle at center, #11141a 0%, #05070a 100%) !important;
        background-position: center 40%, center, center, center !important;
        background-repeat: no-repeat, repeat, repeat, no-repeat !important;
        background-size: 380px auto, 30px 30px, 30px 30px, 100% 100% !important;
        background-attachment: fixed !important;
    }

    h1 { 
        color: #D4AF37 !important; 
        text-align: center; 
        text-shadow: 0px 0px 20px rgba(212, 175, 55, 0.8) !important; 
        font-family: 'Courier New', Courier, monospace; 
        margin-top: -30px;
    }

    .stButton>button { 
        width: 100%; 
        background-color: #D4AF37 !important; 
        color: black !important; 
        font-weight: bold; 
        border-radius: 12px; 
        height: 3.8em; 
        transition: 0.5s;
        box-shadow: 0px 0px 20px rgba(212, 175, 55, 0.3);
    }

    .result-box { 
        padding: 25px; 
        border-radius: 20px; 
        border: 1px solid rgba(212, 175, 55, 0.4); 
        background-color: rgba(0, 0, 0, 0.85); 
        text-align: right; 
        margin-top: 20px;
        backdrop-filter: blur(15px);
    }

    .heuristic-danger { 
        padding: 15px; 
        border-radius: 10px; 
        border: 2px solid #ff4b4b; 
        background-color: rgba(100, 0, 0, 0.3); 
        color: #ff9999; 
        text-align: right; 
        margin-bottom: 10px;
        font-weight: bold;
    }
    
    .footer { 
        position: fixed; 
        left: 0; bottom: 0; width: 100%; 
        text-align: center; 
        color: #D4AF37; 
        padding: 10px; 
        background-color: rgba(5, 7, 10, 0.9); 
        border-top: 1px solid #D4AF37; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- محرك التحليل الاستباقي المطور (لحل مشكلة الروابط المخفية) ---
def advanced_heuristic_analysis(url):
    alerts = []
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    path = parsed_url.path.lower()
    
    # 1. كشف المواقع المجانية (أكبر مصدر للروابط الخبيثة)
    malicious_hosts = ['canva.site', 'wixsite.com', 'web.app', 'firebaseapp.com', 'github.io', '000webhost', 'pages.dev']
    if any(host in domain for host in malicious_hosts):
        alerts.append("⚠️ تحذير: الرابط مستضاف على خدمة مجانية؛ غالباً ما تُستخدم في حملات التصيد.")

    # 2. كشف الكلمات المريبة في المسار (Path) وليس الدومين فقط
    danger_keywords = ['login', 'signin', 'verify', 'bank', 'secure', 'update', 'account', 'office', 'password']
    if any(word in url.lower() for word in danger_keywords):
        alerts.append("⚠️ تحذير: يحتوي الرابط على كلمات تدل على محاولة سرقة بيانات (Tactic: Phishing).")

    # 3. فحص البروتوكول
    if not url.startswith("https://"):
        alerts.append("🚫 خطر: الرابط غير مشفر (HTTP)؛ أي بيانات تدخلها يمكن سرقتها بسهولة.")

    # 4. كشف الروابط الطويلة جداً (Obfuscation)
    if len(url) > 80:
        alerts.append("⚠️ تحذير: الرابط طويل جداً؛ قد يكون محاولة لإخفاء النطاق الحقيقي.")

    return alerts

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام التتبع الجنائي الذكي</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="ضع الرابط هنا للفحص...")

if st.button("تحليل الرابط الآن"):
    if not target_url:
        st.warning("⚠️ يرجى إدخال رابط أولاً")
    else:
        # تنفيذ التحليل الاستباقي أولاً
        heuristic_results = advanced_heuristic_analysis(target_url)
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري التحليل المعمق..."):
            try:
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                
                # إذا كان الرابط جديداً، نطلبه للفحص
                if response.status_code == 404:
                    requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": target_url})
                    st.info("ℹ️ هذا الرابط جديد؛ تم إرساله للمختبرات العالمية، انتظر ثوانٍ...")
                    time.sleep(5)
                    response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)

                st.markdown("---")

                # عرض تحذيرات "مرجان" الاستباقية بغض النظر عن نتيجة المختبرات
                if heuristic_results:
                    st.subheader("🕵️ نتائج فحص محرك مرجان الذكي:")
                    for alert in heuristic_results:
                        st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
                
                # عرض نتائج المختبرات العالمية
                if response.status_code == 200:
                    stats = response.json()['data']['attributes']['last_analysis_stats']
                    malicious = stats.get('malicious', 0)
                    
                    if malicious > 0:
                        st.error(f"🚨 المختبرات العالمية تؤكد: الرابط خبيث (تم رصده من قبل {malicious} مصدر)")
                    elif heuristic_results:
                        st.warning("⚠️ المختبرات العالمية لم ترصده بعد، ولكن 'مرجان' ينصح بالحذر الشديد بناءً على سلوك الرابط.")
                    else:
                        st.success("✅ الرابط يبدو آمناً حالياً.")
                
                st.markdown(f'<div class="result-box">الرابط المفحوص: {target_url}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error("حدث خطأ في الاتصال بقاعدة البيانات العالمية.")

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace System v2.0</div>', unsafe_allow_html=True)
