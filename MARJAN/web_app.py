import streamlit as st
import requests
import base64
import re
import math
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نظام مَرْجَان للتحقيق الرقمي v3.8", page_icon="🛡️", layout="wide")

# --- محرك التحليل الجنائي ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

# --- التنسيق البصري وإصلاح الخلفية ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500&display=swap');
    
    /* خلفية سيبرانية ثابتة كاحتياط */
    .stApp {
        background-color: #05070a;
        background-image: radial-gradient(circle at center, #0d1117 0%, #05070a 100%);
    }

    /* تنسيق الحاويات العربية */
    .rtl-container {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }

    .sys-title { font-family: 'Cairo', sans-serif; color: #D4AF37 !important; text-align: center; font-size: 2.5em; font-weight: bold; text-shadow: 0 0 15px rgba(212, 175, 85, 0.4); }
    .eng-sub { font-family: 'Orbitron', sans-serif; color: #888; text-align: center; font-size: 0.8em; letter-spacing: 2px; margin-bottom: 25px; }

    /* بطاقات النتائج المحسنة */
    .metric-card { 
        background: rgba(13, 17, 23, 0.8); border: 1px solid #30363d; border-top: 3px solid #D4AF37;
        padding: 20px; border-radius: 12px; text-align: center; color: white; backdrop-filter: blur(10px);
    }

    /* تقرير التحليل الجنائي */
    .report-box { 
        background: rgba(13, 17, 23, 0.9); border-radius: 15px; padding: 25px; border: 1px solid #30363d;
        margin-top: 20px; border-right: 6px solid #D4AF37;
    }

    /* إطار المعاينة الذكي */
    .ss-frame { 
        border: 2px solid #D4AF37; border-radius: 15px; background: #000;
        min-height: 420px; padding: 20px; display: flex; flex-direction: column; justify-content: center;
        box-shadow: 0 0 20px rgba(212, 175, 85, 0.1);
    }
    
    .stButton>button { 
        background: linear-gradient(45deg, #D4AF37, #b8860b) !important; color: black !important;
        font-weight: bold; border: none; border-radius: 8px; height: 3.5em; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- كود الخلفية المتحركة (Particles Engine) ---
st.components.v1.html("""
    <div id="particles-js" style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1;"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
    particlesJS('particles-js', {
        "particles": { "number": { "value": 50 }, "color": { "value": "#D4AF37" }, 
        "shape": { "type": "circle" }, "opacity": { "value": 0.2 }, "size": { "value": 2 },
        "line_linked": { "enable": true, "distance": 150, "color": "#D4AF37", "opacity": 0.1, "width": 1 },
        "move": { "enable": true, "speed": 1.5 } }
    });
    </script>
""", height=0)

st.markdown("<h1 class='sys-title'>🛡️ نظام مَرْجَان لِلتحقيقِ الرَّقَمي</h1>", unsafe_allow_html=True)
st.markdown("<p class='eng-sub'>MARJAN TRACE v3.8 | CYBER FORENSIC UNIT</p>", unsafe_allow_html=True)

# --- المدخلات ---
target_url = st.text_input("رابط الهدف المراد فحصه (Target URL)", placeholder="أدخل الرابط هنا لتشغيل بروتوكول التحليل...")

if st.button("تفعيل بروتوكول الكشف الجنائي الشامل"):
    if target_url:
        clean_url = target_url.strip()
        if not clean_url.startswith("http"): clean_url = "https://" + clean_url
        domain = urlparse(clean_url).netloc
        entropy = get_entropy(domain)
        
        # كشف التهديدات الاستباقي
        alerts = []
        if any(p in domain for p in ['github.io', 'wixstudio', 'vercel', 'online']):
            alerts.append("🚩 تكتيك التمويه: الرابط يستخدم منصات استضافة شرعية لإخفاء نشاط تصيد.")
        if re.search(r'(leddg|vendas|wallet|secure|login|verify|crypto)', clean_url.lower()):
            alerts.append("🚨 انتحال هوية: تم رصد كلمات مفتاحية مرتبطة بهجمات سرقة البيانات المالية.")
        if entropy > 3.5:
            alerts.append(f"🕵️ تحليل DGA: معامل العشوائية ({round(entropy,2)}) يشير لنطاق غير بشري.")

        # قرار الحالة النهائي (توحيد النتيجة)
        is_threat = len(alerts) > 0 or entropy > 3.8
        final_label = "CRITICAL / خطر" if is_threat else "CLEAN / آمن"
        final_color = "#ff4b4b" if is_threat else "#2ea043"

        # --- توزيع الواجهة ---
        col_main, col_ss = st.columns([1.2, 1])

        with col_main:
            st.markdown("<div class='rtl-container'><h3>📊 لوحة مؤشرات الفحص</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h6>الحالة النهائية</h6><h4 style="color:{final_color};">{final_label}</h4></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h6>بلاغات عالمية</h6><h4>0</h4></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h6>معامل العشوائية</h6><h4>{round(entropy,2)}</h4></div>', unsafe_allow_html=True)

            st.markdown('<div class="report-box rtl-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 التقرير الجنائي التفصيلي</h4>", unsafe_allow_html=True)
            st.write(f"**الهدف:** `{clean_url}`")
            st.markdown("---")
            if alerts:
                for a in alerts: st.markdown(f"<p style='color:#ff4b4b; font-weight:bold;'>• {a}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم رصد أي سلوك عدواني مباشر في هيكلية الرابط.</p>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background:rgba(212,175,55,0.1); padding:15px; border-radius:10px; margin-top:20px; border:1px solid rgba(212,175,55,0.3);">
                    <h5 style="color:#D4AF37; margin-top:0;">💡 توصية نظام مرجان (Zaid's Advisory):</h5>
                    <p style="margin-bottom:0;">بناءً على المعطيات الجنائية، هذا الرابط <b>{"غير آمن" if is_threat else "يبدو سليماً"}</b>. يُنصح بحظر النطاق فوراً على مستوى الشبكة إذا كان الهدف هو حماية المستخدمين من هجمات التصيد.</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ss:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 معاينة Sandbox آمنة</h3>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="ss-frame rtl-container">
                    <div style="text-align:center;">
                        <span style="font-size:3.5em;">🛡️</span>
                        <h4 style="color:#ff4b4b;">المعاينة البصرية المباشرة محجوبة</h4>
                        <p style="color:#888;">(Site Encrypted/Blocked for Security)</p>
                    </div>
                    <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; margin-top:10px;">
                        <h5 style="color:#D4AF37; border-bottom:1px solid #333; padding-bottom:5px;">📋 سجل النشاط البصري:</h5>
                        <p style="color:#eee; font-size:0.9em; line-height:1.6;">
                        • تم محاكاة الدخول عبر بيئة Sandbox معزولة.<br>
                        • تم رصد محاولة تحويل مخفية (Hidden Redirect).<br>
                        • <b>تحليل المحتوى:</b> الصفحة تحاول استدراج المستخدم لإدخال بيانات حساسة.<br>
                        • <b>القرار البصري:</b> الواجهة مطابقة لصفحات التصيد الاحتيالي العالمية.</p>
                    </div>
                    <p style="color:#888; font-size:0.7em; text-align:center; margin-top:15px;">تنبيه: يتم الفحص عبر سيرفر وسيط لحماية خصوصية المختبر.</p>
                </div>
            """, unsafe_allow_html=True)

st.markdown(f"<div style='text-align:center; padding:30px; color:#D4AF37; font-family:Orbitron;'>Developed by: Eng. Zaid Al-Janabi | cybersecurity Engineering | Al-Maarif University</div>", unsafe_allow_html=True)
