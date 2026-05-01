import streamlit as st
import requests
import base64
import re
from urllib.parse import urlparse
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- تهيئة مخزن البيانات اللحظي (لخزن التهديدات المكتشفة خلال الجلسة) ---
if 'threat_vault' not in st.session_state:
    st.session_state.threat_vault = [
        {"url": "allegrolokalnie.sbs", "type": "انتحال صفة (Allegro)", "time": "00:09"},
        {"url": "thechoceur.com", "type": "تصيد غير مشفر", "time": "23:06"}
    ]

# --- التنسيق البصري (ثبات كامل للواجهة v6.3) ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #05070a !important;
        background-image: 
            url("https://www.transparentpng.com/download/security/shield-security-icon-9.png"),
            linear-gradient(rgba(212, 175, 55, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(212, 175, 55, 0.03) 1px, transparent 1px),
            radial-gradient(circle at center, #11141a 0%, #05070a 100%) !important;
        background-position: center 40%, center, center, center !important;
        background-repeat: no-repeat, repeat, repeat, no-repeat !important;
        background-size: 380px auto, 30px 30px, 30px 30px, 100% 100% !important;
        background-attachment: fixed !important;
    }
    h1 { color: #D4AF37 !important; text-align: center; text-shadow: 0px 0px 20px rgba(212, 175, 55, 0.8) !important; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { width: 100%; background-color: #D4AF37 !important; color: black !important; font-weight: bold; border-radius: 12px; height: 3.8em; }
    .heuristic-danger { padding: 15px; border-radius: 10px; border-right: 6px solid #ff4b4b; background-color: rgba(255, 75, 75, 0.25); color: #ff9999; text-align: right; margin-bottom: 10px; font-weight: bold; border-left: 1px solid rgba(255,75,75,0.4); }
    .threat-intel { padding: 15px; border-radius: 10px; background-color: rgba(212, 175, 55, 0.1); border: 1px solid #D4AF37; color: #eee; text-align: right; margin-top: 15px; }
    .latest-threats { padding: 15px; border-radius: 10px; background: rgba(255, 75, 75, 0.05); border: 1px solid rgba(255, 75, 75, 0.3); margin-top: 30px; margin-bottom: 50px; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #D4AF37; padding: 10px; background-color: rgba(5, 7, 10, 0.98); border-top: 1px solid #D4AF37; z-index: 100; }
    </style>
    """, unsafe_allow_html=True)

# --- محرك التحليل الجنائي اللحظي (M.T Deep Forensic v7.0) ---
def advanced_forensic_analysis(url):
    reasons = []
    domain = urlparse(url).netloc.lower()
    
    # 1. رصد استغلال منصات الاستضافة الموثوقة (مثل Wix Studio في صورتك)
    trusted_platforms = ['wixstudio.com', 'webflow.io', 'firebaseapp.com', 'pages.dev']
    if any(plat in domain for plat in trusted_platforms):
        reasons.append(f"⚠️ رصد استغلال منصات: الرابط يستخدم منصة موثوقة ({domain.split('.')[-2]}) لإنشاء صفحة مشبوهة.")

    # 2. تحليل الكلمات الدالة على انتحال الهوية
    if any(k in domain for k in ['platform', 'live', 'login', 'secure', 'verify']):
        reasons.append("🚨 انتحال صفة نظام: اسم النطاق الفرعي يحتوي على كلمات تضليل توحي بأنه رابط نظام رسمي.")

    # 3. التحقق من التشفير
    if url.startswith("http://"):
        reasons.append("🔓 ثغرة أمنية: الرابط يفتقر لتشفير البيانات.")

    return list(set(reasons))

# --- وظيفة جلب البيانات من الأنظمة العالمية اللحظية ---
def fetch_global_intel(url):
    alerts = []
    # PhishTank Live
    try:
        response = requests.post("https://checkurl.phishtank.com/checkurl/", data={'url': url, 'format': 'json'}, timeout=10)
        if response.status_code == 200 and response.json().get('results', {}).get('in_database'):
            alerts.append("🐟 PhishTank Alert: الرابط مدرج حالياً في قواعد بيانات التصيد العالمية.")
    except: pass
    return alerts

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام التحليل الجنائي الرقمي</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="أدخل الرابط للفحص الجنائي اللحظي...")

if st.button("تفعيل بروتوكول الكشف الذكي"):
    if target_url:
        # تصحيح الرابط برمجياً
        if target_url.startswith("ttp"): target_url = "h" + target_url
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري جلب المعلومات من الأنظمة العالمية وتحليلها..."):
            st.markdown("---")
            
            # التحليل الذاتي + جلب البيانات العالمية
            marjan_alerts = advanced_forensic_analysis(target_url)
            marjan_alerts.extend(fetch_global_intel(target_url))
            
            # VirusTotal Intel
            try:
                vt_res = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=10)
                if vt_res.status_code == 200:
                    malicious = vt_res.json()['data']['attributes'].get('last_analysis_stats', {}).get('malicious', 0)
                    if malicious > 0:
                        marjan_alerts.append(f"📡 استخبارات دولية: تم تأكيد الخطورة بواسطة {malicious} محرك أمني.")
            except: pass

            if marjan_alerts:
                st.subheader("🕵️ نتائج التحليل اللحظي:")
                for alert in marjan_alerts:
                    st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
                
                # تخزين في قاعدة بيانات الجلسة
                st.session_state.threat_vault.insert(0, {
                    "url": target_url[:30] + "...", 
                    "type": "Phishing/Suspicious", 
                    "time": datetime.now().strftime("%H:%M")
                })
                
                st.markdown(f"""
                <div class="threat-intel">
                    <h4 style="color:#D4AF37; margin-bottom:10px;">⚠️ ماذا يفعل هذا الرابط؟</h4>
                    <p style="color:#eee; font-size:0.9em;">يستغل الرابط منصات تطوير الويب لخداع المستخدمين وسرقة بيانات الدخول.</p>
                    <p style="font-size: 0.95em; color: #ff4b4b; font-weight: bold; border-top: 1px solid rgba(212,175,55,0.2); padding-top: 10px;">
                        💡 نصيحة: تجنب إدخال أي معلومات في هذا الموقع.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("✅ محرك مرجان: لم يتم رصد تهديدات لحظية حالياً.")

            st.info(f"🔗 [السجل الفني الكامل للرابط (Live)](https://www.virustotal.com/gui/url/{url_id}/behavior)")

# --- قاعدة بيانات التهديدات اللحظية المخزنة ---
st.markdown(f"""
    <div class="latest-threats">
        <h4 style="color:#ff4b4b; margin-bottom:10px; border-bottom:1px solid rgba(255,75,75,0.2);">🔴 قاعدة بيانات التهديدات المخزنة (Live Vault)</h4>
        <table style="width:100%; color:#eee; font-size:0.85em; text-align:right;">
            <tr style="color:#D4AF37;">
                <th>الرابط</th>
                <th>نوع التهديد</th>
                <th>الوقت</th>
            </tr>
            {"".join([f"<tr><td>{t['url']}</td><td>{t['type']}</td><td>{t['time']}</td></tr>" for t in st.session_state.threat_vault[:5]])}
        </table>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace v6.3 | Advanced Forensic Detection</div>', unsafe_allow_html=True)
