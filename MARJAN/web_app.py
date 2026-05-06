import streamlit as st
import math
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace v9.5", layout="wide")

# --- محرك التحليل ---
def analyze_url(url):
    # محاكاة لنتائج التحليل بناءً على معطياتك السابقة
    domain = urlparse(url).netloc.lower()
    entropy = round(-sum((f := url.count(c)/len(url)) * math.log2(f) for c in set(url)), 2) if url else 0
    status = "CRITICAL / خطر" if entropy > 3.0 else "CLEAN / آمن"
    color = "#ff4b4b" if "خطر" in status else "#2ea043"
    return status, color, 2, entropy

# --- التنسيق البصري المحدث ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600&family=Orbitron:wght@700&display=swap');
    .stApp { background-color: #05070a !important; }
    
    /* مستطيل المعلومات الأفقي المنظم */
    .metric-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        background: rgba(13, 17, 23, 0.9);
        border: 1px solid rgba(212, 175, 85, 0.3);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    .metric-item {
        text-align: center;
        font-family: 'Cairo', sans-serif;
        flex: 1;
        border-left: 1px solid rgba(212, 175, 85, 0.1);
    }
    .metric-item:last-child { border-left: none; }
    
    .metric-label { color: #D4AF37; font-size: 0.9rem; margin-bottom: 5px; opacity: 0.8; }
    .metric-value { color: white; font-size: 1.6rem; font-family: 'Orbitron', sans-serif; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- واجهة البرنامج ---
st.markdown("<h1 style='text-align:center; color:#D4AF37; font-family:Orbitron;'>MARJAN TRACE</h1>", unsafe_allow_html=True)

url_input = st.text_input("أدخل الرابط المراد فحصه:", placeholder="https://...")

if st.button("بدء بروتوكول التحليل"):
    if url_input:
        status, color, evidence_count, entropy_val = analyze_url(url_input)
        
        # عرض البيانات في مستطيل أفقي منظم كما طلبت
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-item">
                <div class="metric-label">معامل العشوائية</div>
                <div class="metric-value">{entropy_val}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">الأدلة المرصودة</div>
                <div class="metric-value">{evidence_count}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">الحالة الجنائية</div>
                <div class="metric-value" style="color:{color};">{status}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # باقي أقسام التقرير والـ Sandbox تستمر هنا...
        st.info("تم تحديث هيكل البيانات بنجاح.")
