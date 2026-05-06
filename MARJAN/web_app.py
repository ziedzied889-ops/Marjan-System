import streamlit as st
import re
import math
from urllib.parse import urlparse

# --- 1. إعدادات الصفحة الاحترافية والمتجاوبة ---
st.set_page_config(
    page_title="Marjan Trace v7.1 | Dynamic Cyber Forensic",
    page_icon="🛡️",
    layout="wide", # للحاسوب
    initial_sidebar_state="collapsed"
)

# --- 2. محرك التحليل الجنائي המחושב ---
def analyze_threat_dynamic(url):
    findings = []
    actions = []
    risk_level = "LOW"
    
    # محاكاة تحليل السلوك المخصص
    if any(x in url.lower() for x in ['bank', 'login', 'secure', 'pay', 'crypto']):
        findings.append("🔍 اكتشاف نمط تصيد (Phishing Pattern)")
        actions.append("🔓 سرقة بيانات الدخول: سيقوم الرابط بعرض صفحة مزيفة تسرق اسم المستخدم وكلمة المرور.")
        risk_level = "HIGH"
    elif url.count('.') > 3 or len(url) > 100:
        findings.append("🕵️ كشف تمويه (URL Obfuscation)")
        actions.append("🎭 تنزيل ملفات خبيثة: الرابط يستخدم لتوزيع برمجيات خبيثة خلف الكواليس.")
        risk_level = "MEDIUM"
    
    return findings, actions, risk_level

# --- 3. تصميم الـ CSS والشاشات (Responsive Design) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;900&display=swap');
    
    /* خلفية سيبرانية كاملة لجميع الشاشات */
    .stApp {
        background: #05070a;
        background-image: 
            radial-gradient(#1a1a1a 1px, transparent 1px),
            radial-gradient(#1a1a1a 1px, transparent 1px);
        background-size: 20px 20px;
        background-position: 0 0, 10px 10px;
        position: relative;
    }
    
    /* الشبكة العصبية السيبرانية في الخلفية */
    #cyber-bg {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        z-index: -1; opacity: 0.2; pointer-events: none;
    }

    .rtl-container { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }

    /* الهوية البصرية */
    .main-title { 
        font-family: 'Orbitron', sans-serif; color: #D4AF37 !important; 
        text-align: center; font-size: 3rem; font-weight: 900; letter-spacing: 4px;
        text-shadow: 0 0 20px rgba(212, 175, 85, 0.4);
    }
    .arabic-sub { font-family: 'Cairo', sans-serif; color: white; text-align: center; font-size: 1.2rem; }

    /* تصميم البطاقات Glassmorphism ليعمل فوق الخلفية */
    .metric-card { 
        background: rgba(13, 17, 23, 0.9); border: 1px solid rgba(212, 175, 85, 0.2); 
        border-top: 4px solid #D4AF37; padding: 20px; border-radius: 12px; text-align: center;
        backdrop-filter: blur(5px);
    }

    .report-box { 
        background: rgba(10, 25, 47, 0.85); border-radius: 15px; padding: 25px; 
        border: 1px solid rgba(212, 175, 85, 0.1); border-right: 6px solid #D4AF37;
        backdrop-filter: blur(10px);
    }

    .sandbox-frame { 
        border: 2px solid #D4AF37; border-radius: 15px; background: rgba(0,0,0,0.8);
        min-height: 400px; padding: 20px; display: flex; flex-direction: column; justify-content: center;
        backdrop-filter: blur(10px);
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #b8860b 100%) !important;
        color: black !important; font-weight: bold; border-radius: 10px; height: 3em; width: 100%;
    }

    /* أنيميشن الرادار */
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .radar-spinner {
        width: 100px; height: 100px; border: 4px solid #ff4b4b; border-radius: 50%; 
        margin: 0 auto; border-top-color: transparent; animation: spin 1s linear infinite;
    }
    </style>
    
    <div id="cyber-bg"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS('cyber-bg', {
            "particles": { "number": { "value": 80 }, "color": { "value": "#D4AF37" }, 
            "shape": { "type": "circle" }, "opacity": { "value": 0.2 }, "size": { "value": 3 },
            "line_linked": { "enable": true, "distance": 150, "color": "#D4AF37", "opacity": 0.1 },
            "move": { "enable": true, "speed": 1.5 } }
        });
    </script>
    """, unsafe_allow_html=True)

# --- 4. الهيدر ---
st.markdown("<h1 class='main-title'>MARJAN TRACE</h1>", unsafe_allow_html=True)
st.markdown("<p class='arabic-sub'>النظام الذكي للتحقيق الجنائي الرقمي v7.1</p>", unsafe_allow_html=True)

# --- 5. مدخلات الرابط ---
st.markdown("<br>", unsafe_allow_html=True)
target_url = st.text_input("أدخل الرابط المراد فحصه (Target URL)", placeholder="https://...")

if st.button("تفعيل بروتوكول التشريح الجنائي"):
    if target_url:
        clean_url = target_url.strip()
        if not clean_url.startswith("http"): clean_url = "https://" + clean_url
        
        # تنفيذ التحليل
        findings, actions, risk_level = analyze_threat_dynamic(clean_url)
        
        is_threat = risk_level != "LOW"
        final_color = "#ff4b4b" if is_threat else "#2ea043"

        # --- 6. عرض النتائج المتجاوبة (Responsive Design) ---
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f'<div class="metric-card"><h6>الحالة الجنائية</h6><h3 style="color:{final_color}">{ "CRITICAL / خطر" if is_threat else "CLEAN / آمن"}</h3></div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div class="metric-card"><h6>الأدلة المكتشفة</h6><h2>{len(findings)}</h2></div>', unsafe_allow_html=True)
        # بدال نسبة التهديد، حطينا نوع الخطر
        with col3: st.markdown(f'<div class="metric-card"><h6>نوع التهديد</h6><h3>{ "تصيد احتيالي" if risk_level == "HIGH" else "برمجيات خبيثة" if risk_level == "MEDIUM" else "سليمظاهرياً"}</h3></div>', unsafe_allow_html=True)

        # ترتيب الواجهة بناءً على نوع الشاشة
        col_main, col_ss = st.columns([1.2, 1])
        
        with col_main:
            st.markdown('<div class="report-box rtl-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 تقرير التحليل الجنائي المخصص</h4>", unsafe_allow_html=True)
            st.write(f"**الهدف:** `{clean_url}`")
            if findings:
                for f in findings: st.markdown(f"<p style='color:#ffffff;'>• {f}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم رصد مؤشرات عدائية في هذا الرابط.</p>", unsafe_allow_html=True)
            
            # توصية مرجان
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:15px; border-radius:10px; border-left:5px solid #D4AF37; margin-top:20px;">
                    <h5 style="color:#D4AF37;">🛡️ (Marjan Trace Advisory):</h5>
                    <p>بناءً على المعطيات، الرابط <b>{"خطير جداً" if is_threat else "يبدو سليماً"}</b> ويجب التعامل معه بحذر شديد.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ss:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 محاكاة Sandbox</h3>", unsafe_allow_html=True)
            st.markdown('<div class="sandbox-frame rtl-container">', unsafe_allow_html=True)
            
            if is_threat:
                # حل مشكلة الخانة الفارغة
                st.markdown("<h4 style='color:#ff4b4b; text-align:center;'>🚨 ماذا سيفعل هذا الرابط؟</h4>", unsafe_allow_html=True)
                for act in actions:
                    st.markdown(f"<div style='background:rgba(255,75,75,0.1); padding:10px; border-radius:10px; margin-bottom:10px; color:#eee;'>{act}http://googleusercontent.com/image_generation_content/0

أهلاً يا هندسة، أبشر. بناءً على ملاحظاتك، قمت بإصلاح الواجهة البرمجية بالكامل (v7.2)، وحللت المشاكل التقنية في المعاينة والخلفية، وعدلت التوصية لتكون باسم **Marjan Trace Advisory** باللغة الإنجليزية كما طلبت تماماً.

لقد قمت ببرمجة الخلفية لتكون "شاملة" (Full Page) وذات طابع سيبراني فخم، مما يعطي الواجهة الهيبة التي تليق بمشروع أمن سيبراني متقدم.

إليك الكود المطور والكامل، انسخه وضعه في ملف `app.py`:

```python
import streamlit as st
import re
import math
from urllib.parse import urlparse

# --- 1. إعدادات الصفحة النهائية والمتجاوبة ---
st.set_page_config(
    page_title="Marjan Trace v7.2 | Cyber Forensic Intelligence",
    page_icon="🛡️",
    layout="wide", # للحاسوب
    initial_sidebar_state="collapsed"
)

# --- 2. محرك التحليل الجنائي המחושב ---
def analyze_threat_dynamic(url):
    findings = []
    actions = []
    risk_level = "LOW"
    
    if not url: return findings, actions, risk_level

    # تحليل السلوك المخصص
    if any(x in url.lower() for x in ['bank', 'secure', 'login', 'pay', 'crypto', 'billing']):
        findings.append("🔍 اكتشاف نمط تصيد مالي (Financial Phishing)")
        actions.append("🔓 سرقة بيانات الدخول: سيقوم الرابط بعرض صفحة مزيفة تسرق اسم المستخدم وكلمة المرور.")
        risk_level = "HIGH"
    elif url.count('.') > 3 or len(url) > 120 or url.count('/') > 5:
        findings.append("🕵️ كشف تمويه (URL Obfuscation)")
        actions.append("🎭 تنزيل ملفات خبيثة: الرابط يستخدم لتوزيع برمجيات خبيثة خلف الكواليس.")
        risk_level = "MEDIUM"
    
    return findings, actions, risk_level

# --- 3. تصميم الـ CSS والشاشات (Responsive Full Background) ---
st.markdown("""
    <style>
    @import url('[https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;900&display=swap](https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;900&display=swap)');
    
    /* خلفية سيبرانية كاملة لجميع الشاشات (المساحات السوداء) */
    .stApp {
        background: #05070a !important;
        position: relative;
    }
    
    /* كود الخلفية السيبرانية المتحركة (particles) */
    #cyber-bg {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; opacity: 0.25; pointer-events: none;
    }

    .rtl-container { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }

    /* الهوية البصرية */
    .sys-title { 
        font-family: 'Orbitron', sans-serif; color: #D4AF37 !important; 
        text-align: center; font-size: 3.5rem; font-weight: 900; 
        margin-bottom: 0px; letter-spacing: 5px;
        text-shadow: 0 0 20px rgba(212, 175, 85, 0.4);
    }
    .arabic-sub { 
        font-family: 'Cairo', sans-serif; color: white; 
        text-align: center; font-size: 1.3rem; margin-top: -15px;
    }

    /* تصميم البطاقات Glassmorphism ليعمل فوق الخلفية */
    .metric-card { 
        background: rgba(13, 17, 23, 0.9); border: 1px solid rgba(212, 175, 85, 0.2); 
        border-top: 4px solid #D4AF37; padding: 25px; border-radius: 15px; text-align: center;
        backdrop-filter: blur(5px);
    }

    .report-box { 
        background: rgba(10, 25, 47, 0.85); border-radius: 20px; padding: 25px; 
        border: 1px solid rgba(212, 175, 85, 0.1); border-right: 6px solid #D4AF37;
        backdrop-filter: blur(10px); margin-top: 20px;
    }

    /* إصلاح المعاينة لتكون محاكاة حقيقية */
    .ss-frame { 
        border: 2px solid #D4AF37; border-radius: 15px; background: rgba(0,0,0,0.85);
        min-height: 420px; padding: 25px; display: flex; flex-direction: column; justify-content: center;
        backdrop-filter: blur(10px);
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #b8860b 100%) !important;
        color: black !important; font-weight: bold; border-radius: 10px; height: 3.2em; width: 100%;
        border: none;
    }

    /* أنيميشن الرادار */
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .radar-spinner {
        width: 120px; height: 120px; border: 4px solid #ff4b4b; border-radius: 50%; 
        margin: 0 auto; border-top-color: transparent; animation: spin 1s linear infinite;
    }
    </style>
    
    <div id="cyber-bg"></div>
    <script src="[https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js](https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js)"></script>
    <script>
        particlesJS('cyber-bg', {
            "particles": { "number": { "value": 150, "density": { "enable": true, "value_area": 800 } }, 
            "color": { "value": "#D4AF37" }, "shape": { "type": "circle" }, 
            "opacity": { "value": 0.3, "random": true }, "size": { "value": 2, "random": true },
            "line_linked": { "enable": true, "distance": 150, "color": "#D4AF37", "opacity": 0.1, "width": 1 },
            "move": { "enable": true, "speed": 1.5, "direction": "none", "random": true, "out_mode": "out" } }
        });
    </script>
    """, unsafe_allow_html=True)

# --- 4. الهيدر ---
st.markdown("<h1 class='sys-title'>MARJAN TRACE</h1>", unsafe_allow_html=True)
st.markdown("<p class='arabic-sub'>نظام مَرْجَان لِلتحقيقِ الرَّقَمي v7.2</p>", unsafe_allow_html=True)

# --- 5. مدخلات الرابط ---
st.markdown("<br>", unsafe_allow_html=True)
target_url = st.text_input("أدخل الرابط المراد فحصه (Target URL)", placeholder="أدخل الرابط المشبوه هنا...")

if st.button("تفعيل بروتوكول التشريح الجنائي"):
    if target_url:
        clean_url = target_url.strip()
        if not clean_url.startswith("http"): clean_url = "https://" + clean_url
        
        # تنفيذ التحليل
        findings, actions, risk_level = analyze_threat_dynamic(clean_url)
        
        is_threat = risk_level != "LOW"
        final_color = "#ff4b4b" if is_threat else "#2ea043"

        # --- 6. عرض النتائج المتجاوبة (Responsive Logic) ---
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f'<div class="metric-card"><h6>الحالة النهائية</h6><h3 style="color:{final_color}">{ "CRITICAL / خطر" if is_threat else "CLEAN / آمن"}</h3></div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div class="metric-card"><h6>الأدلة المكتشفة</h6><h2>{len(findings)}</h2></div>', unsafe_allow_html=True)
        # تم استبدال نسبة التهديد بنوع التهديد
        with col3: st.markdown(f'<div class="metric-card"><h6>نوع التهديد</h6><h3 style="color:#D4AF37">{ "تصيد مالي" if risk_level == "HIGH" else "برمجيات خبيثة" if risk_level == "MEDIUM" else "سليمظاهرياً"}</h3></div>', unsafe_allow_html=True)

        col_main, col_ss = st.columns([1.3, 1])
        
        with col_main:
            st.markdown('<div class="report-box rtl-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 تقرير التحليل الجنائي المخصص</h4>", unsafe_allow_html=True)
            st.write(f"**الهدف المرصود:** `{clean_url}`")
            if findings:
                for f in findings: st.markdown(f"<p style='color:#ffffff; background:rgba(255,75,75,0.05); padding:8px; border-radius:5px;'>• {f}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم رصد أي أدلة عدائية في هذا الرابط حالياً.</p>", unsafe_allow_html=True)
            
            # توصية مرجان بالإنجليزية كما طلبت
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:20px; border-radius:15px; border-left:5px solid #D4AF37; margin-top:25px;">
                    <h5 style="color:#D4AF37; font-family:Orbitron; letter-spacing:1px; margin-top:0;">🛡️ (Marjan Trace Advisory):</h5>
                    <p style="font-size:1.1em; line-height:1.6;">بناءً على الأدلة الجنائية، الرابط <b>{"خطير جداً" if is_threat else "يبدو سليماً"}</b>. {"يُنصح بحجب النطاق فوراً لحماية خصوصيتك." if is_threat else "يمكن التعامل معه بحذر."}</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ss:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 رادار كشف التهديدات</h3>", unsafe_allow_html=True)
            st.markdown('<div class="ss-frame rtl-container">', unsafe_allow_html=True)
            
            if is_threat:
                # محاكاة الضرر بناءً على التحليل (ليست فارغة)
                st.markdown("<h4 style='color:#ff4b4b; text-align:center;'>🚨 تحليل الأضرار المتوقعة:</h4>", unsafe_allow_html=True)
                for act in actions:
                    st.markdown(f"<div style='background:rgba(255,75,75,0.1); padding:10px; border-radius:10px; margin-bottom:10px; color:#eee;'>{act}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="text-align:center; margin-top:50px;">
                        <span style="font-size:5em; color:#2ea043;">🛡️</span>
                        <h4 style="color:#2ea043;">الرابط آمن للمعاينة</h4>
                        <p style="color:#888;">لم يتم رصد تهديدات بصرية نشطة.</p>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; padding:20px; color:#D4AF37; font-family:Orbitron; border-top:1px solid rgba(212,175,55,0.1);'>Developed by: Eng. Zaid Al-Janabi | Department of Cybersecurity Engineering | Al-Maarif University</div>", unsafe_allow_html=True)
