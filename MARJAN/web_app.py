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
    .main { background-color: #05070a; }
    .stApp { background-color: #05070a; }
    h1 { color: #D4AF37 !important; text-align: center; text-shadow: 2px 2px #000; }
    h3 { color: #D4AF37 !important; text-align: center; }
    .stButton>button { width: 100%; background-color: #D4AF37 !important; color: black !important; font-weight: bold; border-radius: 15px; height: 3.5em; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #B8962E !important; transform: scale(1.02); }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #D4AF37; padding: 10px; background-color: #0a0c10; font-weight: bold; border-top: 1px solid #D4AF37; }
    .result-box { padding: 20px; border-radius: 15px; border: 1px solid #D4AF37; background-color: #000000; text-align: right; margin-bottom: 10px; }
    .heuristic-warning { padding: 15px; border-radius: 10px; border: 1px solid #ff4b4b; background-color: #2b0b0b; color: #ff9999; text-align: right; margin-bottom: 15px; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# --- وظيفة التحليل الاستباقي (Heuristic Engine) ---
def advanced_heuristic_analysis(url):
    alerts = []
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    # 1. كشف تمويه Punycode
    if "xn--" in domain:
        alerts.append("❗ تم رصد تشفير Punycode: محاولة لإخفاء الهوية الحقيقية للنطاق عبر محارف دولية.")
    
    # 2. كشف الكلمات المفتاحية لهجمات التصيد
    phishing_triggers = ['login', 'verify', 'account', 'secure', 'update', 'banking', 'support', 'office365']
    if any(trigger in url.lower() for trigger in phishing_triggers):
        alerts.append("❗ كلمات مريبة: الرابط يحتوي على مصطلحات تُستخدم عادةً لاستدراج الضحايا.")
    
    # 3. كشف استغلال الخدمات المجانية (مثل Canva التي خدعتنا سابقاً)
    free_hosting = ['canva.site', 'wixsite.com', 'web.app', 'firebaseapp.com', 'github.io']
    if any(service in domain for service in free_hosting):
        alerts.append(f"⚠️ نطاق فرعي مريب: يتم استضافة الصفحة على خدمة مجانية ({domain})، غالباً ما تُستغل للتصيد.")

    # 4. فحص أمن البروتوكول
    if url.startswith("http://"):
        alerts.append("🚫 بروتوكول غير آمن: الرابط لا يستخدم التشفير (HTTP)، مما يسهل اعتراض البيانات.")
        
    # 5. كشف الطول المفرط (Obfuscation)
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
        # البدء بالتحليل الذاتي أولاً
        heuristic_results = advanced_heuristic_analysis(target_url)
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري الفحص المعمق ودمج النتائج الذكية..."):
            try:
                # طلب البيانات من VirusTotal
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                
                if response.status_code == 404:
                    requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": target_url})
                    time.sleep(10) 
                    response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)

                st.markdown("---")

                # عرض نتائج التحليل الذاتي (Heuristic)
                if heuristic_results:
                    st.subheader("🕵️ نتائج التحليل الاستباقي (مرجان الذكي):")
                    for alert in heuristic_results:
                        st.markdown(f'<div class="heuristic-warning">{alert}</div>', unsafe_allow_html=True)
                
                # عرض نتائج قواعد البيانات العالمية
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
st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace System | University of Al-Maarif</div>', unsafe_allow_html=True)
