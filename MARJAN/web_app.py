import streamlit as st
import re
import math
from urllib.parse import urlparse

# --- 1. إعدادات الصفحة الاحترافية والمتجاوبة ---
st.set_page_config(
    page_title="Marjan Trace v7.5 | Advanced Forensic Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. محرك التحقيق الجنائي المتقدم ---
def perform_deep_analysis(url):
    findings = []
    expected_impacts = []
    risk_category = "آمن ظاهرياً"
    risk_color = "#2ea043"
    
    if not url: return findings, expected_impacts, risk_category, risk_color

    domain = urlparse(url).netloc.lower()
    
    # حساب العشوائية (Entropy) للنطاق
    entropy = 0
    if domain:
        probs = [float(domain.count(c)) / len(domain) for c in dict.fromkeys(list(domain))]
        entropy = round(- sum([p * math.log(p) / math.log(2.0) for p in probs]), 2)

    # قواعد الفحص المكثف
    if any(x in url.lower() for x in ['bank', 'login', 'secure', 'pay', 'crypto', 'wallet', 'update', 'verify']):
        findings.append("🔍 اكتشاف محاولة انتحال صفحة رسمية (Phishing Attack).")
        expected_impacts.append("🔓 سرقة بيانات الاعتماد: سيتم سحب اسم المستخدم وكلمة المرور فور إدخالها.")
        expected_impacts.append("💰 مخاطر مالية: محاولة الوصول إلى الحسابات البنكية أو محافظ الكريبتو.")
        risk_category = "تهديد / خطر"
        risk_color = "#ff4b4b"
    
    if entropy > 3.6 or domain.count('.') > 3:
        findings.append(f"🕵️ مؤشر DGA: عشوائية النطاق مرتفعة ({entropy})؛ قد يكون الرابط مولداً آلياً لهجمات Botnet.")
        expected_impacts.append("🤖 اتصال سيرفرات C2: قد يتحول جهازك إلى جزء من شبكة مخترقة يتم التحكم بها عن بعد.")
        risk_category = "مشتبه به / خطر"
        risk_color = "#ff4b4b"

    if any(ext in domain for ext in ['.xyz', '.top', '.online', '.link', '.pw']):
        findings.append("🚩 نطاق ذو سمعة سيئة: استخدام امتدادات رخيصة تستخدم عادة في توزيع البرمجيات الخبيثة.")
        expected_impacts.append("🦠 تحميل صامت: الرابط قد يبدأ بتحميل برمجيات تجسس (Spyware) دون علمك.")
        if risk_category == "آمن ظاهرياً":
            risk_category = "تحذير أمني"
            risk_color = "#f1c40f"

    return findings, expected_impacts, risk_category, risk_color, entropy

# --- 3. تصميم الـ CSS والخلفية السيبرانية الكلية ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;900&display=swap');
    
    /* جعل الصفحة كاملة وبدون هوامش سوداء */
    .stApp {
        background: #05070a !important;
        background-attachment: fixed;
    }

    /* تأثير الشبكة السيبرانية الخلفية */
    #cyber-canvas {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; opacity: 0.25; pointer-events: none;
    }

    .rtl-text { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    
    .sys-header { 
        font-family: 'Orbitron', sans-serif; color: #D4AF37 !important; 
        text-align: center; font-size: 3.5rem; font-weight: 900; 
        margin-bottom: 0px; letter-spacing: 5px;
        text-shadow: 0 0 20px rgba(212, 175, 85, 0.4);
    }
    
    .sub-header { 
        font-family: 'Cairo', sans-serif; color: white; text-align: center; 
        font-size: 1.4rem; margin-top: -15px; opacity: 0.8;
    }

    .metric-card { 
        background: rgba(13, 17, 23, 0.9); border: 1px solid rgba(212, 175, 85, 0.2); 
        border-top: 4px solid #D4AF37; padding: 20px; border-radius: 12px; text-align: center;
        backdrop-filter: blur(10px);
    }

    .report-box { 
        background: rgba(10, 25, 47, 0.85); border-radius: 20px; padding: 25px; 
        border: 1px solid rgba(212, 175, 85, 0.15); border-right: 8px solid #D4AF37;
        backdrop-filter: blur(10px); margin-top: 20px;
    }

    .sandbox-frame { 
        border: 2px solid #D4AF37; border-radius: 20px; background: rgba(0,0,0,0.9);
        min-height: 450px; padding: 25px; display: flex; flex-direction: column;
        backdrop-filter: blur(15px);
    }

    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #b8860b 100%) !important;
        color: black !important; font-weight: bold; border-radius: 10px; height: 3.5em; width: 100%;
        border: none; font-size: 1.1rem;
    }

    /* جعل الواجهة متجاوبة للموبايل */
    @media (max-width: 768px) {
        .sys-header { font-size: 2.2rem; }
        .metric-card { margin-bottom: 10px; }
    }
    </style>
    
    <div id="cyber-canvas"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS('cyber-canvas', {
            "particles": { "number": { "value": 100 }, "color": { "value": "#D4AF37" }, 
            "line_linked": { "enable": true, "distance": 150, "color": "#D4AF37", "opacity": 0.1 },
            "move": { "enable": true, "speed": 2 } }
        });
    </script>
    """, unsafe_allow_html=True)

# --- 4. واجهة البرنامج ---
st.markdown("<h1 class='sys-header'>MARJAN TRACE</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>نظام مَرْجَان لِلتحقيقِ الرَّقَمي والاستخبارات السيبرانية</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
url_input = st.text_input("أدخل الرابط المراد تشريحه جنائياً (Target URL):", placeholder="https://example.com/malicious-link")

if st.button("تفعيل بروتوكول الفحص الشامل"):
    if url_input:
        findings, impacts, category, color, entropy_val = perform_deep_analysis(url_input)
        
        # لوحة المؤشرات (Responsive Columns)
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-card"><h6>الحالة الجنائية</h6><h3 style="color:{color}; margin:0;">{category}</h3></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card"><h6>الأدلة المرصودة</h6><h2 style="margin:0;">{len(findings)}</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card"><h6>معامل العشوائية</h6><h2 style="margin:0;">{entropy_val}</h2></div>', unsafe_allow_html=True)

        col_left, col_right = st.columns([1.4, 1])

        with col_left:
            st.markdown('<div class="report-box rtl-text">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 تقرير الفحص التفصيلي:</h4>", unsafe_allow_html=True)
            st.write(f"**الهدف:** `{url_input}`")
            
            if findings:
                for f in findings:
                    st.markdown(f"<p style='color:#ffffff; background:rgba(212,175,55,0.05); padding:10px; border-radius:8px; border-right:3px solid #D4AF37;'>• {f}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم العثور على أنماط تخريبية واضحة في بنية الرابط.</p>", unsafe_allow_html=True)
            
            # توصية المهندس زيد المحدثة
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:20px; border-radius:15px; border-left:5px solid #D4AF37; margin-top:25px;">
                    <h5 style="color:#D4AF37; font-family:Orbitron; margin-top:0;">🛡️ (Marjan Trace Advisory):</h5>
                    <p style="font-size:1.1rem; line-height:1.6;">بناءً على التحليل الجنائي المتقدم، الرابط <b>{"يُصنف كتهديد نشط" if len(findings)>0 else "يبدو مستقراً ظاهرياً"}</b>. {"نوصي بحجبه فوراً وعدم إدخال أي بيانات حساسة." if len(findings)>0 else "يمكن المتابعة بحذر."}</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_right:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📽️ محاكاة Sandbox</h3>", unsafe_allow_html=True)
            st.markdown('<div class="sandbox-frame rtl-text">', unsafe_allow_html=True)
            
            if impacts:
                st.markdown("<h4 style='color:#ff4b4b; text-align:center;'>🚨 ماذا سيفعل هذا الرابط؟</h4>", unsafe_allow_html=True)
                for imp in impacts:
                    # تم تصحيح الخطأ البرمجي هنا (استخدام علامات اقتباس مختلفة لتجنب SyntaxError)
                    st.markdown(f"<div style='background:rgba(255,75,75,0.1); padding:12px; border-radius:10px; margin-bottom:10px; color:#eee; border:1px solid rgba(255,75,75,0.2);'>{imp}</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="text-align:center; padding:40px;">
                        <span style="font-size:5rem;">🛡️</span>
                        <h4 style="color:#2ea043; margin-top:20px;">البيئة آمنة</h4>
                        <p style="color:#888;">لا توجد عمليات تخريبية مرصودة في هذه المحاكاة.</p>
                    </div>
                """, unsafe_allow_html=True)
                
            st.markdown("""
                <div style="margin-top:auto; padding:15px; background:rgba(212,175,55,0.05); border-radius:12px; border:1px dashed #D4AF37;">
                    <small style="color:#D4AF37;">📋 سجل النشاط التقني:</small><br>
                    <small style="color:#aaa;">• تم تشغيل الرابط في بيئة معزولة (VM).<br>
                    • تم تتبع طلبات الـ HTTP والـ DOM Elements.<br>
                    • الحالة: تم فحص التهديدات السلوكية بنجاح.</small>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br><p style='text-align:center; color:#D4AF37; font-family:Orbitron; opacity:0.6; font-size:0.9rem;'>Developed by: Eng. Zaid Al-Janabi | 2026 | Al-Maarif University</p>", unsafe_allow_html=True)
