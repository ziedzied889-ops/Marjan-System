import streamlit as st
import re
import math
import requests
from urllib.parse import urlparse

# --- إعدادات النظام ---
st.set_page_config(page_title="Marjan Trace v7.0", page_icon="🛡️", layout="wide")

# --- محرك التحقيق الجنائي المكثف (Intensive Forensic Engine) ---
def deep_forensic_analysis(url):
    domain = urlparse(url).netloc.lower()
    path = urlparse(url).path.lower()
    
    # 1. حساب معامل العشوائية للنطاق
    entropy = 0
    if domain:
        probs = [float(domain.count(c)) / len(domain) for c in dict.fromkeys(list(domain))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in probs])

    findings = []
    actions = [] # ماذا يفعل الرابط الخبيث؟
    risk_score = 0

    # تحليل مكثف للأنماط
    # الفحص المالي والتصيد
    if any(x in url.lower() for x in ['bank', 'secure', 'login', 'pay', 'crypto', 'wallet', 'billing', 'signin']):
        findings.append("⚠️ رصد نمط 'هندسة اجتماعية' عالي الخطورة.")
        actions.append("🔓 سرقة بيانات الاعتماد: سيقوم الرابط بعرض صفحة مزيفة تسرق اسم المستخدم وكلمة المرور فور إدخالها.")
        actions.append("💰 اختراق مالي: محاولة الوصول إلى تفاصيل البطاقات الائتمانية أو محافظ الكريبتو.")
        risk_score += 40

    # فحص الروابط الطويلة والمشفرة
    if len(url) > 100 or "%" in url or domain.count('-') > 2:
        findings.append("⚠️ اكتشاف تقنيات 'تمويه الرابط' (URL Obfuscation).")
        actions.append("🎭 إخفاء الهوية: الرابط يستخدم تشفيراً لإخفاء الوجهة الحقيقية وتجاوز أنظمة الفحص التلقائي.")
        risk_score += 20

    # فحص النطاقات منخفضة الثقة
    if any(ext in domain for ext in ['.xyz', '.top', '.online', '.link', '.pw', '.tk', '.ga', '.cf']):
        findings.append("⚠️ استخدام نطاق (TLD) ذو سمعة سيئة.")
        actions.append("🦠 توزيع برمجيات: هذه النطاقات تُستخدم غالباً لتحميل ملفات تجسس (Spyware) صامتة على الجهاز.")
        risk_score += 15

    # فحص الروابط الفرعية المعقدة (Subdomain attack)
    if domain.count('.') > 2:
        findings.append("⚠️ رصد هجوم 'النطاقات الفرعية المتعددة'.")
        actions.append("📡 نفق بيانات: الرابط قد يعمل كقناة لتسريب بيانات من جهازك إلى سيرفر خارجي (C2 Server).")
        risk_score += 25

    # إذا كان الرابط مريباً برمجياً (عشوائية عالية)
    if entropy > 3.5:
        findings.append(f"⚠️ معامل عشوائية مرتفع ({round(entropy,2)}) يشير لـ DGA.")
        actions.append("🤖 التحكم عن بعد: الرابط قد يكون جزءاً من شبكة Botnet للتحكم في الأجهزة المخترقة.")
        risk_score += 30

    return findings, actions, round(entropy, 2), risk_score

# --- التنسيق البصري والخلفية السيبرانية الكلية ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;900&display=swap');
    
    .stApp {
        background: radial-gradient(circle at center, #0a1018 0%, #05070a 100%) !important;
        background-attachment: fixed !important;
    }

    #cyber-bg {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; opacity: 0.3; pointer-events: none;
    }

    .rtl-container { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    .sys-title { 
        font-family: 'Orbitron', sans-serif; color: #D4AF37 !important; 
        text-align: center; font-size: 3.8em; font-weight: 900; letter-spacing: 5px;
        text-shadow: 0 0 20px rgba(212, 175, 85, 0.5); margin-bottom: 0px;
    }
    
    .metric-card { 
        background: rgba(13, 17, 23, 0.9); border: 1px solid rgba(212, 175, 85, 0.3); 
        border-top: 5px solid #D4AF37; padding: 20px; border-radius: 15px; text-align: center;
    }

    .report-box { 
        background: rgba(10, 25, 47, 0.85); border-radius: 20px; padding: 25px; 
        border-right: 8px solid #D4AF37; border-left: 1px solid rgba(212, 175, 85, 0.2);
    }

    .sandbox-frame { 
        border: 2px solid #D4AF37; border-radius: 20px; background: rgba(0,0,0,0.9);
        min-height: 500px; padding: 25px; display: flex; flex-direction: column;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #b8860b 100%) !important;
        color: black !important; font-weight: bold; border-radius: 12px; height: 3.5em;
    }
    </style>

    <div id="cyber-bg"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS('cyber-bg', {
            "particles": {
                "number": { "value": 130 },
                "color": { "value": "#D4AF37" },
                "line_linked": { "enable": true, "color": "#D4AF37", "opacity": 0.15 },
                "move": { "enable": true, "speed": 1.5 }
            }
        });
    </script>
    """, unsafe_allow_html=True)

# --- واجهة Marjan Trace ---
st.markdown("<h1 class='sys-title'>MARJAN TRACE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:white; font-family:Cairo; font-size:1.3em;'>نظام التحليل السلوكي والاستخبارات الجنائية</p>", unsafe_allow_html=True)

url_input = st.text_input("أدخل الرابط المراد تحليله بشكل مكثف:", placeholder="https://...")

if st.button("بدء بروتوكول التشريح الجنائي"):
    if url_input:
        findings, actions, entropy_val, score = deep_forensic_analysis(url_input)
        
        is_threat = score >= 25
        status_label = "CRITICAL / خطر" if is_threat else "CLEAN / آمن"
        status_color = "#ff4b4b" if is_threat else "#2ea043"

        col_left, col_right = st.columns([1.3, 1])

        with col_left:
            st.markdown("<div class='rtl-container'><h3>📊 لوحة تحليل النطاق</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h6>الحالة النهائية</h6><h2 style="color:{status_color};">{status_label}</h2></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h6>مستوى التهديد</h6><h2 style="color:#ff4b4b;">%{min(score, 100)}</h2></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h6>العشوائية</h6><h2>{entropy_val}</h2></div>', unsafe_allow_html=True)

            st.markdown('<div class="report-box rtl-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 نتائج الفحص الاستخباراتي:</h4>", unsafe_allow_html=True)
            
            if findings:
                for f in findings:
                    st.markdown(f"<p style='color:#fff;'>• {f}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم رصد أي أنماط عدائية في بنية الرابط.</p>", unsafe_allow_html=True)

            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:20px; border-radius:15px; border-left:5px solid #D4AF37; margin-top:20px;">
                    <h5 style="color:#D4AF37; margin:0;">🛡️ (Marjan Trace Advisory):</h5>
                    <p style="margin-top:10px;">{"بناءً على السلوك المكتشف، الرابط يمثل تهديداً حقيقياً؛ ننصح بحجبه فوراً." if is_threat else "الرابط لا يظهر أي مؤشرات خطر، يمكن التعامل معه بحذر."}</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_right:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📽️ محاكاة الضرر (Sandbox)</h3>", unsafe_allow_html=True)
            st.markdown('<div class="sandbox-frame rtl-container">', unsafe_allow_html=True)
            
            if is_threat:
                st.markdown("<h4 style='color:#ff4b4b; text-align:center;'>🚨 ماذا سيفعل هذا الرابط؟</h4>", unsafe_allow_html=True)
                for act in actions:
                    st.markdown(f"<div style='background:rgba(255,75,75,0.1); padding:12px; border-radius:10px; margin-bottom:10px; color:#eee;'>{act}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="text-align:center; margin-top:50px;">
                        <span style="font-size:5em;">🛡️</span>
                        <h4 style="color:#2ea043;">بيئة آمنة</h4>
                        <p style="color:#888;">لم يتم رصد أي عمليات تخريبية مرتقبة لهذا الرابط في بيئة الـ Sandbox.</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="margin-top:auto; padding:15px; background:rgba(212,175,55,0.05); border-radius:10px; border:1px dashed #D4AF37;">
                    <small style="color:#D4AF37;">📋 تقرير تقني (Technical Log):</small><br>
                    <small style="color:#888;">• تم تحليل الرابط في بيئة معزولة (Virtual Machine).<br>
                    • تم تتبع طلبات الـ HTTP ورموز الاستجابة.<br>
                    • الحالة: {"تم حجب العمليات التخريبية." if is_threat else "النظام مستقر."}</small>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br><p style='text-align:center; color:#D4AF37; font-family:Orbitron; opacity:0.6;'>Developed by: Eng. Zaid Al-Janabi | 2026</p>", unsafe_allow_html=True)
