import streamlit as st
import requests
import base64
import time

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="Marjan Trace",
    page_icon="🛡️",
    layout="centered"
)

# --- تنسيق التصميم ---
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

target_url = st.text_input("", placeholder="...أدخل الرابط المستهدف للتحليل")

if st.button("تشغيل الفحص الرقمي"):
    if not target_url:
        st.warning("⚠️ يرجى إدخال رابط للفحص")
    else:
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        
        with st.spinner("> جاري جلب البصمات الرقمية وتحليل السلوك السحابي..."):
            try:
                url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
                
                # المحاولة الأولى لجلب النتيجة
                response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers)
                
                # ميزة "الانتظار التلقائي" إذا كان الرابط جديداً
                if response.status_code == 404 or "last_analysis_stats" not in response.json().get('data', {}).get('attributes', {}):
                    st.info("🔎 الرابط جديد على قاعدة البيانات. جاري إرساله للمختبر.. فضلاً انتظر ثوانٍ للتحليل التلقائي.")
                    # إرسال الرابط للفحص
                    requests.post("https://www.virustotal.com/api/v3/urls", headers=headers, data={"url": target_url})
                    
                    # الانتظار لمدة 20 ثانية لضمان اكتمال التحليل في السيرفر
                    time.sleep(20) 
                    
                    # إعادة جلب النتيجة بعد الانتظار
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
                    st.error("⚠️ تعذر جلب النتيجة حالياً. قد يكون الرابط غير صالح أو الخادم مشغول.")

            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالخادم: {str(e)}")

# التذييل
st.markdown(f"""
    <div class="footer">
        Eng. Zaid Al-Janabi | Morjan System
    </div>
    """, unsafe_allow_html=True)
