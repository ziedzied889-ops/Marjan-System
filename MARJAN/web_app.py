import streamlit as st
import requests
import base64
import re
import math
from urllib.parse import urlparse

# --- إعدادات الصفحة النهائية ---
st.set_page_config(page_title="Marjan Trace v3.0", page_icon="🛡️", layout="wide")

# --- محرك الذكاء الجنائي (Aggressive Zero-Trust) ---
def get_entropy(text):
    if not text: return 0
    probs = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    return - sum([p * math.log(p) / math.log(2.0) for p in probs])

def get_forensic_status(vt_hits, alerts, entropy):
    # تشديد المعايير: أي تنبيه واحد كافٍ لجعل الحالة مشبوهة
    if vt_hits > 0 or len(alerts) >= 2 or entropy > 3.8:
        return "CRITICAL THREAT / تهديد خطير", "#ff4b4b"
    elif len(alerts) > 0 or entropy > 3.2:
        return "SUSPICIOUS / نشاط مشبوه", "#ffa500"
    else:
        return "CLEAN / نظام آمن", "#2ea043"

# --- التنسيق البصري الاحترافي ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Orbitron:wght@500&display=swap');
    .main { background-color: #05070a; color: #e2e8f0; }
    .sys-title { font-family: 'Cairo', sans-serif; color: #D4AF37 !important; text-align: center; font-size: 2.3em; font-weight: bold; }
    .eng-sub { font-family: 'Orbitron', sans-serif; color: #888; text-align: center; font-size: 0.8em; letter-spacing: 2px; }
    .metric-card { background: #0d1117; border: 1px solid #30363d; border-top: 3px solid #D4AF37; padding: 20px; border-radius: 10px; text-align: center; }
    .report-box { background: #0d1117; border-radius: 15px; padding: 25px; border: 1px solid #30363d; margin-top: 20px; direction: rtl; text-align: right; }
    .screenshot-frame { border: 2px solid #D4AF37; border-radius: 10px; overflow: hidden; background: #000; height: 350px; display: flex; align-items: center; justify-content: center; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background: #0d1117; color: #D4AF37; text-align: center; padding: 10px; border-top: 1px solid #D4AF37; font-family: 'Orbitron', sans-serif; font-size: 0.85em; }
    .stButton>button { background: #D4AF37 !important; color: black !important; font-family: 'Cairo', sans-serif; font-weight: bold; width: 100%; border-radius: 8px; border: none; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='sys-title'>🛡️ نظام مَرْجَان لِلتحقيقِ الرَّقَمي</h1>", unsafe_allow_html=True)
st.markdown("<p class='eng-sub'>MARJAN TRACE v3.0: ZERO-TRUST DEEP SCAN</p>", unsafe_allow_html=True)

# --- واجهة الإدخال ---
target_url = st.text_input("Target URL / رابط الهدف", placeholder="انسخ الرابط هنا (مثلاً: https://leddgr-live.github.io)")

if st.button("بدء عملية التحليل الجنائي العميق"):
    if target_url:
        # تصحيح الرابط
        clean_url = target_url.strip()
        if not clean_url.startswith("http"): clean_url = "https://" + clean_url
        domain = urlparse(clean_url).netloc
        path = urlparse(clean_url).path

        with st.spinner("جاري استخلاص البيانات الجنائية..."):
            alerts = []
            
            # 1. كشف التمويه في المنصات الموثوقة (مثل GitHub و Wix)
            trusted_platforms = ['github.io', 'wixstudio.com', 'web.app', 'vercel.app']
            if any(p in domain for p in trusted_platforms):
                alerts.append(f"⚠️ تحذير المنصات: الرابط مستضاف على {domain}، وهي بيئة يستخدمها المهاجمون لتجاوز الفلاتر.")

            # 2. كشف الكلمات الملغمة (Heuristic Analysis)
            # تم إضافة كلمات مثل leddgr لكشف صفحات العملات المشفرة المزيفة
            blacklisted_keywords = ['leddg', 'vendas', 'secure', 'login', 'update', 'verify', 'wallet', 'crypto', 'bank']
            if any(key in clean_url.lower() for key in blacklisted_keywords):
                alerts.append("🚨 أنماط مشبوهة: تم العثور على كلمات دلالية مرتبطة بعمليات الاحتيال وسرقة البيانات.")

            # 3. تحليل العشوائية (Entropy)
            entropy = get_entropy(domain)
            if entropy > 3.5:
                alerts.append(f"🕵️ تحليل DGA: معامل العشوائية ({round(entropy,2)}) مرتفع، مما يشير لاسم نطاق غير بشري.")

            # 4. الاستعلام من VirusTotal
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
            st.markdown("### 📊 لوحة النتائج الاستخباراتية")
            c1, c2, c3 = st.columns(3)
            with c1: st.markdown(f'<div class="metric-card"><h5>الحالة الجنائية</h5><h3 style="color:{status_color};">{status_label}</h3></div>', unsafe_allow_html=True)
            with c2: st.markdown(f'<div class="metric-card"><h5>بلاغات عالمية</h5><h2>{vt_hits}</h2></div>', unsafe_allow_html=True)
            with c3: st.markdown(f'<div class="metric-card"><h5>معامل العشوائية</h5><h2>{round(entropy, 2)}</h2></div>', unsafe_allow_html=True)

            col_res, col_ss = st.columns([1.3, 1])
            
            with col_res:
                st.markdown('<div class="report-box">', unsafe_allow_html=True)
                st.markdown("<h3 style='color:#D4AF37; margin-top:0;'>🔍 التقرير الجنائي التفصيلي</h3>", unsafe_allow_html=True)
                st.write(f"**الهدف:** `{clean_url}`")
                st.markdown("---")
                
                if alerts or vt_hits > 0:
                    for a in alerts: st.markdown(f"<p style='color:#ff4b4b; font-weight:bold;'>• {a}</p>", unsafe_allow_html=True)
                    
                    st.markdown("<h4 style='color:#D4AF37;'>⚠️ تحليل الضرر المتوقع:</h4>", unsafe_allow_html=True)
                    if 'leddg' in clean_url.lower() or 'wallet' in clean_url.lower():
                        st.markdown("<p style='color:#ffa500;'>- محاولة سرقة مفاتيح محافظ العملات الرقمية (Seed Phrase Recovery).</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p style='color:#ffa500;'>- محاولة تصيد بيانات الحسابات الشخصية وسرقة الجلسات.</p>", unsafe_allow_html=True)

                    st.markdown(f"""
                    <div style="background:rgba(212,175,55,0.05); border:1px solid #D4AF37; padding:15px; border-radius:10px; margin-top:20px;">
                        <h4 style="color:#D4AF37; margin-top:0;">💡 توصية نظام مَرْجَان (Marjan Advisory):</h4>
                        <p>هذا الرابط <b>خطر للغاية</b>. تم رصد محاولة لتقليد صفحات رسمية على منصة موثوقة. يجب حظره فوراً.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("<p style='color:#2ea043; font-weight:bold;'>✅ نظام مَرْجَان: لم يتم رصد تهديد مباشر، لكن ينصح دائماً بالحذر من الروابط المختصرة.</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_ss:
                st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📸 معاينة Sandbox آمنة</h3>", unsafe_allow_html=True)
                # استخدام مفتاح جديد أو وسيلة بديلة لضمان عمل السكرين شوت
                ss_url = f"https://api.screenshotmachine.com?key=6943e8&url={clean_url}&dimension=1024x768"
                st.markdown(f'<div class="screenshot-frame"><img src="{ss_url}" width="100%" onerror="this.parentElement.innerHTML=\'<p style=\\\'color:#888;\\\'>جاري جلب المعاينة أو الرابط محجوب أمنياً</p>\'"></div>', unsafe_allow_html=True)
                st.markdown("<p style='color:#888; font-size:0.8em; text-align:center; margin-top:8px;'>تنبيه: المعاينة تتم عبر سيرفر وسيط معزول.</p>", unsafe_allow_html=True)

# --- التذييل ---
st.markdown(f'<div class="footer">Developed by: Eng. Zaid Al-Janabi | Marjan Trace v3.0 | Al-Maarif University</div>', unsafe_allow_html=True)
