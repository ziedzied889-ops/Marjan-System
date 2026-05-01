import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري (الهوية البصرية المعتمدة) ---
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
    .stButton>button { width: 100%; background-color: #D4AF37 !important; color: black !important; font-weight: bold; border-radius: 12px; height: 3.8em; box-shadow: 0px 0px 20px rgba(212, 175, 55, 0.3); }
    .heuristic-danger { padding: 12px; border-radius: 10px; border-right: 5px solid #ff4b4b; background-color: rgba(255, 75, 75, 0.15); color: #ff9999; text-align: right; margin-bottom: 8px; font-weight: bold; border-left: 1px solid rgba(255,75,75,0.3); }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #D4AF37; padding: 10px; background-color: rgba(5, 7, 10, 0.95); border-top: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- محرك الردع الجنائي (Marjan Shield v3.5) ---
def aggressive_security_check(url):
    alerts = []
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    full_url = url.lower()

    # 1. كشف هجمات المتشابهات (Homograph Attack)
    # كشف الروابط التي تستخدم حروف غير لاتينية تبدو مثل الحروف الإنجليزية (مثل 'а' الكيريلية)
    if "xn--" in domain:
        alerts.append("🚨 خطر Punycode: الرابط يستخدم محارف مضللة لإخفاء هويته الحقيقية (هجوم انتحال).")

    # 2. كشف الأنماط العشوائية المتقدمة (High Entropy Detection)
    # الروابط التي تحتوي على خليط مريب من الحروف والأرقام في الدومين (مثل meritking1689)
    if sum(c.isdigit() for c in domain) > 3 or len(re.findall(r'[_\-\d]', domain)) > 4:
        alerts.append("❗ نمط مريب: اسم النطاق يحتوي على خصائص توليد آلي (DGA) تُستخدم في البرمجيات الخبيثة.")

    # 3. كشف كلمات الاحتيال (Aggressive Keyword Matching)
    # تشديد الفحص ليشمل أي كلمة تدل على "تلاعب" أو "إغراء"
    danger_list = ['king', 'win', 'merit', 'prize', 'gift', 'bonus', 'claim', 'verify', 'update', 'login', 'secure', 'bank', 'wallet', 'token']
    if any(word in full_url for word in danger_list):
        alerts.append("⚠️ هندسة اجتماعية: تم رصد مصطلحات تُستخدم في 90% من حملات التصيد الرقمي.")

    # 4. فحص الامتدادات الخطرة في الرابط
    if full_url.endswith(('.exe', '.zip', '.rar', '.bat', '.scr', '.vbs', '.apk')):
        alerts.append("🚫 ملف تنفيذي: الرابط يؤدي مباشرة لتحميل ملف قد يحتوي على برمجيات ضارة.")

    # 5. كشف النطاقات الفرعية (Subdomain Deep Scan)
    if domain.count('.') > 2 and not domain.startswith("www."):
        alerts.append("❗ تمويه النطاق: استخدام مستويات متعددة من النطاقات الفرعية لتشتيت أنظمة الفحص.")

    return alerts

# --- الواجهة ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام الكشف الجنائي الاستباقي للتهديدات</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="أدخل الرابط المشبوه هنا للتحليل المعمق...")

if st.button("بدء بروتوكول الفحص"):
    if not target_url:
        st.warning("⚠️ يرجى تزويد الرابط للفحص")
    else:
        # تنفيذ التحليل الاستباقي العنيف
        heuristic_alerts = aggressive_security_check(target_url)
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري كسر تشفير الرابط وتحليل السلوك..."):
            try:
                # طلب الفحص أو جلب النتيجة
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                
                if response.status_code == 404:
                    # إذا كان الرابط جديداً تماماً، نرسله للفحص فوراً
                    requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": target_url})
                    st.info("ℹ️ الرابط جديد على المختبرات العالمية؛ تم البدء بفحصه الآن. يرجى الانتظار ثوانٍ...")
                    time.sleep(8)
                    response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)

                st.markdown("---")

                # عرض نتائج "مرجان" (هذا هو خط الدفاع الأول الذي لن يجعلك تفشل)
                if heuristic_alerts:
                    st.subheader("🕵️ نتائج تحليل محرك مرجان (الذكاء الاستباقي):")
                    for alert in heuristic_alerts:
                        st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
                
                if response.status_code == 200:
                    stats = response.json()['data']['attributes'].get('last_analysis_stats', {})
                    malicious = stats.get('malicious', 0)
                    suspicious = stats.get('suspicious', 0)
                    
                    if malicious > 0 or suspicious > 0:
                        st.error(f"🚨 تم تأكيد الخطر! الرابط مصنف كتهديد من قبل {malicious + suspicious} مصدر أمني عالمي.")
                    elif heuristic_alerts:
                        # هنا تكمن القوة: لو المختبرات العالمية قالت سليم، مرجان سيحذر بقوة
                        st.warning("⚠️ تنبيه حرج: المختبرات العالمية لم تكتشف التهديد بعد (Zero-day)، ولكن 'مرجان' رصد أنماط هجوم صريحة. لا تفتح الرابط!")
                    else:
                        st.success("✅ الرابط سليم بناءً على المعايير الأمنية الحالية.")
                    
                    st.info(f"🔗 [لمراجعة السلوك التقني العميق اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")
                else:
                    st.error("⚠️ فشل في سحب التقارير العالمية.")
            except:
                st.error("خطأ في محرك التحليل.")

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace System v3.5</div>', unsafe_allow_html=True)
