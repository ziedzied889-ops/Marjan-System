import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري (الدرع، الشبكة الرقمية، والتوهج الذهبي) ---
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
    }

    .stButton>button { 
        width: 100%; 
        background-color: #D4AF37 !important; 
        color: black !important; 
        font-weight: bold; 
        border-radius: 12px; 
        height: 3.8em; 
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
        padding: 12px; 
        border-radius: 10px; 
        border-right: 5px solid #ff4b4b; 
        background-color: rgba(255, 75, 75, 0.1); 
        color: #ff9999; 
        text-align: right; 
        margin-bottom: 8px;
        font-size: 0.9em;
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

# --- محرك التحليل الاستباقي العالي الدقة (Enhanced Heuristic Engine) ---
def advanced_heuristic_analysis(url):
    alerts = []
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    # 1. كشف التمويه بالعلامات التجارية (Brand Impersonation)
    brands = ['facebook', 'google', 'microsoft', 'instagram', 'apple', 'paypal', 'netflix', 'amazon', 'binance']
    for brand in brands:
        if brand in domain and domain != f"{brand}.com":
            alerts.append(f"⚠️ محاولة انتحال: الرابط يحاول تقليد نطاق {brand} الرسمي.")

    # 2. كشف كثرة النطاقات الفرعية (Subdomain Tunneling)
    if domain.count('.') > 3:
        alerts.append("❗ بنية مريبة: الرابط يحتوي على نطاقات فرعية متعددة، أسلوب شائع لإخفاء الوجهة الحقيقية.")

    # 3. كشف الكلمات المفتاحية الخطيرة (Deep Keyword Scan)
    danger_pattern = r"(login|signin|verify|account|secure|update|billing|token|auth|wallet)"
    if re.search(danger_pattern, url.lower()):
        alerts.append("⚠️ صيد بيانات: الرابط يحتوي على كلمات مفتاحية تُستخدم في هجمات التصيد.")

    # 4. كشف الاستضافات المجانية المريبة
    suspicious_hosts = ['canva.site', 'wixsite.com', 'web.app', 'firebaseapp.com', 'github.io', 'pages.dev', '000webhostapp.com']
    if any(host in domain for host in suspicious_hosts):
        alerts.append(f"⚠️ استضافة مجانية: الموقع مستضاف على ({domain})، وهي بيئة خصبة للروابط المؤقتة الخبيثة.")

    # 5. أمن البروتوكول
    if not url.startswith("https://"):
        alerts.append("🚫 غير مشفر: الرابط يستخدم HTTP، بياناتك معرضة للاعتراض.")

    return alerts

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام التتبع الجنائي والتحليل الاستباقي</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="أدخل الرابط المراد تحليله جنائياً...")

if st.button("تشغيل الفحص الرقمي"):
    if not target_url:
        st.warning("⚠️ يرجى تزويد الرابط للفحص")
    else:
        heuristic_results = advanced_heuristic_analysis(target_url)
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري تنفيذ بروتوكولات الفحص..."):
            try:
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                
                if response.status_code == 404:
                    requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": target_url})
                    time.sleep(6) # انتظار قصير للتحليل الأولي
                    response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)

                st.markdown("---")

                # عرض التحليل الاستباقي لـ "مرجان"
                if heuristic_results:
                    st.subheader("🕵️ نتائج تحليل محرك مرجان:")
                    for alert in heuristic_results:
                        st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
                
                # عرض نتائج المختبرات العالمية ورابط السلوك
                if response.status_code == 200:
                    data = response.json()['data']['attributes']
                    stats = data.get('last_analysis_stats', {})
                    malicious = stats.get('malicious', 0)
                    suspicious = stats.get('suspicious', 0)
                    
                    if malicious > 0 or suspicious > 0:
                        st.error(f"🚨 تنبيه أمني: تم تصنيف الرابط كخطر من قبل {malicious + suspicious} مختبر عالمي.")
                    elif heuristic_results:
                        st.warning("🟡 تحذير: المختبرات العالمية تعتبره سليماً، لكن محرك مرجان يرصد سلوكاً مريباً جداً!")
                    else:
                        st.success("✅ الرابط سليم بناءً على البيانات المتوفرة.")
                    
                    # إعادة إضافة رابط مراجعة السلوك التقني العميق
                    st.info(f"🔗 [لمراجعة السلوك التقني العميق اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")
                else:
                    st.error("⚠️ فشل الاتصال بقواعد البيانات العالمية.")

            except Exception as e:
                st.error("خطأ فني في محرك التحليل.")

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace System v2.5</div>', unsafe_allow_html=True)
