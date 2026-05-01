import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري القوي (الخلفية الرقمية المفروضة) ---
st.markdown("""
    <style>
    /* فرض الخلفية الرقمية على كل طبقات التطبيق */
    [data-testid="stAppViewContainer"] {
        background-color: #05070a !important;
        background-image: 
            linear-gradient(rgba(212, 175, 55, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(212, 175, 55, 0.03) 1px, transparent 1px),
            radial-gradient(circle at center, #11141a 0%, #05070a 100%) !important;
        background-size: 30px 30px, 30px 30px, 100% 100% !important;
        background-attachment: fixed !important;
    }

    /* إزالة أي خلفيات بيضاء أو رمادية من الحاويات */
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background: transparent !important;
    }

    .main { 
        background: transparent !important; 
    }

    /* العناوين والتوهج الذهبي */
    h1 { 
        color: #D4AF37 !important; 
        text-align: center; 
        text-shadow: 0px 0px 15px rgba(212, 175, 55, 0.6) !important; 
        font-family: 'Courier New', Courier, monospace; 
        margin-top: -50px;
    }
    h3 { 
        color: #D4AF37 !important; 
        text-align: center; 
        font-weight: normal; 
        opacity: 0.8;
    }
    
    /* تصميم الأزرار الاحترافي */
    .stButton>button { 
        width: 100%; 
        background-color: #D4AF37 !important; 
        color: black !important; 
        font-weight: bold; 
        border-radius: 10px; 
        height: 3.5em; 
        border: none; 
        transition: 0.4s;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.3);
    }
    
    .stButton>button:hover { 
        background-color: #f1c40f !important; 
        transform: translateY(-2px); 
        box-shadow: 0px 8px 25px rgba(212, 175, 55, 0.5);
    }

    /* التذييل أسفل الصفحة */
    .footer { 
        position: fixed; 
        left: 0; 
        bottom: 0; 
        width: 100%; 
        text-align: center; 
        color: #D4AF37; 
        padding: 10px; 
        background-color: rgba(5, 7, 10, 0.95); 
        font-weight: bold; 
        border-top: 1px solid #D4AF37; 
        z-index: 100;
    }

    /* صناديق النتائج بتأثير زجاجي */
    .result-box { 
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid rgba(212, 175, 55, 0.3); 
        background-color: rgba(0, 0, 0, 0.6); 
        text-align: right; 
        margin-bottom: 10px; 
        backdrop-filter: blur(10px);
    }

    .heuristic-warning { 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #ff4b4b; 
        background-color: rgba(43, 11, 11, 0.7); 
        color: #ff9999; 
        text-align: right; 
        margin-bottom: 15px; 
        font-size: 0.9em; 
    }
    
    /* حقل إدخال الرابط */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(212, 175, 55, 0.5) !important;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- وظيفة التحليل الاستباقي (Heuristic Engine) ---
def advanced_heuristic_analysis(url):
    alerts = []
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    if "xn--" in domain:
        alerts.append("❗ تم رصد تشفير Punycode: محاولة لإخفاء الهوية الحقيقية للنطاق عبر محارف دولية.")
    
    phishing_triggers = ['login', 'verify', 'account', 'secure', 'update', 'banking', 'support', 'office365']
    if any(trigger in url.lower() for trigger in phishing_triggers):
        alerts.append("❗ كلمات مريبة: الرابط يحتوي على مصطلحات تُستخدم عادةً لاستدراج الضحايا.")
    
    free_hosting = ['canva.site', 'wixsite.com', 'web.app', 'firebaseapp.com', 'github.io']
    if any(service in domain for service in free_hosting):
        alerts.append(f"⚠️ نطاق فرعي مريب: يتم استضافة الصفحة على خدمة مجانية ({domain})، غالباً ما تُستغل للتصيد.")

    if url.startswith("http://"):
        alerts.append("🚫 بروتوكول غير آمن: الرابط لا يستخدم التشفير (HTTP)، مما يسهل اعتراض البيانات.")
        
    if len(url) > 100:
        alerts.append("❗ تعمية الرابط: طول الرابط مبالغ فيه، وهي تقنية لإخفاء النطاق الحقيقي عن عين المستخدم.")

    return alerts

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3>التحليل الجنائي والذكاء الاستباقي للروابط</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="...أدخل الرابط للفحص الفوري")

if st.button("تشغيل الفحص الرقمي"):
    if not target_url:
        st.warning("⚠️ يرجى إدخال رابط للفحص")
    else:
        heuristic_results = advanced_heuristic_analysis(target_url)
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري الفحص المعمق ودمج النتائج الذكية..."):
            try:
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                
                if response.status_code == 404:
                    requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": target_url})
                    time.sleep(10) 
                    response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)

                st.markdown("---")

                if heuristic_results:
                    st.subheader("🕵️ نتائج التحليل الاستباقي (مرجان الذكي):")
                    for alert in heuristic_results:
                        st.markdown(f'<div class="heuristic-warning">{alert}</div>', unsafe_allow_html=True)
                
                if response.status_code == 200:
                    data = response.json()['data']['attributes']
                    if 'last_analysis_stats' in data:
                        stats = data['last_analysis_stats']
                        malicious = stats.get('malicious', 0)
                        suspicious = stats.get('suspicious', 0)
                        
                        if malicious > 0 or suspicious > 0:
                            st.error(f"🚨 تأكيد التهديد أمنياً!")
                            st.markdown(f'<div class="result-box" style="color:#f85149; border-color:#f85149;">الحالة: خبيث (بناءً على {malicious + suspicious} مختبر عالمي)</div>', unsafe_allow_html=True)
                        elif heuristic_results:
                            st.warning("🟡 تنبيه: المختبرات العالمية لم تبلغ عنه بعد، ولكن خصائص الرابط مريبة جداً!")
                        else:
                            st.success("🟢 الرابط سليم")
                            st.markdown(f'<div class="result-box" style="color:#00FF41;">الحالة: نظيف (Clean) وفقاً للمعايير الحالية</div>', unsafe_allow_html=True)
                        
                        st.info(f"🔗 [لمراجعة السلوك التقني العميق اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")
                else:
                    st.error("⚠️ عذراً، الخادم مشغول أو تجاوزت حد الطلبات.")

            except Exception as e:
                st.error(f"حدث خطأ تقني: {str(e)}")

# --- التذييل ---
st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace System</div>', unsafe_allow_html=True)
