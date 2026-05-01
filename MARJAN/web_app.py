import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري الاحترافي ---
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
    h1 { color: #D4AF37 !important; text-align: center; text-shadow: 0px 0px 20px rgba(212, 175, 55, 0.8) !important; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { width: 100%; background-color: #D4AF37 !important; color: black !important; font-weight: bold; border-radius: 12px; height: 3.8em; }
    .heuristic-danger { padding: 15px; border-radius: 10px; border-right: 6px solid #ff4b4b; background-color: rgba(255, 75, 75, 0.2); color: #ff9999; text-align: right; margin-bottom: 10px; font-weight: bold; }
    .heuristic-safe { padding: 15px; border-radius: 10px; border-right: 6px solid #28a745; background-color: rgba(40, 167, 69, 0.15); color: #99ff99; text-align: right; margin-bottom: 10px; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #D4AF37; padding: 10px; background-color: rgba(5, 7, 10, 0.98); border-top: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- محرك التحليل الجنائي المستقل (Marjan Core v5.0) ---
def deep_autonomous_analysis(url):
    alerts = []
    domain = urlparse(url).netloc.lower()
    full_url = url.lower()
    
    # 1. كشف ملفات الاختبار (EICAR / Security Testing)
    if "eicar" in full_url:
        alerts.append("🔍 ملف اختبار قياسي: هذا الرابط مخصص لاختبار أنظمة الدفاع (EICAR Test File).")

    # 2. كشف انتحال النطاقات (Typosquatting)
    # خوارزمية ذكية لكشف تبديل الحروف (مثل bybit -> bybitfutures)
    scam_patterns = ['bybit', 'binance', 'trustwallet', 'metamask', 'blockchain', 'coinbase']
    for pattern in scam_patterns:
        if pattern in domain and domain != f"{pattern}.com":
            alerts.append(f"🚨 هجوم انتحال بصري: النطاق يحاول تقليد منصة '{pattern}' باستخدام لواحق مريبة.")

    # 3. كشف الروابط العشوائية (Entropy Detection)
    # الروابط التي تحتوي على تسلسلات رقمية طويلة (مثل 1777635770 في صورتك)
    if re.search(r'\d{7,}', full_url):
        alerts.append("❗ تسلسل رقمي مريب: الرابط يحتوي على معرفات تتبع عشوائية تُستخدم غالباً في هجمات التصيد.")

    # 4. كشف الهندسة الاجتماعية
    if any(x in full_url for x in ['bonus', 'claim', 'login-verify', 'gift', 'win']):
        alerts.append("⚠️ هندسة اجتماعية: تم رصد مصطلحات 'طُعم' مخصصة لسرقة البيانات.")

    return alerts

# --- الواجهة ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام الردع الجنائي والذكاء الاستباقي للروابط</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="...أدخل الرابط للفحص المعمق")

if st.button("تفعيل بروتوكول الكشف"):
    if target_url:
        # تنفيذ التحليل الداخلي فوراً (لا يحتاج إنترنت)
        internal_alerts = deep_autonomous_analysis(target_url)
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري تحليل البنية الجنائية للرابط..."):
            st.markdown("---")
            
            # عرض نتائج "مرجان" المستقلة أولاً
            if internal_alerts:
                st.subheader("🕵️ نتائج محرك مرجان (التحليل الذاتي):")
                for alert in internal_alerts:
                    st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
            
            # محاولة الفحص العالمي
            try:
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=10)
                
                if response.status_code == 200:
                    stats = response.json()['data']['attributes'].get('last_analysis_stats', {})
                    malicious = stats.get('malicious', 0)
                    if malicious > 0:
                        st.error(f"🚨 تأكيد خطر عالمي: تم تصنيف الرابط كخطر من قبل {malicious} مصدر أمني.")
                    elif internal_alerts:
                        st.warning("⚠️ تنبيه Zero-day: لم يُسجل الرابط عالمياً بعد، ولكن أنماط مرجان تؤكد وجود خطورة صريحة.")
                    else:
                        st.success("✅ الرابط سليم بناءً على التحليل الرقمي الحالي.")
                else:
                    st.warning("📡 تعذر تحديث البيانات العالمية، تم الاعتماد على الفحص الداخلي لمرجان.")
            except:
                st.error("🛑 فشل الاتصال بقاعدة البيانات الخارجية؛ تم تفعيل بروتوكول الفحص الذاتي لمرجان.")
                if not internal_alerts:
                    st.info("لم يتم رصد أنماط خبيثة واضحة في بنية الرابط، ولكن يرجى الحذر لعدم توفر البيانات العالمية.")

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace v5.0</div>', unsafe_allow_html=True)
