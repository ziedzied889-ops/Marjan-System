import streamlit as st
import requests
import base64

# --- إعدادات الصفحة (تظهر في المتصفح) ---
st.set_page_config(
    page_title="Marjan Trace",
    page_icon="🛡️",
    layout="centered"
)

# --- تنسيق التصميم (الألوان: ذهبي وأسود سايبير) ---
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
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #B8860B !important;
        border-color: #00d2ff;
    }
    .stTextInput>div>div>input {
        background-color: #010409 !important;
        color: white !important;
        border: 1px solid #D4AF37 !important;
        text-align: right;
        border-radius: 10px;
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
        color: #00FF41;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3>التحليل الجنائي للروابط المشبوهة</h3>", unsafe_allow_html=True)
st.write("\n")

# مدخل الرابط
target_url = st.text_input("", placeholder="...أدخل الرابط المستهدف للتحليل")

# زر الفحص
if st.button("تشغيل الفحص الرقمي"):
    if not target_url:
        st.warning("⚠️ يرجى إدخال رابط للفحص")
    else:
        # مفتاح الأمان الخاص بك
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        
        with st.spinner("> جاري تحليل البصمات الرقمية للرابط..."):
            try:
                # معالجة الرابط
                url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
                headers = {"x-apikey": API_KEY}
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                
                st.markdown("---")
                
                if response.status_code == 200:
                    stats = response.json()['data']['attributes']['last_analysis_stats']
                    malicious = stats['malicious']
                    
                    if malicious > 0:
                        st.error(f"🔴 تم رصد تهديد أمني!")
                        st.markdown(f"""<div class="result-box" style="color: #f85149; border-color: #f85149;">
                            الحالة: خبيث (Malicious)<br>
                            عدد المحركات التي حذرت من الرابط: {malicious}
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.success("🟢 الرابط سليم وجاهز للاستخدام")
                        st.markdown(f"""<div class="result-box">
                            الحالة: نظيف (Clean)<br>
                            لم يتم العثور على أنشطة تخريبية أو برمجيات خبيثة.
                        </div>""", unsafe_allow_html=True)
                else:
                    st.info("الرابط جديد على قاعدة البيانات، تم إرساله للفحص العميق. يرجى المحاولة بعد دقيقة.")
                    requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": target_url})

            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالخادم: {str(e)}")

# التذييل باسمك
st.markdown(f"""
    <div class="footer">
        Eng. Zaid Al-Janabi | Morjan System 
    </div>
    """, unsafe_allow_html=True)
