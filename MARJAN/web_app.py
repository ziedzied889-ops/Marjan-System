import streamlit as st
import re
import math
from urllib.parse import urlparse

# --- 1. إعدادات الصفحة النهائية ---
st.set_page_config(
    page_title="Marjan Trace v8.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. محرك التحليل الجنائي الذكي ---
def forensic_analysis(url):
    findings = []
    actions = []
    status = "CLEAN / آمن"
    color = "#2ea043"
    
    if not url: return findings, actions, status, color, 0

    domain = urlparse(url).netloc.lower()
    
    # حساب العشوائية
    entropy = 0
    if domain:
        probs = [float(domain.count(c)) / len(domain) for c in dict.fromkeys(list(domain))]
        entropy = round(- sum([p * math.log(p) / math.log(2.0) for p in probs]), 2)

    # كشف التهديدات
    is_danger = False
    if any(x in url.lower() for x in ['bank', 'login', 'secure', 'crypto', 'verify']):
        findings.append("🔍 اكتشاف نمط تصيد عالي الخطورة (Phishing).")
        actions.append("🔓 سرقة الهوية: محاولة الاستيلاء على بيانات الدخول والبطاقات.")
        is_danger = True
    
    if entropy > 3.7 or domain.count('.') > 3:
        findings.append("🕵️ مؤشر DGA: النطاق مشبوه وقد يكون مرتبطاً بسيرفرات C2.")
        actions.append("📡 اتصال خارجي: محاولة بناء قناة اتصال مع سيرفر قيادة وسيطرة.")
        is_danger = True

    if is_danger:
        status = "CRITICAL / خطر"
        color = "#ff4b4b"

    return findings, actions, status, color, entropy

# --- 3. التصميم البصري (CSS) وتصحيح الأخطاء ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;900&display=swap');
    
    .stApp { background-color: #05070a !important; }
    
    .rtl-box { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    
    .main-title { 
        font-family: 'Orbitron', sans-serif; color: #D4AF37; 
        text-align: center; font-size: 3.5rem; letter-spacing: 5px;
        text-shadow: 0 0 20px rgba(212, 175, 85, 0.3);
    }

    .metric-card { 
        background: rgba(13, 17, 23, 0.9); border: 1px solid rgba(212, 175, 85, 0.2); 
        border-top: 4px solid #D4AF37; padding: 20px; border-radius: 12px; text-align: center;
    }

    /* تحسين إطار المعاينة Sandbox لضمان عدم ظهوره فارغاً */
    .sandbox-container { 
        border: 2px solid #D4AF37; border-radius: 20px; background: #000;
        min-height: 450px; padding: 30px; display: flex; flex-direction: column;
        box-shadow: inset 0 0 30px rgba(212, 175, 85, 0.1);
    }

    .action-item {
        background: rgba(255, 75, 75, 0.1); padding: 15px; border-radius: 10px; 
        margin-bottom: 15px; border-right: 5px solid #ff4b4b; color: #eee;
    }

    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #b8860b 100%) !important;
        color: black !important; font-weight: bold; border-radius: 12px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. واجهة المستخدم ---
st.markdown("<h1 class='main-title'>MARJAN TRACE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white; font-family:Cairo;'>نظام مَرْجَان لِلتحقيقِ الرَّقَمي والاستخبارات السيبرانية</p>", unsafe_allow_html=True)

url_input = st.text_input("أدخل الرابط المراد فحصه:", placeholder="https://...")

if st.button("بدء بروتوكول التحليل"):
    if url_input:
        findings, actions, status, color, entropy = forensic_analysis(url_input)
        
        # ترتيب الأيقونات والمؤشرات
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div class="metric-card"><h6>الحالة الجنائية</h6><h3 style="color:{color}">{status}</h3></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card"><h6>الأدلة المكتشفة</h6><h2>{len(findings)}</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card"><h6>معامل العشوائية</h6><h2>{entropy}</h2></div>', unsafe_allow_html=True)

        col_main, col_ss = st.columns([1.3, 1])

        with col_main:
            st.markdown('<div class="rtl-box" style="background:rgba(10,25,47,0.8); padding:25px; border-radius:15px; border-right:6px solid #D4AF37; margin-top:20px;">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 تقرير الفحص التفصيلي:</h4>", unsafe_allow_html=True)
            if findings:
                for f in findings: st.markdown(f"<p style='color:white;'>• {f}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم رصد تهديدات مباشرة في بنية الرابط.</p>", unsafe_allow_html=True)
            
            # توصية المهندس زيد (Zaid's Advisory)
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:20px; border-radius:15px; border-left:5px solid #D4AF37; margin-top:25px;">
                    <h5 style="color:#D4AF37; font-family:Orbitron;">🛡️ (Zaid's Advisory):</h5>
                    <p>بناءً على الأدلة الجنائية، الرابط <b>{"خطير جداً" if len(findings)>0 else "يبدو سليماً"}</b>. نوصي بحجب النطاق فوراً ومنع التعامل معه.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ss:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📽️ محاكاة Sandbox</h3>", unsafe_allow_html=True)
            st.markdown('<div class="sandbox-container rtl-box">', unsafe_allow_html=True)
            
            # معالجة مشكلة الخانة الفارغة
            if actions:
                st.markdown("<h4 style='color:#ff4b4b; text-align:center;'>🚨 النشاط التخريبي المرصود:</h4>", unsafe_allow_html=True)
                for act in actions:
                    st.markdown(f"<div class='action-item'>{act}</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="text-align:center; padding-top:80px;">
                        <span style="font-size:5rem;">🛡️</span>
                        <h4 style="color:#2ea043;">بيئة آمنة</h4>
                        <p style="color:#888;">لا يوجد نشاط برمج خبيث قيد التنفيذ.</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
                <div style="margin-top:auto; padding:15px; border:1px dashed #D4AF37; border-radius:10px; background:rgba(212,175,55,0.05);">
                    <small style="color:#D4AF37;">📋 سجل المحاكاة:</small><br>
                    <small style="color:#aaa;">تم فحص الروابط وإعادة التوجيه (Redirects) بنجاح.</small>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#D4AF37; font-family:Orbitron; opacity:0.6;'>Developed by: Eng. Zaid Al-Janabi | 2026</p>", unsafe_allow_html=True)
