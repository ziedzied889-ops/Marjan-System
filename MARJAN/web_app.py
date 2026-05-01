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
    .heuristic-danger { padding: 15px; border-radius: 10px; border-right: 6px solid #ff4b4b; background-color: rgba(255, 75, 75, 0.25); color: #ff9999; text-align: right; margin-bottom: 10px; font-weight: bold; border-left: 1px solid rgba(255,75,75,0.4); }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #D4AF37; padding: 10px; background-color: rgba(5, 7, 10, 0.98); border-top: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- المحرك الجنائي الذكي (Marjan Ultra Logic) ---
def advanced_scam_detector(url):
    reasons = []
    domain = urlparse(url).netloc.lower()
    full_url = url.lower()
    
    # 1. كشف انتحال المنصات (The bybitfutures detector)
    known_brands = ['bybit', 'binance', 'coinbase', 'kucoin', 'meta', 'google', 'apple', 'paypal']
    for brand in known_brands:
        if brand in domain and domain != f"{brand}.com":
            reasons.append(f"🚨 محاولة انتحال: الرابط يستخدم اسم '{brand}' في نطاق غير رسمي.")

    # 2. كشف كلمات الاستدراج (Scam Keywords)
    scam_words = ['futures', 'trade', 'login', 'verify', 'claim', 'bonus', 'free', 'gift', 'win']
    if any(word in full_url for word in scam_words):
        reasons.append("⚠️ هندسة اجتماعية: تم رصد مصطلحات 'طُعم' تُستخدم غالباً في منصات التداول الوهمية.")

    # 3. تحليل النطاقات المشبوهة
    if re.search(r'\d{2,}', domain): # وجود أرقام متتالية في الدومين
        reasons.append("❗ بنية مريبة: اسم النطاق يحتوي على أرقام عشوائية، وهي سمة للروابط المؤقتة.")

    return reasons

# --- الواجهة ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام الردع الجنائي والذكاء الاصطناعي</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="أدخل الرابط المشبوه للتحليل...")

if st.button("تفعيل بروتوكول الكشف"):
    if target_url:
        # فحص مرجان أولاً وقبل كل شيء
        marjan_analysis = advanced_scam_detector(target_url)
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري تنفيذ التحليل الاستباقي المعمق..."):
            try:
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                st.markdown("---")

                # عرض تحذيرات مرجان فوراً (حتى لو النتيجة العالمية "سليم")
                if marjan_analysis:
                    st.subheader("🕵️ اكتشافات محرك مرجان الاستباقي:")
                    for r in marjan_analysis:
                        st.markdown(f'<div class="heuristic-danger">{r}</div>', unsafe_allow_html=True)
                
                # دمج النتيجة العالمية
                if response.status_code == 200:
                    malicious = response.json()['data']['attributes'].get('last_analysis_stats', {}).get('malicious', 0)
                    if malicious > 0:
                        st.error(f"🚨 تأكيد عالمي: الرابط خبيث بشهادة {malicious} مختبر.")
                    elif marjan_analysis:
                        st.warning("⚠️ تنبيه Zero-day: الرابط جديد عالمياً، لكن محرك مرجان رصد سلوك انتحال صريح. لا تفتحه!")
                    else:
                        st.success("✅ الرابط يبدو آمناً بناءً على الفحص الحالي.")
                else:
                    if marjan_analysis:
                        st.warning("⚠️ تنبيه: تعذر جلب البيانات العالمية، لكن محرك مرجان يؤكد وجود شبهة عالية.")
                    else:
                        st.error("⚠️ فشل في الاتصال بقاعدة البيانات.")
            except:
                st.error("خطأ في المحرك.")

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace v4.5</div>', unsafe_allow_html=True)
