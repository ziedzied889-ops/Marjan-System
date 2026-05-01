import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري (ثابت كما هو في Screenshot 2026-05-01 142240.jpg) ---
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
    .stButton>button { width: 100%; background-color: #D4AF37 !important; color: black !important; font-weight: bold; border-radius: 12px; height: 3.8em; box-shadow: 0px 0px 20px rgba(212, 175, 55, 0.3); }
    .heuristic-danger { padding: 12px; border-radius: 10px; border-right: 5px solid #ff4b4b; background-color: rgba(255, 75, 75, 0.1); color: #ff9999; text-align: right; margin-bottom: 8px; font-size: 0.9em; border-left: 1px solid rgba(255,75,75,0.2); }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #D4AF37; padding: 10px; background-color: rgba(5, 7, 10, 0.9); border-top: 1px solid #D4AF37; }
    .stTextInput>div>div>input { background-color: rgba(255, 255, 255, 0.05) !important; color: white !important; border: 1px solid rgba(212, 175, 55, 0.3) !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- محرك الذكاء الاصطناعي الاستباقي (Marjan Intelligence Core) ---
def deep_forensic_analysis(url):
    alerts = []
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    path = parsed.path.lower()
    full_url = url.lower()

    # 1. تحليل التشابه البصري (Typosquatting Detection)
    # كشف محاولات تقليد النطاقات الشهيرة بتبديل حروف بسيطة
    targets = {'facebook.com': 'facebo0k', 'google.com': 'g00gle', 'binance.com': 'binance-support', 'apple.com': 'appIe'}
    for official, fake_part in targets.items():
        if fake_part in netloc:
            alerts.append(f"🚨 انتحال بصري: النطاق يحاول تقليد منصة '{official.split('.')[0]}' بشكل مضلل.")

    # 2. كشف الروابط الديناميكية العشوائية (Entropy Logic)
    # الروابط التي تحتوي على تسلسل حروف وأرقام طويل وغير مفهوم (مثل meritking1689)
    if re.search(r'[a-z0-9]{10,}', netloc) or len(re.findall(r'\d', netloc)) > 5:
        alerts.append("❗ بنية مشبوهة: النطاق يحتوي على تسلسل عشوائي رقمي؛ أسلوب شائع في روابط 'التصيد السريع'.")

    # 3. كشف كلمات الاحتيال والهندسة الاجتماعية (Social Engineering Patterns)
    scam_regex = r"(king|win|claim|gift|prize|bonus|login|verify|secure|update|bank|account|merit)"
    if re.search(scam_regex, full_url):
        alerts.append("⚠️ هندسة اجتماعية: تم رصد مصطلحات 'طعم' تُستخدم لإغراء الضحايا بالضغط على الرابط.")

    # 4. كشف النطاقات الفرعية المفرطة (Tunneling Detection)
    if netloc.count('.') > 3:
        alerts.append("❗ تضليل تقني: استخدام طبقات متعددة من النطاقات الفرعية لإخفاء المصدر الحقيقي.")

    # 5. كشف ملفات الاختبار والمنظمات الأمنية (EICAR / Test Files)
    if "eicar" in full_url:
        alerts.append("🔍 ملف اختبار: تم رصد بصمة EICAR؛ هذا الرابط مخصص لأغراض فحص فاعلية الأنظمة فقط.")

    # 6. فحص الاستضافة (Host Reputation)
    if any(h in netloc for h in ['pages.dev', 'web.app', 'github.io', '000webhost', 'firebaseapp']):
        alerts.append("🟡 استضافة مفتوحة: الرابط يعمل على منصة استضافة مجانية؛ يجب الحذر من محتوى هذه الصفحات.")

    return alerts

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3>التحليل الجنائي والذكاء الاستباقي للروابط</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="...أدخل الرابط للفحص الفوري")

if st.button("تشغيل الفحص الرقمي"):
    if not target_url:
        st.warning("⚠️ يرجى إدخال رابط للفحص")
    else:
        # تنفيذ التحليل الاستباقي المعمق
        heuristic_results = deep_forensic_analysis(target_url)
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري تنفيذ بروتوكولات الفحص والتحليل الجنائي..."):
            try:
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                
                # معالجة الروابط الجديدة التي لم تُفحص سابقاً
                if response.status_code == 404:
                    requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": target_url})
                    time.sleep(7) 
                    response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)

                st.markdown("---")

                # عرض التحليل الذكي لنظام مرجان
                if heuristic_results:
                    st.subheader("🕵️ نتائج تحليل محرك مرجان الذكي:")
                    for alert in heuristic_results:
                        st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
                
                if response.status_code == 200:
                    data = response.json()['data']['attributes']
                    stats = data.get('last_analysis_stats', {})
                    malicious = stats.get('malicious', 0)
                    suspicious = stats.get('suspicious', 0)
                    
                    # دمج قرارات المختبرات مع قرار "مرجان"
                    if malicious > 0 or suspicious > 0:
                        st.error(f"🚨 تأكيد التهديد! تم رصد الرابط كخطر بواسطة {malicious + suspicious} مختبر عالمي.")
                    elif heuristic_results:
                        st.warning("⚠️ تنبيه: المختبرات العالمية تعتبر الرابط سليماً، لكن 'مرجان' ينصح بالحذر الشديد بناءً على الأنماط المريبة.")
                    else:
                        st.success("✅ الرابط يبدو آمناً بناءً على الفحص الحالي.")
                    
                    # رابط السلوك التقني العميق
                    st.info(f"🔗 [لمراجعة السلوك التقني العميق اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")
                else:
                    st.error("⚠️ فشل في الوصول لقاعدة البيانات العالمية.")

            except Exception:
                st.error("حدث خطأ تقني في محرك الفحص.")

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace System v3.0</div>', unsafe_allow_html=True)
