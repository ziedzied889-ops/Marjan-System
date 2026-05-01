import streamlit as st
import requests
import base64
import time
import re
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري المتطور مع درع الأمن السيبراني ---
st.markdown("""
    <style>
    /* إعداد الخلفية الأساسية مع الشبكة والدرع */
    [data-testid="stAppViewContainer"] {
        background-color: #05070a !important;
        background-image: 
            /* طبقة الدرع الأمني في المنتصف */
            url("https://www.transparentpng.com/download/security/shield-security-icon-9.png"),
            /* طبقة الشبكة الرقمية */
            linear-gradient(rgba(212, 175, 55, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(212, 175, 55, 0.03) 1px, transparent 1px),
            /* التدرج اللوني العميق */
            radial-gradient(circle at center, #11141a 0%, #05070a 100%) !important;
        
        /* إعدادات التموضع: الدرع في المنتصف، الشبكة متكررة */
        background-position: center 40%, center, center, center !important;
        background-repeat: no-repeat, repeat, repeat, no-repeat !important;
        background-size: 400px auto, 30px 30px, 30px 30px, 100% 100% !important;
        background-attachment: fixed !important;
    }

    /* جعل الدرع يبدو كعلامة مائية (شفافية خفيفة) */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(5, 7, 10, 0.4); /* تعتيم إضافي ليظهر الدرع بشكل خافت */
        z-index: -1;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background: transparent !important;
    }

    .main { 
        background: transparent !important; 
    }

    /* العناوين مع توهج ذهبي */
    h1 { 
        color: #D4AF37 !important; 
        text-align: center; 
        text-shadow: 0px 0px 20px rgba(212, 175, 55, 0.8) !important; 
        font-family: 'Courier New', Courier, monospace; 
        margin-top: -30px;
        font-weight: bold;
    }
    h3 { 
        color: #D4AF37 !important; 
        text-align: center; 
        font-weight: normal;
        background: rgba(0,0,0,0.4);
        display: inline-block;
        padding: 5px 20px;
        border-radius: 50px;
        width: 100%;
    }
    
    /* تصميم الأزرار */
    .stButton>button { 
        width: 100%; 
        background-color: #D4AF37 !important; 
        color: black !important; 
        font-weight: bold; 
        border-radius: 12px; 
        height: 3.8em; 
        border: 1px solid #D4AF37; 
        transition: 0.5s;
        box-shadow: 0px 0px 20px rgba(212, 175, 55, 0.3);
        text-transform: uppercase;
    }
    
    .stButton>button:hover { 
        background-color: #f39c12 !important; 
        transform: scale(1.01); 
        box-shadow: 0px 0px 40px rgba(212, 175, 55, 0.6);
    }

    /* التذييل */
    .footer { 
        position: fixed; 
        left: 0; bottom: 0; width: 100%; 
        text-align: center; 
        color: #D4AF37; 
        padding: 12px; 
        background-color: rgba(5, 7, 10, 0.98); 
        font-weight: bold; 
        border-top: 1px solid #D4AF37; 
        z-index: 100;
        letter-spacing: 1px;
    }

    /* صناديق النتائج الزجاجية المعتمة */
    .result-box { 
        padding: 25px; 
        border-radius: 20px; 
        border: 1px solid rgba(212, 175, 55, 0.4); 
        background-color: rgba(0, 0, 0, 0.75); 
        text-align: right; 
        margin-top: 20px;
        backdrop-filter: blur(15px);
        box-shadow: 0px 10px 30px rgba(0,0,0,0.8);
    }

    /* حقل الإدخال */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.07) !important;
        color: #D4AF37 !important;
        border: 1px solid rgba(212, 175, 55, 0.6) !important;
        text-align: center;
        border-radius: 10px !important;
        font-size: 1.2rem !important;
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
