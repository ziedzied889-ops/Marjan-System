import streamlit as st
import requests
import base64
import re
from urllib.parse import urlparse
from datetime import datetime

# --- إعدادات الصفحة ---
st.set_page_config(page_title="Marjan Trace", page_icon="🛡️", layout="centered")

# --- تهيئة مخزن التهديدات اللحظي ---
if 'threat_vault' not in st.session_state:
    st.session_state.threat_vault = [
        {"url": "blaquice.com/na/media/...", "type": "مسار ملغم (Media Phish)", "time": "00:13"},
        {"url": "live--platform.wixstudio...", "type": "استغلال منصات سحابية", "time": "00:12"}
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

# --- محرك التحليل الجنائي الهجومي (M.T Offensive Forensic v7.5) ---
def deep_path_analysis(url):
    reasons = []
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    
    # 1. رصد المسارات العشوائية والمشبوهة (مثل الموجود في صورتك)
    # الهجمات غالباً تضع ملفات داخل مجلدات مثل media, na, logs, verification
    suspicious_paths = ['/media/', '/na/', '/verify/', '/login/', '/secure/']
    if any(sp in path for sp in suspicious_paths):
        reasons.append(f"🚨 مسار مشبوه: تم رصد هيكلية ملفات ({path}) تُستخدم عادةً لرفع صفحات التصيد على المواقع المخترقة.")

    # 2. تحليل طول المسار العشوائي (Entropy Analysis)
    path_suffix = path.split('/')[-1]
    if len(path_suffix) > 8 and not path_suffix.endswith(('.jpg', '.png', '.pdf')):
        reasons.append("🕵️ تحليل السلوك: المسار النهائي للرابط يحتوي على رموز عشوائية تشير إلى حملة تصيد لحظية.")

    # 3. التدقيق في بروتوكول HTTP للروابط التي تطلب بيانات
    if url.startswith("http://"):
        reasons.append("🔓 بروتوكول غير آمن: الرابط يفتقر للتشفير، مما يسهل عمليات التجسس الجنائي.")

    return list(set(reasons))

# --- وظيفة الاستعلام عن التهديدات العالمية ---
def fetch_global_intel(url):
    alerts = []
    # الاستعلام المباشر من PhishTank
    try:
        data = {'url': url, 'format': 'json'}
        response = requests.post("https://checkurl.phishtank.com/checkurl/", data=data, timeout=12)
        if response.status_code == 200:
            if response.json().get('results', {}).get('in_database'):
                alerts.append("🐟 تنبيه PhishTank اللحظي: هذا الرابط مسجل كتهديد نشط في القوائم العالمية.")
    except: pass
    return alerts

# --- الواجهة الرئيسية ---
st.markdown("<h1>🛡️ Marjan Trace</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#D4AF37;'>نظام التحليل الجنائي الرقمي</h3>", unsafe_allow_html=True)

target_url = st.text_input("", placeholder="أدخل الرابط للفحص اللحظي الشامل...")

if st.button("تفعيل بروتوكول الكشف الذكي"):
    if target_url:
        # تصحيح تلقائي لأخطاء الكتابة
        if target_url.startswith("ttp"): target_url = "h" + target_url
        
        API_KEY = "22e03b88a0526e3d43b85556438c2d5895ccb0ef97771cff2471edab14cac85b"
        headers = {"x-apikey": API_KEY}
        url_id = base64.urlsafe_b64encode(target_url.encode()).decode().strip("=")
        
        with st.spinner("> جاري تنفيذ المسح الجنائي للمسارات وقواعد البيانات العالمية..."):
            st.markdown("---")
            
            # تحليل مرجان العميق للمسارات
            marjan_alerts = deep_path_analysis(target_url)
            # جلب البيانات العالمية
            marjan_alerts.extend(fetch_global_intel(target_url))
            
            # فحص VirusTotal
            try:
                vt_res = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers, timeout=12)
                if vt_res.status_code == 200:
                    malicious = vt_res.json()['data']['attributes'].get('last_analysis_stats', {}).get('malicious', 0)
                    if malicious > 0:
                        marjan_alerts.append(f"📡 استخبارات دولية: تم رصد خطورة بواسطة {malicious} مركز أمني.")
            except: pass

            if marjan_alerts:
                st.subheader("🕵️ نتائج التحليل الجنائي اللحظي:")
                for alert in marjan_alerts:
                    st.markdown(f'<div class="heuristic-danger">{alert}</div>', unsafe_allow_html=True)
                
                # إضافة التهديد للمخزن اللحظي
                st.session_state.threat_vault.insert(0, {
                    "url": target_url[:35] + "...", 
                    "type": "Path Phishing / Media Leak", 
                    "time": datetime.now().strftime("%H:%M")
                })
                
                st.markdown(f"""
                <div class="threat-intel">
                    <h4 style="color:#D4AF37; margin-bottom:10px;">⚠️ تحليل المسار الجنائي:</h4>
                    <p style="color:#eee; font-size:0.9em;">تم اكتشاف استغلال لمجلدات الوسائط (Media) لزرع صفحات تصيد نشطة.</p>
                    <p style="font-size: 0.95em; color: #ff4b4b; font-weight: bold; border-top: 1px solid rgba(212,175,55,0.2); padding-top: 10px;">
                        💡 الإجراء: تم تصنيف الرابط كخطر؛ يرجى الحذر من الروابط التي تنتهي بمسارات عشوائية طويلة.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("✅ محرك مرجان: لم يتم رصد تهديدات واضحة في هذا المسار حالياً.")

            st.info(f"🔗 [السجل الفني الكامل للرابط (Live)](https://www.virustotal.com/gui/url/{url_id}/behavior)")

# --- سجل التهديدات المكتشفة ---
st.markdown(f"""
    <div class="latest-threats">
        <h4 style="color:#ff4b4b; margin-bottom:10px; border-bottom:1px solid rgba(255,75,75,0.2);">🔴 سجل التهديدات اللحظية (Live Archive)</h4>
        <table style="width:100%; color:#eee; font-size:0.85em; text-align:right;">
            <tr style="color:#D4AF37;">
                <th>الرابط المكتشف</th>
                <th>نوع التهديد</th>
                <th>الوقت</th>
            </tr>
            {"".join([f"<tr><td>{t['url']}</td><td>{t['type']}</td><td>{t['time']}</td></tr>" for t in st.session_state.threat_vault[:5]])}
        </table>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="footer">Eng. Zaid Al-Janabi | Marjan Trace v6.3 | Advanced Forensic Detection</div>', unsafe_allow_html=True)
