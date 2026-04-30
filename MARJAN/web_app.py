import streamlit as st
import requests
import base64

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="Marjan Trace",
    page_icon="🛡️",
    layout="centered"
)

# --- تنسيق التصميم (الذهبي والأسود) ---
st.markdown("""
    <style>
    .main { background-color: #05070a; }
    .stApp { background-color: #05070a; }
    h1 { color: #D4AF37 !important; text-align: center; font-family: 'Arial', sans-serif; text-shadow: 2px 2px #000; }
    h3 { color: #D4AF37 !important; text-align: center; font-family: 'Arial'; }
    .stButton>button {
        width: 100%;
        background-color: #D4AF37 !important;
        color: black !important;
        font-weight: bold;
        border-radius: 15px;
        height: 3.5em;
        border: 2px solid #D4AF37;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        color: #D4AF37;
        padding: 10px;
        background-color: #0a0c10;
        font-weight: bold;
    }
    .result-box {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #D4AF37;
        background-color: #000000;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3>التحليل الجنائي للروابط المشبوهة</h3>", unsafe_allow_html=True)
st.write("\n")

target_url = st.text_input("", placeholder="...أدخل الرابط المستهدف للتحليل المعمق")

if st.button("تشغيل الفحص الرقمي"):
    if not target_url:
        st.warning("⚠️ يرجى إدخال رابط للفحص")
    else:
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        
        with st.spinner("> جاري تحليل البصمات الرقمية وتشريح الرابط..."):
            try:
                url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                
                st.markdown("---")
                
                if response.status_code == 200:
                    data = response.json()['data']['attributes']
                    stats = data.get('last_analysis_stats', {})
                    malicious = stats.get('malicious', 0)
                    suspicious = stats.get('suspicious', 0)
                    
                    if malicious > 0 or suspicious > 0:
                        st.error(f"🚨 تم رصد تهديد أمني!")
                        st.markdown(f"""<div class="result-box" style="color: #f85149; border-color: #f85149;">
                            الحالة: خبيث أو مشبوه<br>
                            عدد المحركات المحذرة: {malicious + suspicious}
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.success("🟢 الرابط سليم وجاهز للاستخدام")
                        st.markdown(f"""<div class="result-box" style="color: #00FF41;">
                            الحالة: نظيف (Clean)<br>
                            لم يتم العثور على أنشطة تخريبية في السجلات الحالية.
                        </div>""", unsafe_allow_html=True)
                    
                    st.info(f"🔗 [لمراجعة السلوك التقني العميق اضغط هنا](https://www.virustotal.com/gui/url/{url_id}/behavior)")

                elif response.status_code == 404:
                    st.info("🔎 الرابط جديد.. جاري إرساله للفحص لأول مرة. أعد المحاولة بعد دقيقة.")
                    requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": target_url})
                else:
                    st.error("⚠️ الخادم مشغول حالياً، يرجى المحاولة بعد قليل.")

            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")

# --- التذييل (هويتك الأصلية) ---
st.markdown(f"""
    <div class="footer">
        Eng. Zaid Al-Janabi | Marjan Trace System
    </div>
    """, unsafe_allow_html=True)
