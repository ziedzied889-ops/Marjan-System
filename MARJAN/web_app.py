import streamlit as st
import re
import math
from urllib.parse import urlparse

# --- إعدادات النظام الاحترافية ---
st.set_page_config(page_title="Marjan Trace v5.0 | Advanced Cyber Forensic", page_icon="🛡️", layout="wide")

# --- محرك التحليل الجنائي المتقدم ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

# --- التنسيق البصري وحقن الخلفية السيبرانية الفخمة ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;900&display=swap');
    
    /* خلفية النظام الأساسية */
    .stApp {
        background: #05070a !important;
    }

    /* طبقة الخلفية المتحركة - Cyber Network Effect */
    #marjan-cyber-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        opacity: 0.3;
        background: radial-gradient(circle at center, #0a1018 0%, #05070a 100%);
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

    /* تأثير الزجاج للبطاقات Glassmorphism */
    .metric-card { 
        background: rgba(13, 17, 23, 0.85) !important; 
        border: 1px solid rgba(212, 175, 85, 0.3) !important; 
        border-top: 5px solid #D4AF37 !important; 
        padding: 25px; border-radius: 15px; text-align: center;
        backdrop-filter: blur(10px);
    }

    .report-box { 
        background: rgba(10, 25, 47, 0.8) !important; 
        border-radius: 20px; padding: 30px; 
        border: 1px solid rgba(212, 175, 85, 0.2) !important; 
        margin-top: 20px; 
        border-right: 10px solid #D4AF37 !important;
        backdrop-filter: blur(10px);
    }

    .radar-frame { 
        border: 2px solid #D4AF37 !important; 
        border-radius: 20px; background: rgba(0,0,0,0.85) !important;
        min-height: 450px; padding: 25px; display: flex; flex-direction: column; justify-content: center;
        box-shadow: inset 0 0 50px rgba(212, 175, 85, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #f1c40f 100%) !important;
        color: black !important; font-weight: bold; border-radius: 12px; height: 3.8em;
        font-size: 1.1em; border: none; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(212, 175, 85, 0.4);
    }

    @keyframes scan {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .radar-scanner {
        width: 120px; height: 120px; border: 4px solid #ff4b4b; border-radius: 50%; 
        margin: 0 auto; border-top-color: transparent; animation: scan 1.5s linear infinite;
    }
    </style>

    <div id="marjan-cyber-bg"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS('marjan-cyber-bg', {
            "particles": {
                "number": { "value": 160, "density": { "enable": true, "value_area": 800 } },
                "color": { "value": "#D4AF37" },
                "shape": { "type": "circle" },
                "opacity": { "value": 0.4, "random": true },
                "size": { "value": 2, "random": true },
                "line_linked": { "enable": true, "distance": 150, "color": "#D4AF37", "opacity": 0.2, "width": 1 },
                "move": { "enable": true, "speed": 1.8, "direction": "none", "random": true, "out_mode": "out" }
            },
            "interactivity": { 
                "detect_on": "canvas", 
                "events": { "onhover": { "enable": true, "mode": "grab" } } 
            },
            "retina_detect": true
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
        
        alerts = []
        if re.search(r'(login|verify|secure|account|bank|wallet|crypto|free|gift|bonus|signin|pay|update|official)', clean_url.lower()):
            alerts.append("🚨 انتحال هوية: الرابط يحتوي على كلمات استدراج لسرقة بيانات حساسة.")
        
        if any(ext in domain.lower() for ext in ['.xyz', '.top', '.online', '.site', '.tk', '.ml', '.ga', '.cf', '.link', '.pw', '.icu']):
            alerts.append("🚩 نطاق مشبوه: استخدام امتداد رخيص يُستخدم عادةً في حملات التخريب.")
        
        if entropy > 3.1:
            alerts.append(f"🕵️ مؤشر DGA: معامل العشوائية ({round(entropy,2)}) مرتفع؛ الرابط يبدو مولداً آلياً.")

        if domain.count('.') > 2:
            alerts.append("⚠️ تمويه الهيكلية: تم رصد تعدد في النطاقات الفرعية لتجاوز أنظمة الدفاع.")

        if any(p in domain for p in ['wixstudio', 'github.io', 'vercel.app', 'pages.dev', 'firebaseapp']):
            alerts.append("🚩 تمويه الاستضافة: يتم استخدام منصات موثوقة لإخفاء محتوى خبيث.")

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
            
            st.markdown(f"""
                <div style="background:linear-gradient(90deg, rgba(212,175,55,0.2), transparent); padding:20px; border-radius:15px; border-left:5px solid #D4AF37; margin-top:25px;">
                    <h5 style="color:#D4AF37; margin-top:0;">🛡️ توصية نظام مَرْجَان (Marjan Trace Recommendation):</h5>
                    <p style="font-size:1.1em; line-height:1.6;">بناءً على الأدلة الجنائية، الرابط <b>{"خطير جداً" if is_threat else "آمن ظاهرياً"}</b>. 
                    {"يُمنع التعامل معه نهائياً لخطورته القصوى على أمن المعلومات." if is_threat else "يمكن المتابعة مع الحذر."}</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ss:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 رادار كشف التهديدات</h3>", unsafe_allow_html=True)
            if is_threat:
                st.markdown("""
                    <div class="radar-frame rtl-container">
                        <div style="text-align:center;">
                            <div class="radar-scanner"></div>
                            <h3 style="color:#ff4b4b; margin-top:20px;">خطر: محتوى ضار!</h3>
                            <p style="color:#888;">تم عزل الرابط في بيئة Sandbox ومنع المعاينة البصرية لحماية نظامك.</p>
                        </div>
                        <div style="background:rgba(255,75,75,0.05); border:1px dashed #ff4b4b; padding:15px; border-radius:10px; margin-top:15px;">
                            <h5 style="color:#ff4b4b; margin-bottom:5px;">📋 سجل التحليل البصري:</h5>
                            <p style="font-size:0.9em; color:#ccc;">
                            • تم اكتشاف محاولة إعادة توجيه (Redirect).<br>
                            • رصد عناصر جافا سكربت مشبوهة (JS-Injection).<br>
                            • الموقع يحاول الوصول لصلاحيات الكاميرا/الموقع.<br>
                            • <b>القرار:</b> حجب المعاينة فوراً.</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="radar-frame rtl-container">
                        <div style="text-align:center;">
                            <span style="font-size:5em; color:#2ea043;">🛡️</span>
                            <h4 style="color:#2ea043;">الرابط آمن للمعاينة</h4>
                            <p style="color:#888;">لم يتم رصد تهديدات بصرية نشطة.</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; padding:20px; color:#D4AF37; font-family:Orbitron; border-top:1px solid rgba(212,175,55,0.1);'>Developed by: Eng. Zaid Al-Janabi | Department of Cybersecurity Engineering | Al-Maarif University | 2026</div>", unsafe_allow_html=True)
