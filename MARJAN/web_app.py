import streamlit as st
import requests
import base64
import re
import math
from urllib.parse import urlparse

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace v2.5", page_icon="🛡️", layout="wide")

# --- محرك التحليل الجنائي المتقدم ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

def analyze_payload_behavior(url, alerts):
    behavior = []
    if "login" in url or "verify" in url or "bank" in url:
        behavior.append("🎯 محاولة سرقة بيانات الاعتماد (Credential Phishing)")
    if "wix" in url or "studio" in url or "redirect" in url:
        behavior.append("🔗 استخدام منصات وسيطة لتجاوز الحماية (Bypassing Gateways)")
    if len(alerts) > 1:
        behavior.append("🛡️ محاولة حقن ملفات تعريف ارتباط مشبوهة (Session Hijacking)")
    return behavior

def get_forensic_status(hits, alerts, entropy):
    if hits > 0 or len(alerts) >= 2 or entropy > 3.9:
        return "CRITICAL THREAT / تهديد خطير", "#ff4b4b"
    elif len(alerts) == 1 or entropy > 3.5:
        return "SUSPICIOUS / نشاط مشبوه", "#ffa500"
    else:
        return "CLEAN / نظام آمن", "#2ea043"

# --- التنسيق البصري (Cyber Dashboard) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500&display=swap');
    .main { background-color: #05070a; color: #e2e8f0; }
    .sys-title { font-family: 'Cairo', sans-serif; color: #D4AF37 !important; text-align: center; font-size: 2.3em; font-weight: bold; }
    .eng-sub { font-family: 'Orbitron', sans-serif; color: #888; text-align: center; font-size: 0.8em; letter-spacing: 2px; }
    .metric-card { background: #0d1117; border: 1px solid #30363d; border-top: 3px solid #D4AF37; padding: 20px; border-radius: 10px; text-align: center; }
    .report-box { background: #0d1117; border-radius: 15px; padding: 25px; border: 1px solid #30363d; margin-top: 20px; direction: rtl; text-align: right; }
    .screenshot-frame { border: 2px solid #D4AF37; border-radius: 10px; overflow: hidden; background: #000; min-height: 300px; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background: #0d1117; color: #D4AF37; text-align: center; padding: 10px; border-top: 1px solid #D4AF37; font-family: 'Orbitron', sans-serif; font-size: 0.85em; }
    .stButton>button { background: #D4AF37 !important; color: black !important; font-family: 'Cairo', sans-serif; font-weight: bold; width: 100%; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='sys-title'>🛡️ نظام مَرْجَان لِلتحقيقِ الرَّقَمي</h1>", unsafe_allow_html=True)
st.markdown("<p class='eng-sub'>MARJAN TRACE v2.5: AGGRESSIVE DETECTION MODE</p>", unsafe_allow_html=True)

target_url = st.text_input("Target URL / رابط الهدف", placeholder="example.com")

if st.button("تفعيل بروتوكول الكشف الشامل"):
    if target_url:
        if not target_url.startswith("http"): target_url = "https://" + target_url
        domain = urlparse(target_url).netloc
        
        with st.spinner("Executing Deep Analysis..."):
            # 1. التحليل السلوكي المحلي (صارم جداً)
            alerts = []
            entropy = get_entropy(domain)
            
            # كشف التخفي وراء المنصات (مثل Wix المستخدم في الرابط الخبيث)
            if "wix" in domain or "studio" in domain:
                alerts.append("⚠️ استغلال منصات استضافة: الرابط يستخدم بيئة استضافة سحابية لإخفاء الهوية الجنائية.")
            
            phish_patterns = [r'login', r'verify', r'sign', r'account', r'secure', r'update', r'billing', r'en-', r'vendas']
            if any(re.search(p, target_url.lower()) for p in phish_patterns):
                alerts.append("🚨 أنماط تصيد نشطة: تم رصد هيكلية رابط مطابقة لهجمات الهندسة الاجتماعية.")
            
            if entropy > 3.6:
                alerts.append(f"🕵️ تحليل عشوائية (Entropy: {round(entropy,2)}): النطاق يظهر سلوك توليد آلي (DGA) مرتفع.")

            # 2. الاستخبارات الخارجية (VirusTotal)
            vt_hits = 0
            API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
            u_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
            try:
                res = requests.get(f"https://www.virustotal.com/api/v3/urls/{u_id}", headers={"x-apikey": API_KEY}, timeout=10)
                if res.status_code == 200:
                    vt_hits = res.json()['data']['attributes']['last_analysis_stats']['malicious']
            except: pass

            status_label, status_color = get_forensic_status(vt_hits, alerts, entropy)
            behaviors = analyze_payload_behavior(target_url, alerts)

            # --- النتائج ---
            st.markdown("### 📊 نتائج الفحص الاستخباراتي")
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h5>الحالة الجنائية</h5><h3 style="color:{status_color};">{status_label}</h3></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h5>بلاغات التهديد</h5><h2>{vt_hits}</h2></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h5>معامل العشوائية</h5><h2>{round(entropy, 2)}</h2></div>', unsafe_allow_html=True)

            col_res, col_ss = st.columns([1.2, 1])
            
            with col_res:
                st.markdown('<div class="report-box">', unsafe_allow_html=True)
                st.markdown("<h3 style='color:#D4AF37; margin-top:0;'>🔍 تقرير التحليل الجنائي</h3>", unsafe_allow_html=True)
                st.write(f"**الهدف:** `{target_url}`")
                st.markdown("---")
                
                for a in alerts: st.markdown(f"<p style='color:#ff4b4b; font-weight:bold;'>• {a}</p>", unsafe_allow_html=True)
                
                if behaviors:
                    st.markdown("<h4 style='color:#D4AF37;'>⚠️ تحليل السلوك المتوقع (Payload Analysis):</h4>", unsafe_allow_html=True)
                    for b in behaviors: st.markdown(f"<p style='color:#ffa500;'>- {b}</p>", unsafe_allow_html=True)

                st.markdown(f"""
                <div style="background:rgba(212,175,55,0.05); border:1px solid #D4AF37; padding:15px; border-radius:10px; margin-top:20px;">
                    <h4 style="color:#D4AF37; margin-top:0;">💡 توصية نظام مَرْجَان (Marjan Advisory):</h4>
                    <p>الرابط تم تصنيفه كـ <b>{status_label}</b> بناءً على تحليل الأنماط السلوكية. يمنع التعامل معه نهائياً.</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_ss:
                st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 معاينة Sandbox آمنة</h3>", unsafe_allow_html=True)
                ss_url = f"https://api.screenshotmachine.com?key=6943e8&url={target_url}&dimension=1024x768"
                st.markdown(f'<div class="screenshot-frame"><img src="{ss_url}" width="100%"></div>', unsafe_allow_html=True)
                st.markdown("<p style='color:#888; font-size:0.8em; text-align:center; margin-top:8px;'>تنبيه: يتم التقاط الصورة في بيئة معزولة تقنياً.</p>", unsafe_allow_html=True)

st.markdown(f'<div class="footer">Developed by: Eng. Zaid Al-Janabi | Marjan Trace v2.5 | Al-Maarif University</div>', unsafe_allow_html=True)
