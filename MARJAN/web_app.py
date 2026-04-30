import streamlit as st
import requests
import base64
import time

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- التنسيق البصري ---
st.markdown("""
    <style>
    .main { background-color: #05070a; }
    .stApp { background-color: #05070a; }
    h1 { color: #D4AF37 !important; text-align: center; text-shadow: 2px 2px #000; }
    h3 { color: #D4AF37 !important; text-align: center; }
    .stButton>button { width: 100%; background-color: #D4AF37 !important; color: black !important; font-weight: bold; border-radius: 15px; height: 3.5em; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #D4AF37; padding: 10px; background-color: #0a0c10; font-weight: bold; }
    .result-box { padding: 20px; border-radius: 15px; border: 1px solid #D4AF37; background-color: #000000; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3>التحليل الجنائي للروابط المشبوهة</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="...أدخل الرابط للفحص الفوري")

if st.button("تشغيل الفحص الرقمي"):
    if not target_url:
        st.warning("⚠️ يرجى إدخال رابط للفحص")
    else:
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري الفحص المعمق.. يرجى الانتظار ثوانٍ..."):
            try:
                # محاولة جلب النتيجة مباشرة
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                
                # إذا كان الرابط جديداً تماماً (404)
                if response.status_code == 404:
                    # نرسله للفحص
                    requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": target_url})
                    # ننتظر قليلاً ونحاول مرة أخرى تلقائياً (حتى لا يحتاج المستخدم للضغط مرة ثانية)
                    time.sleep(10) 
                    response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)

                st.markdown("---")
                
                if response.status_code == 200:
                    data = response.json()['data']['attributes']
                    # التأكد من وجود إحصائيات التحليل
                    if 'last_analysis_stats' in data:
                        stats = data['last_analysis_stats']
                        malicious = stats.get('malicious', 0)
                        suspicious = stats.get('suspicious', 0)
                        
                        if malicious > 0 or suspicious > 0:
                            st.error(f"🚨 تم رصد تهديد أمني!")
                            st.markdown(f'<div class="result-box" style="color:#f85149;">الحالة: خبيث أو مشبوه<br>عدد التهديدات: {malicious + suspicious}</div>', unsafe_allow_html=True)
                        else:
                            st.success("🟢 الرابط سليم")
                            st.markdown(f'<div class="result-box" style="color:#00FF41;">الحالة: نظيف (Clean)</div>', unsafe_allow_html=True)
                        
                        st.info(f"🔗 [لمراجعة السلوك التقني العميق اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")
                    else:
                        st.info("🔎 الرابط قيد التحليل الآن.. انتظر ثوانٍ وأعد الضغط لرؤية النتيجة النهائية.")
                else:
                    st.error("⚠️ عذراً، الخادم مشغول حالياً (4 طلبات بالدقيقة).")

            except Exception as e:
                st.error(f"حدث خطأ تقني: {str(e)}")

# --- التذييل ---
st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace System </div>', unsafe_allow_html=True)
