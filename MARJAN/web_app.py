import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري (ثابت لضمان الهوية البصرية) ---
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
    .heuristic-danger { padding: 15px; border-radius: 10px; border-right: 6px solid #ff4b4b; background-color: rgba(255, 75, 75, 0.2); color: #ff9999; text-align: right; margin-bottom: 10px; font-weight: bold; border-left: 1px solid rgba(255,75,75,0.4); box-shadow: 0px 5px 15px rgba(0,0,0,0.3); }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #D4AF37; padding: 10px; background-color: rgba(5, 7, 10, 0.98); border-top: 1px solid #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# --- محرك التحليل السلوكي المتطور (Marjan Forensic Engine v4.0) ---
def ultimate_security_logic(url):
    alerts = []
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    full_url = url.lower()
    
    # 1. كشف النطاقات المشبوهة (Top-Level Domain Analysis)
    # النطاقات التي تنتهي بـ .xyz, .top, .online, .site غالباً ما تُستخدم في الهجمات
    suspicious_tlds = ['.xyz', '.top', '.pw', '.online', '.site', '.club', '.tk', '.ml', '.ga', '.cf', '.gq']
    if any(domain.endswith(tld) for tld in suspicious_tlds):
        alerts.append(f"❗ نطاق عالي الخطورة: الامتداد ({domain.split('.')[-1]}) يُصنف إحصائياً كأحد أكثر النطاقات استخداماً في الهجمات السيبرانية.")

    # 2. خوارزمية كشف العشوائية (Advanced Entropy Detection)
    # كشف الروابط التي تحتوي على أكثر من 3 أرقام متتالية أو رموز غريبة في الدومين
    if re.search(r'\d{3,}', domain) or len(re.findall(r'[\-\d]', domain)) > 3:
        alerts.append("🚨 بصمة توليد آلي: تم رصد نمط (DGA)؛ اسم النطاق لا يبدو بشرياً بل تم توليده برمجياً للتضليل.")

    # 3. كشف الهندسة الاجتماعية (Deep Keyword Intelligence)
    scam_patterns = ['king', 'win', 'prize', 'gift', 'merit', 'bonus', 'claim', 'verify', 'update', 'account', 'login', 'secure', 'billing', 'support']
    if any(pattern in full_url for pattern in scam_patterns):
        alerts.append("⚠️ هندسة اجتماعية: الرابط يستخدم مصطلحات 'طُعم' مخصصة لسرقة بيانات المستخدمين.")

    # 4. كشف انتحال الهوية (Brand Mimicry & Homograph)
    if "xn--" in domain or "@" in domain:
        alerts.append("❗ تمويه رقمي: الرابط يستخدم تقنية Punycode أو الرموز المخفية لانتحال مواقع رسمية.")

    # 5. كشف الاستضافة المجانية والـ Redirects
    free_hosts = ['canva.site', 'wixsite.com', 'web.app', 'firebaseapp.com', 'github.io', 'pages.dev', '000webhostapp.com', 'bit.ly', 't.co', 'tinyurl.com']
    if any(host in domain for host in free_hosts):
        alerts.append("⚠️ وسيط مجهول: الرابط مستضاف على خدمة مجانية أو يستخدم اختصاراً للروابط لإخفاء الوجهة النهائية.")

    return alerts

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام الردع الجنائي والذكاء الاصطناعي للروابط</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="...ضع الرابط هنا للتحليل الجنائي المعمق")

if st.button("تفعيل بروتوكول الكشف"):
    if not target_url:
        st.warning("⚠️ يرجى إدخال الرابط أولاً")
    else:
        # تنفيذ التحليل الاستباقي العنيف
        heuristic_alerts = ultimate_security_logic(target_url)
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري كسر تشفير الرابط وتحليل السجل الجنائي..."):
            try:
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                
                # التعامل مع الروابط الجديدة فوراً
                if response.status_code == 404:
                    requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": target_url})
                    st.info("ℹ️ الرابط جديد كلياً؛ تم إرساله للفحص العالمي الآن. يرجى الانتظار...")
                    time.sleep(10) # زيادة وقت الانتظار لضمان دقة التحليل الأولي
                    response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)

                st.markdown("---")

                # عرض تحذيرات "مرجان" (الأولوية القصوى لمنع الفشل)
                if heuristic_alerts:
                    st.subheader("🕵️ نتائج التحليل الجنائي لمحرك مرجان:")
                    for alert in heuristic_alerts:
                        st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
                
                if response.status_code == 200:
                    stats = response.json()['data']['attributes'].get('last_analysis_stats', {})
                    malicious = stats.get('malicious', 0)
                    suspicious = stats.get('suspicious', 0)
                    
                    if malicious > 0 or suspicious > 0:
                        st.error(f"🚨 تأكيد الخطر! الرابط مصنف كتهديد من قبل {malicious + suspicious} مختبر عالمي.")
                    elif heuristic_alerts:
                        # هذا هو "صمام الأمان": لو المختبرات العالمية أخطأت، مرجان يصححها
                        st.warning("⚠️ تنبيه أمني حرج: المختبرات العالمية لم ترصد التهديد بعد (Zero-day)، ولكن خوارزمية مرجان اكتشفت سلوكاً عدائياً صريحاً. ينصح بعدم الدخول.")
                    else:
                        st.success("✅ الرابط سليم بناءً على المعايير الأمنية الحالية.")
                    
                    # رابط السلوك التقني العميق (دائماً متاح للمهندس)
                    st.info(f"🔗 [لمراجعة السلوك التقني العميق اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")
                else:
                    st.error("⚠️ تعذر جلب التقارير العالمية حالياً.")
            except:
                st.error("خطأ تقني في الاتصال بالخادم.")

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace System v4.0</div>', unsafe_allow_html=True)
