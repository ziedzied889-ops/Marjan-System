import streamlit as st
import re
import math
from urllib.parse import urlparse

# --- 1. إعدادات النظام ---
st.set_page_config(page_title="Marjan Trace v8.5", layout="wide", initial_sidebar_state="collapsed")

# --- 2. محرك التحليل الجنائي المطور ---
def advanced_forensic_engine(url):
    findings = []
    actions = []
    status = "CLEAN / آمن"
    color = "#2ea043"
    
    if not url: return findings, actions, status, color, 0

    domain = urlparse(url).netloc.lower()
    
    # حساب العشوائية (Entropy)
    entropy = 0
    if domain:
        probs = [float(domain.count(c)) / len(domain) for c in dict.fromkeys(list(domain))]
        entropy = round(- sum([p * math.log(p) / math.log(2.0) for p in probs]), 2)

    # التحقق من خباثة الرابط (تطوير الفحص ليشمل النطاقات المشبوهة)
    is_malicious = False
    
    # فحص الكلمات الدلالية
    if any(x in url.lower() for x in ['bank', 'login', 'secure', 'crypto', 'fortnite', 'free']):
        findings.append("🔍 رصد محاولة استدراج (Phishing) باستخدام كلمات دلالية مخادعة.")
        actions.append("🔓 سحب البيانات: محاولة الاستيلاء على حسابات المستخدم.")
        is_malicious = True

    # فحص الامتدادات (التي ظهرت في صورتك مثل .top)
    if any(domain.endswith(ext) for ext in ['.top', '.xyz', '.online', '.link', '.pw', '.tk']):
        findings.append(f"🚩 نطاق عالي الخطورة: الامتداد ({domain.split('.')[-1]}) يستخدم غالباً في الهجمات السيبرانية.")
        actions.append("🦠 برمجيات خبيثة: احتمالية تحميل تلقائي لملفات ضارة.")
        is_malicious = True

    if entropy > 3.4:
        findings.append(f"🕵️ مؤشر DGA: عشوائية النطاق ({entropy}) تشير إلى رابط مولد برمجياً.")
        actions.append("📡 اتصال C2: محاولة ربط الجهاز بسيرفرات تحكم مشبوهة.")
        is_malicious = True

    if is_malicious:
        status = "CRITICAL / خطر"
        color = "#ff4b4b"

    return findings, actions, status, color, entropy

# --- 3. تصميم الواجهة (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;900&display=swap');
    .stApp { background-color: #05070a !important; }
    .rtl-box { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    .main-title { font-family: 'Orbitron', sans-serif; color: #D4AF37; text-align: center; font-size: 3rem; }
    
    /* إطار المعاينة Sandbox */
    .sandbox-frame { 
        border: 2px solid #D4AF37; border-radius: 20px; background: #000;
        min-height: 400px; padding: 25px; position: relative;
    }
    
    /* تنسيق الأيقونات لتكون على اليسار */
    .side-icons {
        position: absolute; left: 15px; top: 50%; transform: translateY(-50%);
        display: flex; flex-direction: column; gap: 20px; font-size: 1.5rem;
    }

    .action-card {
        background: rgba(255, 75, 75, 0.1); padding: 12px; border-radius: 10px; 
        margin-bottom: 10px; border-right: 4px solid #ff4b4b; color: #eee;
    }

    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #b8860b 100%) !important;
        color: black !important; font-weight: bold; border-radius: 10px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. بناء الصفحة ---
st.markdown("<h1 class='main-title'>MARJAN TRACE</h1>", unsafe_allow_html=True)

url_input = st.text_input("أدخل الرابط المراد تشريحه جنائياً:", placeholder="https://...")

if st.button("بدء الفحص الجنائي المتقدم"):
    if url_input:
        findings, actions, status, color, entropy = advanced_forensic_engine(url_input)
        
        # كروت المؤشرات
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f'<div style="background:#0d1117; padding:20px; border-radius:10px; border-top:4px solid #D4AF37; text-align:center;"><small>الحالة</small><h3 style="color:{color}">{status}</h3></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div style="background:#0d1117; padding:20px; border-radius:10px; border-top:4px solid #D4AF37; text-align:center;"><small>الأدلة</small><h2>{len(findings)}</h2></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div style="background:#0d1117; padding:20px; border-radius:10px; border-top:4px solid #D4AF37; text-align:center;"><small>العشوائية</small><h2>{entropy}</h2></div>', unsafe_allow_html=True)

        col_rep, col_san = st.columns([1.2, 1])

        with col_rep:
            st.markdown('<div class="rtl-box" style="background:rgba(10,25,47,0.8); padding:20px; border-radius:15px; border-right:5px solid #D4AF37; margin-top:20px;">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 تقرير التشريح:</h4>", unsafe_allow_html=True)
            if findings:
                for f in findings: st.markdown(f"<p style='color:white; font-size:0.95rem;'>• {f}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم رصد تهديدات في بنية الرابط.</p>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:15px; border-radius:12px; border-left:4px solid #D4AF37; margin-top:20px;">
                    <h6 style="color:#D4AF37; margin:0;">🛡️ (Zaid's Advisory):</h6>
                    <p style="margin:5px 0 0 0; font-size:0.9rem;">بناءً على الأدلة الجنائية، الرابط <b>{"خبيث ويجب حجبه" if len(findings)>0 else "يبدو مستقراً"}</b>. ننصح بعدم النقر نهائياً.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_san:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📽️ Sandbox</h3>", unsafe_allow_html=True)
            st.markdown('<div class="sandbox-frame rtl-box">', unsafe_allow_html=True)
            
            # الأيقونات على اليسار داخل الـ Sandbox
            st.markdown("""
                <div class="side-icons">
                    <span title="عزل البيئة">🛡️</span>
                    <span title="تتبع الاتصال">🌐</span>
                    <span title="كشف التشفير">🔐</span>
                </div>
            """, unsafe_allow_html=True)

            if actions:
                st.markdown("<h4 style='color:#ff4b4b; text-align:center;'>⚠️ النشاط المتوقع:</h4>", unsafe_allow_html=True)
                for act in actions:
                    st.markdown(f"<div class='action-card'>{act}</div>", unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center; opacity:0.5; padding-top:100px;"><h5>البيئة آمنة</h5><p>لا يوجد نشاط تخريبي</p></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#D4AF37; opacity:0.5;'>Eng. Zaid Al-Janabi | 2026</p>", unsafe_allow_html=True)
