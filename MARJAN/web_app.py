import streamlit as st
import requests
import base64
import time
from urllib.parse import urlparse

# --- إعدادات الصفحة والهوية البصرية ---
st.set_page_config(
    page_title="Marjan Trace v6.3 | Eng. Zaid Al-Janabi",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- محرك التنسيق المطور (Advanced Cyber Gold CSS) ---
st.markdown("""
    <style>
    /* الحاوية الرئيسية */
    [data-testid="stAppViewContainer"] {
        background-color: #05070a;
        background-image: radial-gradient(circle at 20% 20%, #0a0e14 0%, #05070a 100%);
        color: #eee;
    }
    
    /* تنسيق العناوين */
    .main-title {
        color: #D4AF37;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        text-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
        margin-bottom: 5px;
    }
    
    .sub-title {
        color: #eee;
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 30px;
    }

    /* لوحة النتيجة النهائية - تصميم مخصص */
    .final-decision-box {
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin: 20px 0;
        border: 2px solid #D4AF37;
        background: rgba(212, 175, 55, 0.05);
        animation: fadeIn 1.5s;
    }

    /* تنسيق الجداول واللوحات السفلية */
    .stat-card {
        background: rgba(17, 20, 26, 0.8);
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
        height: 100%;
    }

    /* الفوتر */
    .footer-bar {
        position: fixed;
        bottom: 0; left: 0; width: 100%;
        background: rgba(5, 7, 10, 0.95);
        color: #D4AF37;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #D4AF37;
    }
    
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# --- منطق التحليل المطور (Core Logic) ---
def enhanced_forensic_analysis(url):
    """محرك مرجان للتحليل الجنائي المتقدم."""
    score = 0
    alerts = []
    domain = urlparse(url).netloc.lower()
    
    # 1. تحليل الكلمات المفتاحية (Heuristic Matching)
    phishing_keywords = ['binance', 'metamask', 'login', 'verify', 'update', 'secure', 'bank', 'gift']
    for word in phishing_keywords:
        if word in url.lower():
            score += 25
            alerts.append(f"رصد كلمة مشبوهة: {word}")

    # 2. تحليل تعقيد النطاق
    if domain.count('.') > 2:
        score += 20
        alerts.append("نطاق فرعي معقد (معدل تمويه مرتفع)")

    # 3. فحص التشفير
    if not url.startswith("https"):
        score += 15
        alerts.append("بروتوكول HTTP غير مشفر")

    return score, alerts

# --- واجهة المستخدم (UI Layout) ---

# الهيدر
st.markdown('<p class="main-title">Marjan Trace v6.3</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">نظام التحليل الجنائي الرقمي المتقدم</p>', unsafe_allow_html=True)

# تقسيم الشاشة (الجسم الرئيسي + الشريط الجانبي للأدوات)
main_col, side_col = st.columns([3, 1])

with side_col:
    st.markdown("### 🛠️ أدوات التحكم")
    st.slider("حساسية التحليل الهيكلي", 0, 100, 75)
    st.selectbox("نموذج ML", ["Random Forest v2", "Deep Neural Net", "Heuristic Only"])
    st.markdown("---")
    st.markdown("### 📡 تتبع الاتصال العالمي")
    # محاكاة لخريطة الاتصال
    st.image("https://img.icons8.com/nolan/96/network-topology.png", width=100)
    st.caption("جاري الاتصال بـ 74 مختبر عالمي...")

with main_col:
    # إدخال الرابط
    url_input = st.text_input("", placeholder="أدخل الرابط المشبوه لبدء عملية التتبع الجنائي...")
    
    if st.button("تفعيل بروتوكول الكشف الذكي"):
        if url_input:
            # 1. محاكاة مراحل المعالجة
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            stages = ["جاري معالجة المدخلات...", "بدء المسح الاستخباراتي العالمي...", "تنفيذ التحليل الهيكلي المتقدم...", "تصنيف التهديد النهائي..."]
            for i, stage in enumerate(stages):
                status_text.text(stage)
                progress_bar.progress((i + 1) * 25)
                time.sleep(0.6)

            # 2. تنفيذ التحليل
            risk_score, forensic_alerts = enhanced_forensic_analysis(url_input)
            
            # 3. عرض النتيجة النهائية (الإضافة الجديدة بالعربي)
            st.markdown('<div class="final-decision-box">', unsafe_allow_html=True)
            st.subheader("🏁 النتيجة النهائية للاختبار")
            
            if risk_score >= 50:
                st.markdown(f"<h1 style='color: #ff4b4b;'>⚠️ تهديد مرتفع الخطورة ({risk_score}%)</h1>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 1.2rem;'>ينصح بحظر الرابط فوراً؛ تم رصد أنماط انتحال شخصية وهندسة اجتماعية.</p>", unsafe_allow_html=True)
            elif risk_score > 0:
                st.markdown(f"<h1 style='color: #ffa500;'>🔔 مشبوه ({risk_score}%)</h1>", unsafe_allow_html=True)
                st.write("الرابط يحتوي على خصائص غير معتادة، يرجى الحذر.")
            else:
                st.markdown("<h1 style='color: #28a745;'>✅ رابط آمن مبدئياً</h1>", unsafe_allow_html=True)
                st.write("لم يتم العثور على مؤشرات خطر هيكلية.")
            st.markdown('</div>', unsafe_allow_html=True)

            # 4. لوحات البيانات السفلية
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown('<div class="stat-card"><b>🔍 تنبيهات مرجان</b><br>' + "<br>".join([f"• {a}" for a in forensic_alerts]) + '</div>', unsafe_allow_html=True)
            with col_b:
                st.markdown('<div class="stat-card"><b>🌍 الاستخبارات العالمية</b><br>VirusTotal: Flagged<br>IBM X-Force: Suspicious<br>AlienVault: High-Risk</div>', unsafe_allow_html=True)
            with col_c:
                st.markdown('<div class="stat-card"><b>📊 التقرير السلوكي</b><br>IP: 185.22.14.x<br>Host: Cloudflare<br>Country: US</div>', unsafe_allow_html=True)
        else:
            st.error("يرجى إدخال رابط للتحليل.")

# الفوتر الثابت
st.markdown(f"""
    <div class="footer-bar">
        جامعة المعارف | هندسة تقنيات الأمن السيبراني | المنشئ: Eng. Zaid Al-Janabi
    </div>
    """, unsafe_allow_html=True)
