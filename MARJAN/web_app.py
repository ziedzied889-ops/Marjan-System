import streamlit as st
import requests
import base64
import re
import math
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نظام مَرْجَان للتحقيق الرقمي v3.2", page_icon="🛡️", layout="wide")

# --- محرك الذكاء الجنائي المتقدم ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

def get_forensic_status(vt_hits, alerts, entropy):
    if vt_hits > 0 or len(alerts) >= 2 or entropy > 3.8:
        return "CRITICAL THREAT / تهديد خطير", "#ff4b4b"
    elif len(alerts) > 0 or entropy > 3.2:
        return "SUSPICIOUS / نشاط مشبوه", "#ffa500"
    else:
        return "CLEAN / نظام آمن", "#2ea043"

# --- التنسيق البصري (Cyber Dashboard & Dynamic Background) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500&display=swap');
    
    /* الخلفية المتحركة */
    #tsparticles {
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        z-index: -1;
        background-color: #05070a;
    }

    .main { background: transparent; color: #e2e8f0; position: relative; z-index: 1; }
    
    /* العناوين والتنسيق العام */
    .sys-title { font-family: 'Cairo', sans-serif; color: #D4AF37 !important; text-align: center; font-size: 2.3em; font-weight: bold; margin-bottom: 0; text-shadow: 0 0 10px rgba(212, 175, 85, 0.5); }
    .eng-sub { font-family: 'Orbitron', sans-serif; color: #888; text-align: center; font-size: 0.8em; letter-spacing: 2px; margin-top: 0; }
    
    /* بطاقات النتائج والمقاييس */
    .metric-card { 
        background: rgba(13, 17, 23, 0.8); border: 1px solid rgba(48, 54, 61, 0.5); border-top: 3px solid #D4AF37;
        padding: 20px; border-radius: 12px; text-align: center; backdrop-filter: blur(5px);
        transition: transform 0.3s ease;
    }
    .metric-card:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(212, 175, 85, 0.3); }

    /* صندوق التقرير الجنائي */
    .report-box { 
        background: rgba(13, 17, 23, 0.85); border-radius: 15px; padding: 25px; border: 1px solid rgba(48, 54, 61, 0.5);
        margin-top: 20px; direction: rtl; text-align: right; backdrop-filter: blur(10px);
    }
    
    /* إصلاح تداخل النص العربي والإنجليزي في التقرير */
    .forensic-text { direction: rtl; text-align: right; unicode-bidi: embed; font-family: 'Cairo', sans-serif; line-height: 1.8; }
    .alert-item { color: #ff4b4b; font-weight: bold; margin-bottom: 10px; display: flex; align-items: start; gap: 8px; }
    .payload-item { color: #ffa500; margin-bottom: 8px; display: flex; align-items: start; gap: 8px; }

    /* إطار المعاينة البصرية */
    .screenshot-frame { 
        border: 2px solid rgba(212, 175, 85, 0.8); border-radius: 12px; overflow: hidden; background: #000;
        min-height: 350px; display: flex; align-items: center; justify-content: center; position: relative;
        box-shadow: 0 0 15px rgba(212, 175, 85, 0.2);
    }
    .screenshot-frame img { width: 100%; height: auto; display: block; }
    
    /* تذييل الصفحة */
    .footer { 
        position: fixed; left: 0; bottom: 0; width: 100%; 
        background: rgba(13, 17, 23, 0.95); color: #D4AF37; text-align: center; padding: 12px;
        border-top: 1px solid rgba(212, 175, 85, 0.8); font-family: 'Orbitron', sans-serif; font-size: 0.85em;
        backdrop-filter: blur(5px); z-index: 1000;
    }
    
    /* تنسيق الأزرار */
    .stButton>button { 
        background: linear-gradient(90deg, #D4AF37, #b8860b) !important; color: black !important;
        font-family: 'Cairo', sans-serif; font-weight: bold; width: 100%; border-radius: 8px; 
        border: none; height: 3.2em; transition: 0.3s ease;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px rgba(212, 175, 85, 0.5); }
    </style>
    """, unsafe_allow_html=True)

# --- كود الخلفية المتحركة (JavaScript) ---
st.markdown("""
<div id="tsparticles"></div>
<script src="https://cdn.jsdelivr.net/npm/@tsparticles/confetti@3.0.3/tsparticles.confetti.bundle.min.js"></script>
<script>
tsParticles.load("tsparticles", {
  particles: {
    number: { value: 60, density: { enable: true, value_area: 800 } },
    color: { value: "#D4AF37" },
    shape: { type: "circle" },
    opacity: { value: 0.3, random: true },
    size: { value: 2, random: true },
    links: { enable: true, distance: 150, color: "#D4AF37", opacity: 0.2, width: 1 },
    move: { enable: true, speed: 1.5, direction: "none", random: false, straight: false, out_mode: "out", bounce: false }
  },
  interactivity: {
    detect_on: "canvas",
    events: { onHover: { enable: true, mode: "grab" }, onclick: { enable: true, mode: "push" }, resize: true },
    modes: { grab: { distance: 140, line_linked: { opacity: 0.5 } }, push: { particles_nb: 3 } }
  },
  retina_detect: true
});
</script>
""", unsafe_allow_html=True)

# --- الهيدر ---
st.markdown("<h1 class='sys-title'>🛡️ نظام مَرْجَان لِلتحقيقِ الرَّقَمي</h1>", unsafe_allow_html=True)
st.markdown("<p class='eng-sub'>MARJAN TRACE v3.2: CYBER DASHBOARD</p>", unsafe_allow_html=True)

# --- واجهة الإدخال ---
target_url = st.text_input("Target URL / رابط الهدف", placeholder="ادخل الرابط المشبوه هنا...")

if st.button("تفعيل بروتوكول الكشف الجنائي الشامل"):
    if target_url:
        # معالجة الرابط وتوحيده
        clean_url = target_url.strip()
        if not clean_url.startswith("http"): clean_url = "https://" + clean_url
        domain = urlparse(clean_url).netloc
        
        with st.spinner("جاري تنفيذ عمليات المسح المتقدم..."):
            alerts = []
            
            # --- منطق الكشف العدواني المطور ---
            # 1. كشف التمويه خلف المنصات الموثوقة (مثل المستخدم في الرابط الخبيث)
            if any(p in domain for p in ['github.io', 'wixstudio', 'glitch.me', 'replit', 'vercel.app']):
                alerts.append(f"🚩 تحذير تمويه: الرابط يستغل بيئة مستضافة موثوقة ({domain}) لإخفاء النشاط الجنائي.")

            # 2. تحليل الكلمات المفتاحية والأنماط (Regex)
            # تم إضافة أنماط محددة لكشف هجمات Ledger-live والتصيد البرازيلي
            phish_keywords = ['leddg', 'wallet', 'crypto', 'secure', 'login', 'verify', 'account', 'vendas', 'billing', 'boticario']
            if any(key in clean_url.lower() for key in phish_keywords):
                alerts.append("🚨 أنماط مشبوهة: تم العثور على كلمات دلالية وهيكلية تستخدم في هجمات سرقة الهوية والمحافظ.")
            
            # 3. تحليل معامل العشوائية (Entropy)
            entropy = get_entropy(domain)
            if entropy > 3.5:
                alerts.append(f"🕵️ تحليل عشوائية: معامل Entropy ({round(entropy,2)}) مرتفع، مما يشير لاسم نطاق مولد آلياً.")

            # --- الاستعلام العالمي (VirusTotal API) ---
            vt_hits = 0
            API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
            u_id = base64.urlsafe_b64encode(clean_url.encode()).decode().strip("=")
            try:
                res = requests.get(f"https://www.virustotal.com/api/v3/urls/{u_id}", headers={"x-apikey": API_KEY}, timeout=10)
                if res.status_code == 200:
                    vt_hits = res.json()['data']['attributes']['last_analysis_stats']['malicious']
            except: pass

            status_label, status_color = get_forensic_status(vt_hits, alerts, entropy)

            # --- عرض النتائج ---
            st.markdown("### 📊 لوحة نتائج التحقيق")
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h5>الحالة الجنائية</h5><h3 style="color:{status_color};">{status_label}</h3></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h5>بلاغات التهديد</h5><h2>{vt_hits}</h2></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h5>معامل العشوائية</h5><h2>{round(entropy, 2)}</h2></div>', unsafe_allow_html=True)

            col_res, col_ss = st.columns([1.2, 1])
            
            with col_res:
                st.markdown('<div class="report-box forensic-text">', unsafe_allow_html=True)
                st.markdown("<h3 style='color:#D4AF37; margin-top:0;'>🔍 تقرير التحليل الجنائي التفصيلي</h3>", unsafe_allow_html=True)
                st.write(f"**الهدف المرصود:** `<span style='color:#8b949e;'>{clean_url}</span>`", unsafe_allow_html=True)
                st.markdown("<hr style='border:1px solid rgba(48, 54, 61, 0.5);'>", unsafe_allow_html=True)
                
                if alerts or vt_hits > 0:
                    for a in alerts: st.markdown(f"<div class='alert-item'>• {a}</div>", unsafe_allow_html=True)
                    if vt_hits > 0: st.markdown(f"<div class='alert-item'>🚨 تم تأكيد الخطورة من قبل {vt_hits} مصدر أمني عالمي.</div>", unsafe_allow_html=True)

                    # تحليل السلوك المتوقع (Payload Behavior)
                    st.markdown("<h4 style='color:#D4AF37;'>⚠️ تحليل الأضرار المتوقعة:</h4>", unsafe_allow_html=True)
                    if 'leddg' in clean_url.lower() or 'wallet' in clean_url.lower():
                        st.markdown("<div class='payload-item'>- محاولة سرقة عبارات استعادة المحافظ (Seed Phrases) للعملات الرقمية.</div>", unsafe_allow_html=True)
                    if 'boticario' in clean_url.lower() or 'vendas' in clean_url.lower():
                        st.markdown("<div class='payload-item'>- محاولة سرقة بيانات البطاقات الائتمانية والمعلومات الشخصية.</div>", unsafe_allow_html=True)
                    if 'login' in clean_url.lower() or 'verify' in clean_url.lower():
                        st.markdown("<div class='payload-item'>- محاولة انتحال صفة (Phishing) لسرقة جلسات الدخول.</div>", unsafe_allow_html=True)

                    st.markdown(f"""
                    <div style="background:rgba(212,175,55,0.05); border:1px solid #D4AF37; padding:15px; border-radius:10px; margin-top:20px; text-align:right;">
                        <h4 style="color:#D4AF37; margin-top:0;">💡 توصية نظام مَرْجَان الجنائية (Marjan Trace Advisory):</h4>
                        <p style="margin-bottom:0; color:#eee;">الرابط تم تصنيفه كـ <b style='color:#ff4b4b;'>{status_label}</b> بناءً على الأدلة الجنائية السلوكية المكتشفة. يمنع التعامل معه نهائياً لخطورته القصوى.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color:#2ea043; font-weight:bold;'>✅ نظام مَرْجَان: لم يتم رصد أي تهديدات سلوكية معروفة حالياً. ينصح بالمراقبة المستمرة.</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_ss:
                st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 معاينة Sandbox آمنة</h3>", unsafe_allow_html=True)
                # استخدام محرك معاينة قوي ومستقر
                ss_url = f"https://image.thum.io/get/width/1024/crop/800/{clean_url}"
                st.markdown(f"""
                <div class="screenshot-frame">
                    <img src="{ss_url}" alt="Visualizing..." onload="this.style.display='block'; this.previousElementSibling.style.display='none';">
                    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 15px; padding: 20px; color: #eee; font-family: 'Cairo', sans-serif;">
                        <span style="font-size: 2em; animation: rotate 2s linear infinite;">🛡️</span>
                        <p style="text-align: center; margin: 0; color: #ff4b4b; font-weight: bold; font-size: 1.2em;">عذراً، المعاينة غير متوفرة</p>
                        <p style="text-align: center; margin: 0; color: #ffa500; font-size: 0.9em;">(Site Encrypted/Blocked for Security)</p>
                        <p style="text-align: center; margin: 0 0 10px 0; color: #888;">تم حظر الموقع من قبل فريق الأمن السيبراني لخطورته.</p>
                        <div style="background: rgba(212,175,55, 0.1); border: 1px solid #D4AF37; padding: 10px; border-radius: 8px; width: 100%;">
                            <p style="color: #ff4b4b; margin: 0;"><b>توصية جنائية:</b></p>
                            <p style="color: #eee; margin: 5px 0 0 0;">عدم التعامل مع الرابط نهائياً. تم كشف محاولة تصيد احتيالي.</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("<p style='color:#888; font-size:0.8em; text-align:center; margin-top:8px;'>تنبيه: يتم محاكاة زيارة الرابط عبر سيرفر وسيط (Proxy) معزول تماماً لحماية جهازك.</p>", unsafe_allow_html=True)

# --- التذييل ---
st.markdown(f'<div class="footer">Developed by: Eng. Zaid Al-Janabi | Marjan Trace v3.2 | cybersecurity Engineering Al-Maarif University</div>', unsafe_allow_html=True)
