import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري ---
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
    h1 { color: #D4AF37 !important; text-align: center; text-shadow: 0px 0px 20px rgba(212, 175, 55, 0.8) !important; }
    .stButton>button { width: 100%; background-color: #D4AF37 !important; color: black !important; font-weight: bold; border-radius: 12px; height: 3.8em; }
    .heuristic-danger { padding: 12px; border-radius: 10px; border-right: 5px solid #ff4b4b; background-color: rgba(255, 75, 75, 0.1); color: #ff9999; text-align: right; margin-bottom: 8px; }
    .heuristic-info { padding: 12px; border-radius: 10px; border-right: 5px solid #00ccff; background-color: rgba(0, 204, 255, 0.1); color: #99ebff; text-align: right; margin-bottom: 8px; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #D4AF37; padding: 10px; background-color: rgba(5, 7, 10, 0.9); border-top: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- محرك التحليل الجنائي المحدث (Standard Test File Detection) ---
def advanced_security_scan(url):
    alerts = []
    info = []
    domain = urlparse(url).netloc.lower()
    
    # 1. كشف ملفات اختبار EICAR القياسية
    if "eicar" in url.lower():
        info.append("🔍 تنبيه: هذا الرابط مرتبط بملفات اختبار الأمن القياسية (EICAR). يُستخدم لاختبار فاعلية برامج الحماية.")

    # 2. تحليل الأنماط المريبة (نفس المنطق السابق لتقوية الاكتشاف)
    if re.search(r'\d{4,}', domain):
        alerts.append("❗ نمط عشوائي: اسم النطاق يحتوي على تسلسل رقمي مريب.")
    
    if any(word in url.lower() for word in ['king', 'win', 'prize', 'merit', 'bonus']):
        alerts.append("⚠️ كلمات تحفيزية: الرابط يستخدم أسلوب الهندسة الاجتماعية.")

    return alerts, info

# --- الواجهة ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام التحليل الاستباقي والكشف الجنائي</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="أدخل الرابط للفحص...")

if st.button("تشغيل الفحص الرقمي"):
    if target_url:
        alerts, info = advanced_security_scan(target_url)
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري تحليل البصمة الرقمية..."):
            try:
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                st.markdown("---")

                # عرض معلومات ملفات الاختبار
                for i in info:
                    st.markdown(f'<div class="heuristic-info">{i}</div>', unsafe_allow_html=True)

                # عرض تنبيهات مرجان
                for a in alerts:
                    st.markdown(f'<div class="heuristic-danger">{a}</div>', unsafe_allow_html=True)
                
                if response.status_code == 200:
                    malicious = response.json()['data']['attributes'].get('last_analysis_stats', {}).get('malicious', 0)
                    if malicious > 0:
                        st.error(f"🚨 تم تأكيد التهديد بواسطة {malicious} مختبر عالمي.")
                    elif alerts:
                        st.warning("🟡 تحذير: لم يُصنف عالمياً بعد، لكن أنماط 'مرجان' تشير لشبهة عالية.")
                    else:
                        st.success("✅ الرابط سليم بناءً على البيانات المتوفرة.")
                    
                    st.info(f"🔗 [لمراجعة السلوك التقني العميق اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")
                else:
                    st.error("⚠️ تعذر جلب البيانات العالمية.")
            except:
                st.error("خطأ في الاتصال.")

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace System v2.6</div>', unsafe_allow_html=True)
