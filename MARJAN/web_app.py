import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري الاحترافي (نفس التصميم في Screenshot 2026-05-01 094203_2.png) ---
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
    h3 { color: #D4AF37 !important; text-align: center; font-weight: normal; }

    .stButton>button { 
        width: 100%; background-color: #D4AF37 !important; color: black !important; 
        font-weight: bold; border-radius: 12px; height: 3.8em; 
        box-shadow: 0px 0px 20px rgba(212, 175, 55, 0.3);
    }

    .result-box { 
        padding: 25px; border-radius: 20px; border: 1px solid rgba(212, 175, 55, 0.4); 
        background-color: rgba(0, 0, 0, 0.85); text-align: right; margin-top: 20px;
        backdrop-filter: blur(15px);
    }

    .heuristic-danger { 
        padding: 12px; border-radius: 10px; border-right: 5px solid #ff4b4b; 
        background-color: rgba(255, 75, 75, 0.1); color: #ff9999; 
        text-align: right; margin-bottom: 8px; font-size: 0.9em;
    }
    
    .footer { 
        position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; 
        color: #D4AF37; padding: 10px; background-color: rgba(5, 7, 10, 0.9); 
        border-top: 1px solid #D4AF37; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- محرك التحليل الجنائي المتقدم (Extreme Heuristic Mode) ---
def deep_security_analysis(url):
    alerts = []
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    full_path = url.lower()
    
    # 1. كشف النطاقات العشوائية (Entropy/Randomness Detection)
    # الروابط الخبيثة غالباً تستخدم حروف وأرقام عشوائية مثل meritking1689
    if re.search(r'\d{3,}', domain) or len(re.findall(r'[0-9]', domain)) > 4:
        alerts.append("❗ نمط عشوائي مريب: اسم النطاق يحتوي على تسلسل رقمي مريب يُستخدم عادةً في الروابط المؤقتة.")

    # 2. كشف الكلمات الجاذبة لعمليات الاحتيال (Scam/Phishing Keywords)
    scam_keywords = ['king', 'win', 'prize', 'gift', 'bonus', 'claim', 'login', 'secure', 'verify', 'merit']
    if any(word in full_path for word in scam_keywords):
        alerts.append("⚠️ كلمات تحفيزية: الرابط يحتوي على مصطلحات تُستخدم في هندسة الاحتيال الاجتماعي.")

    # 3. كشف النطاقات الفرعية الطويلة (Subdomain Analysis)
    if domain.count('.') > 2:
        alerts.append("❗ تضليل النطاق: استخدام نطاقات فرعية متعددة لإخفاء الهوية الحقيقية للموقع.")

    # 4. كشف انتحال الهوية (Brand Mimicry)
    common_targets = ['google', 'facebook', 'binance', 'apple', 'pay', 'bank']
    for brand in common_targets:
        if brand in domain and domain.split('.')[-2] != brand:
            alerts.append(f"⚠️ شبهة انتحال: الرابط يحاول محاكاة العلامة التجارية '{brand}'.")

    # 5. فحص خدمات الاستضافة المشبوهة
    if any(host in domain for host in ['pages.dev', 'web.app', 'firebaseapp.com', 'github.io', '000webhost']):
        alerts.append("🟡 بيئة استضافة مجانية: الموقع يعمل على خدمة استضافة غالباً ما تُستغل لإطلاق هجمات سريعة.")

    return alerts

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3>التحليل الجنائي والذكاء الاستباقي للروابط</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="...أدخل الرابط للفحص الفوري")

if st.button("تشغيل الفحص الرقمي"):
    if not target_url:
        st.warning("⚠️ يرجى إدخال رابط للفحص")
    else:
        # تنفيذ التحليل الاستباقي المعمق أولاً
        heuristic_results = deep_security_analysis(target_url)
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري تنفيذ بروتوكولات الفحص والتحليل الجنائي..."):
            try:
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                
                if response.status_code == 404:
                    requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": target_url})
                    time.sleep(5) 
                    response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)

                st.markdown("---")

                # عرض تنبيهات "مرجان" (هذا الجزء هو الذي سيكشف الرابط حتى لو كان "سليماً" عالمياً)
                if heuristic_results:
                    st.subheader("🕵️ نتائج تحليل محرك مرجان الاستباقي:")
                    for alert in heuristic_results:
                        st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
                
                if response.status_code == 200:
                    data = response.json()['data']['attributes']
                    stats = data.get('last_analysis_stats', {})
                    malicious = stats.get('malicious', 0)
                    
                    if malicious > 0:
                        st.error(f"🚨 تأكيد التهديد! تم تصنيف الرابط كخطر بواسطة {malicious} مختبر عالمي.")
                    elif heuristic_results:
                        st.warning("⚠️ المختبرات العالمية لم ترصد تهديداً بعد، ولكن 'مرجان' ينصح بالحذر الشديد بناءً على الأنماط المريبة المكتشفة.")
                    else:
                        st.success("✅ الرابط يبدو آمناً بناءً على الفحص الحالي.")
                    
                    # رابط مراجعة السلوك التقني العميق
                    st.info(f"🔗 [لمراجعة السلوك التقني العميق اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")
                else:
                    st.error("⚠️ فشل في سحب البيانات العالمية.")

            except Exception as e:
                st.error(f"حدث خطأ في محرك الفحص.")

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace System v2.5</div>', unsafe_allow_html=True)
