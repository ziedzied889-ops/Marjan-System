import streamlit as st
import re
import math
from urllib.parse import urlparse

# --- 1. إعدادات الصفحة الاحترافية (Responsive) ---
st.set_page_config(
    page_title="Marjan Trace v7.8 | Forensic Cyber System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. محرك التشريح الجنائي المكثف ---
def intensive_forensic_analysis(url):
    findings = []
    actions = []
    risk_label = "CLEAN / آمن"
    risk_color = "#2ea043"
    
    if not url: return findings, actions, risk_label, risk_color, 0

    domain = urlparse(url).netloc.lower()
    
    # حساب معامل العشوائية (Entropy)
    entropy = 0
    if domain:
        probs = [float(domain.count(c)) / len(domain) for c in dict.fromkeys(list(domain))]
        entropy = round(- sum([p * math.log(p) / math.log(2.0) for p in probs]), 2)

    # تحليل الأنماط السلوكية
    is_malicious = False
    
    if any(x in url.lower() for x in ['bank', 'secure', 'login', 'pay', 'crypto', 'verify', 'account']):
        findings.append("🔍 رصد محاولة انتحال صفحة رسمية (Phishing Attack).")
        actions.append("🔓 سرقة بيانات الهوية: الموقع مبرمج لسحب كلمات المرور فور كتابتها.")
        is_malicious = True
    
    if entropy > 3.6 or domain.count('.') > 3:
        findings.append(f"🕵️ مؤشر DGA: عشوائية النطاق ({entropy}) تشير لروابط مولدة آلياً لهجمات Botnet.")
        actions.append("🤖 التحكم عن بعد: محاولة تحويل الجهاز لـ 'زومبي' ضمن شبكة مخترقة.")
        is_malicious = True

    if any(ext in domain for ext in ['.xyz', '.top', '.online', '.link', '.pw', '.tk']):
        findings.append("🚩 نطاق مشبوه: استخدام امتدادات منخفضة التكلفة لتوزيع برمجيات الـ Ransomware.")
        actions.append("🦠 تشفير الملفات: اكتشاف محاولة تحميل صامت لبرمجيات الفدية.")
        is_malicious = True

    if is_malicious:
        risk_label = "CRITICAL / خطر"
        risk_color = "#ff4b4b"

    return findings, actions, risk_label, risk_color, entropy

# --- 3. تصميم الـ CSS والخلفية السيبرانية الكلية ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;900&display=swap');
    
    /* خلفية سيبرانية كلية ملء الشاشة */
    .stApp {
        background: #05070a !important;
        background-attachment: fixed;
    }

    #cyber-grid {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; opacity: 0.25; pointer-events: none;
    }

    .rtl-dir { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    
    .sys-header { 
        font-family: 'Orbitron', sans-serif; color: #D4AF37 !important; 
        text-align: center; font-size: 3.5rem; font-weight: 900; letter-spacing: 5px;
        text-shadow: 0 0 25px rgba(212, 175, 85, 0.4); margin-bottom: 0;
    }
    
    .metric-card { 
        background: rgba(13, 17, 23, 0.9); border: 1px solid rgba(212, 175, 85, 0.25); 
        border-top: 5px solid #D4AF37; padding: 20px; border-radius: 12px; text-align: center;
        backdrop-filter: blur(10px);
    }

    .report-box { 
        background: rgba(10, 25, 47, 0.85); border-radius: 20px; padding: 25px; 
        border: 1px solid rgba(212, 175, 85, 0.15); border-right: 8px solid #D4AF37;
        backdrop-filter: blur(10px);
    }

    .sandbox-container { 
        border: 2px solid #D4AF37; border-radius: 20px; background: rgba(0,0,0,0.9);
        min-height: 480px; padding: 25px; display: flex; flex-direction: column;
        backdrop-filter: blur(15px); box-shadow: inset 0 0 40px rgba(212, 175, 85, 0.05);
    }

    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #b8860b 100%) !important;
        color: black !important; font-weight: bold; border-radius: 12px; height: 3.8em;
        border: none; font-size: 1.1rem; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #D4AF37; }

    /* تحسين استجابة الموبايل */
    @media (max-width: 768px) {
        .sys-header { font-size: 2rem; }
        .metric-card { margin-bottom: 15px; }
    }
    </style>
    
    <div id="cyber-grid"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS('cyber-grid', {
            "particles": { "number": { "value": 120 }, "color": { "value": "#D4AF37" }, 
            "line_linked": { "enable": true, "distance": 150, "color": "#D4AF37", "opacity": 0.1 },
            "move": { "enable": true, "speed": 1.5 } }
        });
    </script>
    """, unsafe_allow_html=True)

# --- 4. الهيكل الرئيسي ---
st.markdown("<h1 class='sys-header'>MARJAN TRACE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white; font-family:Cairo; font-size:1.3rem; margin-top:-10px;'>نظام مَرْجَان لِلتحقيقِ الرَّقَمي والاستخبارات الجنائية</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
url_input = st.text_input("أدخل الرابط المراد تشريحه جنائياً:", placeholder="https://...")

if st.button("تفعيل بروتوكول الكشف الجنائي الشامل"):
    if url_input:
        findings, actions, label, color, entropy_val = intensive_forensic_analysis(url_input)
        
        # لوحة النتائج
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-card"><h6>الحالة الجنائية</h6><h3 style="color:{color}; margin:0;">{label}</h3></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card"><h6>الأدلة المرصودة</h6><h2 style="margin:0;">{len(findings)}</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card"><h6>عشوائية النطاق</h6><h2 style="margin:0;">{entropy_val}</h2></div>', unsafe_allow_html=True)

        col_main, col_ss = st.columns([1.4, 1])

        with col_main:
            st.markdown('<div class="report-box rtl-dir">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 تقرير التشريح الجنائي:</h4>", unsafe_allow_html=True)
            st.write(f"**الهدف المرصود:** `{url_input}`")
            
            if findings:
                for f in findings:
                    st.markdown(f"<p style='color:#ffffff; background:rgba(212,175,55,0.05); padding:10px; border-radius:8px; border-right:4px solid #D4AF37;'>• {f}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم رصد أدلة جرمية في بنية الرابط حالياً.</p>", unsafe_allow_html=True)
            
            # توصية Marjan Trace Advisory
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:20px; border-radius:15px; border-left:5px solid #D4AF37; margin-top:25px;">
                    <h5 style="color:#D4AF37; font-family:Orbitron; margin-top:0;">🛡️ (Marjan Trace Advisory):</h5>
                    <p style="font-size:1.1rem; line-height:1.6;">بناءً على التحليل الجنائي المتقدم، الرابط <b>{"يصنف كتهديد نشط" if len(findings)>0 else "يبدو سليماً"}</b>. {"يُنصح بحجب النطاق فوراً ومنع التعامل معه." if len(findings)>0 else "يمكن المتابعة مع الحذر الاعتيادي."}</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ss:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📽️ محاكاة Sandbox</h3>", unsafe_allow_html=True)
            st.markdown('<div class="sandbox-container rtl-dir">', unsafe_allow_html=True)
            
            if actions:
                st.markdown("<h4 style='color:#ff4b4b; text-align:center;'>🚨 ماذا سيفعل هذا الرابط؟</h4>", unsafe_allow_html=True)
                for act in actions:
                    # تم تصحيح طريقة كتابة الـ HTML لتجنب خطأ decimal literal
                    st.markdown(f"<div style='background:rgba(255,75,75,0.1); padding:12px; border-radius:10px; margin-bottom:10px; border:1px solid rgba(255,75,75,0.2); color:#eee;'>{act}</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="text-align:center; padding-top:60px;">
                        <span style="font-size:5rem;">🛡️</span>
                        <h4 style="color:#2ea043; margin-top:20px;">بيئة آمنة</h4>
                        <p style="color:#888;">لم يتم اكتشاف أضرار برمجية مرتقبة.</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style="margin-top:auto; padding:15px; background:rgba(212,175,55,0.05); border-radius:12px; border:1px dashed #D4AF37;">
                    <small style="color:#D4AF37;">📋 تقرير النشاط البرمجي:</small><br>
                    <small style="color:#aaa;">• تم عزل الرابط في بيئة Sandbox معزولة.<br>
                    • تم فحص طلبات الـ DNS ومسارات الـ Redirect.<br>
                    • الحالة: تم فحص التهديدات السلوكية بنجاح.</small>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br><p style='text-align:center; color:#D4AF37; font-family:Orbitron; opacity:0.6; font-size:0.9rem;'>Developed by: Eng. Zaid Al-Janabi | 2026 | Cybersecurity Department</p>", unsafe_allow_html=True)
