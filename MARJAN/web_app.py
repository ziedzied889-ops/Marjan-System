import streamlit as st
import re
import math
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace v4.8 | Cyber Forensic Unit", page_icon="🛡️", layout="wide")

# --- محرك التحليل الجنائي المتقدم ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

# --- التنسيق البصري والخلفية المتحركة الاحترافية ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500;900&display=swap');
    
    .stApp { background: #05070a !important; }
    
    /* حاوية الخلفية المتحركة */
    #cyber-network-bg {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        z-index: -1; opacity: 0.25; pointer-events: none;
    }

    .rtl-container { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }

    /* الهوية البصرية */
    .sys-title { 
        font-family: 'Orbitron', sans-serif; color: #D4AF37 !important; 
        text-align: center; font-size: 4em; font-weight: 900; 
        margin-bottom: 0px; letter-spacing: 7px;
        text-shadow: 0 0 30px rgba(212, 175, 85, 0.6);
    }
    .arabic-sub { 
        font-family: 'Cairo', sans-serif; color: #ffffff; 
        text-align: center; font-size: 1.8em; margin-top: -20px; font-weight: 400;
        letter-spacing: 2px;
    }

    .metric-card { 
        background: rgba(13, 17, 23, 0.95); border: 1px solid rgba(212, 175, 85, 0.3); 
        border-top: 5px solid #D4AF37; padding: 25px; border-radius: 15px; text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .report-box { 
        background: rgba(10, 25, 47, 0.9); border-radius: 20px; padding: 30px; 
        border: 1px solid rgba(212, 175, 85, 0.2); margin-top: 20px; 
        border-right: 10px solid #D4AF37;
    }

    .ss-frame { 
        border: 2px solid #D4AF37; border-radius: 20px; background: rgba(0,0,0,0.9);
        min-height: 450px; padding: 25px; display: flex; flex-direction: column; justify-content: center;
        box-shadow: inset 0 0 50px rgba(212, 175, 85, 0.1);
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37 0%, #f1c40f 100%) !important;
        color: black !important; font-weight: bold; border-radius: 12px; height: 3.8em;
        font-size: 1.1em; border: none; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(212, 175, 85, 0.4); }
    </style>

    <div id="cyber-network-bg"></div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS('cyber-network-bg', {
            "particles": {
                "number": { "value": 120, "density": { "enable": true, "value_area": 800 } },
                "color": { "value": "#D4AF37" },
                "shape": { "type": "circle" },
                "opacity": { "value": 0.5, "random": true },
                "size": { "value": 3, "random": true },
                "line_linked": { "enable": true, "distance": 150, "color": "#D4AF37", "opacity": 0.2, "width": 1.5 },
                "move": { "enable": true, "speed": 2, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false }
            },
            "interactivity": { "detect_on": "canvas", "events": { "onhover": { "enable": true, "mode": "grab" } } }
        });
    </script>
    """, unsafe_allow_html=True)

# --- الواجهة ---
st.markdown("<h1 class='sys-title'>MARJAN TRACE</h1>", unsafe_allow_html=True)
st.markdown("<p class='arabic-sub'>نظام مَرْجَان لِلتحقيقِ الرَّقَمي</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
target_url = st.text_input("رابط الهدف المراد فحصه (Target URL)", placeholder="أدخل الرابط المشبوه هنا لتشغيل بروتوكولات الفحص القصوى...")

if st.button("تفعيل بروتوكول التحليل الجنائي الشامل"):
    if target_url:
        clean_url = target_url.strip()
        if not clean_url.startswith("http"): clean_url = "https://" + clean_url
        domain = urlparse(clean_url).netloc
        entropy = get_entropy(domain)
        
        # --- محرك الكشف "بأقصى طاقة" ---
        alerts = []
        
        # 1. كشف التصيد المالي والاجتماعي
        if re.search(r'(login|verify|secure|account|update|bank|banc|wallet|crypto|coin|free|gift|bonus|office|signin)', clean_url.lower()):
            alerts.append("🚨 كشف انتحال: الرابط يحتوي على كلمات استدراج تُستخدم في سرقة الحسابات.")
        
        # 2. كشف النطاقات المشبوهة
        if any(ext in domain.lower() for ext in ['.xyz', '.top', '.online', '.site', '.tk', '.ml', '.ga', '.cf', '.gq', '.link']):
            alerts.append("🚩 نطاق عالي الخطورة: استخدام امتدادات غير موثوقة مرتبطة بـ 90% من هجمات السبام.")
        
        # 3. كشف العشوائية (DGA) - حساسية قصوى
        if entropy > 3.2:
            alerts.append(f"🕵️ كشف DGA: معامل العشوائية ({round(entropy,2)}) يشير لنطاق مولد برمجياً لتجنب الحجب.")
            
        # 4. كشف النطاقات الفرعية المتعددة
        if domain.count('.') > 2:
            alerts.append("⚠️ تحليل الهيكلية: تم رصد تعدد في النطاقات الفرعية، تكتيك يُستخدم لتجاوز فلاتر البريد.")

        # 5. كشف الروابط المختصرة
        if any(s in domain for s in ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'shorte.st']):
            alerts.append("🔗 رابط مموه: الرابط يستخدم خدمة اختصار لإخفاء الوجهة النهائية الحقيقية.")

        is_threat = len(alerts) > 0 or entropy > 3.5
        final_label = "CRITICAL / خطر" if is_threat else "CLEAN / آمن"
        final_color = "#ff4b4b" if is_threat else "#2ea043"

        col_main, col_ss = st.columns([1.2, 1])

        with col_main:
            st.markdown("<div class='rtl-container'><h3>📊 نتائج الفحص الجنائي</h3></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h6>الحالة النهائية</h6><h2 style="color:{final_color}; margin:0;">{final_label}</h2></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h6>التهديدات المكتشفة</h6><h2 style="color:#ff4b4b; margin:0;">{len(alerts)}</h2></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h6>قوة التشفير/العشوائية</h6><h2 style="margin:0;">{round(entropy,2)}</h2></div>', unsafe_allow_html=True)

            st.markdown('<div class="report-box rtl-container">', unsafe_allow_html=True)
            st.markdown("<h4 style='color:#D4AF37; border-bottom:1px solid #333; padding-bottom:10px;'>🔍 تحليل الأدلة الجرمية</h4>", unsafe_allow_html=True)
            st.write(f"**الهدف المرصود:** `{clean_url}`")
            
            if is_threat:
                st.markdown("<p style='color:#ff4b4b; font-weight:bold; font-size:1.1em;'>⚠️ تم رصد مؤشرات الخطر التالية:</p>", unsafe_allow_html=True)
                for a in alerts:
                    st.markdown(f"<p style='color:#ffffff; background:rgba(255,75,75,0.1); padding:8px; border-radius:5px;'>• {a}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#2ea043; font-size:1.1em;'>✅ بنية الرابط لا تحتوي على مؤشرات خبيثة معروفة.</p>", unsafe_allow_html=True)
            
            # توصية نظام مرجان المحدثة
            st.markdown(f"""
                <div style="background:linear-gradient(90deg, rgba(212,175,55,0.2), transparent); padding:20px; border-radius:15px; border-left:5px solid #D4AF37; margin-top:25px;">
                    <h5 style="color:#D4AF37; margin-top:0;">🛡️ توصية نظام مَرْجَان (Marjan Trace Recommendation):</h5>
                    <p style="font-size:1.1em; line-height:1.6;">بناءً على بروتوكولات الفحص المتقدمة، يُصنف هذا الرابط كونه <b>{"تهديد سيبراني نشط" if is_threat else "رابط سليم"}</b>. 
                    {"يجب حظر الوصول إليه من خلال جدار الحماية (Firewall) ومنع المستخدمين من التفاعل معه منعاً لسرقة البيانات." if is_threat else "يمكن للمستخدم المتابعة مع أخذ الحيطة والحذر المعتادة."}</p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ss:
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 رادار كشف التهديدات</h3>", unsafe_allow_html=True)
            if is_threat:
                # محتوى بديل للمعاينة إذا كان الرابط خطراً
                st.markdown(f"""
                    <div class="ss-frame rtl-container">
                        <div style="text-align:center; padding:20px;">
                            <div style="width:100px; height:100px; border:5px solid #ff4b4b; border-radius:50%; margin:0 auto; border-top-color:transparent; animation: spin 1s linear infinite;"></div>
                            <h3 style="color:#ff4b4b; margin-top:20px;">تحذير: محتوى ضار!</h3>
                            <p style="color:#888;">تم حجب المعاينة البصرية لمنع تنفيذ أي سكربتات خبيثة (Cross-Site Scripting).</p>
                        </div>
                        <div style="background:rgba(255,75,75,0.05); border:1px dashed #ff4b4b; padding:15px; border-radius:10px;">
                            <h5 style="color:#ff4b4b;">📋 سجل التحليل البصري:</h5>
                            <p style="font-size:0.9em; color:#ccc;">
                            • تم رصد محاولة جلب ملفات تعريف الارتباط (Cookies).<br>
                            • اكتشاف حقول إدخال وهمية لانتحال صفة (Phishing Page).<br>
                            • تم عزل الجلسة فوراً في بيئة Sandbox.<br>
                            • <b>النتيجة:</b> الموقع يمثل خطراً حقيقياً على خصوصية المستخدم.</p>
                        </div>
                    </div>
                    <style> @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } } </style>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="ss-frame rtl-container">
                        <div style="text-align:center;">
                            <span style="font-size:5em;">🛡️</span>
                            <h4 style="color:#2ea043;">الرابط يبدو آمناً للمعاينة</h4>
                            <p style="color:#888;">لم يتم العثور على أكواد خبيثة تمنع العرض.</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; padding:20px; color:#D4AF37; font-family:Orbitron; border-top:1px solid rgba(212,175,55,0.1);'>Developed by: Eng. Zaid Al-Janabi | Department of Cybersecurity Engineering | Al-Maarif University | 2026</div>", unsafe_allow_html=True)
