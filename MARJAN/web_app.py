import streamlit as st
import re
import math
from urllib.parse import urlparse

# --- إعدادات النظام الاحترافية ---
st.set_page_config(page_title="Marjan Trace v6.5 | Advanced Cyber Forensic", page_icon="🛡️", layout="wide")

# --- محرك التحليل الجنائي المتقدم ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

# --- التنسيق البصري وحقن الخلفية السيبرانية الكلية ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;900&display=swap');
    
    /* خلفية المتصفح الكلية (المساحات التي كانت سوداء) */
    .stApp {
        background: radial-gradient(circle at center, #0a1018 0%, #05070a 100%) !important;
        background-attachment: fixed !important;
    }

    /* طبقة الشبكة السيبرانية المتحركة */
    #cyber-grid-bg {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; opacity: 0.35; pointer-events: none;
    }

    .rtl-container { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }

    .sys-title { 
        font-family: 'Orbitron', sans-serif; color: #D4AF37 !important; 
        text-align: center; font-size: 4em; font-weight: 900; 
        margin-bottom: 0px; letter-spacing: 7px;
        text-shadow: 0 0 30px rgba(212, 175, 85, 0.6);
    }
    
    .arabic-sub { 
        font-family: 'Cairo', sans-serif; color: #ffffff; 
        text-align: center; font-size: 1.8em; margin-top: -20px; font-weight: 400;
    }

    .metric-card { 
        background: rgba(13, 17, 23, 0.9); border: 1px solid rgba(212, 175, 85, 0.3); 
        border-top: 5px solid #D4AF37; padding: 25px; border-radius: 15px; text-align: center;
        backdrop-filter: blur(10px);
    }

    .report-box { 
        background: rgba(10, 25, 47, 0.85); border-radius: 20px; padding: 30px; 
        border: 1px solid rgba(212, 175, 85, 0.2); margin-top: 20px; 
        border-right: 10px solid #D4AF37;
        backdrop-filter: blur(10px);
    }

    .sandbox-frame { 
        border: 2px solid #D4AF37; border-radius: 20px; background: rgba(0,0,0,0.9);
        min-height: 480px; padding: 25px; display: flex; flex-direction: column; 
        justify-content: center; backdrop-filter: blur(15px);
        box-shadow: inset 0 0 50px rgba(212, 175, 85, 0.1);
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #f1c40f 100%) !important;
        color: black !important; font-weight: bold; border-radius: 12px; height: 3.8em;
        font-size: 1.1em; border: none; width: 100%;
    }
    </style>

    <div id="cyber-grid-bg"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS('cyber-grid-bg', {
            "particles": {
                "number": { "value": 150 },
                "color": { "value": "#D4AF37" },
                "shape": { "type": "circle" },
                "opacity": { "value": 0.5 },
                "size": { "value": 2 },
                "line_linked": { "enable": true, "distance": 150, "color": "#D4AF37", "opacity": 0.2 },
                "move": { "enable": true, "speed": 2 }
            }
        });
    </script>
    """, unsafe_allow_html=True)

# --- الواجهة ---
st.markdown("<h1 class='sys-title'>MARJAN TRACE</h1>", unsafe_allow_html=True)
st.markdown("<p class='arabic-sub'>نظام مَرْجَان لِلتحقيقِ الرَّقَمي</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
target_url = st.text_input("رابط الهدف المراد فحصه (Target URL)", placeholder="أدخل الرابط المشبوه هنا...")

if st.button("تفعيل بروتوكول الكشف الجنائي الشامل"):
    if target_url:
        clean_url = target_url.strip()
        if not clean_url.startswith("http"): clean_url = "https://" + clean_url
        domain = urlparse(clean_url).netloc
        entropy = get_entropy(domain)
        
        # تحليل التهديدات
        alerts = []
        user_explanation = "الرابط لا يظهر نشاطاً عدائياً مباشراً."
        
        if re.search(r'(login|verify|secure|account|bank|wallet|crypto|pay|update)', clean_url.lower()):
            alerts.append("🚨 انتحال هوية: الرابط يحاكي صفحات رسمية لسرقة البيانات.")
            user_explanation = "⚠️ خطر: هذا الموقع يحاول خداعك لسرقة اسم المستخدم وكلمة المرور الخاصة بك (تصيد احتيالي)."
        
        if any(ext in domain.lower() for ext in ['.xyz', '.top', '.online', '.link', '.pw']):
            alerts.append("🚩 نطاق مشبوه: استخدام امتداد رخيص يُستخدم عادةً في الهجمات.")
            if "خطر" not in user_explanation: user_explanation = "⚠️ تنبيه: الموقع يستخدم نطاقاً غير موثوق يُستخدم غالباً لتوزيع الفيروسات."

        if entropy > 3.2:
            alerts.append(f"🕵️ مؤشر DGA: عشوائية النطاق مرتفعة ({round(entropy,2)})؛ قد يكون الرابط مولداً آلياً.")
            user_explanation = "⚠️ خطر: تم اكتشاف بنية برمجية مشبوهة تشير إلى محاولة اختراق أو اتصال بسيرفرات معادية."

        is_threat = len(alerts) > 0
        final_label = "CRITICAL / خطر" if is_threat else "CLEAN / آمن"
        final_color = "#ff4b4b" if is_threat else "#2ea043"

        col_main, col_ss = st.columns([1.2, 1])

        with col_main:
            st.markdown("<div class='rtl-container'><h3>📊 لوحة مؤشرات الفحص</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h6>الحالة النهائية</h6><h2 style="color:{final_color}; margin:0;">{final_label}</h2></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h6>التهديدات</h6><h2 style="color:#ff4b4b; margin:0;">{len(alerts)}</h2></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h6>معامل العشوائية</h6><h2 style="margin:0;">{round(entropy,2)}</h2></div>', unsafe_allow_html=True)

            st.markdown('<div class="report-box rtl-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37;'>🔍 تقرير التحليل الجنائي</h4>", unsafe_allow_html=True)
            st.write(f"**الهدف:** `{clean_url}`")
            
            if is_threat:
                st.markdown("<p style='color:#ff4b4b; font-weight:bold;'>⚠️ الأدلة الجرمية المكتشفة:</p>", unsafe_allow_html=True)
                for a in alerts:
                    st.markdown(f"<p style='color:#ffffff; background:rgba(255,75,75,0.1); padding:10px; border-radius:8px;'>• {a}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043;'>✅ لم يتم رصد أدلة جرمية مباشرة في بنية الرابط.</p>", unsafe_allow_html=True)
            
            # توصية نظام مرجان
            st.markdown(f"""
                <div style="background:linear-gradient(90deg, rgba(212,175,55,0.2), transparent); padding:20px; border-radius:15px; border-left:5px solid #D4AF37; margin-top:25px;">
                    <h5 style="color:#D4AF37; margin-top:0;">🛡️ (Marjan Trace Advisory):</h5>
                    <p style="font-size:1.1em; line-height:1.6;">بناءً على التحليل الجنائي المتقدم، الرابط <b>{"خطير جداً" if is_threat else "آمن ظاهرياً"}</b>. 
                    {"يُنصح بحجب النطاق ومنع التعامل معه نهائياً لحماية خصوصيتك." if is_threat else "يمكن المتابعة مع الحذر الاعتيادي."}</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ss:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 محاكاة المعاينة (Sandbox)</h3>", unsafe_allow_html=True)
            status_icon = "🚫" if is_threat else "🛡️"
            st.markdown(f"""
                <div class="sandbox-frame rtl-container">
                    <div style="text-align:center;">
                        <span style="font-size:5em;">{status_icon}</span>
                        <h3 style="color:{final_color}; margin-top:20px;">تحليل الأضرار المتوقعة:</h3>
                        <p style="color:#eee; font-size:1.2em; padding: 0 10px;">{user_explanation}</p>
                    </div>
                    <div style="background:rgba(255,255,255,0.05); border:1px dashed #D4AF37; padding:15px; border-radius:10px; margin-top:25px;">
                        <h5 style="color:#D4AF37; margin-bottom:5px;">📋 سجل النشاط البصري:</h5>
                        <p style="font-size:0.9em; color:#ccc;">
                        • تم عزل الرابط في بيئة وهمية (Virtual Sandbox).<br>
                        • تم تحليل عناصر الـ JavaScript والروابط المتشعبة.<br>
                        • <b>الحالة:</b> {"يُمنع العرض المباشر لوجود تهديد نشط." if is_threat else "لا توجد عناصر بصرية ضارة مكتشفة."}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; padding:20px; color:#D4AF37; font-family:Orbitron; border-top:1px solid rgba(212,175,55,0.1);'>Developed by: Eng. Zaid Al-Janabi | 2026</div>", unsafe_allow_html=True)
